# AWS Identity Center（要件と制限）

> **本ページは Kiro Web 版（<https://app.kiro.dev>）の仕様です。**
> Kiro IDE / Kiro CLI とは別製品です。**Kiro Web は [2026-09-01 に一般提供（GA）になりました](https://kiro.dev/changelog/web/kiro-web-is-now-generally-available/)。**

**出典**: <https://kiro.dev/docs/web/identity-center/>（Page updated: October 21, 2026）

組織で AWS Identity Center を使っている場合、**利用者が Kiro Web のセッションを開始する前に、管理者が Cloud Sessions を有効にする必要があります**。また、**管理者が設定した共有設定の一部が Kiro Web には適用されません**。

---

## 📑 このページの内容

1. [組織で Cloud Sessions を有効にする](#組織で-cloud-sessions-を有効にする)
2. [要件](#要件)
3. [Kiro Sign-In アプリケーション](#kiro-sign-in-アプリケーション)
4. [制限 — 適用されない共有設定](#制限--適用されない共有設定)
5. [利用開始の手順](#利用開始の手順)
6. [トラブルシューティング](#トラブルシューティング)

---

## 組織で Cloud Sessions を有効にする

公式は「Administrators must enable Cloud Sessions before users in the organization can start Kiro Web sessions」として、**利用者がアクセスする前に管理者が有効化する必要がある**と説明しています。

手順は3ステップです。

1. **Kiro プロファイルを所有する AWS アカウント**に移動する
2. **Settings > Kiro Settings** に移動する
3. **Cloud Sessions** をオンにする

> 公式ページの 2026-10-01 版は手順 1 を「**Kiro を構成している AWS アカウント**（the AWS account where Kiro is configured）」と書いていました。
> 2026-10-21 版で「**Kiro プロファイルを所有する AWS アカウント**（the AWS account that owns the Kiro profile）」に変わっています。

### トグルの名前は2回変わっています

| 時点 | トグルの名前 |
|------|-----------|
| 2026-08-14 以前 | **Autonomous agents** |
| 2026-08-14 時点 | **Cloud Sessions (Preview)** |
| **2026-09-02 時点（現行）** | **Cloud Sessions** |

現行の公式は次のように説明しています。

> **Cloud Sessions** was previously labeled **Kiro Web (Preview)**. Organizations that already enabled the previous setting stay enabled. For organizations setting up Kiro for the first time, an administrator must opt in before users can start Kiro Web sessions.

**既に以前の設定を有効化していた組織は有効のまま維持されます。** 新規に設定する組織は、
利用者がセッションを開始する前に管理者がオプトインする必要があります。

> **このトグルは Kiro Web だけでなく、Agent Focus Mode のクラウドセッションと
> Kiro CLI（別製品）の `kiro-cli --cloud` も対象範囲に含みます**（[Cloud Sessions](../01_features/07_cloud-sessions.md)）。

---

## 要件

公式が挙げている要件は4点です（2026-10-21 版）。

| # | 要件 | 補足 |
|---|------|------|
| 1 | **Kiro Profile が必要** | **Q Developer Profile では動作しません** |
| 2 | **利用者が選びうる各 Kiro プロファイルを所有する AWS アカウントで、Cloud Sessions を有効にする** | **Settings > Kiro Settings** から（[上記](#組織で-cloud-sessions-を有効にする)）。2026-10-01 版は「管理者が、Kiro を構成している AWS アカウントで有効にする」でした |
| 3 | **リージョン** | **US East（N. Virginia）`us-east-1` のみ**（2026-09-02 更新で「Preview 中は」という限定が外れました） |
| 4 | **IAM Identity Center インスタンスの Kiro Sign-In アプリケーションを有効のままにし、割り当てを必須にしない** | [下記](#kiro-sign-in-アプリケーション) |

> ⚠️ **要件の変遷（公式ページの版ごと）。**
>
> | 版 | 要件の数 | 変更点 |
> |----|---------|-------|
> | 2026-10-01 版より前 | 4 点 | 「A GitHub or GitLab repository provider connected to Kiro」（Kiro に接続されたリポジトリプロバイダ）を含む |
> | 2026-10-01 版 | 3 点 | 上記のリポジトリプロバイダの項目が**削除**された（同じ時期に `docs/web/` の前提条件からも削除） |
> | **2026-10-21 版（現行）** | **4 点** | 管理者の有効化の項目が「各 Kiro プロファイルを所有する AWS アカウント」の表現に変わり、**Kiro Sign-In アプリケーションの項目が追加**された |
>
> リポジトリプロバイダの項目は 2026-10-21 版にも**ありません**。一方で同じページの「Getting started」には **「Connect GitHub or GitLab to give the agent access to your repositories」**（GitHub か GitLab を接続してエージェントにリポジトリへのアクセスを与える）が残っており、
> `docs/cloud-sessions/` は前提条件を「A connected GitHub or GitLab account, **if you want to work on repositories**」と書いています。
> 要件から外した理由は公式に書かれていないため**未確認**です。

### ⚠️ Q Developer Profile では動作しません

公式は次のように明記しています。

> Kiro Web requires a Kiro Profile — it does not work with Q Developer Profiles

Amazon Q Developer から移行した環境では、プロファイルの種類を確認してください。

---

## Kiro Sign-In アプリケーション

**2026-10-21 版で新設された節です。** 公式は次のように説明しています。

> When an administrator creates a Kiro profile that uses IAM Identity Center, Kiro automatically creates two AWS managed applications in that IAM Identity Center instance:

**IAM Identity Center を使う Kiro プロファイルを管理者が作成すると、Kiro はその IAM Identity Center インスタンスに AWS マネージドアプリケーションを2つ自動で作成します。**

| アプリケーション | 公式の説明 |
|---------------|----------|
| **Kiro プロファイルのアプリケーション**（例: `KiroProfile-us-east-1`） | 利用者は Kiro のサブスクリプションを通じてこのアプリケーションに割り当てられる |
| **Kiro Sign-In アプリケーション**（名前が `Kiro Sign-In -` で始まる） | Kiro Web が `app.kiro.dev` でのサインインに使う。**AWS アクセスポータルには表示されない**ため、利用者にはタイルが見えない |

| 項目 | 内容 |
|------|------|
| アプリケーションの組 | **Kiro プロファイルごとに1組**。複数の Kiro プロファイルを持つ組織には、**同じ名前の Kiro Sign-In アプリケーションが複数**ありうる |

### 有効のままにする（してはいけないこと）

| # | してはいけないこと |
|---|----------------|
| 1 | Kiro Sign-In アプリケーションを**無効化・削除しない**（重複に見えても） |
| 2 | Kiro Sign-In アプリケーションを **Require assignments（割り当てを必須）にしない** |

公式は、どちらの変更も「**パスワードと MFA の入力後に Kiro Web のサインインが `access_denied` で失敗する**原因になりうる」と説明しています。対処は[トラブルシューティング](#kiro-web-で-access_denied-になる場合)を参照してください。

> **「Do not require assignments」にしても、Kiro のサブスクリプションが付与されるわけではありません。**
> 公式は「Setting Do not require assignments lets identities reach the sign-in application. It does not give anyone a Kiro subscription.」と書いており、**利用者にはいずれかのプロファイルで有効な Kiro サブスクリプションが必要**です。

### 複数の Kiro プロファイルがある組織

**すべての Kiro Sign-In アプリケーションを有効にし、割り当てを必須にしない**状態にします。また、利用者が選びうる**各 Kiro プロファイルを所有する AWS アカウントで Cloud Sessions を有効**にします。

---

## 制限 — 適用されない共有設定

公式は「The following shared settings configured by your administrator **do not apply** to the Kiro Web experience」として、**管理者が設定しても Kiro Web には効かない項目**を挙げています。

| # | 適用されない共有設定 |
|---|------------------|
| 1 | Include suggestions with code references（コード参照付きの提案） |
| 2 | Model Context Protocol（MCP） |
| 3 | Model availability（利用できるモデル） |
| 4 | Member account subscriptions（メンバーアカウントのサブスクリプション） |
| 5 | MCP registry URL |
| 6 | **Encryption key** — **Customer Managed Keys（CMK）は Kiro Web ではサポートされません** |

### その他のガバナンスポリシー

公式は次のように説明しています。

> Other enterprise governance policies (such as model selection and web tool controls) are not currently available for Kiro Web.

モデル選択や web ツール制御といった**その他のエンタープライズガバナンスポリシーも、現時点では Kiro Web で利用できません**。

### エージェント設定は利用者ごとに個別管理されます

公式は次のように説明しています。

> Agent settings, including **GitHub and GitLab connections**, sandbox configuration, and data collection preferences, are managed separately by each user in Kiro Web Settings.

| 項目 | 管理する場所 |
|------|-----------|
| **GitHub 接続・GitLab 接続** | **利用者ごと**（Kiro Web の Settings）<br>※ 2026-09-02 更新で GitLab 接続が追記されました |
| サンドボックス設定 | **利用者ごと**（同上） |
| データ収集の設定 | **利用者ごと**（同上） |

> つまり、**管理者が一括で統制できない設定があります。** MCP・モデル可用性・CMK が
> 共有設定として効かない点と合わせて、導入前に確認が必要です。
>
> サンドボックスの設定内容は [01_features/05_sandbox.md](../01_features/)、
> データ収集のオプトアウト手順は [03_data-protection.md](03_data-protection.md) を参照してください。

---

## 利用開始の手順

公式の手順は3ステップです。

1. Identity Center の資格情報で <https://app.kiro.dev> にサインインする
2. **GitHub または GitLab を接続**して、エージェントにリポジトリへのアクセスを与える
3. エージェントで作業を始める

接続手順の詳細は [01_setup.md](01_setup.md) を参照してください。

### ファイアウォールがある場合

IAM Identity Center を使う場合、**追加で許可が必要なエンドポイント**があります（SSO ポータル・OIDC トークン交換・外部 IdP のドメインなど）。一覧は [04_reference/01_allowed-domains.md](../04_reference/) を参照してください。

---

## トラブルシューティング

### Kiro Web で `access_denied` になる場合

**2026-10-21 版で新設された節です。** 公式は次のように説明しています。

> If Kiro IDE or Kiro CLI sign-in works for the same user and start URL but Kiro Web shows `access_denied`, a Kiro Sign-In application is the likely cause.

| 項目 | 内容 |
|------|------|
| 症状 | 同じ利用者・同じ開始 URL で **Kiro IDE・Kiro CLI のサインインは通る**のに、**Kiro Web が `access_denied` を表示する**（パスワードと MFA の入力後） |
| 公式が挙げる原因 | **Kiro Sign-In アプリケーションが無効**、または**割り当てが必須になっている** |
| 利用者の作業 | Kiro IDE と Kiro CLI は**このアプリケーションを使わない**ため、管理者が下記を行う間も **IDE・CLI では作業を続けられる** |

管理者が Kiro Sign-In アプリケーションを確認・修正する手順（公式）:

| # | 手順 |
|---|------|
| 1 | IAM Identity Center インスタンスを管理する **AWS アカウント**にサインインし、そのインスタンスの AWS リージョンで **IAM Identity Center コンソール**を開く |
| 2 | **Applications** を選び、**AWS managed** タブを選ぶ |
| 3 | 名前が `Kiro Sign-In -` で始まるアプリケーションを探す。**同じ名前のものが複数あれば、すべて確認する** |
| 4 | アプリケーションの **Status が Inactive** なら、それを選び **Actions > Enable** を選ぶ |
| 5 | 各 Kiro Sign-In アプリケーションを開き、**ユーザーとグループの割り当て方式**を確認する。**Require assignments** なら、**Action > Edit Details** を選び、**Do not require assignments** を選んで **Save changes** を選ぶ |
| 6 | Kiro Sign-In アプリケーションが**削除されている**場合は **AWS サポート**に連絡する |
| 7 | 利用者に、**プライベートブラウザウィンドウ**で `app.kiro.dev` に再度サインインしてもらう |

必要な権限（公式の記述）:

| 操作 | 権限 |
|------|------|
| IAM Identity Center を開き、アプリケーションを表示する | 権限が必要 |
| アプリケーションを有効にする | `sso:UpdateApplication` |
| 割り当て方式を変更する | `sso:PutApplicationAssignmentConfiguration` |

> 公式は「Your organization's policies may require more read permissions.」（組織のポリシーによっては、さらに読み取り権限が必要になる場合がある）とも書いています。

---

## 🔗 関連ページ

- [01_setup.md](01_setup.md) — セットアップと最初のタスク
- [03_data-protection.md](03_data-protection.md) — データ保護（エンタープライズ利用者は自動的にオプトアウト）
- [04_firewalls.md](04_firewalls.md) — ファイアウォール・プロキシの設定
- 公式: <https://kiro.dev/docs/web/identity-center/>

---

[← 03_deployment に戻る](README.md)
