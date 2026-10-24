# Arabic localization — complete and live-verified

### Arabic complete localization — 2026-10-23 (published and live-verified)

- Owner authorization: complete Arabic localization from the English reference, adaptive titles, URLs and all content, all phases in one pass without questions. This supersedes historical Spanish-only, preview-only and one-page-per-turn limits. German, Italian and Persian are already complete.
- Delivered scope: all 20 English source files, 18 public pages plus localized 404, 4,699 reviewed content units and 507 shared UI/hero entries; all 16 forms and their results translated. Modern Standard Arabic, `ar`, native `العربية`, RTL, native Arabic slugs, exact query = Title = H1; homepage `/ar/`, no duplicate keyword-slug home.
- Original Hugo/Hugoplate design retained. Reuse self-hosted OFL Vazirmatn v33.003, Arabic-only responsive styles, RTL navigation/forms, LTR code and numeric fields. Latin specifications and USD prices are isolated in bidi elements; table wrappers keep multiline specifications together on mobile. Home, tables, forms, code and localized 404 visually inspected at mobile and desktop widths. Owner hero WebP remains byte-identical (51,196 bytes; SHA-256 `af91640a83f2564d6b91777550e9b9d6435eeca232b876473037c58f95346fb1`); embedded English artwork is the explicit preservation exception. Alt text and separate CTA SVG translated.
- English parity: original numbers, USD prices, dates, code, heading IDs, form IDs/options/algorithms and affiliate URLs/attributes/positions retained. Contact stays noindex and outside the sitemap. Brands/software, technical tokens and exact external admin-menu names remain intentionally Latin. No original-language prose changed; all 238 existing main contents match the tracked baseline exactly. An older Persian QA folder predates its final table bidi fix; comparison was corrected to the actual generated baseline, not relaxed.
- Local checks: complete source/rendered audit, strict locale/site-integrity/recovery/French/German/Italian/Persian checks pass. Full Chromium: 18 pages, 90 geometry cases at 320/390/768/1280/1920, 16 forms, 18,736 exhaustive English-compared states, zero findings. Subsequent CSS-only table isolation passed another 90 geometry/font/bidi cases. Project-prefix preview: 19 pages including 404, 380 menu links, 266 picker links, 200 article links and 149 assets; noindex, no production canonical/hreflang or analytics, zero findings. English prose residual review found only intentional product/documentation names.
- Final local overlay: 259 HTML files, 252 language switchers, 14 locale homes and 240 sitemap URLs. Source is based on `a7710207c8b99b6db1c44eeda837e7b493d23802`. CI now includes the full Arabic gate after preserved German/Italian/Persian gates; the job timeout covers all four 35-minute watchdogs plus build overhead. No generated `cloudflare-public` or Worker assets manually edited.
- Publication complete: source `c54f4d9810e6f90ed7a3dfbf0aac111cbe0f9783` -> successful [Prepare Cloudflare static site run 40043294289](https://github.com/agurkin2021-gif/vpsforwebsite/actions/runs/40043294289) -> generated static `db2ae42f495427e6b28cac82e9a435efcacf5fa2` -> successful Cloudflare Workers Build check `120721741884` on that generated commit. German, Italian, Persian and Arabic CI matrices all passed. No generated output or Worker assets manually edited.
- Actual live verification: all 18 routes HTTP 200, exact Title/H1, native self-canonicals and EN/AR/x-default equivalence, complete body and control parity with the local release; 360 menu links, 313 internal Arabic links and 114 anchor links checked. Sitemap contains exactly 17 indexable Arabic routes; Contact remains noindex. All 54 robots checks pass; a nonexistent Arabic URL returns localized HTTP 404. Owner hero remains 51,196 bytes with the original SHA-256. Live Chromium: 90 geometry/font/bidi cases at five widths, all 16 forms and 18,736 exhaustive English-compared states, language roundtrips, zero findings. Live completion: `2026-10-24T00:25:11.387Z`.
- Evidence: isolated `vpsforwebsite-arabic/qa-output/`, including `arabic-audit.json`, `arabic-final-browser/report.json`, `arabic-release-geometry/report.json`, `arabic-preview.json`, `existing-locale-regression.json`, `integration-checks.log`, `residual-review.json`, `deployment-evidence.json`, `live-seo/`, `live-browser/`, `live-visual/` and `visual/`. Persistent route and translation-method notes: `research/arabic-localization-2026-10-23.md`.

## Route ownership

| English source | Arabic query / Title / H1 | URL |
| --- | --- | --- |
| `_index.md` | استضافة VPS للمواقع | `/ar/` |
| `about/_index.md` | من نحن | `/ar/من-نحن/` |
| `contact/_index.md` | اتصل بنا | `/ar/اتصل-بنا/` |
| `privacy-policy.md` | سياسة الخصوصية | `/ar/سياسة-الخصوصية/` |
| `vps-sizing-for-website.md` | تحديد موارد VPS للمواقع | `/ar/تحديد-موارد-vps-للمواقع/` |
| `website-migration-to-vps.md` | نقل موقع إلى VPS | `/ar/نقل-موقع-إلى-vps/` |
| `managed-vs-unmanaged-vps.md` | VPS المدار مقابل غير المدار | `/ar/vps-المدار-مقابل-غير-المدار/` |
| `vps-for-wordpress.md` | VPS لووردبريس | `/ar/vps-لووردبريس/` |
| `vps-for-woocommerce.md` | VPS لووكومرس | `/ar/vps-لووكومرس/` |
| `vps-vs-shared-hosting.md` | VPS مقابل الاستضافة المشتركة | `/ar/vps-مقابل-الاستضافة-المشتركة/` |
| `vps-for-multiple-websites.md` | VPS لمواقع متعددة | `/ar/vps-لمواقع-متعددة/` |
| `vps-with-control-panel.md` | VPS مع لوحة تحكم | `/ar/vps-مع-لوحة-تحكم/` |
| `fastpanel-vps-hosting.md` | استضافة VPS مع FASTPANEL | `/ar/استضافة-vps-مع-fastpanel/` |
| `how-to-host-a-website-on-vps.md` | كيفية استضافة موقع على VPS | `/ar/كيفية-استضافة-موقع-على-vps/` |
| `vps-security-checklist.md` | قائمة التحقق من أمان VPS | `/ar/قائمة-التحقق-من-أمان-vps/` |
| `vps-backup-strategy.md` | استراتيجية النسخ الاحتياطي لخادم VPS | `/ar/استراتيجية-النسخ-الاحتياطي-لخادم-vps/` |
| `vps-monitoring.md` | مراقبة VPS | `/ar/مراقبة-vps/` |
| `how-to-choose-vps-location.md` | كيفية اختيار موقع خادم VPS | `/ar/كيفية-اختيار-موقع-خادم-vps/` |

## Implementation references

- Translation workflow: English-source units, a shared reviewed translation memory and page-by-page editorial review. Later guide drafts additionally use machine assistance on public English prose; drafts remain isolated and unapproved until reviewed and corrected. Human-language review specifically corrects PHP workers, headroom, staging, checkout, restore semantics and product names. Structural parity and browser tests are separate gates and do not substitute for that review.

- [Hugo language configuration](https://gohugo.io/configuration/languages/) and [multilingual routing](https://gohugo.io/content-management/multilingual/).
- [Hostinger Arabic terminology](https://www.hostinger.com/eg/vps-hosting), terminology reference only; no competitor pricing or claims imported. No measured Arabic search-volume claim.
- Existing self-hosted Vazirmatn v33.003, SIL OFL 1.1; supports Arabic script, no runtime font service.

Translation, publication and actual live verification are complete. No requested Arabic pages remain pending.
