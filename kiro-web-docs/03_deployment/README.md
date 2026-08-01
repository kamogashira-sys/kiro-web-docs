# 03_deployment - 導入・運用

**Kiro Web を使い始めるための設定と、組織で導入する際に必要な要件をまとめたセクションです。**

> 🚧 **構築中**（Phase 1 完了時点）。本文は Phase 2b で追加します。
>
> ⚠️ 本セクションは **Kiro Web 版**の仕様を扱います。

---

## 📂 このセクションのファイル

| ファイル | 内容 | 公式ドキュメント |
|---------|------|---------------|
| `01_setup.md` | **セットアップ**（ソーシャルログイン / AWS Identity Center）・最初のタスク | `web/setup/`・`web/first-task/` |
| `02_identity-center.md` | **AWS Identity Center**（要件・制限） | `web/identity-center/` |
| `03_data-protection.md` | **データ保護**（保存リージョン・暗号化・オプトアウト） | `web/data-protection/` |
| `04_firewalls.md` | **ファイアウォール・プロキシ・データ境界** | `web/firewalls/` |

---

## 📌 Kiro Web は「インストール」しません

Kiro Web はブラウザから使うホスト型サービスです（<https://app.kiro.dev>）。IDE 版のようなインストール手順はなく、**ログインとリポジトリ連携**が導入作業になります。

---

## 📌 許可すべきドメイン・IP の一覧は 04_reference にあります

ファイアウォールやプロキシの設定に必要な**ドメイン・URL・IP の一覧**は [04_reference/01_allowed-domains.md](../04_reference/) にまとめています。本セクションでは要件と考え方を扱います。

---

## 関連セクション

- [00_information](../00_information/) - 公式情報源の構造
- [01_features](../01_features/) - 機能詳細ガイド
- [02_update](../02_update/) - 更新履歴
- [04_reference](../04_reference/) - リファレンス
