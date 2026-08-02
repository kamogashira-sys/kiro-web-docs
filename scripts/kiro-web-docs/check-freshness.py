#!/usr/bin/env python3
"""check-freshness.py - 新エントリ・docs 更新の検知（★外部サイトに依存）

使用方法:
    ./scripts/kiro-web-docs/check-freshness.py
    ./scripts/kiro-web-docs/check-freshness.py --offline <snapshot-dir>
        # ネットワークを使わず、取得済みスナップショットで検証する（テスト用）

⚠️ **本スクリプトは外部サイト（kiro.dev）にアクセスします。**
   ネットワーク障害・レート制限で失敗しうるため `make check-kiro-web-all` には
   **含めません**。手動または nightly で実行します。

IDE 版から**再設計**した理由:
    IDE 版は「版番号の3情報源の和集合」で新バージョンを検知する。Kiro Web には
    **版番号が存在しない**（F-W2）ため、検知の単位を**スラッグ**に置き換えた。
    さらに **フィードは Web エントリを 0 件しか返さない**（F-W4・配信対象かは未確認）
    ため、フィードに依存しない設計にしている。

検知の系統（D-W4）:
    主系統1: `sitemap.xml` の `changelog/web/` URL 差分 → 新エントリのスラッグ
    主系統2: `changelog/web/` 索引ページの実取得（RSC）→ 日付・タイトル
    補助:    Atom・RSS → `term="Web"` が観測できたら報告（主系統への昇格を検討する材料）

    ⚠️ **`/changelog/web/page/\\d+/` は新エントリとして扱わない**（F-W15）。
       現時点で 404 だが、同じサイトの他系列には既に実在するため、
       エントリが増えれば Web にも現れる。

検証内容:
    1. **新エントリの検知**: 公式のスラッグ集合 ⊆ 文書に記載済みか
    2. **S3（最新エントリ日付）**: 公式の最新日付が文書の記載と一致するか
    3. **S4（docs の最新更新日）**: 公式 docs の `dateModified` の最大値が
       文書の記載と一致するか（**F-W16 の対策**。changelog に出ない更新を拾う）
    4. **S2（docs ページ数）**: `llms.txt` の `## Web` 区分の件数が SSoT と一致するか
    5. **`page/\\d+` の出現**: Web 系列にページ送りが現れたら報告（検知系統の見直しが必要）

fail-safe 設計（IDE 版から継承）:
    - **取得の失敗（ネットワーク・HTTP エラー）→ exit 0 ＋ 手動確認の案内**
      （CI やネットワーク不調で赤くしない）
    - **取得は成功したが抽出0件 → exit 1**（公式サイトの構造変化の疑い）
    - 新エントリの発見自体は **exit 1**（対応が必要という意味）
"""
import argparse
import importlib.util
import json
import os
import re
import subprocess
import sys

DOC_ROOT = "kiro-web-docs"
DOC_CHANGELOG = f"{DOC_ROOT}/02_update/01_changelog.md"
DOC_LIMITS = f"{DOC_ROOT}/04_reference/04_limits.md"
DOC_STRUCTURE = f"{DOC_ROOT}/00_information/01_official-site-structure.md"

# SSoT（本スクリプトが守る分）
SSOT_S1 = 7            # changelog エントリ数
SSOT_S2 = 20           # docs Web ページ数
SSOT_S3 = "2026-07-01"  # 最新エントリ日付
SSOT_S4 = "2026-07-23"  # docs の最新更新日（JSON-LD dateModified の最大値）

BASE = "https://kiro.dev"
# ⚠️ 末尾スラッシュ必須（無しは 301・本文0バイト — F-W11）。
#    User-Agent は空文字の明示指定が 403 になるため必ず指定する。
UA = "Mozilla/5.0"
CURL = ["curl", "-sS", "--max-time", "30", "-A", UA]

# `changelog/web/` 配下の URL。page/N は除外する（F-W15）。
WEB_ENTRY_RE = re.compile(r"https://kiro\.dev/changelog/web/([a-z0-9\-]+)/?")
PAGE_RE = re.compile(r"/changelog/web/page/\d+")
# JSON-LD の dateModified（ISO 形式・F-W23）
DATE_MODIFIED_RE = re.compile(r'"dateModified"\s*:\s*"(\d{4}-\d{2}-\d{2})')


def repo_root():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))


def load_extractor():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "extract-changelog.py")
    spec = importlib.util.spec_from_file_location("extract_changelog", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class Fetcher:
    """オンライン取得とオフライン（スナップショット）を同じ形で扱う。"""

    def __init__(self, offline_dir=None):
        self.offline_dir = offline_dir
        self.failures = []

    def get(self, url, offline_name=None):
        if self.offline_dir:
            if not offline_name:
                return None
            path = os.path.join(self.offline_dir, offline_name)
            if not os.path.isfile(path):
                self.failures.append(f"{path}（スナップショットが無い）")
                return None
            return open(path, encoding="utf-8", errors="replace").read()
        try:
            r = subprocess.run(CURL + [url], capture_output=True, text=True, timeout=60)
        except (OSError, subprocess.SubprocessError) as exc:
            self.failures.append(f"{url}（{exc}）")
            return None
        if r.returncode != 0 or not r.stdout:
            self.failures.append(f"{url}（curl 終了コード {r.returncode}）")
            return None
        return r.stdout


def doc_slugs():
    """文書に記載済みのスラッグ（出典 URL から）を集める。"""
    if not os.path.isfile(DOC_CHANGELOG):
        return set()
    txt = open(DOC_CHANGELOG, encoding="utf-8").read()
    return set(re.findall(r"https://kiro\.dev/changelog/web/([a-z0-9\-]+)/", txt))


def doc_value(path, pattern):
    if not os.path.isfile(path):
        return None
    m = re.search(pattern, open(path, encoding="utf-8").read())
    return m.group(1) if m else None


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--offline", metavar="DIR",
                    help="スナップショットのディレクトリを使う（ネットワークを使わない）")
    args = ap.parse_args()
    os.chdir(repo_root())

    print("=== kiro-web-docs 新エントリ・docs 更新の検知 ===")
    if args.offline:
        print(f"（オフラインモード: {args.offline}）")
    print("")

    f = Fetcher(args.offline)
    errors, notes, warnings = [], [], []

    # ---- 主系統1: sitemap ----
    print("🔍 sitemap から changelog/web/ のスラッグを取得中...")
    sitemap = f.get(f"{BASE}/sitemap.xml", "meta/sitemap.xml")
    official_slugs = set()
    pages_found = []
    if sitemap:
        for m in WEB_ENTRY_RE.finditer(sitemap):
            official_slugs.add(m.group(1))
        pages_found = PAGE_RE.findall(sitemap)
        # page/N は WEB_ENTRY_RE では拾わないが、念のため除去する
        official_slugs = {s for s in official_slugs if not re.fullmatch(r"page", s)}

    # ---- 主系統2: 索引ページ ----
    print("🔍 changelog/web/ 索引から日付・タイトルを取得中...")
    index_html = f.get(f"{BASE}/changelog/web/", "changelog/_index.html")
    entries = []
    if index_html:
        ex = load_extractor()
        try:
            entries = ex.extract_index(index_html)
        except Exception as exc:  # 構造変化で例外になる場合も抽出失敗として扱う
            errors.append(f"索引の抽出で例外が発生しました: {exc}")

    # ---- 補助: フィード ----
    print("🔍 フィードの Web カテゴリを確認中（補助）...")
    # ⚠️ フィードの URL は `/changelog/feed.atom`。**`/feed.atom` は 404**（実測）。
    #    オフラインモード（スナップショット）では気づけないため、
    #    check-urls.sh の到達性チェックで発覚した。
    feed = f.get(f"{BASE}/changelog/feed.atom", "meta/feed.atom")
    feed_web = feed.count('term="Web"') if feed else None

    # ---- docs の更新日（S4）----
    print("🔍 docs の dateModified を取得中...")
    docs_dates = {}
    if args.offline:
        docs_dir = os.path.join(args.offline, "docs")
        if os.path.isdir(docs_dir):
            for name in sorted(os.listdir(docs_dir)):
                if not name.endswith(".html"):
                    continue
                html = open(os.path.join(docs_dir, name), encoding="utf-8",
                            errors="replace").read()
                m = DATE_MODIFIED_RE.search(html)
                if m:
                    docs_dates[name] = m.group(1)
        else:
            f.failures.append(f"{docs_dir}（docs スナップショットが無い）")
    else:
        # llms.txt から Web 区分のページ URL を取り、各ページの JSON-LD を見る
        llms = f.get(f"{BASE}/llms.txt", "meta/llms.txt")
        web_urls = []
        if llms:
            sec = re.split(r"(?m)^## ", llms)
            for s in sec:
                if s.startswith("Web"):
                    web_urls = [u for u in re.findall(r"\((https://kiro\.dev/docs/web[^)]*)\)", s)]
                    break
        for u in web_urls:
            page = u[:-3] + "/" if u.endswith(".md") else u
            html = f.get(page)
            if not html:
                continue
            m = DATE_MODIFIED_RE.search(html)
            if m:
                docs_dates[page] = m.group(1)

    # ---- fail-safe: 取得失敗 ----
    if f.failures and not official_slugs and not entries:
        print("")
        print("⚠️  一次情報を取得できませんでした（**未検証**です）")
        for x in f.failures[:5]:
            print(f"   - {x}")
        print("   ネットワークまたは公式サイト側の一時的な問題の可能性があります。")
        print("   手動確認の手順: kiro-web-docs/05_meta/10_update-guide.md §5")
        print("   （URL は末尾スラッシュ必須・-A \"Mozilla/5.0\" が必要）")
        return 0

    # ---- 取得は成功したが抽出0件 → 構造変化の疑い ----
    if sitemap and not official_slugs:
        errors.append("sitemap は取得できましたが changelog/web/ のエントリを"
                      "1件も抽出できませんでした（URL 構造の変化を疑ってください）")
    if index_html and not entries:
        errors.append("索引 HTML は取得できましたがエントリを1件も抽出できませんでした"
                      "（RSC 構造の変化を疑ってください）")

    # ---- 1. 新エントリの検知 ----
    known = doc_slugs()
    new_slugs = sorted(official_slugs - known)
    gone_slugs = sorted(known - official_slugs)
    for s in new_slugs:
        e = next((x for x in entries if x["slug"] == s), None)
        d = e["date"] if e else "日付不明"
        errors.append(f"🆕 新しい changelog エントリがあります: {d} / {s}"
                      f"（{BASE}/changelog/web/{s}/ — 文書に未記載）")
    for s in gone_slugs:
        warnings.append(f"文書にあるが公式 sitemap に無いスラッグ: {s}"
                        "（公式が削除した／URL が変わった可能性）")

    # ---- 2. S1・S3 ----
    if official_slugs:
        notes.append(f"公式のエントリ数: {len(official_slugs)}（SSoT S1 = {SSOT_S1}）")
        if len(official_slugs) != SSOT_S1:
            errors.append(f"エントリ数が {len(official_slugs)} で SSoT S1 ({SSOT_S1}) と"
                          "一致しません（SSoT と文書の更新が必要）")
    if entries:
        latest = max((e["date"] for e in entries if e["date"]), default=None)
        if latest:
            notes.append(f"公式の最新エントリ日付: {latest}（SSoT S3 = {SSOT_S3}）")
            if latest != SSOT_S3:
                errors.append(f"最新エントリ日付が {latest} で SSoT S3 ({SSOT_S3}) と"
                              "一致しません")

    # ---- 3. S4（docs の最新更新日）----
    if docs_dates:
        newest = max(docs_dates.values())
        newest_pages = [k for k, v in docs_dates.items() if v == newest]
        notes.append(f"docs の最新更新日: {newest}（SSoT S4 = {SSOT_S4}）"
                     f" / {len(docs_dates)} ページ確認")
        if newest != SSOT_S4:
            errors.append(
                f"docs の最新更新日が {newest} で SSoT S4 ({SSOT_S4}) と一致しません"
                f"（更新されたページ: {', '.join(newest_pages[:3])}）"
                "。**changelog に現れない docs 更新の可能性があります（F-W16）**"
            )
        # changelog の最新より新しい docs 更新の件数を報告（F-W16 の常時監視）
        newer = {k: v for k, v in docs_dates.items() if v > SSOT_S3}
        if newer:
            notes.append(
                f"最新 changelog エントリ（{SSOT_S3}）より新しい docs 更新: {len(newer)} 件"
            )

    # ---- 4. S2（docs ページ数）----
    if args.offline:
        n_docs = len(docs_dates)
    else:
        llms = f.get(f"{BASE}/llms.txt", "meta/llms.txt")
        n_docs = 0
        if llms:
            for s in re.split(r"(?m)^## ", llms):
                if s.startswith("Web"):
                    n_docs = len(re.findall(r"(?m)^\s*- \[", s))
                    break
    if n_docs:
        notes.append(f"docs Web ページ数: {n_docs}（SSoT S2 = {SSOT_S2}）")
        if n_docs != SSOT_S2:
            errors.append(f"docs Web ページ数が {n_docs} で SSoT S2 ({SSOT_S2}) と"
                          "一致しません（新規ページの追加／削除の可能性）")

    # ---- 5. page/N の出現 ----
    if pages_found:
        errors.append(
            f"⚠️ `changelog/web/page/N` が sitemap に出現しました（{len(pages_found)} 件）。"
            "エントリが1ページに収まらなくなったため、**索引の全ページを巡回する実装に"
            "変更する必要があります**（F-W15）"
        )
    elif sitemap:
        notes.append("`changelog/web/page/N` は未出現（従来どおり索引1ページで全量取得可）")

    # ---- 補助: フィード ----
    if feed_web is not None:
        notes.append(f"フィードの `term=\"Web\"`: {feed_web} 件"
                     + ("（従来どおり 0 件。フィードは補助のまま）" if feed_web == 0
                        else " → **主系統への昇格を検討できます**"))

    # ---- 出力 ----
    print("")
    print("=== チェック結果 ===")
    for n in notes:
        print(f"   - {n}")
    if f.failures:
        print("")
        print(f"⚠️  一部の取得に失敗しました（{len(f.failures)} 件）:")
        for x in f.failures[:5]:
            print(f"   - {x}")
    if warnings:
        print("")
        print(f"⚠️  警告 {len(warnings)} 件:")
        for w in warnings:
            print(f"   - {w}")
    print("")

    if errors:
        print(f"❌ 対応が必要な事項 {len(errors)} 件:")
        for e in errors:
            print(f"   - {e}")
        print("")
        print("❌ 更新の追随が必要です（手順: kiro-web-docs/05_meta/10_update-guide.md §5）")
        return 1

    print("✅ 新しいエントリ・docs 更新はありません（SSoT と一致）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
