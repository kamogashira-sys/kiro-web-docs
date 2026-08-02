#!/usr/bin/env python3
"""check-counts.py - kiro-web-docs 件数整合チェック（正準値の水平展開）

使用方法:
    ./scripts/kiro-web-docs/check-counts.py
    ./scripts/kiro-web-docs/check-counts.py --html-dir kiro-web-docs/06_embedded-docs/20260801/docs
        # 一次情報 HTML があれば、正準値が公式の実体と一致するかも検証する

目的:
    「表を1行増やしたのに見出しや本文の件数を直し忘れた」を機械的に落とす。
    **表・コードブロック（実体）から数え**、それを文書中の件数記述と突き合わせる。

検証する正準値（作業計画書 D-W7 の件数系）:
    S1  changelog エントリ数              = 7
    S2  docs Web ページ数                 = 20
    S5  Common dependencies 許可ドメイン数 = 73
    S6  firewalls の URL/ドメイン表の行数  = 34
    S7  GitLab 送信元 IP 数               = 3
    S12 cross-region inference 対応リージョン数 = 3

3方向から突き合わせる:
    (a) 節見出しの `（N 行）` / `（N 件）` が、**その節の最初の表**の実行数と一致するか
    (b) 内訳表の各行と合計行が、対応する節の実行数と一致するか
    (c) SSoT 定数が、文書内の実体および（HTML があれば）公式の実体と一致するか

⚠️ 実装上の注意（Phase 2a の教訓）:
    - **必ず節単位にスコープを切ってから照合する。** 文書全体を対象に
      「（N 件）」を探すと別の節の数値を拾って誤検知する（check-coverage.py で
      実際に MISMATCH を誤報告した）。
    - 「N 件」「N 行」は日本語の一般的な助数詞なので、**全件を機械判定すると
      部分集合の記述を誤検出する**。本スクリプトは
      **「節見出しに宣言された件数」と「その節の実体」**に限定して照合する。
    - 1つの節に表が複数ある場合（例: プレースホルダの説明表）は
      **最初の表**を実体とみなす。

fail-safe:
    - 一次情報 HTML が無い場合、(c) の公式との照合はスキップして **exit 0**。
      ただし「未検証です」と明示表示する（IDE 版から継承）。
"""
import argparse
import glob
import html as html_mod
import os
import re
import sys

DOC_ROOT = "kiro-web-docs"

# ローカル管理（GitHub 非公開）。走査対象から除く。
LOCAL_ONLY = ("05_meta", "06_embedded-docs", "work_plans", "work_records")

# ------------------------------------------------------------
# SSoT（正準値）— 件数系。値の出典は kiro-web-docs/05_meta/10_update-guide.md §7
# ------------------------------------------------------------
SSOT = {
    "S1": {"value": 7, "label": "changelog エントリ数",
           "doc": f"{DOC_ROOT}/02_update/01_changelog.md"},
    "S2": {"value": 20, "label": "docs Web ページ数",
           "doc": f"{DOC_ROOT}/00_information/01_official-site-structure.md"},
    "S5": {"value": 73, "label": "Common dependencies 許可ドメイン数",
           "doc": f"{DOC_ROOT}/04_reference/01_allowed-domains.md"},
    "S6": {"value": 34, "label": "firewalls の URL/ドメイン表の行数",
           "doc": f"{DOC_ROOT}/04_reference/01_allowed-domains.md"},
    "S7": {"value": 3, "label": "GitLab 送信元 IP 数",
           "doc": f"{DOC_ROOT}/04_reference/01_allowed-domains.md"},
    "S12": {"value": 3, "label": "cross-region inference 対応リージョン数",
            "doc": f"{DOC_ROOT}/04_reference/04_limits.md"},
}

SEP_RE = re.compile(r"^\s*\|[\s:\-|]+\|\s*$")
HEAD_RE = re.compile(r"^(#{2,4})\s+(.*?)\s*$")
# 節見出しに宣言された件数: 「（15 行）」「（6 件・上記の代替）」「（5 種類）」
DECLARED_RE = re.compile(r"[（(]\s*(\d+)\s*(行|件|種類|ドメイン|項目)")
# IPv4 アドレス
IPV4_RE = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")


def repo_root():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))


def is_local_only(path):
    norm = path.replace(os.sep, "/")
    return any(f"/{lo}/" in norm or norm.startswith(f"{lo}/") for lo in LOCAL_ONLY)


def parse_sections(path):
    """Markdown を節単位に切り分ける。

    返り値: [{"level", "title", "line", "declared", "tables": [行数...],
              "code_blocks": [本文...], "body": 本文}]
    ⚠️ 節スコープを切ることが本関数の存在意義（文書全体を対象にすると誤検知する）。
    """
    lines = open(path, encoding="utf-8").read().split("\n")
    sections = []
    cur = {"level": 0, "title": "(冒頭)", "line": 1, "declared": None,
           "tables": [], "code_blocks": [], "body": []}
    in_fence = False
    fence_buf = None
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.strip().startswith("```"):
            if in_fence:
                cur["code_blocks"].append("\n".join(fence_buf))
                fence_buf = None
                in_fence = False
            else:
                in_fence = True
                fence_buf = []
            i += 1
            continue
        if in_fence:
            fence_buf.append(line)
            i += 1
            continue

        m = HEAD_RE.match(line)
        if m:
            sections.append(cur)
            d = DECLARED_RE.search(m.group(2))
            cur = {"level": len(m.group(1)), "title": m.group(2).strip(), "line": i + 1,
                   "declared": (int(d.group(1)), d.group(2)) if d else None,
                   "tables": [], "code_blocks": [], "body": []}
            i += 1
            continue

        # 表の検出（ヘッダ行 + 区切り行 + データ行）
        if line.strip().startswith("|") and i + 1 < len(lines) and SEP_RE.match(lines[i + 1]):
            j = i + 2
            n = 0
            while j < len(lines) and lines[j].strip().startswith("|"):
                n += 1
                j += 1
            cur["tables"].append(n)
            cur["body"].extend(lines[i:j])
            i = j
            continue

        cur["body"].append(line)
        i += 1

    if in_fence and fence_buf:
        cur["code_blocks"].append("\n".join(fence_buf))
    sections.append(cur)
    for s in sections:
        s["body"] = "\n".join(s["body"])
    return sections


def count_domains(text):
    """コードブロックからドメインらしいトークンを数える（S5 用）。"""
    toks = re.findall(r"[a-z0-9][a-z0-9.\-]*\.[a-z]{2,}", text)
    return len(set(toks)), len(toks)


# ------------------------------------------------------------
# (a) 節見出しの宣言件数 vs その節の実体
# ------------------------------------------------------------
def check_declared(errors, checked):
    docs = sorted(glob.glob(f"{DOC_ROOT}/**/*.md", recursive=True))
    docs = [d for d in docs if not is_local_only(d)]
    for path in docs:
        for sec in parse_sections(path):
            if not sec["declared"]:
                continue
            declared, unit = sec["declared"]
            # 実体の候補: 節の最初の表の行数。表が無ければコードブロックのトークン数。
            if sec["tables"]:
                actual = sec["tables"][0]
                kind = "表の行数"
                # ⚠️ 1行のセルに `<br>` で複数項目を並べた表がある
                #    （例: 対応リージョン3件を1行にまとめた表）。行数で数えると
                #    「宣言3 vs 実体1」と誤検知するため、**セル内の <br> 区切りの
                #    項目数**を実体とみなす。
                #
                #    ⚠️ この救済は **`<br>` が実在する表に限る**。条件を
                #    「宣言と一致したら採用」にすると、`<br>` が無い表でも
                #    br_max=1 が宣言1と一致してしまい、**1行の表の規則が常に
                #    通ってしまう**（実装当初これで NT-30 の狙った規則が
                #    発火しなかった）。
                if actual != declared and re.search(r"<br\s*/?>", sec["body"]):
                    br_max = max(
                        (len(re.split(r"<br\s*/?>", cell)) for row in
                         re.findall(r"(?m)^\|(.*)\|\s*$", sec["body"])
                         for cell in row.split("|")),
                        default=1,
                    )
                    if br_max > 1:
                        actual = br_max
                        kind = "セル内の <br> 区切り項目数"
            elif sec["code_blocks"]:
                uniq, _ = count_domains("\n".join(sec["code_blocks"]))
                actual = uniq
                kind = "コードブロックのドメイン数"
            else:
                continue  # 実体が無い節（説明だけの見出し）は対象外
            checked.append((path, sec["line"], sec["title"], declared, actual))
            if declared != actual:
                errors.append(
                    f"{path}:{sec['line']} 節「{sec['title']}」の宣言 {declared}{unit} が"
                    f"{kind} {actual} と一致しません"
                )


# ------------------------------------------------------------
# (b) 内訳表と合計
# ------------------------------------------------------------
def check_breakdown(errors, notes):
    """`01_allowed-domains.md` の内訳表（各グループの行数 → 合計）を検証する。

    内訳表の各行が、対応する節の実表の行数と一致し、かつ合計が S6 と一致すること。
    """
    path = f"{DOC_ROOT}/04_reference/01_allowed-domains.md"
    if not os.path.isfile(path):
        return
    sections = parse_sections(path)
    # グループ節（`### 1-1. ...（2 行）`）の実表行数を集める
    group_actual = {}
    for sec in sections:
        m = re.match(r"(1-\d)\.", sec["title"])
        if m and sec["tables"]:
            group_actual[m.group(1)] = sec["tables"][0]

    # 内訳表を含む節を探す
    bd = next((s for s in sections if "内訳" in s["title"]), None)
    if not bd:
        errors.append(f"{path}: 行数の内訳表が見つかりません（S6 の根拠が示せない）")
        return

    # ⚠️ 数値セルは `| **34** |` のように強調されていることがある。
    #    `\d+` だけを見る正規表現では合計行を取り落とす（実装当初これで
    #    「合計行がありません」と誤検知した）。強調記号を許容する。
    rows = re.findall(r"(?m)^\|\s*([^|]+?)\s*\|\s*\**\s*(\d+)\s*\**\s*\|", bd["body"])
    total_declared = None
    subtotal = 0
    for label, num in rows:
        num = int(num)
        if "合計" in label:
            total_declared = num
            continue
        subtotal += num
        m = re.match(r"(1-\d)\.", label.strip())
        if m and m.group(1) in group_actual:
            if group_actual[m.group(1)] != num:
                errors.append(
                    f"{path}: 内訳表の「{label.strip()}」が {num} ですが、"
                    f"当該節の表は {group_actual[m.group(1)]} 行です"
                )
    if total_declared is None:
        errors.append(f"{path}: 内訳表に合計行がありません")
    else:
        if subtotal != total_declared:
            errors.append(
                f"{path}: 内訳表の合計が {total_declared} ですが、各行の和は {subtotal} です"
            )
        if total_declared != SSOT["S6"]["value"]:
            errors.append(
                f"{path}: 内訳表の合計 {total_declared} が SSoT S6 "
                f"({SSOT['S6']['value']}) と一致しません"
            )
        notes.append(f"S6: 内訳の和 {subtotal} = 合計行 {total_declared} = SSoT "
                     f"{SSOT['S6']['value']}")


# ------------------------------------------------------------
# (c) SSoT 定数 vs 文書内の実体
# ------------------------------------------------------------
def check_ssot_in_docs(errors, notes):
    # S5: 許可ドメインのコードブロック
    path = SSOT["S5"]["doc"]
    if os.path.isfile(path):
        found = False
        for sec in parse_sections(path):
            if "サンドボックスの依存関係取得先" in sec["title"] or "Common dependencies" in sec["title"]:
                for cb in sec["code_blocks"]:
                    uniq, total = count_domains(cb)
                    if uniq < 10:
                        continue
                    found = True
                    if uniq != SSOT["S5"]["value"]:
                        errors.append(
                            f"{path}: 許可ドメインのコードブロックが {uniq} 件"
                            f"（重複除去前 {total}）ですが SSoT S5 は {SSOT['S5']['value']} です"
                        )
                    if total != uniq:
                        errors.append(
                            f"{path}: 許可ドメインのコードブロックに重複があります"
                            f"（{total} → 重複除去後 {uniq}）"
                        )
                    notes.append(f"S5: コードブロックのドメイン {uniq} 件")
        if not found:
            errors.append(f"{path}: 許可ドメインのコードブロックが見つかりません（S5 の根拠なし）")

    # S7: GitLab 送信元 IP（表の中の IPv4 を数える）
    path = SSOT["S7"]["doc"]
    if os.path.isfile(path):
        ips = set()
        for sec in parse_sections(path):
            if "GitLab" in sec["title"]:
                ips |= set(IPV4_RE.findall(sec["body"]))
        if not ips:
            errors.append(f"{path}: GitLab 送信元 IP が見つかりません（S7 の根拠なし）")
        elif len(ips) != SSOT["S7"]["value"]:
            errors.append(
                f"{path}: GitLab 送信元 IP が {len(ips)} 件ですが SSoT S7 は "
                f"{SSOT['S7']['value']} です"
            )
        else:
            notes.append(f"S7: GitLab 送信元 IP {len(ips)} 件")

    # S12: cross-region inference の対応リージョン数
    # 推論リージョンは `us-east-1` のようなリージョンコードで書かれている。
    # ⚠️ 節スコープを切る。文書全体を対象にすると、保存リージョン（1件）や
    #    Identity Center の提供リージョンの記述を数え込む。
    path = SSOT["S12"]["doc"]
    if os.path.isfile(path):
        found = False
        for sec in parse_sections(path):
            if "推論の処理先" in sec["title"] or "対応リージョン" in sec["title"]:
                regions = set(re.findall(r"\b(us-(?:east|west)-\d)\b", sec["body"]))
                if not regions:
                    continue
                found = True
                if len(regions) != SSOT["S12"]["value"]:
                    errors.append(
                        f"{path}:{sec['line']} 節「{sec['title']}」の推論リージョンが "
                        f"{len(regions)} 件（{sorted(regions)}）ですが SSoT S12 は "
                        f"{SSOT['S12']['value']} です"
                    )
                else:
                    notes.append(f"S12: 推論リージョン {len(regions)} 件 {sorted(regions)}")
        if not found:
            errors.append(f"{path}: 推論リージョンの記述が見つかりません（S12 の根拠なし）")

    # S1 / S2: 文書中の記述が SSoT と一致するか（節スコープで限定）
    path = SSOT["S1"]["doc"]
    if os.path.isfile(path):
        n = len(re.findall(r"(?m)^## (\d{4}-\d{2}-\d{2}):", open(path, encoding="utf-8").read()))
        if n != SSOT["S1"]["value"]:
            errors.append(
                f"{path}: エントリ見出しが {n} 件ですが SSoT S1 は {SSOT['S1']['value']} です"
            )
        else:
            notes.append(f"S1: changelog のエントリ見出し {n} 件")


# ------------------------------------------------------------
# (c') 一次情報 HTML との突き合わせ（任意）
# ------------------------------------------------------------
def check_against_html(html_dir, errors, notes):
    """公式 HTML から実体を数え、SSoT 定数と照合する。

    ⚠️ `.md` companion は使わない（firewalls は3サーフェス連結・プレースホルダが潰れる）。
    """
    def read(name):
        path = os.path.join(html_dir, name)
        if not os.path.isfile(path):
            return None
        return open(path, encoding="utf-8").read()

    # S6: firewalls の表のデータ行数
    fw = read("web_firewalls.html")
    if fw:
        body = re.sub(r"(?s)<script.*?</script>", "", fw)
        rows = 0
        for t in re.findall(r"(?s)<table.*?</table>", body):
            rows += len([r for r in re.findall(r"(?s)<tr.*?</tr>", t) if "<td" in r])
        if rows != SSOT["S6"]["value"]:
            errors.append(
                f"公式 firewalls HTML の表データ行が {rows} ですが SSoT S6 は "
                f"{SSOT['S6']['value']} です（公式ページが変わった可能性）"
            )
        else:
            notes.append(f"S6: 公式 HTML の表データ行 {rows}（一致）")

    # S5: internet-access の許可ドメイン
    ia = read("web_sandbox_internet-access.html")
    if ia:
        s = re.sub(r"(?s)<script.*?</script>", "", ia)
        i = s.find("The following domains are automatically allowed")
        j = s.find("Open internet", i) if i >= 0 else -1
        seg = s[i:j] if i >= 0 and j > i else ""
        txt = html_mod.unescape(re.sub(r"<[^>]+>", "\n", seg))
        doms = {l.strip() for l in txt.split("\n")
                if re.fullmatch(r"[a-z0-9][a-z0-9.\-]*\.[a-z]{2,}", l.strip())}
        if doms:
            if len(doms) != SSOT["S5"]["value"]:
                errors.append(
                    f"公式 internet-access HTML の許可ドメインが {len(doms)} 件ですが "
                    f"SSoT S5 は {SSOT['S5']['value']} です（公式ページが変わった可能性）"
                )
            else:
                notes.append(f"S5: 公式 HTML の許可ドメイン {len(doms)} 件（一致）")

    # S7: gitlab の送信元 IP
    gl = read("web_gitlab.html")
    if gl:
        ips = set(IPV4_RE.findall(re.sub(r"(?s)<script.*?</script>", "", gl)))
        # バージョン様の誤検出を避けるため、オクテットが4つ揃うものだけ
        ips = {ip for ip in ips if len(ip.split(".")) == 4}
        if ips and len(ips) != SSOT["S7"]["value"]:
            errors.append(
                f"公式 gitlab HTML の IPv4 が {len(ips)} 件ですが SSoT S7 は "
                f"{SSOT['S7']['value']} です（公式ページが変わった可能性）"
            )
        elif ips:
            notes.append(f"S7: 公式 HTML の送信元 IP {len(ips)} 件（一致）")

    # S2: docs Web ページ数（HTML ファイル数で代用）
    n = len(glob.glob(os.path.join(html_dir, "web*.html")))
    if n:
        if n != SSOT["S2"]["value"]:
            errors.append(
                f"公式 docs のスナップショットが {n} ページですが SSoT S2 は "
                f"{SSOT['S2']['value']} です"
            )
        else:
            notes.append(f"S2: スナップショットの docs ページ {n} 件（一致）")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--html-dir", help="取得済み docs HTML のディレクトリ（任意）")
    args = ap.parse_args()
    os.chdir(repo_root())

    print("=== kiro-web-docs 件数整合チェック（正準値の水平展開） ===")
    print("")

    errors, notes, checked = [], [], []

    print("🔍 節見出しの宣言件数と実体を照合中...")
    check_declared(errors, checked)

    print("🔍 内訳表と合計を照合中...")
    check_breakdown(errors, notes)

    print("🔍 SSoT 定数と文書内の実体を照合中...")
    check_ssot_in_docs(errors, notes)

    if args.html_dir and os.path.isdir(args.html_dir):
        print(f"🔍 一次情報 HTML と照合中（{args.html_dir}）...")
        check_against_html(args.html_dir, errors, notes)
    else:
        print("⚠️  一次情報 HTML との照合をスキップしました")
        print("   → これは「公式と一致することを検証した」ではありません（**未検証**です）")
        print("   使い方: check-counts.py --html-dir <docs HTML のディレクトリ>")

    print("")
    print("=== チェック結果 ===")
    print(f"節見出しの宣言件数を照合: {len(checked)} 件")
    for path, line, title, declared, actual in checked:
        mark = "OK " if declared == actual else "NG "
        print(f"   {mark}{path}:{line} 「{title[:44]}」 宣言={declared} 実体={actual}")
    print("")
    if notes:
        print("正準値の確認:")
        for n in notes:
            print(f"   - {n}")
        print("")

    if errors:
        print(f"❌ エラー {len(errors)} 件:")
        for e in errors:
            print(f"   - {e}")
        print("")
        print("❌ 件数整合チェックに失敗しました")
        return 1

    print("✅ すべての件数記述が実体と一致しています")
    return 0


if __name__ == "__main__":
    sys.exit(main())
