# 許可ドメイン・URL・IP の一覧

> **本ページは Kiro Web 版（<https://app.kiro.dev>）の仕様です。**
> Kiro IDE / Kiro CLI とは別製品です。**Kiro Web は Preview 段階**です。

**出典**: <https://kiro.dev/docs/web/firewalls/>（Page updated: May 27, 2026）・<https://kiro.dev/docs/web/sandbox/internet-access/>（Page updated: April 21, 2026）・<https://kiro.dev/docs/web/gitlab/>（Page updated: July 16, 2026）

> ⚠️ **本ページの値はすべて公式ページの HTML 版から取っています。**
> `firewalls` の `.md` 版は3サーフェス分が連結されているため使用していません
> （[00_information/02_information-sources.md](../00_information/02_information-sources.md#b-3製品分の内容が連結される1ページ)）。

---

## 📑 このページの内容

許可リストは**目的が違う3系統**に分かれます。混同しないでください。

| # | 系統 | 誰が通信するか | 件数 |
|---|------|--------------|------|
| 1 | [Kiro Web 本体のエンドポイント](#1-kiro-web-本体のエンドポイント34-行) | **利用者のネットワーク → Kiro のバックエンド** | **34 行** |
| 2 | [サンドボックスの依存関係取得先](#2-サンドボックスの依存関係取得先73-ドメイン) | **サンドボックス → パッケージレジストリ** | **73 ドメイン** |
| 3 | [GitLab 側で許可する送信元 IP](#3-gitlab-側で許可する送信元-ip3-件) | **Kiro Web → 利用者の GitLab** | **3 件** |

---

## 1. Kiro Web 本体のエンドポイント（34 行）

**出典**: <https://kiro.dev/docs/web/firewalls/>（HTML 版）

自社ネットワークのファイアウォール・プロキシで許可します。考え方と構成別の必要グループは [03_deployment/04_firewalls.md](../03_deployment/04_firewalls.md) を参照してください。

### 1-1. Core URLs — 全 Kiro 製品共通（2 行）

公式は「required by all Kiro products (IDE, CLI, and Web)」としています。

| URL | 用途 |
|-----|------|
| `app.kiro.dev` | サインインポータル |
| `assets.app.kiro.dev` | アプリケーションアセット |

### 1-2. Core URLs — Kiro Web に必要（15 行）

公式は「Every Kiro Web deployment also needs the following URLs. These cover AI services and telemetry.」としています。

| URL | 用途 |
|-----|------|
| `kaa-assets.app.kiro.dev` | エージェントアプリケーションのアセット |
| `kiro.dev` | Kiro の Web サイトとドキュメント |
| `prod.us-east-1.auth.desktop.kiro.dev` | トークンの交換・更新・ログアウト |
| `kiro-prod-us-east-1.auth.us-east-1.amazoncognito.com` | Cognito 認証 |
| `management.us-east-1.kiro.dev` | 構成・アクセス管理 |
| `q.*.amazonaws.com` | Kiro サービスのエンドポイント（**レガシー**・下記の注意を参照） |
| `prod.us-east-1.telemetry.kiro.aws.dev` | テレメトリとメトリクス |
| `prod.download.desktop.kiro.dev` | ダウンロードと更新 |
| `a0.awsstatic.com` | AWS の静的アセット |
| `dataplane.rum.us-east-1.amazonaws.com` | CloudWatch RUM（US East） |
| `dataplane.rum.eu-central-1.amazonaws.com` | CloudWatch RUM（ヨーロッパ） |
| `prod.assets.shortbread.aws.dev` | Cookie 同意のアセット |
| `prod.log.shortbread.aws.dev` | Cookie 同意のログ |
| `prod.tools.shortbread.aws.dev` | Cookie 同意のツール |
| `rendering.aperture-public-api.feedback.console.aws.dev` | フィードバックフォーム |

> ⚠️ **`q.<region>.amazonaws.com` はレガシーですが、まだ必要です。**
> 公式は「将来のリリースで廃止予定。廃止が完了するまではランタイム・管理・テレメトリの
> 各エンドポイントと併せて許可リストに残す必要がある」としています。
> **廃止時期は公式に示されていないため未確認です。**

### 1-3. Social sign-in（1 行）

Google または GitHub でサインインする場合に追加します。

| URL | 用途 |
|-----|------|
| `cognito-identity.us-east-1.amazonaws.com` | ソーシャルサインインのフェデレーテッドアイデンティティ |

### 1-4. IAM Identity Center（6 行）

AWS IAM Identity Center で認証する場合に追加します。

| URL | 用途 |
|-----|------|
| `<region>.signin.aws` | AWS サインイン |
| `<sso-region>.signin.aws.amazon.com` | AWS サインイン（代替） |
| `<idc-directory-id-or-alias>.awsapps.com` | IAM Identity Center ポータル |
| `portal.sso.<sso-region>.amazonaws.com` | SSO ポータル |
| `assets.sso-portal.<sso-region>.amazonaws.com` | SSO ポータルのアセット |
| `oidc.<sso-region>.amazonaws.com` | OIDC トークン交換 |

**置き換えるプレースホルダ**:

| プレースホルダ | 置き換える値 |
|--------------|-----------|
| `<idc-directory-id-or-alias>` | IAM Identity Center インスタンスの**ディレクトリ ID またはエイリアス** |
| `<sso-region>` | インスタンスが有効化されている **AWS リージョン** |

### 1-5. External identity providers（2 行）

IAM Identity Center と外部 IdP を併用する場合、**サインインフローが IdP のドメインを経由する**ため、そのドメインも許可します。

| アイデンティティプロバイダ | 許可するドメイン |
|----------------------|--------------|
| Microsoft Entra ID | `login.microsoftonline.com` |
| Okta | `<your-org>.okta.com` |

> 公式は、どの IdP が設定されているか不明な場合は**アイデンティティチームに正確なドメインを確認する**よう案内しています。

### 1-6. Subscription management（2 行）

Google・GitHub・AWS Builder ID でサインインする場合、Kiro は **Stripe** を課金に使います。

| URL | 用途 |
|-----|------|
| `billing.stripe.com` | 有料プランの課金ポータル |
| `checkout.stripe.com` | プランのアップグレード時のチェックアウト |

> **IAM Identity Center を使うエンタープライズ顧客はこの2件が不要**です（公式明記）。

### 1-7. Wildcard rules（6 件・上記の代替）

ネットワークポリシーでワイルドカードが使える場合、許可リストを簡略化できます。

| ワイルドカード | 対象 |
|--------------|------|
| `*.kiro.dev` | Kiro の**単一階層**サブドメインすべて |
| `*.app.kiro.dev` | アプリケーションと CDN のアセット |
| `*.kiro.aws.dev` | テレメトリのエンドポイント |
| `*.amazonaws.com` | AWS サービスのエンドポイントすべて（Kiro サービス・RUM・OIDC・SSO・Cognito） |
| `*.shortbread.aws.dev` | Cookie 同意 |
| `*.signin.aws` | IAM Identity Center のサインイン |

> ⚠️ **ファイアウォールによってサブドメインの一致範囲が違います。** 単一階層しか一致しない
> 実装では `*.kiro.dev` は `app.kiro.dev` に一致しますが **`assets.app.kiro.dev` には一致しません**
> （これは必須2件の一方です）。`*.app.kiro.dev` も追加するか、多階層を明示的に列挙してください。

### 行数の内訳（合計 34 行）

| グループ | 行数 |
|---------|-----|
| 1-1. Core URLs（全製品共通） | 2 |
| 1-2. Core URLs（Kiro Web） | 15 |
| 1-3. Social sign-in | 1 |
| 1-4. IAM Identity Center | 6 |
| 1-5. External identity providers | 2 |
| 1-6. Subscription management | 2 |
| 1-7. Wildcard rules | 6 |
| **合計** | **34** |

---

## 2. サンドボックスの依存関係取得先（73 ドメイン）

**出典**: <https://kiro.dev/docs/web/sandbox/internet-access/>（Page updated: April 21, 2026）

**これは系統1とは別物です。** サンドボックス内のエージェントがパッケージを取得するための許可リストで、**ネットワークアクセスレベルを「Common dependencies」にすると自動的に許可されます**（利用者が個別に設定する必要はありません）。

ネットワークアクセスレベルの選択肢は [01_features/05_sandbox.md](../01_features/05_sandbox.md#ネットワークアクセスレベル4-種類) を参照してください。

### Common dependencies で自動的に許可される 73 ドメイン

公式ページに列挙されている全件です（アルファベット順・**73 件**）。

```
alpinelinux.org          amazonaws.com            anaconda.com
apache.org               apt.llvm.org             archlinux.org
aws.amazon.com           azure.com                bitbucket.org
bower.io                 centos.org               cocoapods.org
continuum.io             cpan.org                 crates.io
debian.org               docker.com               docker.io
dot.net                  dotnet.microsoft.com     eclipse.org
fedoraproject.org        gcr.io                   ghcr.io
github.com               githubusercontent.com    gitlab.com
golang.org               google.com               goproxy.io
gradle.org               hashicorp.com            haskell.org
hex.pm                   java.com                 java.net
jcenter.bintray.com      json-schema.org          json.schemastore.org
k8s.io                   launchpad.net            maven.org
mcr.microsoft.com        metacpan.org             microsoft.com
nodejs.org               npmjs.com                npmjs.org
nuget.org                oracle.com               packagecloud.io
packages.microsoft.com   packagist.org            pkg.go.dev
ppa.launchpad.net        pub.dev                  pypa.io
pypi.org                 pypi.python.org          pythonhosted.org
quay.io                  ruby-lang.org            rubyforge.org
rubygems.org             rubyonrails.org          rustup.rs
rvm.io                   sourceforge.net          spring.io
swift.org                ubuntu.com               visualstudio.com
yarnpkg.com
```

### カスタム許可リストの書式

「Common dependencies」に含まれないドメインが必要な場合、**カンマ区切りのカスタムリスト**を指定できます。**サブドメインをまとめて含めるには `.domain` 形式**を使います。

| 記述 | 意味 |
|------|------|
| `api.example.com` | **この特定のドメインのみ**を許可 |
| `.example.com` | `example.com` **と全サブドメイン**（`api.example.com`・`www.example.com` など）を許可 |
| `api.example.com, .cdn.example.com` | 複数のドメインとサブドメインパターンを許可 |

> **先頭のドット（`.example.com`）の有無で意味が変わります。** ドット無しは完全一致のみです。

---

## 3. GitLab 側で許可する送信元 IP（3 件）

**出典**: <https://kiro.dev/docs/web/gitlab/>（Page updated: July 16, 2026）

**これは方向が逆です。** 系統1・2は「Kiro 側への送信」ですが、これは **Kiro Web から利用者の GitLab インスタンスへの受信**です。

公式は次のように説明しています。

> If your GitLab instance is reachable over the public internet and uses IP allowlisting or firewall rules, you must allow inbound traffic from the following Kiro Web source IP addresses.

GitLab インスタンスがインターネット経由で到達可能で、**IP 許可リストやファイアウォールルールを使っている場合**、次の送信元 IP からの受信を許可する必要があります。

| Kiro Web の送信元 IP |
|------------------|
| `34.228.181.128` |
| `44.219.176.187` |
| `54.226.244.221` |

> `gitlab.com` を使っている場合は、この設定は通常不要です（自社の IP 制限がある場合を除く）。
> セルフホストの GitLab を IP 制限している場合に必要になります。

---

## 🔗 関連ページ

- [03_deployment/04_firewalls.md](../03_deployment/04_firewalls.md) — 許可リストの考え方・構成別に必要なグループ
- [01_features/05_sandbox.md](../01_features/05_sandbox.md) — サンドボックスのネットワークアクセスレベル
- [01_features/06_repository-integration.md](../01_features/06_repository-integration.md) — GitHub / GitLab 連携
- [02_environment-variables.md](02_environment-variables.md) — 環境変数・シークレット
- 公式: <https://kiro.dev/docs/web/firewalls/>・<https://kiro.dev/docs/web/sandbox/internet-access/>・<https://kiro.dev/docs/web/gitlab/>

---

[← 04_reference に戻る](README.md)
