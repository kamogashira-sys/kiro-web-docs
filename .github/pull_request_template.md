# Pull Request

## Description

Brief description of the changes in this PR.

## Type of Change

Please delete options that are not relevant.

- [ ] 🐛 Bug fix (typo, wrong value, broken link)
- [ ] ✨ New documentation (new page or section)
- [ ] 💥 Breaking change (section restructure, file rename/move)
- [ ] 📚 Documentation update (existing page updated for a new Kiro Web changelog entry or docs update)
- [ ] 🔧 Maintenance (scripts, CI, templates)

## Changes Made

- [ ] Updated documentation files
- [ ] Added new documentation
- [ ] Fixed typos or errors
- [ ] Improved formatting or structure
- [ ] Updated examples or code snippets
- [ ] Other: _______________

## Sections Updated

- [ ] `kiro-web-docs/00_information/` (公式サイトの構造・情報源)
- [ ] `kiro-web-docs/01_features/` (機能詳細ガイド)
- [ ] `kiro-web-docs/02_update/` (changelog・アップデート情報)
- [ ] `kiro-web-docs/03_deployment/` (導入・運用・データ保護・ファイアウォール)
- [ ] `kiro-web-docs/04_reference/` (許可ドメイン・環境変数・MCP・上限値)
- [ ] `scripts/` / `Makefile` / CI
- [ ] Other: _______________

## Kiro Web changelog entry

**Kiro Web has no version numbers.** If this change concerns a specific update, give the
changelog entry as **date + slug** (e.g., `2026-07-01 / iam-roles-and-authorize-powers-for-third-party-services`), or `N/A`.

## Checklist

- [ ] I have read the [documentation workflow](WORKFLOW.md) and [commit checklist](COMMIT_CHECKLIST.md)
- [ ] Every technical statement cites a primary source (kiro.dev docs / changelog)
- [ ] Statements that cannot be verified officially are explicitly marked 未確認
- [ ] **No reasons/causality are asserted unless officially stated** (facts and inference are kept separate)
- [ ] I have performed a self-review of my own changes
- [ ] I have checked for typos and grammatical errors
- [ ] My changes are consistent with existing documentation structure
- [ ] Dates use ISO format (`YYYY-MM-DD`)
- [ ] Kiro Web / Kiro IDE / Kiro CLI are not conflated; links to sibling products state that they are a different product
- [ ] **Table values, paths, and counts are taken from the HTML, not the `.md` companion**
- [ ] kiro.dev URLs end with a trailing slash (no trailing slash returns 301)

## Testing

- [ ] `make check-kiro-web-all` passes locally (exit 0)
- [ ] `make check-kiro-web-ignore` passes locally (exit 0)
- [ ] If I created or modified a validation script, I ran a **negative test per rule** and verified restoration with `diff`
- [ ] I have verified that all links work correctly
- [ ] I have checked that Mermaid diagrams and tables render properly (if applicable)

## Related Issues

Closes #(issue number)

## Additional Notes

Add any additional notes or context about the PR here.

---

**Important**: This is an unofficial documentation project. By submitting this PR, you acknowledge that this project is not affiliated with Kiro or Amazon Web Services, Inc.
