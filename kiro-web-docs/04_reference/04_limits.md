# 上限値・保持期間・リージョン

> **本ページは Kiro Web 版（<https://app.kiro.dev>）の仕様です。**
> Kiro IDE / Kiro CLI とは別製品です。**Kiro Web は Preview 段階**です。

**出典**: <https://kiro.dev/docs/web/using-the-agent/>（Page updated: April 21, 2026）・<https://kiro.dev/docs/web/using-the-agent/creating-tasks/>（Page updated: April 21, 2026）・<https://kiro.dev/docs/web/automations/>（Page updated: June 18, 2026）・<https://kiro.dev/docs/web/data-protection/>（Page updated: July 14, 2026）・<https://kiro.dev/changelog/web/start-without-a-repo-switch-modes-anytime/>（June 2, 2026）

> 本ページの値はすべて公式ページの HTML 版と公式 changelog から取っており、本サイトの検証スクリプトが公式との一致を機械的に確認しています。

---

## 📑 早見表

| 項目 | 値 | 出典 |
|------|---|------|
| **並列タスクの上限** | **10** | `using-the-agent/creating-tasks` |
| **1オートメーションあたりのスケジュール数の上限** | **5** | `automations` |
| **オートメーションのプロンプト文字数の上限** | **10,000** 文字 | `automations` |
| **セッションの保持期間** | **90** 日 | `using-the-agent` |
| **サンドボックスのディスク容量** | **128GB** | changelog（2026-06-02） |
| **リージョン間推論の対応リージョン数** | **3** | `data-protection` |
| **データ保存リージョン** | **US East（N. Virginia）のみ**（Preview 中） | `data-protection` |
| **Free Tier の入力保持期間**（不正利用検知） | **最長 60** 日 | `data-protection`（**未確認注記あり**） |
| **GPT モデルのフラグ付きトラフィック保持** | **最長 30** 日 | `data-protection` |
| **転送中の暗号化** | **TLS 1.2** 以上 | `data-protection` |
| **サンドボックスの許可ドメイン数**（Common dependencies） | **73** | `sandbox/internet-access` |
| **ファイアウォール許可リストの行数** | **34** | `firewalls` |
| **GitLab 送信元 IP 数** | **3** | `gitlab` |

---

## タスクの上限

### 並列実行は 10 件までです

公式は、タスクの状態遷移の説明の中で次のように述べています。

> **Queued** — The task is waiting to start. This happens when you've reached the limit of **10 concurrent tasks**.

| 項目 | 値 |
|------|---|
| **同時実行できるタスク数** | **10** |
| 上限に達した場合 | 新しいタスクは **Queued（待機）** 状態になる |

### タスクの状態（5 種類）

| 状態 | 意味 |
|------|------|
| **Queued** | 開始待ち。**並列 10 件の上限に達している**とこの状態になる |
| **In progress** | エージェントが作業中（要件の分析・コードの記述・テストの実行） |
| **Needs attention** | 入力が必要、またはエージェントに確認事項がある。応答するとブロックが解除される |
| **Completed** | 作業が完了しプルリクエストが作成された。**フィードバックを与えると Queued に戻り、枠が空き次第 In progress になる** |
| **Cancelled** | キャンセルされた。**再開できません** |

> **Completed にフィードバックを与えると再びキューに入ります。** つまりフィードバックのやり取りも
> 並列 10 件の枠を消費します。

---

## セッションの保持期間

公式は次のように明記しています。

> Sessions expire after **90 days**, at which point chat messages and logs are deleted. Pull requests, code changes, and conversations on GitHub are not affected.

| 項目 | 内容 |
|------|------|
| **セッションの有効期限** | **90 日** |
| 期限到来時に削除されるもの | **チャットメッセージ**と**ログ** |
| **影響を受けないもの** | **プルリクエスト・コードの変更・GitHub 上の会話** |

> 成果物（PR・コード）は残りますが、**やり取りの経緯は 90 日で消えます。**
> 経緯を残したい場合は PR のコメントなど GitHub 側に記録してください。

---

## オートメーションの上限

**出典**: <https://kiro.dev/docs/web/automations/>（Page updated: June 18, 2026）

| 項目 | 値 | 公式の記述 |
|------|---|-----------|
| **1オートメーションあたりのスケジュール数** | **5** | "You can add up to **five** schedules per automation" |
| **プロンプトの文字数** | **10,000** 文字 | "Prompts can be up to **10,000 characters**" |

> ⚠️ 公式本文でスケジュール数は**綴り（`five`）**で書かれています。数字の `5` を検索しても見つかりません。

### スケジュールの3モード

| モード | 内容 |
|-------|------|
| **Hourly** | 毎時0分に、`Run every` で指定した間隔で実行（例: 1 時間ごと・6 時間ごと） |
| **Daily** | 1 日 1 回、指定した時刻に実行 |
| **CRON** | カスタムの cron 式で完全に制御 |

### ⚠️ スケジュールは UTC で評価されます

公式は次のように説明しています。

> Schedules are evaluated in **UTC**. In the automations list, a schedule's next run is shown in your local time alongside its UTC equivalent, for example At 9:00 AM (1:00 PM UTC).

| 項目 | 内容 |
|------|------|
| **評価のタイムゾーン** | **UTC** |
| 一覧での表示 | **ローカル時刻と UTC の両方**が表示される（例: `At 9:00 AM (1:00 PM UTC)`） |

設定中は生成された cron 式が下に表示されます（例: 1 時間ごとなら `Generates: cron(0 */1 * * ? *)`）。

> **cron 式を自分で書く場合も UTC 基準**です。日本時間（JST = UTC+9）で考えると9時間ずれます。

---

## サンドボックスのディスク容量

**出典**: <https://kiro.dev/changelog/web/start-without-a-repo-switch-modes-anytime/>（June 2, 2026）

| 項目 | 値 |
|------|---|
| **サンドボックスのディスク容量** | **128GB** |

公式は changelog の `Improvements` で次のように説明しています。

> **Sandbox disk**: A larger sandbox disk (now 128GB) lets you work with bigger repositories and heavier dependency installs without running out of space

> ⚠️ **この値は公式ドキュメントではなく changelog にしか記載がありません。**
> しかも**公式サイトで折りたたまれている項目**の中にあります
> （[00_information/02_information-sources.md](../00_information/02_information-sources.md#落とし穴2-折りたたまれた項目は-html-に存在しない)）。
> 2026-06-02 時点で「now 128GB」と記述されたもので、それ以降の変更は確認していません。

---

## リージョンとデータの所在

**出典**: <https://kiro.dev/docs/web/data-protection/>（Page updated: July 14, 2026）

### データの保存先（1 リージョン）

| 項目 | 内容 |
|------|------|
| **保存リージョン** | **US East（N. Virginia）のみ**（Preview 中） |
| 対象 | タスクの説明・チャットメッセージ・コードの変更 |

### 推論の処理先（3 リージョン）

**リージョン間推論により、処理は米国内の別リージョンになる場合があります。保存先は変わりません。**

| 対応地域 | 推論リージョン |
|---------|--------------|
| United States | `us-east-1`（N. Virginia）<br>`us-west-2`（Oregon）<br>`us-east-2`（Ohio） |

### Kiro Web 自体の提供リージョン

| 項目 | 内容 |
|------|------|
| **AWS Identity Center 利用時** | Preview 中は **`us-east-1` のみ** |

詳細は [03_deployment/03_data-protection.md](../03_deployment/03_data-protection.md) と [03_deployment/02_identity-center.md](../03_deployment/02_identity-center.md) を参照してください。

---

## 暗号化

| 項目 | 内容 |
|------|------|
| **転送中** | **TLS 1.2 以上** |
| **保存時** | AWS KMS の **AWS 所有キー**（利用者の操作は不要） |
| **カスタマー管理キー（CMK）** | **サポートされません** |

---

## 不正利用検知の保持期間

| 対象 | 保持期間 |
|------|---------|
| **Kiro Free Tier 利用者の入力** | **最長 60 日** |
| **OpenAI GPT モデルのフラグ付きトラフィック** | **最長 30 日** |

> ⚠️ **この2つの値は「Free Tier が存在する」前提の記述です。** ところが
> `docs/web/`・`docs/web/setup/` は「Kiro Web は無料枠では使えない」としており、
> **公式ページ間で食い違っています（2026-08-01 時点で未解決）**。
> 本サイトはどちらが正しいかを断定しません。
> 詳細は [03_deployment/03_data-protection.md](../03_deployment/03_data-protection.md#free-tier-conflict) を参照してください。

---

## ネットワーク関連の件数

| 項目 | 値 | 詳細 |
|------|---|------|
| **ファイアウォール許可リストの行数** | **34** | [01_allowed-domains.md](01_allowed-domains.md#1-kiro-web-本体のエンドポイント34-行) |
| ワイルドカードルール | 6 件 | 同上 |
| **サンドボックスの許可ドメイン**（Common dependencies） | **73** | [01_allowed-domains.md](01_allowed-domains.md#2-サンドボックスの依存関係取得先73-ドメイン) |
| **GitLab 送信元 IP** | **3** | [01_allowed-domains.md](01_allowed-domains.md#3-gitlab-側で許可する送信元-ip3-件) |

---

## 公式に記載が見つからなかった項目（未確認）

以下は本サイトが公式ドキュメントで確認できなかったため、**値を書きません**。

| 項目 | 状態 |
|------|------|
| 1リポジトリあたり・1セッションあたりのリポジトリ数の上限 | **未確認**（「複数リポジトリ」は明記されているが上限の記載なし） |
| タスクの実行時間の上限 | **未確認** |
| オートメーションの作成数の上限（スケジュール数ではなく本体の数） | **未確認** |
| サンドボックスの CPU・メモリ | **未確認**（ディスク容量のみ記載あり） |
| Preview 期間の週次利用上限の具体値 | **未確認**（最古の changelog エントリに「usage is subject to weekly limits」の記述はあるが数値の記載なし） |

---

## 🔗 関連ページ

- [01_allowed-domains.md](01_allowed-domains.md) — 許可ドメイン・URL・IP の一覧
- [02_environment-variables.md](02_environment-variables.md) — 環境変数・シークレット・IAM ロール
- [03_mcp-configuration.md](03_mcp-configuration.md) — MCP 設定と Powers
- [03_deployment/03_data-protection.md](../03_deployment/03_data-protection.md) — データ保護の詳細
- [02_update/01_changelog.md](../02_update/01_changelog.md) — 更新履歴

---

[← 04_reference に戻る](README.md)
