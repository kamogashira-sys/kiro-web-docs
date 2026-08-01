#!/usr/bin/env python3
"""公式 Kiro Web changelog の HTML から一次情報を抽出する（作業計画書 Phase 2a-0）。

Kiro Web には**バージョン番号が存在しない**（F-W2: 索引の RSC は 7/7 が
`"version":"$undefined"`・`"patches":[]`）。したがって本スクリプトは版番号を扱わず、
**日付＋スラッグ**を正準キーとして扱う。

なぜ HTML の DOM ではなく RSC ペイロードを見るのか（F-W22）
----------------------------------------------------------------
changelog エントリの `Improvements` / `Fixes` は Radix UI のアコーディオンで、
レンダリング済み HTML では **`hidden` な空 div** になっている。`<article>` 内の
`<li>` を数えると **0 件**になり、公式が公開している項目（実測21項目）が
静かに落ちる。中身は RSC (React Server Components) の flight ペイロードにのみある。

flight ペイロードの取り出し方（実装の要点）
----------------------------------------------------------------
1. HTML 内の `self.__next_f.push([1,"<JSON文字列リテラル>"])` を全部集め、
   **JSON 文字列リテラルとして `json.loads` する**。これで「エスケープされた JSON」
   （`\\"key\\":\\"value\\"`）が素の JSON に戻る。
   → 正規表現でエスケープ JSON を直接相手にしない。素の JSON 前提の正規表現
     （`"patches"\\s*:\\s*\\[...\\]` 等）は 0 件になるという罠を、そもそも回避する。
2. 連結した flight は `<id>:<payload>` の行形式。各 payload は **JSON として妥当**
   （実測: 全8ファイルでパース成功）。
3. React 要素は `["$", tag, key, props]` の配列。子に `"$L24"` のような
   **別 row への遅延参照**が現れる。
   ⚠️ `start-without-a-repo-switch-modes-anytime` は **アコーディオン節が本文 row と
   別の row（`$L24`・`$L25`）にある**。本文 row だけを走査すると折りたたみ項目が
   **0 件**になる（実測）。
   → 対策を**二重**にしている: (a) **全 row を走査**する (b) **参照を解決**する。
     どちらか一方が公式側の変更で効かなくなっても項目を失わない。
     実測（`start-without-a-repo` で節数を計測）:
       本文 row のみ＋参照解決なし = **0** / 本文 row のみ＋解決あり = 2 /
       全 row＋解決なし = 2 / 全 row＋解決あり = 2（重複排除後）

節の境界について
----------------------------------------------------------------
アコーディオンは「節タイトル」と「子の `<ul>`」を持つ**1つの要素**なので、木構造を
たどれば境界は自明に決まる。文字列走査で `Improvements` 以降を切り出す実装にすると、
次の節（`Fixes`）の項目を飲み込む（実測で 5 → 11 件に膨らんだ）。木でたどることで
この問題を構造的に回避している。

fail-safe 設計（IDE 版から継承）
----------------------------------------------------------------
- **取得（読み込み）自体の失敗** → exit 0 ＋ 手動確認の案内（ネットワーク・
  ファイル欠落で CI を赤くしない）
- **読み込み成功かつ抽出0件** → **exit 1**（公式サイトの構造変化の疑い）

使い方
----------------------------------------------------------------
    extract-changelog.py --index <索引HTML>        # スラッグ・日付・タイトル
    extract-changelog.py --entry <エントリHTML>...  # 本文・粒度・折りたたみ項目
    extract-changelog.py --entry <...> --text       # 人が読む形式
"""

from __future__ import annotations

import argparse
import json
import re
import sys

# ------------------------------------------------------------
# 日付の正規化
# ------------------------------------------------------------
# 索引は略記（`Jul 1, 2026`）、エントリページは月名フル（`July 1, 2026`）で
# **表記が異なる**（F-W3: 索引 7/7 が略記・エントリ 7/7 が月名フル）。両方を扱う。
# ⚠️ May は略記と月名フルが同形。May だけを見て形式を判定してはいけない。
# ロケール依存を避けるため月名テーブルは自前で持つ（strptime を使わない）。
MONTHS = {
    "january": 1, "february": 2, "march": 3, "april": 4, "may": 5, "june": 6,
    "july": 7, "august": 8, "september": 9, "october": 10, "november": 11, "december": 12,
    "jan": 1, "feb": 2, "mar": 3, "apr": 4, "jun": 6,
    "jul": 7, "aug": 8, "sep": 9, "oct": 10, "nov": 11, "dec": 12,
}

DATE_RE = re.compile(
    r"\b(" + "|".join(sorted(MONTHS, key=len, reverse=True)) + r")\b\.?\s+(\d{1,2}),?\s+(\d{4})",
    re.IGNORECASE,
)


def normalize_date(text: str) -> str | None:
    """`Jul 1, 2026` / `July 1, 2026` → `2026-07-01`。タイムゾーン変換はしない。"""
    m = DATE_RE.search(text or "")
    if not m:
        return None
    month = MONTHS[m.group(1).lower()]
    return f"{int(m.group(3)):04d}-{month:02d}-{int(m.group(2)):02d}"


# ------------------------------------------------------------
# RSC flight ペイロードの復元
# ------------------------------------------------------------
PUSH_RE = re.compile(r'self\.__next_f\.push\(\[\s*\d+\s*,\s*("(?:[^"\\]|\\.)*")')
ROW_RE = re.compile(r"(?m)^([0-9a-zA-Z]+):(.*)$")


def load_flight(html: str) -> dict[str, object]:
    """HTML から flight を復元し、`{row_id: パース済み payload}` を返す。

    payload が JSON として妥当でない row（`I[9766,[],""]` のようなモジュール宣言）は
    そのまま生文字列で残す。要素の木をたどるときは無視される。
    """
    chunks = [json.loads(m.group(1)) for m in PUSH_RE.finditer(html)]
    flight = "".join(chunks)
    rows: dict[str, object] = {}
    for m in ROW_RE.finditer(flight):
        raw = m.group(2)
        try:
            rows[m.group(1)] = json.loads(raw)
        except (json.JSONDecodeError, ValueError):
            rows[m.group(1)] = raw
    return rows


def resolve(node, rows: dict[str, object], depth: int = 0):
    """`"$L24"` 形式の遅延参照を解決する。

    ⚠️ これが無いと `start-without-a-repo-switch-modes-anytime` の折りたたみ項目が
    0 件になる（節が本文 row とは別 row にある）。
    """
    if depth > 40:  # 参照ループ・異常な深さへの保険
        return node
    if isinstance(node, str):
        m = re.fullmatch(r"\$L([0-9a-zA-Z]+)", node)
        if m and m.group(1) in rows:
            return resolve(rows[m.group(1)], rows, depth + 1)
        return node
    if isinstance(node, list):
        return [resolve(x, rows, depth + 1) for x in node]
    if isinstance(node, dict):
        return {k: resolve(v, rows, depth + 1) for k, v in node.items()}
    return node


def is_element(node) -> bool:
    """React 要素 `["$", tag, key, props]` かどうか。"""
    return isinstance(node, list) and len(node) >= 4 and node[0] == "$"


def walk(node):
    """木の全ノードを深さ優先で列挙する。"""
    yield node
    if isinstance(node, list):
        for x in node:
            yield from walk(x)
    elif isinstance(node, dict):
        for v in node.values():
            yield from walk(v)


def node_text(node) -> str:
    """要素ノードから可読テキストを再帰的に集める。

    ⚠️ 単純な文字列抽出では `<strong>` の後続テキストが落ちる（実測で
    「Workspace progress indicator:」だけになり説明文が消えた）。子を順に
    たどって連結する。
    """
    out: list[str] = []

    def rec(n):
        if isinstance(n, str):
            if n.startswith("$"):  # "$undefined" 等のセンチネルは本文ではない
                return
            out.append(n)
        elif is_element(n):
            props = n[3]
            if isinstance(props, dict):
                rec(props.get("children"))
        elif isinstance(n, list):
            for x in n:
                rec(x)
        elif isinstance(n, dict):
            rec(n.get("children"))

    rec(node)
    return re.sub(r"\s+", " ", "".join(out)).strip()


# ------------------------------------------------------------
# 索引の抽出（スラッグ・日付・タイトル）
# ------------------------------------------------------------
def extract_index(html: str) -> list[dict]:
    """索引 HTML から Web エントリのメタを抽出する。

    `productLabel` が `Web` のものだけを採る（索引には他系列も載りうる）。
    ⚠️ `/changelog/web/page/N` は**エントリではない**ので除外する（F-W15: 他系列では
    既に page/2 以降が実在しており、Web でも増えれば出現する）。
    """
    rows = load_flight(html)
    entries: dict[str, dict] = {}

    for row in list(rows.values()):
        for node in walk(resolve(row, rows)):
            if not isinstance(node, dict):
                continue
            url = node.get("entryUrl")
            if not isinstance(url, str) or "/changelog/web/" not in url:
                continue
            slug = url.rstrip("/").rsplit("/", 1)[-1]
            if re.fullmatch(r"page/\d+|\d+", slug) or "/page/" in url:
                continue
            label = node.get("productLabel")
            if isinstance(label, str) and label != "Web":
                continue
            date = normalize_date(node.get("date") or "")
            title = _entry_title(node)
            prev = entries.get(slug, {})
            entries[slug] = {
                "slug": slug,
                "date": date or prev.get("date"),
                "title": title or prev.get("title"),
                # version は Web には存在しない（F-W2）。索引 RSC も "$undefined"。
                # 実値が入っていたら公式仕様の変化なので拾って報告する。
                "version": _real_version(node.get("version")) or prev.get("version"),
                "url": url,
            }

    return sorted(entries.values(), key=lambda e: (e["date"] or "", e["slug"]), reverse=True)


def _real_version(value) -> str | None:
    """`"$undefined"` 等のセンチネルを除いた実値の版番号だけを返す。"""
    if isinstance(value, str) and value and not value.startswith("$"):
        return value
    return None


def _entry_title(node: dict) -> str | None:
    """索引のエントリメタノードからタイトルを取る。

    ⚠️ タイトルはメタノードの `title` キーには**入っていない**（実測: キーは
    `date`・`version`・`productLabel`・`isAllPage`・`patches`・`entryUrl`・`children` のみ）。
    `children` 配下の `<h2>` にある。しかもリンクは素の `<a>` ではなく
    `$L26` 形式のクライアントコンポーネント参照なので、タグ名で `a` を探す実装では
    取れない（実測で 0 件になった）。→ `<h2>` を探す。
    """
    for child in walk(node.get("children")):
        if is_element(child) and child[1] == "h2" and isinstance(child[3], dict):
            text = node_text(child[3].get("children"))
            if text:
                return text
    return None


# ------------------------------------------------------------
# エントリ本文の抽出（粒度判定・折りたたみ項目）
# ------------------------------------------------------------
SCRIPT_RE = re.compile(r"(?s)<script.*?</script>")
# レンダリング済み HTML 側に残る Radix アコーディオンの痕跡。**節ごとに1個**現れる
# （実測: W-L3 の2エントリは 2 個・W-L2 の5エントリは 0 個・索引は 4 個）。
# 節の中身自体は hidden な空 div なので取り出せないが、「節がいくつあるか」は分かる。
ACCORDION_MARK_RE = re.compile(r"--radix-accordion-content-height")


def count_rendered_accordions(html: str) -> int:
    """レンダリング済み HTML から折りたたみ節の数を数える（RSC とは独立した情報源）。"""
    return len(ACCORDION_MARK_RE.findall(SCRIPT_RE.sub("", html)))


def extract_entry(html: str, slug: str | None = None) -> dict:
    """エントリ HTML から本文構造を抽出し、粒度（W-L2 / W-L3）を判定する。

    W-L2 = `<h2>` 節または導入文のみの機能紹介型
    W-L3 = `Improvements` / `Fixes` の折りたたみ節を持つ保守型（**節内の全項目**を返す）

    ⚠️ 節数は **RSC 側の抽出結果**と**レンダリング済み HTML 側のマーカー数**の
    2系統で数え、食い違ったら呼び出し側が失敗として扱えるようにする。
    RSC の形が変わって折りたたみが取れなくなると、粒度が黙って W-L2 に落ちて
    公式の項目が静かに消えるため（実測で `defaultOpen` を改名しただけで再現した）。
    """
    rows = load_flight(html)

    title = None
    date = None
    intro = None
    headings: list[str] = []
    blocks: list[dict] = []
    body_seen = False
    sections: list[dict] = []
    seen_sections: set[tuple[str, int]] = set()

    for row in list(rows.values()):
        tree = resolve(row, rows)
        for node in walk(tree):
            if not is_element(node):
                continue
            tag, props = node[1], node[3]
            if not isinstance(props, dict):
                continue

            # h1 = エントリタイトル
            if tag == "h1" and title is None:
                title = node_text(props.get("children")) or None

            # h2 = 節見出し（W-L2 の構造）
            if tag == "h2":
                text = node_text(props.get("children"))
                if text and text not in headings:
                    headings.append(text)

            # アコーディオン節: title + defaultOpen を持つ要素（F-W22）
            # ⚠️ 節は「タイトル」と「子の ul」を持つ1要素。木でたどるので境界は
            #    自明に決まる（文字列走査だと次の節の項目を飲み込む）。
            if "defaultOpen" in props and isinstance(props.get("title"), str):
                items = [
                    node_text(li[3].get("children"))
                    for li in walk(props.get("children"))
                    if is_element(li) and li[1] == "li" and isinstance(li[3], dict)
                ]
                items = [t for t in items if t]
                # 全 row を走査するうえ参照も解決するため、同じ節が複数経路で
                # 見つかる（本文 row 経由と参照先 row 直接）。**項目の内容まで含めて**
                # 重複排除する（タイトルと件数だけをキーにすると、同名・同数の
                # 別内容の節が片方消える）。
                key = (props["title"], tuple(items))
                if items and key not in seen_sections:
                    seen_sections.add(key)
                    sections.append({"title": props["title"], "count": len(items), "items": items})

            # 本文コンテナ: 直下は「見出し div」と「<p>」が交互に並ぶ平坦な並び。
            # 最初の <p> を導入文、以降を blocks（見出しと本文の対）として取る。
            # ⚠️ 全 row を走査するため本文コンテナは複数回見つかる。`not blocks` を
            #    ガードにすると、本文が「導入文 <p> のみ＋折りたたみ」のエントリ
            #    （blocks が空のまま終わる）で2回処理され、導入文が blocks に
            #    重複して入る（実測: session-stability で再現）。専用フラグで抑える。
            if tag == "div" and isinstance(props.get("className"), str) \
                    and "changelog prose" in props["className"] and not body_seen:
                body_seen = True
                children = props.get("children")
                seq = children if isinstance(children, list) else [children]
                for child in seq:
                    if not is_element(child) or not isinstance(child[3], dict):
                        continue
                    text = node_text(child[3].get("children"))
                    if not text:
                        continue
                    if child[1] == "p":
                        if intro is None:
                            intro = text
                        else:
                            blocks.append({"type": "p", "text": text})
                    elif child[1] in ("div", "h2", "h3"):
                        # 見出しは heading-anchor-wrapper div に包まれている
                        level = 2
                        for h in walk(child):
                            if is_element(h) and h[1] in ("h2", "h3"):
                                level = int(h[1][1])
                                break
                        blocks.append({"type": f"h{level}", "text": text})

    # 日付: エントリページは月名フル（F-W3）。本文コンテナ外の time/日付表示も拾う。
    for row in list(rows.values()):
        for node in walk(resolve(row, rows)):
            if isinstance(node, str):
                d = normalize_date(node)
                if d:
                    date = date or d
        if date:
            break

    rendered_sections = count_rendered_accordions(html)

    return {
        "slug": slug,
        "title": title,
        "date": date,
        "granularity": "W-L3" if sections else "W-L2",
        "intro": intro,
        "headings": headings,
        "blocks": blocks,
        "sections": sections,
        "item_total": sum(s["count"] for s in sections),
        # 交差検証用。RSC 抽出とレンダリング HTML で節数が一致するか
        "rendered_section_count": rendered_sections,
        "section_count_matches": len(sections) == rendered_sections,
    }


# ------------------------------------------------------------
# 出力
# ------------------------------------------------------------
def print_index_text(entries: list[dict]) -> None:
    print(f"=== 索引: {len(entries)} エントリ（新しい順） ===")
    for e in entries:
        ver = f" version={e['version']}" if e.get("version") else ""
        print(f"  {e['date'] or '????-??-??'}  {e['slug']}{ver}")
        if e.get("title"):
            print(f"      {e['title']}")


def print_entry_text(entry: dict) -> None:
    print(f"=== {entry['slug'] or entry['title']} ===")
    print(f"  日付       : {entry['date']}")
    print(f"  タイトル   : {entry['title']}")
    print(f"  粒度       : {entry['granularity']}")
    if entry["intro"]:
        print(f"  導入文     : {entry['intro'][:120]}{'…' if len(entry['intro']) > 120 else ''}")
    if entry["headings"]:
        print(f"  h2 見出し  : {len(entry['headings'])} 件")
        for h in entry["headings"]:
            print(f"      - {h}")
    if entry["blocks"]:
        print(f"  本文ブロック: {len(entry['blocks'])} 件")
        for b in entry["blocks"]:
            prefix = "  ## " if b["type"] == "h2" else ("  ### " if b["type"] == "h3" else "      ")
            print(f"    {prefix}{b['text']}")
    if entry["sections"]:
        print(f"  折りたたみ : {len(entry['sections'])} 節 / 計 {entry['item_total']} 項目")
        for s in entry["sections"]:
            print(f"      [{s['title']}] {s['count']} 件")
            for it in s["items"]:
                print(f"        - {it}")
    if not entry["section_count_matches"]:
        print(f"  ⚠️ 節数の不一致: RSC={len(entry['sections'])} / "
              f"レンダリング HTML={entry['rendered_section_count']}")


def main() -> int:
    p = argparse.ArgumentParser(
        description="公式 Kiro Web changelog HTML から一次情報を抽出する（RSC ペイロードを読む）",
    )
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--index", metavar="HTML", help="changelog/web/ 索引ページの HTML")
    g.add_argument("--entry", metavar="HTML", nargs="+", help="エントリページの HTML（複数可）")
    p.add_argument("--text", action="store_true", help="人が読む形式で出力する（既定は JSON）")
    args = p.parse_args()

    paths = [args.index] if args.index else args.entry
    loaded: list[tuple[str, str]] = []
    for path in paths:
        try:
            with open(path, encoding="utf-8") as fh:
                loaded.append((path, fh.read()))
        except OSError as exc:
            # fail-safe: 取得（読み込み）自体の失敗では落とさない
            print(f"⚠️  読み込めませんでした: {path}（{exc}）", file=sys.stderr)

    if not loaded:
        print("⚠️  一次情報 HTML を読み込めませんでした（未検証です）", file=sys.stderr)
        print("   取得手順: kiro-web-docs/05_meta/10_update-guide.md §5", file=sys.stderr)
        print("   URL は末尾スラッシュ必須・-A \"Mozilla/5.0\" が必要です", file=sys.stderr)
        return 0

    if args.index:
        path, html = loaded[0]
        entries = extract_index(html)
        if not entries:
            # 読み込みは成功したのに0件 → 構造変化の疑い（fail-safe の反対側）
            print(f"❌ {path}: エントリを1件も抽出できませんでした", file=sys.stderr)
            print("   公式サイトの構造が変わった可能性があります（RSC の形・"
                  "entryUrl / productLabel のキー名を確認してください）", file=sys.stderr)
            return 1
        if args.text:
            print_index_text(entries)
        else:
            print(json.dumps(entries, ensure_ascii=False, indent=2))
        return 0

    results = []
    failed = []
    mismatched = []
    for path, html in loaded:
        slug = re.sub(r"\.html?$", "", path.rsplit("/", 1)[-1])
        entry = extract_entry(html, slug=slug)
        # 本文が空なら抽出失敗として扱う（タイトルすら取れないのは構造変化）
        if not entry["title"] and not entry["intro"] and not entry["headings"] \
                and not entry["blocks"] and not entry["sections"]:
            failed.append(path)
        elif not entry["section_count_matches"]:
            mismatched.append((path, len(entry["sections"]), entry["rendered_section_count"]))
        results.append(entry)

    if failed:
        print("❌ 以下のエントリから本文を抽出できませんでした:", file=sys.stderr)
        for path in failed:
            print(f"     {path}", file=sys.stderr)
        print("   公式サイトの構造が変わった可能性があります"
              "（RSC の要素形・アコーディオンの props を確認してください）", file=sys.stderr)
        return 1

    if mismatched:
        # RSC 抽出とレンダリング HTML で節数が食い違う = 折りたたみ項目の取り逃しの疑い。
        # 粒度が黙って W-L2 に落ちると公式の項目が消えるため、必ず失敗させる。
        print("❌ 折りたたみ節の数が RSC とレンダリング HTML で一致しません:", file=sys.stderr)
        for path, rsc, rendered in mismatched:
            print(f"     {path}: RSC={rsc} / レンダリング HTML={rendered}", file=sys.stderr)
        print("   抽出漏れの疑いがあります（RSC のアコーディオン props が"
              "変わった可能性）。項目を落としたまま公開しないでください", file=sys.stderr)
        return 1

    if args.text:
        for entry in results:
            print_entry_text(entry)
            print()
    else:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
