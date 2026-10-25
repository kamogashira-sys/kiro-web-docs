# Steering（エージェントを継続的に導く）

> **本ページは Kiro Web 版（<https://app.kiro.dev>）の仕様です。**
> Kiro IDE / Kiro CLI とは別製品です。**Kiro Web は [2026-09-01 に一般提供（GA）になりました](https://kiro.dev/changelog/web/kiro-web-is-now-generally-available/)。**
>
> ⚠️ **かつて公式にあった「3つのインターフェースで同じように動作する」という一文は、
> 移転先の現行ページにはありません**（[下記](#3つのインターフェースの関係公式の記述は移転で変わりました)）。

**出典**: <https://kiro.dev/docs/steering/>（Page updated: October 21, 2026・**移転先。旧 `docs/web/steering/` は2026-08-12以前は Page updated: May 27, 2026**）

Steering は、**Markdown ファイルを通じてエージェントに永続的な知識を与える**仕組みです。毎回セッションで規約を説明する代わりに、確立したパターン・ライブラリ・標準に一貫して従わせられます。

---

## 📑 このページの内容

1. [ステアリングファイル](#ステアリングファイル)
2. [3つのインターフェースの関係（公式の記述は移転で変わりました）](#3つのインターフェースの関係公式の記述は移転で変わりました)
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

公式は Steering を「**Guide Kiro's AI with persistent context through markdown documents that define your standards, architecture, and conventions**」（ページの説明文）と位置づけ、次のように述べています。

> Steering gives Kiro persistent knowledge about your project through markdown files. Instead of explaining your conventions in every chat, steering files ensure Kiro consistently follows your established patterns, libraries, and standards.

用途として挙げられているのは次のとおりです。

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

## 3つのインターフェースの関係（公式の記述は移転で変わりました）

### ⚠️ かつての「same way」の一文は現行ページにありません

本サイトはこれまで、次の一文を**現行の公式ドキュメントの記述**として掲載していました。

> Steering files work the **same way** across Kiro IDE, Kiro CLI, and Kiro Web.

**2026-09-13 の実測で、この一文は移転先の <https://kiro.dev/docs/steering/>（Page updated: October 21, 2026）に存在しないことを確認しました**（2026-10-02 版・2026-10-21 版でも存在しません）。
`same way`・`work the same`・`across Kiro IDE`・`Kiro CLI, and Kiro Web`・`identically` のいずれも 0 件でした。
2026-10-02 版では `same way` が 1 件現れますが、これは別の文（「On Kiro Web, you can steer autonomous-mode tasks the same way — …」・[下記](#モードによる違い)）の一部で、Steering ファイルが3つのインターフェースで同じように動作するという一文ではありません。

この一文が確認できる場所は次のとおりです。

| 出典 | 状態（2026-09-13 実測） |
|------|--------------------|
| 旧 `docs/web/steering/`（本サイトの 2026-08-01 snapshot） | **あった**（移転前のページ） |
| <https://kiro.dev/docs/steering/>（移転先・現行） | **無い** |
| 公式ブログ <https://kiro.dev/blog/introducing-kiro-web/> | **ある** |

> **ブログにあることを根拠に「公式が明記している」とは書きません。**
> 本サイトはブログを[背景の補足に限る](../00_information/01_official-site-structure.md#関連ブログ3本)方針です。
> **一文が消えた理由は公式に説明がないため未確認**です。「同一でなくなった」という意味なのか、
> 移転時に落ちただけなのかは**判断できません**。

### 現在も確認できるのは「同じ形式」までです

[2026-05-07 のエントリ](../02_update/01_changelog.md#2026-05-07-introducing-kiro-web-preview)には、
現在も次の記述があります（changelog エントリは書き換わらない一次情報です）。

> using the same **format** that works in Kiro IDE and Kiro CLI

**「同じ形式（format）」までは公式に確認できます。** 動作全体が同一であるという記述は、
現行の公式ドキュメントには**ありません**。

### 現行ページは「差分の表」を持っています

移転先のページは、一文で「同じ」と述べる代わりに、**サーフェスごとの対応表**を掲載しています（公式の表をそのまま転記）。

| Capability | IDE | CLI | **Web** | Mobile |
|-----------|:---:|:---:|:-------:|:------:|
| `.kiro/steering/`（リポジトリ内） | ✓ | ✓ | **✓** | ✓ |
| `~/.kiro/steering/`（ローカルの個人設定） | ✓ | ✓ | **—** | — |
| Upload local steering to cloud configuration | Opt-in | Opt-in | **✓** | — |
| Generate foundation files via UI | ✓ | — | **—** | — |
| Inclusion modes | ✓ | V3: full; V1/V2: partial | **✓** | ✓ |
| `AGENTS.md` support | ✓ | ✓ | **✓** | ✓ |

> ⚠️ **2026-10-02 版で表の2行が変わりました。**
> 3行目は「Cloud steering managed in Web settings（IDE —・CLI —・Web ✓）」から
> 「**Upload local steering to cloud configuration**（IDE **Opt-in**・CLI **Opt-in**・Web ✓）」に、
> 5行目は「Inclusion modes (always, fileMatch, manual)」から「**Inclusion modes**」（CLI 欄が **V3: full; V1/V2: partial**）に変わりました。
> **Web の欄はどちらも ✓ のままです。** CLI の欄の詳細は別製品（Kiro CLI）の仕様のため、本サイトでは扱いません。

**Kiro Web で対応していないのは 2 項目**です。

| 項目 | Web での扱い |
|------|-----------|
| **`~/.kiro/steering/`** | **非対応**。公式は「On Web, "Global steering" refers to your local `~/.kiro/steering/` directory, **which the cloud sandbox cannot read**」と説明しています。**クラウドサンドボックスはローカルのディレクトリを読めません**。個人の steering をクラウドセッションで使い回すには **Configuration Sync でアップロード**します（**Agent Config > Cloud Config** からアップロードし、クラウド側のコピーは **Agent Config > Steering** で作成・編集します。クラウド側のコピーが**すべてのクラウドセッションに適用**されます） |
| **UI での foundation ファイル生成** | **IDE のみ**（Web は非対応） |

### 現行ページが書いている Kiro Web 固有の動作

| 場面 | 公式の説明 |
|------|----------|
| **Autonomous モード** | **タスク中に与えた方向づけが、そのタスクの steering として働く**（「you can steer autonomous-mode tasks the same way — direction you give during the task acts as steering for it」） |
| **コードレビュー** | **PR へのフィードバックでエージェントを操縦できる**（[下記](#コードレビューを通じて教える)） |

同名でも仕様が異なる機能（例: [Specs](02_specs.md#kiro-ide-との違い2026-08-12-の移転時点で失われた記述)）と同様に、
**公式が同一と書いていない部分を「同じ」とは書きません**。

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

公式は 2026-10-02 版で次のように説明しています。

> On Kiro Web, you can steer autonomous-mode tasks the same way — direction you give during the task acts as steering for it.

| モード | 操縦の仕方 |
|-------|----------|
| **Autonomous モード** | 上記の例と**同じように操縦できる**。**タスク中に与えた方向づけが、そのタスクのステアリングとして機能する** |
| **既定（協調）モード** | チャットで**リアルタイムに**方向づけする（上記の例） |

> ⚠️ **2026-09-02 版の記述は「On Kiro Web, the agent asks clarifying questions upfront in autonomous mode - your answers act as steering for that task. In the default mode, you can steer continuously as you iterate together.」でした。**
> 2026-10-02 版では「冒頭の明確化の質問」と「既定モードでの継続的な操縦」の記述が無くなっています。
> 同じ時期に `docs/web/autonomous-mode/` からも Clarification の段階が削除されています（[01_agent-modes.md](01_agent-modes.md#動作の3段階公式の説明)）。

詳細は [01_agent-modes.md](01_agent-modes.md) を参照してください。

---

## 🔗 関連ページ

- [01_agent-modes.md](01_agent-modes.md) — 2つのモード（操縦の仕方が違う）
- [02_specs.md](02_specs.md) — Specs（公式が IDE との差分を明記している機能）
- [03_automations.md](03_automations.md) — Schedule（Scheduled tasks。誰もいない状態で実行されるため規約が重要）
- [06_repository-integration.md](06_repository-integration.md) — PR フィードバックへの対応
- 公式: <https://kiro.dev/docs/steering/>（移転先）

---

[← 01_features に戻る](README.md)
