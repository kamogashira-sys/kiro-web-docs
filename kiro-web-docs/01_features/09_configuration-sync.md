# Configuration Sync（個人設定をクラウドへ同期する）

> **本ページは Kiro Web 版（<https://app.kiro.dev>）の仕様です。**
> Kiro IDE / Kiro CLI とは別製品です。**Kiro Web は [2026-09-01 に一般提供（GA）になりました](https://kiro.dev/changelog/web/kiro-web-is-now-generally-available/)。**

**出典**: <https://kiro.dev/docs/web/cloud-configuration/>（Page updated: September 2, 2026）

---

## 📑 このページの内容

1. [何を解決する機能か](#何を解決する機能か)
2. [アップロードできる6つのフォルダ](#アップロードできる6つのフォルダ)
3. [除外されるもの](#除外されるもの)
4. [⚠️ `mcp.json` は `env` の値が平文で上がります](#-mcpjson-は-env-の値が平文で上がります)
5. [アップロードの手順](#アップロードの手順)
6. [6つのステータス](#6つのステータス)
7. [Powers の同期は2経路](#powers-の同期は2経路)
8. [ローカルセッションにも適用する](#ローカルセッションにも適用する)
9. [上限](#上限)
10. [アップロードした後](#アップロードした後)

---

## 何を解決する機能か

公式は次のように説明しています。

> Kiro IDE and Kiro CLI read your personal configuration from the local `~/.kiro` directory. Cloud sessions run in a managed sandbox that cannot access your machine, so that directory does not apply there automatically. Configuration Sync closes the gap: upload supported folders from your local `.kiro` directory to Kiro Web, and the agent uses the cloud copy in every cloud session. You can also apply the cloud copy to new local IDE and CLI sessions.

| | 内容 |
|---|---|
| 前提 | Kiro IDE と Kiro CLI は**ローカルの `~/.kiro`** から個人設定を読む |
| 問題 | Cloud Session は**利用者のマシンにアクセスできない**マネージドサンドボックスで動くため、**そのディレクトリは自動では効かない** |
| 解決 | ローカルの `.kiro` から**対応フォルダをアップロード**すると、**すべての Cloud Session でクラウド上の複製が使われる** |
| 追加 | クラウド上の複製を**新しいローカルの IDE / CLI セッションにも適用**できる |

**開始場所**: Kiro Web の設定を開き、サイドバーの **Configuration** の下にある **Sync** を選びます。

> Open Kiro Web settings and select **Sync** under **Configuration** in the sidebar to get started.

### 個人設定とプロジェクト設定は別です

公式は次のように説明しています。

> Configuration Sync covers your **personal** configuration. Project configuration committed under `.kiro/` in a repository already travels with the repository because the sandbox clones it.

| 設定の範囲 | クラウドへの届き方 |
|-----------|----------------|
| **個人設定** | **Configuration Sync でアップロードする**（本ページ） |
| **プロジェクト設定**（リポジトリに `.kiro/` としてコミットしたもの） | **リポジトリと一緒に運ばれる**（サンドボックスがクローンするため。アップロードは不要） |

---

## アップロードできる6つのフォルダ

公式は次のように説明しています。

> Upload one top-level folder from your local `.kiro` directory at a time. Six folders are supported:

**ローカルの `.kiro` 直下のフォルダを、1度に1つずつ**アップロードします。対応するのは**6つ**です。

| フォルダ | アップロードされるもの | クラウド側の管理場所 |
|---------|-------------------|----------------|
| `steering/` | Markdown の Steering ファイル | **Settings > Steering** |
| `agents/` | カスタムエージェントの定義と付随ファイル | **Settings > Agents** |
| `hooks/` | フックの定義ファイル | **Settings > Hooks** |
| `skills/` | `SKILL.md` と付随するテキストファイル | **Settings > Skills** |
| `powers/` | インストール済みの Powers（[後述](#powers-の同期は2経路)） | **Settings > Powers** |
| `settings/` | `mcp.json` の MCP サーバー | **Kiro Web サンドボックスの MCP サーバー設定** |

Steering の詳細は [04_steering.md](04_steering.md)、MCP の詳細は
[../04_reference/03_mcp-configuration.md](../04_reference/03_mcp-configuration.md) を参照してください。

---

## 除外されるもの

公式は次のように説明しています。

> Anything else at the root of `.kiro`, such as session state, caches, and runtime folders, is rejected. Within supported folders, Kiro filters machine-generated content such as `.git`, `node_modules`, and `.DS_Store`.

| 対象 | 扱い |
|------|------|
| `.kiro` 直下の**上記6つ以外**（セッション状態・キャッシュ・ランタイムのフォルダなど） | **拒否される** |
| 対応フォルダの**中**にあるマシン生成物（`.git`・`node_modules`・`.DS_Store` など） | **除外される** |

---

## ⚠️ `mcp.json` は `env` の値が平文で上がります

**公式が警告として明示している項目です。**

> An uploaded `mcp.json` includes literal values from each server's `env` object. Review the comparison before uploading. Prefer sandbox environment variables and secrets instead of storing credentials directly in `mcp.json`.

| 項目 | 内容 |
|------|------|
| 何が起きるか | アップロードした `mcp.json` には、**各サーバーの `env` オブジェクトの値がそのまま（literal values）含まれます** |
| すべきこと | **アップロード前に比較（comparison）を確認する** |
| 推奨 | **`mcp.json` に認証情報を直接持たせず**、サンドボックスの環境変数とシークレットを使う |

サンドボックスの環境変数とシークレットは
[../04_reference/02_environment-variables.md](../04_reference/02_environment-variables.md) を参照してください。

---

## アップロードの手順

公式が示す手順です。

| # | 手順 |
|---|------|
| 1 | Kiro Web で **Settings > Sync** を開く |
| 2 | 対応フォルダを**1つ**（例: `~/.kiro/steering`）アップロード領域に**ドラッグ**する。またはフォルダ選択で指定する |
| 3 | **各ファイルとそのステータスを確認**する。行を展開すると中身を確認できる |
| 4 | 同期するファイルを選び、**`Upload N files`** を選ぶ。**ファイルごとに進捗が表示され、失敗したファイルは再試行できる** |

---

## 6つのステータス

公式は「各ステータスはアップロードが何をするかを表す」と説明しています。

| ステータス | 意味 | 既定の選択 |
|-----------|------|----------|
| **New** | クラウドに存在しないファイル | **選択済み** |
| **Update** | クラウドに**内容が異なる**同名ファイルがある | **未選択**（オプトイン。**アップロードするとクラウド側を置き換えるため**）。Steering ファイルと MCP サーバーは**左右に並べた比較**が表示される |
| **Synced** | すでにクラウド側と一致している | **アップロードされない** |
| **Unsupported** | **クラウドの保存先が無い**カテゴリのファイル（例: バイナリの skill ファイル） | — |
| **Too large** | **1項目あたりのサイズ上限を超えている**。同期する前に小さくする必要がある | — |
| **Error** | **安全な操作を決められない**（例: **2つのローカルファイルが同じクラウド文書に対応する**）。ローカルで解消して再アップロードする | — |

---

## Powers の同期は2経路

公式は「Powers follow one of two paths」と説明しています。

| 経路 | 条件 | 動作 |
|------|------|------|
| **Catalog Powers** | Power の名前が**カタログの Power と完全一致**する | Kiro が**名前でインストール**し、**サービスが確認済みのファイル群を提供**する。アップロードの確認画面で操作対象になるのは **`POWER.md` のみ** |
| **Custom Powers** | カタログに無い | **個々のテキストファイルとしてアップロードされる** |

> ⚠️ **大文字小文字だけが違う名前は拒否されます。**
> カタログまたは Amazon 管理の Power と**大文字小文字の違いだけ**が異なる名前は**拒否されます**。
> カスタム Power として使うには**フォルダ名を変更**してください。

Powers と MCP の詳細は [05_sandbox.md](05_sandbox.md) を参照してください。

---

## ローカルセッションにも適用する

公式は次のように説明しています。

> Cloud configuration always applies to cloud sessions. You can also carry it into local work.

**クラウド設定は Cloud Session には常に適用されます。** ローカルの作業にも持ち込めます。

> On the Configuration Sync page, enable **Apply your cloud configuration to local sessions**. When a new local IDE or CLI session starts, Kiro loads your cloud Steering files, custom agents, Skills, Powers, and Hooks.

| 項目 | 内容 |
|------|------|
| 設定場所 | Configuration Sync のページで **`Apply your cloud configuration to local sessions`** を有効にする |
| いつ読まれるか | **新しいローカルの IDE / CLI セッションが開始したとき** |
| 何が読まれるか | クラウドの **Steering ファイル・カスタムエージェント・Skills・Powers・Hooks** |

> **このトグルはローカルの `.kiro` に書き込みません。**
>
> > The toggle does not write cloud content into your local `.kiro` directory or replace existing local files.
>
> **クラウドの内容をローカルの `.kiro` に書き込むことも、既存のローカルファイルを置き換えることもしません。**

---

## 上限

公式が「Limits」として挙げている項目です。数値は
[../04_reference/04_limits.md](../04_reference/04_limits.md#configuration-sync-の上限) にもまとめています。

| 項目 | 上限 |
|------|------|
| 一度にアップロードできるフォルダ | **対応する最上位フォルダを1つずつ** |
| 1項目あたりのサイズ | **4,000,000 バイト**（[04_limits.md](../04_reference/04_limits.md#configuration-sync-の上限)） |
| 1つの Skill に含められるファイル数 | **25 ファイル**（[04_limits.md](../04_reference/04_limits.md#configuration-sync-の上限)） |
| 1つのカスタム Power に含められるファイル数 | **50 ファイル**（[04_limits.md](../04_reference/04_limits.md#configuration-sync-の上限)） |
| Skills とカスタム Power のファイル形式 | **テキストファイルのみ** |
| `Update` を選んだときの動作 | **クラウド側を置き換える**。**ファイルの内容はマージされない** |

---

## アップロードした後

公式は次のように説明しています。

> Uploaded configuration appears on its feature-specific settings page, where supported items can be viewed, edited, downloaded, or deleted. It then applies automatically to cloud sessions alongside project configuration cloned with the repository.

アップロードした設定は**機能ごとの設定ページに現れ**、対応する項目は
**表示・編集・ダウンロード・削除**ができます。その後、
**リポジトリと一緒にクローンされたプロジェクト設定と並んで、Cloud Session に自動的に適用**されます。

### 同期は片方向です

> Uploading is local-to-cloud. Changes made in Kiro Web settings are not written back to your machine. Treat your local `.kiro` directory as the source of truth when you want to preserve the same configuration on disk, then upload again when it changes.

| 項目 | 内容 |
|------|------|
| 方向 | **ローカル → クラウド**の一方向 |
| Kiro Web 側で編集した内容 | **利用者のマシンには書き戻されません** |
| 同じ設定をディスク上に保ちたい場合 | **ローカルの `.kiro` を正（source of truth）として扱い**、変更したら**もう一度アップロードする** |

---

## 🔗 関連ページ

公式が「Related」として挙げているページです。

| 公式の項目 | 本サイトの該当ページ |
|-----------|-----------------|
| Cloud sessions - where uploaded configuration takes effect | [07_cloud-sessions.md](07_cloud-sessions.md) |
| Steering - writing Steering files | [04_steering.md](04_steering.md) |
| Powers and MCP - extending the cloud sandbox | [05_sandbox.md](05_sandbox.md) / [../04_reference/03_mcp-configuration.md](../04_reference/03_mcp-configuration.md) |

> **公式の Related には、本サイトが収録していないページも含まれます。**
> `Configuration scopes`（`/docs/configuration`・個人・プロジェクト・クラウドの設定がどう組み合わさるか）・
> `Custom agents`（`/docs/custom-agents`）・`Skills`（`/docs/skills`）・`Hooks`（`/docs/hooks`）は
> **`docs/web/` 配下ではない全製品共通ページ**で、
> 本サイトの収録範囲（`docs/web/` の 18 ページ＋移転先ページ）に**含まれていません**。

- [08_memory.md](08_memory.md) — エージェントが自動で学習する Memory との違い
- [../04_reference/04_limits.md](../04_reference/04_limits.md) — 上限値の一覧
