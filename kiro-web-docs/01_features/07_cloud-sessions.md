# Cloud Sessions（Kiro Web の実行環境そのもの）

> **本ページは Kiro Web 版（<https://app.kiro.dev>）の観点から Cloud Sessions を扱います。**
> Cloud Sessions 自体は Features 区分の**全製品共通ページ**（`docs/cloud-sessions/`）で説明されている機能で、
> Kiro IDE・Kiro CLI・Mobile にも共通します。ただし**Kiro Web のすべてのセッションは Cloud Session です**
> （後述）。そのため本サイトに収録し、Web からの利用に焦点を当てて記述します。

**出典**: <https://kiro.dev/docs/cloud-sessions/>（Page updated: September 2, 2026）

---

## 📑 このページの内容

1. [Cloud Session とは](#cloud-session-とは)
2. [Kiro Web のすべてのセッションは Cloud Session です](#kiro-web-のすべてのセッションは-cloud-session-です)
3. [動作の仕組み](#動作の仕組み)
4. [前提条件](#前提条件)
5. [構成情報の扱い](#構成情報の扱い)
6. [サーフェス間の移動](#サーフェス間の移動)
7. [現時点の制限](#現時点の制限)

---

## Cloud Session とは

公式は次のように説明しています。

> A cloud session runs the Kiro agent harness in a managed cloud sandbox instead of on your machine. The session belongs to your Kiro account, not to any one app: start it in the browser, hand it a long task, close your laptop, and check on it later from your phone, your terminal, or the IDE. The agent keeps working in the sandbox whether or not you're connected.

**Cloud Session は、Kiro のエージェント基盤をローカルマシンではなく管理されたクラウドサンドボックスで実行する**仕組みです。セッションは**特定のアプリに属さず、Kiro アカウントに属します**。ブラウザで開始し、長時間のタスクを任せてノートPCを閉じても、後でスマートフォン・ターミナル・IDE から確認できます。**接続の有無に関わらず、エージェントはサンドボックス内で作業を継続します。**

### 対応状況（Capability 表・公式）

| 機能 | IDE | CLI | Web | Mobile |
|------|:---:|:---:|:---:|:------:|
| Cloud Session の作成 | ✓ | ✓ | ✓ | ✓ |
| 既存 Cloud Session の再開・操縦 | ✓ | ✓ | ✓ | ✓ |
| Autonomous モード | ✓ | ✓ | ✓ | ✓ |
| スケジュール実行（Automations） | — | — | ✓ | — |

> **Kiro Web は4項目すべてに対応しています。** Automations（[03_automations.md](03_automations.md)）は
> **Web 固有の機能**であることが、この表から確認できます。

### Preview の前提バージョン

公式は次のように明記しています。

> Creating and attaching from the IDE requires **Kiro IDE v1.0.293 or later**, and from the CLI requires **Kiro CLI v2.17 or later**.

| インターフェース | 必要バージョン |
|--------------|--------------|
| Kiro IDE | **v1.0.293 以降** |
| Kiro CLI | **v2.17 以降** |
| Kiro Web | バージョン番号なし（[README.md](../README.md#-kiro-web-にはバージョン番号がありません)） |

---

## Kiro Web のすべてのセッションは Cloud Session です

公式は次のように明記しています。

> Every Kiro Web session is a cloud session; the browser is the native surface for this feature. After your administrator enables **Cloud Sessions** and, if your organization uses an external IdP, configures the IdP for Kiro Web, you do not need to complete any per-user setup beyond signing in.

**Kiro Web の全セッションが Cloud Session です。** ブラウザは Cloud Sessions の**ネイティブなサーフェス**です。

| 前提 | 内容 |
|------|------|
| **管理者が Cloud Sessions を有効にする** | 必須（[02_identity-center.md](../03_deployment/02_identity-center.md#組織で-cloud-sessions-を有効にする)） |
| **外部 IdP を使う組織** | **Kiro Web 向けに IdP を構成する**必要がある |
| **利用者ごとの作業** | 上記が済んでいれば、**サインイン以外に必要な設定はありません** |

> ⚠️ **2026-09-02 更新で前提が明記されました。** 移転前は
> 「the browser is the native surface for this feature, **with no setup beyond signing in**」
> （サインイン以外の設定は不要）とだけ書かれていましたが、現行は
> **管理者による有効化と外部 IdP の構成が前提**であることが加わっています（2026-09-13 実測）。

> つまり、**本サイトの [01_agent-modes.md](01_agent-modes.md) 等で説明している「セッション」は、
> すべてこのページで説明する Cloud Session の Web からの利用形態です。** 用語上は区別していますが、
> 実体は同じ仕組みです。

### Web からの開始手順（公式）

1. <https://app.kiro.dev> にサインインする
2. 接続済みの [GitHub](06_repository-integration.md) または [GitLab](06_repository-integration.md) アカウントから作業対象のリポジトリを選ぶ
3. エージェントとチャットして探索・実装・反復する。準備ができたらプルリクエストの作成を依頼するか、[Autonomous モード](01_agent-modes.md#autonomous-モード)を有効にして計画・実装・PR作成を任せる

### セッションはブラウザタブ・デバイスを越えて継続します

公式は次のように説明しています。

> Your sessions persist across browser tabs and devices. Close the tab mid-task and the agent keeps working; the session list shows live status when you return.

**タブを閉じてもエージェントは作業を継続**し、戻ったときにセッション一覧で状態を確認できます。定期的な作業には [Automations](03_automations.md) が、開始操作なしに Cloud Session をスケジュール実行します。

[Mobile アプリ](https://kiro.dev/docs/mobile/)も同じセッションに接続でき、スマートフォンから diff の確認や承認応答ができます。

---

## 動作の仕組み

公式は次のように説明しています。

> When you create a cloud session, Kiro provisions an isolated sandbox and starts the same agent harness that runs locally in the IDE and CLI. If you attach repositories, Kiro clones them **server-side** through your connected source provider; your local working copy is never uploaded.

| 段階 | 内容 |
|------|------|
| 1 | **隔離されたサンドボックス**を用意する |
| 2 | IDE・CLI でローカル実行するのと**同じエージェント基盤**を起動する |
| 3 | リポジトリを接続すると、**サーバー側で**接続済みのソースプロバイダ経由でクローンする（**ローカルの作業コピーはアップロードされません**） |
| 4 | エージェントがサンドボックス内でファイルの読み書き・ビルド・シェルコマンドを実行する |
| 5 | 結果をソースプロバイダ経由（通常はプルリクエスト）または会話内で直接返す |

### セッションはクライアントと独立して存在します

公式は次の3点を挙げています。

| # | 特徴 | 内容 |
|---|------|------|
| 1 | **クライアントは着脱可能** | Web・Mobile・IDE・CLI は同一セッションへの**ビュー**。クライアントの切断はエージェントを止めない |
| 2 | **状態はマシンを越えて残る** | 会話履歴・接続リポジトリ・サンドボックスのファイル状態はクラウドに残る。どのサーフェスから再接続しても続きから見える |
| 3 | **承認は接続を待つ** | 誰も接続していない間にエージェントが[権限](https://kiro.dev/docs/permissions/)を必要とする操作をする場合、リクエストは保留され、次に接続したクライアントに提示される |

サンドボックス自体の詳細（ネットワークアクセス・環境変数・環境構成）は [05_sandbox.md](05_sandbox.md) を参照してください。

---

## 前提条件

公式が挙げる前提条件は3点です。

| # | 前提条件 |
|---|---------|
| 1 | **Pro / Pro+ / Pro Max / Power のいずれかのサブスクリプション**。Cloud Session は**既存のクレジットモデル**を使い、**クラウド計算資源に対する別料金はかかりません** |
| 2 | リポジトリで作業する場合、接続済みの [GitHub](06_repository-integration.md) または [GitLab](06_repository-integration.md) アカウント |
| 3 | **AWS Identity Center 組織の場合**: 管理者が Kiro を構成している AWS アカウントの **Settings > Kiro Settings** で **Cloud Sessions** を有効化する必要がある（[03_deployment/02_identity-center.md](../03_deployment/02_identity-center.md)）。Cloud Session が動くのは **US East（N. Virginia）`us-east-1` のみ** |
| 4 | **Okta または Microsoft Entra ID を外部 IdP に使う組織の場合**: 管理者が **Cloud Sessions** を有効化し、**既存の Kiro OIDC アプリケーションに `https://app.kiro.dev/signin/oauth` を追加**する必要がある（[2026-08-17 のエントリ](../02_update/01_changelog.md#2026-08-17-kiro-web-access-with-okta-and-microsoft-entra-id)） |

> ⚠️ **2026-09-02 更新で前提条件が変わりました（2026-09-13 実測）。**
> ① サブスクリプションが「有料（Pro 以上）」から **Pro / Pro+ / Pro Max / Power の列挙**になり、
> **クレジットモデルを使い別料金は無い**ことが明記されました。
> ② リージョンの記述から「**Preview 中は**」という限定が外れました。
> ③ **外部 IdP（Okta / Microsoft Entra ID）を使う組織向けの項目が追加**されました。

---

## 構成情報の扱い

公式は次のように説明しています。

> - **Project configuration travels with the repo:** steering, specs, custom agents, hooks, and MCP servers committed under `.kiro/` in your repository apply in cloud sessions automatically, because the sandbox clones the repository.
> - **Personal configuration can sync through your account:** your local `~/.kiro/` directory stays local and isn't applied to a cloud session. Use **Settings > Configuration Sync** in Kiro Web to upload supported personal configuration. Manage the cloud copy from its feature-specific settings page, including account-backed Powers under **Settings > Powers**.

| 構成の種類 | 扱い |
|-----------|------|
| **プロジェクト構成**（リポジトリの `.kiro/` 配下） | **リポジトリと一緒に移動**。Steering・Specs・カスタムエージェント・Hooks・MCP サーバーはサンドボックスがリポジトリをクローンする際に自動的に適用される |
| **個人構成**（`~/.kiro/`） | **ローカルに留まり、Cloud Session には適用されません**。持ち込むには [Kiro Web の Settings](https://app.kiro.dev/settings/cloud-config) の **Configuration Sync** からアップロードする |
| **アップロード後のクラウド側の管理** | **機能ごとの設定ページ**で行う（アカウント側で持つ **Powers** は **Settings > Powers**） |

> ⚠️ **2026-09-02 更新で表現が変わりました。** 移転前は
> 「Personal configuration stays local: your `~/.kiro/` directory isn't applied automatically.」でしたが、
> 現行は「**Personal configuration can sync through your account**」（アカウント経由で同期できる）が見出しになり、
> 設定画面の名称も **Cloud configuration** から **Configuration Sync** に変わっています（2026-09-13 実測）。

公式はセッション内で何が起きるかを表にまとめており、個人構成の行は次のとおりです。

| 項目 | ローカルマシン | クラウドサンドボックス |
|------|------------|----------------|
| **Local personal configuration（`~/.kiro/`）** | **Stays local** | **Not applied; use personal Cloud configuration for supported account-backed items** |

> 本サイトの [04_steering.md](04_steering.md) は**リポジトリの `.kiro/steering/`** を前提に説明しています。これは「プロジェクト構成」に該当するため、Cloud Session でも自動的に適用されます。

サンドボックスの環境（インターネットアクセス・環境変数・セットアップコマンド）は [05_sandbox.md](05_sandbox.md) を参照してください。

---

## サーフェス間の移動

公式は同一の Cloud Session を別のサーフェスから開く方法を示しています。

| 元 | 先 | 方法 |
|----|----|------|
| Web または Mobile | CLI（**別製品**） | `kiro-cli --resume-id <session-id>` |
| IDE（Agent Focus Mode） | Web | セッションのメニューから **Open in Kiro Web** |
| IDE（Agent Focus Mode） | CLI | セッションのメニューから **Open with Kiro CLI** |
| CLI | Web | `app.kiro.dev` でセッションを開く |
| いずれか | Mobile | Mobile アプリのセッション一覧に表示される |

> IDE の Agent Focus Mode は姉妹サイト [kiro-ide-docs](https://github.com/kamogashira-sys/kiro-ide-docs) の対象範囲です。
> CLI の `--cloud` フラグは姉妹サイト [q-cli-docs](https://github.com/kamogashira-sys/q-cli-docs) の対象範囲です。
> 本サイトでは Kiro Web からの利用にのみ焦点を当てています。

---

## 現時点の制限

**出典**: <https://kiro.dev/docs/cloud-sessions/>（Page updated: September 2, 2026）

公式が「**Current limitations**」として明記している制限は5点です。

| # | 制限 | 内容 |
|---|------|------|
| 1 | **並列実行数の上限** | **クラウドセッションは同時に 10 本まで**実行できる |
| 2 | **リポジトリ構成は固定** | セッション作成時に選んだリポジトリで固定される（**CLI は `/repo` で後から追加可能**）。別のリポジトリで作業するには新しいセッションを開始する |
| 3 | **Supervised モード非対応** | Cloud Session は **Autopilot または Autonomous** のみ。**変更ごとの承認は利用できない** |
| 4 | **リネーム不可** | **IDE・CLI から** Cloud Session の名前を変更できない |
| 5 | **サーフェスごとの機能差** | 各サーフェスで一部のコマンド・機能が未対応。**この差はサーフェスとリリースによって異なる** |

> ⚠️ **節の名前と内容が変わりました（2026-09-13 実測）。**
> 移転前は「Preview 中の制限」という位置づけで、**ブランチ選択ができない**という項目と
> 「Preview の成熟に伴い縮小予定」という説明がありましたが、現行は
> **「Current limitations（現時点の制限）」**になり、**ブランチ選択の項目は無くなり**、
> 代わりに**並列実行数の上限（10 本）**が加わっています。
>
> **ブランチ選択については [2026-08-31 のエントリ「Pick a Branch When You Pick a Repository」](../02_update/01_changelog.md#2026-08-31-pick-a-branch-when-you-pick-a-repository)が公開されています。**
> ただしこのエントリは**タイトルと日付以外の本文を抽出できない型**（W-L2）のため、
> **具体的な操作方法は公式から確認できていません**。

> **上限「10」は[並列タスクの上限](../04_reference/04_limits.md#並列実行は-10-件までです)とは別の指標です**
> （あちらは1セッション群で同時実行できる**タスク**の数、こちらは同時に持てる**クラウドセッション**の数）。
> **偶然どちらも 10 です。**

---

## 🔗 関連ページ

- [01_agent-modes.md](01_agent-modes.md) — 2つのモード（Cloud Session 上での操縦方法）
- [03_automations.md](03_automations.md) — Automations（Cloud Session のスケジュール実行・Web 固有）
- [05_sandbox.md](05_sandbox.md) — サンドボックス（Cloud Session の実行環境の詳細）
- [06_repository-integration.md](06_repository-integration.md) — GitHub / GitLab 連携
- [03_deployment/02_identity-center.md](../03_deployment/02_identity-center.md) — AWS Identity Center 組織での有効化手順
- 公式: <https://kiro.dev/docs/cloud-sessions/>

---

[← 01_features に戻る](README.md)
