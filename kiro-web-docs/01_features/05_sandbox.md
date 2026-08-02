# サンドボックス（タスクの実行環境）

> **本ページは Kiro Web 版（<https://app.kiro.dev>）の仕様です。**
> Kiro IDE / Kiro CLI とは別製品です。**Kiro Web は Preview 段階**です。

**出典**: <https://kiro.dev/docs/web/sandbox/>（Page updated: June 11, 2026）・<https://kiro.dev/docs/web/sandbox/internet-access/>（Page updated: April 21, 2026）・<https://kiro.dev/docs/web/sandbox/environment-configuration/>（Page updated: July 23, 2026）・<https://kiro.dev/docs/web/sandbox/mcp/>（Page updated: June 18, 2026）

サンドボックスは、**エージェントがタスクを実行する隔離された環境**です。**タスクごとに専用のサンドボックス**が作られます。

---

## 📑 このページの内容

1. [動作の流れ（5段階）](#動作の流れ5段階)
2. [設定できる4項目](#設定できる4項目)
3. [ネットワークアクセスレベル（4種類）](#ネットワークアクセスレベル4-種類)
4. [環境の自動構成](#環境の自動構成)
5. [Powers と MCP サーバー](#powers-と-mcp-サーバー)
6. [サンドボックスの外側で動くもの](#サンドボックスの外側で動くもの)

---

## 動作の流れ（5段階）

公式は、タスクを割り当てたときのエージェントの動作を5段階で説明しています。

| # | 段階 |
|---|------|
| 1 | **隔離されたサンドボックス環境を起動する** |
| 2 | **認可されたリポジトリ**をサンドボックスにクローンする |
| 3 | **検出したプロジェクト設定に基づいて環境を構成する** |
| 4 | **明示的に許可されたリソースにのみアクセスして**タスクを実行する |
| 5 | **タスク完了時にサンドボックスを破棄する** |

設定は **Agent 設定ページの Sandbox** から行います。

| 項目 | 値 |
|------|---|
| **ディスク容量** | **128GB**（[04_reference/04_limits.md](../04_reference/04_limits.md#サンドボックスのディスク容量)） |
| CPU・メモリ | **未確認**（公式に記載が見つかりませんでした） |

> ディスク容量は**公式ドキュメントではなく changelog にのみ**記載があり、
> しかも公式サイトで折りたたまれている項目の中にあります。

---

## 設定できる4項目

| 項目 | 内容 | 詳細 |
|------|------|------|
| **Internet Access** | エージェントが到達できるドメインの制御 | [下記](#ネットワークアクセスレベル4-種類) |
| **Powers and MCP** | Powers のインストール・カスタム MCP サーバーの設定 | [04_reference/03_mcp-configuration.md](../04_reference/03_mcp-configuration.md) |
| **Environment Variables** | タスク実行用の環境変数とシークレット | [04_reference/02_environment-variables.md](../04_reference/02_environment-variables.md) |
| **Environment Configuration** | プロジェクト向けのサンドボックス環境の構成（IAM ロールを含む） | [下記](#環境の自動構成) |

---

## ネットワークアクセスレベル（4 種類）

**出典**: <https://kiro.dev/docs/web/sandbox/internet-access/>

タスク実行中にエージェントがアクセスできるドメインを制御します。**3つのレベルとカスタム許可リスト**があります。

| レベル | 到達できる範囲 |
|-------|------------|
| **Connections access only** | **サンドボックスが機能するための最小限**。GitHub リポジトリのクローン・PR の作成と更新・ゲートウェイサービス経由の GitHub アクセス |
| **Common dependencies** | 上記 ＋ **主要なパッケージレジストリと開発ツール（73 ドメイン）** |
| **Open internet** | **制限なし** |
| **Custom allow-list** | **カンマ区切りで自分で指定** |

### Connections access only が最も安全です

公式は次のように説明しています。

> This is the most secure option and recommended when your tasks don't require external dependencies.

**外部の依存関係が不要なタスクではこれが推奨**です。

### Common dependencies

公式は「allows the agent to install dependencies from popular package managers **without requiring full internet access**」と説明しています。**フルのインターネットアクセスなしに**依存関係をインストールできます。

自動的に許可される **73 ドメイン**の一覧は [04_reference/01_allowed-domains.md](../04_reference/01_allowed-domains.md#2-サンドボックスの依存関係取得先73-ドメイン) にあります。

### ⚠️ Open internet のリスク（公式の警告）

公式は次のように警告しています。

> Enabling network permissions exposes your environment to security risks. These include **prompt injection attacks**, **extraction of code and secrets**, **introduction of malware or security flaws**, and **use of content that may violate licensing terms**. Consider these risks carefully before enabling network permissions.

| 公式が挙げるリスク |
|--------------|
| **プロンプトインジェクション攻撃** |
| **コードとシークレットの抽出** |
| **マルウェアやセキュリティ上の欠陥の導入** |
| **ライセンス条項に違反する可能性のあるコンテンツの利用** |

> この警告は「Open internet」に限らず、**ネットワーク権限を有効にすること全般**についてのものです。

### カスタム許可リストの書式

| 記述 | 意味 |
|------|------|
| `api.example.com` | **この特定のドメインのみ** |
| `.example.com` | `example.com` **と全サブドメイン** |
| `api.example.com, .cdn.example.com` | 複数指定 |

> **先頭のドットの有無で意味が変わります。** 詳細は
> [04_reference/01_allowed-domains.md](../04_reference/01_allowed-domains.md#カスタム許可リストの書式) を参照してください。

---

## 環境の自動構成

**出典**: <https://kiro.dev/docs/web/sandbox/environment-configuration/>（Page updated: July 23, 2026 — **Kiro Web の docs で最も新しい更新**）

公式は、エージェントが**プロジェクトの種類を検出して自動的にサンドボックスを構成する**と説明しています。判断材料はリポジトリの構成ファイルです。

| 公式が挙げる例 |
|------------|
| `package.json` |
| `requirements.txt` |
| ビルドマニフェスト |

**手動セットアップなしで環境がプロジェクトの要件に合う**とされています。

### AWS API を呼ぶ場合（IAM ロール）

サンドボックス内のエージェントや MCP サーバーが AWS API を呼ぶ必要がある場合、**Kiro Web が代わりに引き受ける IAM ロール**を設定できます。**短期間だけ有効な認証情報**がサンドボックスに渡され、タスク完了時に削除されます。

設定手順と信頼ポリシーは [04_reference/02_environment-variables.md](../04_reference/02_environment-variables.md#iam-ロールaws-api-の呼び出し) を参照してください。

---

## Powers と MCP サーバー

**出典**: <https://kiro.dev/docs/web/sandbox/mcp/>

エージェントにツールとコンテキストを追加する方法が2種類あります。

| 方式 | 内容 |
|------|------|
| **Powers** | **Kiro Web に同梱されている統合群**。**Settings > Agent > Sandbox > Manage powers** で管理 |
| **MCP servers** | **Model Context Protocol** を使ったカスタム統合。**手動で設定**し、各タスクの開始時にサンドボックスに読み込まれる |

| 項目 | 対応状況 |
|------|---------|
| **ローカル MCP サーバー** | ✅ 対応 |
| **リモート MCP サーバー** | ❌ **現時点では利用できません** |

設定方法・OAuth 認可・セキュリティ警告は [04_reference/03_mcp-configuration.md](../04_reference/03_mcp-configuration.md) を参照してください。

---

## サンドボックスの外側で動くもの

**「サンドボックスがあるから安全」ではありません。** 公式が明記している例外があります。

### ⚠️ MCP サーバーはサンドボックスの制限を受けません

公式は次のように明記しています。

> MCP servers run **outside the agent's tool-execution sandbox** — they are not subject to the same restrictions as agent tool calls

| 項目 | 内容 |
|------|------|
| MCP サーバーの実行場所 | **エージェントのツール実行サンドボックスの外側** |
| 受ける制限 | **エージェントのツール呼び出しと同じ制限は受けません** |
| アクセスできるもの | ワークスペースのファイルシステム全体・**環境変数とシークレット** |

詳細は [04_reference/03_mcp-configuration.md](../04_reference/03_mcp-configuration.md#mcp-security-warning) を参照してください。

### ⚠️ シークレットは持ち出されうる前提で扱ってください

公式は、エージェントが**コードの変更・ログ・外部へのリクエスト**を通じてシークレットを持ち出しうると明記しています。

詳細は [04_reference/02_environment-variables.md](../04_reference/02_environment-variables.md#secrets-exfiltration-warning) を参照してください。

### ⚠️ リポジトリのコード内の指示にエージェントは従います

公式は繰り返し次の警告を出しています。

> The agent learns from and follows instructions in the repository code, even if those instructions are malicious.

**信頼できるリポジトリだけを選んでください。特に公開リポジトリと非公開リポジトリを混在させるときは注意が必要です。**

> サンドボックスはリソースへのアクセスを制限しますが、**プロンプトインジェクションを防ぐものではありません。**
> 公式が Open internet の警告でプロンプトインジェクションを挙げているのはこのためです。

---

## 🔗 関連ページ

- [01_agent-modes.md](01_agent-modes.md) — タスクの実行モード
- [03_automations.md](03_automations.md) — Automations（実行ごとに独立したサンドボックス）
- [04_reference/01_allowed-domains.md](../04_reference/01_allowed-domains.md) — 許可ドメインの一覧（73 ドメイン）
- [04_reference/02_environment-variables.md](../04_reference/02_environment-variables.md) — 環境変数・シークレット・IAM ロール
- [04_reference/03_mcp-configuration.md](../04_reference/03_mcp-configuration.md) — MCP 設定と Powers
- [04_reference/04_limits.md](../04_reference/04_limits.md) — ディスク容量ほかの値
- 公式: <https://kiro.dev/docs/web/sandbox/>

---

[← 01_features に戻る](README.md)
