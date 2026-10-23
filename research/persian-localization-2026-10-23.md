# Persian localization — work in progress

### Persian localization — 2026-10-23 (active; not published)

- Owner explicitly requests the complete Persian version from English, page by page, adaptive titles, URLs and all content, all stages in one pass without questions. This supersedes historical Spanish-only, preview-only and one-page-per-turn limits. German and Italian are already complete and must not be restarted.
- Isolated checkout `vpsforwebsite-persian`, baseline `86b8f39a7ef23ff232fa6ccc32f4e10374390fa6`. Scope: 20 English source files, 18 public pages plus localized 404, 507 shared UI/hero entries and 16 forms. Original English source and other-locale prose remain unchanged.
- Persian uses `fa` / `fa-IR`, native `فارسی`, semantic `dir="rtl"`, natural Persian slugs and query = Title = H1. Homepage `/fa/`, title `سرور مجازی برای سایت`; no duplicate keyword-slug homepage. Native Persian font and RTL adjustments are locale-scoped within the original Hugoplate design.
- Preserve original numbers/USD prices/dates, all code and command direction, original heading IDs, form IDs/values/algorithms, affiliate URLs/attributes/placement, Contact noindex and sitemap exclusion. The original owner WebP and its embedded English lettering remain the explicit artwork-preservation exception; translate alt text and separate CTA SVG.
- Reviewed checkpoint: 20/20 English source files fully manually reviewed (4699 content units), plus all 507 shared UI entries. Completed sources: `_index.md`, `about/_index.md`, `contact/_index.md`, `fastpanel-vps-hosting.md`, `how-to-choose-vps-location.md`, `how-to-host-a-website-on-vps.md`, `managed-vs-unmanaged-vps.md`, `privacy-policy.md`, `sections/_index.md`, `sections/call-to-action.md`, `vps-backup-strategy.md`, `vps-for-multiple-websites.md`, `vps-for-woocommerce.md`, `vps-for-wordpress.md`, `vps-monitoring.md`, `vps-security-checklist.md`, `vps-sizing-for-website.md`, `vps-vs-shared-hosting.md`, `vps-with-control-panel.md`, `website-migration-to-vps.md`. All English source content is now translated; publication remains gated on full QA.
- Complete local browser evidence: all 18 pages / 90 geometry cases at 320/390/768/1280/1920, 16 forms / 18,736 exhaustive English-compared input states, zero findings (`qa-output/persian-browser/report.json`). Final typography refinement independently passes all 90 geometry cases, font/code/bidi checks and language roundtrips (`qa-output/persian-release-geometry/report.json`); form markup/scripts remain identical. Full CI matrix will run again on the publication source.
- RTL visual refinement: keep original artwork byte-for-byte, native Vazirmatn for form labels, LTR code/number inputs, and 58 semantic `bdi` wrappers around unchanged Latin specs/prices in RTL tables. Visual inspection confirmed readable mobile/desktop tables, forms, code and localized 404. Full main DOM comparison after unwrapping those 58 spans confirms no content, forms or scripts changed from the exhaustive-matrix build. Reports: `qa-output/release-delta.json`, `qa-output/persian-release-geometry/report.json`, `qa-output/visual/`.
- Complete local source/rendered audit passes: 20 source files, 18 public pages, 16 forms; final responsive RTL pass: 90 geometry cases at five widths, no findings. The full English-compared calculator matrix passes with zero findings. Preview: 19 pages including 404, 380 menu links, 247 language-picker links, 200 article links, 149 assets, all checks pass. Recovery, strict locale, French, German, Italian and site-integrity checks pass; all 219 pre-existing main contents are unchanged. Merged output: 240 HTML documents / 223 sitemap URLs. Source publication, successful prepare-static/generated commit/Cloudflare deployment and actual live verification remain pending.
- Publication checkpoint: source `e60429cb8dd15053991d5611059bd309c3dfdbe6`, prepare-static run `40034309455`, generated `2fd87de37d9666310c9f659c4e91d224cd82f844`, Cloudflare build `7a23fa63-9510-4b24-91bb-162d3bc9010d` all succeeded. CI DE/IT/FA each passes 18 pages / 90 geometry / 16 forms / 18,736 states. Actual live SEO, menu/internal/anchor links, 54 robots checks, localized 404 and original hero hash pass. A final Persian-only font refinement sets theme font variables inside main content so the homepage hero and calculator also use Vazirmatn; the enhanced all-heading/all-label font and geometry audit passes 90 cases. No content or form algorithm changes. Final live browser matrix and font deployment verification remain pending.

## Route ownership

| English source | Persian query / Title / H1 | URL |
| --- | --- | --- |
| `_index.md` | سرور مجازی برای سایت | `/fa/` |
| `about/_index.md` | درباره ما | `/fa/درباره-ما/` |
| `contact/_index.md` | تماس با ما | `/fa/تماس-با-ما/` |
| `privacy-policy.md` | سیاست حفظ حریم خصوصی | `/fa/سیاست-حفظ-حریم-خصوصی/` |
| `vps-sizing-for-website.md` | تعیین منابع سرور مجازی برای سایت | `/fa/تعیین-منابع-سرور-مجازی-برای-سایت/` |
| `website-migration-to-vps.md` | انتقال سایت به سرور مجازی | `/fa/انتقال-سایت-به-سرور-مجازی/` |
| `managed-vs-unmanaged-vps.md` | سرور مجازی مدیریت شده یا مدیریت نشده | `/fa/سرور-مجازی-مدیریت-شده-یا-مدیریت-نشده/` |
| `vps-for-wordpress.md` | سرور مجازی برای وردپرس | `/fa/سرور-مجازی-برای-وردپرس/` |
| `vps-for-woocommerce.md` | سرور مجازی برای ووکامرس | `/fa/سرور-مجازی-برای-ووکامرس/` |
| `vps-vs-shared-hosting.md` | سرور مجازی یا هاست اشتراکی | `/fa/سرور-مجازی-یا-هاست-اشتراکی/` |
| `vps-for-multiple-websites.md` | سرور مجازی برای چند سایت | `/fa/سرور-مجازی-برای-چند-سایت/` |
| `vps-with-control-panel.md` | سرور مجازی با کنترل پنل | `/fa/سرور-مجازی-با-کنترل-پنل/` |
| `fastpanel-vps-hosting.md` | میزبانی سرور مجازی با FASTPANEL | `/fa/میزبانی-سرور-مجازی-با-fastpanel/` |
| `how-to-host-a-website-on-vps.md` | نحوه میزبانی سایت روی سرور مجازی | `/fa/نحوه-میزبانی-سایت-روی-سرور-مجازی/` |
| `vps-security-checklist.md` | چک لیست امنیت سرور مجازی | `/fa/چک-لیست-امنیت-سرور-مجازی/` |
| `vps-backup-strategy.md` | استراتژی پشتیبان گیری سرور مجازی | `/fa/استراتژی-پشتیبان-گیری-سرور-مجازی/` |
| `vps-monitoring.md` | مانیتورینگ سرور مجازی | `/fa/مانیتورینگ-سرور-مجازی/` |
| `how-to-choose-vps-location.md` | نحوه انتخاب موقعیت سرور مجازی | `/fa/نحوه-انتخاب-موقعیت-سرور-مجازی/` |

## RTL implementation references

- [HTML dir semantics](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Global_attributes/dir).
- [Vazirmatn v33.003](https://github.com/rastikerdar/vazirmatn/tree/v33.003), SIL Open Font License 1.1. Self-hosted, Persian-only; no runtime font service.

Translation and local source/preview/RTL gates are complete. The full browser decision matrix also passes. Publication/live gates remain pending.
