#!/usr/bin/env python3
"""check-links.py - kiro-web-docs 内部リンク整合チェック

使用方法:
    ./scripts/kiro-web-docs/check-links.py
    ./scripts/kiro-web-docs/check-links.py --check-anchors   # アンカー(見出し)実在も検査(日本語含む)
    ./scripts/kiro-web-docs/check-links.py --check-anchors --paths <file...>
        # 指定ファイルのみ検査（既定の除外を適用しない。05_meta 等のローカル管理文書の
        # 相互リンク検証用）

機能:
    - kiro-web-docs/**/*.md ＋ ルート README.md ＋ .github/*.md の
      相対 Markdown リンクを抽出し、リンク先ファイルの実在を検証
    - 同一ファイル内アンカー（`#...`）と他ファイルのアンカーの実在を検証
    - kiro.dev の外部リンクの書式を検証:
        - **changelog も docs も末尾スラッシュ必須**（無しは 301 リダイレクト）
          ⚠️ IDE 版は changelog だけを対象にしていたが、Web 版では docs も
             20/20 が 301 になることを実測した（F-W11）ため両方を検査する
        - 姉妹製品（IDE / CLI）のページへのリンクは「別製品」であることの明示を促す
          （検出のみ・警告）
    - 上記以外の http(s)/mailto/tel は到達性を検証しない（check-urls.sh の担当）

除外（スコープ外・ローカル管理のため。ソースのスキャン／リンク先の検証の両方に適用）:
    - kiro-web-docs/06_embedded-docs/**  … 公式サイトページのスナップショット（GitHub 非公開）
    - kiro-web-docs/05_meta/**           … 保守手順書・テンプレート（GitHub 非公開）
    - kiro-web-docs/work_plans/**        … 作業計画書（GitHub 非公開）
    - work_records/**                    … 作業記録（GitHub 非公開）
    - *_plan.md                          … gitignore 対象の計画書
"""
import glob
import os
import re
import sys

LINK_RE = re.compile(r'\[([^\]]*)\]\(([^)]+)\)')
# 素の URL（<https://...> 形式を含む）も書式検証の対象にする
BARE_URL_RE = re.compile(r'<?(https://kiro\.dev/[^\s>)"\']*)>?')
HEADING_RE = re.compile(r'^#{1,6}\s+(.*?)\s*$')
# 明示的な HTML アンカー（`<a id="..."></a>`）。絵文字を含む見出しは slug の生成規則が
# 処理系で揺れるため、リンク先には明示アンカーを使う。
HTML_ANCHOR_RE = re.compile(r'<a\s+(?:id|name)=["\']([^"\']+)["\']')

EXCLUDE_SUBSTR = (
    "kiro-web-docs/06_embedded-docs/",   # 公式サイトページのスナップショット（GitHub 非公開）
    "kiro-web-docs/05_meta",             # 保守手順書・テンプレート（GitHub 非公開）
    "kiro-web-docs/work_plans",          # 作業計画書（GitHub 非公開）
    "work_records/",                     # 作業記録（GitHub 非公開）
    "_plan.md",                          # *_plan.md は gitignore 対象の計画書
)
SKIP_PREFIX = ("http://", "https://", "mailto:", "tel:")

# GitHub が解決する相対リンク（`../../issues` = リポジトリの Issues タブ）。
# ファイルシステム上には存在しないため実在検証の対象外にする。
# **`../` の数はファイルの階層で変わる**ので個数を固定しない（IDE 版で
# 固定文字列で列挙していたため深さ4の形が全件リンク切れ扱いになった実例がある）。
GITHUB_RELATIVE_RE = re.compile(
    r"^(?:\.\./)+(?:issues|pulls|discussions|wiki)(?:/\d+)?$"
)

# ⚠️ プレースホルダを含む URL は書式検証の対象外にする。
# 手順書・テンプレート・ワークフローには `https://kiro.dev/changelog/web/<slug>/` の
# ような雛形 URL が意図的にある。これを実 URL として検査すると常時 FAIL になる
# （Phase 1 の暫定検査で末尾スラッシュ違反3件を報告したが、全件この誤検知だった）。
PLACEHOLDER_RE = re.compile(r"[<>{}]|\((?:スラッグ|パス|slug|path)\)|（")

# kiro.dev は末尾スラッシュがないと 301 リダイレクトになる。
# ⚠️ **changelog だけでなく docs も同様**（F-W11: docs 20ページを末尾スラッシュ無しで
#    取得すると 20/20 が 301・本文0バイト）。IDE 版は changelog のみを対象にしていた。
SLASH_REQUIRED_RE = re.compile(r'^https://kiro\.dev/(?:changelog|docs)(?:/|$)')

# 姉妹製品のドキュメント。Web 版から参照するときは「別製品の同名機能」である旨の
# 明示が必要（D-W5）。ここでは URL の存在を検出して報告するだけで、文面の検査は
# check-notation.py（Phase 3）の担当にする。所有権を分けて規則の重複を避ける。
SIBLING_DOCS_RE = re.compile(r'^https://kiro\.dev/docs/(cli/|(?!web/)[a-z])')


def repo_root():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))


def is_excluded(path):
    norm = path.replace(os.sep, "/")
    return any(sub in norm for sub in EXCLUDE_SUBSTR)


def slugify(heading):
    """GitHub 風 slug。記号除去・空白をハイフン・小文字化。
    GitHub は空白 1 文字ごとにハイフン 1 つ（連続空白を潰さない。例: 「a / b」→ a--b）。"""
    s = heading.strip().lower()
    s = s.replace("`", "")
    s = re.sub(r"[^\w\s\-ぁ-んァ-ヶ一-龠ー]", "", s)
    return re.sub(r"\s", "-", s)


def strip_code(txt):
    """フェンスコードブロックとインラインコードスパンを除去（コード内のリンク記法例は
    Markdown ではリンクとして描画されないため、リンク抽出の対象外にする）。"""
    out = []
    in_fence = False
    for line in txt.splitlines(keepends=True):
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        out.append(re.sub(r"`[^`\n]*`", "", line))
    return "".join(out)


def collect_headings(filepath):
    slugs = set()
    in_fence = False
    try:
        with open(filepath, encoding="utf-8") as f:
            for line in f:
                # フェンス内の「# コメント」を見出しと誤認しない
                if line.lstrip().startswith("```"):
                    in_fence = not in_fence
                    continue
                if in_fence:
                    continue
                for m in HTML_ANCHOR_RE.finditer(line):
                    slugs.add(m.group(1).lower())
                m = HEADING_RE.match(line)
                if m:
                    slugs.add(slugify(m.group(1)))
    except OSError:
        pass
    return slugs


def check_kiro_url(url):
    """kiro.dev の URL の書式を検証し、問題があれば理由を返す（なければ None）。"""
    if PLACEHOLDER_RE.search(url):
        return None  # 雛形 URL は検査しない
    # フィード・llms.txt・sitemap は静的ファイルなので末尾スラッシュの規則は適用されない
    if os.path.splitext(url)[1]:
        return None
    if SLASH_REQUIRED_RE.match(url) and not url.endswith("/"):
        return ("kiro.dev の changelog / docs の URL は末尾スラッシュが必須"
                "（スラッシュなしは 301 リダイレクト・本文0バイト）")
    return None


def main():
    args = sys.argv[1:]
    check_anchors = "--check-anchors" in args
    paths_mode = "--paths" in args
    target_paths = []
    if paths_mode:
        # --paths 以降をすべて検査対象ファイルとして受け取る（フラグは --paths より前に置く）
        target_paths = args[args.index("--paths") + 1:]
        if not target_paths:
            print("❌ --paths にファイルを 1 つ以上指定してください")
            sys.exit(2)
    os.chdir(repo_root())

    if paths_mode:
        missing = [p for p in target_paths if not os.path.isfile(p)]
        if missing:
            for p in missing:
                print(f"❌ --paths 指定ファイルが存在しません: {p}")
            sys.exit(2)
        files = sorted(target_paths)
    else:
        files = (sorted(glob.glob("kiro-web-docs/**/*.md", recursive=True))
                 + ["README.md"]
                 + sorted(glob.glob(".github/*.md")))

    checked = 0
    url_checked = 0
    broken = []
    anchor_broken = []
    bad_urls = []
    sibling_links = []
    heading_cache = {}

    for f in files:
        if not paths_mode and (is_excluded(f) or f.endswith(".bak")):
            continue
        base = os.path.dirname(f)
        try:
            txt = open(f, encoding="utf-8").read()
        except OSError:
            continue
        # コードブロック内のリンク記法例・コマンド例の URL を誤検出しない
        txt = strip_code(txt)

        # kiro.dev の URL 書式検証（Markdown リンクと素の URL の両方）
        seen_urls = set()
        for m in BARE_URL_RE.finditer(txt):
            url = m.group(1).rstrip(".,)")
            if url in seen_urls:
                continue
            seen_urls.add(url)
            url_checked += 1
            reason = check_kiro_url(url)
            if reason:
                bad_urls.append((f, url, reason))
            if SIBLING_DOCS_RE.match(url) and not PLACEHOLDER_RE.search(url):
                sibling_links.append((f, url))

        for m in LINK_RE.finditer(txt):
            target = m.group(2).strip()
            # 同一ファイル内アンカー（`#...` のみのリンク）。目次リンクがここに該当する。
            if target.startswith("#"):
                if check_anchors:
                    anchor = target[1:]
                    checked += 1
                    if f not in heading_cache:
                        heading_cache[f] = collect_headings(f)
                    if anchor.lower() not in heading_cache[f]:
                        anchor_broken.append((f, target, anchor))
                continue
            if target.startswith(SKIP_PREFIX):
                continue
            if GITHUB_RELATIVE_RE.match(target.rstrip("/")):
                continue
            path, _, anchor = target.partition("#")
            if not path:
                continue
            resolved = os.path.normpath(os.path.join(base, path))
            # 除外パス（GitHub 非公開のローカル管理領域）へのリンクは検証対象外。
            # --paths ではローカル管理文書そのものを検査するため除外を適用しない。
            if not paths_mode and is_excluded(resolved):
                continue
            checked += 1
            if not os.path.exists(resolved):
                broken.append((f, target, resolved))
                continue
            # アンカー検査（任意）
            if check_anchors and anchor and resolved.endswith(".md"):
                # ⚠️ **非 ASCII（日本語）アンカーも検査する。**
                # IDE 版では「誤検知しやすい」として既定でスキップしていた結果、
                # **公開文書の壊れたアンカー4件を見逃していた**。スキップは復活させないこと。
                # 日本語・絵文字見出しへリンクするときは slug を手で組まず
                # `<a id="...">` の明示アンカーを使うのが安全。
                if resolved not in heading_cache:
                    heading_cache[resolved] = collect_headings(resolved)
                if anchor.lower() not in heading_cache[resolved]:
                    anchor_broken.append((f, target, anchor))

    print("=== kiro-web-docs 内部リンク整合チェック ===")
    print("")
    print(f"チェックした相対リンク数: {checked}")
    print(f"リンク切れ: {len(broken)} 件")
    for f, t, r in broken:
        print(f"  ❌ {f}: '{t}' -> {r}")

    print("")
    print(f"kiro.dev URL の書式チェック: {url_checked} 件中 {len(bad_urls)} 件が不正")
    for f, u, reason in bad_urls:
        print(f"  ❌ {f}: {u}")
        print(f"      → {reason}")

    if check_anchors:
        print("")
        print(f"アンカー検査: 切れ {len(anchor_broken)} 件（日本語アンカーも検査対象）")
        for f, t, a in anchor_broken:
            print(f"  ⚠️  {f}: '{t}'（見出し '#{a}' が見つからない）")

    print("")
    print(f"姉妹製品（IDE / CLI / 共有）ドキュメントへのリンク: {len(sibling_links)} 件")
    if sibling_links:
        print("   → 「別製品／共有ドキュメント」であることを本文で明示しているか確認してください")
        print("     （文面の検査は check-notation.py の担当。ここでは所在の一覧のみ）")
        for f, u in sibling_links:
            print(f"      {f}: {u}")

    print("")
    total_errors = len(broken) + len(bad_urls) + (len(anchor_broken) if check_anchors else 0)
    if total_errors > 0:
        print("❌ リンクチェックに失敗しました")
        sys.exit(1)
    print("✅ すべての内部リンクと kiro.dev URL の書式が有効です")
    sys.exit(0)


if __name__ == "__main__":
    main()
