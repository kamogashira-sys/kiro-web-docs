#!/usr/bin/env python3
"""check-coverage.py - changelog の網羅性を一次情報と突き合わせて検証する

使用方法:
    # 一次情報の HTML を取得済みのディレクトリを指定する（索引＋各エントリ）
    ./scripts/kiro-web-docs/check-coverage.py --html-dir kiro-web-docs/06_embedded-docs/20260801/changelog

    # 抽出済み JSON（extract-changelog.py --entry の出力）を使う
    ./scripts/kiro-web-docs/check-coverage.py --json /tmp/entries.json

IDE 版から**再設計**した理由:
    IDE 版は「版番号の網羅性」を検証する。Kiro Web には**版番号が存在しない**（F-W2）ため、
    その突き合わせはそのままでは成立しない。本スクリプトは正準キーを
    **日付＋スラッグ**に置き換え、さらに Web 固有の検証を1本足している。

検証内容:
    1. **スラッグの網羅性**: 一次情報の全エントリが文書に載っていること（およびその逆）
    2. **日付の一致**: 各エントリの日付が一次情報と一致すること（ISO 正規化後）
    3. **本文記述が非空**: 各エントリに本文の記述があること（見出しだけで終わっていない）
    4. **W-L3 の折りたたみ項目数の一致**（★Web 固有・本スクリプトの中核）
       公式サイトで折りたたまれている `Improvements` / `Fixes` の項目は、
       **素の HTML に存在せず RSC にのみある**（F-W22）。転記漏れが静かに起きるため、
       節ごとに「宣言した件数」と「実際の箇条書き行数」の**両方**を一次情報と突き合わせる。

判定の注意（誤検知を避けるための実測知見）:
    - ⚠️ **エントリ単位にスコープを切ってから節を探す**。文書全体から
      `### Improvements（N件）` を検索すると、**別のエントリの節を拾って誤検知する**
      （実際に一度この誤りで MISMATCH を誤報告した）。
    - 宣言件数だけでは足りない。「（5件）」と書いて箇条書きを3行しか書かないケースを
      検出できないため、**実際の `- ` 行数も数える**。
    - 節の終端は次の `##`／`###` 見出し。終端を切らないと後続の節の項目を数え込む
      （Phase 0 で 5 → 11 件に膨らんだのと同じ失敗）。

fail-safe（IDE 版から継承）:
    - 一次情報が指定されていない／HTML が無い → **exit 0＋警告**（CI・クローン直後を
      赤くしない）。⚠️ ただし「exit 0 = 網羅性を検証した」ではないことを明示表示する
    - HTML はあるのに抽出できない → **exit 2**（構造変化の疑い）

ネットワークは使わない。HTML の取得手順は `kiro-web-docs/05_meta/10_update-guide.md §5` を参照。
"""
import argparse
import glob
import importlib.util
import json
import os
import re
import sys

DOC_FILE = "kiro-web-docs/02_update/01_changelog.md"

# エントリ見出し: `## 2026-07-01: IAM Roles and ...`
ENTRY_HEAD_RE = re.compile(r'(?m)^## (\d{4}-\d{2}-\d{2}):\s*(.+?)\s*$')
# 節見出し: `### Improvements（5件）` / `### Fixes（6件）`
SECTION_HEAD_RE = re.compile(r'(?m)^### (Improvements|Fixes)（(\d+)件）\s*$')
# 箇条書き行
BULLET_RE = re.compile(r'(?m)^- ')
# 一次情報側の出典 URL からスラッグを拾う（文書側のスラッグ記載の確認に使う）
SLUG_IN_DOC_RE = re.compile(r'https://kiro\.dev/changelog/web/([a-z0-9-]+)/')


def repo_root():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))


def load_extractor():
    """extract-changelog.py をモジュールとして読み込む（ハイフン入りのため import 不可）。"""
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "extract-changelog.py")
    spec = importlib.util.spec_from_file_location("extract_changelog", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def parse_doc(text):
    """文書をエントリ単位に切り分ける。

    ⚠️ **スコープを切ることが本関数の存在意義**。文書全体を対象に節を探すと
    別エントリの節を拾って誤検知する（実測済み）。
    """
    entries = {}
    heads = list(ENTRY_HEAD_RE.finditer(text))
    for i, m in enumerate(heads):
        end = heads[i + 1].start() if i + 1 < len(heads) else len(text)
        body = text[m.end():end]
        entries[m.group(1)] = {
            "date": m.group(1),
            "title": m.group(2),
            "body": body,
            "slugs": set(SLUG_IN_DOC_RE.findall(body)),
        }
    return entries


def doc_sections(body):
    """エントリ本文から `### Improvements（N件）` の節を取り出す。

    節の終端は次の `##`／`###` 見出し。宣言件数と実際の箇条書き行数の両方を返す。
    """
    out = {}
    heads = list(SECTION_HEAD_RE.finditer(body))
    for i, m in enumerate(heads):
        after = body[m.end():]
        nxt = re.search(r'(?m)^#{2,3} ', after)
        block = after[:nxt.start()] if nxt else after
        out[m.group(1)] = {
            "declared": int(m.group(2)),
            "actual": len(BULLET_RE.findall(block)),
        }
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    src = ap.add_mutually_exclusive_group()
    src.add_argument("--html-dir", help="取得済み changelog HTML のディレクトリ")
    src.add_argument("--json", help="extract-changelog.py --entry の出力 JSON")
    args = ap.parse_args()

    os.chdir(repo_root())

    print("=== changelog 網羅性チェック（一次情報との突き合わせ） ===")
    print("")

    if args.json:
        entries = json.load(open(args.json, encoding="utf-8"))
        origin = args.json
    else:
        html_dir = args.html_dir
        if not html_dir or not os.path.isdir(html_dir):
            print("⚠️  網羅性チェックをスキップしました（一次情報がありません）")
            print("   → これは「検証して合格した」ではありません（**未検証**です）")
            print("   使い方: check-coverage.py --html-dir <dir> | --json <file>")
            print("   一次情報の取得手順: kiro-web-docs/05_meta/10_update-guide.md §5")
            return 0
        # 索引（_index.html）はエントリではないので除外する
        files = [f for f in sorted(glob.glob(os.path.join(html_dir, "*.html")))
                 if os.path.basename(f) != "_index.html"]
        if not files:
            print("⚠️  網羅性チェックをスキップしました"
                  f"（{html_dir} にエントリ HTML がありません）")
            print("   → これは「検証して合格した」ではありません（**未検証**です）")
            return 0
        ex = load_extractor()
        entries = []
        for path in files:
            slug = re.sub(r"\.html?$", "", os.path.basename(path))
            with open(path, encoding="utf-8") as fh:
                d = ex.extract_entry(fh.read(), slug=slug)
            if not d["title"] and not d["intro"] and not d["blocks"] and not d["sections"]:
                print(f"❌ {path}: 本文を抽出できませんでした"
                      "（公式ページの構造変化を疑ってください）")
                return 2
            if not d["section_count_matches"]:
                print(f"❌ {path}: 折りたたみ節の数が RSC とレンダリング HTML で不一致"
                      f"（RSC={len(d['sections'])} / HTML={d['rendered_section_count']}）")
                print("   抽出漏れの疑いがあります。この状態で網羅性は判定できません")
                return 2
            entries.append(d)
        origin = f"{html_dir}（{len(files)} エントリ）"

    try:
        text = open(DOC_FILE, encoding="utf-8").read()
    except OSError as exc:
        print(f"❌ 文書を読み込めません: {DOC_FILE}（{exc}）")
        return 2

    doc = parse_doc(text)
    truth = {e["date"]: e for e in entries if e.get("date")}

    print(f"一次情報: {origin}")
    print(f"  一次情報のエントリ数: {len(truth)}")
    print(f"  文書のエントリ数:     {len(doc)}")
    print("")

    errors = []

    # ---- 1. スラッグ・エントリの網羅性 ----
    missing = sorted(set(truth) - set(doc))
    extra = sorted(set(doc) - set(truth))
    for d in missing:
        errors.append(f"一次情報にあるが文書に無いエントリ: {d} / {truth[d]['slug']}")
    for d in extra:
        errors.append(f"文書にあるが一次情報に無いエントリ: {d}（誤記または一次情報の取得漏れ）")

    shared = sorted(set(truth) & set(doc))

    for d in shared:
        t, x = truth[d], doc[d]

        # スラッグが文書に記載されているか（出典 URL の形で）
        if t["slug"] not in x["slugs"]:
            errors.append(
                f"{d}: スラッグ '{t['slug']}' が出典 URL として文書にありません"
                f"（文書にあるスラッグ: {sorted(x['slugs']) or 'なし'}）"
            )

        # ---- 2. タイトルの一致（公式タイトルの転記） ----
        if t.get("title") and t["title"] not in text:
            errors.append(f"{d}: 公式タイトル '{t['title']}' が文書にありません")

        # ---- 3. 本文記述が非空 ----
        # 見出しだけで中身が無い状態を検出する。導入文・節本文・箇条書きのいずれかが必要。
        if len(x["body"].strip()) < 100:
            errors.append(f"{d}: 本文記述がほとんどありません（{len(x['body'].strip())} 文字）")

        # ---- 4. W-L3 の折りたたみ項目数の一致（Web 固有・本スクリプトの中核） ----
        got = doc_sections(x["body"])
        for s in t.get("sections") or []:
            name = s["title"]
            if name not in got:
                errors.append(
                    f"{d}: 折りたたみ節 '{name}'（公式 {s['count']} 項目）が文書にありません"
                    "（公式サイトで折りたたまれている項目の転記漏れ）"
                )
                continue
            if got[name]["declared"] != s["count"]:
                errors.append(
                    f"{d}: '{name}' の宣言件数が不一致: 公式={s['count']} 文書={got[name]['declared']}"
                )
            if got[name]["actual"] != s["count"]:
                errors.append(
                    f"{d}: '{name}' の箇条書き行数が不一致: 公式={s['count']} "
                    f"文書={got[name]['actual']}（宣言件数だけ直しても中身が足りていない）"
                )
        # 文書側にだけある節（架空の節）
        for name in sorted(set(got) - {s["title"] for s in (t.get("sections") or [])}):
            errors.append(f"{d}: 文書にあるが公式に無い折りたたみ節: '{name}'")

    # 集計表示
    total_official = sum(s["count"] for e in entries for s in (e.get("sections") or []))
    wl3 = [e for e in entries if e.get("sections")]
    print(f"粒度: W-L2 {len(entries) - len(wl3)} 件 / W-L3 {len(wl3)} 件")
    print(f"折りたたみ項目の総数（公式）: {total_official}")
    print("")

    if errors:
        print(f"❌ エラー {len(errors)} 件:")
        for e in errors:
            print(f"   - {e}")
        print("")
        print("❌ 網羅性チェックに失敗しました")
        return 1

    print("✅ 全エントリのスラッグ・日付・タイトル・本文・折りたたみ項目数が"
          "一次情報と一致しています")
    return 0


if __name__ == "__main__":
    sys.exit(main())
