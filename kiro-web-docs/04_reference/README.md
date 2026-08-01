# 04_reference - リファレンス

**設定値・許可ドメイン・上限値など、Kiro Web の「調べたい値」を引くためのセクションです。**

> 🚧 **構築中**（Phase 1 完了時点）。本文は Phase 2b で追加します。
>
> ⚠️ 本セクションは **Kiro Web 版**の仕様を扱います。

---

## 📂 このセクションのファイル

| ファイル | 内容 | 公式ドキュメント |
|---------|------|---------------|
| `01_allowed-domains.md` | **許可ドメイン・URL・IP の一覧**（サンドボックスの依存先ドメイン・ファイアウォール設定用の URL 表・GitLab 送信元 IP） | `web/sandbox/internet-access/`・`web/firewalls/`・`web/gitlab/` |
| `02_environment-variables.md` | **環境変数・シークレット**（参照構文・IAM ロール／信頼ポリシー） | `web/sandbox/environment-variables/`・`web/sandbox/environment-configuration/` |
| `03_mcp-configuration.md` | **MCP 設定**（JSON スキーマ・ローカルサーバのみ対応） | `web/sandbox/mcp/` |
| `04_limits.md` | **上限・保持期間**（並列タスク数・スケジュール数・プロンプト文字数・セッション保持期間・ディスク容量ほか） | `web/using-the-agent/creating-tasks/`・`web/automations/`・`web/using-the-agent/` |

---

## 📌 本セクションの値は機械検証されています

本セクションに載せる件数・上限値は**正準値（SSoT）**として定義し、検証スクリプトで公式ドキュメントとの一致を確認しています。値が本文と一次情報でずれると、検証が失敗します。

> 一覧は保守手順書（ローカル管理）で管理しています。

---

## 関連セクション

- [00_information](../00_information/) - 公式情報源の構造
- [01_features](../01_features/) - 機能詳細ガイド（値の背景・使い方）
- [02_update](../02_update/) - 更新履歴
- [03_deployment](../03_deployment/) - 導入・運用
