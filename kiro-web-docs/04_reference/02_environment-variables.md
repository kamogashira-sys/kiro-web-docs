# 環境変数・シークレット・IAM ロール

> **本ページは Kiro Web 版（<https://app.kiro.dev>）の仕様です。**
> Kiro IDE / Kiro CLI とは別製品です。**Kiro Web は Preview 段階**です。

**出典**: <https://kiro.dev/docs/web/sandbox/environment-variables/>（Page updated: April 21, 2026）・<https://kiro.dev/docs/web/sandbox/environment-configuration/>（Page updated: July 23, 2026）

> ⚠️ **本ページの記法・ポリシーはすべて公式ページの HTML 版から取っています。**
> 出典の2ページは `.md` 版で **`${...}` が裸の `` `$` `` に潰れます**
> （`${aws:SourceIdentity}` が `.md` では判別不能）。
> 詳細は [00_information/02_information-sources.md](../00_information/02_information-sources.md#a-プレースホルダが潰れる2ページ) を参照してください。

---

## 📑 このページの内容

1. [環境変数とシークレット](#環境変数とシークレット)
2. [参照構文 `${key_name}`](#参照構文-key_name)
3. [同じキーが両方にある場合](#同じキーが両方にある場合)
4. [サンドボックスの環境構成](#サンドボックスの環境構成)
5. [IAM ロール（AWS API の呼び出し）](#iam-ロールaws-api-の呼び出し)
6. [信頼ポリシー](#信頼ポリシー)

---

## 環境変数とシークレット

サンドボックスに値を渡す方法が2種類あります。

| 種類 | 用途（公式の説明） | 暗号化 |
|------|----------------|-------|
| **Environment Variables** | タスク実行中にエージェントが使える変数。**機密でない**設定値に使う | — |
| **Secrets** | 機密の資格情報や API キー。サンドボックスで**環境変数として公開される** | **保存時に暗号化** |

設定場所は **Settings > Agent タブ > Sandbox** です。

<a id="secrets-exfiltration-warning"></a>
### ⚠️ シークレットは持ち出されうる前提で扱ってください（公式の警告）

公式は次のように明記しています。

> The agent may exfiltrate these secrets through code changes, logs, or external requests, so only provide secrets necessary for the task and only use the agent with repositories you trust.

| リスク | 公式が挙げる経路 |
|-------|--------------|
| シークレットの持ち出し | **コードの変更**・**ログ**・**外部へのリクエスト** |

**対処として公式が求めていること**:

1. **タスクに必要なシークレットだけを設定する**
2. **信頼できるリポジトリでのみエージェントを使う**

> 「暗号化されている」のは**保存時**です。**タスク実行中はサンドボックス内で環境変数として
> 見える状態**になり、エージェントも MCP サーバーも読めます
> （[03_mcp-configuration.md](03_mcp-configuration.md#mcp-security-warning)）。

---

## 参照構文 `${key_name}`

MCP サーバーの設定などから環境変数・シークレットを参照するときは、**`${key_name}` 形式**を使います。

公式の記述（HTML 版）:

> Use the `${key_name}` syntax to reference the key names of your environment variables and secrets in the server configuration

### 使用例（公式の設定例）

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
| 環境変数とシークレットの書き分け | **同じ記法**（公式: "Both environment variables and secrets use the same syntax"） |
| 値が解決されるタイミング | **サンドボックスの起動時**（公式: "The values are resolved when the sandbox starts"） |

> ⚠️ **公式ドキュメントの `.md` 版ではこの記法が読み取れません。** `.md` 版は
> 「Use the **`$`** syntax」となっており、`${key_name}` が 1 つも残っていません。
> 本ページは HTML 版から取っています。

---

## 同じキーが両方にある場合

公式は次のように明記しています。

> If the same key exists in both environment variables and secrets, the environment variable value takes precedence.

| 条件 | 優先されるもの |
|------|------------|
| 同じキー名が **Environment Variables と Secrets の両方**にある | **Environment Variables の値** |

> シークレット側が勝つと思い込むと、意図せず機密でない値が使われます。**環境変数が優先**です。

---

## サンドボックスの環境構成

**出典**: <https://kiro.dev/docs/web/sandbox/environment-configuration/>（Page updated: July 23, 2026）

> このページは **Kiro Web の docs で最も新しい更新**です（2026-08-01 時点）。

### 自動構成

公式は、エージェントが**プロジェクトの種類を検出して自動的にサンドボックスを構成する**と説明しています。判断に使うのはリポジトリの構成ファイルです。

| 公式が挙げる例 |
|------------|
| `package.json` |
| `requirements.txt` |
| ビルドマニフェスト |

**手動セットアップなしで環境がプロジェクトの要件に合う**とされています。

### 手動構成

**Agent 設定ページの Sandbox** から変更できる項目です。

| 項目 | 内容 | 本サイトの該当ページ |
|------|------|------------------|
| **Environment variables** | タスク実行用の変数とシークレット | 本ページ |
| **Internet access** | エージェントが到達できるドメインの制御 | [01_allowed-domains.md](01_allowed-domains.md#2-サンドボックスの依存関係取得先73-ドメイン) |
| **Powers and MCP** | Powers のインストール・カスタム MCP サーバーの設定 | [03_mcp-configuration.md](03_mcp-configuration.md) |

---

## IAM ロール（AWS API の呼び出し）

サンドボックス内のエージェントや MCP サーバーが **AWS API を呼ぶ**必要がある場合（インフラのデプロイ・CloudWatch ログの照会・アカウント内リソースの管理など）、**Kiro Web が代わりに引き受ける IAM ロール**を設定できます。

> この機能は [2026-07-01 のエントリ](../02_update/01_changelog.md#2026-07-01-iam-roles-and-authorize-powers-for-third-party-services)で追加されました。

### 資格情報の受け渡し（公式の説明）

| 項目 | 内容 |
|------|------|
| タスク実行時 | Kiro Web が**ロールを引き受け**、**短期間だけ有効な認証情報**をサンドボックスに渡す |
| 使えるもの | **エージェント・CLI ツール・サンドボックス内で動く MCP サーバーのすべて** |
| 更新 | タスク実行中に**自動更新**される |
| 削除 | **タスク完了時に削除**される |

### 設定手順

1. **下記の信頼ポリシー**を持つ IAM ロールを AWS アカウントに作成する
2. **Settings** → **Agent** タブ
3. **Sandbox** の下の **IAM Role** を選ぶ
4. 作成した IAM ロールの **ARN** を入力する

### 保存時に検証されます

公式は次のように説明しています。

> Kiro Web validates the role when you save. If the role cannot be assumed — for example, because the trust policy is missing or the ARN is incorrect — you'll see an error and the configuration won't be saved.

**ロールを引き受けられない場合（信頼ポリシーが無い・ARN が誤っている等）はエラーになり、設定は保存されません。**

---

## 信頼ポリシー

### 必要な権限

公式は、Kiro Web がロールを引き受けるために、信頼ポリシーが **`q.amazonaws.com` サービスプリンシパル**に対して次の権限を許可する必要があると説明しています。

| 必要なアクション |
|--------------|
| `sts:AssumeRole` |
| `sts:SetSourceIdentity` |
| `sts:TagSession` |

### source identity の役割（公式の説明）

> The source identity is your Kiro user ID, which ensures that only your Kiro account can assume the role and provides an immutable audit trail in CloudTrail.

| 項目 | 内容 |
|------|------|
| source identity の値 | **自分の Kiro ユーザー ID** |
| 効果1 | **自分の Kiro アカウントだけ**がロールを引き受けられる |
| 効果2 | **CloudTrail に変更不可能な監査証跡**が残る |

### 公式の信頼ポリシー（HTML 版から転記）

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "Service": "q.amazonaws.com"
            },
            "Action": [
                "sts:AssumeRole",
                "sts:SetSourceIdentity"
            ],
            "Condition": {
                "StringEquals": {
                    "sts:SourceIdentity": "<your-kiro-userId>"
                }
            }
        },
        {
            "Effect": "Allow",
            "Principal": {
                "Service": "q.amazonaws.com"
            },
            "Action": "sts:TagSession",
            "Condition": {
                "ForAllValues:StringEquals": {
                    "aws:TagKeys": [
                        "GroupIds",
                        "KiroSessionId"
                    ]
                }
            }
        }
    ]
}
```

### 置き換える値

| プレースホルダ | 置き換える値 | 取得方法（公式の説明） |
|--------------|-----------|------------------|
| `<your-kiro-userId>` | 実際の Kiro ユーザー ID | **IAM Role 設定のドロワーに表示**されます（コピーボタン付きで、ポリシーに直接貼り付けられます） |

### セッションタグ

`sts:TagSession` の条件では、許可されるタグキーが2つに限定されています。

| 許可されるタグキー |
|--------------|
| `GroupIds` |
| `KiroSessionId` |

> ⚠️ **公式ドキュメントの `.md` 版では `${aws:SourceIdentity}` などの記述が
> 裸の `` `$` `` に潰れます。** 上記のポリシーは HTML 版から転記しています。
> 貼り付ける前に公式ページ（HTML）でも確認してください。

---

## 🔗 関連ページ

- [03_mcp-configuration.md](03_mcp-configuration.md) — MCP 設定（環境変数・シークレットの参照先）
- [01_allowed-domains.md](01_allowed-domains.md) — サンドボックスのネットワークアクセス
- [01_features/05_sandbox.md](../01_features/05_sandbox.md) — サンドボックスの仕組み
- [02_update/01_changelog.md](../02_update/01_changelog.md#2026-07-01-iam-roles-and-authorize-powers-for-third-party-services) — IAM ロール追加時のエントリ
- 公式: <https://kiro.dev/docs/web/sandbox/environment-variables/>・<https://kiro.dev/docs/web/sandbox/environment-configuration/>

---

[← 04_reference に戻る](README.md)
