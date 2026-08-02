#!/usr/bin/env python3
"""check-notation.py - kiro-web-docs 表記規約チェック

使用方法:
    ./scripts/kiro-web-docs/check-notation.py

D-W10（表記規約）の確定内容:
    (a) **他製品のコマンド・固有機能の混入**
        Kiro Web はブラウザから使うサービスなので、CLI コマンド（`kiro-cli` 等）や
        IDE 固有の概念（`Code OSS`・キーバインド等）が本文に出るのは誤り。
        ただし**「別製品である」と説明する文脈は正当**なので、同じ行に
        区別を示す語（IDE / CLI / 別製品 / 姉妹）があれば許容する。
    (b) **製品名の揺れ**
        `Kiro web` / `kiro Web` のような大文字小文字の崩れを検出する。
    (c) **非 ISO 日付**
        本サイトの日付は `YYYY-MM-DD`。英語表記（`Jul 1, 2026`）は
        **公式表記の引用・出典表示・表記形式の説明**でのみ許容する。
    (d) **存在しない版番号の創作**
        Kiro Web には版番号が無い（F-W2）。`1.0.5` のような文字列を
        Web の文脈で使ったら要出典。
        ⚠️ 実測で判明した**正当な例外3種**を許可リストにする:
           - `TLS 1.2`      … プロトコル版（`data-protection` の公式記述）
           - `Mozilla/5.0`  … User-Agent の指定（取得手順）
           - `1.0.242` 等   … **Kiro IDE の実在する版**への言及（対比の説明で使う）
        許可リストは**実行時に必ず表示**する（暗黙に見逃さないため）。
    (e) **取得日の本文混入**
        「いつ取得したか」は作業記録に書く。本文の出典日は公式の更新日を使う。
        ⚠️ `.github/` の規約文書は「取得日は本文に書かない」というルール自体を
           書いているので対象外にする。
    (f) **裸 URL 直後の全角文字による autolink 事故**
        `<https://...>` を使わず裸で書き、直後に全角文字が続くと処理系によって
        リンク範囲が崩れる。
    (g) **禁止表現（推測表現）**
        「おそらく」「と思われる」等。
        ⚠️ **`.github/` の規約文書は禁止表現の一覧そのものを載せている**ため
           対象外にする（実測で7件ヒットした）。

⚠️ 設計方針:
    規則の所有権を分ける。URL の書式は check-links.py、件数は check-counts.py、
    値の水平展開は check-consistency.py が持つ。本スクリプトは**表記**だけを見る。
"""
import glob
import os
import re
import sys

DOC_ROOT = "kiro-web-docs"
LOCAL_ONLY = ("05_meta", "06_embedded-docs", "work_plans", "work_records")

# 規約そのものを記述しているファイル。禁止表現の一覧・取得日ルールを含むため、
# (e) と (g) の検査対象から外す。
POLICY_DOCS = (".github/WORKFLOW.md", ".github/COMMIT_CHECKLIST.md",
               ".github/pull_request_template.md")

# ------------------------------------------------------------
# (a) 他製品のコマンド・固有機能
# ------------------------------------------------------------
OTHER_PRODUCT_PATTERNS = [
    (re.compile(r"\bkiro-cli\b"), "Kiro CLI のコマンド"),
    (re.compile(r"\bq\s+chat\b"), "Amazon Q CLI のコマンド"),
    (re.compile(r"\bCode OSS\b"), "Kiro IDE の基盤（IDE 固有）"),
    (re.compile(r"\.kiro/hooks\b"), "Kiro IDE の Hooks（Web には無い）"),
]
# 「別製品である」と説明する文脈を示す語。同じ行にあれば許容する。
DISTINCTION_RE = re.compile(r"Kiro IDE|Kiro CLI|別製品|姉妹|IDE 版|CLI 版|対比|IDE の")

# ------------------------------------------------------------
# (b) 製品名の揺れ
# ------------------------------------------------------------
PRODUCT_NAME_RE = re.compile(r"\b(?:kiro\s+Web|Kiro\s+web|KIRO\s+WEB)\b")

# ------------------------------------------------------------
# (c) 非 ISO 日付
# ------------------------------------------------------------
MONTHS = (r"(?:January|February|March|April|May|June|July|August|September|"
          r"October|November|December|Jan|Feb|Mar|Apr|Jun|Jul|Aug|Sep|Oct|Nov|Dec)")
EN_DATE_RE = re.compile(rf"\b{MONTHS}\.?\s+\d{{1,2}},\s*\d{{4}}")
# 英語日付が許される文脈（出典表示・公式表記の引用・表記形式の説明）
DATE_OK_RE = re.compile(r"Page updated|出典|公式|引用|略記|月名フル|形式|表記|>")

# ------------------------------------------------------------
# (d) 版番号の創作
# ------------------------------------------------------------
VERSION_RE = re.compile(r"(?<![\d.\w])\d+\.\d+(?:\.\d+)?(?![\d.])")
# 実測で確認した正当な例外（暗黙に見逃さないよう実行時に表示する）
VERSION_ALLOW = [
    (re.compile(r"TLS\s+\d+\.\d+"), "TLS のプロトコル版（公式 data-protection の記述）"),
    (re.compile(r"Mozilla/\d+\.\d+"), "User-Agent の指定（HTML 取得の作法）"),
    (re.compile(r"(?:Kiro IDE|IDE)\s*(?:の)?\s*`?\d+\.\d+\.\d+`?"),
     "Kiro IDE の実在する版への言及（3製品の対比）"),
    (re.compile(r"`\d+\.\d+\.\d+`\s*(?:のような|に相当|に対応)"),
     "IDE の版番号の書式を例示（Web には無いことの説明）"),
]

# ------------------------------------------------------------
# (e) 取得日の混入
# ------------------------------------------------------------
FETCH_DATE_RE = re.compile(r"取得日\s*[:：]|取得日は\s*\d{4}")

# ------------------------------------------------------------
# (f) autolink 事故
# ------------------------------------------------------------
# 裸の URL（`<...>` でも `[...](...)` でもない）の直後に全角文字が続く
BARE_URL_FULLWIDTH_RE = re.compile(
    r"(?<![<(\[])\bhttps?://[^\s<>()\[\]]+[０-９Ａ-Ｚａ-ｚぁ-んァ-ヶ一-龠、。（）「」]")

# ------------------------------------------------------------
# (g) 禁止表現
# ------------------------------------------------------------
BANNED = ["おそらく", "と思われる", "と思われます", "かもしれない", "かもしれません",
          "だろう", "でしょう", "予想されます"]


def repo_root():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))


def is_local_only(path):
    norm = path.replace(os.sep, "/")
    return any(f"/{lo}/" in norm or norm.startswith(f"{lo}/") for lo in LOCAL_ONLY)


def target_files():
    files = sorted(glob.glob(f"{DOC_ROOT}/**/*.md", recursive=True))
    files = [f for f in files if not is_local_only(f)]
    files += ["README.md"] + sorted(glob.glob(".github/*.md"))
    return [f for f in files if os.path.isfile(f)]


def code_line_flags(path):
    """各行がフェンスコードブロック内かどうかを返す（1-indexed）。"""
    flags = {}
    in_fence = False
    for i, line in enumerate(open(path, encoding="utf-8"), 1):
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            flags[i] = True
            continue
        flags[i] = in_fence
    return flags


def main():
    os.chdir(repo_root())
    print("=== kiro-web-docs 表記規約チェック ===")
    print("")

    errors = []
    allowed_versions = []   # (path, line, matched, reason)
    stats = {"files": 0, "lines": 0}

    for path in target_files():
        stats["files"] += 1
        in_code = code_line_flags(path)
        is_policy = path in POLICY_DOCS

        for i, line in enumerate(open(path, encoding="utf-8"), 1):
            stats["lines"] += 1
            code = in_code.get(i, False)

            # (a) 他製品のコマンド・固有機能（コードブロック内も対象。手順に混ざると害）
            for pat, label in OTHER_PRODUCT_PATTERNS:
                m = pat.search(line)
                if m and not DISTINCTION_RE.search(line):
                    errors.append(
                        f"{path}:{i} (a) {label} が Web の文脈に混入しています: "
                        f"{m.group(0)!r}（別製品と明示するか削除してください）"
                    )

            if code:
                continue  # 以降の規則はコードブロック外のみ

            # (b) 製品名の揺れ
            m = PRODUCT_NAME_RE.search(line)
            if m:
                errors.append(
                    f"{path}:{i} (b) 製品名の表記が揺れています: {m.group(0)!r}"
                    "（正: `Kiro Web`）"
                )

            # (c) 非 ISO 日付
            for m in EN_DATE_RE.finditer(line):
                if not DATE_OK_RE.search(line):
                    errors.append(
                        f"{path}:{i} (c) 英語表記の日付が出典・引用以外で使われています: "
                        f"{m.group(0)!r}（本文は ISO `YYYY-MM-DD`）"
                    )

            # (d) 版番号の創作
            for m in VERSION_RE.finditer(line):
                reason = None
                for allow_pat, label in VERSION_ALLOW:
                    if any(a.start() <= m.start() and m.end() <= a.end()
                           for a in allow_pat.finditer(line)):
                        reason = label
                        break
                if reason:
                    allowed_versions.append((path, i, m.group(0), reason))
                else:
                    errors.append(
                        f"{path}:{i} (d) 版番号のような文字列があります: {m.group(0)!r}"
                        "（Kiro Web には版番号が存在しません。許可リストに無い値は"
                        "出典を示すか削除してください）"
                    )

            # (e) 取得日の混入（規約文書は対象外）
            if not is_policy and FETCH_DATE_RE.search(line):
                errors.append(
                    f"{path}:{i} (e) 取得日が本文に書かれています"
                    "（取得日は作業記録に残し、本文には公式の出典日を書きます）"
                )

            # (f) autolink 事故
            m = BARE_URL_FULLWIDTH_RE.search(line)
            if m:
                errors.append(
                    f"{path}:{i} (f) 裸の URL の直後に全角文字があります: {m.group(0)[-40:]!r}"
                    "（`<https://...>` で囲むか半角空白を入れてください）"
                )

            # (g) 禁止表現（規約文書は対象外）
            if not is_policy:
                for w in BANNED:
                    if w in line:
                        errors.append(
                            f"{path}:{i} (g) 推測表現が使われています: {w!r}"
                            "（一次情報で確認して断定するか「未確認」と明示してください）"
                        )

    print(f"検査ファイル: {stats['files']} 件 / {stats['lines']} 行")
    print("")
    print(f"(d) 版番号の許可リストに合致した記述: {len(allowed_versions)} 件")
    if allowed_versions:
        print("   ※ 暗黙に見逃さないよう全件を表示します")
        for path, line, matched, reason in allowed_versions:
            print(f"      {path}:{line} {matched!r} … {reason}")
    print("")

    if errors:
        print(f"❌ エラー {len(errors)} 件:")
        for e in errors:
            print(f"   - {e}")
        print("")
        print("❌ 表記規約チェックに失敗しました")
        return 1

    print("✅ 表記規約に違反はありません")
    return 0


if __name__ == "__main__":
    sys.exit(main())
