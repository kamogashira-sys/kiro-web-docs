#!/usr/bin/env python3
"""Capture an auditable Kiro Web v2 primary-source snapshot.

The snapshot has explicit changelog index and entry boundaries.  Every request
is recorded in manifest.tsv, and a file is admitted to the snapshot only after
HTTP 2xx, non-empty content, and the persisted byte/hash values agree.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import html
import importlib.util
import json
import os
import re
import sys
import tempfile
import time
from datetime import datetime
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit, urlunsplit
from urllib.request import Request, build_opener
from zoneinfo import ZoneInfo

BASE = "https://kiro.dev"
UA = "Mozilla/5.0"
FIELDS = [
    "request_url", "final_url", "kind", "http_status", "content_type", "bytes",
    "sha256", "retrieved_at_jst", "save_path", "date_modified", "date_modified_status", "result", "error",
    "slug", "title", "index_url",
]
DATE_MODIFIED_RE = re.compile(r'\\?"dateModified\\?"\s*:\s*\\?"(\d{4}-\d{2}-\d{2})')
MISSING_DATE_MODIFIED_ALLOWLIST = {"https://kiro.dev/docs/web/memory/"}
# Shared 区分（更新手順書 §8.1）。**S2/S4 の Web 集合には入れない**。
# 本サイトが出典として引用しているため dateModified の照合対象にする。
SHARED_DOCS = {
    f"{BASE}/docs/privacy-and-security/data-protection/": "docs/shared_privacy-and-security_data-protection.html",
    f"{BASE}/docs/privacy-and-security/firewalls/": "docs/shared_privacy-and-security_firewalls.html",
}
# §8.3 のリンク先ページ（他サーフェス／全製品共通ページ）。Shared 区分とは別枠。
LINKED_DOCS = {
    f"{BASE}/docs/specs/": "docs/linked_specs.html",
    f"{BASE}/docs/steering/": "docs/linked_steering.html",
    f"{BASE}/docs/cloud-sessions/": "docs/linked_cloud-sessions.html",
}
# dateModified を必須とする kind。Web 集合以外も出典日照合に使うため抽出する。
DATE_MODIFIED_KINDS = {"web-doc", "shared-doc", "linked-doc"}
TITLE_RE = re.compile(r"(?is)<title[^>]*>\s*(.*?)\s*</title>")
PAGE_PATH_RE = re.compile(r"^/changelog/web/page/(\d+)/$")
ENTRY_PATH_RE = re.compile(r"^/changelog/web/([a-z0-9-]+)/$")


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def timestamp() -> str:
    return datetime.now(ZoneInfo("Asia/Tokyo")).isoformat(timespec="seconds")


def normal_url(url: str) -> str:
    """Normalize an official page URL while preserving the original request URL in manifest."""
    parts = urlsplit(url)
    path = parts.path
    if path.endswith(".md"):
        path = path[:-3]
    if not path.endswith("/") and not path.endswith((".xml", ".txt", ".atom")):
        path += "/"
    return urlunsplit((parts.scheme or "https", parts.netloc or "kiro.dev", path, "", ""))


def text_title(body: bytes) -> str:
    m = TITLE_RE.search(body.decode("utf-8", errors="replace"))
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", m.group(1)))).strip() if m else ""


def save_atomic(path: Path, body: bytes) -> tuple[int, str]:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp = tempfile.mkstemp(prefix=".capture-", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as fh:
            fh.write(body)
            fh.flush()
            os.fsync(fh.fileno())
        persisted = Path(temp).read_bytes()
        if persisted != body:
            raise OSError("保存後の本文が取得本文と一致しません")
        os.replace(temp, path)
        return len(persisted), hashlib.sha256(persisted).hexdigest()
    except Exception:
        try:
            os.unlink(temp)
        except FileNotFoundError:
            pass
        raise


class Capture:
    def __init__(self, root: Path, retries: int = 0, delay: float = 0.0):
        self.root = root
        self.records: list[dict[str, str]] = []
        self.opener = build_opener()
        # ⚠️ CI から公式サイトへ都度取得するために追加（2026-09-13）。
        #    retries: **一時障害のみ**再試行する。404 は何度試しても 404 なので
        #             再試行しない（存在しないものを待つ意味がない）。
        #    delay:   リクエスト間の待機。公式サイトへの負荷を抑える。
        self.retries = max(0, retries)
        self.delay = max(0.0, delay)
        self._requested = 0

    # 再試行する対象。HTTP 5xx と通信レベルの失敗のみ。
    RETRIABLE_STATUS = range(500, 600)

    def _fetch(self, request_url: str):
        """1 リクエストを実行する。一時障害なら指数バックオフで再試行する。"""
        last = None
        for attempt in range(self.retries + 1):
            if self._requested and self.delay:
                time.sleep(self.delay)
            self._requested += 1
            try:
                request = Request(request_url, headers={"User-Agent": UA})
                with self.opener.open(request, timeout=30) as response:
                    return (response.getcode(), response.geturl(),
                            response.headers.get_content_type(), response.read())
            except HTTPError as exc:
                last = exc
                if exc.code not in self.RETRIABLE_STATUS:
                    raise
            except (URLError, OSError) as exc:
                last = exc
            if attempt < self.retries:
                wait = self.delay + 2.0 * (2 ** attempt)
                print(f"   ↻ 再試行 {attempt + 1}/{self.retries}（{wait:.1f}s 待機）: "
                      f"{request_url} … {last}", file=sys.stderr)
                time.sleep(wait)
        raise last if last else ValueError("取得に失敗しました")

    def add(self, request_url: str, kind: str, relative_path: str, **extra: str) -> dict[str, str]:
        record = {key: "" for key in FIELDS}
        record.update({"request_url": request_url, "kind": kind, **extra})
        requested_at = timestamp()
        try:
            status, final_url, content_type, body = self._fetch(request_url)
            record.update({
                "final_url": final_url, "http_status": str(status),
                "content_type": content_type, "retrieved_at_jst": requested_at,
            })
            if not 200 <= status <= 299:
                raise ValueError(f"HTTP {status}")
            if not body:
                raise ValueError("空本文")
            save_path = self.root / relative_path
            size, digest = save_atomic(save_path, body)
            # Re-read the renamed file: the manifest must describe the actual snapshot.
            persisted = save_path.read_bytes()
            if len(persisted) != size or hashlib.sha256(persisted).hexdigest() != digest:
                raise ValueError("保存後の bytes または sha256 が一致しません")
            record.update({
                "bytes": str(size), "sha256": digest, "save_path": relative_path,
                "result": "success", "title": text_title(body),
            })
            if kind in DATE_MODIFIED_KINDS:
                date_match = DATE_MODIFIED_RE.search(body.decode("utf-8", errors="replace"))
                record["date_modified"] = date_match.group(1) if date_match else ""
                if record["date_modified"]:
                    record["date_modified_status"] = "verified"
                elif request_url in MISSING_DATE_MODIFIED_ALLOWLIST:
                    record.update({
                        "date_modified_status": "unverified-official-missing",
                        "error": "official page does not provide an ISO dateModified",
                    })
                else:
                    record.update({
                        "result": "failed", "date_modified_status": "missing-unapproved",
                        "error": "JSON-LD dateModified を抽出できません",
                    })
            if record["result"] == "failed":
                # Do not retain a required doc as a success artifact when required extraction failed.
                save_path.unlink(missing_ok=True)
                record.update({"save_path": "", "bytes": "", "sha256": ""})
        except HTTPError as exc:
            record.update({
                "final_url": exc.geturl() or "", "http_status": str(exc.code),
                "retrieved_at_jst": requested_at, "result": "failed", "error": f"HTTP {exc.code}",
            })
        except (URLError, OSError, ValueError) as exc:
            record.update({"retrieved_at_jst": requested_at, "result": "failed", "error": str(exc)})
        self.records.append(record)
        return record

    def write_manifest(self) -> None:
        path = self.root / "manifest.tsv"
        path.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", newline="", dir=path.parent,
                                         prefix=".manifest-", delete=False) as fh:
            writer = csv.DictWriter(fh, fieldnames=FIELDS, delimiter="\t", extrasaction="raise")
            writer.writeheader()
            writer.writerows(self.records)
            temp = fh.name
        os.replace(temp, path)


def extractor():
    path = Path(__file__).with_name("extract-changelog.py")
    spec = importlib.util.spec_from_file_location("extract_changelog", path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


def sitemap_urls(text: str) -> set[str]:
    return {normal_url(item) for item in re.findall(r"https://kiro\.dev/[^<\s]+", text)}


def page_filename(url: str) -> str:
    m = PAGE_PATH_RE.match(urlsplit(url).path)
    return f"changelog/indexes/_page-{m.group(1)}.html" if m else "changelog/indexes/_index.html"


def entry_filename(url: str) -> tuple[str, str]:
    m = ENTRY_PATH_RE.match(urlsplit(url).path)
    if not m:
        raise ValueError(f"changelog entry URL として認識できません: {url}")
    return m.group(1), f"changelog/entries/{m.group(1)}.html"


def doc_filename(url: str) -> str:
    path = urlsplit(url).path.strip("/").replace("/", "_") or "web"
    return f"docs/{path}.html"


def web_urls_from_llms(text: str) -> set[str]:
    section = re.search(r"(?ms)^## Web\s*$\n(.*?)(?=^## |\Z)", text)
    if not section:
        return set()
    return {normal_url(item) for item in re.findall(r"https://kiro\.dev/docs/web[^\s)>]*", section.group(1))}


def require_success(records: list[dict[str, str]], kinds: set[str]) -> list[str]:
    return [f"{r['kind']}: {r['request_url']} ({r['error'] or r['http_status']})"
            for r in records if r["kind"] in kinds and r["result"] != "success"]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--output", required=True, help="v2 snapshot root (new or empty directory)")
    # CI から公式サイトへ都度取得するための引数（2026-09-13 追加）。
    parser.add_argument("--retries", type=int, default=0,
                        help="一時障害（HTTP 5xx・通信エラー）の再試行回数（既定 0）")
    parser.add_argument("--delay", type=float, default=0.0,
                        help="リクエスト間の待機秒数（既定 0。CI では 0.5 を推奨）")
    args = parser.parse_args()
    root = Path(args.output).resolve()
    if root.exists() and any(root.iterdir()):
        print(f"❌ 出力先は新規または空でなければなりません: {root}", file=sys.stderr)
        return 2
    root.mkdir(parents=True, exist_ok=True)

    cap = Capture(root, retries=args.retries, delay=args.delay)
    sitemap = cap.add(f"{BASE}/sitemap.xml", "sitemap", "meta/sitemap.xml")
    llms = cap.add(f"{BASE}/llms.txt", "llms", "meta/llms.txt")
    cap.add(f"{BASE}/changelog/feed.atom", "feed", "meta/feed.atom")
    if sitemap["result"] != "success" or llms["result"] != "success":
        cap.write_manifest()
        print("❌ sitemap または llms.txt を取得できませんでした", file=sys.stderr)
        return 1

    site_urls = sitemap_urls((root / "meta/sitemap.xml").read_text(encoding="utf-8", errors="replace"))
    pages = {f"{BASE}/changelog/web/"}
    pages |= {url for url in site_urls if PAGE_PATH_RE.match(urlsplit(url).path)}
    index_entries: dict[str, dict] = {}
    ex = extractor()
    for page in sorted(pages, key=lambda u: (u != f"{BASE}/changelog/web/", u)):
        record = cap.add(page, "changelog-index", page_filename(page))
        if record["result"] != "success":
            continue
        try:
            parsed = ex.extract_index((root / record["save_path"]).read_text(encoding="utf-8"))
        except Exception as exc:
            record.update({"result": "failed", "error": f"索引抽出失敗: {exc}"})
            (root / record["save_path"]).unlink(missing_ok=True)
            record["save_path"] = record["bytes"] = record["sha256"] = ""
            continue
        if not parsed:
            record.update({"result": "failed", "error": "索引からエントリを抽出できません"})
            (root / record["save_path"]).unlink(missing_ok=True)
            record["save_path"] = record["bytes"] = record["sha256"] = ""
            continue
        for item in parsed:
            slug = item["slug"]
            existing = index_entries.get(slug)
            if existing and (existing["date"] != item["date"] or existing["title"] != item["title"]):
                record.update({"result": "failed", "error": f"slug {slug} の日付またはタイトルが索引間で不一致"})
                continue
            index_entries[slug] = {**item, "index_url": page}

    sitemap_entries = {entry_filename(url)[0] for url in site_urls if ENTRY_PATH_RE.match(urlsplit(url).path)}
    for slug, item in sorted(index_entries.items()):
        url = normal_url(item["url"])
        record = cap.add(url, "changelog-entry", entry_filename(url)[1], slug=slug,
                         title=item.get("title") or "", index_url=item["index_url"])
        if record["result"] != "success":
            continue
        try:
            entry = ex.extract_entry((root / record["save_path"]).read_text(encoding="utf-8"), slug=slug)
            if not entry["date"] or not entry["title"] or not entry["section_count_matches"]:
                raise ValueError("entry 日付/タイトル/折りたたみ節を完全抽出できません")
            if entry["date"] != item["date"] or entry["title"] != item["title"]:
                raise ValueError("entry と index の日付またはタイトルが不一致")
        except Exception as exc:
            record.update({"result": "failed", "error": f"entry 抽出失敗: {exc}"})
            (root / record["save_path"]).unlink(missing_ok=True)
            record["save_path"] = record["bytes"] = record["sha256"] = ""

    llms_text = (root / "meta/llms.txt").read_text(encoding="utf-8", errors="replace")
    web_urls = web_urls_from_llms(llms_text)
    for url in sorted(web_urls):
        cap.add(url, "web-doc", doc_filename(url))
    # These pages are intentionally outside the Web S2/S4 set (see SHARED_DOCS / LINKED_DOCS).
    for url, save_path in sorted(SHARED_DOCS.items()):
        cap.add(url, "shared-doc", save_path)
    for url, save_path in sorted(LINKED_DOCS.items()):
        cap.add(url, "linked-doc", save_path)

    success_entries = {r["slug"] for r in cap.records if r["kind"] == "changelog-entry" and r["result"] == "success"}
    success_docs = {r["request_url"] for r in cap.records if r["kind"] == "web-doc" and r["result"] == "success"}
    dates = {r["request_url"] for r in cap.records if r["kind"] == "web-doc" and r["date_modified_status"] == "verified"}
    unverified_dates = {r["request_url"] for r in cap.records
                        if r["kind"] == "web-doc" and r["date_modified_status"] == "unverified-official-missing"}
    summary = {
        "sitemap_entry_slugs": sorted(sitemap_entries),
        "index_entry_slugs": sorted(index_entries),
        "manifest_success_entry_slugs": sorted(success_entries),
        "llms_web_urls": sorted(web_urls),
        "manifest_success_web_urls": sorted(success_docs),
        "date_modified_urls": sorted(dates),
        "unverified_date_modified_urls": sorted(unverified_dates),
        "max_entry_date": max((item["date"] for item in index_entries.values() if item["date"]), default=None),
        # ⚠️ S4 は **Web docs 18 ページのみ**から算出する。Shared / §8.3 のページを混ぜてはいけない。
        "max_docs_date_modified": max((r["date_modified"] for r in cap.records if r["kind"] == "web-doc"), default=None),
        # 出典日照合（check-consistency.py）が使う。Web 集合の外にある引用先ページの実測日。
        "extra_doc_date_modified": {
            r["request_url"]: r["date_modified"]
            for r in sorted(cap.records, key=lambda x: x["request_url"])
            if r["kind"] in ("shared-doc", "linked-doc") and r["result"] == "success"
        },
    }
    (root / "meta").mkdir(exist_ok=True)
    (root / "meta/validation.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    cap.write_manifest()

    errors = require_success(cap.records, {"sitemap", "llms", "feed", "changelog-index", "changelog-entry", "web-doc", "shared-doc", "linked-doc"})
    if sitemap_entries != set(index_entries) or sitemap_entries != success_entries:
        errors.append("changelog の sitemap/index/manifest 成功 slug 集合が一致しません")
    if web_urls != success_docs or web_urls != (dates | unverified_dates):
        errors.append("Web docs の llms/manifest 成功/dateModified 状態 URL 集合が一致しません")
    if unverified_dates != MISSING_DATE_MODIFIED_ALLOWLIST:
        errors.append("dateModified の未検証例外 URL 集合が許可リストと一致しません")
    if errors:
        print("❌ v2 snapshot capture failed:", file=sys.stderr)
        for error in errors:
            print(f"   - {error}", file=sys.stderr)
        return 1
    print(f"✅ v2 snapshot captured: {root}")
    print(f"   changelog entries: {len(success_entries)} / docs: {len(success_docs)}")
    print(f"   latest changelog: {summary['max_entry_date']} / latest docs: {summary['max_docs_date_modified']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
