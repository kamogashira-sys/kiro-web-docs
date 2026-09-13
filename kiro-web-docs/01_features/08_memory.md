# Memory（エージェントが学習すること）

> **本ページは Kiro Web 版（<https://app.kiro.dev>）の仕様です。**
> Kiro IDE / Kiro CLI とは別製品です。**Kiro Web は [2026-09-01 に一般提供（GA）になりました](https://kiro.dev/changelog/web/kiro-web-is-now-generally-available/)。**

**出典**: <https://kiro.dev/docs/web/memory/>

> ⚠️ **本ページの出典には出典日がありません。** 公式ページに JSON-LD の `dateModified` が無く、
> `Page updated` の表示もありません（Web 18 ページ中このページのみ・2026-09-13 実測）。
> このため本サイトの**出典日 vs 公式の更新日の機械照合が効きません**
> （[情報源の落とし穴](../00_information/02_information-sources.md)を参照）。

---

## 📑 このページの内容

1. [Memory とは](#memory-とは)
2. [どこで見られるか](#どこで見られるか)
3. [Kiro はどうやって Memory を作るか](#kiro-はどうやって-memory-を作るか)
4. [Memory と Steering の違い](#memory-と-steering-の違い)
5. [使い分け](#使い分け)

---

## Memory とは

公式は次のように説明しています。

> Memory is what the agent learns over time. As you work with Kiro Web and give it feedback, it picks up your preferences and applies them to future work, so you don't have to restate the same guidance in every session.

**Memory は、エージェントが時間をかけて学習した内容です。** Kiro Web で作業してフィードバックを与えると、
エージェントが**利用者の好みを取り込み、以後の作業に適用**します。
そのため、**毎回のセッションで同じ指示を言い直す必要がありません**。

---

## どこで見られるか

公式は次のように説明しています。

> You can see what Kiro has learned in the Memory section of your Kiro Web Settings. Memory is maintained automatically, so there's nothing to turn on and nothing to add manually. You can delete any memory you don't want the agent to keep. Until Kiro has collected anything, this section shows No memories yet.

| 項目 | 内容 |
|------|------|
| 場所 | Kiro Web の **Settings の Memory セクション** |
| 有効化 | **不要**（自動で維持される。オンにするものは無い） |
| 手動追加 | **できない**（手で足すものは無い） |
| 削除 | **できる**（残したくない memory を削除できる） |
| 何も無いとき | **`No memories yet`** と表示される |

---

## Kiro はどうやって Memory を作るか

公式は次のように説明しています。

> Only your feedback, as the user who created the task, influences what the agent learns. Other reviewers' comments don't affect it. The clearer and more consistent your direction, the more useful memory becomes over time.

| 項目 | 内容 |
|------|------|
| 学習に影響するもの | **タスクを作成した利用者本人のフィードバックのみ** |
| 学習に影響しないもの | **他のレビュアーのコメント** |
| 良くする条件 | 指示が**明確で一貫している**ほど、memory は時間とともに有用になる |

---

## Memory と Steering の違い

公式は次のように説明しています。

> Both memory and steering help the agent follow your preferences, but you create them in different ways.

**どちらもエージェントに利用者の好みを守らせるための仕組み**ですが、**作られ方が違います。**

公式の比較表です。

| | **Memory** | **Steering** |
|---|---|---|
| **作られ方** | エージェントが**作業とフィードバックから自動で学習する** | 利用者が**明示的に書く**（Settings または `.kiro/steering/` の Markdown ファイル） |
| **どこにあるか** | **Settings の中** | **Settings とファイルシステムの両方** |
| **利用者が操作できる範囲** | **削除のみ** | **すべての編集** |

Steering の詳細は [04_steering.md](04_steering.md) を参照してください。

> ⚠️ **`.kiro/steering/` は Kiro Web では扱いが異なります。** 公式の比較表では、
> `.kiro/steering/`（リポジトリ内の Steering ファイル）は Web でも有効ですが、
> **`~/.kiro/steering/`（個人の Steering）は Web ではそのままでは読まれません**。
> 個人設定をクラウドへ上げる仕組みが [Configuration Sync](09_configuration-sync.md) です。

---

## 使い分け

公式は次のように説明しています。

> Use steering when you want to state a rule explicitly and control exactly what the agent follows. Memory complements it by capturing the preferences the agent picks up as you work together.

| 使う場面 | 仕組み |
|---------|-------|
| **ルールを明示的に宣言し、エージェントが従う内容を正確に制御したい** | **Steering** |
| **一緒に作業する中でエージェントが拾った好みを蓄積させたい** | **Memory**（Steering を補完する） |

---

## 🔗 関連ページ

公式が「Related links」として挙げているページです。

| 公式の項目 | 本サイトの該当ページ |
|-----------|-----------------|
| Steering: guide the agent with persistent, explicit conventions | [04_steering.md](04_steering.md) |
| Teaching through code reviews: shape what the agent learns with PR feedback | [06_repository-integration.md](06_repository-integration.md) |
| Working with the agent: how the agent uses context and past learnings to respond | [01_agent-modes.md](01_agent-modes.md) |

- [09_configuration-sync.md](09_configuration-sync.md) — 個人設定（Steering・エージェント・Skills 等）をクラウドへ上げる
- [../04_reference/04_limits.md](../04_reference/04_limits.md) — 上限値の一覧
