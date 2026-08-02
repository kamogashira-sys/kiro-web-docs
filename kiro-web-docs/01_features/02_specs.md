# Specs（要件・設計・タスクを作ってから実装する）

> **本ページは Kiro Web 版（<https://app.kiro.dev>）の仕様です。**
> Kiro IDE / Kiro CLI とは別製品です。**Kiro Web は Preview 段階**です。

**出典**: <https://kiro.dev/docs/web/specs/>（Page updated: July 22, 2026）

> このページは Kiro Web の docs で3番目に新しい更新です（2026-08-01 時点）。

Specs は、いきなりコードを書き始めるのではなく、**要件・設計・タスクの計画を作ってからエージェントに実装させる**進め方です。計画はブラウザ上でレビューして修正できます。

---

## 📑 このページの内容

1. [3種類の spec](#3種類の-spec)
2. [spec セッションの開始](#spec-セッションの開始)
3. [生成される3つの成果物](#生成される3つの成果物)
4. [タスクの実行](#タスクの実行)
5. [Kiro IDE との違い（公式が明記している3点）](#kiro-ide-との違い公式が明記している3点)

---

## 3種類の spec

公式は「Kiro Web supports the **same spec types as the IDE**」として、3種類を挙げています。

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

> You can add multiple repositories to a single spec session, and the agent will plan and coordinate changes across all of them.

**1つの spec セッションに複数のリポジトリを追加でき、エージェントはそれら全体にまたがって計画と変更の調整を行います。**

> **⚠️ 公式の警告**: 信頼できるリポジトリだけを選んでください。**特に公開リポジトリと
> 非公開リポジトリを混在させるときは注意が必要です。** エージェントは
> **リポジトリのコードにある指示から学習し、それに従います。その指示が悪意あるものであっても同様です。**

---

## 生成される3つの成果物

公式は「Every spec produces three artifacts that you review directly in your browser」として、次を挙げています。

| ファイル | 内容 |
|---------|------|
| **`requirements.md`** | **ユーザーストーリーと受け入れ基準** |
| **`design.md`** | **技術アーキテクチャと実装方針** |
| **`tasks.md`** | **個別で追跡可能な実装タスクのリスト** |

### Bug spec は `requirements.md` の代わりに `bugfix.md` を作ります

公式は次のように説明しています。

> A Bug spec produces a **bugfix.md** instead, a bugfix analysis that captures the current defect, the expected behavior, and the behavior that must stay unchanged to prevent regressions

`bugfix.md` に記録されるのは3点です。

| # | 内容 |
|---|------|
| 1 | **現在の不具合** |
| 2 | **期待される挙動** |
| 3 | **リグレッションを防ぐために変わってはいけない挙動** |

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

### ⚠️ プロンプトではなくボタンで開始します

公式は次のように明記しています。

> You start the work using buttons, not by prompting the agent

| 操作 | 方法 |
|------|------|
| **すべてのタスクを実行** | グローバルの **Run all** コントロールを使う |
| **特定のタスクを実行** | **`tasks.md` のビュー**から個別のタスクを選ぶ |

### 完了後

作業が完了すると、エージェントが**実施内容の説明付きでプルリクエストを作成**します。その後もフィードバックを与えてエージェントに更新をプッシュさせられます。

---

## Kiro IDE との違い（公式が明記している3点）

公式ページには「**Differences from the IDE**」という節があり、**Kiro IDE の Specs と web で異なる点**が3つ挙げられています。

| # | Kiro Web での挙動 | Kiro IDE（公式の対比） |
|---|----------------|-------------------|
| 1 | **チャット入力ボックスから Spec を選ぶ** | **専用の Specs ペイン**から選ぶ |
| 2 | **1つの spec セッションに複数リポジトリを追加**でき、エージェントがそれら全体で計画する | （公式は Web 側の特徴として記述） |
| 3 | **ブラウザで成果物をレビュー・編集し、ローカルにダウンロードできる** | （同上） |

> **これは公式が明記している差分です。** 本サイトが推測したものではありません。
>
> 同時に公式は「**same spec types as the IDE**」（spec の種類は IDE と同じ）とも書いています。
> **「種類は同じ、操作方法とリポジトリの扱いが違う」**というのが公式の説明です。

公式は IDE 側の完全なワークフローについて `docs/specs`（**Kiro IDE 版のドキュメント — 別製品**）を案内しています。IDE 版の解説は姉妹サイト [kiro-ide-docs](https://github.com/kamogashira-sys/kiro-ide-docs) にあります。

---

## 🔗 関連ページ

- [01_agent-modes.md](01_agent-modes.md) — 協調モードと Autonomous モード
- [04_steering.md](04_steering.md) — Steering（spec の生成にも影響する）
- [06_repository-integration.md](06_repository-integration.md) — 複数リポジトリの扱い
- [02_update/01_changelog.md](../02_update/01_changelog.md#2026-06-11-gitlab-support-and-specs-in-the-browser) — Specs がブラウザに来たときのエントリ
- 公式: <https://kiro.dev/docs/web/specs/>

---

[← 01_features に戻る](README.md)
