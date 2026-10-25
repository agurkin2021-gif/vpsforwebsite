# Japanese localization

### Japanese localization — 2026-10-25 (validated locally; publication pending)

- Owner requested Japanese (`ja`) with every page individually adapted. Complete scope: 20 English source files (18 public pages plus two shared sections), a localized 404, 4,699 reviewed content units, 507 shared UI/hero entries and 16 interactive forms. Homepage query = Title = H1 is `Webサイト向けVPS`, at `/ja/`; each other page has its own native Japanese query/title/H1 and matching slug. Full route ownership is recorded in `research/japanese-localization-2026-10-25.md` and `data/japanese_review.json`.
- All pages were translated and reviewed individually, preserving article depth, technical values, USD prices/check dates, commands, anchors, form semantics/algorithms, affiliate destinations/attributes/placement, and the original owner hero artwork. About renders its full source body. Contact remains noindex, outside the sitemap, without an invented address or form. No Japan-location, yen-price, traffic or ranking claims were added.
- Local production-like Chromium validation passed all 18 pages at eight widths (320, 360, 390, 430, 768, 1024, 1280, 1920 px): 144 geometry cases, all 16 forms and all 18,736 input states compared with English outcomes and numbers, actual button submissions and equivalent EN/JA navigation. Zero findings. Headline/hero overlaps, horizontal overflow, loaded Japanese font, missing images and language-menu bounds are checked. Reviewed mobile/desktop screenshots and supplemental CTA/404 checks passed.
- Static Japanese coverage/SEO/structure/affiliate/link validation passed: 20 source files, 18 rendered pages, 16 forms, zero errors. German, Italian, Persian and Arabic static regression audits each passed all 18 pages. Recovery audit: 159 preserved cached pages, 15 locale homes, 270 selectors, zero errors. Site integrity: 278 HTML pages, 380 local targets, 96 stylesheets, zero errors; three integrity unit tests passed. Deployment sitemap contains 257 indexable URLs, including 17 Japanese pages.
- Preview build under `https://preview.example.test/preview/` passed all 18 Japanese pages and 155 local targets, including native encoded URLs, navigation, canonical/hreflang and asset prefixes. The preview is a local test fixture, not a published website.
- Japanese typography uses a local 358,884-byte variable Noto Sans JP subset covering all 976 used glyphs, licensed under SIL OFL. `scripts/build-japanese-font.py` verifies the pinned upstream font and coverage, and generates both the subset and outlined Japanese CTA SVG. Scoped CSS provides Japanese line breaking, headline sizing, table/code scrolling and responsive buttons. The original homepage hero is unchanged (SHA-256 `af91640a83f2564d6b91777550e9b9d6435eeca232b876473037c58f95346fb1`).
- `data/japanese_review.json` seals reviewed source/UI/font/CTA hashes (text normalized to LF). CI now adds Japanese static and full browser gates, with all 18 EN/JA roundtrips and seven-day evidence artifacts, while retaining existing DE/IT/FA/AR gates. Before changing Japanese source, review the affected page, update glyph coverage when needed and renew the review manifest deliberately.
- Publication is authorized through the established GitHub main → Prepare static generated commit → Cloudflare Worker flow. Baseline `0c6e648abb71e00b9751806ad0d30281cb1f8ea9`; isolated checkout `vpsforwebsite-japanese`. Source push, CI/generated commit, Cloudflare success and ordinary production verification are still pending. Never publish English scaffolds or hand-edit generated static assets.

## Page-specific query and route ownership

| English source | Japanese query / Title / H1 | URL |
| --- | --- | --- |
| `_index.md` | Webサイト向けVPS | `/ja/` |
| `vps-for-wordpress.md` | WordPress向けVPS | `/ja/wordpress向けvps/` |
| `vps-for-woocommerce.md` | WooCommerce向けVPS | `/ja/woocommerce向けvps/` |
| `vps-sizing-for-website.md` | VPSのスペックの選び方 | `/ja/vpsのスペックの選び方/` |
| `vps-vs-shared-hosting.md` | VPSと共用サーバーの違い | `/ja/vpsと共用サーバーの違い/` |
| `vps-for-multiple-websites.md` | 複数サイト向けVPS | `/ja/複数サイト向けvps/` |
| `vps-with-control-panel.md` | コントロールパネル付きVPS | `/ja/コントロールパネル付きvps/` |
| `managed-vs-unmanaged-vps.md` | マネージドVPSとアンマネージドVPSの違い | `/ja/マネージドvpsとアンマネージドvpsの違い/` |
| `fastpanel-vps-hosting.md` | FASTPANEL対応VPS | `/ja/fastpanel対応vps/` |
| `how-to-host-a-website-on-vps.md` | VPSでWebサイトを公開する方法 | `/ja/vpsでwebサイトを公開する方法/` |
| `website-migration-to-vps.md` | WebサイトのVPS移行 | `/ja/webサイトのvps移行/` |
| `vps-security-checklist.md` | VPSのセキュリティチェックリスト | `/ja/vpsのセキュリティチェックリスト/` |
| `vps-backup-strategy.md` | VPSのバックアップ戦略 | `/ja/vpsのバックアップ戦略/` |
| `vps-monitoring.md` | VPSの監視 | `/ja/vpsの監視/` |
| `how-to-choose-vps-location.md` | VPSのリージョンの選び方 | `/ja/vpsのリージョンの選び方/` |
| `about/_index.md` | 当サイトについて | `/ja/当サイトについて/` |
| `contact/_index.md` | お問い合わせ | `/ja/お問い合わせ/` |
| `privacy-policy.md` | プライバシーポリシー | `/ja/プライバシーポリシー/` |

Terminology reference: https://vps.sakura.ad.jp/specification/ (Japanese VPS terminology only; no competitor prices or Japan-location claims imported). Language configuration: https://gohugo.io/configuration/languages/. No search-volume or ranking claims.
