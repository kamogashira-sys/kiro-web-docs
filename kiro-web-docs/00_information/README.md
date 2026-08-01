# 00_information - 公式情報源の構造と使い分け

**Kiro Web の公式情報がどこにどんな形で置かれているのか、どう使い分けるのかをまとめたセクションです。**

> 🚧 **構築中**（Phase 1 完了時点）。本文は Phase 2b で追加します。

---

## 📂 このセクションのファイル

| ファイル | 内容 |
|---------|------|
| `01_official-site-structure.md` | **公式サイトの構造マップ**。`changelog/web/` 系列・docs の Web 区分・sitemap・`llms.txt` の関係 |
| `02_information-sources.md` | **情報源の使い分けと落とし穴**。`.md` companion の壊れ方・RSC ペイロード・日付形式の2種 |

---

## 📢 Kiro Web とは

**Kiro Web** はブラウザから使う Kiro のインターフェースです（<https://app.kiro.dev>）。

| 項目 | 内容 |
|------|------|
| 提供形態 | ホスト型サービス（インストール不要） |
| 段階 | **Preview** |
| 公式ドキュメント | <https://kiro.dev/docs/web/>（20ページ） |
| 公式 changelog | <https://kiro.dev/changelog/web/>（7エントリ） |

---

## 🔖 3つのインターフェース

公式の `llms.txt` は次の説明で始まります。

> Kiro is a coding agent with an IDE, CLI, and web interface.

| インターフェース | 公式ドキュメント | 本サイトの扱い |
|----------------|---------------|--------------|
| **Web** | `/docs/web/`（20ページ） | **本サイトの対象** |
| IDE | `/docs/`（117ページ） | 姉妹サイト [kiro-ide-docs](https://github.com/kamogashira-sys/kiro-ide-docs) |
| CLI | `/docs/cli/`（101ページ） | 姉妹サイト [q-cli-docs](https://github.com/kamogashira-sys/q-cli-docs) |

**3つは別製品です。** 同名機能でも仕様が異なることがあります。

---

## 関連セクション

- [01_features](../01_features/) - 機能詳細ガイド
- [02_update](../02_update/) - 更新履歴
- [03_deployment](../03_deployment/) - 導入・運用
- [04_reference](../04_reference/) - リファレンス
