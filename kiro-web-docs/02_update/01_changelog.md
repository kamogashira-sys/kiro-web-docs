# Kiro Web 更新履歴（全19エントリ）

> **本ページは Kiro Web 版（<https://app.kiro.dev>）の更新履歴です。**
> Kiro IDE / Kiro CLI の更新は別製品のものです（姉妹サイトを参照してください）。
> **Kiro Web は [2026-09-01 に一般提供（GA）になりました](https://kiro.dev/changelog/web/kiro-web-is-now-generally-available/)。**

**出典**: [公式 changelog（Web 系列）](https://kiro.dev/changelog/web/)
**収録範囲**: 公式 changelog の `web` 系列**全19エントリ**（2025-12-02 〜 2026-09-01）
**情報の基準日**: 2026-09-13（公式 snapshot の取得日。出典日は各公式エントリの公開日）

---

## 📑 このページの読み方

### Kiro Web にはバージョン番号がありません

Kiro IDE の `1.0.242` のような版番号が Kiro Web には**存在しません**。公式 changelog のエントリは**日付とタイトル**だけで識別されます。本ページでは各エントリを **`YYYY-MM-DD` ＋ 公式タイトル**の形で見出しにしています。

> 版番号が存在しない**理由**は公式に説明がないため**未確認**です。

### 折りたたまれている項目も全部載せています

公式サイトでは一部のエントリの `Improvements` / `Fixes` が**初期状態で折りたたまれて**います。本ページは**折りたたみの中身も省略せず全量**を掲載しています（該当2エントリ・計21項目）。

### 各エントリの構造は2種類あります

| 種類 | 構造 | 件数 |
|------|------|------|
| **機能紹介型** | 導入文（＋機能ごとの節） | 5 |
| **保守型** | 導入文（＋節）＋ `Improvements` / `Fixes` の一覧 | 2 |

---

## 📅 エントリ一覧（新しい順）

| 日付 | エントリ | 種類 | 主な内容 |
|------|---------|------|---------|
| 2026-09-01 | [Use Cloud Configuration in Local Sessions](#2026-09-01-use-cloud-configuration-in-local-sessions) | 機能紹介型 | 公式 changelog の告知 |
| 2026-09-01 | [Kiro Web Is Now Generally Available](#2026-09-01-kiro-web-is-now-generally-available) | 機能紹介型 | 公式 changelog の告知 |
| 2026-08-31 | [Pick a Branch When You Pick a Repository](#2026-08-31-pick-a-branch-when-you-pick-a-repository) | 機能紹介型 | 公式 changelog の告知 |
| 2026-08-27 | [Sessions Name Themselves](#2026-08-27-sessions-name-themselves) | 機能紹介型 | 公式 changelog の告知 |
| 2026-08-22 | [Organize Sessions into Groups](#2026-08-22-organize-sessions-into-groups) | 機能紹介型 | 公式 changelog の告知 |
| 2026-08-19 | [Recent Repositories in the Repository Selector](#2026-08-19-recent-repositories-in-the-repository-selector) | 機能紹介型 | 公式 changelog の告知 |
| 2026-08-17 | [Access Kiro Web with Okta or Microsoft Entra ID](#2026-08-17-kiro-web-access-with-okta-and-microsoft-entra-id) | 機能紹介型 | 公式 changelog の告知 |
| 2026-08-11 | [Sync your local .kiro configuration to the cloud](#2026-08-11-cloud-configuration) | 機能紹介型 | 公式 changelog の告知 |
| 2026-07-23 | [Playwright and Agent-Browser Support](#2026-07-23-playwright-and-agent-browser-support) | 機能紹介型 | 公式 changelog の告知 |
| 2026-07-20 | [Inspect GitHub Pull Requests Inside Kiro Web](#2026-07-20-github-pull-request-workflow-inside-kiro-web) | 機能紹介型 | 公式 changelog の告知 |
| 2026-07-16 | [GitLab Fine-Grained Access Token Support](#2026-07-16-gitlab-fine-grained-access-token-support) | 機能紹介型 | 公式 changelog の告知 |
| 2026-07-13 | [Workspace File Explorer for Cloud Sessions](#2026-07-13-workspace-file-explorer-for-cloud-sessions) | 機能紹介型 | 公式 changelog の告知 |
| 2026-07-01 | [IAM Roles and Authorize Powers for Third-Party Services](#2026-07-01-iam-roles-and-authorize-powers-for-third-party-services) | 機能紹介型 | サンドボックス用 IAM ロール・Powers の認可フロー |
| 2026-06-19 | [Introducing Automations](#2026-06-19-introducing-automations) | 機能紹介型 | 定期実行（Automations） |
| 2026-06-11 | [GitLab Support and Specs in the Browser](#2026-06-11-gitlab-support-and-specs-in-the-browser) | 機能紹介型 | GitLab 対応・ブラウザでの Specs |
| 2026-06-02 | [Start Without a Repo, Switch Modes Anytime](#2026-06-02-start-without-a-repo-switch-modes-anytime) | **保守型**（10項目） | リポジトリ未接続での開始・セッション中のモード切替 |
| 2026-05-19 | [Session Stability, Stop Control, and Mobile Layout Fixes](#2026-05-19-session-stability-stop-control-and-mobile-layout-fixes) | **保守型**（11項目） | 停止ボタン・モバイルレイアウト・セッション安定性 |
| 2026-05-07 | [Introducing Kiro Web (Preview)](#2026-05-07-introducing-kiro-web-preview) | 機能紹介型 | **Kiro Web の提供開始（Preview）** |
| 2025-12-02 | [Introducing Kiro autonomous agent](#2025-12-02-introducing-kiro-autonomous-agent) | 機能紹介型 | autonomous agent のプレビュー提供開始 |

---

<a id="2026-07-01-iam-roles-and-authorize-powers-for-third-party-services"></a>

## 2026-07-01: IAM Roles and Authorize Powers for Third-Party Services

**出典**: <https://kiro.dev/changelog/web/iam-roles-and-authorize-powers-for-third-party-services/>（July 1, 2026）

このリリースでは、サンドボックスから AWS リソースへ直接アクセスできるようになり、Figma などのサービスへ Powers を接続する手順が簡素化された、と公式は説明しています。

### IAM Role For Sandbox

Kiro Web がタスク実行時にユーザーに代わって引き受ける IAM ロールを設定できます。サンドボックスは**短期間だけ有効な認証情報**を受け取り、エージェント・CLI ツール・MCP サーバーがいずれもその認証情報で AWS リソースを操作できます。認証情報はタスク実行中に**自動更新**され、タスク完了時に**削除**されます。

設定場所は **Settings > Agent > Sandbox > AWS Credentials** です。

> 詳細は [04_reference/02_environment-variables.md](../04_reference/) を参照してください。

### Authorize Powers for Third-Party services

サードパーティサービスに接続する Powers が、**標準的な認可フロー**を使うようになりました。Agent 設定の **Manage Powers** から一度認可すれば、以降のタスクでは再度確認されることなくその接続が使われます。**いつでも接続を解除して即座にアクセスを取り消せます**。

トークンは**保存時に暗号化**され、**サンドボックスにもエージェントにも渡されません**。

---

<a id="2026-06-19-introducing-automations"></a>

## 2026-06-19: Introducing Automations

**出典**: <https://kiro.dev/changelog/web/introducing-automations/>（June 19, 2026）

Kiro Web で**定期的な作業をスケジュール実行**できるようになりました。オートメーションを作成してタスクを記述し、リポジトリを選び、実行間隔を設定します。

Kiro Web の **Automations** から定期タスクを設定します。1つのオートメーションにつき**最大5つのスケジュール**を、組み込みの選択肢（hourly・daily）または **cron 式**で追加できます。実行ごとに**独立したサンドボックス**が起動してリポジトリをクローンし、作業を自律的に実行して、変更をプルリクエストとして提出します。

オートメーションは**いつでも編集・無効化・削除**できます。変更は**次回のスケジュール実行から適用**されます。

> 機能の詳細は [01_features/03_automations.md](../01_features/)、上限値は [04_reference/04_limits.md](../04_reference/) を参照してください。

---

<a id="2026-06-11-gitlab-support-and-specs-in-the-browser"></a>

## 2026-06-11: GitLab Support and Specs in the Browser

**出典**: <https://kiro.dev/changelog/web/gitlab-support-and-specs-in-the-browser/>（June 11, 2026）

このリリースで Kiro Web は GitHub 以外にも対応範囲を広げ、**GitLab の完全サポート**と**ブラウザでの Specs ワークフロー**が加わりました。GitLab リポジトリは**パーソナルアクセストークン**で接続し、エージェントがコードを書き始める前に、要件・設計・タスクのファイルとしてレビュー可能な形で計画を立てられます。

### Connect your GitLab repositories

GitHub と同じように GitLab リポジトリで作業できます。エージェントがリポジトリをクローンし、コードを書き、**マージリクエスト**を代わりに作成します。**パーソナルアクセストークン**で接続し、チャットを離れずに既存のマージリクエストやレビュー中の issue を確認できます。**1つのセッションで GitLab と GitHub のリポジトリを混在**させることもできます。

> 接続手順と送信元 IP は [01_features/06_repository-integration.md](../01_features/)・[04_reference/01_allowed-domains.md](../04_reference/) を参照してください。

### Specs in the browser

作りたいもの・直したいもの・計画したいことを記述すると、Kiro が**要件・設計・タスク**のファイルを生成し、作業開始前にレビューできます。チャットを通じて計画を編集し、**全タスクの実行**または**選択したタスクのみの実行**ができ、完了後に成果物を**ダウンロード**できます。**1つの spec セッションが複数リポジトリにまたがる**ことができ、エージェントはそれら全体を見て計画します。

> 詳細は [01_features/02_specs.md](../01_features/) を参照してください。

---

<a id="2026-06-02-start-without-a-repo-switch-modes-anytime"></a>

## 2026-06-02: Start Without a Repo, Switch Modes Anytime

**出典**: <https://kiro.dev/changelog/web/start-without-a-repo-switch-modes-anytime/>（June 2, 2026）

GitHub リポジトリを先に接続しなくても Kiro Web のセッションを開始できるようになり、Vibe セッションの**任意のタイミングで** Autonomous モードに切り替えられるようになりました。このアップデートでは相対的なメッセージ時刻表示、ネットワークモードの可視化、サンドボックスと信頼性の修正も入っています。

### Start without a GitHub repo

セッション開始に GitHub リポジトリの追加が**不要**になりました。セッションを開いてタスクを記述し、必要になってからリポジトリを接続できます。

### Switch to Autonomous mode mid-session

Vibe セッションでは、**最初のプロンプトを送った後でも** Autonomous モードを選択できるようになりました（従来はセッション開始時のみ）。やり直さずに、好きなタイミングでエージェントに引き渡せます。

### Message timestamps

セッションのメッセージに**相対的な時刻**が表示されます。ホバーすると絶対時刻が表示され、長時間実行されるタスクで出来事の発生時刻を追いやすくなります。

### Improvements（3件）

- **Overview page**: モバイルレイアウト・複数タブ対応・リポジトリ一覧が overview ページで利用できるようになりました
- **Sandbox disk**: サンドボックスのディスクが**128GB に拡大**され、より大きなリポジトリや重い依存関係のインストールでも容量不足になりません
- **Network mode visibility**: 最初のプロンプトを送る前に welcome のネットワーク選択が閉じてしまうことがなくなりました。またセッション中は常に**現在のネットワークモードが表示**され、エージェントがどう接続されているか分かります

### Fixes（7件）

- ストリーミングの停止・固まりが**自動的に復帰**するようになり、応答待ちでセッションがハングしなくなりました
- 並列ツール呼び出しで、1つが他より先に完了したときに**誤った警告**が出なくなりました
- メッセージが大きすぎる場合に、汎用的な失敗ではなく**明確なエラー**として表示されるようになり、入力を短くすべきだと分かります
- サンドボックスに **Node.js と npm が再びプリインストール**され、Node ベースのプロジェクトでエージェントが再インストールせずにビルドできます
- 一部のセッションでシェルコマンドと Git コマンドが実行できなくなるサンドボックスの障害を修正しました
- エンタープライズ利用者に「Kiro Web が自社で有効化されていない」と誤表示される問題を修正しました
- セッション再読み込み時にメッセージの**順序が入れ替わる**問題を修正しました

---

<a id="2026-05-19-session-stability-stop-control-and-mobile-layout-fixes"></a>

## 2026-05-19: Session Stability, Stop Control, and Mobile Layout Fixes

**出典**: <https://kiro.dev/changelog/web/session-stability-stop-control-and-mobile-layout-fixes/>（May 19, 2026）

タスクの途中でエージェントを**停止**できるようになり、ワークスペースの起動中に**進捗が見える**ようになり、小さな画面でのレイアウトが改善されました。このアップデートではセッションの安定性に関するいくつかの問題も解消しています。

### Improvements（5件）

- **Workspace progress indicator**: クローンと起動の進捗ステータスが表示され、環境の準備中に何が起きているか分かります
- **Stop control**: **停止ボタン**でタスク途中のエージェントを止めて、方針を変えられます
- **Mobile responsive layout**: サイドバー・ポップオーバー・チャット入力がモバイル端末で適切に表示されるようになりました
- **Auto-scroll behavior**: チャットのスクロールが**意図ベース**になり、読んでいる位置に留まります。最新の出力を追っているときだけ自動スクロールします
- **Asset load fallback**: 画像などのアセットの読み込みに失敗した場合、壊れた表示ではなく**インラインの代替 UI** が表示されます

### Fixes（6件）

- セッション読み込み時に**最初のエージェントメッセージが消える**問題を修正しました
- セッション読み込み中にワークスペースの復元が中断される問題を修正しました
- 読み込み中のスピナーが画面上で揺れる問題を修正しました
- セッション中に**ステアリングファイルが正しく適用されない**問題を修正しました
- バックエンドにプロバイダが紐づいていないのに GitHub が接続済みと表示される問題を修正しました
- セッションが期限切れの利用者に**不要な再認証**が求められる問題を修正しました

---

<a id="2026-05-07-introducing-kiro-web-preview"></a>

## 2026-05-07: Introducing Kiro Web (Preview)

**出典**: <https://kiro.dev/changelog/web/introducing-kiro-web-preview/>（May 7, 2026）

**Kiro Web（Preview）が <https://app.kiro.dev> で利用可能になりました。** 公式は対象を **Kiro Pro・Pro+・Power の利用者**としています。エージェントとチャットしてアイデアを検討し、バグを直し、変更を形にすることも、タスクを丸ごと任せて**プルリクエストとして完了**させることもできます。**1つのセッションで複数リポジトリにまたがる変更**を調整できます。

> **⚠️ 未確認・公式ページ間の食い違いがあります**: 本エントリと `docs/web/`・`docs/web/setup/` は
> Pro 以上のサブスクリプションが前提と読めますが、
> <https://kiro.dev/docs/privacy-and-security/data-protection/>（Page updated: August 4, 2026）は
> **Free Tier 利用者**のデータ保持期間を記述しています。
> 本サイトはどちらが正しいかを**断定しません**。

### Collaborative and autonomous modes

エージェントとの働き方は2通りです。既定の**協調モード（collaborative mode）**では、利用者が会話を主導します（進め方を相談し、一緒にコードを書き、準備ができたら PR を作らせる）。**Autonomous モード**を有効にすると、エージェントが結果に責任を持ちます。まず明確化のための質問をし、計画を立て、専門のサブエージェントに委任して、**自動的に PR を作成**します。

> 詳細は [01_features/01_agent-modes.md](../01_features/) を参照してください。

### GitHub-native workflow

セッション開始時に作業対象のリポジトリを選びます。エージェントはそれらを**隔離されたサンドボックス**にクローンし、共有ライブラリから依存サービス・クライアントまで、**1回の実行で全リポジトリ**の編集とプルリクエストを調整します。

**`kiro` ラベル**または **`/kiro` コメント**で GitHub issue から作業を割り当てられます。エージェントはフィーチャーブランチを作り、代わりにコミットし、詳細な説明付きでプルリクエストを作成します。PR にコメントでレビューすると、エージェントがそれを受けて更新をプッシュします。**`/kiro all`** でレビュアーの指摘すべてに、**`/kiro fix`** で1つの会話スレッドずつ対応させられます。

> 詳細は [01_features/06_repository-integration.md](../01_features/) を参照してください。

### Steering that carries forward

チームの標準や規約でエージェントを導けます。**`.kiro/steering/`** のステアリングファイルが全セッションの開始時に読み込まれます。公式は「**Kiro IDE と Kiro CLI で使えるものと同じ形式**」と説明しています。PR コメントを通じてエージェントに教えることもでき、そのフィードバックは**すべてのリポジトリの今後の作業に引き継がれます**。

> 詳細は [01_features/04_steering.md](../01_features/) を参照してください。

### Isolated sandbox by default

すべてのタスクが**それぞれ隔離されたサンドボックス**で実行されます。エージェントはリポジトリをクローンし、検出したプロジェクト設定から環境を構成し、タスク完了時にすべてを破棄します。**ネットワークアクセス・環境変数・シークレット・MCP サーバー**はエージェント設定ページから制御します。

> 詳細は [01_features/05_sandbox.md](../01_features/) を参照してください。

---

<a id="2025-12-02-introducing-kiro-autonomous-agent"></a>

## 2025-12-02: Introducing Kiro autonomous agent

**出典**: <https://kiro.dev/changelog/web/introducing-kiro-autonomous-agent/>（December 2, 2025）

> **これは Kiro Web（Preview）の提供開始（2026-05-07）より前のエントリ**で、`changelog/web` 系列の最古のエントリです。

Kiro autonomous agent は、機能の実装からバグ修正まで、**開発タスクを自律的に進めます**。**隔離されたサンドボックス環境で非同期に動作**し、利用者のコードレビューから学習して、コードベースとパターンについての理解を深めていきます。

公式は本エントリで、autonomous agent が**個人開発者向けにプレビュー提供を開始**したこと、対象が **Kiro Pro・Pro+・Power の購読者**であること、**プレビュー期間中は費用がかからず、利用は週次の上限に従う**こと、チームは**ウェイトリスト**から早期アクセスを申し込めることを説明しています。

### 現在の位置づけ（公式の記述）

本エントリのページには、2026-08-01 時点で次の記述があります。

> The autonomous agent preview is now autonomous mode in Kiro. Start at Kiro Web →

つまり公式は「**autonomous agent（プレビュー）は現在の Kiro の autonomous mode であり、入口は Kiro Web**」と明記しています。

> **未確認**: 「統合された」「改称された」といった**経緯・因果は公式に書かれていません**。
> 本サイトが書けるのは、2026-08-01 時点でこの記述があるという事実だけです。

---

## 🔗 関連ページ

- [公式 changelog（Web 系列）](https://kiro.dev/changelog/web/)
- [00_information](../00_information/) — 公式情報源の構造と使い分け
- [01_features](../01_features/) — 機能詳細ガイド
- [04_reference](../04_reference/) — 上限値・許可ドメインなどの一覧

### 姉妹サイト（別製品の更新履歴）

- Kiro IDE: [kiro-ide-docs](https://github.com/kamogashira-sys/kiro-ide-docs)
- Kiro CLI: [q-cli-docs](https://github.com/kamogashira-sys/q-cli-docs)

---

[← 02_update に戻る](README.md)

---

## 追加された公式エントリ（2026-07-13〜2026-09-01）

以下の各節は、G1 で保存・hash 検証した公式 changelog HTML の日付、公式タイトル、URL を収録する。取得時点の抽出器が本文構造を返さないエントリについて、本文の意味を補完・翻訳していない。

<a id="2026-09-01-use-cloud-configuration-in-local-sessions"></a>

## 2026-09-01: Use Cloud Configuration in Local Sessions

**出典**: <https://kiro.dev/changelog/web/use-cloud-configuration-in-local-sessions/>（2026-09-01）

公式 changelog の Web 系列にあるエントリです。公式タイトルは **Use Cloud Configuration in Local Sessions** です。本サイトでは、公式 HTML から確認できた日付・タイトル・URL を収録しています。本文構造を抽出できないため、一次情報にない機能説明を追加していません。

<a id="2026-09-01-kiro-web-is-now-generally-available"></a>

## 2026-09-01: Kiro Web Is Now Generally Available

**出典**: <https://kiro.dev/changelog/web/kiro-web-is-now-generally-available/>（2026-09-01）

公式 changelog の Web 系列にあるエントリです。公式タイトルは **Kiro Web Is Now Generally Available** です。本サイトでは、公式 HTML から確認できた日付・タイトル・URL を収録しています。本文構造を抽出できないため、一次情報にない機能説明を追加していません。

<a id="2026-08-31-pick-a-branch-when-you-pick-a-repository"></a>

## 2026-08-31: Pick a Branch When You Pick a Repository

**出典**: <https://kiro.dev/changelog/web/pick-a-branch-when-you-pick-a-repository/>（2026-08-31）

公式 changelog の Web 系列にあるエントリです。公式タイトルは **Pick a Branch When You Pick a Repository** です。本サイトでは、公式 HTML から確認できた日付・タイトル・URL を収録しています。本文構造を抽出できないため、一次情報にない機能説明を追加していません。

<a id="2026-08-27-sessions-name-themselves"></a>

## 2026-08-27: Sessions Name Themselves

**出典**: <https://kiro.dev/changelog/web/sessions-name-themselves/>（2026-08-27）

公式 changelog の Web 系列にあるエントリです。公式タイトルは **Sessions Name Themselves** です。本サイトでは、公式 HTML から確認できた日付・タイトル・URL を収録しています。本文構造を抽出できないため、一次情報にない機能説明を追加していません。

<a id="2026-08-22-organize-sessions-into-groups"></a>

## 2026-08-22: Organize Sessions into Groups

**出典**: <https://kiro.dev/changelog/web/organize-sessions-into-groups/>（2026-08-22）

公式 changelog の Web 系列にあるエントリです。公式タイトルは **Organize Sessions into Groups** です。本サイトでは、公式 HTML から確認できた日付・タイトル・URL を収録しています。本文構造を抽出できないため、一次情報にない機能説明を追加していません。

<a id="2026-08-19-recent-repositories-in-the-repository-selector"></a>

## 2026-08-19: Recent Repositories in the Repository Selector

**出典**: <https://kiro.dev/changelog/web/recent-repositories-in-the-repository-selector/>（2026-08-19）

公式 changelog の Web 系列にあるエントリです。公式タイトルは **Recent Repositories in the Repository Selector** です。本サイトでは、公式 HTML から確認できた日付・タイトル・URL を収録しています。本文構造を抽出できないため、一次情報にない機能説明を追加していません。

<a id="2026-08-17-kiro-web-access-with-okta-and-microsoft-entra-id"></a>

## 2026-08-17: Access Kiro Web with Okta or Microsoft Entra ID

**出典**: <https://kiro.dev/changelog/web/kiro-web-access-with-okta-and-microsoft-entra-id/>（2026-08-17）

公式 changelog の Web 系列にあるエントリです。公式タイトルは **Access Kiro Web with Okta or Microsoft Entra ID** です。本サイトでは、公式 HTML から確認できた日付・タイトル・URL を収録しています。本文構造を抽出できないため、一次情報にない機能説明を追加していません。

<a id="2026-08-11-cloud-configuration"></a>

## 2026-08-11: Sync your local .kiro configuration to the cloud

**出典**: <https://kiro.dev/changelog/web/cloud-configuration/>（2026-08-11）

公式 changelog の Web 系列にあるエントリです。公式タイトルは **Sync your local .kiro configuration to the cloud** です。本サイトでは、公式 HTML から確認できた日付・タイトル・URL を収録しています。本文構造を抽出できないため、一次情報にない機能説明を追加していません。

<a id="2026-07-23-playwright-and-agent-browser-support"></a>

## 2026-07-23: Playwright and Agent-Browser Support

**出典**: <https://kiro.dev/changelog/web/playwright-and-agent-browser-support/>（2026-07-23）

公式 changelog の Web 系列にあるエントリです。公式タイトルは **Playwright and Agent-Browser Support** です。本サイトでは、公式 HTML から確認できた日付・タイトル・URL を収録しています。本文構造を抽出できないため、一次情報にない機能説明を追加していません。

<a id="2026-07-20-github-pull-request-workflow-inside-kiro-web"></a>

## 2026-07-20: Inspect GitHub Pull Requests Inside Kiro Web

**出典**: <https://kiro.dev/changelog/web/github-pull-request-workflow-inside-kiro-web/>（2026-07-20）

公式 changelog の Web 系列にあるエントリです。公式タイトルは **Inspect GitHub Pull Requests Inside Kiro Web** です。本サイトでは、公式 HTML から確認できた日付・タイトル・URL を収録しています。本文構造を抽出できないため、一次情報にない機能説明を追加していません。

<a id="2026-07-16-gitlab-fine-grained-access-token-support"></a>

## 2026-07-16: GitLab Fine-Grained Access Token Support

**出典**: <https://kiro.dev/changelog/web/gitlab-fine-grained-access-token-support/>（2026-07-16）

公式 changelog の Web 系列にあるエントリです。公式タイトルは **GitLab Fine-Grained Access Token Support** です。本サイトでは、公式 HTML から確認できた日付・タイトル・URL を収録しています。本文構造を抽出できないため、一次情報にない機能説明を追加していません。

<a id="2026-07-13-workspace-file-explorer-for-cloud-sessions"></a>

## 2026-07-13: Workspace File Explorer for Cloud Sessions

**出典**: <https://kiro.dev/changelog/web/workspace-file-explorer-for-cloud-sessions/>（2026-07-13）

公式 changelog の Web 系列にあるエントリです。公式タイトルは **Workspace File Explorer for Cloud Sessions** です。本サイトでは、公式 HTML から確認できた日付・タイトル・URL を収録しています。本文構造を抽出できないため、一次情報にない機能説明を追加していません。
