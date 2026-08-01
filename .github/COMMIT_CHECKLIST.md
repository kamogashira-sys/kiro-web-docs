# コミット前チェックリスト

このチェックリストは、ドキュメントの品質を保証するために、コミット前に必ず確認してください。

> **Kiro Web にはバージョン番号がありません。** IDE/CLI 版のチェックリストにある「バージョン番号の確認」は、
> 本サイトでは「**日付＋スラッグの確認**」に置き換わります（[ワークフロー](WORKFLOW.md)参照）。

---

## 🚫 必須確認事項

### 1. 出典の確認

- [ ] 全ての技術的記述に一次情報の出典がある
- [ ] changelog の内容は公式 changelog（<https://kiro.dev/changelog/web/>）で確認済み
- [ ] 機能仕様・設定値は公式ドキュメント（<https://kiro.dev/docs/web/>）に基づく
- [ ] 各ページに**出典日**（`Page updated` の日付）を記載している
- [ ] 公式に確認できない事項は「未確認」と明示している（推測で断定していない）

### 2. 表現の確認

- [ ] 推測表現（「おそらく」「と思われる」等）を使用していない
- [ ] 「以降」「以前」等の曖昧な表現を避けている
- [ ] 断定的な記述には必ず根拠がある
- [ ] **公式に書かれていない理由・因果・意図を書いていない**（「〜のため」「〜だから」に出典があるか）
- [ ] **Kiro Web / Kiro IDE / Kiro CLI を混同していない**（IDE/CLI の仕様を Web の記述として書いていないか）
- [ ] Kiro Web が **Preview 段階**であることをサイト冒頭で明示している

### 3. 値の取得元の確認

- [ ] **表の値・パス・件数を HTML から取った**（`.md` companion を鵜呑みにしていない）
- [ ] `web/firewalls` の内容に `.md` を使っていない（**3サーフェス分が連結されている**）
- [ ] `${key_name}`・`${aws:SourceIdentity}` 等のプレースホルダを HTML から取った（`.md` では `` `$` `` に潰れる）
- [ ] changelog の**折りたたみ節（Improvements・Fixes）の項目を1つも省略していない**

### 4. リンクの確認

- [ ] 全ての内部リンクが有効である（相対パス）
- [ ] 全ての外部リンクが有効である
- [ ] **kiro.dev の URL は末尾スラッシュ付き**（`changelog` も `docs` も、スラッシュなしは **301 リダイレクト**になる）
- [ ] 姉妹サイト（IDE/CLI 版）へのリンクに「**別製品**」であることを明記している

### 5. 公開範囲の確認

- [ ] ローカル管理対象（`work_plans/`・`05_meta/`・`06_embedded-docs/`・`work_records/`）がコミットに含まれていない
- [ ] **ローカル絶対パス・ユーザー名が公開ファイルに含まれていない**（`check-ignore.sh` が機械検出します）

---

## 📋 changelog エントリの確認（版番号がないため）

### 正準キーは「日付＋スラッグ」

```bash
# 索引（スラッグ・日付・タイトル）— 末尾スラッシュ必須。空 UA は 403
curl -sS -A "Mozilla/5.0" -o /tmp/web-idx.html "https://kiro.dev/changelog/web/"

# エントリ本文
curl -sS -A "Mozilla/5.0" -o /tmp/web-entry.html "https://kiro.dev/changelog/web/<slug>/"
```

### ⚠️ 折りたたみ節の中身は素の HTML に存在しません

`Improvements`・`Fixes` は Radix UI のアコーディオンで、レンダリング済み HTML では **`hidden` な空 div** です。
`<article>` 内の `<li>` を数えると **0 件**になります（実際にそう誤測定しました）。

**中身は RSC ペイロードにのみあります。** 抽出には専用スクリプトを使ってください。

```bash
python3 scripts/kiro-web-docs/extract-changelog.py --entry /tmp/web-entry.html
```

> RSC は**エスケープされた JSON**（`\"title\":\"...\"`）です。素の JSON 前提の正規表現
> （`"patches"\s*:\s*\[...\]` など）は **0 件**になります。

### 日付の扱い

- 正は**公式ページの表示日**。本サイトでは **ISO `YYYY-MM-DD`** に変換して記載
- **索引は略記（`Jul 1, 2026`）・エントリページは月名フル（`July 1, 2026`）**。両形式に対応すること
- ⚠️ **May は両形式が同形**。May のエントリだけを見て形式を判定しない
- docs の出典日は **JSON-LD の `dateModified`**（ISO 形式）から取るのが確実
- ⚠️ 表示側は `Page updated: <!-- -->June 18, 2026` と**コメントが挟まる**
- **タイムゾーン変換は行わない**
- **取得日は本文に書かない**（作業記録に残す）

---

## 🔍 検証方法

### 自動検証

```bash
cd <リポジトリのルート>
make check-kiro-web-quick    # 執筆中の常用（links / structure のみ）
make check-kiro-web-ignore   # 公開範囲の機械確認（コミット前に必須・exit 0 必須）
make check-kiro-web-all      # コミット前・公開前
```

> **`check-kiro-web-quick` は全チェックではありません**（links / structure のみ）。
> 執筆中の素早い確認用です。**コミット前には `check-kiro-web-all` を実行してください**
> （利用可能なターゲットは `make` で確認できます）。

> ⚠️ **`check-kiro-web-all` の exit 0 は「全部を検証した」を意味しません**。
> 網羅性チェック（`check-kiro-web-coverage`）は**一次情報のスナップショットが無いと
> スキップして成功扱い**になります（クローン直後・CI）。スキップ時は出力に
> 「**未検証です**」と表示されるので、必ず出力を読んでください。
>
> 外部情報源に依存する検証（外部 URL の到達性・新エントリ検知）は **Phase 3 で追加予定**です。
> `all` には含めません（ネットワーク障害やレート制限で CI が赤くなるのを避けるため）。

### 手動検証

1. **出典の確認** — 技術的記述に出典リンクと出典日があるか／リンクが有効か
2. **日付＋スラッグの確認** — 公式 changelog と一致するか
3. **推測表現の確認** — 「おそらく」「と思われる」等がないか／**理由を勝手に補っていないか**
4. **Web / IDE / CLI の区別** — 他製品の仕様を Web の記述として書いていないか

---

## ✅ コミット前の最終確認

- [ ] 全てのチェック項目を確認した
- [ ] **`make check-kiro-web-all` を実行した（exit 0）** — `quick` では代用できません
- [ ] `make check-kiro-web-ignore` を実行した（exit 0）
- [ ] 検証スクリプトを新規作成・改修した場合、**規則ごとにネガティブテスト**を行い、`diff` で復元を検証した
- [ ] 公開範囲の確認を実施した（`git status` ＋ `git check-ignore`）
- [ ] コミットメッセージが明確である

---

## 📝 コミットメッセージガイドライン

### フォーマット

```
<type>: <subject>

<body>

<footer>
```

### Type

- `docs`: ドキュメント変更
- `chore(scripts)`: 検証スクリプト変更
- `chore(ci)`: CI 設定変更
- `fix`: 誤記・リンク切れ等の修正
- `chore`: その他のツール・設定変更

### 例

**版番号がないため、subject には日付とエントリ名を書きます。**

```
docs: 2026-07-01 エントリ対応（IAM ロール・Powers の認可）

- changelog にエントリを追加（W-L2）
- 04_reference/02_environment-variables.md に IAM 信頼ポリシーを追記
- 出典日: 2026-07-01

出典: https://kiro.dev/changelog/web/iam-roles-and-authorize-powers-for-third-party-services/
```

---

## 🔗 関連ドキュメント

- [ドキュメント作成ワークフロー](WORKFLOW.md)
- [サイト本体 README](../kiro-web-docs/README.md)

---

**最終更新**: 2026-08-01
