# AWS Identity Center（要件と制限）

> **本ページは Kiro Web 版（<https://app.kiro.dev>）の仕様です。**
> Kiro IDE / Kiro CLI とは別製品です。**Kiro Web は Preview 段階**です。

**出典**: <https://kiro.dev/docs/web/identity-center/>（Page updated: June 11, 2026）

組織で AWS Identity Center を使っている場合、Kiro Web の利用には**追加の要件**があります。また、**管理者が設定した共有設定の一部が Kiro Web には適用されません**。

---

## 📑 このページの内容

1. [組織で Kiro Web を有効化する（管理者作業）](#組織で-kiro-web-を有効化する管理者作業)
2. [要件](#要件)
3. [制限 — 適用されない共有設定](#制限--適用されない共有設定)
4. [利用開始の手順](#利用開始の手順)

---

## 組織で Kiro Web を有効化する（管理者作業）

公式は「Administrators must enable the Kiro Web agent before users in the organization can access it」として、**利用者がアクセスする前に管理者が有効化する必要がある**と説明しています。

手順は3ステップです。

1. **Kiro を構成している AWS アカウント**に移動する
2. **Settings > Kiro Settings** に移動する
3. **Autonomous agents** をオンにする

> 有効化する項目の名前は **「Autonomous agents」** です（「Kiro Web」という名前の項目ではありません）。

---

## 要件

公式が挙げている要件は4点です。

| # | 要件 | 補足 |
|---|------|------|
| 1 | **Kiro Profile が必要** | **Q Developer Profile では動作しません** |
| 2 | **Kiro に接続された GitHub アカウント** | — |
| 3 | **管理者による有効化** | Kiro を構成している AWS アカウントの **Settings > Kiro Settings** から（[上記](#組織で-kiro-web-を有効化する管理者作業)） |
| 4 | **リージョン** | Preview 中は **US East（N. Virginia）`us-east-1` のみ** |

### ⚠️ Q Developer Profile では動作しません

公式は次のように明記しています。

> Kiro Web requires a Kiro Profile — it does not work with Q Developer Profiles

Amazon Q Developer から移行した環境では、プロファイルの種類を確認してください。

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

> Agent settings — including GitHub connections, sandbox configuration, and data collection preferences — are managed separately by each user on the Kiro Web Settings page.

| 項目 | 管理する場所 |
|------|-----------|
| GitHub 接続 | **利用者ごと**（Kiro Web の Settings ページ） |
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
2. **GitHub を接続**して、エージェントにリポジトリへのアクセスを与える
3. エージェントで作業を始める

接続手順の詳細は [01_setup.md](01_setup.md) を参照してください。

### ファイアウォールがある場合

IAM Identity Center を使う場合、**追加で許可が必要なエンドポイント**があります（SSO ポータル・OIDC トークン交換・外部 IdP のドメインなど）。一覧は [04_reference/01_allowed-domains.md](../04_reference/) を参照してください。

---

## 🔗 関連ページ

- [01_setup.md](01_setup.md) — セットアップと最初のタスク
- [03_data-protection.md](03_data-protection.md) — データ保護（エンタープライズ利用者は自動的にオプトアウト）
- [04_firewalls.md](04_firewalls.md) — ファイアウォール・プロキシの設定
- 公式: <https://kiro.dev/docs/web/identity-center/>

---

[← 03_deployment に戻る](README.md)
