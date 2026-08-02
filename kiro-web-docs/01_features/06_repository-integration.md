# GitHub / GitLab 連携

> **本ページは Kiro Web 版（<https://app.kiro.dev>）の仕様です。**
> Kiro IDE / Kiro CLI とは別製品です。**Kiro Web は Preview 段階**です。

**出典**: <https://kiro.dev/docs/web/github/>（Page updated: June 11, 2026）・<https://kiro.dev/docs/web/gitlab/>（Page updated: July 16, 2026）

Kiro Web は **GitHub と GitLab の両方**に対応しています。**1つのセッションで両方を混在**させることもできます。

> GitLab 対応は [2026-06-11 のエントリ](../02_update/01_changelog.md#2026-06-11-gitlab-support-and-specs-in-the-browser)で追加されました。

---

## 📑 このページの内容

1. [GitHub と GitLab の比較](#github-と-gitlab-の比較)
2. [GitHub — インストールと権限](#github--インストールと権限)
3. [GitHub — issue からタスクを割り当てる](#github--issue-からタスクを割り当てる)
4. [GitHub — PR の作成者と authorship](#github--pr-の作成者と-authorship)
5. [PR フィードバックへの対応](#pr-フィードバックへの対応)
6. [複数ユーザーで同じリポジトリを使う](#複数ユーザーで同じリポジトリを使う)
7. [GitLab — 接続とトークン](#gitlab--接続とトークン)
8. [GitLab — 権限の絞り方](#gitlab--権限の絞り方)
9. [GitLab — ネットワークアクセス](#gitlab--ネットワークアクセス)
10. [両方を1セッションに混在させる](#両方を1セッションに混在させる)

---

## GitHub と GitLab の比較

| 項目 | **GitHub** | **GitLab** |
|------|-----------|-----------|
| 接続方法 | **Kiro Agent GitHub app** の認可 | **パーソナルアクセストークン（PAT）** |
| 提出形式 | **プルリクエスト** | **マージリクエスト** |
| issue からのタスク割り当て | ✅ **`kiro` ラベル / `/kiro` コメント** | 記載なし（**未確認**） |
| PR 作成者の切り替え | ✅ 設定で自分のユーザーに変更できる | 記載なし（**未確認**） |
| セルフホスト | — | ✅ 対応（**インターネット到達性が必要**） |
| プライベート（VPC 内のみ） | — | ❌ **未対応**（公式明記） |

### 共通の動作

どちらも次の流れです。

| # | 動作 |
|---|------|
| 1 | **隔離されたサンドボックス**に認可されたリポジトリ／プロジェクトをクローンする |
| 2 | **フィーチャーブランチを作成**し、明確なメッセージでコミットし、プッシュする |
| 3 | **変更内容・実装方針・検討したトレードオフ**を説明した PR / MR を作成する |

### コミットの共同作者

公式は両方のページで次のように説明しています。

> The agent acts on your behalf and includes both you and itself as co-authors in every commit, ensuring proper attribution.

**すべてのコミットに、利用者とエージェントの両方が共同作者として記録されます。**

---

## GitHub — インストールと権限

### 接続手順

1. <https://app.kiro.dev> にアクセスして **Settings > Agent** に移動する
2. **GitHub** の下の **Connect GitHub** をクリックする
3. **Kiro Agent GitHub app** を認可する
4. **特定のリポジトリ**または**組織のすべてのリポジトリ**へのアクセスを許可する

### 2層のアクセス制御

公式は「Connecting to GitHub requires several layers of access control」として、次の構造を説明しています。

| 層 | 誰が設定するか | 何を決めるか |
|---|--------------|-----------|
| **アプリのインストール** | **組織またはアカウントのオーナー**（**1回のみ**） | **Kiro がアクセスできるリポジトリの最大範囲**。設定はグローバルで、組織の全ユーザーが共有する |
| **リポジトリレベルのアクセス** | 各ユーザー | 自分が**書き込み権限**を持つリポジトリのみ作業できる |

公式は「This two-layer approach ensures that owners control the maximum scope of access while individual users can only assign tasks to repositories they personally have access to」と説明しています。

### 表示されるリポジトリの条件（2つを同時に満たす）

| # | 条件 |
|---|------|
| 1 | **Kiro Agent GitHub app** がそのリポジトリにインストール・認可されている |
| 2 | **自分の GitHub アカウント**がそのリポジトリにアクセスできる |

この2条件を満たす限り、**誰がアプリをインストールしたかに関わらず**、個人アカウント・共有リポジトリ・組織のリポジトリが表示されます。

### タスクを割り当てられるのは書き込み権限があるリポジトリのみ

公式は次のように明記しています。

> Users can only assign tasks to repositories where they have **write permissions**. Other users cannot assign tasks on your behalf—each user controls their own agent tasks.

| 項目 | 内容 |
|------|------|
| タスクの割り当て | **書き込み権限があるリポジトリのみ** |
| 他ユーザーによる代理割り当て | **できません**（各ユーザーが自分のエージェントタスクを制御する） |

---

## GitHub — issue からタスクを割り当てる

| 方法 | 動作 |
|------|------|
| **`kiro` ラベルを付ける** | Kiro が作業を開始し、**その issue のすべてのコメントを聞き取って**追加のコンテキストやフィードバックとして扱う |
| **コメントで `/kiro` とメンションする** | **その issue を** Kiro に割り当てる |

### 前提条件

| 条件 | 未達の場合 |
|------|----------|
| **Kiro Agent GitHub app がそのリポジトリにインストールされている** | 動作しません |
| **GitHub アカウントを Kiro に登録済み** | `/kiro` を使うと**サインアップ方法の案内が届きます** |

---

## GitHub — PR の作成者と authorship

### 既定は Kiro Agent GitHub app です

公式は次のように説明しています。

> By default, pull requests are created by the Kiro Agent GitHub app. You can change this so PRs are created as your GitHub user instead

### 自分のユーザーに変更する手順

1. **Settings** → **Agent** タブ
2. **Pull request** の下の **Create pull requests as your GitHub user** をオンにする

### いつ必要か（公式の説明）

> This is useful when your repository has **branch protection rules** or **CI workflows** that depend on the PR author.

| 状況 | 理由 |
|------|------|
| **ブランチ保護ルール**がある | PR の作成者に依存する |
| **CI ワークフロー**がある | 同上 |

> **PR 作成者が app のままだと CI が動かない**構成があります。CI が期待どおりに走らない場合は
> この設定を確認してください。

### エージェントが応答する相手

公式は「The agent only responds to your explicit feedback and instructions (the user who created the task)」としています。**タスク作成者の明示的なフィードバックと指示にのみ応答します。**

---

## PR フィードバックへの対応

### 2つのコマンド

| コマンド | 動作 | 使いどき |
|---------|------|---------|
| **`/kiro all`** | **PR 全体の、すべてのレビュアーからのすべてのコメント**に対応する | フィードバックを一度に処理したいとき |
| **`/kiro fix`** | **特定の会話スレッド内のすべてのコメント**に対応する | 1つの議題に集中したいとき |

### コメントを対応対象から外す方法

公式は次のように説明しています。

> To prevent a comment from being addressed, **delete it** or **reply with your own perspective** before using a command.

| 方法 |
|------|
| **コメントを削除する** |
| **コマンドを使う前に自分の見解を返信する** |

`app.kiro.dev/agent` のタスクビューからフィードバックを与えることもできます。

### GitHub Action のフィードバック

公式は次のように説明しています。

> GitHub Action feedback (automated checks, tests, security scans) is **automatically addressed** when you provide any feedback.

**自動チェック・テスト・セキュリティスキャンの結果は、何らかのフィードバックを与えると自動的に対応されます。**

### ⚠️ 「対応する」と「学習する」は別です

| 動作 | 対象 |
|------|------|
| **コメントに対応する**（`/kiro all`） | **すべてのレビュアー**のコメント |
| **エージェントが学習する** | **タスク作成者のフィードバックのみ**（他のレビュアーのコメントは学習に影響しません） |

詳細は [04_steering.md](04_steering.md#コードレビューを通じて教える) を参照してください。

---

## 複数ユーザーで同じリポジトリを使う

公式は「each user can independently assign tasks」として、次を説明しています。

| # | 動作 |
|---|------|
| 1 | **Kiro Agent GitHub app はリポジトリごとに1回インストールすれば足りる** |
| 2 | 登録済みの各ユーザーが**独立してタスクを割り当てられる** |
| 3 | **複数ユーザーが同じ GitHub issue を割り当てた場合、ユーザーごとに別々のタスクが作られる** |
| 4 | 各タスクは**それぞれ独立した隔離サンドボックス**で実行される |

### 公式が挙げるベストプラクティス

- **チームで調整して同じ issue の重複作業を避ける**
- **GitHub の issue 割り当て機能**で誰が何をしているかを示す
- 似たタスクを割り当てる前に**オープンな PR を確認**して競合を避ける

> **同じ issue に複数人が `kiro` ラベルを付けると、人数分のタスクが走ります。** 意図しない
> 重複を避けるための注意です。

---

## GitLab — 接続とトークン

### 接続手順

1. GitLab で自分のアバターを選び **Preferences** → **Access > Personal access tokens** → **Generate token**
2. **トークンの形式を選んで**作成する（[下記](#gitlab--権限の絞り方)）
3. Kiro で **Settings** → **Agent** タブ
4. **GitLab** の下の **Connect GitLab** をクリック
5. パーソナルアクセストークンを貼り付け、**GitLab インスタンスを選ぶ**（既定で `gitlab.com`）

接続後は、セッション作成時またはセッション中のリポジトリ追加時に GitLab のプロジェクトを選べます。

### セルフホストの GitLab

公式は次のように説明しています。

> If you use a self-managed GitLab instance, update the **Instance URL** to point to your instance when configuring your personal access token. **Self-managed instances must be reachable over the internet** for Kiro Web to connect.

| 項目 | 内容 |
|------|------|
| 設定 | **Instance URL** を自分のインスタンスに変更する |
| 要件 | **インターネット経由で到達可能でなければなりません** |

### ⚠️ トークンの有効期限に注意

公式は次のように説明しています。

> GitLab personal access tokens can have an expiration date. When your token expires, **Kiro Web loses access** to your GitLab projects. You'll see a connection error when trying to use GitLab in a session.

| 事象 | 対処 |
|------|------|
| トークンが期限切れ | **GitLab プロジェクトへのアクセスを失う**。セッションで GitLab を使おうとすると接続エラーになる |
| 復旧 | **同じ権限で新しいトークンを生成**し、**Settings > Agent** で更新する |

---

## GitLab — 権限の絞り方

エージェントのアクセス範囲は**パーソナルアクセストークンに与えた権限で決まります**。GitLab には2種類のトークンがあります。

### Fine-grained token（公式の推奨）

公式は fine-grained token を **recommended** としています。スコープではなく**粒度の細かい権限**を使い、特定のリソースとリポジトリに限定できます。

**付与する権限**:

| セクション | 必要な権限 |
|-----------|----------|
| **Group and project** | Code（Download, Push）・Merge Request（Read, Create）・Work Item（Read） |
| **User** | Project（Read）・User（Read） |

> ⚠️ **公式の注意**: **`Project (Read)` は User セクションで付与する必要があります。**
> Group and project 側だけで付与しても、**Kiro はプロジェクトを一覧できません。**

`Work Item (Read)` は**issue とマージリクエストのコメントの読み取り**をカバーします。

トークン作成時は、**Kiro に作業させたいリポジトリを group and project access に含める**設定にします。

### ⚠️ プロジェクト一覧に出てもクローンできないことがあります

公式は次のように説明しています。

> The project picker lists all projects you are a member of, but the agent can only clone and push to repositories **within the token's group and project access**. A project can appear in the picker yet fail to clone if it is outside the token's selection.

| 項目 | 挙動 |
|------|------|
| プロジェクトピッカーの表示 | **自分がメンバーである全プロジェクト** |
| エージェントが実際に扱える範囲 | **トークンの group and project access の範囲内のみ** |
| 症状 | ピッカーには出るが**クローンに失敗する** |
| 対処 | **GitLab でトークンの group and project access を編集**して対象プロジェクトを含める |

### Legacy token（スコープ）

| スコープ | できること |
|---------|----------|
| **`api`** | **フルアクセス**。Kiro の GitLab 機能すべてに対応 |
| **`read_api`** | **読み取り専用**。プロジェクト・MR・issue を確認できるが、**ブランチのプッシュや MR の作成はできない** |
| **`write_repository`** | **コードへのアクセスのみ**。ブランチのプッシュと MR の作成はできるが、**issue にアクセスできない** |

### その他のアクセスに関する注意

- エージェントは**自分の GitLab ユーザーがアクセスできるプロジェクトにのみ**アクセスできる
- **アクセスの取り消し**は、GitLab でパーソナルアクセストークンを削除するか、**Settings の Agent タブから GitLab を切断**する

> 出典の [03_deployment/01_setup.md](../03_deployment/01_setup.md#gitlab-を接続する) は
> `setup` ページ（Page updated: June 11, 2026）に基づき「`api` スコープ」を案内していますが、
> **より新しい `gitlab` ページ（July 16, 2026）は fine-grained token を推奨**しています。
> 新規に作成する場合は fine-grained token を検討してください。

---

## GitLab — ネットワークアクセス

### 公開インスタンス（IP 許可リストがある場合）

GitLab インスタンスがインターネット経由で到達可能で、**IP 許可リストやファイアウォールルールを使っている場合**、Kiro Web の**送信元 IP からの受信を許可**する必要があります。

| リージョン | 送信元 IP |
|-----------|----------|
| **US East（N. Virginia）`us-east-1`** | `34.228.181.128`<br>`44.219.176.187`<br>`54.226.244.221` |

一覧は [04_reference/01_allowed-domains.md](../04_reference/01_allowed-domains.md#3-gitlab-側で許可する送信元-ip3-件) にもあります。

### ⚠️ VPC 内のみのインスタンスは未対応です

公式は次のように明記しています。

> Kiro Web does **not yet support** GitLab instances that are only accessible from within an AWS VPC.

**AWS VPC 内からのみアクセス可能な GitLab インスタンスには対応していません。**

---

## 両方を1セッションに混在させる

公式は次のように説明しています。

> You can add both GitLab and GitHub repositories to the same session. The agent works across all selected repositories at once—reading code, making changes, and **opening a merge request on GitLab and a pull request on GitHub as appropriate for each provider**.

| 項目 | 内容 |
|------|------|
| 混在 | **GitLab と GitHub を同一セッションに追加できる** |
| 動作 | 選択したすべてのリポジトリで同時に作業する |
| 提出 | **プロバイダごとに適切な形式**（GitLab は MR・GitHub は PR） |

これにより、**異なるプロバイダにホストされたプロジェクトにまたがる変更を調整**できます。

> **⚠️ 公式の警告（繰り返し）**: 信頼できるリポジトリだけを選んでください。**特に公開リポジトリと
> 非公開リポジトリを混在させるときは注意が必要です。** エージェントは
> **リポジトリのコードにある指示から学習し、それに従います。その指示が悪意あるものであっても同様です。**

---

## エージェントに依頼できること

### GitHub

| 種類 | 内容 |
|------|------|
| **コードの作業** | リポジトリのクローン・変更・ブランチのプッシュ・**プルリクエストの作成** |
| **プルリクエストの確認** | オープン／最近マージされた PR の一覧・PR のコメントの読み取り・**インラインのレビューコメントの読み取り** |
| **issue の確認** | オープンな issue の一覧・特定の issue の詳細表示 |

### GitLab

| 種類 | 内容 |
|------|------|
| **コードの作業** | プロジェクトのクローン・変更・ブランチのプッシュ・**マージリクエストの作成** |
| **マージリクエストの確認** | オープン／マージ済み MR の一覧・**詳細と差分の表示**・MR のブランチの特定・**ディスカッションとノートの読み取り** |
| **issue の確認** | オープンな issue の一覧・詳細表示・コメントの読み取り |

---

## 🔗 関連ページ

- [01_agent-modes.md](01_agent-modes.md) — タスクの作り方（issue からの割り当てを含む）
- [04_steering.md](04_steering.md) — PR フィードバックによる学習
- [05_sandbox.md](05_sandbox.md) — サンドボックス（クローン先）
- [03_deployment/01_setup.md](../03_deployment/01_setup.md) — 接続のセットアップ手順
- [04_reference/01_allowed-domains.md](../04_reference/01_allowed-domains.md) — GitLab 送信元 IP
- 公式: <https://kiro.dev/docs/web/github/>・<https://kiro.dev/docs/web/gitlab/>

---

[← 01_features に戻る](README.md)
