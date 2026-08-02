# MCP 設定と Powers

> **本ページは Kiro Web 版（<https://app.kiro.dev>）の仕様です。**
> Kiro IDE / Kiro CLI とは別製品です。**Kiro Web は Preview 段階**です。

**出典**: <https://kiro.dev/docs/web/sandbox/mcp/>（Page updated: June 18, 2026）

> ⚠️ **本ページの設定例はすべて公式ページの HTML 版から取っています。**
> このページの `.md` 版は **`${key_name}` が裸の `` `$` `` に潰れており**、設定の書き方が
> 読み取れません（`.md` 版に `${key_name}` は 1 つも残っていません）。
> 詳細は [00_information/02_information-sources.md](../00_information/02_information-sources.md#a-プレースホルダが潰れる2ページ) を参照してください。

---

## 📑 このページの内容

1. [Powers と MCP サーバーの違い](#powers-と-mcp-サーバーの違い)
2. [⚠️ MCP サーバーはサンドボックスの制限を受けません（公式の警告）](#mcp-security-warning)
3. [MCP サーバーの設定](#mcp-サーバーの設定)
4. [対応しているサーバーの種類](#対応しているサーバーの種類)
5. [環境変数・シークレットの参照](#環境変数シークレットの参照)
6. [Power の認可（OAuth）](#power-の認可oauth)

---

## Powers と MCP サーバーの違い

公式は、エージェントにツールとコンテキストを追加する方法が**2種類**あると説明しています。

| 方式 | 内容（公式の説明） | 設定 |
|------|----------------|------|
| **Powers** | **Kiro Web に同梱されている統合群**。専門的なツールとコンテキストをエージェントに追加する | セッションで有効にする Powers を選ぶ。**Settings > Agent タブ > Sandbox > Manage powers** |
| **MCP servers** | **Model Context Protocol** を使ったカスタムツール統合。**完全に制御できる** | **手動で設定**し、各タスクの開始時にサンドボックスに読み込まれる |

> **Powers は Kiro Web に固有の概念**です。Kiro IDE / Kiro CLI の MCP 設定とは別扱いにしてください。

---

<a id="mcp-security-warning"></a>
## ⚠️ MCP サーバーはサンドボックスの制限を受けません（公式の警告）

公式はセキュリティ警告として次のように明記しています。

> MCP stdio servers execute arbitrary commands inside your environment with the same privileges and access as the agent itself. This includes access to your source code, environment variables, secrets, and any credentials available in the session.

**MCP stdio サーバーは、エージェント自身と同じ権限・同じアクセス範囲で、環境内で任意のコマンドを実行します。**

### MCP サーバーを追加する前に理解しておくこと（公式の5項目）

| # | 内容 |
|---|------|
| 1 | 設定した **command と args は環境内のプロセスとして動作する** — インストールする実行ファイルと同じ慎重さで扱うこと |
| 2 | MCP サーバーは**ワークスペースのファイルシステムに完全にアクセスできる**（ソースコード・設定ファイルを含む） |
| 3 | MCP サーバーは**セッションに設定された環境変数とシークレットを読める** |
| 4 | **MCP サーバーはエージェントのツール実行サンドボックスの外側で動作する** — **エージェントのツール呼び出しと同じ制限は受けない** |
| 5 | 侵害された、または悪意ある MCP サーバーは、**追加のユーザー確認なしに**コード・資格情報・データを持ち出せる |

### 公式が求めていること

> Only install MCP servers from sources you trust and have reviewed. You are responsible for evaluating the security of any MCP server you configure. Kiro does not vet, sandbox, or restrict the behavior of third-party MCP servers.

| 項目 | 内容 |
|------|------|
| インストール元 | **信頼でき、かつ自分でレビューしたもののみ** |
| セキュリティ評価の責任 | **利用者** |
| Kiro 側の関与 | **サードパーティ MCP サーバーの審査・サンドボックス化・挙動の制限をしません** |

> **項目4が特に重要です。** 「サンドボックスがあるから安全」ではありません。
> MCP サーバーは**サンドボックスの外**で動き、シークレットも読めます
> （[02_environment-variables.md](02_environment-variables.md#secrets-exfiltration-warning)）。

公式は追加の指針として `docs/cli/mcp/security` にリンクしています。**これは Kiro CLI 版のページ（別製品のドキュメント）**ですが、公式が Web のページから参照しているものです。

---

## MCP サーバーの設定

### 追加手順

1. **Settings** に移動し **Agent** タブを選ぶ
2. **MCP server settings** の下の **Add server** をクリック
3. **サーバー名**・**種類（HTTP または local）**・**コマンドまたは URL** を入力する

### 読み込みのタイミング

公式は次のように説明しています。

> MCP servers are loaded when the sandbox starts and remain available throughout task execution.

**サンドボックスの起動時に読み込まれ、タスク実行中は利用可能な状態が続きます。**

### 設定例（公式の記述をそのまま転記）

```json
{
  "mcpServers": {
    "aws-knowledge-mcp-server": {
      "command": "uvx",
      "args": [
        "fastmcp",
        "run",
        "https://knowledge-mcp.global.api.aws"
      ],
      "env": {}
    }
  }
}
```

| キー | 内容 |
|------|------|
| `mcpServers` | サーバー定義のマップ（キーがサーバー名） |
| `command` | 実行するコマンド |
| `args` | コマンドの引数（配列） |
| `env` | 環境変数のマップ（[参照構文](#環境変数シークレットの参照)が使える） |

---

## 対応しているサーバーの種類

公式は次のように明記しています。

> Only local MCP servers are currently supported. Remote MCP servers are not available at this time.

| 種類 | 対応状況 |
|------|---------|
| **ローカル MCP サーバー** | ✅ 対応 |
| **リモート MCP サーバー** | ❌ **現時点では利用できません** |

> 設定画面では種類として「HTTP または local」を選べますが、公式ページの
> 「Supported servers」節は**ローカルのみ対応**と明記しています。
> この2つの記述の関係について公式の説明はないため**未確認**です。
> リモートサーバーを前提にした構成は組めないものとして扱ってください。

---

## 環境変数・シークレットの参照

MCP の設定から環境変数とシークレットを参照して、資格情報や設定値を安全に渡せます。

公式の記述（HTML 版）:

> Use the `${key_name}` syntax to reference the key names of your environment variables and secrets in the server configuration

### 公式の設定例

```json
{
  "mcpServers": {
    "server-name": {
      "command": "executable",
      "args": ["arg1", "arg2"],
      "env": {
        "ENV_VAR_KEY": "${my_env_var_key}",
        "SECRET_KEY": "${my_secret_key}"
      }
    }
  }
}
```

| 項目 | 内容 |
|------|------|
| 記法 | **`${キー名}`** |
| 環境変数とシークレット | **同じ記法**（公式明記） |
| 値の解決タイミング | **サンドボックスの起動時** |

環境変数・シークレット自体の設定と優先順位は [02_environment-variables.md](02_environment-variables.md) を参照してください。

---

## Power の認可（OAuth）

一部の Powers は、**Figma・Stripe・Supabase** などのサードパーティサービスに接続するため、**OAuth による認可**が必要です。

> この仕組みは [2026-07-01 のエントリ](../02_update/01_changelog.md#2026-07-01-iam-roles-and-authorize-powers-for-third-party-services)で追加されました。

### 認可は一度だけです

公式は次のように説明しています。

> You complete this once when you install the Power, and the agent uses the connection for all future tasks without prompting you again.

**Power のインストール時に一度完了させれば、以降のタスクでは再確認なしに接続が使われます。**

### 認可が必要かどうかの見分け方

| 状態 | 表示 |
|------|------|
| OAuth が必要な Power | Powers 一覧で**その Power の隣に `Authorize` ボタンが表示される** |
| 認可が不要な Power | **インストール直後から使える** |

### 認可の手順

1. **Settings** → **Agent** タブ
2. **Sandbox** の下の **Manage Powers** を選ぶ
3. 接続したい Power を見つけて **Authorize** を選ぶ
4. **新しいブラウザタブ**が開き、サービスの同意画面が表示される
5. 要求されている権限を確認して承認する
6. Kiro Web にリダイレクトされ、**その Power が接続済みと表示される**

認可後は、**どのタスクでもその Power の MCP サーバーが使えます**。接続を解除するか、サービス側がアクセスを取り消すまで、再認可は不要です。

### 接続の解除

1. Agent 設定の **Manage Powers** に移動する
2. 対象の Power を見つけて **Disconnect** を選ぶ

| 項目 | 内容 |
|------|------|
| 解除の効果 | **保存されている資格情報が即座に取り消される** |
| Power 自体 | **インストールされたまま**残る |
| ツールの動作 | 接続を必要とするツールは、**再認可するまで動作しなくなる** |

### トークンの保護（公式の記述）

[2026-07-01 のエントリ](../02_update/01_changelog.md#2026-07-01-iam-roles-and-authorize-powers-for-third-party-services)で公式は次のように説明しています。

> Tokens are encrypted at rest and never exposed to the sandbox or the agent.

| 項目 | 内容 |
|------|------|
| トークンの保存 | **保存時に暗号化** |
| サンドボックス・エージェントへの露出 | **されません** |

> シークレット（[02_environment-variables.md](02_environment-variables.md)）は
> **サンドボックス内で環境変数として見える**のに対し、**Power の OAuth トークンは
> サンドボックスにもエージェントにも渡されません**。扱いが違う点に注意してください。

---

## 🔗 関連ページ

- [02_environment-variables.md](02_environment-variables.md) — 環境変数・シークレット・IAM ロール
- [01_allowed-domains.md](01_allowed-domains.md) — サンドボックスのネットワークアクセス
- [01_features/05_sandbox.md](../01_features/05_sandbox.md) — サンドボックスの仕組み
- 公式: <https://kiro.dev/docs/web/sandbox/mcp/>

---

[← 04_reference に戻る](README.md)
