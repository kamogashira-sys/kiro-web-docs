# Automations（定期実行）

> **本ページは Kiro Web 版（<https://app.kiro.dev>）の仕様です。**
> Kiro IDE / Kiro CLI とは別製品です。**Kiro Web は Preview 段階**です。

**出典**: <https://kiro.dev/docs/web/automations/>（Page updated: June 18, 2026）

Automations は、**セッションを自分で開始せずに、スケジュールに従ってプロンプトをリポジトリに対して実行させる**機能です。

> この機能は [2026-06-19 のエントリ](../02_update/01_changelog.md#2026-06-19-introducing-automations)で追加されました。

---

## 📑 このページの内容

1. [何ができるか](#何ができるか)
2. [オートメーションの作成](#オートメーションの作成)
3. [スケジュール](#スケジュール)
4. [一覧と操作](#一覧と操作)
5. [結果の確認](#結果の確認)

---

## 何ができるか

公式は次のように説明しています。

> You describe the work once, choose when it runs, and Kiro carries it out in **autonomous mode**. The agent reads the code, makes changes, and opens a pull request when there's something to review.

| 項目 | 内容 |
|------|------|
| 記述 | **作業内容を一度書く** |
| 実行タイミング | **スケジュールで指定** |
| 実行モード | **Autonomous モード**（[01_agent-modes.md](01_agent-modes.md#autonomous-モード)） |
| 動作 | コードを読み、変更を加え、**レビューすべきものがあればプルリクエストを作成** |

### 公式が挙げている用途

繰り返し発生する保守作業に向いているとして、次を挙げています。

- **changelog の生成**
- **新規 issue のトリアージ**
- **依存関係の更新**
- **マージ済みプルリクエストの要約**

---

## オートメーションの作成

`app.kiro.dev` の左サイドバーから **Automations** を開きます。

作成時に設定する項目は次のとおりです。

| 項目 | 内容 |
|------|------|
| **名前** | オートメーションの名前 |
| **Status** | **Enabled** のままにするとスケジュールで実行される。無効にすると実行せずに保存できる |
| **Prompt** | オートメーションが行うべきことを記述する。**最大 10,000 文字** |
| **リポジトリ** | 対象のリポジトリ（1つ以上） |
| **Schedules** | 実行タイミング（1つ以上・**最大 5 つ**） |

### ⚠️ プロンプトは「誰もいない状態で実行される」前提で書きます

公式は次のように注意しています。

> Be specific about the task and the expected output, since the automation runs without anyone there to clarify.

**明確化してくれる人がいない状態で実行される**ため、タスクと期待される出力を具体的に書く必要があります。

> 対話的なセッションと違い、**エージェントが質問しても答える人がいません。** タスクの書き方は
> [01_agent-modes.md](01_agent-modes.md#タスクを書くときのコツ公式の5項目) のコツが特に重要になります。
> チームの規約は [Steering ファイル](04_steering.md)に置いておくと毎回書かずに済みます。

---

## スケジュール

各オートメーションは**1つ以上のスケジュール**で動きます。

| 項目 | 値 |
|------|---|
| **1オートメーションあたりのスケジュール数** | **最大 5**（公式本文では綴りで `five`） |
| 各スケジュールの間隔 | **それぞれ別の間隔を設定できます** |

追加は **+ Add schedule** です。

### 3つのモード

| モード | 内容 |
|-------|------|
| **Hourly** | **毎時0分**に、`Run every` で指定した間隔で実行（例: 1 時間ごと・6 時間ごと） |
| **Daily** | **1 日 1 回**、指定した時刻に実行 |
| **CRON** | **カスタムの cron 式**で完全に制御 |

### ⚠️ スケジュールは UTC で評価されます

公式は次のように明記しています。

> Schedules are evaluated in **UTC**. In the automations list, a schedule's next run is shown in your local time alongside its UTC equivalent, for example At 9:00 AM (1:00 PM UTC).

| 項目 | 内容 |
|------|------|
| **評価のタイムゾーン** | **UTC** |
| 一覧の表示 | **ローカル時刻と UTC の両方**（例: `At 9:00 AM (1:00 PM UTC)`） |

設定中は生成された cron 式が下に表示されます（1 時間ごとなら `Generates: cron(0 */1 * * ? *)`）。

> **cron 式を自分で書く場合も UTC 基準**です。日本時間（JST = UTC+9）とは9時間ずれます。
> 「毎朝9時に実行」したい場合、cron では 0 時（UTC）を指定します。

---

## 一覧と操作

**Automations** の一覧では、各行に次が表示されます。

| 表示項目 |
|--------|
| オートメーションの名前 |
| プロンプトのプレビュー |
| 接続されているリポジトリ |
| スケジュール |
| 現在のステータス |

| 操作 | 方法 |
|------|------|
| 名前で検索 | 検索ボックス |
| 状態で絞り込み | ステータスフィルタ |
| **Edit** | 名前・プロンプト・リポジトリ・ステータス・スケジュールを変更 |

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

> Each time an automation runs, it creates a session visible in your session list alongside interactive sessions.

**実行のたびにセッションが作られ、対話的なセッションと並んでセッション一覧に表示されます。** 実行のセッションを開くと、会話・実行したステップ・作成されたプルリクエストを確認できます。

> 公式は、これが**オートメーションが期待どおりに動いているかを確認する最良の方法**であり、
> 期待した変更が出なかった実行のトラブルシュートにも使えるとしています。

### 変更はプルリクエストとして提出されます

公式は次のように明記しています。

> Because the work lands as a pull request rather than a direct commit, nothing reaches your main branch without your review.

| 項目 | 内容 |
|------|------|
| 提出形式 | **プルリクエスト**（直接コミットではない） |
| 対象 | **影響を受ける各リポジトリ**ごとに作成される |
| 帰結 | **レビューなしに main ブランチへ届くものはありません** |

### 実行ごとに独立したサンドボックス

[2026-06-19 のエントリ](../02_update/01_changelog.md#2026-06-19-introducing-automations)で公式は次のように説明しています。

> Each run spins up an independent sandbox, clones your repositories, executes the work autonomously, and opens a pull request with the changes.

**実行ごとに独立したサンドボックスが起動**します（[05_sandbox.md](05_sandbox.md)）。

---

## 🔗 関連ページ

- [01_agent-modes.md](01_agent-modes.md) — Autonomous モード（オートメーションの実行モード）
- [04_steering.md](04_steering.md) — Steering（オートメーションの挙動を規約で導く）
- [05_sandbox.md](05_sandbox.md) — サンドボックス（実行環境）
- [04_reference/04_limits.md](../04_reference/04_limits.md#オートメーションの上限) — 上限値（スケジュール 5・プロンプト 10,000 文字）
- 公式: <https://kiro.dev/docs/web/automations/>

---

[← 01_features に戻る](README.md)
