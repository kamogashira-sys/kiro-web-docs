# データ保護（保存先・暗号化・オプトアウト）

> **本ページは Kiro Web 版（<https://app.kiro.dev>）の仕様です。**
> Kiro IDE / Kiro CLI とは別製品です。**Kiro Web は [2026-09-01 に一般提供（GA）になりました](https://kiro.dev/changelog/web/kiro-web-is-now-generally-available/)。**

**出典**: <https://kiro.dev/docs/privacy-and-security/data-protection/>（Page updated: August 4, 2026・**移転先。旧 `docs/web/data-protection/` は2026-08-04以前は Page updated: July 14, 2026**）

> このページは2026-08-04に更新され、2026-08-12以前の公式サイト再構成で
> `docs/privacy-and-security/data-protection/` へ移転しました。

---

## 📑 このページの内容

1. [責任共有モデル](#責任共有モデル)
2. [データの保存先](#データの保存先)
3. [リージョン間推論（cross-region inference）](#リージョン間推論cross-region-inference)
4. [暗号化](#暗号化)
5. [サービス改善への利用](#サービス改善への利用)
6. [データ共有をオプトアウトする](#データ共有をオプトアウトする)
7. [不正利用の検知](#不正利用の検知)
8. [⚠️ Free Tier に関する公式ページ間の食い違い](#free-tier-conflict)

---

## 責任共有モデル

公式は **AWS の責任共有モデル**が Kiro Web のデータ保護にも適用されると説明しています。

| 主体 | 責任範囲（公式の説明） |
|------|------------------|
| **AWS** | AWS クラウド全体を動かす**グローバルインフラストラクチャの保護** |
| **利用者** | インフラ上にホストする**自分のコンテンツの管理**、および利用する AWS サービスの**セキュリティ設定と管理タスク** |

---

## データの保存先

### 何が保存されるか

公式は、Kiro が次のものを保存すると説明しています（2026-08-04 更新で IDE/CLI/Web 共通の記述に変更）。

- 質問・応答（questions, responses）
- コード等の追加コンテキスト（additional context such as code and metadata）
- 不正利用検知のため、一部の場合に上記を保存（[不正利用の検知](#不正利用の検知)）

> ⚠️ **記述が「Kiro Web が保存する」から「Kiro が保存する」に変わりました。**
> 旧記述（task descriptions・chat messages・code changes）から
> 新記述（questions・responses・additional context）に文言が変わっていますが、
> **実質的に指している内容は同種**と判断できます。公式による説明変更の意図は不明のため、
> 変更があったという事実のみを記載します。

### 保存されるリージョン

> If you are a Kiro Free Tier user or a Kiro individual subscriber, your content, such as prompts and responses, will be stored in the US East (N. Virginia) Region.

**Kiro Free Tier 利用者・個人サブスクライバーの場合、コンテンツは US East（N. Virginia）リージョンに保存されます。**

> ⚠️ **2026-08-04 の更新で「Preview中は全コンテンツがUS East」という記述が、
> 利用者区分別の記述に変わりました。** 新たに「Kiro enterprise user の場合、
> プロファイルが構成されているリージョンに保存される場合がある」という記述が追加されています
> （"your content ... may be stored in the region where your profile is configured"）。
> **Kiro Web に enterprise 利用者区分が存在するかは [02_identity-center.md](02_identity-center.md) の
> 対象（AWS Identity Center 利用）と関連する可能性がありますが、この記述が Kiro Web の
> Identity Center 利用者にも適用されるかは公式から判別できないため未確認です。**

---

## リージョン間推論（cross-region inference）

Kiro Web は**リージョン間推論**を使い、大規模言語モデル（LLM）の推論性能と信頼性を高めるためにトラフィックを複数の AWS リージョンに分散します。公式は「需要が高い時期のスループットと回復力の向上、性能の改善」を挙げています。

### ⚠️ 保存先と処理先は別です

公式は次のように明記しています。

> Cross region inference doesn't affect where your data is stored.

**保存先と処理先は別です。** 2026-08-04 の更新で「All data remains stored in the US East (N. Virginia) Region during the preview」という**Preview全体を対象にした一文が削除**され、保存先はデータの保存節（[前述](#保存されるリージョン)・利用者区分別）を参照する形に変わりました。

| 項目 | リージョン |
|------|----------|
| **データの保存先** | Free Tier・個人サブスクライバーは **US East（N. Virginia）のみ**（[前述](#保存されるリージョン)） |
| **推論の処理先** | 保存先と異なるリージョンになる場合がある（下表） |

### 対応リージョン（2026-08-04 の更新でヨーロッパが追加）

> ⚠️ **本サイトの正準値 S12（推論リージョン3件）に影響する変更です。** 実測を記録します。

| 対応地域 | 推論リージョン |
|---------|--------------|
| United States | **US East（N. Virginia）`us-east-1`**<br>**US West（Oregon）`us-west-2`**<br>**US East（Ohio）`us-east-2`**<br>AWS GovCloud (US-East)<br>AWS GovCloud (US-West) |
| **Europe（2026-08-04 新設）** | Europe (Frankfurt) `eu-central-1`<br>Europe (Ireland) `eu-west-1`<br>Europe (Paris) `eu-west-3`<br>Europe (Stockholm) `eu-north-1`<br>Europe (Milan) `eu-south-1`<br>Europe (Spain) `eu-south-2` |

> **この表が Kiro Web にそのまま適用されるかは未確認です。** 本ページは2026-08-04の更新で
> IDE/CLI/Web共通の記述に変わっており（[前述](#何が保存されるか)）、GovCloud・欧州リージョンの
> 追加が Kiro Web のユーザーにも実際に関係するかは公式から判別できません。
> 従来の「米国内3リージョン」という記述（S12=3）は**この共通ページの旧内容**であり、
> 現時点でKiro Web固有の対応リージョン数を確定できないため、**S12は実測差分の記録に留め、
> 正準値としての更新は見送ります**（Phase 5 で再検討）。

> 実験的機能向けの「グローバルクロスリージョン推論」も新設されていますが、
> **「実験的タグが付いたモデル・機能のみ」に限定される**ため、Kiro Web の通常機能への
> 影響は未確認です。

---

## 暗号化

### 転送中の暗号化

> All communication between customers and **Kiro** and between **Kiro** and its downstream dependencies is protected using TLS 1.2 or higher connections.

> ⚠️ **移転により主語が「Kiro Web」から「Kiro」に一般化されました。**
> 移転前の `docs/web/data-protection/` は `between customers and **Kiro Web**` と書いていましたが、
> 全製品共通ページである現行の `docs/privacy-and-security/data-protection/` は **Kiro** です（2026-09-13 実測）。
> **Kiro Web に限った記述ではなくなっている**点に注意してください（保護内容そのものは同じです）。

| 経路 | 保護 |
|------|------|
| 利用者 ↔ Kiro Web | **TLS 1.2 以上** |
| Kiro Web ↔ 下流の依存サービス | **TLS 1.2 以上** |

### 保存時の暗号化

公式は、Kiro Web が **AWS Key Management Service（AWS KMS）の AWS 所有キー（AWS owned keys）**でデータを暗号化すると説明しています。**利用者側で保護のための操作は不要**です。

> ⚠️ **カスタマー管理キー（CMK）は Kiro Web ではサポートされません。**
> これは Identity Center の共有設定が適用されない項目の1つです
> （[02_identity-center.md](02_identity-center.md#制限--適用されない共有設定)）。
>
> **2026-08-04 の移転後、移転先ページには「Kiro enterprise で管理者が CMK を設定できる」という
> 新しい記述が追加されています。** この記述が Kiro Web にも適用されるのか、
> IDE/CLI のみを指すのかは公式ページから判別できないため**未確認**です。
> 上記の Identity Center 経由の非対応記述（共有設定として適用されない）と矛盾するかどうかも
> 現時点では判断できません。

---

## サービス改善への利用

### 対象となる利用者

公式は次のように説明しています。

> We may use certain content from Kiro Free Tier and Kiro individual subscribers for service improvement.

> ⚠️ **2026-08-04 の更新で「Kiro Web Free Tier」から「Kiro Free Tier」に文言が変わりました**
> （「Web」が削除）。これも本ページが IDE/CLI/Web 共通の記述に変わったことによる変化と考えられますが、
> Kiro Web の Free Tier 利用者を指す実質的な内容は変わっていないと判断できます。

| 利用者区分 | サービス改善への利用 |
|-----------|------------------|
| **Kiro Free Tier** | 対象になりうる |
| **個人サブスクライバー**（individual subscribers） | 対象になりうる |
| **エンタープライズ利用者** | **対象外**（「We do not use content from Kiro enterprise users for service improvement」） |

公式は「個人サブスクライバー」を、**有料の Kiro サブスクリプションを持ち、ソーシャルログイン（GitHub・Google など）または AWS Builder ID でアクセスする利用者**と定義しています。

> **2026-08-04 の更新で新規追加**: Amazon Q Developer Pro サブスクリプションで
> AWS アカウント経由で Kiro にアクセスする場合、コンテンツはサービス改善に使われません。

### 対象となるコンテンツ

質問・その他の入力・Kiro が生成した応答とコード（2026-08-04 更新で「タスクの説明・チャットメッセージ」から文言変更）。

公式が挙げている用途は、よくある質問へのより良い応答の提供、運用上の問題の修正、デバッグ、**モデルの訓練**です。

---

## データ共有をオプトアウトする

### 既定の動作

公式は次のように説明しています。

> By default, Kiro collects usage data, errors, crash reports, and other metrics as well as content for service improvement from Kiro Free Tier users and Kiro individual subscribers.

**既定では収集されます**（Free Tier 利用者・個人サブスクライバー）。

### エンタープライズ利用者は自動的にオプトアウトされます

> Kiro enterprise users are automatically opted out of telemetry and content collection by AWS.

エンタープライズ利用者は、テレメトリとコンテンツ収集から**自動的にオプトアウトされます**。ただし**ユーザーアクティビティレポート用のテレメトリ設定は Kiro コンソールで管理者が制御し、エンタープライズ利用者自身は設定できません**。

### オプトアウトの手順（Web）

1. サインインして **Settings** に移動する
2. **Agent** 設定を選ぶ
3. **Allow AWS to use your Kiro Web content for service improvement** をオフにする

### ⚠️ オプトアウトしても保存される場合があります

公式は次のように注記しています。

> If you are a Kiro Free Tier user, opting out of sharing your data for service improvement does not affect our ability to store your inputs for abuse detection purposes as described in more detail here.

**Free Tier 利用者の場合、サービス改善のオプトアウトは「不正利用検知のための入力の保存」には影響しません。** 保持期間は[次節](#不正利用の検知)を参照してください。

---

## 不正利用の検知

すべての Kiro 利用者・全モデルに適用される Amazon Bedrock の不正利用検知に**加えて**、公式は次を挙げています。

| 対象 | 保持期間 | 目的 |
|------|---------|------|
| **Kiro Free Tier 利用者のみ** | 入力を**最長 60 日** | 規約違反の活動の検知と、検知能力の向上 |
| **OpenAI GPT モデル** | 分類器がフラグを立てたトラフィックを**最長 30 日** | 自動オフライン不正利用検知 |

### 保存内容の扱い

- Free Tier 利用者の入力は、**Kiro の基盤となる生成 AI モデルの改善には使われません**
- ただし**不正利用検知用の分類器ツールの開発・改善には使われる場合があります**
- フラグが立ったトラフィックは、**推論が処理されたリージョンに保存**されます

### 違反時の措置

公式は、Kiro またはモデルの不正利用、あるいは不正利用への対処の failure が、**Kiro へのアクセスの停止または終了につながる場合がある**と説明しています。誤って違反と判定されたと考える場合はサポートに連絡するよう案内しています。

---

<a id="free-tier-conflict"></a>
## ⚠️ Free Tier に関する公式ページ間の食い違い

**2026-08-01 時点で未解決**でした。**2026-08-04 に本ページが移転先へ更新され、食い違いは継続しています**（Phase 4 で `docs/web/` トップの2026-08-14更新内容を確認する）。

| 出典 | Page updated | 記述の要旨 |
|------|-------------|-----------|
| `docs/web/`・`docs/web/setup/` | 2026-06-11 | Kiro Web の利用には **Pro 以上**が必要。**「Kiro Web is not available on the free tier」** |
| **本ページ**（`docs/privacy-and-security/data-protection/`・移転先） | **2026-08-04**（より新しい） | **「Kiro Web Free Tier」**という区分が繰り返し登場し、Free Tier 利用者のデータ保持（60 日）・オプトアウト・不正利用検知が記述されている |

### 本サイトの扱い

- **どちらが正しいかを断定しません**
- **両方の記述を示します**（本ページと [01_setup.md](01_setup.md#free-tier-conflict) の双方に明記）
- **「更新日が新しい方を採る」という機械的な判断もしません**

> 更新日の新しさは一般には有力な手がかりです。しかし**それを根拠に一方を否定すると、
> 公式が書いていないことを本サイトが決めたことになります。**
> 判断の経緯は [00_information/02_information-sources.md](../00_information/02_information-sources.md#落とし穴5-公式ページ間で記述が食い違うことがある) に記載しています。

実際の適用条件は公式ページで確認してください。

---

## 🔗 関連ページ

- [01_setup.md](01_setup.md) — セットアップ（サブスクリプションの要件）
- [02_identity-center.md](02_identity-center.md) — CMK 非対応・共有設定の制限
- [04_firewalls.md](04_firewalls.md) — テレメトリのエンドポイント
- [04_reference/04_limits.md](../04_reference/) — 保持期間などの値の一覧
- 公式: <https://kiro.dev/docs/privacy-and-security/data-protection/>（移転先）

---

[← 03_deployment に戻る](README.md)
