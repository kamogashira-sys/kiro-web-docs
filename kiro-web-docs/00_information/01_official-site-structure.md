# 公式サイトの構造マップ（Kiro Web の情報はどこにあるか）

> **本ページは Kiro Web 版（<https://app.kiro.dev>）に関する情報源の構造をまとめたものです。**
> Kiro IDE / Kiro CLI とは別製品であり、公式サイト上でも別のツリーに置かれています。
> **Kiro Web は [2026-09-01 に一般提供（GA）になりました](https://kiro.dev/changelog/web/kiro-web-is-now-generally-available/)。**

**出典**: <https://kiro.dev/docs/web/>・<https://kiro.dev/changelog/web/>・<https://kiro.dev/sitemap.xml>・<https://kiro.dev/llms.txt>
**実測日**: 2026-08-16（本ページの全数値はこの日に取得した一次情報の実測値。2026-08-01時点の値は移転前の記録として注記）

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

`kiro.dev` の sitemap には **474 の URL** が登録されています（2026-08-16 実測。2026-08-01 時点は463 URL）。内訳は次のとおりです。

| 区画 | URL 数（2026-08-16） | URL 数（2026-08-01） | Kiro Web との関係 |
|------|-------------------|-------------------|-----------------|
| `docs/`（IDE ＋ 共有ドキュメント） | 188 | 117 | 共有ドキュメントのみ関係する |
| `changelog/` | 109 | 104 | **`changelog/web/` の 7 件が本サイトの対象** |
| `docs/cli/` | 35 | 101 | 別製品（Kiro CLI） |
| `blog/` | 92 | 88 | Kiro Web 関連が 3 本 |
| **`docs/web/`** | **15** | 20 | **本サイトの主対象**（5ページ移転） |
| その他（トップページ・製品ページなど） | 35 | 33 | — |

> ⚠️ **`docs/`（IDE＋共有）と `docs/cli/` の区分自体が大きく変化しています**（117→188・101→35）。
> 2026-08 の公式サイト再構成で、多数のページが CLI 区分から IDE/共有区分に移動した可能性がありますが、
> **この再構成の詳細は本作業の範囲外**（Kiro Web に直接関係しないため）であり、**未確認**です。
> 本サイトが扱う `docs/web/` の増減（20→15）とその移転先（IDE/共有区分内の `docs/specs/`・`docs/steering/`・
> `docs/privacy-and-security/`）のみを対象とします。

**Kiro Web の一次情報は `docs/web/` の 18 ページと `changelog/web/` の 19 エントリ**です。この **37 件**が本サイトの収録範囲の中核になります。2026-08-01 時点の 27 件とページ移転の記録は、前記の当時実測値として参照してください。

---

## Kiro Web の情報が置かれている4か所

| # | 場所 | 内容 | 本サイトでの位置づけ |
|---|------|------|------------------|
| 1 | <https://kiro.dev/changelog/web/> | 更新履歴（**19 エントリ**・2025-12-02 〜 2026-09-01） | **更新内容と日付の正**。[02_update](../02_update/01_changelog.md) に全量掲載 |
| 2 | <https://kiro.dev/docs/web/> | 公式ドキュメント（**18 ページ**） | **機能仕様・設定・リファレンス値の正** |
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
| **Web** | `changelog/web/` | **19** | ✅ **全件収録** |
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
| **Web** | **`page/2` が存在**（snapshot: 2026-09-05） |

Web は現在19エントリで `page/2` を含む複数ページです。**`/changelog/<系列>/page/N/` はこの公式サイトの一般的な仕組み**であり、本サイトの検証スクリプトはこの URL を新エントリとして数えず、索引ページとして巡回します。

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

| 区分 | URL パターン | ページ数（2026-08-16） | ページ数（2026-08-01） |
|------|------------|---------------------|---------------------|
| **Web** | `docs/web/…` | **15** | 20 |
| IDE ＋ 共有 | `docs/…`（`cli`・`web` 以外） | 188 | 117 |
| CLI | `docs/cli/…` | 35 | 101 |

### Kiro Web の 15 ページ（全量・2026-08-16 実測）

URL パスの階層で示します（**これが親子関係の正**）。

```
docs/web/                                  … Kiro Web の入口
├── setup/                                 … セットアップ（first-task を統合）
├── using-the-agent/                       … エージェントの使い方
│   ├── chatting/                          … チャット
│   └── creating-tasks/                    … タスクの作成
├── autonomous-mode/                       … Autonomous モード
├── automations/                           … Automations（定期実行）
├── sandbox/                               … サンドボックス
│   ├── environment-configuration/         … 環境の構成
│   ├── environment-variables/             … 環境変数・シークレット
│   ├── internet-access/                   … ネットワークアクセス
│   └── mcp/                               … Powers and MCP
├── github/                                … GitHub 連携
├── gitlab/                                … GitLab 連携
└── identity-center/                       … AWS Identity Center
```

各ページの本サイトでの配置は [サイト本体の README](../README.md) と各セクションの README を参照してください。

> **`sandbox/mcp` のタイトルは `Powers and MCP`**（2026-08-01 のスナップショット時点で既にこの表記だったため、
> 2026-08 の更新による変更ではない）。

### 移転したページ（2026-08 の再構成）

**5ページが移転しました。旧 URL は HTTP 200 を返すが実体のない移転スタブ**であり、
ステータスコードだけを見る検査では検出できません（`check-urls.sh` にスタブ検出を実装済み。
`moved to <a href="..."` を本文から検出する方式）。

| 旧パス（`docs/web/` 配下） | 移転先 | 移転先の区分 | Web 固有記述の有無 |
|--------------------------|-------|------------|------------------|
| `first-task/` | `docs/web/setup/` | Web（統合） | ✅ 全内容が統合され残存 |
| `specs/` | `docs/specs/` | Features（全製品共通） | 🔴 **0件（消滅）**。「Differences from the IDE」節も消滅 |
| `steering/` | `docs/steering/` | Features（全製品共通） | 🟡 4件残存（内容は本サイトの記載と一致） |
| `data-protection/` | `docs/privacy-and-security/data-protection/` | 共通（IDE/CLI/Web統合ページに変化） | 🟡 Free Tier記述14件は残存。ページ全体がIDE/CLI/Web共通に構造変化 |
| `firewalls/` | `docs/privacy-and-security/firewalls/` | 共通（Surface-specific タブ構成） | 🟡 Web タブに34行が残存（変化なしを実測確認済み） |

> **移転先が全製品共通ページになった場合、Web 固有の記述が失われている場合があります**
> （`docs/specs/` が実例）。移転先の URL を単純に置換するだけでは不十分で、
> **ページ単位で内容を判定する必要があります**（詳細は [02_information-sources.md](02_information-sources.md)）。

### 共有ドキュメント（Shared）

Web 専用ではないものの Web にも関わるページがあります（`llms.txt` の `## Shared` 区分・2026-08-16 実測で34ページ。2026-08-01 時点は31ページ）。

| ページ | Web との関わり |
|-------|--------------|
| `docs/billing/…` | サブスクリプション・課金 |
| `docs/models/…` | 利用できるモデル |
| `docs/privacy-and-security/…` | プライバシー・セキュリティ（**data-protection・firewalls の移転先**） |
| `docs/migrating-from-q-developer/…` | Amazon Q Developer からの移行 |
| `docs/specs/`・`docs/steering/`（2026-08-16 新設） | **specs・steering の移転先**（Features 区分） |
| `docs/cloud-sessions/`（2026-08-16 新設） | **Kiro Web の全セッションの実行環境**（[01_features/07_cloud-sessions.md](../01_features/07_cloud-sessions.md)） |

本サイトは**Web に関わる範囲でのみ**これらを参照します。

### 公式が Web docs から他製品・共有ページへ張っているリンク

`docs/specs`・`docs/specs/bugfix-specs`・`docs/steering`・`docs/mcp/security`（2026-08-04 更新で `docs/cli/mcp/security` から変更）・`docs/powers`・`docs/mcp`（2026-08-04 新設リンク）・`docs/privacy-and-security/vpc-endpoints`・`docs/troubleshooting`・`docs/enterprise/concepts`・`docs/enterprise/settings`・`docs/enterprise/governance`・`docs/enterprise/monitor-and-track/user-activity`・`docs/cloud-sessions`（2026-08-16 新設リンク）

本サイトでこれらに触れるときは、**別製品または共有ドキュメントであること**を明示します。

---

## 機械可読な索引（sitemap と llms.txt）

公式サイトには機械可読な索引が2種類あり、**中身が違います**。

| 索引 | URL | 内容 | 総数（2026-08-16） | 総数（2026-08-01） |
|------|-----|------|------------------|------------------|
| **sitemap** | <https://kiro.dev/sitemap.xml> | サイト全体の URL（docs・changelog・blog・製品ページ） | **474 URL** | 463 URL |
| **llms.txt** | <https://kiro.dev/llms.txt> | ドキュメントの索引を **IDE / CLI / Web / Shared / Optional** に区分 | **194 URL** | 203 URL |

### llms.txt の区分と件数（2026-08-16 実測）

| 区分 | 件数（2026-08-16） | 件数（2026-08-01） |
|------|------------------|------------------|
| IDE | 89 | 64 |
| CLI | 35 | 66 |
| **Web** | **15** | 20 |
| Shared | 34 | 31 |
| Optional | 21 | 22 |

> ⚠️ **IDE・CLI 区分の件数変化（64→89・66→35）が Web の変化（20→15）より大きい。**
> `docs/cli/` の sitemap 件数も 101→35 に減少しており、**CLI 区分の多数のページが
> IDE/共有区分に統合された可能性**がありますが、これは本サイトの収録範囲外（Kiro Web に
> 直接関係しない）のため**未確認のまま**とします。

### ⚠️ llms.txt は docs を網羅していません

sitemap の docs ページ（2026-08-16 実測: 237 件。2026-08-01 時点は238件）と `llms.txt`（194 件）を突き合わせると、**sitemap にあって `llms.txt` に無いページが 43 件**あります（2026-08-01 時点は36件）。

**Web 区分は sitemap と完全一致します**（どちらも同じ 15 ページ・差分 0）。

| 突き合わせ | 結果（2026-08-16） | 結果（2026-08-01） |
|-----------|------------------|------------------|
| Web 区分（`llms.txt`）と sitemap の `docs/web/` | **15 = 15・差分 0（完全一致）** | 20 = 20・差分 0 |
| docs 全体 | sitemap 237 vs `llms.txt` 194（**43 件が `llms.txt` に無い**） | sitemap 238 vs 203（36件） |

→ **Kiro Web の範囲では `llms.txt` をページ全量の根拠に使えます。** ただし他製品の範囲では欠落があるため、全量を数えるときは sitemap を併用します。

> **2026-08-16 実測で判明**: sitemapのみに存在する43件の区分を分析した結果、**全43件が IDE/共有区分**でした
> （`docs/cli/` の欠落は0件、`docs/web/` の欠落も0件）。2026-08-01時点の記録（36件のうち35件がCLI）とは
> 内訳が完全に変わっています。これは`docs/cli/`区分自体がsitemap上で101→35に減少したことと関連する
> 可能性がありますが、**この再構成の詳細は本サイトの収録範囲外のため未確認**です。

> **減った件数の内訳は特定できません。** Web 区分の5件減（20→15）は移転として確定していますが、
> `llms.txt` 全体の減少（203→194・9件減）のうち Web 以外の要因は未確認です
> （IDE・CLI・Shared・Optional のいずれの区分も件数が変化しているため、単純な差分計算では
> 内訳を特定できません）。

### llms.txt の URL は `.md` 付きです

`llms.txt` に載っている URL は `https://kiro.dev/docs/web/setup.md` のように **`.md` が付いた形**です（2026-08-16 実測時点で194/194 件）。この `.md` 版には既知の欠落があるため、本サイトは**値を HTML から取ります**。詳細は [02_information-sources.md](02_information-sources.md) を参照してください。

> **2026-08-12 の移転で `docs/web/specs.md`・`docs/web/firewalls.md` は404になりました**（実測）。
> 移転先の `.md`（`docs/specs.md`・`docs/privacy-and-security/firewalls.md` 等）は取得可能です。

### ⚠️ llms.txt の字下げはページ階層と一致しません

`llms.txt` の Web 区分では、項目の字下げが URL の階層と食い違う場合があります（2026-08-01時点で20件中7件）。2026-08-16時点の15ページでの再実測は今後の課題です。

→ **ページの親子関係は URL パスを正とします。** `llms.txt` の用途は「ページ全量と製品区分の判定」に限定します。

---

## URL の作法

公式サイトから情報を取るときに必要な作法が2つあります。どちらも実測で確認しています。

| # | 作法 | 実測 |
|---|------|------|
| 1 | **URL は末尾スラッシュを付ける** | `changelog` も `docs` も、スラッシュなしは **301 リダイレクト**（docs 15 ページを試して **15/15 が 301・本文 0 バイト**、スラッシュ付きで 15/15 が 200。2026-08-16 再実測） |
| 2 | **User-Agent を空にしない** | 空文字を明示指定すると **403**。`-A "Mozilla/5.0"` を付ければ確実 |

本サイトが載せる公式ページの URL は、この作法に合わせてすべて末尾スラッシュ付きにしています（機械検証しています）。

---

## 🔗 関連ページ

- [02_information-sources.md](02_information-sources.md) — 情報源の使い分けと落とし穴（`.md` の壊れ方・折りたたみ節）
- [02_update/01_changelog.md](../02_update/01_changelog.md) — 更新履歴（全19エントリ）
- 公式ドキュメント: <https://kiro.dev/docs/web/>
- 公式 changelog: <https://kiro.dev/changelog/web/>

---

[← 00_information に戻る](README.md)
