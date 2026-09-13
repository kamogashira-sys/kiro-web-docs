# Specs（要件・設計・タスクを作ってから実装する）

> **本ページは Kiro Web 版（<https://app.kiro.dev>）の仕様です。**
> Kiro IDE / Kiro CLI とは別製品です。**Kiro Web は [2026-09-01 に一般提供（GA）になりました](https://kiro.dev/changelog/web/kiro-web-is-now-generally-available/)。**

**出典**: <https://kiro.dev/docs/specs/>（Page updated: August 27, 2026・**Features 区分の全製品共通ページに移転**。旧 `docs/web/specs/` は2026-08-12以前は Page updated: July 22, 2026）

> ⚠️ **旧 `docs/web/specs/` は2026-08-12に `docs/specs/`（Features 区分の全製品共通ページ）へ移転しました。**
> 2026-08-01時点では「Kiro Web の docs で3番目に新しい更新」でしたが、この順位は移転前の記録です。

Specs は、いきなりコードを書き始めるのではなく、**要件・設計・タスクの計画を作ってからエージェントに実装させる**進め方です。計画はブラウザ上でレビューして修正できます。

---

## 📑 このページの内容

1. [3種類の spec](#3種類の-spec)
2. [spec セッションの開始](#spec-セッションの開始)
3. [生成される3つの成果物](#生成される3つの成果物)
4. [タスクの実行](#タスクの実行)
5. [Kiro IDE との違い（2026-08-12 の移転時点で失われた記述）](#kiro-ide-との違い2026-08-12-の移転時点で失われた記述)

---

## 3種類の spec

公式は Specs を「**開発プロセスを形式化する構造化された成果物**」と位置づけています。

> Specs or specifications are structured artifacts that formalize the development process for features and bug fixes in your application.

本サイトが扱う3種類は次のとおりです。

> ⚠️ **「Kiro Web supports the same spec types as the IDE」という一文は現行ページにありません。**
> この一文は移転前の `docs/web/specs/`（本サイトの 2026-08-01 snapshot）にありましたが、
> **移転先の `docs/specs/` では確認できません**（2026-09-13 実測）。
> 現行ページは**サーフェスごとのタブ**で説明を分けており、Quick Spec は Web タブに記載があります。

| 種類 | 用途（公式の説明） |
|------|----------------|
| **Feature** | **新機能の構築**。エージェントが要件を集め、技術設計を提案し、作業を個別のタスクに分解する |
| **Bug** | **バグの診断と修正**。エージェントが根本原因を特定し、**外科的な修正**を設計し、**リグレッションを防ぐ**タスクを計画する |
| **Quick Spec** | 要件・設計・タスクを**一度のパスで生成**する。**冒頭で明確化の質問に答えると、フェーズ間の承認ゲートなしにタスクリストに直行する** |

> **Quick Spec は承認ゲートがありません。** Feature / Bug との違いはこの点です。

---

## spec セッションの開始

公式の手順は3ステップです。

1. <https://app.kiro.dev> にアクセスして新しいセッションを開始する
2. チャット入力欄の下の **Select repo** で**1つ以上のリポジトリ**を選ぶ
3. チャット入力ボックスから **Spec** を選び、構築したいこと・修正したいことを記述する

### 複数リポジトリを1セッションに入れられます

公式は次のように説明しています。

> You can add multiple repositories to a single spec session, and the agent plans and coordinates changes across all of them.

**1つの spec セッションに複数のリポジトリを追加でき、エージェントはそれら全体にまたがって計画と変更の調整を行います。**

> **⚠️ 公式の警告**: 信頼できるリポジトリだけを選んでください。**特に公開リポジトリと
> 非公開リポジトリを混在させるときは注意が必要です。** エージェントは
> **リポジトリのコードにある指示から学習し、それに従います。その指示が悪意あるものであっても同様です。**

---

## 生成される3つの成果物

公式は「Every spec generates three key files that form the foundation of your specification」として、次を挙げています。

| ファイル | 内容（公式の説明） |
|---------|------|
| **`requirements.md`**（または **`bugfix.md`**） | **ユーザーストーリー・受け入れ基準・バグ分析**を**構造化された記法で**記録する |
| **`design.md`** | **技術アーキテクチャ・シーケンス図・実装上の考慮事項**を文書化する |
| **`tasks.md`** | **個別で追跡可能なタスクからなる詳細な実装計画**を提供する |

### Bug spec は `requirements.md` の代わりに `bugfix.md` を作ります

現行の公式は、3フェーズの1つ目（**Requirements or Bug Analysis**）を次のように整理しています。

> - Feature Specs: User stories and acceptance criteria in `requirements.md`
> - Bugfix Specs: Bug analysis with **current/expected/unchanged behavior** in `bugfix.md`

`bugfix.md` に記録されるのは3点です。

| # | 内容 |
|---|------|
| 1 | **現在の挙動（current）** |
| 2 | **期待される挙動（expected）** |
| 3 | **変わってはいけない挙動（unchanged）** |

> ⚠️ **2026-08-27 更新で表現が短くなりました。** 移転前の `docs/web/specs/` には
> 「a bugfix analysis that captures the current defect, the expected behavior, and the behavior that
> must stay unchanged to prevent regressions」という一文がありましたが、
> **現行ページでは上記の箇条書きに置き換わっています**（2026-09-13 実測）。3点の内容は変わっていません。

> 公式はここで `docs/specs/bugfix-specs`（**Kiro IDE 版のドキュメント — 別製品**）にリンクしています。

### 成果物の編集とダウンロード

| 操作 | 方法 |
|------|------|
| レビュー | ブラウザで各成果物を開く |
| 修正 | **チャットで計画について会話する**（要件の追加・設計の一部の再考・タスク分解の調整を依頼すると、**エージェントが成果物をその場で更新**する） |
| 保存・共有・IDE への持ち出し | ブラウザで成果物を開き **Download** ボタンで `.md` ファイルをローカルに保存する |

---

## タスクの実行

計画に満足したら、エージェントがセッション中に実装します。

### タスクの開始はチャットで指示します

> ⚠️ **2026-08-27 更新で操作方法の記述が変わりました。**
> 移転前の `docs/web/specs/` には「**You start the work using buttons, not by prompting the agent**」
> （ボタンで開始する。エージェントにプロンプトを出すのではない）という一文がありましたが、
> **現行の `docs/specs/` の Web タブにこの一文はありません**（2026-09-13 実測）。

現行の公式は次のように説明しています。

> Once you're happy with the plan, tell the agent how to proceed in the chat

**計画に満足したら、チャットでエージェントに進め方を伝えます。**

| やりたいこと | 公式が示す言い方 |
|------------|--------------|
| **計画全体を実行する** | **すべてのタスクを進めるよう**エージェントに依頼する |
| **範囲を絞る** | **実装してほしいタスクを名指しする**（公式の例: `implement tasks 1 and 2`） |

作業が完了すると、**エージェントが実施内容の説明を付けてプルリクエストを作成**します。
**その後もフィードバックを与えて、エージェントに更新を push させられます。**

### タスクは並列で実行されます

**出典**: <https://kiro.dev/docs/specs/>（Page updated: August 27, 2026）

spec のタスクをすべて実行すると、Kiro は**タスクリストを解析して依存関係を判断し、独立したタスクを並行実行**します。
公式は「**ほとんどの feature spec で、設定なしに実行時間を大幅に短縮する**」と説明しています。

| 仕組み | 内容 |
|-------|------|
| **依存グラフ** | `tasks.md` のタスクから**依存グラフ**を構築する |
| **wave** | 独立したタスクを **wave** にまとめる。**Wave 1 は依存のないタスク全部**で、これらが並行実行される |

> **並列実行の上限**は [04_reference/04_limits.md](../04_reference/04_limits.md#並列実行は-10-件までです) を参照してください。

### 完了後

作業が完了すると、エージェントが**実施内容の説明付きでプルリクエストを作成**します。その後もフィードバックを与えてエージェントに更新をプッシュさせられます。

---

## Kiro IDE との違い（2026-08-12 の移転時点で失われた記述）

> ⚠️ **本節は公式サイトの再構成（2026-08-12）により、出典が現存しないページのスナップショットに基づきます。**
> 旧 `docs/web/specs/`（Page updated: July 22, 2026）には「**Differences from the IDE**」という節があり、
> **Kiro IDE の Specs と web で異なる点**が3つ挙げられていました。
> **移転先 `docs/specs/`（Page updated: August 12, 2026・Features 区分の全製品共通ページ）を実測したところ、
> この節および「Kiro Web」への言及は0件でした。** 移転時点でこの記述は失われたと判断できます。

旧ページに記載されていた3点差分（出典: 06_embedded-docs の 2026-08-01 スナップショット）:

| # | Kiro Web での挙動（旧記載） | Kiro IDE（公式の対比） |
|---|----------------|-------------------|
| 1 | **チャット入力ボックスから Spec を選ぶ** | **専用の Specs ペイン**から選ぶ |
| 2 | **1つの spec セッションに複数リポジトリを追加**でき、エージェントがそれら全体で計画する | （公式は Web 側の特徴として記述） |
| 3 | **ブラウザで成果物をレビュー・編集し、ローカルにダウンロードできる** | （同上） |

> **これは移転前に公式が明記していた差分です。** 本サイトが推測したものではありません。
>
> **2 の「複数リポジトリを追加できる」という機能自体**は、移転先にも
> 「Kiro Web」という語を使わない一般化された表現で残っています
> （"You can add multiple repositories to a single spec session, and the agent plans and
> coordinates changes across all of them."）。**IDE との対比という文脈は失われましたが、
> 機能の記述自体は消えていません。**
>
> 1・3 について、移転先に同等の記述が残っているかは確認できていません（**未確認**）。
>
> 旧ページは同時に「**same spec types as the IDE**」（spec の種類は IDE と同じ）とも書いていました。

公式は現在、IDE と Web を区別しない共通ページ `docs/specs/`（**Features 区分**）で Specs を説明しています。
IDE 版の解説は姉妹サイト [kiro-ide-docs](https://github.com/kamogashira-sys/kiro-ide-docs) にあります。

---

## 🔗 関連ページ

- [01_agent-modes.md](01_agent-modes.md) — 協調モードと Autonomous モード
- [04_steering.md](04_steering.md) — Steering（spec の生成にも影響する）
- [06_repository-integration.md](06_repository-integration.md) — 複数リポジトリの扱い
- [02_update/01_changelog.md](../02_update/01_changelog.md#2026-06-11-gitlab-support-and-specs-in-the-browser) — Specs がブラウザに来たときのエントリ
- 公式: <https://kiro.dev/docs/specs/>（移転先）

---

[← 01_features に戻る](README.md)
