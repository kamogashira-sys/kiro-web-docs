# 00_information - 公式情報源の構造と使い分け

**Kiro Web の公式情報がどこにどんな形で置かれているのか、どう使い分けるのかをまとめたセクションです。**

---

## 📂 このセクションのファイル

| ファイル | 内容 |
|---------|------|
| [01_official-site-structure.md](01_official-site-structure.md) | **公式サイトの構造マップ**。`changelog/web/` の系列構造・docs の Web 区分（18ページ）・sitemap と `llms.txt` の違い・URL の作法・移転した5ページの記録 |
| [02_information-sources.md](02_information-sources.md) | **情報源の使い分けと落とし穴**。`.md` 版の壊れ方2種・折りたたみ節が HTML に無いこと・日付表記2種・公式ページ間の食い違い |

---

## 📢 Kiro Web とは

**Kiro Web** はブラウザから使う Kiro のインターフェースです（<https://app.kiro.dev>）。

| 項目 | 内容 |
|------|------|
| 提供形態 | ホスト型サービス（インストール不要） |
| 段階 | **一般提供（GA）**（2026-09-01） |
| 公式ドキュメント | <https://kiro.dev/docs/web/>（18ページ。snapshot: 2026-09-13） |
| 公式 changelog | <https://kiro.dev/changelog/web/>（19エントリ。2025-12-02 〜 2026-09-01） |

---

## 🔖 Kiro には複数のサーフェスがあります

公式の `llms.txt` は次の説明で始まります（2026-09-13 実測）。

> Kiro is an AI coding agent built around one unified agent harness: the same agent, sessions, and configuration across every surface. Use it in the Kiro IDE, the Kiro CLI, on the web, on mobile (iOS), with Kiro Crew for orchestrating teams of agents, and in any ACP-compatible editor.

> ⚠️ **この説明は書き換わっています。** 本サイトは以前
> 「Kiro is a coding agent with an IDE, CLI, and web interface.」を引用していましたが、
> **2026-09-13 実測の `llms.txt` にこの一文はありません**。
> 現行は **mobile (iOS)・Kiro Crew・ACP 互換エディタ**にも言及し、
> 「**すべてのサーフェスで同じエージェント・セッション・構成**」という説明になっています。

`llms.txt` の区分（`## Web`・`## CLI` など）に載っているページ数は次のとおりです（2026-09-13 実測・`docs/` の全 URL は 257 件）。

| サーフェス | 公式ドキュメント | ページ数 | 本サイトの扱い |
|----------|---------------|--------|--------------|
| **Web** | `/docs/web/` | **18** | **本サイトの対象** |
| IDE | `/docs/ide/` | 24 | 姉妹サイト [kiro-ide-docs](https://github.com/kamogashira-sys/kiro-ide-docs) |
| CLI | `/docs/cli/` | 35 | 姉妹サイト [q-cli-docs](https://github.com/kamogashira-sys/q-cli-docs) |
| Crew | `/docs/crew/` | 49 | 対象外 |
| Mobile（Preview） | `## Mobile - Preview` 区分 | — | 対象外 |

**これらは別製品です。** 同名機能でも仕様が異なることがあります。

> `Features`・`Privacy and Security` などの区分は**サーフェス横断の共通ページ**です。
> Kiro Web の出典にも含まれます（[01_official-site-structure.md](01_official-site-structure.md#共有ドキュメントサーフェス横断のページ)）。

---

## 関連セクション

- [01_features](../01_features/) - 機能詳細ガイド
- [02_update](../02_update/) - 更新履歴
- [03_deployment](../03_deployment/) - 導入・運用
- [04_reference](../04_reference/) - リファレンス
