#!/usr/bin/env bash
# check-urls.sh - 公開文書に載せた外部 URL の到達性チェック（★外部サイトに依存）
#
# 使用方法:
#   scripts/kiro-web-docs/check-urls.sh              # 全件
#   scripts/kiro-web-docs/check-urls.sh --important  # 重要 URL のみ（切り分け用）
#
# ⚠️ **本スクリプトは外部サイトにアクセスします。**
#    レート制限・一時障害で失敗しうるため `make check-kiro-web-all` には**含めません**。
#
# 作法（実測で確認・F-W11）:
#   - **末尾スラッシュ必須**: changelog も docs も、無しは 301（本文0バイト）。
#     したがって **`-L`（リダイレクト追随）を使わない**。301 が返ったら
#     「本サイトの URL 表記が誤っている」ことを意味するので失敗にする。
#   - **User-Agent 必須**: 空文字の明示指定は 403。`-A "Mozilla/5.0"` を付ける。
#
# 除外（誤検知を避けるため）:
#   - **雛形 URL**（`<slug>`・`（パス）` 等のプレースホルダを含むもの）。
#     手順書・テンプレートに意図的に存在するため、実 URL として叩くと必ず失敗する。
#     ⚠️ Phase 1 の暫定検査でこの誤検知を 3 件出した実例がある。
#   - ローカル管理領域（work_plans / 05_meta / 06_embedded-docs / work_records）
#
# fail-safe:
#   - **ネットワークそのものが不通なら exit 0 ＋ 案内**（CI やオフラインで赤くしない）
#   - 到達性の失敗（404・301 等）は exit 1

set -uo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$REPO_ROOT" || exit 1

UA="Mozilla/5.0"
IMPORTANT_ONLY=0
[ "${1:-}" = "--important" ] && IMPORTANT_ONLY=1

# 重要 URL（全件チェックが外部要因で落ちたときの切り分け用）
IMPORTANT=(
  "https://kiro.dev/docs/web/"
  "https://kiro.dev/changelog/web/"
  "https://app.kiro.dev"
  "https://kiro.dev/llms.txt"
  "https://kiro.dev/sitemap.xml"
)

echo "=== kiro-web-docs 外部 URL 到達性チェック ==="
echo ""

# ------------------------------------------------------------
# ネットワーク疎通の事前確認（fail-safe）
# ------------------------------------------------------------
if ! curl -sS --max-time 15 -A "$UA" -o /dev/null "https://kiro.dev/"; then
  echo "⚠️  ネットワークに到達できませんでした（**未検証**です）"
  echo "   → これは「URL が有効であることを検証した」ではありません"
  echo "   オフライン環境・プロキシ・一時障害の可能性があります"
  exit 0
fi

# ------------------------------------------------------------
# 検査対象 URL の収集
# ------------------------------------------------------------
if [ "$IMPORTANT_ONLY" -eq 1 ]; then
  printf '%s\n' "${IMPORTANT[@]}" > /tmp/kw_urls.txt
  echo "重要 URL のみを検査します（${#IMPORTANT[@]} 件）"
else
  # 公開文書から http(s) URL を抽出する。
  # ⚠️ 雛形 URL（プレースホルダを含むもの）を除外する。
  python3 - > /tmp/kw_urls.txt <<'PY'
import glob, os, re

EXCLUDE = ("05_meta", "06_embedded-docs", "work_plans", "work_records")

# 雛形 URL（プレースホルダ入り）。実 URL として叩くと必ず失敗する。
PLACEHOLDER = re.compile(r"[<>{}]|（|\((?:スラッグ|パス|slug|path)\)")

# ⚠️ **正規表現の断片**を URL として拾わない。
#    手順書には `grep -oE 'https://kiro\.dev/changelog/web/[^<]*'` のような
#    コマンド例があり、`\.` や `[^<]*` を含む文字列が URL に見える（実測で1件）。
REGEX_FRAGMENT = re.compile(r"\\\.|\[\^|\.\*|\[0-9\]|\\d")

# ⚠️ **他社・他サービスのエンドポイント**は到達性検査の対象にしない。
#    公式の設定例に出てくる外部 API（302 を返す）などを本サイトの誤りとして
#    報告すると、直せないものを永久に赤くすることになる（実測で1件）。
#    許可ドメイン一覧のドメイン（73件）も「叩いて確認する対象」ではない。
THIRD_PARTY = re.compile(
    r"^https?://(?!(?:kiro\.dev|app\.kiro\.dev|github\.com/kamogashira-sys|"
    r"github\.com/kirodotdev))")

files = sorted(glob.glob("kiro-web-docs/**/*.md", recursive=True))
files = [f for f in files if not any(x in f for x in EXCLUDE)]
files += ["README.md"] + sorted(glob.glob(".github/*.md"))

urls = set()
for f in files:
    if not os.path.isfile(f):
        continue
    # コードブロックは除外しない（手順のコマンド内の URL も到達性を見たい）が、
    # 雛形 URL・正規表現の断片・他社サービスはここで落とす。
    for m in re.finditer(r"https?://[^\s<>()\[\]\"'`|]+", open(f, encoding="utf-8").read()):
        u = m.group(0).rstrip(".,;:)")
        if PLACEHOLDER.search(u) or REGEX_FRAGMENT.search(u) or THIRD_PARTY.match(u):
            continue
        urls.add(u)

for u in sorted(urls):
    print(u)
PY
  echo "公開文書から $(wc -l < /tmp/kw_urls.txt) 件の URL を抽出しました"
  echo "（雛形 URL（プレースホルダ入り）は除外しています）"
fi

echo ""

fail=0
ok=0
declare -a failures=()

while IFS= read -r url; do
  [ -z "$url" ] && continue
  # ⚠️ `-L` を使わない。301 は「本サイトの URL 表記が誤っている」ことを意味する。
  code=$(curl -sS --max-time 20 -o /dev/null -w '%{http_code}' -A "$UA" "$url" 2>/dev/null || echo "000")
  case "$code" in
    200|204)
      ok=$((ok + 1))
      ;;
    301|302|307|308)
      failures+=("$code $url  → リダイレクトされました（末尾スラッシュの有無を確認してください）")
      fail=1
      ;;
    000)
      failures+=("--- $url  → 接続できませんでした（一時障害の可能性）")
      fail=1
      ;;
    *)
      failures+=("$code $url")
      fail=1
      ;;
  esac
done < /tmp/kw_urls.txt

echo "到達 OK: $ok 件"
if [ ${#failures[@]} -gt 0 ]; then
  echo ""
  echo "❌ 到達できなかった URL: ${#failures[@]} 件"
  for x in "${failures[@]}"; do
    echo "   - $x"
  done
  echo ""
  echo "❌ URL 到達性チェックに失敗しました"
  echo "   （301 の場合は末尾スラッシュを追加してください — changelog も docs も必須）"
  exit 1
fi

echo ""
echo "✅ すべての外部 URL に到達できました"
exit 0
