# 猫でもわかるKiro Web アップデート情報

**Kiro Web**（<https://app.kiro.dev>）のアップデート情報・機能詳細・リファレンスを、日本語でまとめた**非公式**ドキュメントサイトです。

> 🚧 **本サイトは構築中です**（Phase 1 完了時点）。本文は順次公開します。
>
> ⚠️ **Kiro Web は Preview 段階**です。仕様が変わることがあります。本サイトの各ページには
> 公式ドキュメントの**出典日**を記載しています。

---

## 📚 セクション

| セクション | 内容 |
|-----------|------|
| [00_information](kiro-web-docs/00_information/) | 公式サイトの構造・情報源の使い分け |
| [01_features](kiro-web-docs/01_features/) | 機能詳細ガイド（エージェントモード・Specs・Automations・Steering・Sandbox・リポジトリ連携） |
| [02_update](kiro-web-docs/02_update/) | 更新履歴（[changelog 全7エントリ](kiro-web-docs/02_update/01_changelog.md)）✅ |
| [03_deployment](kiro-web-docs/03_deployment/) | 導入・運用（Setup・Identity Center・データ保護・ファイアウォール） |
| [04_reference](kiro-web-docs/04_reference/) | リファレンス（許可ドメイン・環境変数・MCP 設定・上限値） |

---

## 🐾 姉妹サイト

Kiro は IDE・CLI・Web の3つのインターフェースを持つ**別製品**です。同名の機能でも仕様が異なることがあります。

| 対象 | サイト |
|------|-------|
| **Kiro Web** | **本サイト** |
| Kiro IDE | [猫でもわかるKiro IDE アップデート情報](https://github.com/kamogashira-sys/kiro-ide-docs) |
| Kiro CLI | [猫でもわかるKiro CLI アップデート情報](https://github.com/kamogashira-sys/q-cli-docs) |

---

## 📌 本サイトの方針

| # | 方針 |
|---|------|
| 1 | **一次情報のみ**を根拠にする（公式 changelog・公式ドキュメント・sitemap・`llms.txt`） |
| 2 | 公式に確認できない事項は「**未確認**」と明示し、断定しない |
| 3 | 公式に書かれていない**理由・因果も書かない**（事実と推測を分離する） |
| 4 | 公式ページ間で記述が食い違う場合は**両方を併記**し、どちらが正しいかを裁定しない |
| 5 | 日付は **ISO 形式（`YYYY-MM-DD`）** に正規化する |
| 6 | 各ページに公式の**出典 URL と出典日**を記載する |

---

## 🔗 公式情報源

- Kiro Web: <https://app.kiro.dev>
- 公式ドキュメント（Web）: <https://kiro.dev/docs/web/>
- 公式 changelog（Web）: <https://kiro.dev/changelog/web/>

---

## 🤝 コントリビュート

- [ドキュメント作成ワークフロー](.github/WORKFLOW.md)
- [コミット前チェックリスト](.github/COMMIT_CHECKLIST.md)
- [Code of Conduct](CODE_OF_CONDUCT.md)

## 📄 ライセンス

[MIT License](LICENSE)

---

**免責事項**: 本サイトは非公式のドキュメントプロジェクトであり、Kiro および Amazon Web Services, Inc. とは関係ありません。正確性には努めていますが、内容は公式ドキュメントで必ず確認してください。
