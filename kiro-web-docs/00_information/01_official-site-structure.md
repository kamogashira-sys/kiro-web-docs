# 公式サイトの構造マップ（Kiro Web の情報はどこにあるか）

> **本ページは Kiro Web 版（<https://app.kiro.dev>）に関する情報源の構造をまとめたものです。**
> Kiro IDE / Kiro CLI とは別製品であり、公式サイト上でも別のツリーに置かれています。
> **Kiro Web は [2026-09-01 に一般提供（GA）になりました](https://kiro.dev/changelog/web/kiro-web-is-now-generally-available/)。**

**出典**: <https://kiro.dev/docs/web/>・<https://kiro.dev/changelog/web/>・<https://kiro.dev/sitemap.xml>・<https://kiro.dev/llms.txt>
**実測日**: 2026-09-13（本ページの全数値はこの日に取得した一次情報の実測値。2026-08-16・2026-08-01 時点の値は変化の記録として注記）

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

`kiro.dev` の sitemap には **1,076 の URL** が登録されています（2026-09-13 実測。2026-08-16 時点は474 URL・2026-08-01 時点は463 URL）。

> ⚠️ **URL 数が倍増したのは、フランス語ロケール（`/fr/…`）が sitemap に載ったためです。**
> **1,076 = 英語 538 ＋ `/fr/` 538**（2026-09-13 実測）で、`/fr/docs/web/` も **18 件**あります。
> **日本語ロケールは sitemap にありません。**
> ロケール展開の方針について公式の説明は見つからないため**未確認**です。
> 以下の内訳は**英語 URL（538 件）のみ**を対象にしています。

| 区画 | URL 数（2026-09-13・英語のみ） | URL 数（2026-08-16） | Kiro Web との関係 |
|------|---------------------------|-------------------|-----------------|
| `docs/` 合計 | **249** | 188＋35 | — |
| ├ **`docs/web/`** | **18** | 15 | **本サイトの主対象** |
| ├ `docs/crew/` | 49 | （区分なし） | 別製品（Kiro Crew） |
| ├ `docs/cli/` | 35 | 35 | 別製品（Kiro CLI） |
| ├ `docs/ide/` | 24 | （`docs/` に含む） | 別製品（Kiro IDE） |
| └ その他 `docs/`（Features・共有ドキュメント等） | 123 | （`docs/` に含む） | **共有ドキュメントが関係する** |
| `changelog/` | 143 | 109 | **`changelog/web/` の 21 URL が対象**（一覧 ＋ `page/2` ＋ **19 エントリ**） |
| `blog/` | 99 | 92 | Kiro Web 関連が 3 本 |
| その他（トップページ・製品ページなど） | 47 | 35 | — |

> ⚠️ **`docs/` 配下の区分は 2026-08 以降も変わり続けています。**
> 2026-08-16 時点で存在しなかった **`docs/crew/`（49 ページ）と `docs/ide/`（24 ページ）**が
> 区分として現れています。**この再構成の詳細は本作業の範囲外**（Kiro Web に直接関係しないため）であり、**未確認**です。
> 本サイトが扱う `docs/web/` と、その移転先（`docs/specs/`・`docs/steering/`・`docs/cloud-sessions/`・
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
| **Web** | **`page/2` が存在**（snapshot: 2026-09-13） |

Web は現在19エントリで `page/2` を含む複数ページです。**`/changelog/<系列>/page/N/` はこの公式サイトの一般的な仕組み**であり、本サイトの検証スクリプトはこの URL を新エントリとして数えず、索引ページとして巡回します。

### Kiro Web の更新にバージョン番号はありません

Kiro IDE の `1.0.242` に相当する版番号が **Kiro Web には存在しません**。エントリの識別は**日付とタイトル（スラッグ）**のみです。

| 項目 | Kiro Web | Kiro IDE（対比） |
|------|---------|----------------|
| 更新の識別 | **日付 ＋ スラッグ** | 版番号 `1.0.NNN` |
| changelog の `.md` 版 | **無い**（**19/19 が 404**・2026-09-13 実測。`changelog/web.md` も 404） | 無い |
| フィード（Atom）への掲載 | **掲載される**（直近25件中 **7件** が `term="Web"`・2026-09-13 実測）。ただし**系列別フィードは 404** | 掲載される |

> 版番号が存在しない**理由**は公式に説明がないため**未確認**です。

### フィードは Kiro Web を配信対象にしています（2026-09-13 実測）

<https://kiro.dev/changelog/feed.atom>（全系列の統合フィード）を実測した結果です。

| 項目 | 実測値 |
|------|-------|
| フィード内の全 entry 数 | **25** |
| `<category term="Web">` を持つ entry | **7** |
| 該当エントリの範囲 | 2026-08-17 〜 2026-09-01 |
| 系列別フィード（`changelog/web/feed.atom`・`feed.xml`・`rss.xml`） | **すべて 404** |

> ⚠️ **以前は「直近25件に Web が0件」でした。** 2026-08-16 時点の実測では Web エントリが
> フィードのウィンドウ（直近25件）に入っていませんでしたが、
> **2026-09-13 時点では 7 件が入っています**。
> **フィードが Kiro Web を配信対象にしていることが確認できました。**
>
> ただし**フィードは直近25件しか保持しません**。Web の更新頻度が下がれば、
> 再びウィンドウから外れて 0 件になり得ます。**フィードだけでは取りこぼします。**
> 恒久的にウィンドウに含まれる保証があるかは**公式に記載がないため未確認**です。

---

## docs の区分構造

公式ドキュメントは URL のパスで製品が分かれます。

| 区分 | URL パターン | ページ数（2026-09-13） | ページ数（2026-08-16） | ページ数（2026-08-01） |
|------|------------|---------------------|---------------------|---------------------|
| **Web** | `docs/web/…` | **18** | 15 | 20 |
| Crew | `docs/crew/…` | 49 | （区分なし） | （区分なし） |
| CLI | `docs/cli/…` | 35 | 35 | 101 |
| IDE | `docs/ide/…` | 24 | （`docs/` に含む） | （`docs/` に含む） |
| Features・共有ドキュメント等 | `docs/…`（上記以外） | 123 | 188 | 117 |

### Kiro Web の 18 ページ（全量・2026-09-13 実測）

URL パスの階層で示します（**これが親子関係の正**）。

```
docs/web/                                  … Kiro Web の入口
├── setup/                                 … セットアップ（first-task を統合）
├── using-the-agent/                       … エージェントの使い方
│   ├── chatting/                          … チャット
│   ├── creating-tasks/                    … タスクの作成
│   └── file-explorer/                     … ワークスペースのファイル閲覧 ★未収録
├── autonomous-mode/                       … Autonomous モード
├── automations/                           … Automations（定期実行）
├── cloud-configuration/                   … 個人の .kiro 構成の同期 ★未収録
├── memory/                                … メモリ ★未収録・更新日なし
├── sandbox/                               … サンドボックス
│   ├── environment-configuration/         … 環境の構成
│   ├── environment-variables/             … 環境変数・シークレット
│   ├── internet-access/                   … ネットワークアクセス
│   └── mcp/                               … Powers and MCP
├── github/                                … GitHub 連携
├── gitlab/                                … GitLab 連携
└── identity-center/                       … AWS Identity Center
```

> ★ **3ページは本サイトに対応する解説がありません**（2026-09-13 時点）。
> 理由と各ページの節構成は
> [02_information-sources.md](02_information-sources.md#本サイトが未収録の公式ページ3件) に記録しています。

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

### 共有ドキュメント（サーフェス横断のページ）

Web 専用ではないものの Web にも関わるページがあります。

> ⚠️ **`llms.txt` の `## Shared` 区分は無くなりました**（2026-09-13 実測）。
> 現在は `## Features`（45）・`## Privacy and Security`（8）・`## Commands and Reference`（5）・
> `## Start here`（9）・`## Guides`（6）などに分割されています（**合計 82**）。
> 2026-08-16 時点の `Shared` 区分（34ページ）に対応する単一の区分は現在ありません。

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

| 索引 | URL | 内容 | 総数（2026-09-13） | 総数（2026-08-16） |
|------|-----|------|------------------|------------------|
| **sitemap** | <https://kiro.dev/sitemap.xml> | サイト全体の URL（docs・changelog・blog・製品ページ）。**`/fr/` を含む** | **1,076 URL**（英語 538） | 474 URL |
| **llms.txt** | <https://kiro.dev/llms.txt> | ドキュメントの索引を区分ごとに列挙 | **257 行**（一意 URL は **248**） | 194 URL |

### llms.txt の区分と件数（2026-09-13 実測）

区分の構成そのものが変わっています（`Crew`・`Mobile - Preview` などが新設）。

| 区分 | 件数（2026-09-13） | 区分（2026-08-16） | 件数（2026-08-16） |
|------|------------------|------------------|------------------|
| Features | 45 | Shared | 34 |
| **Web** | **18** | **Web** | **15** |
| CLI | 35 | CLI | 35 |
| Crew | 48 | （区分なし） | — |
| IDE 1.x | 23 | IDE | 89 |
| Enterprise | 22 | — | — |
| Optional | 27 | Optional | 21 |
| Start here | 9 | — | — |
| Privacy and Security | 8 | — | — |
| Guides | 6 | — | — |
| Commands and Reference | 5 | — | — |
| Get Started / Models / Migration | 3 / 3 / 3 | — | — |
| Billing / Mobile - Preview | 1 / 1 | — | — |
| **合計（行数）** | **257** | — | 194 |

> ⚠️ **区分名が置き換わったため、区分ごとの件数を前回と直接比較できません。**
> 旧 `Shared` 区分に相当するのは現在の `Features`・`Privacy and Security` などです。
> **Web 区分（15→18）だけは前後で同じ意味**なので比較できます。
> 区分再編の理由・対応関係について公式の説明はないため**未確認**です。

### llms.txt は docs をほぼ網羅するようになりました

sitemap の docs ページ（**2026-09-13 実測: 249 件**）と `llms.txt`（一意 248 件）を突き合わせると、
**sitemap にあって `llms.txt` に無いページは 1 件だけ**です（`docs/` のトップ）。

| 突き合わせ | 結果（2026-09-13） | 結果（2026-08-16） |
|-----------|------------------|------------------|
| Web 区分（`llms.txt`）と sitemap の `docs/web/` | **18 = 18・差分 0（完全一致）** | 15 = 15・差分 0 |
| docs 全体 | sitemap 249 vs `llms.txt` 248（**`llms.txt` に無いのは `docs/` の1件のみ**） | sitemap 237 vs 194（43件が欠落） |
| `llms.txt` にあって sitemap に無い | **0 件** | （未計測） |

→ **Kiro Web の範囲では `llms.txt` をページ全量の根拠に使えます**（2026-08-16 時点から変わらず差分 0）。

> ⚠️ **2026-08-16 時点にあった「43件の欠落」は解消しています。**
> 当時は sitemap のみに存在するページが 43 件（全件 IDE/共有区分）ありましたが、
> **2026-09-13 実測では 1 件（`docs/` トップ）だけ**です。
> 解消の理由について公式の説明はないため**未確認**です。

### llms.txt の URL は `.md` 付きです

`llms.txt` に載っている URL は `https://kiro.dev/docs/web/setup.md` のように **`.md` が付いた形**です（**2026-09-13 実測で 248/248 件**）。この `.md` 版には既知の欠落があるため、本サイトは**値を HTML から取ります**。詳細は [02_information-sources.md](02_information-sources.md) を参照してください。

> **2026-08-12 の移転で `docs/web/specs.md`・`docs/web/firewalls.md` は404になりました**（実測）。
> 移転先の `.md`（`docs/specs.md`・`docs/privacy-and-security/firewalls.md` 等）は取得可能です。

### ⚠️ llms.txt の字下げはページ階層と一致しません

`llms.txt` の Web 区分では、項目の字下げが URL の階層と食い違う場合があります（**2026-09-13 実測で 18 件中 2 件**。2026-08-01 時点は20件中7件）。

食い違っているのは次の2件です。URL の階層は 1 段（`docs/web/…`）ですが、字下げは 2 段分（4スペース）になっています。

| 項目 | URL の階層 | 字下げ |
|------|----------|-------|
| `web/github` | 1 段 | **2 段分** |
| `web/gitlab` | 1 段 | **2 段分** |

→ **字下げを親子関係の根拠にしてはいけません。** 本サイトは [URL パスの階層](#kiro-web-の-18-ページ全量2026-09-13-実測)を正としています。

→ **ページの親子関係は URL パスを正とします。** `llms.txt` の用途は「ページ全量と製品区分の判定」に限定します。

---

## URL の作法

公式サイトから情報を取るときに必要な作法が2つあります。どちらも実測で確認しています。

| # | 作法 | 実測 |
|---|------|------|
| 1 | **URL は末尾スラッシュを付ける** | `changelog` も `docs` も、スラッシュなしは **301 リダイレクト**（2026-09-13 実測でも `docs/web`・`web/setup`・`web/sandbox`・`web/github`・`web/memory` の **5/5 が 301・本文 0 バイト**。2026-08-16 は docs 15 ページ全件で 15/15 が 301・スラッシュ付きは 15/15 が 200） |
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
