# 公式サイトの構造マップ（Kiro Web の情報はどこにあるか）

> **本ページは Kiro Web 版（<https://app.kiro.dev>）に関する情報源の構造をまとめたものです。**
> Kiro IDE / Kiro CLI とは別製品であり、公式サイト上でも別のツリーに置かれています。
> **Kiro Web は Preview 段階**です。

**出典**: <https://kiro.dev/docs/web/>・<https://kiro.dev/changelog/web/>・<https://kiro.dev/sitemap.xml>・<https://kiro.dev/llms.txt>
**実測日**: 2026-08-01（本ページの全数値はこの日に取得した一次情報の実測値）

---

## 📑 このページの内容

1. [公式サイトの全体像](#公式サイトの全体像)
2. [Kiro Web の情報が置かれている4か所](#kiro-web-の情報が置かれている4か所)
3. [changelog の系列構造](#changelog-の系列構造)
4. [docs の区分構造](#docs-の区分構造)
5. [機械可読な索引（sitemap と llms.txt）](#機械可読な索引sitemap-と-llmstxt)
6. [URL の作法](#url-の作法)

---

## 公式サイトの全体像

`kiro.dev` の sitemap には **463 の URL** が登録されています（2026-08-01 実測）。内訳は次のとおりです。

| 区画 | URL 数 | Kiro Web との関係 |
|------|-------|-----------------|
| `docs/`（IDE ＋ 共有ドキュメント） | 117 | 共有ドキュメントのみ関係する |
| `changelog/` | 104 | **`changelog/web/` の 7 件が本サイトの対象** |
| `docs/cli/` | 101 | 別製品（Kiro CLI） |
| `blog/` | 88 | Kiro Web 関連が 3 本 |
| **`docs/web/`** | **20** | **本サイトの主対象** |
| その他（トップページ・製品ページなど） | 33 | — |

**Kiro Web の一次情報は `docs/web/` の 20 ページと `changelog/web/` の 7 エントリ**です。この 27 件が本サイトの収録範囲の中核になります。

---

## Kiro Web の情報が置かれている4か所

| # | 場所 | 内容 | 本サイトでの位置づけ |
|---|------|------|------------------|
| 1 | <https://kiro.dev/changelog/web/> | 更新履歴（**7 エントリ**・2025-12-02 〜 2026-07-01） | **更新内容と日付の正**。[02_update](../02_update/01_changelog.md) に全量掲載 |
| 2 | <https://kiro.dev/docs/web/> | 公式ドキュメント（**20 ページ**） | **機能仕様・設定・リファレンス値の正** |
| 3 | <https://kiro.dev/blog/> | 関連ブログ（**3 本**） | 背景の補足のみ。本文の主たる根拠にしない |
| 4 | <https://app.kiro.dev> | Kiro Web 本体 | 実機。利用には有料サブスクリプションが必要 |

### 関連ブログ3本

| ブログ | 対応する changelog エントリ |
|-------|------------------------|
| `blog/introducing-kiro-web/` | 2026-05-07 の Kiro Web（Preview）提供開始 |
| `blog/kiro-web-specs-gitlab/` | 2026-06-11 の GitLab 対応・Specs |
| `blog/introducing-kiro-autonomous-agent/` | 2025-12-02 の autonomous agent（**同名スラッグ**） |

> ブログには `.md` 版がありません（3本とも 404）。

---

## changelog の系列構造

公式 changelog は**製品ごとの系列**に分かれています。

| 系列 | URL | エントリ数 | 本サイトの扱い |
|------|-----|-----------|--------------|
| **Web** | `changelog/web/` | **7** | ✅ **全件収録** |
| IDE | `changelog/ide/` | 23 | ❌ 別製品（姉妹サイト [kiro-ide-docs](https://github.com/kamogashira-sys/kiro-ide-docs)） |
| CLI | `changelog/cli/` | 27 | ❌ 別製品（姉妹サイト [q-cli-docs](https://github.com/kamogashira-sys/q-cli-docs)） |
| Models | `changelog/models/` | 17 | ❌ 収録しない（必要時に出典として参照） |
| General | `changelog/general/` | 10 | ❌ 収録しない（同上） |

### ⚠️ ページ送り（`page/N`）が存在します

系列ごとにページ送りの URL があります。**これらはエントリではありません。**

| 系列 | ページ送りの実在（2026-08-01） |
|------|--------------------------|
| メイン（`changelog/`） | `page/2` 〜 `page/9`（**8 件**） |
| IDE | `page/2`・`page/3` |
| CLI | `page/2`・`page/3` |
| Models | `page/2` |
| **Web** | **現時点では存在しない**（`changelog/web/page/2/` は 404） |

Web は現在7エントリなので1ページに収まっていますが、**`/changelog/<系列>/page/N/` はこの公式サイトの一般的な仕組み**です。Web でもエントリが増えれば現れます。本サイトの検証スクリプトは、この URL を新エントリとして数えないようにしています。

### Kiro Web の更新にバージョン番号はありません

Kiro IDE の `1.0.242` に相当する版番号が **Kiro Web には存在しません**。エントリの識別は**日付とタイトル（スラッグ）**のみです。

| 項目 | Kiro Web | Kiro IDE（対比） |
|------|---------|----------------|
| 更新の識別 | **日付 ＋ スラッグ** | 版番号 `1.0.NNN` |
| changelog の `.md` 版 | **無い**（7/7 が 404） | 無い |
| フィード（Atom・RSS）への掲載 | **直近25件に0件**・系列別フィードは404 | 掲載される |

> 版番号が存在しない**理由**は公式に説明がないため**未確認**です。
> フィードが Web を配信対象にしているかも**未確認**です（最新エントリがウィンドウより古いためか、
> そもそも対象外なのかを一次情報から判別できません）。

---

## docs の区分構造

公式ドキュメントは URL のパスで製品が分かれます。

| 区分 | URL パターン | ページ数 |
|------|------------|---------|
| **Web** | `docs/web/…` | **20** |
| IDE | `docs/…`（`cli`・`web` 以外） | 117 |
| CLI | `docs/cli/…` | 101 |

### Kiro Web の 20 ページ（全量）

URL パスの階層で示します（**これが親子関係の正**）。

```
docs/web/                                  … Kiro Web の入口
├── setup/                                 … セットアップ（ログイン方式）
├── first-task/                            … 最初のタスク
├── using-the-agent/                       … エージェントの使い方
│   ├── chatting/                          … チャット
│   └── creating-tasks/                    … タスクの作成
├── autonomous-mode/                       … Autonomous モード
├── specs/                                 … Specs
├── automations/                           … Automations（定期実行）
├── steering/                              … Steering
├── sandbox/                               … サンドボックス
│   ├── environment-configuration/         … 環境の構成
│   ├── environment-variables/             … 環境変数・シークレット
│   ├── internet-access/                   … ネットワークアクセス
│   └── mcp/                               … MCP サーバー
├── github/                                … GitHub 連携
├── gitlab/                                … GitLab 連携
├── identity-center/                       … AWS Identity Center
├── data-protection/                       … データ保護
└── firewalls/                             … ファイアウォール・プロキシ
```

各ページの本サイトでの配置は [サイト本体の README](../README.md) と各セクションの README を参照してください。

### 共有ドキュメント（Shared）

Web 専用ではないものの Web にも関わるページがあります（`llms.txt` の `## Shared` 区分・31ページ）。

| ページ | Web との関わり |
|-------|--------------|
| `docs/billing/…` | サブスクリプション・課金 |
| `docs/models/…` | 利用できるモデル |
| `docs/privacy-and-security/…` | プライバシー・セキュリティ |
| `docs/migrating-from-q-developer/…` | Amazon Q Developer からの移行 |

本サイトは**Web に関わる範囲でのみ**これらを参照します。

### 公式が Web docs から他製品・共有ページへ張っているリンク（11 種）

`docs/specs`・`docs/specs/bugfix-specs`・`docs/steering`・`docs/cli/mcp/security`・`docs/powers`・`docs/privacy-and-security/vpc-endpoints`・`docs/troubleshooting`・`docs/enterprise/concepts`・`docs/enterprise/settings`・`docs/enterprise/governance`・`docs/enterprise/monitor-and-track/user-activity`

本サイトでこれらに触れるときは、**別製品または共有ドキュメントであること**を明示します。

---

## 機械可読な索引（sitemap と llms.txt）

公式サイトには機械可読な索引が2種類あり、**中身が違います**。

| 索引 | URL | 内容 | 総数 |
|------|-----|------|------|
| **sitemap** | <https://kiro.dev/sitemap.xml> | サイト全体の URL（docs・changelog・blog・製品ページ） | **463 URL** |
| **llms.txt** | <https://kiro.dev/llms.txt> | ドキュメントの索引を **IDE / CLI / Web / Shared / Optional** に区分 | **203 URL** |

### llms.txt の区分と件数（2026-08-01 実測）

| 区分 | 件数 |
|------|------|
| IDE | 64 |
| CLI | 66 |
| **Web** | **20** |
| Shared | 31 |
| Optional | 22 |

### ⚠️ llms.txt は docs を網羅していません

sitemap の docs ページ（238 件）と `llms.txt`（203 件）を突き合わせると、**sitemap にあって `llms.txt` に無いページが 36 件**あります。内訳は **`docs/cli/` が 35 件**と **`docs/` 索引が 1 件**です。

**ただし Web 区分は sitemap と完全一致します**（どちらも同じ 20 ページ・差分 0）。

| 突き合わせ | 結果 |
|-----------|------|
| Web 区分（`llms.txt`）と sitemap の `docs/web/` | **20 = 20・差分 0（完全一致）** |
| docs 全体 | sitemap 238 vs `llms.txt` 203（**36 件が `llms.txt` に無い**・うち 35 件は CLI） |
| `llms.txt` にあって sitemap に無い | 1 件（`docs/index/`） |

→ **Kiro Web の範囲では `llms.txt` をページ全量の根拠に使えます。** ただし他製品の範囲では欠落があるため、全量を数えるときは sitemap を併用します。

### llms.txt の URL は `.md` 付きです

`llms.txt` に載っている URL は `https://kiro.dev/docs/web/specs.md` のように **`.md` が付いた形**です（203/203 件）。この `.md` 版には既知の欠落があるため、本サイトは**値を HTML から取ります**。詳細は [02_information-sources.md](02_information-sources.md) を参照してください。

### ⚠️ llms.txt の字下げはページ階層と一致しません

`llms.txt` の Web 区分では、項目の字下げが URL の階層と **20 件中 7 件で食い違います**。

| 食い違いの例 | 字下げから読める階層 | 実際の URL |
|------------|------------------|-----------|
| `first-task`・`github`・`gitlab`・`identity-center` | `firewalls` の子に見える | `docs/web/` の直下 |
| `setup` | `sandbox` の子に見える | `docs/web/` の直下 |

→ **ページの親子関係は URL パスを正とします。** `llms.txt` の用途は「ページ全量と製品区分の判定」に限定します。

---

## URL の作法

公式サイトから情報を取るときに必要な作法が2つあります。どちらも実測で確認しています。

| # | 作法 | 実測 |
|---|------|------|
| 1 | **URL は末尾スラッシュを付ける** | `changelog` も `docs` も、スラッシュなしは **301 リダイレクト**（docs 20 ページを試して **20/20 が 301・本文 0 バイト**、スラッシュ付きで 20/20 が 200） |
| 2 | **User-Agent を空にしない** | 空文字を明示指定すると **403**。`-A "Mozilla/5.0"` を付ければ確実 |

本サイトが載せる公式ページの URL は、この作法に合わせてすべて末尾スラッシュ付きにしています（機械検証しています）。

---

## 🔗 関連ページ

- [02_information-sources.md](02_information-sources.md) — 情報源の使い分けと落とし穴（`.md` の壊れ方・折りたたみ節）
- [02_update/01_changelog.md](../02_update/01_changelog.md) — 更新履歴（全7エントリ）
- 公式ドキュメント: <https://kiro.dev/docs/web/>
- 公式 changelog: <https://kiro.dev/changelog/web/>

---

[← 00_information に戻る](README.md)
