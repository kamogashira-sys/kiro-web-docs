# ファイルエクスプローラ（セッションのワークスペースを見る）

> **本ページは Kiro Web 版（<https://app.kiro.dev>）の仕様です。**
> Kiro IDE / Kiro CLI とは別製品です。**Kiro Web は [2026-09-01 に一般提供（GA）になりました](https://kiro.dev/changelog/web/kiro-web-is-now-generally-available/)。**

**出典**: <https://kiro.dev/docs/web/using-the-agent/file-explorer/>（Page updated: August 22, 2026）

---

## 📑 このページの内容

1. [何ができるか](#何ができるか)
2. [会話からファイルを開く](#会話からファイルを開く)
3. [ワークスペースを見る（2つのタブ）](#ワークスペースを見る2つのタブ)
4. [表示とダウンロード](#表示とダウンロード)
5. [制限](#制限)

---

## 何ができるか

公式は次のように説明しています。

> Every Kiro Web session runs in an isolated sandbox with its own workspace. The file explorer lets you look at that workspace directly: browse the file tree, open any file the agent creates or edits, and download files to your machine — without asking the agent to print them.

**Kiro Web のすべてのセッションは、独自のワークスペースを持つ隔離されたサンドボックスで動きます。**
ファイルエクスプローラはそのワークスペースを**直接見る**ためのものです。

| できること |
|-----------|
| **ファイルツリーを辿る** |
| **エージェントが作成・編集したファイルを開く** |
| **ファイルを自分のマシンにダウンロードする** |

**エージェントに「中身を出力して」と頼まなくても済みます**（`without asking the agent to print them`）。

サンドボックスそのものについては [05_sandbox.md](05_sandbox.md) を参照してください。

---

## 会話からファイルを開く

公式は次のように説明しています。

> When the agent references a workspace file by its full sandbox path, the path renders as a link in prose and inline code. Select it to open the file explorer with that file loaded — the fastest way to jump from a mention to the actual contents. Paths inside fenced code blocks aren't linked, and a trailing line number (like `:42`) is shown but not jumped to.

| 項目 | 動作 |
|------|------|
| リンクになる条件 | エージェントが**サンドボックスのフルパス**でワークスペースのファイルを参照したとき |
| リンクになる場所 | **本文（prose）とインラインコード** |
| 選ぶとどうなるか | **そのファイルを読み込んだ状態でファイルエクスプローラが開く** |
| **リンクにならない場所** | **フェンスコードブロックの中のパス** |
| 末尾の行番号（`:42` のような表記） | **表示はされるが、その行へは飛ばない** |

---

## ワークスペースを見る（2つのタブ）

公式は「The file explorer panel has two tabs」と説明しています。

| タブ | 内容 |
|------|------|
| **Files** | **セッションのワークスペースのルート**。展開できるツリーとして表示される。**フォルダは展開したときに中身を読み込む** |
| **Artifacts** | エージェントが**セッションのアーティファクトとして生成したファイル** |

> Right-click a file in the tree and choose **Copy file path** to copy its path. You can collapse the tree to give the file viewer the full panel width.

| 操作 | 方法 |
|------|------|
| パスをコピーする | ツリーでファイルを**右クリック**して **`Copy file path`** を選ぶ |
| ビューアを広くする | **ツリーを折りたたむ**（ビューアがパネル幅全体を使う） |

---

## 表示とダウンロード

公式は「Selecting a file opens it in the viewer」と説明しています。

| ファイル種別 | ビューアでの表示 |
|-----------|--------------|
| **コード・テキスト** | **シンタックスハイライトと行番号**付きで表示される |
| **Markdown** | **レンダリング済みのプレビュー**で開く。**`View source`** に切り替えると生の Markdown を見られる |
| **画像** | **インラインでプレビュー**される |
| **その他のバイナリ** | **プレビューできない**が、**ダウンロードはできる** |

> Use the download button in the viewer header to save the open file to your machine. The viewer refreshes periodically while the agent works, so a file you're watching reflects the agent's latest edits.

| 項目 | 内容 |
|------|------|
| ダウンロード | ビューアのヘッダにある**ダウンロードボタン**で、開いているファイルを自分のマシンに保存する |
| 自動更新 | **エージェントが作業している間、ビューアは定期的に更新される**ため、見ているファイルは**エージェントの最新の編集を反映する** |

---

## 制限

公式が「Limits」として挙げている項目です。

| # | 制限 | 回避策（公式の記述） |
|---|------|----------------|
| 1 | **非常に大きいファイルはビューアで切り詰められる**。**切り詰められた画像とバイナリはプレビューもダウンロードもできない** | エージェントに**もっと小さい版を作らせる**か、**ファイルをリポジトリに push する** |
| 2 | ツリーに**検索も隠しファイルの表示切り替えも「まだ」ない**（`yet`） | **必要なファイルまで展開する**か、**会話中のファイルリンクから開く** |
| 3 | **ダウンロードは1つずつ**。**ワークスペース全体のダウンロードは無い** | — |
| 4 | エクスプローラが見せるのは**セッションのサンドボックスのワークスペース**で、**自分のローカルマシンではない** | セッションから変更を持ち出すには、**エージェントにプルリクエストを作らせる**か、**個々のファイルをダウンロードする** |

> ⚠️ 制限2の「まだ（`yet`）」は**公式の表現**です。今後の追加が予告されているわけではありません
> （公式に予定の記載はないため**未確認**）。

---

## 🔗 関連ページ

公式が「Related」として挙げているページです。

| 公式の項目 | 本サイトの該当ページ |
|-----------|-----------------|
| Cloud sessions - where the session workspace lives | [07_cloud-sessions.md](07_cloud-sessions.md) |
| Sandbox - the isolated environment behind every session | [05_sandbox.md](05_sandbox.md) |
| Working with the agent - the full Kiro Web experience | [01_agent-modes.md](01_agent-modes.md) |

- [06_repository-integration.md](06_repository-integration.md) — プルリクエストで変更を持ち出す
- [../04_reference/04_limits.md](../04_reference/04_limits.md) — 上限値の一覧
