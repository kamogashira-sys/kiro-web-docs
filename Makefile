# Makefile - kiro-web-docs 検証ツール一括実行
#
# 使用方法:
#   make                        # ヘルプを表示
#   make check-kiro-web-ignore  # 公開範囲チェック（コミット前に必須・exit 0 必須）
#
# ⚠️ 「exit 0」は「検証して合格した」を必ずしも意味しません:
#   - 網羅性チェックは一次情報 HTML が無いとスキップして成功扱いになります
#     （クローン直後・CI では未検証。出力に警告を表示します）
#   - 外部依存のターゲット（-urls / -freshness）は all に含まれません
#   検証スクリプトを新規作成・改修したときは、意図的に文書を壊して検出されることを
#   確認してください（ネガティブテスト）。手順は .github/WORKFLOW.md §6 を参照。
#
# 📌 本ファイルは Phase 1 時点の版です。検証スクリプトの実装に合わせて
#    Phase 2a・Phase 3 でターゲットを追加します（存在しないターゲットは書きません）。

.DEFAULT_GOAL := help

.PHONY: help check-kiro-web-ignore extract-kiro-web-changelog

SCRIPTS := ./scripts/kiro-web-docs

# 一次情報（取得済み HTML）の置き場。網羅性チェックで使う。
# 既定はリポジトリ内のスナップショット置き場（ローカル管理・.gitignore 対象）。
# 未指定・不在ならチェックはスキップする（ネットワークに依存させない）。
# スナップショットを持たない環境（CI・クローン直後）ではスキップされ、
# 「exit 0 = 網羅性を検証した」ではないことに注意する。
# ⚠️ IDE 版は 06_embedded-docs 直下フラットだが、Web 版は日付ディレクトリ配下の入れ子。
HTML_DIR ?= kiro-web-docs/06_embedded-docs

# ------------------------------------------------------------
# ヘルプ
# ------------------------------------------------------------
help:
	@echo "=== kiro-web-docs 検証ツール ==="
	@echo ""
	@echo "利用可能なターゲット:"
	@echo "  make check-kiro-web-ignore     # 公開範囲チェック（コミット前に必須）"
	@echo "                                 #   ローカル管理4系統の除外・公開対象の非除外・"
	@echo "                                 #   トラック状況・ローカル絶対パスの混入を検査"
	@echo ""
	@echo "保守用:"
	@echo "  make extract-kiro-web-changelog INDEX=<html>          # 索引からスラッグ・日付・タイトル"
	@echo "  make extract-kiro-web-changelog ENTRY=\"<html...>\"     # 本文・粒度・折りたたみ項目"
	@echo "    ARGS=--text で人が読む形式。折りたたみ節は RSC のみにあるため必ず本スクリプトを使う"
	@echo ""
	@echo "Phase 2a で追加予定:"
	@echo "  make check-kiro-web-links      # 内部リンク実在＋アンカー＋kiro.dev URL 書式"
	@echo "  make check-kiro-web-structure  # ディレクトリ構成・H1・公開境界"
	@echo "  make check-kiro-web-coverage   # 一次情報との突き合わせ（スラッグ・日付・折りたたみ項目数）"
	@echo ""
	@echo "Phase 3 で追加予定:"
	@echo "  make check-kiro-web-all        # 全チェック（ネットワーク不要のもの全部）"
	@echo "  make check-kiro-web-quick      # 高速チェック（links / structure のみ）"
	@echo "  make check-kiro-web-counts     # 正準値（件数系 SSoT）の水平展開"
	@echo "  make check-kiro-web-consistency # 上限値・保持期間系 SSoT・食い違い注記"
	@echo "  make check-kiro-web-notation   # 表記規約（IDE/CLI 混入・存在しない版番号の創作）"
	@echo "  make check-kiro-web-urls       # 外部 URL の到達性（★外部依存・all には含めない）"
	@echo "  make check-kiro-web-freshness  # 新エントリ検知（★外部依存・all には含めない）"

# ------------------------------------------------------------
# 公開範囲チェック
# ------------------------------------------------------------
# ローカル管理対象が GitHub に出ないことを機械確認する。
# 各コミット前に実行し exit 0 を必須とする（作業計画書 Phase 1-5 / 4-1 / 5-3）。
check-kiro-web-ignore:
	@$(SCRIPTS)/check-ignore.sh

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
