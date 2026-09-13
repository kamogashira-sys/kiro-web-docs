#!/usr/bin/env python3
"""check-consistency.py - kiro-web-docs 記述整合チェック（上限値の水平展開・注記の対称性）

使用方法:
    ./scripts/kiro-web-docs/check-consistency.py

目的:
    同じ値が複数ページに書かれている状態で、**片方だけ直して他方が古い**まま残るのを落とす。
    check-counts.py が「表の実体 vs 宣言件数」を見るのに対し、本スクリプトは
    **「文書 A の値 vs 文書 B の値 vs SSoT 定数」**を見る。

検証する正準値（作業計画書 D-W7 の上限・保持期間系）:
    S8  並列タスク上限          = 10
    S9  スケジュール上限        = 5（公式本文は綴りで `five`）
    S10 プロンプト文字数上限    = 10,000
    S11 セッション保持期間      = 90 日
    S13 サンドボックスディスク  = 128GB
    S14 Free Tier 入力保持 / GPT 分類器 = 60 日 / 30 日

検証内容:
    1. **値の一意性**: 各正準値の「単位付きの記述」が、文書全体で SSoT 以外の値に
       なっていないか（例: 「並列 12 件」と書かれていたら検出）
    2. **所有ファイルへの掲載**: 正準値が `04_reference/04_limits.md`（所有ファイル）に
       記載されているか
    3. **食い違い注記の対称性**（F-W20）: Free Tier の食い違いは
       `03_deployment/01_setup.md` と `03_deployment/03_data-protection.md` の
       **両方**に注記が必要。片側だけだと読者が誤解する
    4. **未確認注記の存在**: S14 は Free Tier の食い違いに依存するため、
       同じページに「未確認」または「食い違い」の注記が必要
    5. **出典日の記載**: 本文ページに `Page updated:` 由来の出典日があるか
       （check-structure.py は出典 URL の有無を見る。**日付は本スクリプトが見る**）
    6. **出典日の水平展開**（作業5-5・2026-08-16 追加）: 同一の公式ページ URL に対する
       `Page updated` の記述が、複数ファイルにまたがるときに食い違っていないか。
       既知の実例: `docs/web/using-the-agent/` の出典日が `01_agent-modes.md` では
       June 11, 2026、`04_limits.md` では April 21, 2026 と**食い違っていた**（未検出のまま
       放置されていた）。1本のファイルの中では正しくても、**同じ公式ページを複数ファイルが
       引用するときに転記元の版がずれる**という失敗様式に対応する。

⚠️ 実装上の注意（Phase 2a・3-1 の教訓）:
    - **数値だけを探さない。** 「10」「5」「90」は文書に無数に現れる。
      **単位や文脈語とセットで**照合する。
    - 誤検知しやすい文脈（節番号・バージョン様の数値・日付）は除外する。
    - 検出できなかったこと自体も報告する（規則が空振りしていないかを見るため）。
"""
import argparse
import glob
import os
import re
import sys

DOC_ROOT = "kiro-web-docs"
LOCAL_ONLY = ("05_meta", "06_embedded-docs", "work_plans", "work_records")

# 正準値の所有ファイル（値の一覧を持つページ）
OWNER = f"{DOC_ROOT}/04_reference/04_limits.md"

# ------------------------------------------------------------
# SSoT（上限・保持期間系）
#   pattern: 「値が書かれている箇所」を拾う正規表現。捕獲群1が数値。
#            文脈語を必ず含め、裸の数値を拾わないようにする。
# ------------------------------------------------------------
SSOT = [
    {
        "id": "S8", "label": "並列タスク上限", "value": "10",
        # 「並列 10 件」「同時実行できるタスク数 | 10」「limit of 10 concurrent tasks」
        "pattern": re.compile(
            r"(?:並列(?:実行)?(?:できる)?(?:タスク)?(?:数)?[^\n|]{0,12}?|"
            r"同時実行[^\n|]{0,12}?|limit of\s+)\**\s*(\d+)\s*\**\s*(?:件|\||\s*concurrent|$)",
            re.MULTILINE),
    },
    {
        "id": "S9", "label": "スケジュール上限", "value": "5",
        # ⚠️ 表形式（`| **1オートメーションあたりのスケジュール数** | **5** |`）では
        #    文脈語と数値が **セル境界 `|` で隔てられる**。`[^\n|]` で境界を跨げない
        #    正規表現にすると1件も拾えない（実装当初これで「記述が見つかりません」と
        #    誤検知した）。セル境界を跨げるようにする。
        "pattern": re.compile(
            r"スケジュール(?:数)?(?:の上限)?[^\n]{0,20}?\**\s*(\d+)\s*\**\s*(?:つ|件|\s*\|)",
            re.MULTILINE),
    },
    {
        "id": "S10", "label": "プロンプト文字数上限", "value": "10000",
        "pattern": re.compile(r"\**\s*(\d{1,3}(?:,\d{3})+)\s*\**\s*文字"),
    },
    {
        "id": "S11", "label": "セッション保持期間", "value": "90",
        # ⚠️ 「セッション」を文脈語にすると、`data-protection` の
        #    「Free Tier 利用者のデータ保持（60 日）」を誤って拾う（実測）。
        #    S11 に固有の語（セッション＋期限/保持/expire）に限定する。
        "pattern": re.compile(
            r"(?:セッション(?:の)?(?:保持期間|有効期限)|Sessions expire after)"
            r"[^\n]{0,20}?\**\s*(\d+)\s*\**\s*(?:日|days)"),
    },
    {
        "id": "S13", "label": "サンドボックスディスク", "value": "128",
        "pattern": re.compile(r"(\d+)\s*GB"),
    },
]

# S14 は2つの値を持つため個別に扱う
S14 = [
    # ⚠️ 「**最長 60** 日」のように**強調が数値と単位の間に割り込む**書き方があり、
    #    `最長\s*\**\s*(\d+)\s*\**\s*日` では拾えない。強調の位置を柔軟にする。
    #    また表形式ではセル境界を跨ぐため `[^\n|]` を使わない。
    {"id": "S14a", "label": "Free Tier 入力保持", "value": "60",
     "pattern": re.compile(r"(?:Free Tier|入力)[^\n]{0,30}?最長\s*\**\s*(\d+)\s*\**\s*日")},
    {"id": "S14b", "label": "GPT 分類器フラグ付きトラフィック保持", "value": "30",
     "pattern": re.compile(r"(?:GPT|分類器|フラグ)[^\n]{0,40}?最長\s*\**\s*(\d+)\s*\**\s*日")},
]

# F-W20: Free Tier の食い違い注記が必要なページ（両方に必要）
CONFLICT_PAGES = [
    f"{DOC_ROOT}/03_deployment/01_setup.md",
    f"{DOC_ROOT}/03_deployment/03_data-protection.md",
]
CONFLICT_MARK_RE = re.compile(r"食い違")
UNCONFIRMED_RE = re.compile(r"未確認|未解決|食い違")

# 出典日。次の3形式のいずれかを認める。
#   (a) `Page updated: June 11, 2026` … docs ページの転記
#   (b) `（July 1, 2026）`             … changelog エントリの公式日付
#   (c) `**実測日**: 2026-08-01`       … sitemap / llms.txt など `Page updated` を
#                                        持たない情報源を扱うページ
# ⚠️ (c) を認めないと `00_information/01_official-site-structure.md` が落ちる。
#    このページの出典は sitemap・llms.txt で、公式側に更新日の表示が無い。
#    「出典日が必要」という規則の目的は**いつ時点の情報かを示すこと**なので、
#    実測日はその目的を満たす。
MONTHS_RE = (r"(?:January|February|March|April|May|June|July|August|"
             r"September|October|November|December)")
SOURCE_DATE_RE = re.compile(rf"Page updated:\s*{MONTHS_RE}\s+\d{{1,2}},\s*\d{{4}}")
ENTRY_DATE_RE = re.compile(rf"[（(]{MONTHS_RE}\s+\d{{1,2}},\s*\d{{4}}[)）]")
MEASURED_DATE_RE = re.compile(r"実測日\**\s*[:：]\s*\d{4}-\d{2}-\d{2}")

# 出典日の水平展開チェック用（作業5-5）:
# 「<URL>（Page updated: 月名 D, YYYY」の対を抜き出す。
# 出典行は `<url1>（Page updated: ...）・<url2>（Page updated: ...）` のように
# `・` 区切りで複数対が並ぶ（例: 01_agent-modes.md:6）。URL と直後の日付を1組として拾う。
#
# ⚠️ 閉じ括弧を要求してはいけない（2026-09-13 修正）。
#    移転のあったページは括弧内に注記が続く形をとる。
#      <https://kiro.dev/docs/specs/>（Page updated: August 27, 2026・**…に移転**。
#        旧 `docs/web/specs/` は…Page updated: July 22, 2026）
#    閉じ括弧を要求すると、この形の出典行が**丸ごと照合から外れる**。
#    実測（2026-09-13）では **10 箇所の出典行**が落ちており、そのうち
#    **3 URL（data-protection・firewalls・setup）は 1 箇所も照合されていなかった**
#    （specs・steering は別の出典行で拾えていたため URL 単位では露見しなかった）。
#
#    括弧内の 2 つ目以降の `Page updated`（旧ページの日付）を拾わないのは、
#    **本文の書式規約**（旧ページ参照は `` `docs/web/specs/` `` のようにバッククォートで書き、
#    `<URL>（Page updated:` の形にしない）に依存している。
#    旧参照を `<URL>（Page updated: …` の形で書くと**旧 URL も拾う**ので、
#    その場合は移転前の URL がスナップショットに無く（上の unmapped 判定で）エラーになる。
URL_DATE_PAIR_RE = re.compile(
    r"<(https://kiro\.dev/[^>\s]+)>\s*[（(]Page updated:\s*("
    + MONTHS_RE + r"\s+\d{1,2},\s*\d{4})"
)

# 出典日 vs スナップショット照合用（2026-09-13 追加）:
# 公式ページの JSON-LD `"dateModified":"YYYY-MM-DDThh:mm:ss.000Z"` を拾う。
DATE_MODIFIED_RE = re.compile(r'"dateModified"\s*:\s*"(\d{4}-\d{2}-\d{2})')

# 月名 → 月番号。`Page updated: September 10, 2026` を ISO に正規化するために使う。
# locale に依存させない（環境によって %B が変わるのを避ける）。
MONTH_TO_NUM = {
    "January": 1, "February": 2, "March": 3, "April": 4, "May": 5, "June": 6,
    "July": 7, "August": 8, "September": 9, "October": 10, "November": 11,
    "December": 12,
}

# 公式 URL → スナップショットのファイル名。
# capture-snapshot.py の保存規則（web-doc / shared-doc / linked-doc）に合わせる。
#   web-doc    : docs_web[_<path>].html
#   shared-doc : shared_<path>.html
#   linked-doc : linked_<name>.html
SNAPSHOT_PREFIX = {
    "docs/web": "docs_web",
    "docs/privacy-and-security": "shared_privacy-and-security",
}
# Web docs 以外で本サイトが出典にしている全製品共通ページ（§8.3 のリンク先）。
LINKED_DOC_NAMES = {"specs", "steering", "cloud-sessions"}

# スナップショットに `dateModified` が無い（＝照合できない）ページ。
# `web/memory/` は取得できない（F-12）。取りこぼしを黙認しないため明示する。
NO_DATE_MODIFIED = {"https://kiro.dev/docs/web/memory/"}


def iso_from_page_updated(date_text):
    """`September 10, 2026` → `2026-09-10`。解釈できない場合は None。"""
    m = re.match(rf"({MONTHS_RE})\s+(\d{{1,2}}),\s*(\d{{4}})", date_text)
    if not m:
        return None
    return f"{int(m.group(3)):04d}-{MONTH_TO_NUM[m.group(1)]:02d}-{int(m.group(2)):02d}"


def snapshot_filename(url):
    """公式 URL → スナップショットのファイル名。対象外なら None。"""
    m = re.match(r"https://kiro\.dev/(.+?)/?$", url)
    if not m:
        return None
    path = m.group(1)
    name = path.split("/")[-1]
    if path == f"docs/{name}" and name in LINKED_DOC_NAMES:
        return f"linked_{name}.html"
    for prefix, stem in SNAPSHOT_PREFIX.items():
        if path == prefix:
            return f"{stem}.html"
        if path.startswith(prefix + "/"):
            rest = path[len(prefix) + 1:].replace("/", "_")
            return f"{stem}_{rest}.html"
    return None


def check_source_date_vs_snapshot(errors, notes, docs_html_dir):
    """(7) 本文の出典日が公式ページの `dateModified`（スナップショット）と一致するか。

    人手で `Page updated` を書き写す運用では、公式が更新されたのに
    出典日だけ古いまま残る事故が起きる。スナップショットの JSON-LD と
    機械照合することで、その事故を検出する。

    スナップショットが無い環境（クローン直後・CI）では検証せず成功にする。
    ただし「検証していない」ことは必ず表示する（黙ってスキップしない）。
    """
    if not docs_html_dir or not os.path.isdir(docs_html_dir):
        reason = (f"{docs_html_dir} が見つかりません" if docs_html_dir
                  else "DOCS_HTML_DIR が指定されていません")
        notes.append(
            "出典日 vs スナップショット: **未検証です**"
            f"（{reason}。"
            "`make check-kiro-web-consistency DOCS_HTML_DIR=...` で照合できます）"
        )
        return

    # スナップショット側の実測値を読む
    actual = {}
    for name in os.listdir(docs_html_dir):
        if not name.endswith(".html"):
            continue
        with open(os.path.join(docs_html_dir, name), encoding="utf-8",
                  errors="replace") as fh:
            m = DATE_MODIFIED_RE.search(fh.read())
        if m:
            actual[name] = m.group(1)

    body_docs = [d for d in public_docs()
                 if os.path.isfile(d) and os.path.basename(d) != "README.md"]
    checked = skipped = 0
    unmapped = set()
    for path in body_docs:
        txt = open(path, encoding="utf-8").read()
        for m in URL_DATE_PAIR_RE.finditer(txt):
            url, date_text = m.group(1), m.group(2)
            line = line_of(txt, m.start())
            if url in NO_DATE_MODIFIED:
                skipped += 1
                continue
            name = snapshot_filename(url)
            if not name or name not in actual:
                unmapped.add(url)
                continue
            written = iso_from_page_updated(date_text)
            if written != actual[name]:
                errors.append(
                    f"出典日がスナップショットと不一致: {url}"
                    f" — 記載 {date_text}（{written}） / 実測 {actual[name]}"
                    f" @ {path}:{line}"
                )
            checked += 1

    notes.append(
        f"出典日 vs スナップショット: {checked} 箇所を照合"
        f"（照合対象外 {skipped} 箇所 / スナップショットに無い URL {len(unmapped)} 件）"
    )
    for url in sorted(NO_DATE_MODIFIED):
        notes.append(f"  ⚠️ 公式に dateModified が無いため未照合: {url}")

    # ⚠️ ここを notes 止まりにしてはいけない（2026-09-13 追加）。
    #    「照合できなかった」を成功扱いにすると、
    #      - capture-snapshot.py に無い公式ページを新しく引用し始めた
    #      - スナップショットのファイル命名が再び変わった
    #      - 古いスナップショットを DOCS_HTML_DIR に指定した
    #    のいずれでも、**緑のまま1件も照合しなくなる**。
    #    実際に check-counts.py（旧命名で S2/S5/S6/S7 が黙ってスキップ）と
    #    check-freshness.py（S2 が常に 17）で同じ型の穴が起きていた。
    for url in sorted(unmapped):
        errors.append(
            f"出典日を照合できません: {url} に対応するファイルが"
            f" {docs_html_dir} にありません"
            "（capture-snapshot.py の取得対象に追加するか、"
            "公式に更新日が無いページなら NO_DATE_MODIFIED に明示してください）"
        )
    if not checked and not skipped:
        errors.append(
            "出典日を1箇所も照合できませんでした"
            f"（{docs_html_dir} が目的のスナップショットか確認してください）"
        )


def repo_root():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))


def is_local_only(path):
    norm = path.replace(os.sep, "/")
    return any(f"/{lo}/" in norm or norm.startswith(f"{lo}/") for lo in LOCAL_ONLY)


def strip_code(txt):
    """フェンスコードブロックを除去する（設定例の中の数値を値の記述と誤読しないため）。"""
    out, in_fence = [], False
    for line in txt.splitlines(keepends=True):
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        out.append(line)
    return "".join(out)


def public_docs():
    docs = sorted(glob.glob(f"{DOC_ROOT}/**/*.md", recursive=True))
    return [d for d in docs if not is_local_only(d)] + ["README.md"]


def line_of(text, pos):
    return text[:pos].count("\n") + 1


def check_values(errors, notes):
    """(1) 値の一意性 と (2) 所有ファイルへの掲載。"""
    for item in SSOT + S14:
        hits = []  # (path, line, found_value)
        for path in public_docs():
            if not os.path.isfile(path):
                continue
            txt = strip_code(open(path, encoding="utf-8").read())
            for m in item["pattern"].finditer(txt):
                found = m.group(1).replace(",", "")
                hits.append((path, line_of(txt, m.start()), found, m.group(0).strip()))

        if not hits:
            # 規則が空振りしている可能性。値が文書から消えたのかもしれない。
            errors.append(
                f"{item['id']}（{item['label']}）の記述が公開文書に見つかりません"
                "（値が消えた／表現が変わった／規則が空振りしている）"
            )
            continue

        wrong = [h for h in hits if h[2] != item["value"]]
        for path, line, found, snippet in wrong:
            errors.append(
                f"{path}:{line} {item['id']}（{item['label']}）が {found} と書かれています"
                f"（正準値は {item['value']}）: {snippet[:60]!r}"
            )

        # 所有ファイルに載っているか
        if not any(h[0] == OWNER for h in hits):
            errors.append(
                f"{item['id']}（{item['label']}）が所有ファイル {OWNER} に記載されていません"
            )

        files = sorted({h[0] for h in hits})
        notes.append(
            f"{item['id']} {item['label']} = {item['value']}: {len(hits)} 箇所 / "
            f"{len(files)} ファイル"
        )


def check_conflict_notes(errors, notes):
    """(3) 食い違い注記の対称性（F-W20）。"""
    missing = []
    for path in CONFLICT_PAGES:
        if not os.path.isfile(path):
            missing.append(f"{path}（ファイルが無い）")
            continue
        if not CONFLICT_MARK_RE.search(open(path, encoding="utf-8").read()):
            missing.append(path)
    if missing:
        errors.append(
            "Free Tier の食い違い注記（F-W20）が次のページにありません: "
            + "・".join(missing)
            + "（片側だけだと読者が一方の記述を確定情報と誤解する）"
        )
    else:
        notes.append(f"F-W20: 食い違い注記が {len(CONFLICT_PAGES)} ページ両方にあります")


def check_unconfirmed_near_s14(errors, notes):
    """(4) S14 の記述には未確認/食い違いの注記が同じページに必要。"""
    for item in S14:
        for path in public_docs():
            if not os.path.isfile(path):
                continue
            txt = strip_code(open(path, encoding="utf-8").read())
            if not item["pattern"].search(txt):
                continue
            if not UNCONFIRMED_RE.search(txt):
                errors.append(
                    f"{path}: {item['id']}（{item['label']}）を記述していますが、"
                    "同じページに「未確認」または「食い違い」の注記がありません"
                    "（Free Tier の存在自体が未解決のため必須）"
                )
    notes.append("S14: 記述のあるページに未確認注記があることを確認しました")


def check_source_dates(errors, notes):
    """(5) 本文ページに出典日（`Page updated:` の転記）があるか。"""
    body_docs = [d for d in public_docs()
                 if os.path.isfile(d) and os.path.basename(d) != "README.md"]
    missing = []
    kinds = {"Page updated": 0, "エントリ日付": 0, "実測日": 0}
    for path in body_docs:
        txt = open(path, encoding="utf-8").read()
        if SOURCE_DATE_RE.search(txt):
            kinds["Page updated"] += 1
        elif ENTRY_DATE_RE.search(txt):
            kinds["エントリ日付"] += 1
        elif MEASURED_DATE_RE.search(txt):
            kinds["実測日"] += 1
        else:
            missing.append(path)
    for path in missing:
        errors.append(
            f"{path}: 出典日（`Page updated: 月名 D, YYYY`）の記載がありません"
            "（いつ時点の情報かを読者が判断できない）"
        )
    notes.append(
        f"出典日: 本文 {len(body_docs)} ページ中 {len(body_docs) - len(missing)} ページに記載あり"
        f"（Page updated {kinds['Page updated']} / エントリ日付 {kinds['エントリ日付']} / "
        f"実測日 {kinds['実測日']}）"
    )


def check_source_date_consistency(errors, notes):
    """(6) 出典日の水平展開: 同一 URL の Page updated が複数ファイル間で食い違っていないか。"""
    # url -> {date: [ (path, line), ... ]}
    by_url = {}
    body_docs = [d for d in public_docs()
                 if os.path.isfile(d) and os.path.basename(d) != "README.md"]
    for path in body_docs:
        txt = open(path, encoding="utf-8").read()
        for m in URL_DATE_PAIR_RE.finditer(txt):
            url, date = m.group(1), m.group(2)
            by_url.setdefault(url, {}).setdefault(date, []).append(
                (path, line_of(txt, m.start()))
            )

    inconsistent = 0
    for url, date_map in sorted(by_url.items()):
        if len(date_map) <= 1:
            continue
        inconsistent += 1
        detail = "; ".join(
            f"{date}（{', '.join(f'{p}:{l}' for p, l in locs)}）"
            for date, locs in sorted(date_map.items())
        )
        errors.append(
            f"出典日の不整合: {url} の Page updated がファイル間で食い違っています: {detail}"
        )

    total_urls = len(by_url)
    notes.append(
        f"出典日の水平展開: 一意な公式 URL {total_urls} 件中 {inconsistent} 件で不整合"
    )


def main():
    parser = argparse.ArgumentParser(
        description="kiro-web-docs の記述整合チェック（上限値・注記・出典日）")
    parser.add_argument(
        "--docs-html-dir",
        help="公式 docs スナップショットの HTML ディレクトリ。"
             "指定すると出典日を JSON-LD の dateModified と照合する")
    args = parser.parse_args()

    os.chdir(repo_root())
    print("=== kiro-web-docs 記述整合チェック（上限値の水平展開・注記の対称性） ===")
    print("")

    errors, notes = [], []

    print("🔍 上限値・保持期間の一意性と掲載を検証中...")
    check_values(errors, notes)

    print("🔍 食い違い注記の対称性を検証中（F-W20）...")
    check_conflict_notes(errors, notes)

    print("🔍 S14 の未確認注記を検証中...")
    check_unconfirmed_near_s14(errors, notes)

    print("🔍 本文ページの出典日を検証中...")
    check_source_dates(errors, notes)

    print("🔍 出典日の水平展開を検証中（作業5-5）...")
    check_source_date_consistency(errors, notes)

    print("🔍 出典日を公式スナップショットと照合中...")
    check_source_date_vs_snapshot(errors, notes, args.docs_html_dir)

    print("")
    print("=== チェック結果 ===")
    for n in notes:
        print(f"   - {n}")
    print("")

    if errors:
        print(f"❌ エラー {len(errors)} 件:")
        for e in errors:
            print(f"   - {e}")
        print("")
        print("❌ 記述整合チェックに失敗しました")
        return 1

    print("✅ 上限値・注記・出典日がすべて整合しています")
    return 0


if __name__ == "__main__":
    sys.exit(main())
