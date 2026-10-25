# 01_features - 機能詳細ガイド

**Kiro Web の各機能を、公式ドキュメントの記述に基づいて解説するセクションです。**

> ⚠️ 本セクションは **Kiro Web 版**の仕様を扱います。Kiro IDE / Kiro CLI の同名機能とは仕様が異なる場合があります。

---

## 📂 このセクションのファイル

| ファイル | 内容 | 公式ドキュメント |
|---------|------|---------------|
| [01_agent-modes.md](01_agent-modes.md) | **2つのモード**（協調モード / Autonomous モード）・タスクの作り方・状態遷移・Web 検索 | `web/using-the-agent/` ＋配下2・`web/autonomous-mode/` |
| [02_specs.md](02_specs.md) | **Specs**（要件・設計・タスクを作ってから実装）。IDE との差分の記述は現行ページで変わっている | `docs/specs/`（全製品共通の移転先） |
| [03_automations.md](03_automations.md) | **Schedule**（公式 docs の現行名称。旧称 Automations。定期実行・UTC 評価・実行ごとに独立サンドボックス） | `web/automations/` |
| [04_steering.md](04_steering.md) | **Steering**（かつての「3インターフェースで同一」の一文は**現行ページに無い**・学習はタスク作成者のみ） | `docs/steering/`（全製品共通の移転先） |
| [05_sandbox.md](05_sandbox.md) | **サンドボックス**（動作5段階・ネットワーク4レベル・**サンドボックスの外側で動くもの**） | `web/sandbox/` ＋配下4 |
| [06_repository-integration.md](06_repository-integration.md) | **GitHub / GitLab 連携**（2層の権限・PR 作成者・トークンの絞り方・混在利用） | `web/github/`・`web/gitlab/` |
| [07_cloud-sessions.md](07_cloud-sessions.md) | **Cloud Sessions**（Kiro Web の全セッションの実行環境そのもの。IDE/CLI/Mobile との相互運用） | `docs/cloud-sessions/`（Features 区分の全製品共通ページ） |
| [08_memory.md](08_memory.md) | **Memory**（全製品共通ページへ移転。**Web タブは「coming soon」**。移転前の Web 専用ページの記述も保存） | `docs/memory/`（旧 `web/memory/` は転送） |
| [09_configuration-sync.md](09_configuration-sync.md) | **Configuration Sync**（個人の `.kiro` をクラウドへ。7フォルダ・6ステータス・**`mcp.json` の `env` は平文**） | `web/cloud-configuration/` |
| [10_file-explorer.md](10_file-explorer.md) | **ファイルエクスプローラ**（セッションのワークスペースを閲覧・ダウンロード） | `web/using-the-agent/file-explorer/` |

> **ファイル番号は追加順です（公式の並び順ではありません）。**
> 公式（`llms.txt`）の並びは Setup → Identity Center → Working with the agent（＋ **File explorer**）
> → Autonomous mode → **Schedule** → **Configuration Sync** → Sandbox の順です（`Memory` は Web 区分から外れ、全製品共通の Features 区分へ移りました）。
> 公式順に振り直すと相互リンクが一斉に壊れるため、**番号は追加順に固定**しています。

---

## 🔍 3製品の書き分けについて

同じ名前の機能でも、公式の記述は3通りに分かれます。本サイトは**公式が書いていることだけ**を書いています。

| 公式の記述 | 該当機能 | 本サイトの扱い |
|-----------|---------|--------------|
| **かつて「同じ」と明記していた** | [Steering](04_steering.md#3つのインターフェースの関係公式の記述は移転で変わりました) | **一文が現行ページから消えた事実**を書く。「同じ」とは書かない |
| **差分を明記** | [Specs](02_specs.md#kiro-ide-との違い2026-08-12-の移転時点で失われた記述)（3点） | 公式の差分をそのまま示す |
| **Web 固有** | [Powers](../04_reference/03_mcp-configuration.md)・[Schedule](03_automations.md) | Web の機能として扱う |

---

## 📌 値の一覧は 04_reference にあります

許可ドメイン・環境変数の構文・MCP 設定・上限値などの**検証可能な値**は [04_reference](../04_reference/) にまとめています。本セクションでは仕組みと使い方を扱い、値はリンクで参照します（同じ値を2箇所に書かないため）。

---

## 関連セクション

- [00_information](../00_information/) - 公式情報源の構造
- [02_update](../02_update/) - 更新履歴
- [03_deployment](../03_deployment/) - 導入・運用
- [04_reference](../04_reference/) - リファレンス
