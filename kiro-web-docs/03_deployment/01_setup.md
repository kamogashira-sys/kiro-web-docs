# セットアップと最初のタスク

> **本ページは Kiro Web 版（<https://app.kiro.dev>）の仕様です。**
> Kiro IDE / Kiro CLI とは別製品です。**Kiro Web は Preview 段階**です。

**出典**: <https://kiro.dev/docs/web/setup/>（Page updated: June 11, 2026）・<https://kiro.dev/docs/web/first-task/>（Page updated: April 21, 2026）

Kiro Web はブラウザから使うサービスなので、**インストールはありません**。「サインイン」と「リポジトリプロバイダの接続」が導入作業になります。

---

## 📑 このページの内容

1. [セットアップの流れ](#セットアップの流れ)
2. [ソーシャルログインの場合](#ソーシャルログインの場合)
3. [AWS Identity Center の場合](#aws-identity-center-の場合)
4. [GitHub を接続する](#github-を接続する)
5. [GitLab を接続する](#gitlab-を接続する)
6. [最初のタスクを実行する](#最初のタスクを実行する)

---

## セットアップの流れ

公式は、**サインイン方法によって手順が異なる**と説明しています。

| サインイン方法 | 前提 | 手順 |
|--------------|------|------|
| **ソーシャルログイン** | AWS Builder ID | [下記](#ソーシャルログインの場合) |
| **AWS Identity Center** | 管理者による有効化が必要 | [下記](#aws-identity-center-の場合) |

どちらの場合も、最後に**リポジトリプロバイダ（GitHub または GitLab）の接続**が必要です。公式は「Kiro Web works with both GitHub and GitLab」と説明しています。

---

## ソーシャルログインの場合

公式の手順は3ステップです。

1. <https://app.kiro.dev> にアクセスし、**AWS Builder ID** でサインインする
2. **有料の Kiro サブスクリプション（Pro 以上）**があることを確認する
3. **リポジトリプロバイダ（GitHub または GitLab）を接続**して、エージェントにリポジトリへのアクセスを与える

<a id="free-tier-conflict"></a>
### ⚠️ 無料枠については公式ページ間で記述が食い違っています（未解決）

本ページの出典である `docs/web/setup/` には、次の記述があります。

> Kiro Web is not available on the free tier.

一方、**より新しい** `docs/web/data-protection/`（Page updated: July 14, 2026）には **Free Tier ユーザー**を前提とした記述があります（データ保持期間・オプトアウト・不正利用検知）。詳細は [03_data-protection.md](03_data-protection.md) を参照してください。

**本サイトはどちらが正しいかを断定しません。** 上記の「Pro 以上が必要」を主たる記述として示しつつ、食い違いがあることを明記します。実際の適用条件は公式ページで確認してください。

---

## AWS Identity Center の場合

### ⚠️ Preview 中の重要な制約（公式の警告）

公式は警告として次の2点を挙げています。

| 制約 | 内容 |
|------|------|
| **リージョン** | Preview 中は **US East（N. Virginia）`us-east-1` のみ** |
| **管理者の有効化が必要** | Kiro を構成している AWS アカウントで **Settings > Kiro Settings** から有効化しないと、利用者はアクセスできない |

### 公式の手順

1. **管理者が組織向けに Kiro Web エージェントを有効化する**
2. Identity Center の資格情報で <https://app.kiro.dev> にサインインする
3. **Kiro Profile が必要**（**Q Developer Profile では動作しません**）
4. リポジトリプロバイダ（GitHub または GitLab）を接続する

要件・制限の詳細は [02_identity-center.md](02_identity-center.md) にまとめています。

---

## GitHub を接続する

公式の手順は4ステップです。

1. **Settings** に移動し、**Agent** タブを選ぶ
2. **GitHub** の下の **Connect GitHub** をクリックする
3. **Kiro Agent GitHub app** を認可する
4. エージェントがアクセスできるリポジトリを選ぶ

### 書き込み権限が必要です

公式は次のように説明しています。

> You must have write permissions on repositories for the agent to create branches and open pull requests.

エージェントがブランチを作成しプルリクエストを開くため、**対象リポジトリへの書き込み権限**が必要です。

### 表示されるリポジトリの条件

公式は「Kiro Web shows all repositories where both conditions are met」として、**次の2つを同時に満たすリポジトリ**が表示されると説明しています。

| # | 条件 |
|---|------|
| 1 | **自分の GitHub ユーザー**がそのリポジトリにアクセスできる |
| 2 | **Kiro Agent GitHub app** がそのリポジトリに対してインストール・認可されている |

この2条件を満たす限り、個人アカウント・共有リポジトリ・組織のリポジトリのいずれも表示されます。

> 逆に言えば、**どちらか一方でも欠けていると表示されません**。リポジトリが見えないときは
> 両方を確認してください。

詳細は [01_features/06_repository-integration.md](../01_features/) を参照してください。

---

## GitLab を接続する

Kiro Web は **パーソナルアクセストークン（PAT）** で GitLab に接続します。公式の手順は5ステップです。

1. GitLab で自分のアバターを選び **Preferences** → **Access > Personal access tokens** → **Generate token**
2. **スコープを選んで**トークンを作成しコピーする
3. Kiro で **Settings** → **Agent** タブ
4. **GitLab** の下の **Connect GitLab** をクリック
5. パーソナルアクセストークンを貼り付け、**GitLab インスタンスを選ぶ**（既定で `gitlab.com` が入力されています）

### スコープについて

公式は次のように説明しています。

> The `api` scope gives Kiro full access; see the GitLab integration guide if you want to scope the token down

**`api` スコープは Kiro にフル権限を与えます。** 絞りたい場合は公式の GitLab 連携ガイド（<https://kiro.dev/docs/web/gitlab/>）を参照してください。

接続後は、セッション作成時またはセッション中のリポジトリ追加時に GitLab のプロジェクトを選べるようになります。

> ファイアウォールで送信元 IP の許可が必要な場合は
> [04_reference/01_allowed-domains.md](../04_reference/) を参照してください。

---

## 最初のタスクを実行する

**出典**: <https://kiro.dev/docs/web/first-task/>（Page updated: April 21, 2026）

### 1. セッションを開始する

1. <https://app.kiro.dev> にアクセスする
2. タスクを開始する前に、必要なら **Select repo** でリポジトリを選ぶ（**任意**）

> リポジトリの選択は必須ではありません。後から接続できます
> （[2026-06-02 のエントリ](../02_update/01_changelog.md#2026-06-02-start-without-a-repo-switch-modes-anytime)で
> リポジトリ未接続の開始に対応しました）。

### 2. タスクを記述する

やってほしいことを明確に書きます。公式が挙げている例は次のとおりです。

**単一リポジトリの例**:

- "Add error handling to the login function in auth.ts"
- "Write unit tests for the UserService class"
- "Update the README with installation instructions"

**複数リポジトリにまたがる例**:

- "Add a new API endpoint in the backend service and update the frontend client to call it"
- "Update the shared authentication library and migrate both the web and mobile apps to use the new version"

特定の要件や制約は記述に含めます。会話の進行に合わせて後から詳細を追加・修正できます。

### 3. リポジトリを選ぶ

セッション開始時に選んでいない場合、作業を依頼した時点で選択を求められます。

> **⚠️ 公式の警告**: 信頼できるリポジトリだけを選んでください。**特に公開リポジトリと
> 非公開リポジトリを混在させるときは注意が必要です。** エージェントは
> **リポジトリのコードにある指示から学習し、それに従います。その指示が悪意あるものであっても同様です。**

### 4. モードによって進み方が変わる

| モード | 進み方 |
|-------|-------|
| **既定のモード** | エージェントが対話的に作業します。依頼を分析し、進め方を相談し、一緒に反復します。納得したらプルリクエストの作成を依頼します |
| **Autonomous モード** | チャット入力バーで **Autonomous** を有効にします。エージェントが明確化の質問をし、計画を立て、専門のサブエージェントで作業を実行し、**自動的にプルリクエストを作成**します |

詳細は [01_features/01_agent-modes.md](../01_features/) を参照してください。

### 5. プルリクエストをレビューする

エージェントがプルリクエストを作成したら、公式は次を挙げています。

- コードの変更と実装方針を確認する
- フィードバックや提案をコメントで残す
- **エージェントが自動的にコメントに対応し、更新をプッシュします**

公式は次のように説明しています。

> Comments like "always use our standard error handling" or "remember to follow our naming conventions" help the agent learn your team's patterns for future work.

「常に標準のエラーハンドリングを使って」「命名規約に従うように」といったコメントは、**今後の作業に向けてチームのパターンを学習させる**のに役立ちます。

---

## 🔗 関連ページ

- [02_identity-center.md](02_identity-center.md) — AWS Identity Center の要件と制限
- [03_data-protection.md](03_data-protection.md) — データ保護（保存リージョン・暗号化・オプトアウト）
- [04_firewalls.md](04_firewalls.md) — ファイアウォール・プロキシの設定
- [01_features](../01_features/) — 機能詳細ガイド
- 公式: <https://kiro.dev/docs/web/setup/>・<https://kiro.dev/docs/web/first-task/>

---

[← 03_deployment に戻る](README.md)
