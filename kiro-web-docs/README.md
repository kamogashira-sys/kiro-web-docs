# 猫でもわかるKiro Web アップデート情報 — サイト本体

**Kiro Web**（<https://app.kiro.dev>）に関する日本語ドキュメントの本体です。

> 🚧 **構築中**（Phase 1 完了時点）。本文は順次追加します。
>
> ⚠️ **Kiro Web は Preview 段階**です。仕様が変わることがあります。

---

## 📚 セクション構成

| セクション | 内容 |
|-----------|------|
| [00_information](00_information/) | 公式サイトの構造・情報源の使い分けと落とし穴 |
| [01_features](01_features/) | 機能詳細ガイド（6ページ） |
| [02_update](02_update/) | 更新履歴（changelog 全エントリ） |
| [03_deployment](03_deployment/) | 導入・運用（4ページ） |
| [04_reference](04_reference/) | リファレンス（検証可能な正準値・4ページ） |

**二層構成**: 機能の解説は `01_features/`、**値の一覧は `04_reference/`** に置いています。同じ値を2箇所に書かず、`01_features/` から `04_reference/` へリンクします。

---

## 🔖 Kiro Web にはバージョン番号がありません

Kiro IDE（`1.0.NNN`）や Kiro CLI と違い、**Kiro Web の更新にバージョン番号はありません**。公式 changelog のエントリは**日付とタイトル（スラッグ）**のみで識別されます。

| 項目 | 内容 |
|------|------|
| 更新の識別 | **日付（ISO）＋スラッグ** |
| changelog エントリ数 | **7**（2025-12-02 〜 2026-07-01） |
| 公式ドキュメントのページ数 | **20**（`llms.txt` の `## Web` 区分） |
| 提供形態 | ホスト型サービス（インストール不要） |
| 段階 | **Preview** |

> 版番号が存在しない**理由**は公式に説明がないため**未確認**です。

---

## 🐾 Kiro Web / Kiro IDE / Kiro CLI は別製品です

同名の機能（Specs・Steering・MCP など）でも仕様が異なることがあります。本サイトの各ページは **Kiro Web 版の仕様**を扱います。

| 対象 | サイト |
|------|-------|
| Kiro IDE | [kiro-ide-docs](https://github.com/kamogashira-sys/kiro-ide-docs) |
| Kiro CLI | [q-cli-docs](https://github.com/kamogashira-sys/q-cli-docs) |

---

## 🔗 公式情報源

- 公式ドキュメント（Web）: <https://kiro.dev/docs/web/>
- 公式 changelog（Web）: <https://kiro.dev/changelog/web/>
- Kiro Web 本体: <https://app.kiro.dev>

---

[← リポジトリのトップに戻る](../README.md)
