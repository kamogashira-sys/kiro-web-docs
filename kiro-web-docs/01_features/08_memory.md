# Memory（エージェントが学習すること）

> **本ページは Kiro Web 版（<https://app.kiro.dev>）の仕様です。**
> Kiro IDE / Kiro CLI とは別製品です。**Kiro Web は [2026-09-01 に一般提供（GA）になりました](https://kiro.dev/changelog/web/kiro-web-is-now-generally-available/)。**

**出典**: <https://kiro.dev/docs/memory/>（Page updated: October 24, 2026）

> ⚠️ **Memory のページは Web 専用から全製品共通へ移転し、Web の記述は「coming soon」になっています。**
> 旧 `docs/web/memory/`（`kiro.dev` 配下）は、現在は `https://kiro.dev/docs/memory/` へ転送されます
> （旧 URL の HTML は `noindex`・`meta refresh`・`canonical` で新 URL を指し、`docs/web/memory.md` は `# Moved` と新 URL を返します）。
> 新しいページ（IDE / CLI / Web の 3 タブ構成）は、**Web タブの 3 か所すべてが「Memory support coming soon.」**です。
> 移転の理由と、Kiro Web の Memory が現在どう動くかは、公式に記載がなく**未確認**です。

---

## 📑 このページの内容

1. [現行の公式ページが Web について書いていること](#現行の公式ページが-web-について書いていること)
2. [Memory とは（全製品共通の説明）](#memory-とは全製品共通の説明)
3. [移転前の Web 専用ページの記述](#移転前の-web-専用ページの記述)
4. [Memory と Steering の違い（移転前の記述）](#memory-と-steering-の違い移転前の記述)

---

## 現行の公式ページが Web について書いていること

`docs/memory/` は、操作の説明を **IDE / CLI / Web** のタブで分けています。Web タブの記述は次のとおりです。

| 節 | Web タブの記述（公式） |
|----|----------------------|
| Control learning and recall（学習と想起の制御） | `Memory support coming soon.` |
| Review what Kiro remembers（記憶内容の確認） | `Memory support coming soon.` |
| See Memory in a session（セッション内での表示） | `Memory support coming soon.` |

| 項目 | 内容 |
|------|------|
| Web での設定・確認・表示の方法 | **公式に記載なし**（上記の「coming soon」のみ） |
| Web で Memory が動いているか | **未確認** |
| 旧ページが書いていた「Settings の Memory セクション」が現行の画面にあるか | **未確認** |

> 公式 <https://kiro.dev/docs/web/>（Page updated: October 23, 2026）の機能一覧には、移転前にあった「Memory — See what the agent learns from your work over time」の項目が**ありません**。
> 本サイトが収録している他の Web docs（16 ページ）と、全製品共通の Cloud sessions・Steering・Specs のページにも、Memory を説明する本文は**ありません**。

---

## Memory とは（全製品共通の説明）

現行の `docs/memory/` の冒頭は、Memory を次のように説明しています（Web 固有の記述ではなく、全製品共通の説明です）。

> Memory lets Kiro carry useful context from one chat session to the next.

**Memory は、Kiro がチャットセッションをまたいで有用な文脈を持ち越す仕組みです。** 公式は、記憶できるものとして次を挙げています。

- リポジトリのコマンドと規約
- 訂正
- デバッグで得た知見
- すでに除外した方法
- 利用者の作業の好み

公式は、Memory を **Kiro のエージェントハーネス**（文脈を組み立ててエージェントを動かす仕組み）の一部としています。各 memory は **title・description・content を持つレコード**で、過去の会話のコピーではありません。

公式ページが Memory と並べて整理している文脈は次のとおりです。

| 文脈 | 公式の説明 |
|------|----------|
| **Memory** | 作業から Kiro が学び、後のセッションで想起できる文脈 |
| **Steering** | Kiro が従う内容を明示的に制御したいときに書くルールと指針 |
| **Session history** | 同じセッションを続ける・再開するときに既にある会話と作業 |
| **Compaction** | 長いセッションを文脈の上限内に収めるための、古い会話履歴の要約 |
| **Knowledge bases (CLI)** | 利用者が選んで索引化し、必要なときに Kiro が検索する参考資料 |

> 公式は「**If a rule must apply consistently, write it in Steering.**」と書いています（常に適用したいルールは Steering に書く）。Steering は [04_steering.md](04_steering.md) を参照してください。

> ⚠️ **IDE / CLI タブの記述は Kiro Web の仕様ではありません。** たとえば「Memory は利用者アカウントごとにローカルへ保存される」「Kiro IDE と Kiro CLI は同じマシンで保存済みの memory を共有する」「Memory のアクセスレベルは IDE の設定（既定は Off）／CLI の `/memories`」といった記述は、**IDE と CLI の説明**です。Kiro Web に当てはめてはいけません。

---

## 移転前の Web 専用ページの記述

次は、移転前の `docs/web/memory/` に書かれていた内容です（このページには `Page updated` も `dateModified` もありませんでした）。
**現行のページには同じ記述がなく、現在の Kiro Web に当てはまるかどうかは未確認です。**

> Memory is what the agent learns over time. As you work with Kiro Web and give it feedback, it picks up your preferences and applies them to future work, so you don't have to restate the same guidance in every session.

**Memory は、エージェントが時間をかけて学習した内容です。** Kiro Web で作業してフィードバックを与えると、エージェントが**利用者の好みを取り込み、以後の作業に適用**します。そのため、**毎回のセッションで同じ指示を言い直す必要がありません**。

| 項目 | 移転前の記述 |
|------|------------|
| 場所 | Kiro Web の **Settings の Memory セクション** |
| 有効化 | **不要**（自動で維持される。オンにするものは無い） |
| 手動追加 | **できない**（手で足すものは無い） |
| 削除 | **できる**（残したくない memory を削除できる） |
| 何も無いとき | **`No memories yet`** と表示される |
| 学習に影響するもの | **タスクを作成した利用者本人のフィードバックのみ** |
| 学習に影響しないもの | **他のレビュアーのコメント** |
| 良くする条件 | 指示が**明確で一貫している**ほど、memory は時間とともに有用になる |

---

## Memory と Steering の違い（移転前の記述）

移転前のページは、次の比較表を載せていました。

> Both memory and steering help the agent follow your preferences, but you create them in different ways.

| | **Memory** | **Steering** |
|---|---|---|
| **作られ方** | エージェントが**作業とフィードバックから自動で学習する** | 利用者が**明示的に書く**（Settings または `.kiro/steering/` の Markdown ファイル） |
| **どこにあるか** | **Settings の中** | **Settings とファイルシステムの両方** |
| **利用者が操作できる範囲** | **削除のみ** | **すべての編集** |

使い分けについて、移転前のページは次のように説明していました。

> Use steering when you want to state a rule explicitly and control exactly what the agent follows. Memory complements it by capturing the preferences the agent picks up as you work together.

| 使う場面 | 仕組み |
|---------|-------|
| **ルールを明示的に宣言し、エージェントが従う内容を正確に制御したい** | **Steering** |
| **一緒に作業する中でエージェントが拾った好みを蓄積させたい** | **Memory**（Steering を補完する） |

> 現行の `docs/memory/` は、Steering を「Rules and guidance you write when you want explicit control over what Kiro follows」、Memory を「Context Kiro learns from your work and can recall in a later session」と整理しています（Web 固有の記述ではありません）。

Steering の詳細は [04_steering.md](04_steering.md) を参照してください。

---

## 🔗 関連ページ

- [04_steering.md](04_steering.md) — Steering（明示的に書くルール）
- [06_repository-integration.md](06_repository-integration.md) — PR のフィードバックでエージェントを導く
- [09_configuration-sync.md](09_configuration-sync.md) — 個人設定（Steering・エージェント・Skills 等）をクラウドへ上げる
- [01_agent-modes.md](01_agent-modes.md) — エージェントの働き方
- 公式: <https://kiro.dev/docs/memory/>
