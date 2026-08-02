# データ保護（保存先・暗号化・オプトアウト）

> **本ページは Kiro Web 版（<https://app.kiro.dev>）の仕様です。**
> Kiro IDE / Kiro CLI とは別製品です。**Kiro Web は Preview 段階**です。

**出典**: <https://kiro.dev/docs/web/data-protection/>（Page updated: July 14, 2026）

> このページは **Kiro Web の docs で2番目に新しい更新**です（2026-08-01 時点）。
> 最新の changelog エントリ（2026-07-01）より後に更新されているため、changelog には現れていません。

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

公式は、Kiro Web が次のものを保存すると説明しています。

- タスクの説明（task descriptions）
- チャットメッセージ（chat messages）
- コードの変更（code changes）
- タスクを実行して応答を生成するための追加コンテキスト

### 保存されるリージョン

> During the preview, all Kiro Web content, such as task descriptions, chat messages, and code changes, is stored in the US East (N. Virginia) Region.

**Preview 中は、すべての Kiro Web のコンテンツが US East（N. Virginia）リージョンに保存されます。**

---

## リージョン間推論（cross-region inference）

Kiro Web は**リージョン間推論**を使い、大規模言語モデル（LLM）の推論性能と信頼性を高めるためにトラフィックを複数の AWS リージョンに分散します。公式は「需要が高い時期のスループットと回復力の向上、性能の改善」を挙げています。

### ⚠️ 保存先と処理先は別です

公式は次のように明記しています。

> Cross-region inference doesn't affect where your data is stored. All data remains stored in the US East (N. Virginia) Region during the preview.

| 項目 | リージョン |
|------|----------|
| **データの保存先** | **US East（N. Virginia）のみ**（Preview 中） |
| **推論の処理先** | 米国内の**別のリージョンになる場合がある**（下表） |

### 対応リージョン（3件）

| 対応地域 | 推論リージョン |
|---------|--------------|
| United States | **US East（N. Virginia）`us-east-1`**<br>**US West（Oregon）`us-west-2`**<br>**US East（Ohio）`us-east-2`** |

> つまり、**データ保存は N. Virginia に限定されますが、処理は米国内3リージョンに分散されます。**
> データ境界の要件がある場合はこの区別が重要です。

---

## 暗号化

### 転送中の暗号化

> All communication between customers and Kiro Web and between Kiro Web and its downstream dependencies is protected using TLS 1.2 or higher connections.

| 経路 | 保護 |
|------|------|
| 利用者 ↔ Kiro Web | **TLS 1.2 以上** |
| Kiro Web ↔ 下流の依存サービス | **TLS 1.2 以上** |

### 保存時の暗号化

公式は、Kiro Web が **AWS Key Management Service（AWS KMS）の AWS 所有キー（AWS owned keys）**でデータを暗号化すると説明しています。**利用者側で保護のための操作は不要**です。

> ⚠️ **カスタマー管理キー（CMK）は Kiro Web ではサポートされません。**
> これは Identity Center の共有設定が適用されない項目の1つです
> （[02_identity-center.md](02_identity-center.md#制限--適用されない共有設定)）。

---

## サービス改善への利用

### 対象となる利用者

公式は次のように説明しています。

> We may use certain content from Kiro Web Free Tier and Kiro individual subscribers for service improvement.

| 利用者区分 | サービス改善への利用 |
|-----------|------------------|
| **Kiro Web Free Tier** | 対象になりうる |
| **個人サブスクライバー**（individual subscribers） | 対象になりうる |
| **エンタープライズ利用者** | **対象外**（「We do not use content from Kiro enterprise users for service improvement」） |

公式は「個人サブスクライバー」を、**有料の Kiro サブスクリプションを持ち、ソーシャルログイン（GitHub・Google など）または AWS Builder ID でアクセスする利用者**と定義しています。

### 対象となるコンテンツ

タスクの説明・チャットメッセージ・その他の入力・Kiro が生成した応答とコード。

公式が挙げている用途は、よくある質問へのより良い応答の提供、運用上の問題の修正、デバッグ、**モデルの訓練**です。

---

## データ共有をオプトアウトする

### 既定の動作

公式は次のように説明しています。

> By default, Kiro Web collects usage data, errors, crash reports, and other metrics as well as content for service improvement from Kiro Free Tier users and Kiro individual subscribers.

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

> If you are a Kiro Free Tier user, opting out of sharing your data for service improvement does not affect our ability to store your inputs for abuse detection purposes.

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

**2026-08-01 時点で未解決**です。

| 出典 | Page updated | 記述の要旨 |
|------|-------------|-----------|
| `docs/web/`・`docs/web/setup/` | 2026-06-11 | Kiro Web の利用には **Pro 以上**が必要。**「Kiro Web is not available on the free tier」** |
| **本ページ**（`docs/web/data-protection/`） | **2026-07-14**（より新しい） | **「Kiro Web Free Tier」**という区分が繰り返し登場し、Free Tier 利用者のデータ保持（60 日）・オプトアウト・不正利用検知が記述されている |

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
- 公式: <https://kiro.dev/docs/web/data-protection/>

---

[← 03_deployment に戻る](README.md)
