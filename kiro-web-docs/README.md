# 猫でもわかるKiro Web アップデート情報 — サイト本体

**Kiro Web**（<https://app.kiro.dev>）に関する日本語ドキュメントの本体です。

> ⚠️ **Kiro Web は Preview 段階**です。仕様が変わることがあります。
> 各ページに公式ドキュメントの**出典 URL と出典日**を記載しています。

---

## 🚀 目的別の入口

| やりたいこと | 見るページ |
|------------|----------|
| **Kiro Web がどんなものか知りたい** | [01_features/01_agent-modes.md](01_features/01_agent-modes.md)（2つのモード） |
| **使い始めたい** | [03_deployment/01_setup.md](03_deployment/01_setup.md)（セットアップと最初のタスク） |
| **組織で導入したい** | [03_deployment/02_identity-center.md](03_deployment/02_identity-center.md) → [03_deployment/04_firewalls.md](03_deployment/04_firewalls.md) |
| **何が変わったか知りたい** | [02_update/01_changelog.md](02_update/01_changelog.md)（全7エントリ） |
| **設定値をピンポイントで調べたい** | [04_reference/](04_reference/)（[早見表](04_reference/04_limits.md#-早見表)） |
| **公式情報の読み方を知りたい** | [00_information/02_information-sources.md](00_information/02_information-sources.md)（落とし穴5つ） |

---

## 📚 セクション構成

| セクション | 内容 |
|-----------|------|
| [00_information](00_information/) | 公式サイトの構造・情報源の使い分けと落とし穴（2ページ） |
| [01_features](01_features/) | 機能詳細ガイド（6ページ） |
| [02_update](02_update/) | 更新履歴（全7エントリ・折りたたみ21項目も全量掲載） |
| [03_deployment](03_deployment/) | 導入・運用（4ページ） |
| [04_reference](04_reference/) | リファレンス（4ページ・検証可能な正準値） |

**二層構成**: 機能の解説は `01_features/`、**値の一覧は `04_reference/`** に置いています。同じ値を2箇所に書かず、`01_features/` から `04_reference/` へリンクします。

---

## 🔖 Kiro Web にはバージョン番号がありません

Kiro IDE（`1.0.NNN`）や Kiro CLI と違い、**Kiro Web の更新にバージョン番号はありません**。公式 changelog のエントリは**日付とタイトル（スラッグ）**のみで識別されます。

| 項目 | 内容 |
|------|------|
| 更新の識別 | **日付（ISO）＋スラッグ** |
| changelog エントリ数 | **7**（2025-12-02 〜 2026-07-01） |
| 公式ドキュメントのページ数 | **20** |
| 提供形態 | ホスト型サービス（**インストール不要**） |
| 段階 | **Preview** |

> 版番号が存在しない**理由**は公式に説明がないため**未確認**です。

---

## ⚠️ 公式情報を読むときの注意（実測で確認したもの）

公式ドキュメントには、素直に読むと**内容が抜け落ちる箇所**があります。詳細は [00_information/02_information-sources.md](00_information/02_information-sources.md) にまとめています。

| # | 落とし穴 | 影響 |
|---|---------|------|
| 1 | **`.md` 版でプレースホルダが潰れる** | `${key_name}` が裸の `` `$` `` になる（2ページ） |
| 2 | **`.md` 版に3製品分の内容が連結される** | `firewalls` は見出しが 8 → 18 に |
| 3 | **折りたたまれた項目が HTML に存在しない** | changelog の **21 項目**が丸ごと抜ける |
| 4 | **日付表記が2種類ある** | 5月は略記と月名フルが同形で判別不能 |
| 5 | **公式ページ間で記述が食い違う** | [Free Tier の有無](03_deployment/03_data-protection.md#free-tier-conflict)（**未解決**） |

本サイトはこれらに対処した上で、**機械検証**（リンク・構成・出典・折りたたみ項目数の一致）を回しています。

---

## 🐾 Kiro Web / Kiro IDE / Kiro CLI は別製品です

同名の機能（Specs・Steering・MCP など）でも仕様が異なることがあります。本サイトの各ページは **Kiro Web 版の仕様**を扱います。

| 対象 | サイト |
|------|-------|
| **Kiro Web** | **本サイト** |
| Kiro IDE | [kiro-ide-docs](https://github.com/kamogashira-sys/kiro-ide-docs) |
| Kiro CLI | [q-cli-docs](https://github.com/kamogashira-sys/q-cli-docs) |

公式が「同一」と明記しているもの（[Steering](01_features/04_steering.md#3つのインターフェースで同じ動作をします公式明記)）と、公式が差分を明記しているもの（[Specs](01_features/02_specs.md#kiro-ide-との違い公式が明記している3点)）は区別して書いています。

---

## 🔗 公式情報源

- 公式ドキュメント（Web）: <https://kiro.dev/docs/web/>
- 公式 changelog（Web）: <https://kiro.dev/changelog/web/>
- Kiro Web 本体: <https://app.kiro.dev>

---

[← リポジトリのトップに戻る](../README.md)
