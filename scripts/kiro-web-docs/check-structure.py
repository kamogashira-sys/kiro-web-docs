#!/usr/bin/env python3
"""check-structure.py - kiro-web-docs のディレクトリ・文書構造チェック

使用方法:
    ./scripts/kiro-web-docs/check-structure.py

検証内容:
    1. 公開5セクション（G1 確定構成）が存在すること
    2. 各セクションに README.md があること（未着手セクションは警告にとどめる）
    3. 各 Markdown が H1 見出しから始まること
    4. 各セクションのファイル軸が G1 で確定した構成に沿っていること
    5. ローカル管理セクション（05_meta / 06_embedded-docs / work_plans）が
       公開文書から参照されていないこと（公開リポジトリからは辿れないため）
    6. **本文ページ（README 以外）の冒頭に「Kiro Web 版の仕様」の明示があること**（D-W5）
       ⚠️ Web 固有の規則。3製品が別物であることを読者が取り違えないようにする
    7. **本文ページに公式の出典 URL があること**（Rev.7 の全ページ出典日必須を継承）

規則は Phase 2a では最小集合とし、量産（Phase 2b）に合わせて拡張する。
未執筆のセクションは「まだ執筆されていない」として警告にとどめ、エラーにしない。
"""
import glob
import os
import re
import sys

DOC_ROOT = "kiro-web-docs"

# G1 で確定した公開セクション
PUBLIC_SECTIONS = [
    "00_information",
    "01_features",
    "02_update",
    "03_deployment",
    "04_reference",
]

# ローカル管理（GitHub 非公開）。公開文書からリンクしてはいけない。
LOCAL_ONLY = ["05_meta", "06_embedded-docs", "work_plans"]

# G1 §2 で確定したファイル軸。想定外のファイルが増えたら構成の見直しが必要
# （＝設計書を更新してからファイルを足す、という順序を守らせる）。
SECTION_FILES = {
    "00_information": [
        "01_official-site-structure.md",
        "02_information-sources.md",
    ],
    "01_features": [
        "01_agent-modes.md",
        "02_specs.md",
        "03_automations.md",
        "04_steering.md",
        "05_sandbox.md",
        "06_repository-integration.md",
    ],
    "02_update": [
        "01_changelog.md",
    ],
    "03_deployment": [
        "01_setup.md",
        "02_identity-center.md",
        "03_data-protection.md",
        "04_firewalls.md",
    ],
    "04_reference": [
        "01_allowed-domains.md",
        "02_environment-variables.md",
        "03_mcp-configuration.md",
        "04_limits.md",
    ],
}

LINK_RE = re.compile(r'\[[^\]]*\]\(([^)]+)\)')

# D-W5: 本文ページ冒頭で「Kiro Web 版の仕様」であることを明示する。
# 表記の揺れを許容する（「Kiro Web 版」「Kiro Web（...）の...」のいずれか）。
WEB_SCOPE_RE = re.compile(r"Kiro Web\s*版|本ページは\s*\*\*Kiro Web|Kiro Web（")

# 出典 URL（公式 docs または changelog）。本文ページには必須。
SOURCE_URL_RE = re.compile(r"https://kiro\.dev/(?:docs|changelog)/")

# 冒頭とみなす行数。ここまでにスコープ明示と出典があること。
HEAD_LINES = 30


def repo_root():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))


def strip_code(txt):
    """フェンスコードブロックとインラインコードを除去する。"""
    out, in_fence = [], False
    for line in txt.splitlines(keepends=True):
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        out.append(re.sub(r"`[^`\n]*`", "", line))
    return "".join(out)


def main():
    os.chdir(repo_root())
    errors, warnings = [], []

    print("=== kiro-web-docs 構造チェック ===")
    print("")

    # ---- 1. 公開セクションの存在 ----
    print("🔍 公開セクションの存在を検証中...")
    for sec in PUBLIC_SECTIONS:
        path = os.path.join(DOC_ROOT, sec)
        if not os.path.isdir(path):
            errors.append(f"公開セクションがありません: {path}")

    # ---- 2. セクションの README ----
    print("🔍 各セクションの README を検証中...")
    written_sections = []
    for sec in PUBLIC_SECTIONS:
        path = os.path.join(DOC_ROOT, sec)
        if not os.path.isdir(path):
            continue
        mds = [f for f in os.listdir(path) if f.endswith(".md")]
        if not mds:
            warnings.append(f"{sec}/ はまだ執筆されていません（Phase 2b で執筆）")
            continue
        if "README.md" not in mds:
            errors.append(f"{sec}/ に README.md がありません（本文が {len(mds)} 件あるのに索引がない）")
        if [f for f in mds if f != "README.md"]:
            written_sections.append(sec)

    # ---- 3. H1 見出しから始まっているか ----
    print("🔍 各 Markdown の H1 見出しを検証中...")
    docs = sorted(glob.glob(f"{DOC_ROOT}/**/*.md", recursive=True))
    docs = [d for d in docs if not any(f"/{lo}/" in d.replace(os.sep, "/") or
                                       d.replace(os.sep, "/").endswith(f"/{lo}")
                                       for lo in LOCAL_ONLY)]
    for d in docs:
        try:
            with open(d, encoding="utf-8") as f:
                first = next((ln for ln in f if ln.strip()), "")
        except OSError:
            continue
        if not first.startswith("# "):
            errors.append(f"{d}: H1 見出し（`# `）から始まっていません: {first.strip()[:40]!r}")

    # ---- 4. 各セクションのファイル軸 ----
    print("🔍 各セクションのファイル軸を検証中...")
    for sec, expected in SECTION_FILES.items():
        sec_dir = os.path.join(DOC_ROOT, sec)
        if not os.path.isdir(sec_dir):
            continue
        present = {f for f in os.listdir(sec_dir) if f.endswith(".md")}
        unexpected = present - set(expected) - {"README.md"}
        if unexpected:
            errors.append(
                f"{sec}/ に想定外のファイルがあります: {sorted(unexpected)}"
                f"（G1 で確定した軸は {expected}）"
            )
        missing = set(expected) - present
        if missing:
            warnings.append(f"{sec}/ の未執筆ファイル: {sorted(missing)}")

    # ---- 5. 公開文書からローカル管理領域へのリンク ----
    print("🔍 公開文書からのリンク先を検証中...")
    for d in docs:
        try:
            txt = strip_code(open(d, encoding="utf-8").read())
        except OSError:
            continue
        for m in LINK_RE.finditer(txt):
            target = m.group(1).strip()
            norm = target.replace(os.sep, "/")
            if norm.startswith(("http://", "https://")):
                continue
            for lo in LOCAL_ONLY:
                if f"{lo}/" in norm:
                    errors.append(
                        f"{d}: ローカル管理領域へのリンクがあります: '{target}'"
                        f"（{lo}/ は GitHub 非公開のため公開リポジトリから辿れない）"
                    )

    # ---- 6・7. 本文ページのスコープ明示と出典 ----
    # README は索引なので対象外（本文ページのみ）。
    print("🔍 本文ページのスコープ明示と出典を検証中...")
    body_docs = [d for d in docs if os.path.basename(d) != "README.md"]
    for d in body_docs:
        try:
            lines = open(d, encoding="utf-8").read().splitlines()
        except OSError:
            continue
        head = "\n".join(lines[:HEAD_LINES])
        if not WEB_SCOPE_RE.search(head):
            errors.append(
                f"{d}: 冒頭 {HEAD_LINES} 行に「Kiro Web 版の仕様」の明示がありません"
                "（D-W5: 3製品を取り違えさせないため必須）"
            )
        if not SOURCE_URL_RE.search(head):
            errors.append(
                f"{d}: 冒頭 {HEAD_LINES} 行に公式の出典 URL がありません"
                "（kiro.dev の docs または changelog を示すこと）"
            )

    # ---- 結果 ----
    print("")
    print("=== チェック結果 ===")
    print(f"検証した公開 Markdown: {len(docs)} 件（うち本文ページ {len(body_docs)} 件）")
    print(f"本文を執筆済みのセクション: {len(written_sections)} / {len(PUBLIC_SECTIONS)}"
          f"（{', '.join(written_sections) or 'なし'}）")
    print("")

    if warnings:
        print(f"⚠️  警告 {len(warnings)} 件（未執筆。エラーではない）:")
        for w in warnings:
            print(f"   - {w}")
        print("")

    if errors:
        print(f"❌ エラー {len(errors)} 件:")
        for e in errors:
            print(f"   - {e}")
        print("")
        print("❌ 構造チェックに失敗しました")
        sys.exit(1)

    print("✅ 構造は健全です")
    sys.exit(0)


if __name__ == "__main__":
    main()
