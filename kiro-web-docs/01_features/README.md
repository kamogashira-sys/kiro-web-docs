# 01_features - 機能詳細ガイド

**Kiro Web の各機能を、公式ドキュメントの記述に基づいて解説するセクションです。**

> 🚧 **構築中**（Phase 1 完了時点）。本文は Phase 2b で追加します。
>
> ⚠️ 本セクションは **Kiro Web 版**の仕様を扱います。Kiro IDE / Kiro CLI の同名機能とは仕様が異なる場合があります。

---

## 📂 このセクションのファイル

| ファイル | 内容 | 公式ドキュメント |
|---------|------|---------------|
| `01_agent-modes.md` | **エージェントのモード**（協調的な進め方 / Autonomous mode）・チャット・タスクの作成 | `web/using-the-agent/`・`web/autonomous-mode/` |
| `02_specs.md` | **Specs**（要件・設計・タスクの計画）。公式が明記する IDE との差分3点 | `web/specs/` |
| `03_automations.md` | **Automations**（定期実行） | `web/automations/` |
| `04_steering.md` | **Steering**（公式は3インターフェースで同一と明記） | `web/steering/` |
| `05_sandbox.md` | **Sandbox**（構成・ネットワークアクセス・環境変数・Powers / MCP） | `web/sandbox/` 配下5ページ |
| `06_repository-integration.md` | **GitHub / GitLab 連携** | `web/github/`・`web/gitlab/` |

---

## 📌 値の一覧は 04_reference にあります

許可ドメイン・環境変数の構文・MCP 設定・上限値などの**検証可能な値**は [04_reference](../04_reference/) にまとめています。本セクションでは仕組みと使い方を扱い、値はリンクで参照します（同じ値を2箇所に書かないため）。

---

## 関連セクション

- [00_information](../00_information/) - 公式情報源の構造
- [02_update](../02_update/) - 更新履歴
- [03_deployment](../03_deployment/) - 導入・運用
- [04_reference](../04_reference/) - リファレンス
