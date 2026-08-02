# Makefile - kiro-web-docs 検証ツール一括実行
#
# 使用方法:
#   make                        # ヘルプを表示
#   make check-kiro-web-quick   # 執筆中の常用（links / structure のみ）
#   make check-kiro-web-all     # コミット前・公開前（ネットワーク不要のもの全部）
#   make check-kiro-web-ignore  # 公開範囲チェック（コミット前に必須・exit 0 必須）
#
# ⚠️ 「exit 0」は「検証して合格した」を必ずしも意味しません:
#   - 網羅性チェックは一次情報 HTML が無いとスキップして成功扱いになります
#     （クローン直後・CI では未検証。出力に「未検証です」と表示します）
#   - 外部依存のターゲット（-urls / -freshness）は all に含まれません
#   検証スクリプトを新規作成・改修したときは、意図的に文書を壊して検出されることを
#   確認してください（ネガティブテスト）。手順は .github/WORKFLOW.md §6 を参照。
#
# 📌 存在しないターゲットは書きません（実装済みのものだけを並べます）。
#    未実装分はヘルプの「Phase 3 で追加予定」に列挙しています。

.DEFAULT_GOAL := help

.PHONY: help \
        check-kiro-web-all check-kiro-web-quick check-kiro-web-ignore \
        check-kiro-web-links check-kiro-web-structure check-kiro-web-coverage \
        check-kiro-web-counts check-kiro-web-consistency \
        extract-kiro-web-changelog

SCRIPTS := ./scripts/kiro-web-docs

# 一次情報（取得済み HTML）の置き場。網羅性チェックで使う。
# 既定はリポジトリ内のスナップショット置き場（ローカル管理・.gitignore 対象）。
# 未指定・不在ならチェックはスキップする（ネットワークに依存させない）。
# スナップショットを持たない環境（CI・クローン直後）ではスキップされ、
# 「exit 0 = 網羅性を検証した」ではないことに注意する。
#
# ⚠️ **IDE 版は 06_embedded-docs 直下フラットだが、Web 版は日付ディレクトリ配下の入れ子**
#    （06_embedded-docs/YYYYMMDD/changelog/*.html）。したがって 06_embedded-docs を
#    そのまま渡しても HTML は見つからない。**最新の日付ディレクトリを自動解決**する。
#    明示指定したいときは HTML_DIR=<dir> を渡す。
SNAPSHOT_ROOT ?= kiro-web-docs/06_embedded-docs
HTML_DIR ?= $(shell ls -d $(SNAPSHOT_ROOT)/*/changelog 2>/dev/null | sort | tail -1)
# docs 側のスナップショット（件数系の正準値を公式の実体と照合するのに使う）
DOCS_HTML_DIR ?= $(shell ls -d $(SNAPSHOT_ROOT)/*/docs 2>/dev/null | sort | tail -1)

# ------------------------------------------------------------
# ヘルプ
# ------------------------------------------------------------
help:
	@echo "=== kiro-web-docs 検証ツール ==="
	@echo ""
	@echo "まとめて実行:"
	@echo "  make check-kiro-web-all        # 全チェック（ネットワーク不要のもの全部）"
	@echo "  make check-kiro-web-quick      # 高速チェック（links / structure のみ。執筆中の確認用）"
	@echo "  make check-kiro-web-ignore     # 公開範囲チェック（コミット前に必須）"
	@echo ""
	@echo "個別に実行（ネットワーク不要）:"
	@echo "  make check-kiro-web-links      # 内部リンク実在＋アンカー＋kiro.dev URL 書式"
	@echo "                                 #   changelog も docs も末尾スラッシュ必須（F-W11）"
	@echo "  make check-kiro-web-structure  # 構成・H1・公開境界・Web 版スコープ明示・出典 URL"
	@echo "  make check-kiro-web-coverage   # 一次情報との突き合わせ"
	@echo "                                 #   スラッグ・日付・タイトル・本文非空・"
	@echo "                                 #   **折りたたみ項目数**（宣言件数と実際の行数の両方）"
	@echo "                                 #   HTML_DIR=<dir> で一次情報の場所を指定"
	@echo "                                 #   （既定 $(HTML_DIR)）"
	@echo "  make check-kiro-web-counts     # 件数系の正準値（S1・S2・S5・S6・S7・S12）"
	@echo "                                 #   節見出しの宣言件数と表の実体・内訳と合計・"
	@echo "                                 #   公式 HTML との一致（DOCS_HTML_DIR があれば）"
	@echo "  make check-kiro-web-consistency # 上限値の水平展開（S8〜S11・S13・S14）・"
	@echo "                                 #   食い違い注記の対称性（F-W20）・出典日の記載"
	@echo ""
	@echo "保守用:"
	@echo "  make extract-kiro-web-changelog INDEX=<html>          # 索引からスラッグ・日付・タイトル"
	@echo "  make extract-kiro-web-changelog ENTRY=\"<html...>\"     # 本文・粒度・折りたたみ項目"
	@echo "    ARGS=--text で人が読む形式。折りたたみ節は RSC のみにあるため必ず本スクリプトを使う"
	@echo ""
	@echo "Phase 3 で追加予定:"
	@echo "  make check-kiro-web-notation   # 表記規約（IDE/CLI 混入・存在しない版番号の創作）"
	@echo "  make check-kiro-web-urls       # 外部 URL の到達性（★外部依存・all には含めない）"
	@echo "  make check-kiro-web-freshness  # 新エントリ検知（★外部依存・all には含めない）"

# ------------------------------------------------------------
# まとめて実行
# ------------------------------------------------------------
# 全チェック。**外部サイトに依存するものは含めない**（-urls / -freshness）。
# ネットワーク障害やレート制限で CI が赤くなるのを避けるため、それらは
# push / nightly / 手動でのみ実行する（先行2サイトと同じ運用）。
# G3（公開判定）ではこのターゲットの exit 0 を条件とする。
check-kiro-web-all: check-kiro-web-links check-kiro-web-structure check-kiro-web-coverage \
                    check-kiro-web-counts check-kiro-web-consistency
	@echo ""
	@echo "✅ kiro-web-docs 全チェックが完了しました"
	@echo "   （外部 URL の到達性と新エントリ検知は別ターゲットです）"

# 高速チェック。執筆中に繰り返し回す用（構造とリンクだけを見る）。
# コミット前は check-kiro-web-all を使う。
check-kiro-web-quick: check-kiro-web-links check-kiro-web-structure
	@echo ""
	@echo "✅ kiro-web-docs 高速チェックが完了しました"
	@echo "   （これは全チェックではありません。コミット前に make check-kiro-web-all を実行してください）"

# 公開範囲チェック。ローカル管理対象が GitHub に出ないことを機械確認する。
# 各コミット前に実行し exit 0 を必須とする（作業計画書 Phase 1-5 / 4-1 / 5-3）。
check-kiro-web-ignore:
	@$(SCRIPTS)/check-ignore.sh

# ------------------------------------------------------------
# 個別ターゲット（ネットワーク不要）
# ------------------------------------------------------------
# 内部リンクの実在・アンカーの実在（日本語含む）・kiro.dev URL の書式
# （changelog も docs も末尾スラッシュ必須 — F-W11）
check-kiro-web-links:
	@$(SCRIPTS)/check-links.py --check-anchors

# ディレクトリ構成（公開5セクション・README の有無・H1 見出し・G1 のファイル軸・
# ローカル管理領域へのリンク禁止・本文ページの Web 版スコープ明示・出典 URL）
check-kiro-web-structure:
	@$(SCRIPTS)/check-structure.py

# changelog を一次情報と突き合わせる（スラッグの網羅性・日付・公式タイトル・本文非空・
# **W-L3 の折りたたみ項目数**）。折りたたみ項目は素の HTML に存在せず RSC のみにあるため
# 転記漏れが静かに起きる。一次情報 HTML が無い環境（CI 等）ではスキップして成功扱いにするが、
# 「未検証です」と明示表示する。
check-kiro-web-coverage:
	@if [ -n "$(HTML_DIR)" ] && [ -d "$(HTML_DIR)" ]; then \
	    $(SCRIPTS)/check-coverage.py --html-dir "$(HTML_DIR)"; \
	else \
	    echo "⚠️  網羅性チェックをスキップ: $(SNAPSHOT_ROOT) に一次情報のスナップショットがありません"; \
	    echo "   → これは「検証して合格した」ではありません（**未検証**です）"; \
	    echo "   取得手順は kiro-web-docs/05_meta/10_update-guide.md §5 を参照"; \
	fi

# 件数系の正準値（S1・S2・S5・S6・S7・S12）を**実体から数えて**文書の記述と突き合わせる。
# 「表を1行増やしたのに見出しの件数を直し忘れた」を落とす。
# docs の HTML スナップショットがあれば、正準値が公式の実体と一致するかも検証する
# （無い場合はその部分をスキップし「未検証です」と表示する）。
check-kiro-web-counts:
	@if [ -n "$(DOCS_HTML_DIR)" ] && [ -d "$(DOCS_HTML_DIR)" ]; then \
	    $(SCRIPTS)/check-counts.py --html-dir "$(DOCS_HTML_DIR)"; \
	else \
	    $(SCRIPTS)/check-counts.py; \
	fi

# 上限・保持期間系の正準値（S8〜S11・S13・S14）が**複数ページで食い違っていないか**を見る。
# check-counts.py が「表の実体 vs 宣言件数」を見るのに対し、こちらは
# 「文書 A の値 vs 文書 B の値 vs SSoT 定数」を見る（水平展開漏れの検出）。
# 併せて Free Tier の食い違い注記の対称性（F-W20）と、本文ページの出典日も検証する。
check-kiro-web-consistency:
	@$(SCRIPTS)/check-consistency.py

# ------------------------------------------------------------
# 保守用（取得済み HTML を対象にするため check-*-all には含めない）
# ------------------------------------------------------------
# 公式 changelog の HTML から一次情報（スラッグ・日付・粒度・折りたたみ項目）を抽出する。
# ⚠️ 折りたたみ節（Improvements / Fixes）は**素の HTML に存在しない**（hidden な空 div）。
#    RSC ペイロードから取るため、grep では代用できない。
# HTML の取得手順は kiro-web-docs/05_meta/10_update-guide.md §5 を参照
# （末尾スラッシュ必須・-A "Mozilla/5.0" が必要）。
INDEX ?=
ENTRY ?=
ARGS ?=
extract-kiro-web-changelog:
	@if [ -z "$(INDEX)" ] && [ -z "$(ENTRY)" ]; then \
	    echo "使い方: make extract-kiro-web-changelog INDEX=\"<索引html>\" [ARGS=--text]"; \
	    echo "        make extract-kiro-web-changelog ENTRY=\"<エントリhtml...>\" [ARGS=--text]"; \
	    exit 2; \
	fi
	@if [ -n "$(INDEX)" ]; then $(SCRIPTS)/extract-changelog.py --index $(INDEX) $(ARGS); fi
	@if [ -n "$(ENTRY)" ]; then $(SCRIPTS)/extract-changelog.py --entry $(ENTRY) $(ARGS); fi
