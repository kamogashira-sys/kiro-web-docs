# エージェントの2つのモード（協調モード / Autonomous モード）

> **本ページは Kiro Web 版（<https://app.kiro.dev>）の仕様です。**
> Kiro IDE / Kiro CLI とは別製品です。**Kiro Web は [2026-09-01 に一般提供（GA）になりました](https://kiro.dev/changelog/web/kiro-web-is-now-generally-available/)。**

**出典**: <https://kiro.dev/docs/web/using-the-agent/>（Page updated: October 2, 2026）・<https://kiro.dev/docs/web/using-the-agent/chatting/>（Page updated: September 30, 2026）・<https://kiro.dev/docs/web/using-the-agent/creating-tasks/>（Page updated: October 2, 2026）・<https://kiro.dev/docs/web/autonomous-mode/>（Page updated: October 2, 2026）

---

## 📑 このページの内容

1. [2つのモードの違い](#2つのモードの違い)
2. [協調モード（既定）](#協調モード既定)
3. [Autonomous モード](#autonomous-モード)
4. [セッション中にモードを切り替える](#セッション中にモードを切り替える)
5. [タスクの作り方](#タスクの作り方)
6. [タスクの状態遷移](#タスクの状態遷移)
7. [チャットでの操縦](#チャットでの操縦)
8. [会話のタイムラインの読み方](#会話のタイムラインの読み方)
9. [Reviews（Summary の中）](#reviewssummary-の中)
10. [バックグラウンドのタブと再接続](#バックグラウンドのタブと再接続)
11. [セッションをグループにまとめる](#セッションをグループにまとめる)
12. [セッション名は自動で付きます](#セッション名は自動で付きます)
13. [Workflows（バックグラウンドで動く多段の計画）](#workflowsバックグラウンドで動く多段の計画)
14. [Web 検索](#web-検索)

---

## 2つのモードの違い

| 項目 | **協調モード**（既定） | **Autonomous モード** |
|------|-------------------|-------------------|
| 主導するのは | **利用者**（会話を主導する） | **エージェント**（結果に責任を持つ） |
| 進め方 | 対話的に反復する | 計画 → サブエージェントで実行 → 完了 |
| プルリクエスト／マージリクエスト | **依頼したときに作成** | **自動的に作成** |
| モデルの選択 | 選べる | **選べない**（エージェントが自動選択） |
| 既定 | **有効** | 無効（チャット入力バーで切り替える。最初のメッセージの前でも後でもよい） |
| 向いている作業 | 探索・設計の議論・密に反復したい作業 | 成果物を明確に説明できて独立実行できる作業 |

---

## 協調モード（既定）

公式は Kiro Web の既定モードを **collaborative（協調的）**と説明しています。「エージェントと対話的に作業し、問題を一緒に反復する」モードです。

### できること

公式が挙げているのは次の5点です。

- 実装方針とトレードオフを議論する
- 自分のコードベースについて質問する
- エージェントにコードを書かせる・修正させる
- フィードバックを与えて実装を反復する
- **納得したらプルリクエストの作成を依頼する**

### エージェントが参照できるもの

公式は、エージェントが次のものにアクセスできると説明しています。

| 情報源 |
|-------|
| **Web 検索**（[下記](#web-検索)） |
| リポジトリのコンテキスト |
| **過去のコードレビューからの学習**（[04_steering.md](04_steering.md#コードレビューを通じて教える)） |

### プルリクエストの作成

変更に満足したらエージェントにプルリクエストの作成を依頼します。エージェントは**フィーチャーブランチを作成し、変更をコミットし、実施内容の説明付きで PR を作成**します。

PR にはその後もフィードバックを与えられます。**エージェントがコメントに応答して更新をプッシュします。**

---

## Autonomous モード

公式は、Autonomous モードを「エージェントがタスクの結果を最初から最後まで所有する」モードと説明しています。

### 有効にする方法

**チャット入力バーの `Autonomous` を切り替えます。** 公式は「either before your first message or at any later point in the session, to hand off without starting over」としており、**最初のメッセージの前でも、セッションの途中でも**切り替えられます。

> **既定ではオフ**です。オフのときは協調モードで作業します。

> 公式ページの 2026-09-02 版は「Toggle Autonomous in the chat input bar **before submitting your message**」でした。
> 2026-10-02 版で、[2026-06-02 のエントリ](../02_update/01_changelog.md#2026-06-02-start-without-a-repo-switch-modes-anytime)（セッション中の切り替え）と一致する記述になりました。

### Workflows との違い

公式は 2026-10-02 版で次の説明を加えています。

> Autonomous mode is distinct from declarative workflows. Autonomous mode lets the agent decide its internal process for one task. A workflow gives the runtime a reusable graph with explicit steps, agents, handoffs, loops, waits, and completion conditions; it can run in the background while you continue the parent conversation.

| 項目 | **Autonomous モード** | **Workflows** |
|------|-------------------|-------------|
| 内部の進め方を決めるのは | **エージェント**（1つのタスクについて） | **再利用できるグラフ**（明示的なステップ・エージェント・引き継ぎ・ループ・待機・完了条件） |
| 実行のされ方 | （この比較の文脈では記載なし） | **バックグラウンド**で動き、その間も親の会話を続けられる |

Workflows は[下記](#workflowsバックグラウンドで動く多段の計画)を参照してください。

### ⚠️ モデルを自分で選べません

公式は次のように明記しています。

> In autonomous mode, the agent selects the model automatically — you cannot choose the model yourself.

| 項目 | 内容 |
|------|------|
| モデルの選択 | **エージェントが自動的に選択**。**利用者は選べません** |

### 動作の3段階（公式の説明）

| # | 段階 | 内容 |
|---|------|------|
| 1 | **Planning**（計画） | 作業をステップに分解し、要件を生成し、**受け入れ基準を定義**する |
| 2 | **Execution**（実行） | **専門のサブエージェント**が各ステップを担当する（コードベースの分析・コードの記述・変更の検証） |
| 3 | **Completion**（完了） | **1つ以上のプルリクエストまたはマージリクエスト**を作成し、変更内容・実装方針・検討したトレードオフを詳しく説明する |

> ⚠️ **公式ページの 2026-09-02 版では4段階でした。** 先頭に **Clarification**（明確化。要件・制約・好みを理解するため作業前に質問し、
> 作業開始前に回答が必要）があり、導入文にも「the agent asks clarifying questions upfront」とありましたが、
> **2026-10-02 版ではどちらも削除**されています。削除の理由は公式に書かれていないため**未確認**です。
> 実行中に明確化が必要になった場合の `Needs attention`（[進捗の確認](#進捗の確認)）の記述は残っています。

この過程を通じて、エージェントは**隔離されたサンドボックス**でリポジトリをクローンして作業します（[05_sandbox.md](05_sandbox.md)）。

### 向いている作業（公式の例）

公式は「成果物を明確に説明でき、エージェントが独立して実行できるタスク」に向いているとして、次を挙げています。

- 1つ以上のリポジトリにまたがる**明確に定義された機能の実装**
- **再現手順が明確なバグ**の修正
- 既存コードへの**テストの記述**
- 確立されたパターンに沿った**リファクタリング**
- **ドキュメント・設定ファイル**の更新

> 公式は、**探索的な作業・設計の議論・密に反復したい作業には協調モードを使う**よう案内しています。

### 進捗の確認

セッションビューから監視できます。エージェントは各フェーズを進むごとに更新を提供します。**実行中に明確化が必要になると、タスクは `Needs attention` 状態になり、入力を待ちます。**

### ⚠️ 必ずプルリクエストが作られるとは限りません

公式は次のように説明しています。

> The agent won't always open a pull request — for some tasks it may provide answers, analysis, or suggestions directly in the chat.

タスクによっては、**PR ではなくチャット内で回答・分析・提案を返す**ことがあります。

### PR コマンド

| コマンド | 動作 |
|---------|------|
| **`/kiro all`** | **PR 全体の、すべてのレビュアーからのすべてのコメント**に対応する |
| **`/kiro fix`** | **特定の会話スレッド内のすべてのコメント**に対応する |

詳細は [06_repository-integration.md](06_repository-integration.md#pr-フィードバックへの対応) を参照してください。

---

## セッション中にモードを切り替える

**Vibe セッションでは、最初のプロンプトを送った後でも Autonomous モードを選べます**（従来はセッション開始時のみ）。やり直さずに、好きなタイミングでエージェントに引き渡せます。

> この変更は [2026-06-02 のエントリ](../02_update/01_changelog.md#2026-06-02-start-without-a-repo-switch-modes-anytime)で追加されました。

---

## タスクの作り方

**出典**: <https://kiro.dev/docs/web/using-the-agent/creating-tasks/>（Page updated: October 2, 2026）・<https://kiro.dev/docs/web/using-the-agent/>（Page updated: October 2, 2026）

### `app.kiro.dev` から

1. <https://app.kiro.dev> にアクセスして **New session** を選ぶ
2. チャット入力欄の下の **Select repo** で**リポジトリを1つ以上選ぶ**（任意）
3. **Add to group** でセッションのグループを選ぶか作る（任意。[下記](#セッションをグループにまとめる)）
4. エージェントにやってほしいことを記述する

> 手順 1〜4 は <https://kiro.dev/docs/web/using-the-agent/>（Page updated: October 2, 2026）の「Start a session」に基づきます。
> 手順 3 は 2026-10-02 版で追加されました。

セッション開始時にリポジトリを選ばなかった場合、作業を依頼した時点で選択を求められます。

**1つのタスクで複数のリポジトリにまたがって作業できます。** 公式は、複数リポジトリにまたがる作業では
**すべての変更を調整し、それぞれのリポジトリでプルリクエストまたはマージリクエストを作成する**としており、
2026-10-02 版で「**even when the repositories span GitHub and GitLab**」（GitHub と GitLab にまたがる場合も）と明記しました。

> **⚠️ 公式の警告**: 信頼できるリポジトリだけを選んでください。**特に公開リポジトリと
> 非公開リポジトリを混在させるときは注意が必要です。** エージェントは
> **リポジトリのコードにある指示から学習し、それに従います。その指示が悪意あるものであっても同様です。**

### GitHub issue から

**先に GitHub を接続する必要があります**（[06_repository-integration.md](06_repository-integration.md)）。

| 方法 | 動作 |
|------|------|
| **`kiro` ラベルを付ける** | エージェントが作業を開始し、**その issue のすべてのコメントを聞き取って**追加のコンテキストやフィードバックとして扱う |
| **コメントで `/kiro` とメンションする** | **その issue を**エージェントに割り当てる |

### タスクを書くときのコツ（公式の5項目）

| # | コツ | 公式の説明 |
|---|------|-----------|
| 1 | **成果物を具体的に書く** | 「ログインフローを改善して」ではなく「**メール確認付きのパスワードリセット機能をログインページに追加して**」のように書く |
| 2 | **解決したい問題を説明する** | 背景と必要な理由を説明する。制約の理解と実装判断の質が上がる |
| 3 | **関連するコンテキストを渡す** | 関連ドキュメント・例・参考にすべき既存コードへのリンク |
| 4 | **受け入れ基準を定義する** | 完了とみなすために満たすべき条件を列挙する |
| 5 | **ステアリングファイルを使う** | `.kiro/steering/` のファイルでチームの標準・アーキテクチャ・規約を定義しておけば、**毎回説明せずに**一貫して従わせられる（[04_steering.md](04_steering.md)） |

---

## タスクの状態遷移

| 状態 | 意味 |
|------|------|
| **Queued** | 開始待ち。**並列 10 件の上限**に達しているとこの状態になる |
| **In progress** | エージェントが作業中（要件の分析・コードの記述・テストの実行） |
| **Needs attention** | 入力が必要、またはエージェントに確認事項がある。応答するとブロックが解除される |
| **Completed** | 作業が完了しプルリクエストが作成された。**フィードバックを与えると Queued に戻り、枠が空き次第 In progress になる** |
| **Cancelled** | キャンセルされた。**再開できません** |

上限値は [04_reference/04_limits.md](../04_reference/04_limits.md#タスクの上限) を参照してください。

---

## チャットでの操縦

**出典**: <https://kiro.dev/docs/web/using-the-agent/chatting/>（Page updated: September 30, 2026）

### タスク作成前

- 異なる実装方針を議論する
- 要件や制約を明確にする
- 技術的な判断についてエージェントの意見を得る

### タスク実行中

- 実装方針についてエージェントを操縦する
- 追加の要件や制約を与える
- 最初の結果を見てから追加の作業を依頼する

### ⚠️ 1セッションに2つ目のタスクは作れません

公式は次のように明記しています。

> Any comments or steering will update the scope of the current task. You cannot create a second task in the same session — to work on a different task, start a new session.

| 項目 | 内容 |
|------|------|
| セッション中のコメント・操縦 | **現在のタスクのスコープを更新する** |
| 2つ目のタスク | **同一セッションでは作れません**。別のタスクは**新しいセッション**で |

### セッションの会話スレッドは1本です

公式は「Each session has a single conversation thread」としています。**別の話題に取り組むときは新しいセッションを開始します。**

### 親チャットと Workflow のステップ（2026-09-30 版で追加）

バックグラウンドの Workflow が動いている間も、**親の会話（メインの会話）は使えます**。公式は2つの会話面を使い分けるよう案内しています。

| 会話面 | 使いどころ（公式の説明） |
|-------|---------------------|
| **親チャット**（Parent chat） | メインのエージェントに、進捗の解釈・より広い問題の解決・全体の方向転換・完了した証拠の要約を頼む |
| **選んだステップ**（Selected step） | **Workflows** を開いてノードを選び、状態に応じた入力欄を使う。一時停止中は **Answer this step**、実行中は **Steer the agent**、それ以外は **Message this step's agent** |

公式は次のように注意しています。

> A direct step message does not necessarily interrupt an active tool call. It applies according to the step's current state and turn boundary. When a step explicitly pauses for input, reply in that step session rather than only in the parent chat.

| 項目 | 内容 |
|------|------|
| ステップへの直接のメッセージ | **実行中のツール呼び出しを中断するとは限らない**。ステップの現在の状態とターンの区切りに従って適用される |
| ステップが入力待ちで一時停止したとき | **親チャットだけでなく、そのステップのセッションで返答する** |

### セッションの保持期間

**90 日**で期限切れになり、チャットメッセージとログが削除されます。**プルリクエスト・マージリクエスト・コードの変更・GitHub または GitLab 上の会話は影響を受けません**（[04_reference/04_limits.md](../04_reference/04_limits.md#セッションの保持期間)）。

---

## 会話のタイムラインの読み方

**出典**: <https://kiro.dev/docs/web/using-the-agent/>（Page updated: October 2, 2026）

| 表示 | 内容（公式の説明） |
|------|----------------|
| **折りたたみブロック** | エージェントの作業中、**連続する推論ステップとツール呼び出しが1つの折りたたみブロック**にまとまる。展開すると詳細を確認できる |
| **Session setup** | 起動時の処理は **Session setup** の下にまとめられる |
| 結果の表示 | Steering・Configuration Sync・タスクリストの結果は**読みやすい要約**として表示される |

> この表示は [2026-09-22 のエントリ](../02_update/01_changelog.md#2026-09-22-reasoning-effort-and-a-grouped-timeline)で告知されました。

---

## Reviews（Summary の中）

**出典**: <https://kiro.dev/docs/web/using-the-agent/>（Page updated: October 2, 2026）

セッションにレビュー（プルリクエスト）がある場合、**Summary** を開くと **Files**・**Artifacts** と並んで **Reviews** が表示されます。

| 操作 | 動作 |
|------|------|
| **Reviews を展開** | その場で一覧を表示する（**Files** か **Artifacts** を選ぶとそのタブに切り替わる） |
| **レビューを選ぶ** | 詳細（変更ファイル・コミット・レビューコメント）を表示する |
| **Back** | レビューの一覧に戻る |

GitHub のプルリクエストの詳細表示と GitLab のマージリクエストの扱いは
[06_repository-integration.md](06_repository-integration.md#セッション内で-pr-を確認するsummary-の-reviews) を参照してください。

> [2026-09-22 のエントリ](../02_update/01_changelog.md#2026-09-22-reasoning-effort-and-a-grouped-timeline)の Improvements で、
> Reviews が **Summary の中の1節**になったことが告知されています。

---

## バックグラウンドのタブと再接続

**出典**: <https://kiro.dev/docs/web/using-the-agent/>（Page updated: October 2, 2026）

セッションを開いたタブがバックグラウンドにある間にマシンがスリープしたりネットワークが変わったりしても、**タブに戻るとセッションが再接続され、切断中に届いたアクティビティが再生されます**。

| 項目 | 内容 |
|------|------|
| 再接続のための操作 | **不要**（メッセージを送り直す必要はない） |
| 接続が切れていなかったセッション | 再生するものが無いため、**戻っても何も変わらない** |

> この動作は [2026-09-22 のエントリ](../02_update/01_changelog.md#2026-09-22-reasoning-effort-and-a-grouped-timeline)で告知されました。

---

## セッションをグループにまとめる

**出典**: <https://kiro.dev/docs/web/using-the-agent/>（Page updated: October 2, 2026）

セッションが増えてきたら、**関連する作業をグループにまとめて**整理できます。
**グループは任意**で、グループに入れていないセッションは **Ungrouped** に残ります。

### セッションを始める前にグループを選ぶ

**セッションを始める前に**、入力欄（composer）の **Add to group** で既存のグループを選ぶか新しく作れます。
あとからサイドバーや Sessions ページで整理することもできます。

> この操作は 2026-10-02 版で追加されました（[2026-09-22 のエントリ](../02_update/01_changelog.md#2026-09-22-reasoning-effort-and-a-grouped-timeline)の Improvements「Session groups from the composer」）。

### グループを作る

サイドバーの **Sessions** パネルでグループ表示に切り替え、**Create group** を選びます。
名前を付けて確定すると、**セッションを入れる前に空のグループがすぐに現れます**。

### セッションを出し入れする

| 操作 | 方法 |
|------|------|
| **既存のグループに入れる** | セッションのメニュー → **Move to group** から選ぶ |
| **新しいグループを作って入れる** | セッションのメニュー → **New group**（作成と移動が**1手順**で済みます） |
| **グループから出す** | セッションのメニュー → **Remove from group**（**Ungrouped** に戻ります） |

### グループのメニューでできること

| 操作 | 動作 |
|------|------|
| **Rename group** | 名前を変える。**そのグループのセッションは新しい名前の側に移ります** |
| **Delete group** | 確認を求められ、グループを削除して**セッションは Ungrouped へ移動**します |

> ⚠️ **グループを削除してもセッションは削除されません。**
> 公式は「Deleting a group never deletes the sessions in it.」と明記しています。

### Sessions ページでの一括操作

**Sessions ページ**（<https://app.kiro.dev/session>）では**複数のセッションをまとめて**操作できます。

| 操作 | 動作 |
|------|------|
| **Move to group** | 選んだセッションを**まとめて同じグループへ移動** |
| **Filter by group** | 選んだグループのセッションだけを表示。**選択操作は不要**（単独で使えます） |

> この機能は [2026-08-22 のエントリ](../02_update/01_changelog.md#2026-08-22-organize-sessions-into-groups)で告知されました。

---

## セッション名は自動で付きます

**出典**: <https://kiro.dev/docs/web/using-the-agent/>（Page updated: October 2, 2026）

公式は次のように説明しています。

> Kiro generates a title for each session from your task and shows it in the session header and the sidebar. If you rename a session yourself, Kiro keeps your title and does not overwrite it with a generated one.

| 動作 | 内容 |
|------|------|
| **自動命名** | **タスクの内容から**タイトルを生成し、**セッションヘッダーとサイドバー**に表示します |
| **自分で改名した場合** | **自分が付けた名前が保持**され、**自動生成されたタイトルで上書きされません** |

> この機能は [2026-08-27 のエントリ](../02_update/01_changelog.md#2026-08-27-sessions-name-themselves)で告知されました。

---

## Workflows（バックグラウンドで動く多段の計画）

**出典**: <https://kiro.dev/docs/web/using-the-agent/>（Page updated: October 2, 2026）・<https://kiro.dev/docs/web/using-the-agent/chatting/>（Page updated: September 30, 2026）・<https://kiro.dev/docs/web/cloud-configuration/>（Page updated: September 30, 2026）・<https://kiro.dev/changelog/web/introducing-workflows/>（September 30, 2026）

公式は `docs/web/using-the-agent/` で次のように説明しています。

> For reusable multi-step orchestration that runs in the background while the main conversation stays available, use Workflows. A workflow can coordinate isolated agents, loops, reviews, and external waits; inspect or message its individual steps under Workflows in the session details.

| 項目 | 内容 |
|------|------|
| 何をするものか | **再利用できる多段のオーケストレーション**。メインの会話を使える状態のまま**バックグラウンド**で動く |
| 調整できるもの | 隔離されたエージェント・ループ・レビュー・外部の待機 |
| 個々のステップ | セッションの詳細の **Workflows** の下で確認し、メッセージを送れる（[親チャットと Workflow のステップ](#親チャットと-workflow-のステップ2026-09-30-版で追加)） |
| Autonomous モードとの違い | [上記](#workflows-との違い) |

### 有効にする（オプトイン）

[2026-09-30 のエントリ](../02_update/01_changelog.md#2026-09-30-introducing-workflows-in-kiro-web)によると、Workflows は **Kiro Web のクラウドセッションでオプトインの機能**として提供されています。

| 操作 | 方法（公式の説明） |
|------|----------------|
| 有効にする | **Settings > Workflows** で **Enable workflows** をオンにする |
| レシピを1つアップロード | **Upload workflow**（`.workflow.json`・`.workflow.yaml`・`.workflow.yml`） |
| フォルダごと取り込む | [Configuration Sync](09_configuration-sync.md) で `.kiro/workflows/` フォルダを取り込む |
| 無効にする | Workflows の画面要素が隠れ、**新しい起動ができなくなる** |

### 同梱のレシピ（3種類）

同エントリは、同梱された3つのレシピから始められるとしています。

| レシピ | 用途（公式の説明） |
|-------|----------------|
| `investigate` | 読み取り専用の調査 |
| `feature-pipeline` | 段階を踏んだ機能の実装 |
| `publish-pr` | プルリクエストの作成とレビューフィードバックへの対応 |

### 起動と進行（changelog の説明）

- 望む成果と、どの程度の構造やレビューが欲しいかを伝えると、**Kiro が Workflow を提案**し、ステップ・エージェント・effort に名前を付けて**バックグラウンドで起動**します
- **各ステップはそれぞれ独自のエージェントセッション**で動き、**それより前のステップが渡したものだけ**を見ます。ステップが入力を必要とすると**実行が一時停止**します
- 親の会話のサイドパネルから **Workflows** を開いて実行を選ぶと、入れ子のステップを確認できます。ステップを選ぶと、**状態・経過時間・エージェント・モデル・effort・ツールのアクティビティ**が表示されます
- 実行は**一時停止・再開・停止**でき、失敗後は**失敗したステップを再試行**できます

> **Workflows の全製品共通の解説**（レシピの書き方・例・実行の管理）は公式の共通ページ
> <https://kiro.dev/docs/workflows/> にあります。このページは IDE・CLI・Web の共通ページで、
> 本サイトは **Kiro Web の docs と Web の changelog に書かれている範囲**だけを記載しています。

---

## Web 検索

公式は、Kiro Web が**リアルタイムに Web を検索**して最新情報にアクセスできると説明しています。モデルの訓練データ作成以降に変わった可能性のある事柄について、最新の回答が得られます。

| 項目 | 内容 |
|------|------|
| 設計上の制約 | **まとまった量のテキストを再現しないよう設計されている** |
| 対応するページ | **公開アクセス可能なページ**（2026-08-04 更新で「ペイウォールや認証の背後にあるページにアクセスできない」という記述から変更） |
| ログ | **検索は引用付きでセッションに記録される**（エージェントが参照した情報源を確認できる） |

---

## 🔗 関連ページ

- [02_specs.md](02_specs.md) — Specs（コードを書く前に要件・設計・タスクを作る）
- [04_steering.md](04_steering.md) — Steering（エージェントを継続的に導く）
- [05_sandbox.md](05_sandbox.md) — サンドボックス（タスクの実行環境）
- [06_repository-integration.md](06_repository-integration.md) — GitHub / GitLab 連携
- [04_reference/04_limits.md](../04_reference/04_limits.md) — 上限値・保持期間
- [03_deployment/01_setup.md](../03_deployment/01_setup.md) — セットアップと最初のタスク
- 公式: <https://kiro.dev/docs/web/using-the-agent/>・<https://kiro.dev/docs/web/autonomous-mode/>

---

[← 01_features に戻る](README.md)
