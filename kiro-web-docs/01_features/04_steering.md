# Steering（エージェントを継続的に導く）

> **本ページは Kiro Web 版（<https://app.kiro.dev>）の仕様です。**
> Kiro IDE / Kiro CLI とは別製品です。**Kiro Web は Preview 段階**です。
>
> ただし Steering については、**公式が「3つのインターフェースで同じように動作する」と明記しています**（[下記](#3つのインターフェースで同じ動作をします公式明記)）。

**出典**: <https://kiro.dev/docs/web/steering/>（Page updated: May 27, 2026）

Steering は、**Markdown ファイルを通じてエージェントに永続的な知識を与える**仕組みです。毎回セッションで規約を説明する代わりに、確立したパターン・ライブラリ・標準に一貫して従わせられます。

---

## 📑 このページの内容

1. [ステアリングファイル](#ステアリングファイル)
2. [3つのインターフェースで同じ動作をします（公式明記）](#3つのインターフェースで同じ動作をします公式明記)
3. [コードレビューを通じて教える](#コードレビューを通じて教える)
4. [セッション中の操縦](#セッション中の操縦)

---

## ステアリングファイル

### 置き場所

公式は次のように説明しています。

> The agent automatically looks for steering files in the **`.kiro/steering/`** folder at the root of your repository.

| 項目 | 内容 |
|------|------|
| **場所** | リポジトリのルートの **`.kiro/steering/`** フォルダ |
| **形式** | **Markdown ファイル** |
| 読み込み | **エージェントが自動的に探します**（設定不要） |
| タイミング | **すべてのセッションの開始時**（[2026-05-07 のエントリ](../02_update/01_changelog.md#2026-05-07-introducing-kiro-web-preview)の記述） |

### 何を書くか（公式が挙げる用途）

公式は「define your team's standards, architecture decisions, and conventions」として、次を挙げています。

| 用途 |
|------|
| **コーディング規約とスタイルガイドライン** |
| **アーキテクチャパターンと設計判断** |
| **技術スタックの選好とバージョン要件** |
| **テストの進め方とカバレッジの期待値** |
| **PR の説明テンプレートとコミットメッセージの形式** |

> **PR の説明テンプレートとコミットメッセージ形式**も対象です。エージェントが作成する
> PR の書式を揃えたい場合はここに書きます。

公式はステアリングファイルの作成方法の詳細について `docs/steering`（**Kiro IDE / 共有のドキュメント — 別製品のページ**）を案内しています。

---

## 3つのインターフェースで同じ動作をします（公式明記）

公式は次のように明記しています。

> Steering files work the **same way** across Kiro IDE, Kiro CLI, and Kiro Web.

| 対象 | 動作 |
|------|------|
| Kiro IDE | **同じ** |
| Kiro CLI | **同じ** |
| Kiro Web | **同じ** |

> **これは公式が明記している「同一」です。** 本サイトは3製品を別物として扱う方針ですが、
> **公式が同一と書いているものについては、推測で差分を作りません。**
>
> [2026-05-07 のエントリ](../02_update/01_changelog.md#2026-05-07-introducing-kiro-web-preview)でも
> 公式は「using the same format that works in Kiro IDE and Kiro CLI」と説明しています。

同名でも仕様が異なる機能（例: [Specs](02_specs.md#kiro-ide-との違い公式が明記している3点)）とは扱いが違う点に注意してください。

---

## コードレビューを通じて教える

ステアリングファイル以外に、**プルリクエストへのフィードバックでもエージェントを導けます**。

公式が挙げているコメントの例:

- "always use our standard error handling"（常に標準のエラーハンドリングを使って）
- "follow our naming conventions"（命名規約に従って）

こうしたコメントを残すと、エージェントは**学習して、すべてのリポジトリの今後の作業にそのパターンを適用**します。

### ⚠️ 学習に影響するのはタスク作成者のフィードバックだけです

公式は次のように明記しています。

> **Only your feedback (the user who created the task) influences the agent's learnings.** Other reviewers' comments don't affect what the agent learns.

| 誰のコメントか | エージェントの学習への影響 |
|--------------|----------------------|
| **タスクを作成した本人** | **影響する** |
| **他のレビュアー** | **影響しません** |

> チームで運用する場合、**他のレビュアーがいくら指摘してもエージェントは学習しません。**
> 学習させたい規約は**タスク作成者がコメントする**か、**ステアリングファイルに書く**必要があります。
>
> なお `/kiro all` コマンドは「すべてのレビュアーのコメントに**対応する**」ものです
> （[06_repository-integration.md](06_repository-integration.md#pr-フィードバックへの対応)）。
> **「対応する」ことと「学習する」ことは別**という公式の区別です。

---

## セッション中の操縦

セッション中はチャットで**リアルタイムに**方向づけできます。公式が挙げている例:

- "Use the repository's existing error handling pattern"（リポジトリの既存のエラーハンドリングパターンを使って）
- "Follow the same approach as the UserService class"（UserService クラスと同じ方針で）
- "Make sure to add integration tests, not just unit tests"（単体テストだけでなく統合テストも追加して）

### モードによる違い

| モード | 操縦の仕方 |
|-------|----------|
| **Autonomous モード** | エージェントが**冒頭で明確化の質問**をする。**その回答がそのタスクのステアリングとして機能する** |
| **既定（協調）モード** | **一緒に反復しながら継続的に操縦できる** |

詳細は [01_agent-modes.md](01_agent-modes.md) を参照してください。

---

## 🔗 関連ページ

- [01_agent-modes.md](01_agent-modes.md) — 2つのモード（操縦の仕方が違う）
- [02_specs.md](02_specs.md) — Specs（公式が IDE との差分を明記している機能）
- [03_automations.md](03_automations.md) — Automations（誰もいない状態で実行されるため規約が重要）
- [06_repository-integration.md](06_repository-integration.md) — PR フィードバックへの対応
- 公式: <https://kiro.dev/docs/web/steering/>

---

[← 01_features に戻る](README.md)
