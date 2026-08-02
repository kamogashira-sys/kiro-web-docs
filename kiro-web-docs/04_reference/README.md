# 04_reference - リファレンス

**設定値・許可ドメイン・上限値など、Kiro Web の「調べたい値」を引くためのセクションです。**

> ⚠️ 本セクションは **Kiro Web 版**の仕様を扱います。

---

## 📂 このセクションのファイル

| ファイル | 内容 | 公式ドキュメント |
|---------|------|---------------|
| [01_allowed-domains.md](01_allowed-domains.md) | **許可ドメイン・URL・IP の一覧**（目的の違う3系統: 本体 34 行・サンドボックス 73 ドメイン・GitLab 送信元 IP 3 件） | `web/firewalls/`・`web/sandbox/internet-access/`・`web/gitlab/` |
| [02_environment-variables.md](02_environment-variables.md) | **環境変数・シークレット**（`${key_name}` 参照構文・優先順位・IAM ロールと信頼ポリシー） | `web/sandbox/environment-variables/`・`web/sandbox/environment-configuration/` |
| [03_mcp-configuration.md](03_mcp-configuration.md) | **MCP 設定と Powers**（設定 JSON・ローカルのみ対応・OAuth 認可・セキュリティ警告） | `web/sandbox/mcp/` |
| [04_limits.md](04_limits.md) | **上限・保持期間・リージョン**（並列 10・スケジュール 5・10,000 文字・90 日・128GB ほか） | `web/using-the-agent/`・`web/using-the-agent/creating-tasks/`・`web/automations/`・`web/data-protection/` |

---

## 📊 早見表

主要な値は [04_limits.md の早見表](04_limits.md#-早見表) にまとめています。

| 項目 | 値 |
|------|---|
| 並列タスクの上限 | **10** |
| セッションの保持期間 | **90 日** |
| オートメーションのスケジュール上限 / プロンプト文字数 | **5** / **10,000 文字** |
| サンドボックスのディスク容量 | **128GB** |
| 許可ドメイン数（Common dependencies） | **73** |

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
