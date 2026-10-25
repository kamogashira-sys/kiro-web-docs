# ファイアウォール・プロキシ・データ境界

> **本ページは Kiro Web 版（<https://app.kiro.dev>）の仕様です。**
> Kiro IDE / Kiro CLI とは別製品です。**Kiro Web は [2026-09-01 に一般提供（GA）になりました](https://kiro.dev/changelog/web/kiro-web-is-now-generally-available/)。**

**出典**: <https://kiro.dev/docs/privacy-and-security/firewalls/>（Page updated: October 16, 2026・**移転先。旧 `docs/web/firewalls/` は2026-08-04以前は Page updated: May 27, 2026**）

> ⚠️ **本ページは公式ページの HTML 版のみを出典にしています。**
> このページの `.md` 版（旧 `docs/web/firewalls.md`）は **Web / privacy-and-security / cli の
> 3サーフェス分が連結**されており、Kiro Web 以外の内容が混ざっています
> （3サーフェスの `.md` は 12,349 バイトで完全に同一）。
> 詳細は [00_information/02_information-sources.md](../00_information/02_information-sources.md#b-3製品分の内容が連結される旧1ページ2026-08-12に移転) を参照してください。
>
> **2026-08-04 の移転後、旧 `docs/web/firewalls.md` は404になりました**（実測）。
> 移転先 `docs/privacy-and-security/firewalls.md` は10,844バイトで依然連結状態ですが
> （`Optional URLs`・`Proxy configuration`等の他サーフェス見出しが混在）、
> 3サーフェスすべてが完全一致するかは**再実測が必要**（作業5-4で対応）。

ネットワークにファイアウォール・プロキシサーバー・データ境界がある場合、Kiro がバックエンドサービスに到達できるよう**特定の URL を許可リストに登録する必要があります**。

**許可すべき URL・ドメインの完全な一覧は [04_reference/01_allowed-domains.md](../04_reference/01_allowed-domains.md) にまとめています。** 本ページでは考え方と構成を説明します。

---

## 📑 このページの内容

1. [ネットワークトラフィックの2種類](#ネットワークトラフィックの2種類)
2. [許可リストの構成（7グループ）](#許可リストの構成7グループ)
3. [レガシーエンドポイントの注意](#レガシーエンドポイントの注意)
4. [ワイルドカードを使う場合の注意](#ワイルドカードを使う場合の注意)
5. [構成別に必要なグループ](#構成別に必要なグループ)

---

## ネットワークトラフィックの2種類

公式は、Kiro が **2種類の送信接続**を行うと説明しています。

| 種類 | 内容 |
|------|------|
| **Application traffic** | Kiro のプロセスからのリクエスト。公式は「**In Kiro Web, it flows through backend services.**」としています（IDE・CLI ではプロキシ設定に従う） |
| **Browser traffic** | サインインはブラウザを使う。このトラフィックは **OS のネットワークスタック**を通り、IDE・CLI で設定したプロキシを経由しない |

> 旧 `docs/web/firewalls/` はこの1つ目を **Agent traffic**（Kiro Web からバックエンドサービスへのリクエスト）と呼んでいました。
> 現行の共通ページは **Application traffic** です。

> **ファイアウォールは両方をネットワークレベルで許可する必要があります**（公式:
> "Your firewall must allow both at the network level."）。
>
> ブラウザ側のトラフィックが OS のネットワークスタックを通る点は見落としやすい箇所です。
> アプリケーション単位でしか許可していない環境ではサインインに失敗します。

---

## 許可リストの構成（7グループ）

公式ページの URL 表のうち Kiro Web に関わるもの（全製品共通の表と Web タブの表）は7つのグループに分かれています。**合計 42 行**です（ワイルドカード9件を含む）。

| # | グループ | 行数 | 必要になる条件 |
|---|---------|-----|--------------|
| 1 | **Core URLs（全製品共通）** | 2 | 常に必要 |
| 2 | **Core URLs（Kiro Web 用）** | 15 | 常に必要（AI サービスとテレメトリ） |
| 3 | **Social sign-in** | 2 | Google または GitHub でサインインする場合（**GitHub サインインは `*.awswaf.com` も必要**・下記） |
| 4 | **IAM Identity Center** | 6 | AWS IAM Identity Center で認証する場合 |
| 5 | **External identity providers** | 2 | 外部 IdP（Entra ID・Okta など）を使う場合 |
| 6 | **AWS GovCloud (US)** | 4 | AWS GovCloud (US) で Kiro を使う場合（**Kiro Web への適用は未確認**・下記） |
| 7 | **Subscription management** | 2 | Google・GitHub・AWS Builder ID でサインインする場合（Stripe の課金ポータル） |
| — | **Wildcard rules**（上記の代替） | 9 | ワイルドカードが使える場合 |

**個別の URL とその用途は [04_reference/01_allowed-domains.md](../04_reference/01_allowed-domains.md) を参照してください。**

### グループ3: GitHub サインインには `*.awswaf.com` が必要です（2026-10-16 版で追加）

公式は次のように説明しています。

> If you sign in with Google or GitHub, allowlist the Cognito endpoint below. GitHub sign-in also loads an AWS WAF CAPTCHA from `*.awswaf.com`. If your firewall or proxy blocks this domain, GitHub sign-in fails.

| 項目 | 内容 |
|------|------|
| 追加された許可対象 | **`*.awswaf.com`**（GitHub サインイン用の AWS WAF CAPTCHA） |
| ブロックした場合 | **GitHub サインインが失敗する**（公式の記述） |
| ワイルドカードを1階層分しか一致させないファイアウォールの場合 | **`*.captcha.awswaf.com` と `*.token.awswaf.com` も許可する** |

> Google サインインに `*.awswaf.com` が必要かどうかは、公式の記述が「GitHub sign-in also loads…」であり、**Google については記載がない**ため未確認です。

### グループ1・2 は必須です

公式は、グループ1を「required by all Kiro products (IDE, CLI, and Web)」、グループ2を「Every Kiro Web deployment also needs the following URLs」と説明しています。

### プレースホルダを含む URL があります

IAM Identity Center と外部 IdP のグループには、環境ごとに置き換えるプレースホルダが含まれます。

| プレースホルダ | 置き換える値 |
|--------------|-----------|
| `<idc-directory-id-or-alias>` | IAM Identity Center インスタンスの**ディレクトリ ID またはエイリアス** |
| `<sso-region>` | インスタンスが有効化されている **AWS リージョン** |
| `<your-org>`（Okta） | 組織のサブドメイン |

> 公式は、どの IdP が設定されているか不明な場合は**アイデンティティチームに正確なドメインを確認する**よう案内しています。

### ⚠️ AWS GovCloud (US) のグループ（2026-10-01 版で表になりました）

公式はグループ6を、サーフェス別タブの外にある**全製品共通の節**に置いています。
一方 `docs/web/` は「Kiro Web is available in US East (N. Virginia) `us-east-1` only」としており、
**AWS GovCloud (US) で Kiro Web を使えるかどうかは公式に記載がないため未確認**です。

2026-08-04 版のこの節は `q-fips.*.amazonaws.com` の2件を並べた箇条書きで、本サイトは行数に含めていませんでした。
2026-10-01 版では `runtime-fips.*.kiro.dev`・`management-fips.*.kiro.dev` の4行の表に変わっています。
公式は「既存の `q`・`q-fips` のルールと併せて追加する（古いクライアントはまだ Q のエンドポイントを必要とする場合がある）」と注記しています。

---

## レガシーエンドポイントの注意

公式は次のように注記しています。

> The `q.<region>.amazonaws.com` endpoints are legacy and will be deprecated in a future release. Until deprecation is complete, you must still allowlist them alongside the runtime, management, and telemetry endpoints.

| 項目 | 内容 |
|------|------|
| 対象 | `q.<region>.amazonaws.com` |
| 状態 | **レガシー**。将来のリリースで廃止予定 |
| 現時点の扱い | **廃止が完了するまでは許可リストに残す必要があります**（ランタイム・管理・テレメトリの各エンドポイントと併せて） |

> **「レガシーだから外していい」ではありません。** 廃止時期は公式に示されていないため**未確認**です。

---

## ワイルドカードを使う場合の注意

ネットワークポリシーでワイルドカードが使える場合、個別ドメインの代わりに `*.kiro.dev` と `*.app.kiro.dev` を許可できます。

### ⚠️ ファイアウォールによってサブドメインの一致範囲が違います

公式は次のように注記しています。

> Note that some firewalls only match a single subdomain level, so `*.kiro.dev` would cover `app.kiro.dev` but not `assets.app.kiro.dev`.

| ワイルドカード | 一致する例 | **一致しない例**（単一階層のみ一致するファイアウォールの場合） |
|--------------|----------|--------------------------------|
| `*.kiro.dev` | `app.kiro.dev` | **`assets.app.kiro.dev`**（2階層下） |

**対処**: `*.app.kiro.dev` も追加する、または多階層のサブドメインを明示的に列挙します。

> ワイルドカードは行数を減らせますが、**自分のファイアウォールがどちらの挙動か確認しないと
> 取りこぼします。** 実際に `assets.app.kiro.dev` は Core URLs の必須2件の一方です。

ワイルドカード9件の一覧は [04_reference/01_allowed-domains.md](../04_reference/01_allowed-domains.md) にあります。

---

## 構成別に必要なグループ

公式の記述から、サインイン方法別に必要なグループを整理すると次のようになります。

| 構成 | 必要なグループ |
|------|--------------|
| **ソーシャルログイン（Google / GitHub）** | 1・2・3・7（GitHub は 3 の `*.awswaf.com` も必要） |
| **AWS Builder ID** | 1・2・7 |
| **IAM Identity Center（外部 IdP なし）** | 1・2・4 |
| **IAM Identity Center（外部 IdP あり）** | 1・2・4・5 |

### エンタープライズは Stripe 不要です

公式は「Enterprise customers using IAM Identity Center don't need these domains」として、**IAM Identity Center を使うエンタープライズ顧客はグループ7（Stripe）が不要**と明記しています。

> グループ6（AWS GovCloud (US)）は Kiro Web への適用が未確認のため、上の表には入れていません。

---

## 🔗 関連ページ

- **[04_reference/01_allowed-domains.md](../04_reference/01_allowed-domains.md) — 許可すべき URL・ドメインの完全な一覧（42 行・ワイルドカード9件を含む）**
- [01_setup.md](01_setup.md) — セットアップ（サインイン方法）
- [02_identity-center.md](02_identity-center.md) — AWS Identity Center の要件
- [03_data-protection.md](03_data-protection.md) — データ保護（テレメトリ）
- [01_features/05_sandbox.md](../01_features/) — サンドボックスのネットワークアクセス（**別の許可リスト**）
- 公式: <https://kiro.dev/docs/privacy-and-security/firewalls/>（移転先）

> ⚠️ **サンドボックスの許可ドメインは本ページの一覧とは別です。** サンドボックス内から
> 依存関係を取得するためのドメイン（73 件）は
> [04_reference/01_allowed-domains.md](../04_reference/01_allowed-domains.md) の別節にあります。

---

[← 03_deployment に戻る](README.md)
