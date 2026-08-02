# 01_features - 機能詳細ガイド

**Kiro Web の各機能を、公式ドキュメントの記述に基づいて解説するセクションです。**

> ⚠️ 本セクションは **Kiro Web 版**の仕様を扱います。Kiro IDE / Kiro CLI の同名機能とは仕様が異なる場合があります。

---

## 📂 このセクションのファイル

| ファイル | 内容 | 公式ドキュメント |
|---------|------|---------------|
| [01_agent-modes.md](01_agent-modes.md) | **2つのモード**（協調モード / Autonomous モード）・タスクの作り方・状態遷移・Web 検索 | `web/using-the-agent/` ＋配下2・`web/autonomous-mode/` |
| [02_specs.md](02_specs.md) | **Specs**（要件・設計・タスクを作ってから実装）。**公式が明記する IDE との差分3点** | `web/specs/` |
| [03_automations.md](03_automations.md) | **Automations**（定期実行・UTC 評価・実行ごとに独立サンドボックス） | `web/automations/` |
| [04_steering.md](04_steering.md) | **Steering**（**公式が3インターフェースで同一と明記**・学習はタスク作成者のみ） | `web/steering/` |
| [05_sandbox.md](05_sandbox.md) | **サンドボックス**（動作5段階・ネットワーク4レベル・**サンドボックスの外側で動くもの**） | `web/sandbox/` ＋配下4 |
| [06_repository-integration.md](06_repository-integration.md) | **GitHub / GitLab 連携**（2層の権限・PR 作成者・トークンの絞り方・混在利用） | `web/github/`・`web/gitlab/` |

---

## 🔍 3製品の書き分けについて

同じ名前の機能でも、公式の記述は3通りに分かれます。本サイトは**公式が書いていることだけ**を書いています。

| 公式の記述 | 該当機能 | 本サイトの扱い |
|-----------|---------|--------------|
| **「同じ」と明記** | [Steering](04_steering.md#3つのインターフェースで同じ動作をします公式明記) | 「公式が同一と明記している」と書く。**推測で差分を作らない** |
| **差分を明記** | [Specs](02_specs.md#kiro-ide-との違い公式が明記している3点)（3点） | 公式の差分をそのまま示す |
| **Web 固有** | [Powers](../04_reference/03_mcp-configuration.md)・[Automations](03_automations.md) | Web の機能として扱う |

---

## 📌 値の一覧は 04_reference にあります

許可ドメイン・環境変数の構文・MCP 設定・上限値などの**検証可能な値**は [04_reference](../04_reference/) にまとめています。本セクションでは仕組みと使い方を扱い、値はリンクで参照します（同じ値を2箇所に書かないため）。

---

## 関連セクション

- [00_information](../00_information/) - 公式情報源の構造
- [02_update](../02_update/) - 更新履歴
- [03_deployment](../03_deployment/) - 導入・運用
- [04_reference](../04_reference/) - リファレンス
