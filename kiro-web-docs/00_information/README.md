# 00_information - 公式情報源の構造と使い分け

**Kiro Web の公式情報がどこにどんな形で置かれているのか、どう使い分けるのかをまとめたセクションです。**

---

## 📂 このセクションのファイル

| ファイル | 内容 |
|---------|------|
| [01_official-site-structure.md](01_official-site-structure.md) | **公式サイトの構造マップ**。`changelog/web/` の系列構造・docs の Web 区分（17ページ）・sitemap と `llms.txt` の違い・URL の作法・移転した6ページの記録 |
| [02_information-sources.md](02_information-sources.md) | **情報源の使い分けと落とし穴**。`.md` 版の壊れ方2種・折りたたみ節が HTML に無いこと・日付表記2種・公式ページ間の食い違い |

---

## 📢 Kiro Web とは

**Kiro Web** はブラウザから使う Kiro のインターフェースです（<https://app.kiro.dev>）。

| 項目 | 内容 |
|------|------|
| 提供形態 | ホスト型サービス（インストール不要） |
| 段階 | **一般提供（GA）**（2026-09-01） |
| 公式ドキュメント | <https://kiro.dev/docs/web/>（17ページ。snapshot: 2026-10-25） |
| 公式 changelog | <https://kiro.dev/changelog/web/>（22エントリ。2025-12-02 〜 2026-10-12） |

---

## 🔖 Kiro には複数のサーフェスがあります

公式の `llms.txt` は次の説明で始まります（2026-09-13 実測）。

> Kiro is an AI coding agent built around one unified agent harness: the same agent, sessions, and configuration across every surface. Use it in the Kiro IDE, the Kiro CLI, on the web, on mobile (iOS), with Kiro Crew for orchestrating teams of agents, and in any ACP-compatible editor.

> ⚠️ **この説明は書き換わっています。** 本サイトは以前
> 「Kiro is a coding agent with an IDE, CLI, and web interface.」を引用していましたが、
> **2026-09-13 実測の `llms.txt` にこの一文はありません**。
> 現行は **mobile (iOS)・Kiro Crew・ACP 互換エディタ**にも言及し、
> 「**すべてのサーフェスで同じエージェント・セッション・構成**」という説明になっています。

`llms.txt` の区分（`## Web`・`## CLI` など）に載っているページ数は次のとおりです（2026-10-25 実測・`llms.txt` の行数は 271 行、`docs/` の一意 URL は 262 件。2026-09-13 は 257 行・248 件）。

| サーフェス | 公式ドキュメント | ページ数 | 本サイトの扱い |
|----------|---------------|--------|--------------|
| **Web** | `/docs/web/` | **17**（2026-09-13 は 18） | **本サイトの対象** |
| IDE | `## IDE 1.x` 区分 | 25 | 姉妹サイト [kiro-ide-docs](https://github.com/kamogashira-sys/kiro-ide-docs) |
| CLI | `## CLI` 区分 | 37 | 姉妹サイト [q-cli-docs](https://github.com/kamogashira-sys/q-cli-docs) |
| Crew | `## Crew` 区分 | 48 | 対象外 |
| Mobile（Preview） | `## Mobile - Preview` 区分 | 1 | 対象外（[下記](#kiro-mobile-について)） |

**これらは別製品です。** 同名機能でも仕様が異なることがあります。

> `Features`・`Privacy and Security` などの区分は**サーフェス横断の共通ページ**です。
> Kiro Web の出典にも含まれます（[01_official-site-structure.md](01_official-site-structure.md#共有ドキュメントサーフェス横断のページ)）。

---

## Kiro Mobile について

公式は Kiro の説明で **mobile (iOS)** にも言及しています（`llms.txt` の冒頭）。本サイトは Kiro Mobile を**対象外**としていますが、2026-10-25 に公式の記載を確認した結果を記録します。

| 項目 | 内容（2026-10-25 実測） |
|------|----------------------|
| 公式ドキュメント | `llms.txt` の **`## Mobile - Preview`** 区分の **1 ページのみ**: <https://kiro.dev/docs/mobile/>（`Page updated: August 4, 2026`。2026-10-04 から更新なし） |
| ページの内容 | 「Use Kiro on the go with the iOS app. Documentation coming soon.」。**Apple TestFlight の early access** で、<https://kiro.dev/mobile/> から request access する、と書かれている |
| 詳細な Mobile ドキュメント | 区分の説明に「detailed mobile documentation is not yet available」とある（**まだ無い**） |
| changelog の系列 | **無い**（sitemap の `changelog/` 配下は `cli`・`crew`・`general`・`govcloud`・`ide`・`models`・`web` のみ） |
| 対応要件（公式の製品ページ <https://kiro.dev/mobile/>） | **iOS 26 以降**と、**Kiro Pro・Pro+・Pro Max・Power のいずれかのアカウント**が必要。公式の導入ページ <https://kiro.dev/docs/getting-started/installation/> は「Kiro Mobile は Android では使えない」と書いている |
| 更新の配布 | 公式の導入ページは「更新は TestFlight 経由で配布される」と書いている（TestFlight アプリから新しいビルドをインストールする） |
| バージョン番号 | 確認した範囲（`docs/mobile`・製品ページ <https://kiro.dev/mobile/>・導入ページ・`llms.txt`・sitemap・Atom フィード）に **Mobile の版番号の記載はありません** |
| 本サイトでの扱い | **対象外**。公式が Kiro Web と並べて書いている箇所（[Cloud Sessions](../01_features/07_cloud-sessions.md) の対比表など）だけを参照する |

> Mobile の更新を追う手段（changelog・版番号）が公式に見当たらないため、本サイトは Mobile の「最新バージョン」を記載できません。**公式に確認できない事項は未確認**として扱います。

---

## 関連セクション

- [01_features](../01_features/) - 機能詳細ガイド
- [02_update](../02_update/) - 更新履歴
- [03_deployment](../03_deployment/) - 導入・運用
- [04_reference](../04_reference/) - リファレンス
