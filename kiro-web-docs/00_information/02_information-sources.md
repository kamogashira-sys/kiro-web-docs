# 情報源の使い分けと落とし穴

> **本ページは Kiro Web 版（<https://app.kiro.dev>）の情報を公式サイトから読み取るときの注意をまとめたものです。**
> Kiro IDE / Kiro CLI とは別製品です。**Kiro Web は [2026-09-01 に一般提供（GA）になりました](https://kiro.dev/changelog/web/kiro-web-is-now-generally-available/)。**

**出典**: <https://kiro.dev/docs/web/>・<https://kiro.dev/changelog/web/>
**実測日**: 2026-09-13（本ページの全数値はこの日に取得した一次情報の実測値。2026-08-16・2026-08-01 時点の値は変化の記録として残している）

公式サイトから Kiro Web の情報を読むとき、**同じページでも読み方によって内容が変わってしまう**場所があります。本ページはその落とし穴と、本サイトがどう対処しているかをまとめています。

---

## 📑 このページの内容

1. [情報源の優先順位](#情報源の優先順位)
2. [落とし穴1: `.md` 版は値が壊れていることがある](#落とし穴1-md-版は値が壊れていることがある)
3. [落とし穴2: 折りたたまれた項目は HTML に存在しない](#落とし穴2-折りたたまれた項目は-html-に存在しない)
4. [落とし穴3: 日付の表記が2種類ある](#落とし穴3-日付の表記が2種類ある)
5. [落とし穴4: changelog に載らない更新がある](#落とし穴4-changelog-に載らない更新がある)
6. [落とし穴5: 公式ページ間で記述が食い違うことがある](#落とし穴5-公式ページ間で記述が食い違うことがある)
7. [本サイトの検証方法](#本サイトの検証方法)

---

## 情報源の優先順位

上位が下位を上書きします。**下位だけを根拠に書くことはしません。**

| 順位 | 情報源 | 用途 | 制約 |
|-----|-------|------|------|
| **1** | `changelog/web/<スラッグ>/` の各エントリ | 更新内容・日付 | **折りたたみ節の中身は HTML に無い**（[落とし穴2](#落とし穴2-折りたたまれた項目は-html-に存在しない)）。`.md` 版は無い（7/7 が 404） |
| **2** | 公式ドキュメント（**HTML を正**） | 機能仕様・設定・値 | `.md` 版に既知の欠落あり（[落とし穴1](#落とし穴1-md-版は値が壊れていることがある)） |
| **3** | `llms.txt` | **ページ全量と製品区分の判定のみ** | 字下げをページ階層の根拠にしない |
| **4** | `sitemap.xml` | ページ・エントリ全量の機械検証 | `page/N` はエントリではない |
| **5** | フィード（Atom / RSS） | **補助のみ** | `changelog/feed.atom`・`changelog/feed.rss` の **2 本**。どちらも**直近25件中 7 件が Web**（2026-09-13 実測）。**系列別フィードは 404**。25件のウィンドウしか無く、Web 全 19 エントリのうち **7 件しか入らない**ため**取りこぼす**（[詳細](01_official-site-structure.md#フィードは-kiro-web-を配信対象にしています2026-09-13-実測)） |
| **6** | Kiro Web 実機（`app.kiro.dev`） | 公式記述の曖昧さの解消 | 有料サブスクリプションが必要。**本サイトは実機確認を行っていません** |
| **7** | 公式ブログ（3本） | 背景の補足 | 本文の主たる根拠にしない |

> 本サイトは**順位1・2で確認できないことは「未確認」と明示**し、断定しません。
> 公式に書かれていない**理由・因果も書きません**（例: 「なぜ版番号が無いのか」）。

---

## 落とし穴1: `.md` 版は値が壊れていることがある

公式ドキュメントは URL に `.md` を付けると Markdown 版が取れます（例: <https://kiro.dev/docs/web/setup.md>）。読みやすく便利ですが、**2026-09-13 時点の Kiro Web 18 ページ中 2 ページで内容が壊れています**（2026-08-16 時点は15ページ中2ページ・2026-08-01 時点は20ページ中3ページ。壊れていた `firewalls` は移転により Web ページの対象外になった）。

> ⚠️ **2026-08 の公式サイト再構成で移転したページは `.md` 版も移転先で取得し直す必要があります。**
> 旧 `docs/web/specs.md` は移転後に**404**になりました（実測。旧ページ自体が移転スタブになったため）。
> 移転先の `.md` は `docs/specs.md` です。

全 18 ページで HTML 版と `.md` 版を機械的に突き合わせて確認した結果です（2026-09-13 実測）。

### (a) プレースホルダが潰れる（2ページ）

設定に書くべき記法が、`.md` 版では**意味を失った形**になります。

| ページ | HTML 版（正しい） | `.md` 版（壊れている） |
|-------|-----------------|-------------------|
| `web/sandbox/mcp` | Use the **`${key_name}`** syntax | Use the **`$`** syntax |
| `web/sandbox/environment-configuration` | use **`${aws:SourceIdentity}`** in resource paths | use **`$`** in resource paths |

**壊れるのは本文中のインラインコードだけで、コードブロックの中は保持されています**（2026-09-13 実測）。

| ページ | `.md` に残る `${...}` | 潰れた箇所 |
|-------|--------------------|----------|
| `web/sandbox/mcp` | **2件**（いずれも JSON コードブロック内の `${my_env_var_key}`・`${my_secret_key}`） | インラインの `${key_name}` が **1箇所** |
| `web/sandbox/environment-configuration` | **3件**（いずれも JSON コードブロック内の `${aws:SourceIdentity}` 2件・`${aws:PrincipalTag/KiroSessionId}` 1件） | インラインの `${aws:SourceIdentity}` が **1箇所** |

> `.md` 版だけを読むと「`$` と書けばよい」と誤解します。**何を書けばいいのか分からなくなる**壊れ方です。

この2ページは本サイトの [04_reference/02_environment-variables.md](../04_reference/) と [04_reference/03_mcp-configuration.md](../04_reference/) の元になるため、**値はすべて HTML から取っています**。

### (b) 3製品分の内容が連結される（旧1ページ・2026-08-12に移転）

`web/firewalls` は2026-08-12に`docs/privacy-and-security/firewalls/`へ移転しました。**移転先も
`.md` 版には Kiro Web 以外の内容が混ざっています**（実測: 2026-08-16）。

| 版 | サイズ・状態（2026-08-01・旧URL） | サイズ・状態（2026-08-16・新URL） |
|----|----------------------------------|----------------------------------|
| `docs/web/firewalls.md` | 12,349 バイト | **404（実測。旧URL自体が移転スタブになったため）** |
| `docs/privacy-and-security/firewalls.md` | 12,349 バイト（3サーフェス一致） | **10,844 バイト**（サイズが変化） |
| `docs/cli/privacy-and-security/firewalls.md` | 12,349 バイト（3サーフェス一致） | **404（実測）** |

> ⚠️ **「3サーフェスの `.md` が完全一致する」という旧知見は、2026-08-16時点で崩れています。**
> `docs/cli/` 区分の sitemap 件数が 101→35 に大幅減少しており（[01_official-site-structure.md](01_official-site-structure.md)参照）、
> `docs/cli/privacy-and-security/firewalls.md` もこの変化の影響で404になったと考えられますが、
> **CLI側の再構成の詳細は本サイトの収録範囲外のため未確認**です。

移転先の `.md` 版には以下の見出しが依然含まれています（Kiro Web 以外の内容）:

| 見出し | 内容 |
|-------|------|
| `Optional URLs` | IDE/CLI 向けの Extensions・Powers/MCP エンドポイント |
| `Proxy configuration` | IDE/CLI 向けのプロキシ設定 |
| `Troubleshooting connection issues` | IDE 向けのトラブルシューティング |
| `Data perimeters` | 全製品共通のデータ境界の説明 |
| `AWS GovCloud` | 全製品共通の GovCloud エンドポイント |

→ **本サイトは移転後も `web/firewalls`（現 `privacy-and-security/firewalls`）について `.md` 版を使いません。HTML 版のみを出典にします。**

### (c) 見出しの集合は全ページで一致します

見出しの集合は HTML と `.md` で一致します（**2026-09-13 実測。Web 18 ページ全件**で、`.md` だけの見出し・HTML だけの見出しがともに 0 件）。

**ただし「見出しが一致すること」は「本文の値が一致すること」を意味しません。** 本サイトは**表の値・パス・件数を全 18 ページで HTML から取る**方針にしています。

---

## 落とし穴2: 折りたたまれた項目は HTML に存在しない

`changelog/web/` の一部のエントリには、`Improvements` と `Fixes` という**折りたたまれた節**があります。公式サイトでは初期状態で閉じています。

**この中身は、ページの HTML を取得しても入っていません。** 折りたたみは JavaScript で描画される仕組み（Radix UI のアコーディオン）で、取得した HTML には**中身が空の隠し要素**しかありません。

| 確認方法 | 結果 |
|---------|------|
| 取得した HTML の記事部分から箇条書き（`<li>`）を数える | **0 件** |
| ページに埋め込まれたデータ（React Server Components のペイロード）から取る | **21 件** |

該当するエントリと項目数:

| エントリ | Improvements | Fixes | 計 |
|---------|-------------|-------|---|
| [2026-05-19 Session Stability, Stop Control, and Mobile Layout Fixes](../02_update/01_changelog.md#2026-05-19-session-stability-stop-control-and-mobile-layout-fixes) | 5 | 6 | 11 |
| [2026-06-02 Start Without a Repo, Switch Modes Anytime](../02_update/01_changelog.md#2026-06-02-start-without-a-repo-switch-modes-anytime) | 3 | 7 | 10 |
| **合計** | **8** | **13** | **21** |

> **公式が公開している 21 項目が、素直に読むと丸ごと抜け落ちます。**
> 本サイトはこの21項目を[更新履歴](../02_update/01_changelog.md)に**全量掲載**し、
> 項目数が公式と一致することを機械検証しています。

サンドボックスのディスク容量（**128GB**）のように、**リファレンスに載せるべき値がこの折りたたみの中にしかない**ケースもあります。

---

## 落とし穴3: 日付の表記が2種類ある

同じ日付が、見る場所によって違う形で書かれています。

| 場所 | 表記 | 例 | 実測（2026-09-13） |
|------|------|---|------|
| changelog の索引ページ（1ページ目・2ページ目） | **略記** | `Aug 11, 2026` | **16 種**（1ページ目 9 種＋2ページ目 7 種）。月名フルは **0 件** |
| changelog の各エントリページ | **月名フル** | `July 1, 2026` | **19/19 件**（略記は **0 件**） |
| docs の各ページ | 月名フル | `Page updated: September 2, 2026` | **17/18 件**（`web/memory` のみ `Page updated` が無い） |

**⚠️ 5月だけは略記と月名フルが同じ形**（`May` = `May`）です。5月のエントリだけを見ても、どちらの表記なのか判別できません（**2026-09-13 実測でも索引2ページ目に `May` の2件が該当**）。

本サイトは**すべて ISO 形式（`YYYY-MM-DD`）に統一**しています。**タイムゾーンの変換は行いません**（公式の表示日をそのまま日付として扱います）。

### docs ページの更新日は機械可読な形でも入っています

各 docs ページには構造化データ（JSON-LD）が埋め込まれており、`dateModified` に **ISO 形式**の更新日が入っています。**`Page updated` を持つ 17 ページすべてで画面表示と一致**しました（2026-09-13 実測）。

| 実測項目 | 結果（2026-09-13） |
|---------|------------------|
| `Page updated` と `dateModified` が一致 | **17 ページ** |
| 不一致 | **0 ページ** |
| どちらも無い | **1 ページ**（`web/memory`） |

> ⚠️ **`Page updated` の日付は連続した文字列として取り出せません。**
> ラベル自体は素の HTML にあります（**17/18 ページ**。`web/memory` のみ無い）が、
> 日付の値が React のコメントマーカーで分断されています（2026-09-13 実測）。
>
> ```html
> <span>Page updated:<!-- --> <!-- -->September 2, 2026</span>
> ```
>
> このため `grep 'Page updated: September 2, 2026'` は **18 ページすべてで 0 件**になります。
> 一方 **`dateModified`（JSON-LD）は連続した ISO 形式**なので、機械照合にはこちらが向きます。
> 本サイトは `check-consistency.py` で**各ページの出典日を snapshot の `dateModified` と機械照合**しています。

---

## 落とし穴4: changelog に載らない更新がある

**公式ドキュメントの更新は、必ずしも changelog に載りません。**

2026-09-13 時点で、**最新の changelog エントリ（2026-09-01）より後に更新された docs ページが 10 件**あります（2026-08-16 時点は11件・2026-08-01 時点は4件）。

| ページ | 更新日（2026-09-13 実測） | 本サイトの収録 |
|-------|-------------------------|--------------|
| `web/`（トップ） | 2026-09-02 | 収録（複数ページの出典） |
| `web/setup` | 2026-09-02 | 収録 |
| `web/identity-center` | 2026-09-02 | 収録 |
| `web/using-the-agent` | 2026-09-02 | 収録 |
| `web/autonomous-mode` | 2026-09-02 | 収録 |
| `web/sandbox/mcp` | 2026-09-02 | 収録 |
| `docs/steering`（移転先） | 2026-09-02 | 収録 |
| `docs/cloud-sessions`（移転先） | 2026-09-02 | 収録 |
| `web/sandbox/environment-configuration` | **2026-09-10** | 収録（**docs で最も新しい更新**） |
| `web/cloud-configuration` | 2026-09-02 | **未収録**（[後述](#本サイトが未収録の公式ページ3件)） |

→ **「最新の changelog エントリの日付」だけを見ていると、仕様変更を見落とします。**
本サイトは各ページに**公式の出典日**（`Page updated` の日付）を記載し、docs 側の更新も監視対象にしています。
`check-freshness.py` の S4（docs 最新更新日）は実測値（**2026-09-10**）に同期しています。

> **2026-09-13 の実測で、本サイトに未反映の内容変更が 6 ページ分見つかりました。**
> セッションのグループ化と自動命名（`web/using-the-agent`）・最近使ったリポジトリ（`web/setup`）・
> Cloud Sessions の有効化とリポジトリプロバイダ（`web/identity-center`）・
> サーフェス比較表（`docs/steering`）の 4 ページは、**上の 10 件に含まれます**。
>
> 残る 2 ページ（ブラウザ操作の `web/sandbox`・PR レビューの `web/github`）は
> **どちらも 2026-08-22 更新**で、上の 10 件には含まれません。
> **前回の作業時点でも出典日が古いまま残っていた**（`web/sandbox` は June 11・`web/github` は August 7 と記載していた）ため、
> 内容の差分にも気づけていませんでした。
>
> → **出典日の追随だけでは不十分**であり、かつ**出典日そのものが古いまま放置される事故も起きます**。
> 本サイトは対策として、出典日を公式の `dateModified` と**機械照合**するようにしました（後述）。

### 本サイトが未収録の公式ページ（3件）

**Kiro Web の公式 18 ページのうち、次の 3 ページは本サイトに対応する解説を置いていません**（2026-09-13 時点）。
気づいていないのではなく、**現時点で未収録であることを明示**します。

| ページ | 更新日 | 公式の節（h2 見出し・2026-09-13 実測） |
|-------|-------|---------|
| `web/cloud-configuration` | 2026-09-02 | What you can upload / Upload and review / How Powers sync / Apply cloud configuration to local sessions / Limits / After uploading |
| `web/using-the-agent/file-explorer` | 2026-08-22 | Open files from the conversation / Browse the workspace / View and download files / Limits |
| `web/memory` | **取得できず**（JSON-LD の `dateModified` が無い） | How Kiro builds memory / Memory vs. steering |

> `web/cloud-configuration` の内容の一部は
> [01_features/07_cloud-sessions.md](../01_features/07_cloud-sessions.md#構成情報の扱い)（Configuration Sync）で触れていますが、
> **ページ全体を対象にした解説はありません**。
> `web/memory` は**公式ページに更新日が無い**ため、本サイトの出典日の規則（`Page updated` の転記）を満たせません。

---

## 落とし穴5: 公式ページ間で記述が食い違うことがある

**Kiro Web に無料枠（Free Tier）があるかどうか**について、公式ページ間で記述が食い違っています（2026-09-13 時点・**未解決**）。

| 出典 | 記述の要旨 |
|------|-----------|
| `docs/web/`（`Page updated`: 2026-09-02） | 前提条件の 1 項目目が **`A Pro, Pro+, Pro Max, or Power subscription`**。本文に **`Kiro Web is available on Pro, Pro+, Pro Max, and Power plans.`** |
| `docs/web/setup/`（`Page updated`: 2026-09-02） | Kiro Web の利用には **Pro 以上**のサブスクリプションが必要（**`Ensure you have a paid Kiro subscription (Pro or higher). Kiro Web is not available on the free tier.`**） |
| `docs/cloud-sessions/`（`Page updated`: 2026-09-02・移転先） | 前提条件は **Pro / Pro+ / Pro Max / Power** のいずれか |
| `docs/privacy-and-security/data-protection/`（`Page updated`: 2026-08-04・移転先。旧 `docs/web/data-protection/` は2026-08-04以前は Page updated: 2026-07-14） | **Free Tier ユーザー**のデータ保持期間について記述がある（＝ Free Tier の存在を前提にしている） |

> ⚠️ **`docs/web/`（トップ）の前提条件は 2026-09-02 に表現が変わりました。**
> 2026-08-14 時点は **`A paid Kiro subscription (Pro or higher)`** でしたが、
> 2026-09-02 時点は **`A Pro, Pro+, Pro Max, or Power subscription`** というプラン列挙になり、
> **`Pro Max` が明示**されました。**要件そのものは存続しています。**
> **表現が変わった理由は公式に説明がないため未確認**です。食い違いそのものは**継続**しています。
>
> 「`Kiro Web is not available on the free tier`」という**明示的な否定文**は、
> 2026-09-13 時点で `docs/web/setup/` にのみあります（トップページには 2026-08-14 時点でも無い）。

### 本サイトの扱い

- **どちらが正しいかを断定しません**
- **両方の記述を示し、食い違いがあることを明記します**
- 「更新日が新しい方を採る」という機械的な判断も**しません**（食い違いの原因が更新漏れとは限らないため）

> 更新日の新しさは、一般には有力な手がかりです。しかし**それを根拠に一方を否定すると、
> 公式が書いていないことを本サイトが決めたことになります。** 本サイトの方針（推測しない）に反します。

この件は公式の是正を待つ扱いにしています。

---

## 本サイトの検証方法

上記の落とし穴は、気をつけていても人の目では取り逃します。本サイトは**機械検証**で担保しています。

| 検証 | 内容 |
|------|------|
| 更新履歴の網羅性 | 公式の全エントリが載っているか／日付・タイトルが一致するか／**折りたたみ21項目の数が一致するか**（宣言した件数と実際の箇条書きの数の両方） |
| リンク | 内部リンクとアンカーの実在／公式 URL が末尾スラッシュ付きか |
| 構成 | 各ページに「Kiro Web 版の仕様」の明示と**公式の出典 URL** があるか |
| 公開範囲 | 公開してはいけないファイルが混ざっていないか |

さらに、**検証スクリプトそのものが機能しているか**も確認しています。意図的にドキュメントを壊して「検出されること」を規則ごとに試し、その後で元に戻して差分がないことを検証する手順です。

---

## 🔗 関連ページ

- [01_official-site-structure.md](01_official-site-structure.md) — 公式サイトの構造マップ
- [02_update/01_changelog.md](../02_update/01_changelog.md) — 更新履歴（折りたたみ21項目も全量掲載）
- [04_reference](../04_reference/) — HTML から取った値の一覧
- 公式ドキュメント: <https://kiro.dev/docs/web/>

---

[← 00_information に戻る](README.md)
