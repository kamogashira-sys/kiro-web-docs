# Schedule（スケジュール実行タスク）

> **本ページは Kiro Web 版（<https://app.kiro.dev>）の仕様です。**
> Kiro IDE / Kiro CLI とは別製品です。**Kiro Web は [2026-09-01 に一般提供（GA）になりました](https://kiro.dev/changelog/web/kiro-web-is-now-generally-available/)。**

**出典**: <https://kiro.dev/docs/web/automations/>（Page updated: October 23, 2026）

Schedule（スケジュール実行タスク）は、**セッションを自分で開始せずに、スケジュールに従ってプロンプトを GitHub または GitLab のリポジトリに対して実行させる**機能です。

公式は「Scheduled tasks are available on **Pro, Pro+, Pro Max, and Power** plans.」と記載しています。

> この機能は [2026-06-19 のエントリ](../02_update/01_changelog.md#2026-06-19-introducing-automations)で追加されました。

> ⚠️ **名称について（公式の表記の違い）**: 上記の公式 docs <https://kiro.dev/docs/web/automations/>（Page updated: October 23, 2026）は、この機能を **Schedule**（本文は **Scheduled tasks**）と呼んでいます。
> URL は従来どおり `docs/web/automations/` です。
> 一方、2026-06-19 の changelog エントリは **Automations** と書いており、
> [2026-10-12 のエントリ](../02_update/01_changelog.md#2026-10-12-model-fallback-and-workflow-updates)の Fixes（Upgrade plan ボタンの修正）も、サブスクリプションが必要なページの例として **Automations** と書いています。
> 名称が変わった理由は公式に記載がなく**未確認**です。
> 本サイトのファイル名（`03_automations.md`）は、相互リンクを保つため変えていません。

---

## 📑 このページの内容

1. [何ができるか](#何ができるか)
2. [スケジュールタスクの作成](#スケジュールタスクの作成)
3. [スケジュール](#スケジュール)
4. [一覧と操作](#一覧と操作)
5. [結果の確認](#結果の確認)

---

## 何ができるか

公式は次のように説明しています。

> You describe the work once, choose when it runs, and Kiro carries it out in **autonomous mode**. The agent reads the code, makes changes, and opens a pull request or merge request when there's something to review.

| 項目 | 内容 |
|------|------|
| 記述 | **作業内容を一度書く** |
| 実行タイミング | **スケジュールで指定** |
| 実行モード | **Autonomous モード**（[01_agent-modes.md](01_agent-modes.md#autonomous-モード)） |
| 動作 | コードを読み、変更を加え、**レビューすべきものがあればプルリクエスト（GitHub）またはマージリクエスト（GitLab）を作成** |

### 公式が挙げている用途

繰り返し発生する保守作業に向いているとして、次を挙げています。

- **changelog の生成**
- **新規 issue のトリアージ**
- **依存関係の更新**
- **マージ済みプルリクエストの要約**

---

## スケジュールタスクの作成

`app.kiro.dev` の左サイドバーから **Schedule** を開き、**Create scheduled task** を選びます。

作成時に設定する項目は次のとおりです（最後に **Create scheduled task** を選びます）。

| 項目 | 内容 |
|------|------|
| **Task name** | タスクの名前（一覧で見分けるための名前） |
| **Status** | **Enabled** のままにするとスケジュールで実行される。無効にすると実行せずに保存できる |
| **Prompt** | タスクが行うべきことを記述する。**最大 10,000 文字** |
| **リポジトリ** | 対象のリポジトリ（1つ以上） |
| **Schedules** | 実行タイミング（1つ以上・**最大 5 つ**） |

### ⚠️ プロンプトは「誰もいない状態で実行される」前提で書きます

公式は次のように注意しています。

> Be specific about the task and the expected output, since the task runs without anyone there to clarify.

**明確化してくれる人がいない状態で実行される**ため、タスクと期待される出力を具体的に書く必要があります。

### プロンプトの例（公式）

公式は、プロンプトを「**無人で実行されるタスクへの指示書**」として扱い、目標・従うべきリポジトリの規約・生成すべきものを書くよう案内しています。changelog を保守するスケジュールタスクの例として、次を挙げています。

```text
Find all pull requests merged to the main branch since yesterday.
Summarize each PR in one line following the format in CHANGELOG.md.
Group changes under "Added", "Changed", and "Fixed" headings.
Open a pull request that appends today's entry to the top of the changelog.
If no pull requests were merged, do nothing.
```

公式は**最後の行が重要**だとしています。関連する作業があるときだけ動くよう指示しておくと、**変更のない日に空のプルリクエストが作られるのを避けられます**。

> 対話的なセッションと違い、**エージェントが質問しても答える人がいません。** タスクの書き方は
> [01_agent-modes.md](01_agent-modes.md#タスクを書くときのコツ公式の5項目) のコツが特に重要になります。
> チームの規約は [Steering ファイル](04_steering.md)に置いておくと毎回書かずに済みます。

---

## スケジュール

各タスクは**1つ以上のスケジュール**で動きます。

| 項目 | 値 |
|------|---|
| **1タスクあたりのスケジュール数** | **最大 5**（公式本文では綴りで `five`） |
| 各スケジュールの間隔 | **それぞれ別の間隔を設定できます** |

追加は **+ Add schedule** です。

### 3つのモード

| モード | 内容 |
|-------|------|
| **Hourly** | **毎時0分**に、`Run every` で指定した間隔で実行（例: 1 時間ごと・6 時間ごと） |
| **Daily** | **1 日 1 回**、指定した時刻に実行 |
| **CRON** | **カスタムの cron 式**で完全に制御 |

### ⚠️ カスタムスケジュールは 1 時間に 1 回まで

公式は次のように明記しています。

> Custom schedules can run at most once per hour. Kiro flags a CRON expression that would run more frequently and prevents submission until you correct it.

| 項目 | 内容 |
|------|------|
| カスタムスケジュールの実行頻度 | **最大で 1 時間に 1 回** |
| それより頻繁な cron 式 | **入力中に指摘され、修正するまで送信できません** |

> この制限は公式ページの 2026-08-04 版には無く、2026-10-02 版で追加されています（現行は <https://kiro.dev/docs/web/automations/>（Page updated: October 23, 2026））。
> [2026-09-22 のエントリ](../02_update/01_changelog.md#2026-09-22-reasoning-effort-and-a-grouped-timeline)の Improvements（Sub-hourly schedule validation）と
> Fixes（拒否されたスケジュールで汎用エラーではなく具体的な理由を表示）にも対応する記述があります。

### ⚠️ スケジュールは UTC で評価されます

公式は次のように明記しています。

> Schedules are evaluated in **UTC**. In the scheduled tasks list, a schedule's next run is shown in your local time alongside its UTC equivalent, for example At 9:00 AM (1:00 PM UTC).

| 項目 | 内容 |
|------|------|
| **評価のタイムゾーン** | **UTC** |
| 一覧の表示 | **ローカル時刻と UTC の両方**（例: `At 9:00 AM (1:00 PM UTC)`） |

設定中は生成された cron 式が下に表示されます（1 時間ごとなら `Generates: cron(0 */1 * * ? *)`）。

> **cron 式を自分で書く場合も UTC 基準**です。日本時間（JST = UTC+9）とは9時間ずれます。
> 「毎朝9時に実行」したい場合、cron では 0 時（UTC）を指定します。

---

## 一覧と操作

**Schedule** の一覧では、各行に次が表示されます。

| 表示項目 |
|--------|
| タスクの名前 |
| プロンプトのプレビュー |
| 接続されているリポジトリ |
| スケジュール |
| 現在のステータス |

| 操作 | 方法 |
|------|------|
| 名前で検索 | 検索ボックス |
| 状態で絞り込み | ステータスフィルタ |
| **Edit**（各行の **Actions** メニュー `⋯`） | 名前・プロンプト・リポジトリ・ステータス・スケジュールを変更 |
| **Delete**（各行の **Actions** メニュー `⋯`） | スケジュールタスクを削除する。**以後の実行はすべて止まります** |

### 有効・無効

| 状態 | 意味 |
|------|------|
| **Active** | 有効でスケジュールに従って実行中 |
| 無効 | **削除せずに実行を一時停止**した状態 |

再有効化は **Edit 画面**または**行のステータストグル**からいつでもできます。

### 変更の適用タイミング

公式は「Changes apply to the next scheduled run」（[2026-06-19 のエントリ](../02_update/01_changelog.md#2026-06-19-introducing-automations)）としています。**変更は次回のスケジュール実行から適用されます。**

---

## 結果の確認

### 実行ごとにセッションが作られます

公式は次のように説明しています。

> Each time a scheduled task runs, it creates a session visible in your session list alongside interactive sessions.

**実行のたびにセッションが作られ、対話的なセッションと並んでセッション一覧に表示されます。** 実行のセッションを開くと、会話・実行したステップ・作成されたプルリクエストを確認できます。

> 公式は、これが**スケジュールタスクが期待どおりに動いているかを確認する最良の方法**であり、
> 期待した変更が出なかった実行のトラブルシュートにも使えるとしています。

### 変更はプルリクエスト／マージリクエストとして提出されます

公式は次のように明記しています。

> Because the work lands as a pull request or merge request rather than a direct commit, nothing reaches your main branch without your review.

| 項目 | 内容 |
|------|------|
| 提出形式 | **プルリクエスト**（GitHub）または**マージリクエスト**（GitLab）。直接コミットではない |
| 対象 | **影響を受ける各リポジトリ**ごとに作成される |
| 帰結 | **レビューなしに main ブランチへ届くものはありません** |

### 実行ごとに独立したサンドボックス

[2026-06-19 のエントリ](../02_update/01_changelog.md#2026-06-19-introducing-automations)（当時の名称は Automations）で公式は次のように説明しています。

> Each run spins up an independent sandbox, clones your repositories, executes the work autonomously, and opens a pull request with the changes.

**実行ごとに独立したサンドボックスが起動**します（[05_sandbox.md](05_sandbox.md)）。

---

## 🔗 関連ページ

- [01_agent-modes.md](01_agent-modes.md) — Autonomous モード（スケジュールタスクの実行モード）
- [04_steering.md](04_steering.md) — Steering（スケジュールタスクの挙動を規約で導く）
- [05_sandbox.md](05_sandbox.md) — サンドボックス（実行環境）
- [04_reference/04_limits.md](../04_reference/04_limits.md#スケジュール実行タスクの上限) — 上限値（スケジュール 5・プロンプト 10,000 文字・カスタムスケジュールは 1 時間に 1 回まで）
- 公式: <https://kiro.dev/docs/web/automations/>

---

[← 01_features に戻る](README.md)
