# Kiro Web 更新履歴（全21エントリ）

> **本ページは Kiro Web 版（<https://app.kiro.dev>）の更新履歴です。**
> Kiro IDE / Kiro CLI の更新は別製品のものです（姉妹サイトを参照してください）。
> **Kiro Web は [2026-09-01 に一般提供（GA）になりました](https://kiro.dev/changelog/web/kiro-web-is-now-generally-available/)。**

**出典**: [公式 changelog（Web 系列）](https://kiro.dev/changelog/web/)
**収録範囲**: 公式 changelog の `web` 系列**全21エントリ**（2025-12-02 〜 2026-09-30）
**情報の基準日**: 2026-10-04（公式 snapshot の取得日。出典日は各公式エントリの公開日）

---

## 📑 このページの読み方

### Kiro Web にはバージョン番号がありません

Kiro IDE の `1.0.242` のような版番号が Kiro Web には**存在しません**。公式 changelog のエントリは**日付とタイトル**だけで識別されます。本ページでは各エントリを **`YYYY-MM-DD` ＋ 公式タイトル**の形で見出しにしています。

> 版番号が存在しない**理由**は公式に説明がないため**未確認**です。

### 折りたたまれている項目も全部載せています

公式サイトでは一部のエントリの `Improvements` / `Fixes` が**初期状態で折りたたまれて**います。本ページは**折りたたみの中身も省略せず全量**を掲載しています（該当3エントリ・計41項目）。

### 各エントリの構造は2種類あります

| 種類 | 構造 | 件数 |
|------|------|------|
| **機能紹介型** | 導入文（＋機能ごとの節） | 18 |
| **保守型** | 導入文（＋節）＋ `Improvements` / `Fixes` の一覧 | 3 |

### 本文は公式の記述の翻訳です

各エントリの本文は、公式エントリの記述を日本語にしたものです。**公式に書かれていない説明は加えていません。**
公式エントリ内の「Learn more」の参照先は、本サイトの対応ページへのリンクに置き換えています。

---

## 📅 エントリ一覧（新しい順）

| 日付 | エントリ | 種類 | 主な内容 |
|------|---------|------|---------|
| 2026-09-30 | [Introducing Workflows in Kiro Web](#2026-09-30-introducing-workflows-in-kiro-web) | 機能紹介型 | Workflows（バックグラウンドで動く多段の計画）・オプトイン |
| 2026-09-22 | [Reasoning Effort and a Grouped Timeline](#2026-09-22-reasoning-effort-and-a-grouped-timeline) | **保守型**（20項目） | 推論の effort の選択・タイムラインの折りたたみ・添付上限・タブの再接続 |
| 2026-09-01 | [Use Cloud Configuration in Local Sessions](#2026-09-01-use-cloud-configuration-in-local-sessions) | 機能紹介型 | クラウドの設定をローカルの IDE / CLI セッションに適用 |
| 2026-09-01 | [Kiro Web Is Now Generally Available](#2026-09-01-kiro-web-is-now-generally-available) | 機能紹介型 | **Kiro Web の一般提供（GA）** |
| 2026-08-31 | [Pick a Branch When You Pick a Repository](#2026-08-31-pick-a-branch-when-you-pick-a-repository) | 機能紹介型 | リポジトリ選択時に作業元のブランチを選ぶ |
| 2026-08-27 | [Sessions Name Themselves](#2026-08-27-sessions-name-themselves) | 機能紹介型 | セッション名の自動生成 |
| 2026-08-22 | [Organize Sessions into Groups](#2026-08-22-organize-sessions-into-groups) | 機能紹介型 | セッションのグループ化 |
| 2026-08-19 | [Recent Repositories in the Repository Selector](#2026-08-19-recent-repositories-in-the-repository-selector) | 機能紹介型 | リポジトリセレクタの Recent セクション |
| 2026-08-17 | [Access Kiro Web with Okta or Microsoft Entra ID](#2026-08-17-kiro-web-access-with-okta-and-microsoft-entra-id) | 機能紹介型 | Okta・Microsoft Entra ID 経由のアクセス |
| 2026-08-11 | [Sync your local .kiro configuration to the cloud](#2026-08-11-cloud-configuration) | 機能紹介型 | 個人の `.kiro` 構成のアップロード（Configuration Sync） |
| 2026-07-23 | [Playwright and Agent-Browser Support](#2026-07-23-playwright-and-agent-browser-support) | 機能紹介型 | サンドボックスでのブラウザ操作 |
| 2026-07-20 | [Inspect GitHub Pull Requests Inside Kiro Web](#2026-07-20-github-pull-request-workflow-inside-kiro-web) | 機能紹介型 | セッション内での PR の確認（Reviews） |
| 2026-07-16 | [GitLab Fine-Grained Access Token Support](#2026-07-16-gitlab-fine-grained-access-token-support) | 機能紹介型 | GitLab の fine-grained access token |
| 2026-07-13 | [Workspace File Explorer for Cloud Sessions](#2026-07-13-workspace-file-explorer-for-cloud-sessions) | 機能紹介型 | ワークスペースのファイル閲覧 |
| 2026-07-01 | [IAM Roles and Authorize Powers for Third-Party Services](#2026-07-01-iam-roles-and-authorize-powers-for-third-party-services) | 機能紹介型 | サンドボックス用 IAM ロール・Powers の認可フロー |
| 2026-06-19 | [Introducing Automations](#2026-06-19-introducing-automations) | 機能紹介型 | 定期実行（Automations） |
| 2026-06-11 | [GitLab Support and Specs in the Browser](#2026-06-11-gitlab-support-and-specs-in-the-browser) | 機能紹介型 | GitLab 対応・ブラウザでの Specs |
| 2026-06-02 | [Start Without a Repo, Switch Modes Anytime](#2026-06-02-start-without-a-repo-switch-modes-anytime) | **保守型**（10項目） | リポジトリ未接続での開始・セッション中のモード切替 |
| 2026-05-19 | [Session Stability, Stop Control, and Mobile Layout Fixes](#2026-05-19-session-stability-stop-control-and-mobile-layout-fixes) | **保守型**（11項目） | 停止ボタン・モバイルレイアウト・セッション安定性 |
| 2026-05-07 | [Introducing Kiro Web (Preview)](#2026-05-07-introducing-kiro-web-preview) | 機能紹介型 | **Kiro Web の提供開始（Preview）** |
| 2025-12-02 | [Introducing Kiro autonomous agent](#2025-12-02-introducing-kiro-autonomous-agent) | 機能紹介型 | autonomous agent のプレビュー提供開始 |

---

<a id="2026-09-30-introducing-workflows-in-kiro-web"></a>

## 2026-09-30: Introducing Workflows in Kiro Web

**出典**: <https://kiro.dev/changelog/web/introducing-workflows/>（September 30, 2026）

公式はこのエントリを「Run reusable, multi-step agent plans in Kiro Web cloud sessions, inspect and guide every step, and keep working in the parent conversation.」と要約しています。

**Workflows が Kiro Web のクラウドセッションで、オプトインの機能として利用できるようになりました。** 再利用できる多段のエージェントの計画をバックグラウンドで実行し、その間も親の会話で作業を続けられます。

### Start a Workflow from the conversation

望む成果と、どの程度の構造やレビューが欲しいかを伝えると、**Kiro が Workflow を提案**し、ステップ・エージェント・effort に名前を付けて**バックグラウンドで起動**します。コードベースのリスクの調査、独立したレビュアーを付けた機能の実装、失敗しているビルドを通すことなどを Kiro に頼めます。**各ステップはそれぞれ独自のエージェントセッションで動き**、Workflows パネルから開けます。各ステップが見るのは**それより前のステップが渡したものだけ**で、ステップが入力を必要とすると**実行が一時停止**します。

同梱された3つのレシピから始められます。

| レシピ | 用途 |
|-------|------|
| `investigate` | 読み取り専用の調査 |
| `feature-pipeline` | 段階を踏んだ機能の実装 |
| `publish-pr` | プルリクエストの作成とレビューフィードバックへの対応 |

### Follow and guide each step

Workflow の実行中は、親の会話のサイドパネルから **Workflows** を開き、実行を選んで入れ子のステップを確認します。ステップを選ぶと、**状態・経過時間・エージェント・モデル・effort・ツールのアクティビティ**が表示されます。ステップが一時停止したら **Answer this step**、実行中は **Steer the agent**、それ以外の指示は **Message this step's agent** を使えます。実行は**一時停止・再開・停止**でき、失敗した後は**失敗したステップを再試行**できます。**Summary**・**Files**・**Artifacts** も同じサイドパネルにあり、成果と証拠をセッションの中に残せます。

### Turn it on and bring your recipes

**Settings > Workflows** を開き、**Enable workflows** をオンにします。レシピを1つアップロードするには **Upload workflow**（`.workflow.json`・`.workflow.yaml`・`.workflow.yml`）を、`.kiro/workflows/` フォルダをまるごと取り込むには **Configuration Sync** を使います。**Workflows をオフにすると、その画面要素が隠れ、新しい起動ができなくなります。**

> Kiro Web の docs に書かれている Workflows の説明は [01_features/01_agent-modes.md](../01_features/01_agent-modes.md#workflowsバックグラウンドで動く多段の計画)、
> レシピのアップロードは [01_features/09_configuration-sync.md](../01_features/09_configuration-sync.md#アップロードできる7つのフォルダ) を参照してください。
> 公式エントリの「Learn more」は全製品共通ページ <https://kiro.dev/docs/workflows/>・<https://kiro.dev/docs/workflows/manage/> を指しています。

---

<a id="2026-09-22-reasoning-effort-and-a-grouped-timeline"></a>

## 2026-09-22: Reasoning Effort and a Grouped Timeline

**出典**: <https://kiro.dev/changelog/web/reasoning-effort-and-a-grouped-timeline/>（September 22, 2026）

Kiro Web で、**対応するモデルの推論の effort を選べる**ようになり、推論とツールのアクティビティが**折りたたみ式のタイムライン**にまとまって、エージェントの応答が見えたままになりました。長いセッションでもドキュメントの添付が安定し、バックグラウンドのタブに戻るとセッションが再接続され、Reviews と What's new が見つけやすくなりました。

### Choose the Reasoning Effort for a Model

推論のレベルを持つモデルでは、ちょっとした編集には低い effort を、慎重さが必要な作業には高い effort を選べます。セレクタは**モデルが対応している場合だけ**表示され、レベルの読み込み中も位置を保ち、キーボード操作に対応しています。

> 公式エントリの「Learn more」は全製品共通ページ <https://kiro.dev/docs/models/effort/> を指しています（本サイトの収録範囲外）。

### A Timeline That Stays Out of the Way

**連続する推論ステップとツール呼び出しが1つの折りたたみブロックにまとまり**、エージェントの応答が見えたままになります。詳細は展開して確認します。起動時の処理は1つの **Session setup** 行にまとまります。Steering・Configuration Sync・タスクリストの結果はより読みやすい形で表示されます。

> 詳細は [01_features/01_agent-modes.md](../01_features/01_agent-modes.md#会話のタイムラインの読み方) を参照してください。

### Attach Documents Across a Long Session

長いセッションの途中で**6件目のドキュメント**をアップロードしても、新しい添付がブロックされなくなりました。**5件までという上限はセッション全体で累積せず、メッセージごとに適用される**ため、以前のアップロードが後のメッセージをブロックしなくなります。影響を受けたセッションは、リセットや再起動なしに**次のメッセージで回復**します。

> 上限値は [04_reference/04_limits.md](../04_reference/04_limits.md#チャットの添付ドキュメント数) を参照してください。

### Sessions Reconnect When You Return to the Tab

バックグラウンドに置いた Kiro Web のタブは、**戻ると再接続し、離れている間に届いたセッションのアクティビティを再生**します。スリープやネットワークの変化の後でも、メッセージを送り直さずに最新のセッションの状態に戻ります。

> 詳細は [01_features/01_agent-modes.md](../01_features/01_agent-modes.md#バックグラウンドのタブと再接続) を参照してください。

### Improvements（8件）

- **What's new feed**: アカウントメニューの上に **What's new** の項目が加わり、Kiro Web の最近のお知らせがまとまります。**既読になるのは1件を開いたときだけ**です
- **Reviews in Summary**: Reviews が **Summary の中の1節**になり、Files・Artifacts と並びます。独自の一覧と詳細表示を持ちます
- **Sub-hourly schedule validation**: **1時間より頻繁なカスタムスケジュール**は入力中に指摘され、式を直すまで **Submit が無効**になります
- **Session groups from the composer**: セッションを開始するプロンプトを書きながら、**グループを選ぶか作れます**
- **Skill load status**: 読み込みに失敗した skill は**失敗と表示**されます
- **Sandbox time used**: 利用できる場合、sessions ページのセッションカードの下に、**その月に使ったサンドボックス時間の合計**が表示されます
- **Faster turn completion**: ターンの完了時に、セッション一覧全体を再読み込みせず、**現在のセッションだけを更新**するようになりました
- **Configuration Sync guidance**: Sync ページに**対応する各フォルダが一覧表示**されます

### Fixes（12件）

- ツール呼び出しの前に、プレースホルダの点が**空のメッセージの吹き出し**として表示される問題を修正しました
- 遅れて届いた推論ステップが、自分のブロックではなく**誤った折りたたみブロックにまとめられる**問題を修正しました
- ストリームのエラー後にツール呼び出しが**実行中のまま残り**、エージェントが固まったように見える問題を修正しました
- 長いセッションタイトルが**サイドバーで切れる**問題を修正しました
- Summary の開き方・切り替え方が、他のサイドパネルのタブと一貫していなかった問題を修正しました
- レビューの詳細がプルリクエストを解決できなかったときに、**生のエラーメッセージ**が表示される問題を修正しました
- 拒否されたスケジュールで、拒否の具体的な理由ではなく**汎用のエラー**が表示される問題を修正しました
- **アクティブなセッション数の上限**に達した状態でセッションを開くと、上限に達したことと再試行できることを説明するメッセージではなく、**サーバーエラー**が表示される問題を修正しました
- 重複した steering ファイルのアップロードが成功と報告される一方で、**カスタムの指示が新しいセッションに届かなくなっていた**問題を修正しました。重複したアップロードは**説明付きで拒否**されるようになりました
- リポジトリに紐づいた steering ドキュメントをソースを変えずに編集すると、**黙ってインラインのコピーに変換され**、リポジトリでの編集が反映されなくなる問題を修正しました
- 更新・削除のエラーで、steering ファイルの作成時用の「新しいファイルを追加する前に既存のファイルを削除する」という案内が表示される問題を修正しました
- 削除済みの steering ファイルを削除すると**エラーが報告される**問題を修正しました。成功として扱われるため、中断された削除の再試行が失敗のように見えなくなりました

---

<a id="2026-09-01-use-cloud-configuration-in-local-sessions"></a>

## 2026-09-01: Use Cloud Configuration in Local Sessions

**出典**: <https://kiro.dev/changelog/web/use-cloud-configuration-in-local-sessions/>（September 1, 2026）

Configuration Sync で、**クラウドの設定を新しいローカルの Kiro IDE・Kiro CLI のセッション**（いずれも別製品）に持ち込めるようになりました。Configuration Sync のページで **Apply your cloud configuration to local sessions** を有効にすると、セッションの開始時にクラウドの **Steering ファイル・カスタムエージェント・Skills・Powers・Hooks** が読み込まれます。**クラウドの内容はクラウドに留まり、ローカルの `.kiro` ディレクトリのファイルを置き換えません。**

> 詳細は [01_features/09_configuration-sync.md](../01_features/09_configuration-sync.md#ローカルセッションにも適用する) を参照してください。

---

<a id="2026-09-01-kiro-web-is-now-generally-available"></a>

## 2026-09-01: Kiro Web Is Now Generally Available

**出典**: <https://kiro.dev/changelog/web/kiro-web-is-now-generally-available/>（September 1, 2026）

**Kiro Web が一般提供（GA）になりました。** 公式は「Build, delegate, and steer development work with Kiro Web from your browser.」として、ブラウザから Kiro Web で開発作業を組み立て、任せ、方向づけできると説明しています。協調的にアイデアを検討することも、**Specs** で作業を形にすることも、タスクを**最初から最後まで任せる**こともできます。

> 3つの働き方は [01_features/01_agent-modes.md](../01_features/01_agent-modes.md)・[01_features/02_specs.md](../01_features/02_specs.md) を参照してください。

---

<a id="2026-08-31-pick-a-branch-when-you-pick-a-repository"></a>

## 2026-08-31: Pick a Branch When You Pick a Repository

**出典**: <https://kiro.dev/changelog/web/pick-a-branch-when-you-pick-a-repository/>（August 31, 2026）

**既定のブランチから始める必要がなくなりました。** セッション用に GitHub または GitLab のリポジトリを選ぶとき、**セレクタの中で作業元のブランチを選べます**。エージェントはそのブランチをクローンし、その上で作業します。

---

<a id="2026-08-27-sessions-name-themselves"></a>

## 2026-08-27: Sessions Name Themselves

**出典**: <https://kiro.dev/changelog/web/sessions-name-themselves/>（August 27, 2026）

新しいセッションには、汎用の既定名の代わりに、**作業内容に基づいてエージェントが生成した説明的なタイトル**が付くようになりました。タイトルは準備ができ次第、**セッションヘッダーとサイドバー**に表示されます。**自分でセッション名を変えるとその名前が保持され**、エージェントが利用者の付けたタイトルを上書きすることはありません。

> 詳細は [01_features/01_agent-modes.md](../01_features/01_agent-modes.md#セッション名は自動で付きます) を参照してください。

---

<a id="2026-08-22-organize-sessions-into-groups"></a>

## 2026-08-22: Organize Sessions into Groups

**出典**: <https://kiro.dev/changelog/web/organize-sessions-into-groups/>（August 22, 2026）

関連するセッションを**グループにまとめて**、増えていくセッション一覧を管理しやすくできます。サイドバーまたは sessions ページでグループを作り、セッションを出し入れし、いつでもグループの**名前を変えたり解散したり**できます。

> 詳細は [01_features/01_agent-modes.md](../01_features/01_agent-modes.md#セッションをグループにまとめる) を参照してください。

---

<a id="2026-08-19-recent-repositories-in-the-repository-selector"></a>

## 2026-08-19: Recent Repositories in the Repository Selector

**出典**: <https://kiro.dev/changelog/web/recent-repositories-in-the-repository-selector/>（August 19, 2026）

いくつかのリポジトリを使うと、リポジトリセレクタの上部に **Recent** セクションが表示されるようになりました。直前まで作業していたリポジトリに、一覧全体をスクロールせず**1クリックで戻れます**。最近のリポジトリは**プロバイダごとにまとめられ**、**検索中は表示から外れます**。

> 表示の条件は [03_deployment/01_setup.md](../03_deployment/01_setup.md#最近使ったリポジトリrecent) を参照してください。

---

<a id="2026-08-17-kiro-web-access-with-okta-and-microsoft-entra-id"></a>

## 2026-08-17: Access Kiro Web with Okta or Microsoft Entra ID

**出典**: <https://kiro.dev/changelog/web/kiro-web-access-with-okta-and-microsoft-entra-id/>（August 17, 2026）

チームが既に使っている **Okta** または **Microsoft Entra ID** の連携を通じて Kiro Web にアクセスできるようになりました。管理者がアクセスを構成した後、**利用者はサインインするだけ**です。公式は「This capability is available with **Kiro Pro and above** subscriptions.」としています。

### Configure Kiro Web access

既存の Kiro OpenID Connect（OIDC）アプリケーションに **`https://app.kiro.dev/signin/oauth`** を追加します。

| IdP | 追加する場所 |
|-----|-----------|
| **Okta** | **Sign-in redirect URI** をもう1つ追加する |
| **Microsoft Entra ID** | **Single-page application** の下に追加する（**Mobile and desktop application** のリダイレクトとは別） |

その後、**Cloud Sessions (Preview)** を有効にします。**Cloud Sessions と API キーの生成は、それぞれ個別に有効にできます。**

> 「Cloud Sessions (Preview)」は本エントリの表記です。現行の `docs/web/identity-center/` ではトグル名は **Cloud Sessions** です
> （[03_deployment/02_identity-center.md](../03_deployment/02_identity-center.md#組織で-cloud-sessions-を有効にする)）。
> 外部 IdP を使う場合の前提条件は [01_features/07_cloud-sessions.md](../01_features/07_cloud-sessions.md#前提条件) を参照してください。

---

<a id="2026-08-11-cloud-configuration"></a>

## 2026-08-11: Sync your local .kiro configuration to the cloud

**出典**: <https://kiro.dev/changelog/web/cloud-configuration/>（August 11, 2026）

**個人の `.kiro` 構成を Kiro Web に持ち込めるようになりました。** **Settings > Configuration Sync** から、ローカルの Steering・カスタムエージェント・Hooks・Skills・Powers・MCP の設定をアップロードし、**すべてのクラウドセッション**で使えます。

### Review before uploading

ローカルの `.kiro` ディレクトリから、`skills/` や `agents/` などの**対応する最上位フォルダを1つ**選ぶかドラッグします。Kiro はアップロードの前に**各ファイルをクラウド側のコピーと照合**します。新しいファイルは既定で選択され、**クラウドの内容を置き換える更新には利用者の入力が必要**です。Steering ファイルと MCP サーバーには**左右に並べた比較**が表示されます。

### Manage configuration from settings

アップロードした項目は対応する設定ページに現れ、それぞれ**表示・編集・ダウンロード・削除**ができます。Steering・Skills・Agents・Hooks・Powers は Settings の下にそれぞれのページがあり、アップロードした MCP サーバーは MCP サーバーの設定に表示されます。**カタログの Powers は名前でインストール**され、**カスタムの Powers はテキストファイルとしてアップロード**されます。

> 「Settings > Configuration Sync」は本エントリの表記です。現行の `docs/web/cloud-configuration/` は **Settings > Sync** と書いています。
> 詳細は [01_features/09_configuration-sync.md](../01_features/09_configuration-sync.md) を参照してください。

---

<a id="2026-07-23-playwright-and-agent-browser-support"></a>

## 2026-07-23: Playwright and Agent-Browser Support

**出典**: <https://kiro.dev/changelog/web/playwright-and-agent-browser-support/>（July 23, 2026）

エージェントの作業は、コードを書くところで終わりではなくなりました。サンドボックスで **Playwright** と **agent-browser CLI** が使えるので、作ったばかりのアプリを**実際のブラウザで開き**、フローをクリックして確かめ、**ブラウザで起きるバグを再現**し、利用者が見る前に **UI の変更を検証**できます。修正を頼めば、ブラウザで確認済みの修正が返ってきます。

> 詳細は [01_features/05_sandbox.md](../01_features/05_sandbox.md#ブラウザ操作headless-chrome-同梱) を参照してください。

---

<a id="2026-07-20-github-pull-request-workflow-inside-kiro-web"></a>

## 2026-07-20: Inspect GitHub Pull Requests Inside Kiro Web

**出典**: <https://kiro.dev/changelog/web/github-pull-request-workflow-inside-kiro-web/>（July 20, 2026）

エージェントがプルリクエストを開くと、**すぐにセッションに表示されます**。**Reviews パネル**が自動で現れ、そのセッションのプルリクエストをすべて一覧表示します。GitHub のプルリクエストを選ぶと、**状態・コミット・変更ファイル**を **unified** または **split** の差分で、会話を離れずに確認できます。レビューやマージの準備ができたら、**1クリックで GitHub で開けます**。

> 本エントリの「Reviews パネル」は公開時点の説明です。現行の `docs/web/github/`（2026-10-01 版）では、Reviews は **Summary の中**にあります
> （[2026-09-22 のエントリ](#2026-09-22-reasoning-effort-and-a-grouped-timeline)・[01_features/06_repository-integration.md](../01_features/06_repository-integration.md#セッション内で-pr-を確認するsummary-の-reviews)）。

---

<a id="2026-07-16-gitlab-fine-grained-access-token-support"></a>

## 2026-07-16: GitLab Fine-Grained Access Token Support

**出典**: <https://kiro.dev/changelog/web/gitlab-fine-grained-access-token-support/>（July 16, 2026）

GitLab に **fine-grained access token** で接続できるようになりました。fine-grained token は**スコープではなく細かな権限**を使い、トークンを**特定のリソースとリポジトリに限定**します。

> 詳細は [01_features/06_repository-integration.md](../01_features/06_repository-integration.md) を参照してください。

---

<a id="2026-07-13-workspace-file-explorer-for-cloud-sessions"></a>

## 2026-07-13: Workspace File Explorer for Cloud Sessions

**出典**: <https://kiro.dev/changelog/web/workspace-file-explorer-for-cloud-sessions/>（July 13, 2026）

エージェントがクラウドサンドボックスで何かを作ったら、**中を見て回れる**ようになりました。セッションのワークスペースを Kiro Web 上で閲覧し、エージェントが作成・編集したファイルを**シンタックスハイライト付きのビューア**で開き、**Markdown と画像をプレビュー**し、必要なものを**ダウンロード**できます。エージェントの応答中の**ファイルパスはリンク**になっており、「予測ページを更新しました」のような応答から実際のファイルへ1クリックで移動できます。

> 詳細は [01_features/10_file-explorer.md](../01_features/10_file-explorer.md) を参照してください。

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
> <https://kiro.dev/docs/privacy-and-security/data-protection/>（Page updated: September 30, 2026）は
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

本エントリのページには、2026-08-01 時点から次の記述があります（2026-10-04 時点でも同じです）。

> The autonomous agent preview is now autonomous mode in Kiro. Start at Kiro Web →

つまり公式は「**autonomous agent（プレビュー）は現在の Kiro の autonomous mode であり、入口は Kiro Web**」と明記しています。

> **未確認**: 「統合された」「改称された」といった**経緯・因果は公式に書かれていません**。
> 本サイトが書けるのは、この記述があるという事実だけです。

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
