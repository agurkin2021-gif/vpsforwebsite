# CHATGPT PROJECT CONTEXT — vpsforwebsite.com

### Persian complete localization — 2026-10-23 (published and live-verified)

- Owner authorization: add the complete Persian version using English as the reference, page by page, adaptive titles, URLs and all content, all phases in one pass without questions. This supersedes historical Spanish-only, preview-only and one-page-per-turn limits. German and Italian were already complete and were preserved.
- Scope delivered: all 20 English source files, 18 public pages plus localized 404, 4,699 manually reviewed content units and all 507 shared UI/hero entries; all 16 interactive forms and every result branch translated. `fa` / `fa-IR`, native `فارسی`, semantic RTL, native Persian URLs and exact query = Title = H1; homepage `/fa/`, no duplicate keyword-slug home.
- Original Hugo/Hugoplate design retained. Self-hosted Vazirmatn v33.003 with upstream SIL OFL 1.1; Persian-only responsive styles, proper form-label font, LTR code/numeric inputs, 58 semantic bidi wrappers for unchanged Latin table specifications/prices. Mobile and desktop home, tables, forms, code and 404 visually inspected. Original owner hero WebP remains byte-identical (51,196 bytes; SHA-256 `af91640a83f2564d6b91777550e9b9d6435eeca232b876473037c58f95346fb1`); its embedded English lettering is the explicit artwork-preservation exception. Separate CTA SVG and image alt text localized.
- Content/SEO parity: original numbers, USD amounts, dates, code, heading IDs, form IDs/options/algorithms and affiliate URLs/attributes/positions retained. Contact stays noindex and outside the sitemap. Brand/software names, technical specifications and exact external admin-menu paths remain intentional Latin tokens. All 219 pre-existing main page contents are unchanged; recovery retains 159 cached pages and all 13 locale homes. Final merged output: 240 HTML pages, 234 language switchers, 223 sitemap URLs.
- Local verification: complete source/rendered audit, strict locale/site-integrity/recovery/French/German/Italian checks pass. Browser: 18 pages, 90 cases at 320/390/768/1280/1920, 16 forms and 18,736 exhaustive English-compared input states, zero findings. Final typography delta independently passed all 90 geometry/font/bidi cases and preserved every form/script. Project-prefix preview: 19 pages including 404, 380 menu links, 247 language-picker links, 200 article links, 149 assets; noindex, no production canonical/hreflang or analytics, zero findings.
- Publication: source `a5d9d5af28e675a81ac1be260cf26a28da73db5f` -> successful [Prepare Cloudflare static site run 40035524745](https://github.com/agurkin2021-gif/vpsforwebsite/actions/runs/40035524745) -> generated static `b3df10069d38d08a1ac6f1c1220aa370a5d56acf` -> Cloudflare Worker build `e3c3e948-bee6-48a2-9580-3c454bcf9346` success on that generated commit. CI repeats German, Italian and Persian matrices; each passes 18 pages / 90 geometry / 16 forms / 18,736 states with zero failures. No generated output or Worker assets were manually edited.
- Actual live verification: all 18 routes HTTP 200, exact titles/H1, native self canonicals, EN/FA/x-default equivalence, complete body/control parity with final local build; 360 menu links, 313 internal Persian links and 114 anchors checked. Sitemap contains exactly 17 indexable Persian routes. 54 robots checks pass; actual missing Persian URL returns localized HTTP 404. Owner hero bytes match. Live Chromium: 36 mobile/desktop geometry cases, all 16 forms / 18,736 English-compared states, language roundtrips, zero findings. The final Persian-only theme-font override also passes a separate live 90-case audit including every heading and form label; English content and calculators are unchanged. Live completion: `2026-10-23T22:51:22.779Z`.
- Evidence is retained locally in the isolated `vpsforwebsite-persian/qa-output/`: `persian-audit.json`, `persian-browser/report.json`, `persian-release-geometry/report.json`, `persian-preview.json`, `existing-locale-regression.json`, `release-delta.json`, `deployment-evidence.json`, `live-seo/`, `live-browser/`, `live-final-fonts/`, `font-release-delta.json`, `visual/`. Persistent source/route and RTL reference notes: `research/persian-localization-2026-10-23.md`. Translation, publication and live gates are complete; no requested Persian pages remain pending.

### Italian complete localization — 2026-10-23 (published and live-verified)

- Owner authorization: add the complete Italian language from English, page by page, all phases in one pass without questions. This supersedes historical Spanish-only, preview-only and one-page-per-turn limits. German is already complete; do not restart it. Work is isolated in `vpsforwebsite-italian` from `ac18c1bf920ba1a738c264751f21a9722b9fc243`; unrelated Korean changes in the original checkout remain untouched.
- All **20/20 English source paths** now have complete manually reviewed Italian equivalents: homepage, 14 guides, About, Contact, Privacy and two shared sections. **18 public pages**, localized 404 and **507 UI/hero dictionary entries** are complete. Homepage `/it/`, exact query/Title/H1 `VPS per siti web`; natural matching Italian titles and slugs throughout. Full inventory: `research/italian-localization-2026-10-23.md`.
- Preserve original Hugo/Hugoplate design, 522 guide anchors, code, numeric facts/USD prices/dates, affiliate destinations/attributes/placements and all form IDs/values/decisions. English and other-locale prose are unchanged. Owner hero stays byte-identical (SHA-256 `af91640a83f2564d6b91777550e9b9d6435eeca232b876473037c58f95346fb1`); its embedded English lettering remains the explicit preservation exception. Italian alt text and separate CTA SVG are localized. Contact remains noindex and excluded from sitemap.
- Complete source/render audit passed: **20 source files, 18 pages, 16 forms**, zero errors. Final local Chromium: **90 viewport cases at 320/390/768/1280/1920, all 16 forms, 18,736 input states compared with English**, zero findings; actual pointer submissions and EN↔IT equivalent-page roundtrips pass. A final shorter Control Panel select label changes only that Italian HTML document; targeted final-build retest passed all five widths and 288 states. Reports: `qa-output/italian-browser-final/report.json`, `qa-output/italian-panel-final/report.json`, `qa-output/italian-publication-audit.json`.
- Merged deployment checks passed: 221 HTML files, 316 internal targets, 88 stylesheet references, 159 recovery snapshots, 12 locale homes, 216 language switchers, zero errors. Existing German source audit, French parity, recovered-locale strict audits and native DE/IT recovery navigation fixtures pass. All **200 pre-existing pages retain identical main content**; original hero hash is unchanged. Merged sitemap has 206 routes, including exactly 17 indexable Italian routes.
- Project-path preview passes for 19 documents including 404: 380 navigation links, 228 language-picker links, 200 article links and 149 assets; no errors. Preview remains noindex without canonical/hreflang head links or analytics. Representative mobile/desktop tables, forms, Contact, 404 and hero screenshots were visually reviewed.
- Native Hugo relref resolves the complete cluster; no temporary partial-translation shortcode remains. Recovery navigation supports native German and Italian equivalents without false translation alternates. Italian structural and full-browser audits now gate the existing prepare-static workflow after German gates; its bounded timeout accommodates both full matrices.
- **Published and live-verified at 2026-10-23T21:11:42.109Z.** Source commit `d1c17ba5f443e95c35fa476d13ec6cc8367db333`; generated deployment commit `3dd4d3fb740066746cc539ce32f46cf9b0424a02`. [Prepare Cloudflare static site](https://github.com/agurkin2021-gif/vpsforwebsite/actions/runs/40023393877) completed **success**, including German and Italian full browser matrices: each 18 pages, 90 geometry cases, 16 forms, 18,736 English-compared states, zero findings. [Italian reports and screenshots](https://github.com/agurkin2021-gif/vpsforwebsite/actions/runs/40023393877/artifacts/12530604732) are retained for seven days.
- Cloudflare **Workers Builds: vpsforwebsite** completed **success** for the generated commit. Build evidence: https://dash.cloudflare.com/424496ecd70fae4cb23aaf2fc46adab0/workers/services/view/vpsforwebsite/production/builds/9fa1f7d0-be97-4f3c-9bb2-0d0c2a6d92f4. Production Hugo validation and Korean internal-link/browser checks also passed. No manual production asset or Worker edits were made.
- Independent actual live HTTPS verification passed **18/18 HTTP 200** routes with Italian Title/H1 and all body text, heading structure, forms, control labels and navigation matching the final build. Checked 360 menu/footer links, 313 internal Italian links and 114 anchor links. Actual sitemap contains exactly **17 indexable Italian routes**; Contact remains noindex without canonical/hreflang and is excluded.
- Actual live Chromium passed **36 viewport cases at 390/1280, all 16 forms and all 18,736 input states against live English**, zero findings; real pointer submissions and equivalent-language roundtrips pass. Robots checks allow all Italian routes for general, Googlebot and Bingbot crawlers (54 checks). The live owner hero is HTTP 200, 51,196 bytes, and retains SHA-256 `af91640a83f2564d6b91777550e9b9d6435eeca232b876473037c58f95346fb1`.
- A nonexistent Italian address returns HTTP 404 with Italian heading `Pagina non trovata` and a working `/it/` home link. Four additional actual live home/panel screenshots at 390/1280 were captured after fonts and images loaded and visually reviewed; no rendering issue found. The existing [French responsive Chromium audit](https://github.com/agurkin2021-gif/vpsforwebsite/actions/runs/40023722810) also completed successfully.
- Complete Italian version is published at **https://vpsforwebsite.com/it/**. No Italian page or publication gate remains pending. Detailed local evidence: `qa-output/deployment-evidence.json`, `qa-output/live-seo/`, `qa-output/italian-browser-live/`; source review: `research/italian-localization-2026-10-23.md`.

### German complete localization — 2026-10-23 (published and live-verified)

- Current owner request: add German page by page, using English as the reference, complete all phases in one pass without further questions. Scope is **vpsforwebsite.com** only. All **20 English Markdown source paths now have German equivalents**: homepage, 14 full guides, About, Contact, Privacy, and two non-rendered shared section sources. There are **18 public German content routes**, plus a localized 404. Do not restart a partial German translation queue.
- German uses `de` / `de-DE`, native `Deutsch` navigation, natural German titles, descriptions, slugs, headings, prose, tables, FAQs, SVG labels, accessibility copy, calculator inputs and results. The homepage is `/de/`, Title/H1 **VPS für Websites**. Exact target query = Title = H1 remains the rule; no duplicate keyword-slug homepage. Full route inventory and evidence: `research/german-localization-2026-10-23.md` and the five associated German review reports.
- English is the reference, not the Korean wording. All 522 original guide section anchors, original numbers/USD amounts, code examples, partner URLs/attributes, control IDs/values and JavaScript decisions are preserved. German gets up to 507 dictionary entries for shared UI/hero strings. The original owner WebP stays byte-identical (SHA-256 `af91640a83f2564d6b91777550e9b9d6435eeca232b876473037c58f95346fb1`); its embedded English lettering is an explicit artwork-preservation exception. German alt text and the separate CTA SVG are localized.
- German Contact remains noindex and excluded from the sitemap, with no invented working contact form. About/Contact body rendering is enabled only for German alongside the existing Korean branch. Other-language prose is unchanged. An independent 41-page EN/KO/ES rendered-content regression comparison passed.
- Production-style source/HTML audit passed for all 18 pages and 16 interactive forms; restored deployment audit passed for 202 HTML files, 280 internal targets, 70 stylesheet references, all 159 recovery snapshots, 11 locale homes and 198 language switchers. All restored-locale audits report zero issues. Five recovered Contact pages retain noindex and are excluded from the merged sitemap by attribute-order-independent parsing.
- Project-path preview passed for all 18 pages plus 404, including 380 German header/footer links, 209 prefixed language-picker links, 200 article links and 265 asset references. Preview remains noindex, without canonical/hreflang head links or analytics loaders. German-only GetPage lookup normalization fixes menu URLs already prefixed by Hugo; other locale branches are unchanged. Recovery-only preview locale homes still require the existing separate overlay.
- `scripts/audit-german.py` and `scripts/qa-german.cjs` are publication gates in the existing prepare-static workflow: source/SEO/link parity, five viewport widths, every select combination in all 16 forms, numerical RAM boundaries, actual pointer submissions and EN↔DE equivalent-page switching. Final local Chromium run passed **18 pages, 90 viewport cases, 16 forms, 18,736 German input states compared with English, zero findings**. After the preview-only routing fixes, the production rebuild and all audits passed again; **all 202 HTML outputs are byte-identical** to the browser-tested build, preserving the 41-page existing-locale regression result. Detailed local logs: `qa-output/final-local-validation.log`, `qa-output/final-html-diff.json`, `qa-output/browser-final/report.json` (local artifacts, not source).
- Final text sweep translated two remaining labels: Contact's primary CTA and the Monitoring diagram's CPU/RAM/storage/network caption. Sequential production comparisons show only those two German HTML documents changed; each rebuild and every structural/integrity audit passed. Independent targeted Chromium checks of both pages at all five widths passed **10/10**, with no clipping, JavaScript errors or missing assets (`qa-output/browser-targeted/report.json`). Form code is unchanged. The QA runner also saves per-page reports and has a bounded 35-minute watchdog; its normal/hung-launch/hung-close shutdown cases passed.
- Work is isolated in `vpsforwebsite-german` from base main `bc666490d693d3c3c752af87de952fdbfe7c7a8e`; unrelated changes in the original local checkout were preserved. Source integration, local validation, automated deployment and actual live verification are complete; evidence follows. Main → generated static commit → Cloudflare Ready → live URL remains mandatory; no manual generated-static or Worker asset edits.

- **Published and live-verified at 2026-10-23T03:34:31.715Z.** Source `main` commit `1cb67568f28920751bf886c28a1c520f2adf38ce`; generated deployment commit `2ff6c42d8911e438c4fe2eb0d768c4c042d9d47a`. [Prepare Cloudflare static site](https://github.com/agurkin2021-gif/vpsforwebsite/actions/runs/39894681997) completed **success**, including the final-source German run: 18 pages, 90 geometry cases, 16 forms, 18,736 input states, zero findings. [Browser reports/screenshots](https://github.com/agurkin2021-gif/vpsforwebsite/actions/runs/39894681997/artifacts/12475648879) are retained for seven days. Production Hugo validation, Korean link routing and Korean multi-site browser checks also succeeded.
- Cloudflare **Workers Builds: vpsforwebsite** succeeded for the generated commit: build `668cb30d-a5e8-4799-869d-61a246321b0b`, deployed version `ca86803c-7296-4876-b7fd-1dcb8fa312a1`. No manual Worker/static asset changes were made.
- The existing [French responsive Chromium audit](https://github.com/agurkin2021-gif/vpsforwebsite/actions/runs/39894883021) also completed successfully. Actual live `robots.txt` allows the German routes, and the fetched owner hero is HTTP 200, 51,196 bytes, with the exact original SHA-256 `af91640a83f2564d6b91777550e9b9d6435eeca232b876473037c58f95346fb1` (`qa-output/live-seo/robots-hero.json`).
- Independent actual live HTTPS/SEO verification passed **18/18 HTTP 200** routes with German Title/H1 and content matching the final build; 360 menu/footer links, 313 internal German links and 114 anchors pass. Sitemap contains exactly 17 indexable German routes; Contact remains noindex without canonical/hreflang. Separate actual live Chromium passed **36 viewport cases (390/1280), all 16 forms and all 18,736 input states against live English, zero findings**, plus actual pointer submissions and equivalent-language roundtrips. Evidence is under `qa-output/live-seo/` and `qa-output/browser-live/` in the isolated checkout.
- The complete German cluster is published at **https://vpsforwebsite.com/de/**. No German page or publication gate remains pending. English reference and other-language prose, original code/price values and owner artwork remain preserved.

### Korean localization 20/20 completion and production verification — 2026-10-20

- Sole site in scope: **vpsforwebsite.com**, repository **agurkin2021-gif/vpsforwebsite**, branch `main`. Source-path audit on 2026-10-20 finds **20 English Markdown paths and 20 matching Korean Markdown paths; none missing**. All 15 planned core commercial/technical Korean pages are published. Two shared section content paths, About, Contact and Privacy Policy also have KO equivalents. Do **not** restart the 11/15 queue described in stale entries below.
- Page 15, `content/korean/how-to-choose-vps-location.md`, was merged by **PR #11** and is live at `/ko/vps-위치-선택-방법/`; 48 original English anchor IDs, 34 original table lines, 140 bullets, 11 numbered steps, six selects/16 values, original JS logic, numeric facts and affiliate links were QA-verified. **PR #12** added Korean Privacy Policy at `/ko/개인정보-처리방침/`, retaining GA4 ID `G-J6X9FNRMH5`, VDSina disclosures and original privacy URL.
- **PR #13** (merge `086c868a9216de90619d001850de2d8de26a75aa`) published Korean About at `/ko/about/`: 7 section IDs and 9 list items preserved, review date **14 October 2026**, VDSina commercial disclosure. English `content/english/about/_index.md` contained the 7 sections but existing `layouts/list.html` did not render section `.Content`. Added a **Korean-only** list section render and Korean-only About hero/diagram strings, leaving English/other-language fallback untouched. Hugo/Chromium 390/1280 QA **39490700135 SUCCESS**; production workflows passed and Opera confirmed all seven sections live.
- **PR #14** (merge `25017d637caeaab43b5164865aad7d3f3ac25971`) published Korean Contact at `/ko/contact/`. Preserves exactly two source paragraphs, `noindex: true` and `sitemap.disable: true`, and makes no claim of an active public contact form. Korean-only hero/diagram labels and native `/ko/`, `/ko/about/` links added. Existing KO-only list render extended to Contact; EN/ES remain as before. Hugo/Chromium 390/1280 QA **39492168453 SUCCESS**; all three production workflows passed, static HTML generated and Opera confirmed live translated Contact/links.
- Final Opera production checks verified KO Location, Privacy, About and Contact public URLs; Privacy contains the original GA4 ID and VDSina disclosure, and About/Contact sections no longer 404. The Korean footer now resolves all About, Contact and Privacy destinations natively rather than falling back to English.
- A separate temporary experimental branch `work/ko-location-20261020` was created before the concurrent PR #11 merged page 15. **Do not merge this duplicate branch**. Canonical released page-15 branch was `work/ko-vps-location-20261020`, already merged via PR #11.
- Next phase is a **sitewide post-publication Korean regression/content sweep**, not translating new core pages. Strictly preserve the English reference, all other locales, URL targets, partner links, original numbers/tables/code/JavaScript. Only authorized domain: vpsforwebsite.com; never touch vpsubuntu.com.



### Korean page 11: live publication and internal-link regression closure — 2026-10-20

- Page 11 `VPS에 웹사이트를 호스팅하는 방법` at `/ko/vps에-웹사이트를-호스팅하는-방법/` is published. Original article source commit `b997a5b9a0dfdff5ef7919c14939aa19d70cf5ae`; Korean-only render-hook correction `3f763abbc6b3b3f6cec3b9be67563a7cd0449075`.
- A post-publication Opera check exposed protocol-relative internal links such as `//ko/...`. Angle-bracket relref placeholders must not pass through relURL before their later expansion. The render hook now preserves those placeholders in its Korean branch; the English/other-language branch is unchanged. No article prose, commands, tables, numbers or checker JavaScript were changed by this repair.
- Production Chromium QA run `39476410608` passed at 390px and 1280px: HTTP 200, exact single Title/H1, self-canonical, indexability, no page-width overflow, no JavaScript errors, no protocol-relative article links, and all 19 distinct same-origin article destinations/anchors reachable. All 72 checker input combinations passed at each viewport (144 actual submissions). Screenshots and JSON report are stored as run artifacts.
- Core Korean queue is now 11/15 published. Continue with page 12 `VPS Security Checklist`, then Backup Strategy, Monitoring and Location; About/Contact/Privacy remain separate final passes. Translate one page and one block at a time; preserve the English reference and other locales.

> READ THIS FILE FIRST IN EVERY NEW CHATGPT SESSION BEFORE CHANGING THE REPOSITORY.
> This file is the persistent project context and decision log for the site.

### Korean FASTPANEL page 10 publication closure — 2026-10-20

- Page 10 `FASTPANEL VPS 호스팅` at `/ko/fastpanel-vps-호스팅/` is **published and verified**: PR #6 merged as source commit `e7b5b485`; Hugo production workflow `39469292860` Success, Cloudflare static preparation `39469292861` Success, generated commit `f863a20e`, Cloudflare deployment Ready.
- Live Korean page opened and visually inspected in Opera. Production Chromium QA `39469627684` passed real 390/1280 viewport geometry with no overflow/JS errors and **36/36 actual form submissions** (all 3×3×2×2 input combinations). Original English guide and all other languages' visible content unchanged.
- Core Korean localization progress: **10/15 pages published**. Next page #11: How to host a website on VPS, to translate individually from the English original. Full evidence and route recorded in `research/korean-localization-2026-10-19.md`.

### Tenth Korean source pass — FASTPANEL VPS Hosting (2026-10-20)

- Page 9 `컨트롤 패널이 있는 VPS` is published from PR #5 source `11aeb5cd`, generated Cloudflare static `74dfa08f`; the live page opened in Opera and the dedicated production Chromium run `39468143187` passed 390px/1280px and nine form scenarios. Page 9 is closed.
- Page 10 scoped to the branded intent `FASTPANEL VPS 호스팅`, exact Title=H1 and slug `/ko/fastpanel-vps-호스팅/`. It is the child of the general control-panel page, not a duplicate selection article.
- On `work/ko-fastpanel-20261020`, complete Korean content has 31 anchored headings (16 H2/15 H3), one plan table/6 lines, 83 bullet points, 17 numbered steps, ten FAQ, original 11 internal Markdown destinations and two unchanged VDSina sponsored article CTAs. All four diagnostic IDs and ten options are unchanged, and original JavaScript conditions/score thresholds are unchanged; three outcomes and all UI copy translated.
- FASTPANEL shared hero's 14 user-facing text/ARIA slots are KO-only conditional translations; EN and other languages retain original else copy, layout and affiliate links. Official VDSina and FASTPANEL setup facts rechecked 2026-10-20; one-GB install minimum is not a production capacity promise.
- Blocking prepublication workflow `.github/workflows/qa-ko-fastpanel.yml` should validate the Hugo build, 390/1280 geometry and all 36 actual form input combinations before merging. After merge, verify main CI -> static Cloudflare generation -> deployed live URL -> separate live browser QA. No publication/complete claim until these succeed. Source of truth remains GitHub main.

- Prepublication [Korean FASTPANEL Chromium run 39468849212](https://github.com/agurkin2021-gif/vpsforwebsite/actions/runs/39468849212) completed **Success**. Hugo 0.158.0 production-style build passed. At **390px and 1280px**, measured document/body scroll widths equal viewport widths; header, hero, H1 and checker bounding rectangles fit. Page produced 31 anchored headings, one table, four selectors/ten options, localized hero, SEO Title/H1/canonical and sponsored partner links, without JS errors. At 390px Chromium selected all **36** combinations of workload (3), site count (3), mail (2) and jobs (2), submitted the form, and confirmed the expected 2 GB / 4 GB / 8 GB Korean guidance. Screenshots were saved as workflow artifacts. This verifies preview QA only; publication/live verification is still pending.

## Current localization pass — Korean, 2026-10-19

- Owner requested Korean `ko`, natural commercial search language and careful page-by-page work. No bulk or shortened article translation.
- First completed source pass: `/ko/`, Title/H1 `웹사이트용 VPS 호스팅`; all seven feature sections, 13 FAQs, four plan tiers, shared CTA and 228 homepage/diagram/form/switcher UI strings translated.
- Registered ko/한국어/ko-KR in Hugo, added Korean navigation with real English fallback destinations until supporting pages are translated. No nonexistent Korean routes or thin placeholder articles.
- All 216 fit-checker input combinations preserve the original five decisions; all results are localized. Preserved 16 rendered homepage affiliate placements and attributes, pricing/spec values, original owner-supplied WebP, and English/Spanish visible text.
- Hugo 0.158.0 production and project-path preview build/SEO checks pass. Local browser QA at 390/1280 px, language switching and mobile navigation pass. Hangul wrapping, pricing labels and FAQ line-height adjusted without changing other languages.
- Hreflang duplication from the upstream SEO partial is removed; shared head emits one set and English x-default. Preview retains noindex and omits canonical/hreflang/GA. Homepage Markdown links resolve under the preview base path.
- Detailed evidence, audit exceptions and the remaining page queue: `research/korean-localization-2026-10-19.md`. No Korean search-volume claims; no invented Korean server locations, Korean-language provider support, KRW billing or local payment options.
- Deployment uses the current AGENTS.md GitHub main → generated Cloudflare static → connected Worker contract. The old Spanish preview-only/no-production instructions are historical for this new authorized language addition. No manual Worker or generated-content editing.
- Homepage published: source `37b43069c4156856731cce5fc759ab83ca932c1a`, generated `efc4b33376a3e6a0da20f5f57c2087631f3ebd71`; both Actions and Cloudflare Workers Builds succeeded. Live `/ko/` returns HTTP 200 with correct SEO and sitemap inclusion.
- Second source pass complete: `웹사이트용 VPS 사양`, `/ko/웹사이트용-vps-사양/`. All 29 headings, four tables, seven FAQs and two tools translated. All 729 diagnostic inputs and nine RAM boundaries preserve the original behavior; worked example returns 2.4 GB and a 4 GB tier. Production/preview builds and responsive/SEO/link checks pass. Sizing publication pending.
- Shared article disclosure now localized with a working English About fallback. Wide Korean plan comparison table supports horizontal scrolling on mobile; English content and behavior unchanged.
- Website migration (page 3) completed as a full Korean source pass: Title/H1 `웹사이트 VPS 이전`, route `/ko/웹사이트-vps-이전/`, source `content/korean/website-migration-to-vps.md`. Original 31 headings, 2 tables, 8 FAQ, 25 numbered items, 106 bullet points, 8 internal guide-link targets and 2 body affiliate links preserved; Korean Markdown render-link now resolves translated targets or falls back to real English pages.
- Korean migration preflight: same 10 controls/values and English decision tree; 2,304/2,304 combinations match readiness classification. Dedicated migration hero strings localized only for KO with EN unchanged.
- Korean website migration publication verified: source `24ee5c9775c9dbe6107e474e9ecddc9bb0877f04`, Hugo validation `39439557832` success, static preparation `39439558022` success, generated static `69b1bbc2eaec9e77d457fda5bdd5f250d285e5ab`, Cloudflare Workers Builds success. Live article opened in Opera (not a 404), Korean hero and form visible; generated Title=H1, self-canonical, index/follow, equivalent hreflang and sitemap confirmed. Full resized mobile/desktop geometry testing not independently performed in this session. Next Korean page: Managed vs Unmanaged VPS. Other Korean pages remain untranslated.

- Korean fourth guide (Managed vs Unmanaged VPS) translated individually on work branch `work/ko-managed-vs-unmanaged-20261020`: exact target Title/H1 `관리형 VPS와 비관리형 VPS`, slug `/ko/관리형-vps와-비관리형-vps/`, source `content/korean/managed-vs-unmanaged-vps.md`. All 36 headings, 40 table lines, 118 bullets, 16 numbered questions, 9 FAQs, original form controls/values and affiliate links preserved; all 36 headings have explicit stable anchors. Interactive Management Fit Checker has the same condition tree and four localized outcomes; source JavaScript normalizes byte-identically to English apart from output messages. Only this guide's shared hero labels were localized conditionally for ko; English and other languages remain as before. Korean-aware internal links resolve completed pages or real English fallbacks. Hugo production validation run `39443264213` succeeded; static preparation run `39443264612` succeeded. Source commit `06478c9d49740bd1b36fdce2f0eb647210e144bd` generated publishable static commit `674030133f94b8800ddc5073194c3c75b0c62a8c`. Cloudflare Workers Builds completed successfully. Live Korean URL opened in Opera after deployment with the correct Korean title, hero and checker. Production HTML has 17 H2 + 19 H3, four tables, eight form selects/18 options, three sponsored affiliate links, index/follow, self-canonical, correct localized article links and hreflang. Independent mobile viewport geometry and end-to-end submit interaction were not browser-tested (Opera screenshot connector unavailable; remote Desktop Commander quota exhausted). Next Korean guide: VPS for WordPress.

### Fifth Korean page: WordPress VPS — 2026-10-20

- Continuing the owner's one-page-at-a-time instruction. Selected exact Korean query/Title/H1 **워드프레스용 VPS**, slug `/ko/워드프레스용-vps/`; file `content/korean/vps-for-wordpress.md`.
- Complete Korean translation in branch `work/ko-wordpress-20261020`: 34 headings, four tables, ten FAQ, one seven-select WordPress VPS Fit Checker with preserved algorithm/inputs, all English section anchor IDs, internal-link fallbacks, original VDSina affiliate URL and numeric examples. WordPress hero and diagram translated with Korean-only conditions in `layouts/_partials/page-header.html`. English/Spanish text/logic retained.
- Audited heading, table, bullet, control-ID/option-value, link and numeric-pricing parity with the English source. Main Hugo build, Cloudflare deployment and live mobile viewport still require verification; do not claim they passed until confirmed.
- After publication validation, next Korean page is **VPS for WooCommerce**.

### Ninth Korean guide: VPS with Control Panel — 2026-10-20 (prepublication)

- Individual intent owner: `컨트롤 패널이 있는 VPS`, exact Title/H1/slug `/ko/컨트롤-패널이-있는-vps/`. Commercial informational choice of whether a VPS needs a hosting control panel and which operating model fits; distinct from provider dashboard, managed support and the FASTPANEL branded child. Search volume not claimed.
- Work branch `work/ko-control-panel-20261020`. Complete Korean source `content/korean/vps-with-control-panel.md` produced in three sequential blocks; preserves 36 original section headings and anchors, 3 tables/22 Markdown table lines, 123 unordered bullets, 12 ordered list lines, 10 FAQ, 7 form selects with 16 option values, 13 original article internal-link occurrences and 2 VDSina sponsored content links. The form has seven Korean outcomes with JavaScript logic byte-identical to English after only the result strings are normalized.
- `layouts/_partials/page-header.html` adds Korean-only strings in the existing control-panel hero; the else branches preserve English/other-language visible content, styles and layout. Korean Markdown link renderer chooses translated targets where present and existing English fallbacks elsewhere.
- Dedicated branch workflow `.github/workflows/qa-ko-control-panel.yml` builds Hugo production-style and runs Chromium 390px/1280px SEO/responsive checks plus nine actual form submissions; screenshots are retained temporarily. This is a verification plan, not a pass claim. Do not merge/publish before success. User's requested English reference remains unchanged.

- Prepublication [Chromium run 39466993685](https://github.com/agurkin2021-gif/vpsforwebsite/actions/runs/39466993685) finished **Success**. Measured HTML and body widths exactly 390/390px and 1280/1280px; header, title, hero grid and form stayed inside both viewports; no page-wide horizontal overflow or JavaScript errors. All 36 section anchors, three tables, seven controls/16 options, Korean Title/H1, canonical, hero and sponsored links passed. Nine actual form interactions (seven result branches plus two priority cases) returned expected Korean outcomes. Screenshots stored as temporary GitHub Actions artifacts. Publication/live gate still pending.

## Project identity

- Project: **vpsforwebsite.com**
- Repository: **agurkin2021-gif/vpsforwebsite**
- Stack: **Hugo**
- Theme/base: **original Hugoplate**
- GitHub is the persistent source of truth for code and project continuity.

## Non-negotiable design rule

The site must use the **original Hugoplate visual system**.

Do NOT create a new visual design on top of Hugoplate.
Do NOT replace the theme with a custom landing-page design.
Do NOT introduce a separate custom color system, typography system, card system, hero system, or page composition unless the user explicitly requests it.

Preserve and reuse Hugoplate's native:

- header and footer;
- hero/banner composition;
- grid;
- spacing;
- typography;
- buttons;
- alternating image + text sections;
- CTA sections;
- responsive behavior;
- dark-mode/theme behavior where present;
- standard Hugo/Hugoplate layouts and components.

The correct approach is:
**keep the Hugoplate design and adapt its existing sections to VPS content.**

Custom CSS/JS should be kept to the minimum required for compatibility or content, not used to redesign the theme.

## Content goal

The homepage is the commercial front page for VPS hosting for websites.

It must explain the offer clearly and lead users to the existing commercial/internal VPS pages in the repository.

Preserve the existing VPS-related content and page intent. Do not invent unrelated sections or redesign the information architecture without an explicit user request.

## SEO invariants

### Exact keyword / Title / H1 / URL rule

For every target commercial page, the primary target query must be used **without tails or additions** in the page naming elements.

Required:
- `Title` = exact primary target query;
- `H1` = exact same text as `Title`;
- URL slug = the same keyword phrase in URL form (lowercase, words separated with hyphens);
- no extra words before or after the primary query in `Title` or `H1`.

Example for the main target:
- primary query: `VPS for website`
- Title: `VPS for website`
- H1: `VPS for website`
- URL form for an internal page would be: `/vps-for-website/`

For the site homepage at `/`, the root URL is retained; do **not** create a duplicate `/vps-for-website/` homepage only to mimic the slug.

Homepage primary target query is fixed as: **VPS for website**.

For every indexable page preserve/check:

- exactly one H1;
- relevant Title;
- relevant meta description;
- self-referencing canonical;
- valid Open Graph metadata where used;
- valid JSON-LD where used;
- internal linking;
- valid sitemap;
- valid robots.txt;
- no duplicate page variants created accidentally;
- no broken internal routes;
- HTTP 200 for intended public pages;
- responsive rendering on mobile and desktop.

Do not sacrifice SEO structure while changing presentation.

## Git / publishing workflow

- Keep the repository on GitHub.
- Work from the repository, not from memory alone.
- Make changes in GitHub and verify the Hugo build.
- Treat the public visual site as the user's review surface.
- The user does **not** want GitHub repository links or commit links as the normal result after visual changes.
- After each completed visual change, provide the **active published site URL**.
- Do not use a long `htmlpreview.github.io` URL as the final deliverable once normal publishing is available.

Target public URLs:

- GitHub Pages interim URL: `https://agurkin2021-gif.github.io/vpsforwebsite/`
- Final custom domain: `https://vpsforwebsite.com/`

Before claiming that either URL is live, verify that it actually opens successfully.

## Current design history

Earlier work incorrectly used Hugoplate mainly as a technical base while adding a custom visual design.

That approach was rejected.

The custom design was then removed and the project direction was reset to:
**original Hugoplate visual system + VPS-specific content only.**

Future sessions must not repeat the rejected custom-design approach.

## Current continuation point

Continue from the current repository state.

Priority:

1. Keep/restore the stock Hugoplate look.
2. Finish the homepage ("морда сайта") using native Hugoplate sections only.
3. Preserve existing VPS content and SEO structure.
4. Verify Hugo build and page routes.
5. Verify GitHub Pages/public deployment.
6. Return the active published site URL for visual review.

If repository code and old chat recollections conflict, inspect the current repository first. For design intent, the rules in this file are authoritative unless the user explicitly changes them.

## Communication rule for this project

After a visual/site edit, the user primarily wants the **working visual URL of the site**, not repository or commit URLs.

Do not claim publication is complete until the public URL has been checked.


## Mandatory context maintenance

After every substantive change to site code, content, SEO, layouts, navigation, deployment, or configuration, update this file in the same work session.

Record:
- what changed;
- new user rules/decisions;
- current state;
- deployment state;
- blockers/known defects;
- exact next continuation point.

A future ChatGPT session must read this file before modifying the repository.


## Context update log

### 2026-10-12
- Permanent review URL rule: after every site/content edit, use this exact fixed browser URL for visual review: `https://htmlpreview.github.io/?https://github.com/agurkin2021-gif/vpsforwebsite/blob/preview/index.html`. Do not invent or rotate preview URLs. The `preview` branch is rebuilt automatically from `main` by `.github/workflows/pages.yml`; the user should be able to keep this URL open and refresh it to see the latest preview.
- Homepage content-gap closure: filled the remaining concise-answer gaps without adding another major section. Hero now defines VPS-for-website; sizing covers WordPress/WooCommerce/multi-site workload differences plus location/CDN and fuller pre-purchase/price-scope checks; recovery explicitly distinguishes snapshot/rollback from backup; an 8-question FAQ/direct-answer section now covers remaining buyer questions including immediate post-purchase sequence. The 22-question homepage inventory is now covered at summary level. Content can be frozen once build and visual verification pass.

- Deep homepage content audit: the six decision blocks are implemented, but content is not frozen yet. Against the prior 22-question inventory, 12 are sufficiently answered, 6 are partial, and 4 remain open (server-location explanation, CDN/Cloudflare effect, snapshot-vs-backup distinction, first steps after purchase). The planned FAQ/direct-answer layer is also absent from the current home layout. Close these through compact additions/FAQ; do not add another large conceptual section.

- VDSina panel screenshot confirms current balance top-up bonuses: from $100 -> +10% bonus; from $1,000 -> +20% bonus. This is a top-up bonus, not a VPS tariff discount; payment systems may still charge extra processing fees. Use only as compact conversion copy and re-verify before future major rewrites because terms can change.

- Payment screenshot bonus confirmation: VDSina finance interface shows 10% bonus on balance top-ups from $100 and 20% bonus from $1,000; interface also warns payment systems may charge extra fees. Treat as conversion copy, not as a claimed server-plan discount.

- Payment screenshot confirmation: VDSina interface visibly lists International card, USDT TRC20, TRX, Bitcoin, Litecoin, Ethereum, BNB, Other cryptocurrencies, SBP, Russian bank card, Other payment methods and SWIFT; crypto minimum shown as $20, international card minimum $10, SWIFT minimum $100. Treat screenshot/interface labels as authoritative current evidence.

- Crypto payment correction: user confirms the exact current crypto methods are explicitly listed in the VDSina payment interface. Treat that interface as authoritative. Exact currency/network labels may be published if copied literally from the panel; do not guess or normalize network names from memory.

- Crypto-payment intent audited: cryptocurrency top-up is a useful conversion/trust feature, not a core SEO/WOW intent. VDSina support publicly confirms crypto funding and a current $20 minimum; public support also mentions USDT TRC20. Exact full coin/network list is not fully verified from official public pages, so do not publish BTC/LTC/ETH/USDT network lists until checked directly in the payment interface or current official documentation.

- VDSina provider-differentiator audit completed. Strongest concrete differentiator found: downloadable full server backup images; VDSina documents downloading the backup as `.img.gz`, while DigitalOcean and Vultr explicitly state provider backups/snapshots cannot be directly downloaded.
- Strong combined positioning: **portable, cloneable, scalable VPS** — clone server, scheduled backups, restore/create server from backup, downloadable image, own ISO/VNC, API management, upward resource scaling while retaining settings.
- Strong architecture-specific advantage: advertised 10 Gbit/s public port plus free local network up to 100 Gbit/s within a location, useful for web+DB+worker multi-VPS designs.
- Keep homepage usage compact: scale without rebuilding; clone before risky changes; keep a portable image; split later over private networking. Do not turn homepage into a provider feature dump.

- Novel-intent hunt #2 completed: strongest new rival to the Fit/Readiness Engine is a **VPS Architecture Planner / "One VPS or Split?"** tool. It decides whether website, DB, staging, workers/automation/AI agent and multi-site workloads should remain on one VPS or be split, and in what order.
- Existing SERPs contain separate articles about DB separation, staging separation and single-vs-multi VPS, but no strong unified website-focused personalized planner was found in this pass.
- Runner-up WOW utility: **VPS True Cost / TCO Calculator** for server + panel + backups + monitoring + admin time + per-site cost.
- Current novelty ranking is stored in `CHATGPT_SEO_AUDIT_BUFFER.md`: Fit/Readiness Engine #1; Architecture Planner #2; website+AI agent combined sizing #3; VPS TCO #4.

- Windows web-stack intent audited: VDSina Standard verifies Windows Server 2025/2022/2019/2016/2012 R2 templates; automatic Windows installation is available from 2 vCPU / 4 GB RAM upward, with the Windows license included, and RDP access is supported.
- Generic `Windows VPS Hosting` is highly competitive and should not be treated as a gap. Relevant website-focused supporting candidates are `VPS for IIS` (P1/P2) and `VPS for ASP.NET` (P2). Keep SQL Server as supporting content first. Exclude generic RDP/trading/desktop intent from the core site.
- Future homepage OS/management fork can remain compact: FASTPANEL, pure Ubuntu/Linux, or Windows Server for IIS/ASP.NET-specific workloads.

- Ubuntu/Linux intent audited: broad `Ubuntu VPS Hosting` and `How to host a website on Ubuntu VPS` are real but heavily covered by competitors. VDSina Standard currently verifies pure Ubuntu 26.04/24.04/22.04/20.04 templates.
- Stronger project-specific supporting angle: `VPS without Control Panel` -> pure Ubuntu/Linux over SSH with Nginx/Apache + runtime + database. Proposed exact page `/vps-without-control-panel/`, status P1/P2 boundary.
- Homepage should eventually show a compact management fork: FASTPANEL/control panel vs pure Ubuntu/Linux over SSH. Detailed commands stay off the homepage.

- FASTPANEL intent audited and promoted to a strong P1 supporting-page candidate. VDSina currently lists **FASTPANEL on Ubuntu 22** as a web-hosting-control-panel deployment option on Standard VPS/VDS. Proposed exact page: `VPS with FASTPANEL` -> `/vps-with-fastpanel/`.
- Keep generic `VPS with Control Panel` as the comparison/choice page; FASTPANEL page should own branded commercial intent: sizing FASTPANEL + websites, verified VDSina deployment path, WordPress/site creation, domains/SSL/PHP/database/multiple-sites workflow.
- Do not infer that FASTPANEL’s 1 GB minimum is a recommended website size; panel overhead and actual workload must be included in sizing.

- SSH intent classification added: `How to connect to VPS via SSH` is important operational content but already well covered in SERPs, so it is not a novel/WOW gap. Keep only a brief SSH mention on the homepage; place the detailed SSH section inside future `How to Host a Website on VPS`, with SSH hardening linked to future `VPS Security Checklist`. Standalone SSH page remains HOLD pending keyword opportunity validation.

- AI-agent adjacent intent audited: broad `VPS for AI agent` is already competitive and is not a novel gap. More defensible website-centric angle is `website + API-based AI agent/automation on one VPS`, with combined sizing and an explicit one-VPS-vs-two-VPS decision.
- VDSina is currently verified as a general self-managed VPS platform with OS/software installation and API management; no dedicated official preinstalled/managed AI-agent offer was found. Do not claim one.
- Keep AI-agent content as a supporting use case / Fit Engine dimension for now; dedicated page remains HOLD pending query validation.

- Novel-intent research completed: strongest under-owned opportunity is a **VPS Fit / Readiness Engine** rather than another generic article. It combines: need-VPS diagnosis, optimize-first branch, translation of real cPanel/CloudLinux usage into VPS sizing, self-managed readiness, migration-risk scoring, and mapping to verified VDSina tiers.
- Closest competitors only cover fragments (generic calculators, cPanel-to-VPS sizing articles, readiness checklists, migration guides). Do not claim nobody has anything similar; differentiation is the combined diagnostic workflow.
- Architecture decision: keep homepage H1 exactly `VPS for website`; use the diagnostic as a homepage supporting utility/message, with deeper routing to sizing, VPS-vs-shared, managed-vs-unmanaged, and migration pages.

- Deep SEO audit expanded further in `CHATGPT_SEO_AUDIT_BUFFER.md`: added pre-purchase gaps (buying checklist, traffic-capacity misconception, RAM-tier meaning, backup vs snapshot, security responsibility, monitoring/scale triggers, location/CDN/email/staging/deployment), niche-use-case scan, authority-content layers, 22-question homepage inventory, homepage information-architecture blueprint, competitor module audit, and Google Search implementation rules.
- Current strategic model for homepage: resolve five buyer decisions — Fit, Size, Responsibility, Risk, Action — while routing deep intents to supporting pages rather than bloating/cannibalizing the homepage.
- New candidate priorities preserved: P1 core = sizing, migration, managed-vs-unmanaged; P2 authority = how to host a website on VPS, security checklist, backup strategy, maintenance checklist; membership-site intent is a promising HOLD candidate pending volume/SERP validation.

- Deep SEO audit expanded: competitor coverage matrix added; confirmed internal-page Hugoplate H1 passes Title through Hugo `title` transformation and therefore exact Title/H1 equality must be verified in generated HTML; identified missing contextual return links from supporting pages and the homepage hero CTA routing too narrowly to WordPress.
- Fixed homepage primary query as `VPS for website`.
- Added exact SEO rule: `Title` = primary query; `H1` = identical `Title`; URL slug = same phrase in URL form; no tails in Title/H1.
- Clarified homepage exception: homepage remains at `/`, so no duplicate `/vps-for-website/` page should be created merely to mirror the slug.
- Root `AGENTS.md` now enforces reading and updating this context before/after substantive repository work.


## Recovered SERP / intent / gap research

Recovered from prior project work on 2026-10-12. This section records what is still known even though the detailed `/research/` artifacts are not present in the current repository.

### SERP / competitors
The prior SERP review for `VPS for website` identified these recurring competitors / result types:
- ServerCalc
- VPS-Mart
- Database Mart
- Hostinger
- Liquid Web
- Cybernews
- TechRadar
- OVHcloud

Observed SERP formats included:
- use-case landing pages;
- provider/commercial pages;
- informational comparison/guides.

### Intent ownership currently preserved
- `/` -> `vps for website`
- `/vps-for-wordpress/` -> WordPress VPS intent
- `/vps-for-woocommerce/` -> WooCommerce VPS intent
- `/vps-vs-shared-hosting/` -> VPS vs shared hosting comparison intent
- `/vps-for-multiple-websites/` -> multiple-sites sizing/operations intent
- `/vps-with-control-panel/` -> control-panel choice intent
- `/managed-vps-for-website/` -> HOLD

### Known open content/intent gaps from the prior audit
The prior audit surfaced these as opportunities/gaps to cover:
- resource-selection decision tree / comparison table / calculator;
- when a website needs VPS vs when it does not;
- WordPress-specific VPS guidance;
- WooCommerce-specific VPS guidance;
- hosting multiple websites on one VPS;
- managed vs unmanaged VPS;
- VPS vs shared hosting;
- concrete resource/spec sizing guidance;
- server/location considerations;
- beginner-oriented deployment guidance.

### Gap-closure status
Important: no reliable explicit closed/open gap ledger is currently stored in this repository.
The recovered prior summary did **not** explicitly mark the above gaps as closed.
Do not claim a gap is closed unless the current page implementation is checked against the intended gap and the result is recorded here.

### Missing research artifacts
A previous project note referenced completed research artifacts such as:
- `/research/serp-2026-10-12.md`
- `/research/competitors.md`
- `/research/intent-map.md`
- `/research/content-gaps.md`

These files are **not present** in current `main` or `preview` as of 2026-10-12. Treat this as a preservation defect. Future SERP/on-page research should be committed to the repository, not left only in chat/local context.


## SEO audit buffer

Persistent SEO/SERP working state is stored in:
- `CHATGPT_SEO_AUDIT_BUFFER.md`

Every new session doing SEO, content architecture, homepage work, supporting-page work, or internal linking must read that file after `CHATGPT_PROJECT_CONTEXT.md`.

The SEO buffer contains:
- current SERP observations;
- competitor patterns;
- homepage keyword ownership;
- on-page gaps;
- supporting-query candidates;
- intent ownership;
- internal-link architecture;
- OPEN / CLOSED / HOLD gap ledger;
- page-by-page continuation point.

### 2026-10-12 continuation decision
- Build **page by page**.
- Finish the homepage first.
- Do not build new supporting pages until the homepage passes its completion gate.
- Homepage owns `VPS for website` plus close semantic variants such as `website VPS hosting` and `VPS hosting for websites`; do not create duplicate pages for those variants.
- High-priority future supporting intents currently identified: `VPS sizing for website`, `Website migration to VPS`, and `Managed vs Unmanaged VPS`.
- Supporting pages must return contextual internal links to the homepage.


### 2026-10-12 — Homepage assembly pass

- Homepage content assembled for visual review using the original Hugoplate visual system; no new custom design system was introduced.
- Exact homepage target is now literal everywhere relevant in page/site naming: `VPS for website`.
- Homepage hero CTA now routes to the on-page Fit/Readiness section instead of routing narrowly to WordPress.
- Homepage is intentionally limited to six major decision blocks:
  1. need-VPS / optimize-first Fit Check;
  2. workload-based sizing + pre-purchase factors;
  3. management path (FASTPANEL/control panel vs pure Ubuntu/Linux vs Windows web stack);
  4. migration pre-flight / rollback thinking;
  5. one-VPS-vs-split architecture decision;
  6. clone/test/scale/recover growth path.
- Strong supporting intents remain supporting-page work and were not expanded into full tutorials on the homepage.
- Provider-specific commercial proof is kept compact: local-network capability, cloning/scaling/recovery/portable backup image, 10 Gbit/s advertised public port, DDoS protection, 24/7 support, daily billing, crypto/card funding and current top-up bonus tiers.
- Final CTA includes an affiliate disclosure and keeps the VDSina partner URL.
- Added a local `layouts/home.html` override that preserves stock Hugoplate classes/composition while adding semantic section anchors, descriptive image alt text and `rel="sponsored nofollow noopener"` for external homepage buttons.
- Current state after this pass: content/IA assembled; Hugo Actions build and public visual rendering must pass before the homepage is called complete/frozen.
- Next continuation point: verify final GitHub Actions build, inspect the published homepage visually/structurally, then decide whether any section should be cut or shortened before moving to supporting pages.


### 2026-10-13 — VPS sizing page completion pass
- /vps-sizing-for-website/ was rebuilt against the stored SERP/intent specification and dense audit.
- Primary query naming is now literal: Title = H1 = VPS sizing for website; a local Hugoplate-preserving page-header override outputs .Title without automatic Title Case transformation.
- Added two no-login interactive utilities inside the page: a transparent RAM budget estimator and a shared-hosting-to-VPS diagnostic using memory/CPU/entry-process/I/O fault patterns. The diagnostic explicitly avoids one-to-one CloudLinux-limit-to-VPS conversion.
- Added numeric RAM, CPU/concurrency, peak-load and storage worked examples; diagnostic symptom matrix; Low/Medium/High confidence labels; explicit fit limits; and mapping to the four verified Standard configurations.
- Added commercial path: VDSina partner CTAs with sponsored/nofollow/noopener attributes and human-readable affiliate disclosure.
- Fixed supporting-page contextual URLs with Hugo relref, so WordPress, WooCommerce, Multiple Websites, Control Panel and VPS vs Shared Hosting resolve correctly in preview and production.
- Added one contextual return link to the homepage and added VPS Sizing to the Guides menu.
- Preview indexing hardening: raw.githack builds now emit noindex,nofollow, omit canonical/hreflang, and the preview workflow removes sitemap.xml. Production behavior remains indexable/self-canonical.
- Added WebPage + BreadcrumbList JSON-LD for inner pages; removed obsolete global meta-keywords; added a real OG image for the sizing page.
- Replaced the upstream Hugoplate favicon with a local three-server-rack SVG favicon.
- Verification: preview workflow for main commit 74b1ec5b0dcdd9b405433c9f876191bbacda9488 succeeded. Preview branch commit 63711e18f4936f82e42b1fa8f1b6d9c4498e5906 contains Title/H1 exact match, noindex/no canonical, no sitemap, 2 JSON-LD blocks, both interactive modules, seven affiliate links, and corrected internal routes.
- Live Hugo production build itself succeeds, but GitHub Pages deployment still fails at actions/deploy-pages@v4 with HTTP 404: GitHub Pages is not enabled for the repository. This is a repository Pages setting blocker, not a Hugo/page build failure.
- Review surface remains the fixed preview workflow/URL until Pages is enabled.


### 2026-10-13 — VPS sizing finalization pass
- Continued work on /vps-sizing-for-website/ instead of moving to the next page.
- Made provider mapping explicit: current VDSina Standard reference tiers now include verified current prices and monthly transfer allowances; values checked against the official Standard pricing page on 2026-10-13.
- Improved RAM estimator UX using native Hugoplate form classes and light/dark panels; arbitrary example values are now placeholders instead of silent defaults, while 25% headroom remains an editable starting assumption.
- Improved Shared Hosting -> VPS diagnostic UX with native form styling, ARIA live result blocks and an additional NPROC/process-count pressure input.
- Added guidance to use CloudLinux/cPanel Resource Usage history rather than a single instantaneous reading.
- Diagnostic logic now includes process-count saturation in findings and repeated-limit scoring.
- Pricing/transfer terms are explicitly caveated as changeable provider terms.
- Source commit for this pass: b65676a7bb871243250550556b2c467053a92f33.
- Verification completed: preview workflow run 38383656385 succeeded. The rendered preview was visually checked at the top, RAM estimator and shared-hosting diagnostic sections. All intended internal route files exist in the preview branch.


### 2026-10-13 — VPS sizing scope closed
- Finished the three remaining planned sizing-page content gaps instead of moving to another page.
- Added a dedicated workload-comparison table covering cached/static, small WordPress, WooCommerce/transactional, multiple-sites and background-worker/automation-heavy patterns.
- Added a bandwidth/monthly-transfer sizing section with an origin-transfer formula, CDN/cache-offload example, and an explicit distinction between transfer allowance and network port speed.
- Expanded panel overhead into panel + mail overhead, covering SMTP/IMAP/POP, spam/AV, queues, logs and mailbox storage, plus the managed-mail alternative.
- Preview build for source commit 5faa184b3f389d82b178afdab0b8ae220d86f65c succeeded.
- Preview artifact commit 1b9064108878378eef319c460a1da15741202464 was visually checked; the three new headings render and the workload table is visible.
- Current decision: /vps-sizing-for-website/ now contains the full material planned for its own approved scope. P2 tools such as TCO, full peak-event planner, architecture planner and migration-risk calculator remain intentionally outside this page.


### 2026-10-13 — Website migration to VPS page
- Next P1 page implemented at /website-migration-to-vps/.
- Primary query, Title and H1 are fixed as: Website migration to VPS.
- SERP/query research was committed to research/website-migration-to-vps-serp-2026-10-13.md. Query family reviewed: website migration to VPS, migrate website to VPS, move website to VPS, transfer website to VPS, shared hosting to VPS migration. Search volume remains unverified.
- Page scope is a same-domain/same-URL hosting migration. URL-changing/domain-changing moves are explicitly separated as a different redirect/mapping problem.
- Core flow: inventory -> destination sizing -> independent backup/rollback -> destination build -> initial copy -> private test -> final write/data sync -> DNS -> mail/HTTPS/external services -> SEO parity -> acceptance/rollback.
- Added a functional no-login Migration cutover preflight checker covering backup, sizing, runtime compatibility, private testing, DNS/TTL, email, final writes, TLS, cron/webhooks/allowlists and rollback.
- Strong migration gaps closed: dual-writer/data divergence risk, final delta/write-freeze logic, DNS TTL semantics, narrow DNS changes, email split risk, cron/worker double execution, webhooks/IP allowlists, same-URL SEO parity, rollback data boundary and post-cutover acceptance.
- Internal linking added: homepage migration block -> migration page; sizing page -> migration page; migration page -> homepage, sizing, control panel, WordPress and WooCommerce.
- Guides menu now includes Website Migration.
- Commercial path uses VDSina partner CTA with rel=sponsored nofollow noopener and a human-readable affiliate disclosure. No claim is made that VDSina includes managed migration.
- Preview build for source commit 4cb87e94ef89969dbff724e0c9dc5b3ea8ad3ada succeeded.
- Generated preview verification: Title = H1 = Website migration to VPS; preview noindex,nofollow present; preview canonical absent; WebPage + BreadcrumbList JSON-LD present; migration checker rendered; 2 affiliate links with matching sponsored attributes.
- Browser visual review completed for the first screen and Migration cutover preflight form; both render in native Hugoplate styling.
- Preview route files confirmed for homepage, sizing and migration; homepage and sizing generated HTML both link to the new migration route.
- Live production Hugo workflow continues to fail only at GitHub Pages deployment because Pages is not enabled/configured; page build itself is successful.
- Next continuation point after user review: dense audit of this page before freezing it, then Managed vs Unmanaged VPS.


### 2026-10-13 — Website migration final audit
- Final dense-audit fixes completed for /website-migration-to-vps/.
- Preflight now requires destination sizing and every applicable unresolved item blocks READY status.
- Email and jobs/webhooks support explicit Not applicable states.
- Backup acceptance now requires restore/import testing where practical plus representative-data verification.
- DNS guidance now says to lower TTL at least one full previous-TTL interval before cutover when possible, and preserves SRV and CAA records as well as mail/verification records.
- Same-domain/same-URL hosting moves explicitly state that the Google site-move address-change tool is not used.
- Cutover checklist uses the stronger restore-tested backup criterion.
- Page content is frozen after final build/render verification; next planned page is Managed vs Unmanaged VPS.


### 2026-10-13 — Managed vs Unmanaged VPS
- Implemented /managed-vs-unmanaged-vps/ with exact Title/H1, responsibility matrix, Management fit checker, total operating cost, support-vs-management, panel-vs-management, incident/backup/security ownership, hybrid paid-admin path and VDSina scope boundary.
- Research saved at research/managed-vs-unmanaged-vps-serp-2026-10-13.md; volume unverified.
- Homepage and migration now link to the page; Guides menu includes it. Page links to homepage, sizing, control panel and migration.
- Preview build for source commit 2445ba35805efff2b7602bebfc5abc8299e92d89 succeeded; preview artifact 77fc5ba02230b3451b38d205c5402fd839fb70a2 was visually checked at first screen and checker.
- Generated checks: Title=H1, preview noindex/nofollow, no preview canonical, JSON-LD present, partner CTA has sponsored/nofollow/noopener.
- VDSina is not described as fully managed: current Standard page lists 24/7 technical support while separate public QA documents administration as an additional ordered service.
- Next planned page after freeze/audit: VPS with FASTPANEL.


### 2026-10-13 — Fresh architecture SERP audit
- Re-ran SERP validation for the pages surrounding the homepage.
- Full audit saved at research/serp-architecture-audit-2026-10-13.md.
- Main correction: do not create VPS without Control Panel as a separate core page; merge that intent into How to host a website on VPS because current SERP resolves to the same manual deployment/tutorial job.
- Replace core VPS Maintenance Checklist with a cleaner VPS Monitoring owner; monitoring has a stronger distinct SERP while maintenance substantially overlaps security and backup.
- Retarget the future FASTPANEL page toward the stronger current commercial phrase FASTPANEL VPS Hosting; run a dedicated page-level SERP before fixing exact Title/H1/URL.
- Add a separate location-decision page (provisionally How to Choose VPS Location) to keep the core cluster at 14; current SERP is distinct around latency, routing, audience geography, CDN/origin and operational/jurisdiction fit.
- Corrected core 14 is recorded in CHATGPT_SEO_AUDIT_BUFFER.md section 54.
- No existing built page was deleted or retargeted by this audit; these are architecture decisions for remaining work.


### 2026-10-13 — Persistent SERP work plan file
- Added root text file `SERP Audit.txt` as the persistent work plan for the homepage support cluster.
- The file records the corrected 14-page architecture, current status, merge/retarget decisions, cannibalization rules, HOLD list, recommended work order and the standard SERP->build->audit workflow.
- This file should be read together with CHATGPT_PROJECT_CONTEXT.md and CHATGPT_SEO_AUDIT_BUFFER.md before continuing the surrounding-page build plan.


### 2026-10-13 — Managed vs Unmanaged VPS frozen
- Rechecked the exact/near-exact SERP after the architecture rewrite; recent 2026 results still show a distinct managed-vs-unmanaged comparison intent. Page remains necessary and should not be merged with the homepage, VPS with Control Panel, or VPS vs Shared Hosting.
- Final dense audit additions: management-claim decoder table, explicit unmanaged-production red flags, stronger total-operating-cost comparison worksheet, official VDSina provider references, and a stricter paid-admin warning for high-impact/custom workloads.
- VDSina truth was revalidated: Standard VPS advertises round-the-clock technical support; separate official QA describes server administration as an additional paid service. Therefore the referred VPS is not represented as fully managed.
- Final preview build after the page edits succeeded; preview artifact 23b73011a5cce24c9cc1a9dee244431ff91adc49. Generated checks: exact Title/H1, preview noindex/nofollow, no preview canonical, checker present, scope-decoder/red-flags/TCO sections present, official references present, sponsored affiliate rel present.
- Browser visual review confirmed the new management-claim decoder renders correctly in native Hugoplate styling.
- SERP Audit.txt now marks Managed vs Unmanaged VPS as BUILT / FROZEN.
- Next work item in the revised plan: exact-query SERP for the FASTPANEL page target.


### 2026-10-13 — FASTPANEL exact SERP target locked
- Ran a dedicated exact-query comparison for FASTPANEL VPS Hosting vs FASTPANEL Hosting vs VPS with FASTPANEL, plus a supporting FASTPANEL VPS check.
- Winner locked: FASTPANEL VPS Hosting.
- Exact page naming: Title = H1 = FASTPANEL VPS Hosting; URL = /fastpanel-vps-hosting/.
- Secondary semantic variant: FASTPANEL Hosting. Natural-language variant: VPS with FASTPANEL. Do not create separate pages for those variants.
- Exact research saved at research/fastpanel-vps-hosting-serp-2026-10-13.md.
- VDSina official Standard page currently lists FASTPANEL on Ubuntu 22 as a Web hosting control panel option.
- FASTPANEL official docs currently state manual-install minimums of 1 GB RAM, 5 GB free disk, 1 CPU core / 1 GHz on a clean supported OS; these are panel minimums, not production website recommendations.
- SERP Audit.txt updated: FASTPANEL VPS Hosting is READY TO BUILD and is now the next work item.


### 2026-10-13 — FASTPANEL VPS Hosting built
- Implemented /fastpanel-vps-hosting/ with exact Title/H1 FASTPANEL VPS Hosting and URL ownership fixed from the exact SERP audit.
- Page covers VDSina FASTPANEL on Ubuntu 22, official FASTPANEL installation minimums vs real production sizing, four practical VPS tiers, a functional FASTPANEL VPS fit checker, first-site workflow, WordPress, multiple-site user isolation, email/database/SSL/backups, security, management boundaries and negative qualification.
- Official facts rechecked on 2026-10-13: VDSina Standard lists FASTPANEL on Ubuntu 22; FASTPANEL manual-install docs list 1 GB RAM / 5 GB free disk / 1 core 1 GHz on a clean supported OS; FASTPANEL docs recommend separate users for separate sites and support WordPress/site creation, backups, mail, SSL, firewall, databases, PHP and scheduled jobs.
- Internal links added: homepage management section -> FASTPANEL VPS Hosting; VPS with Control Panel -> FASTPANEL VPS Hosting; FASTPANEL page -> homepage, control-panel parent, sizing, managed-vs-unmanaged, WordPress, multiple websites and migration.
- Guides menu now includes FASTPANEL VPS Hosting.
- Preview build for source commit 7022e93e301bc823e3a93c95891abec45c0340bd succeeded; artifact 000bf4f1621423152012eaeca225d6bebdd6bd4e was visually checked at the first screen and fit checker.
- Generated checks: exact Title/H1, one H1, preview noindex/nofollow, no preview canonical, WebPage + BreadcrumbList JSON-LD, fit checker present, 2 affiliate links with sponsored/nofollow/noopener, all intended internal links present.
- Added the required contextual return link to the homepage in follow-up commit df21ab789ff24e502612fc54669ac56229837dd8.
- SERP Audit.txt status is now BUILT / NEEDS FINAL DENSE FREEZE AUDIT.
- Next step: dense completion audit of this page before freeze; then deepen VPS with Control Panel.


### 2026-10-13 — FASTPANEL VPS Hosting built and frozen
- Built /fastpanel-vps-hosting/ with exact Title/H1 FASTPANEL VPS Hosting and exact slug /fastpanel-vps-hosting/.
- Page covers panel-minimum vs real workload sizing, VDSina FASTPANEL on Ubuntu 22 deployment, current 1/2/4/8 GB Standard reference tiers, FASTPANEL fit checker, supported OS compatibility, first-site flow, WordPress, multi-site user isolation, email/database/SSL/backups, migration, security/updates, SSH/root responsibility and negative qualification.
- FASTPANEL fit checker deliberately does not recommend the 1 GB panel minimum as the normal production target.
- Official FASTPANEL manual-install requirements and supported OS list were rechecked; VDSina Standard FASTPANEL on Ubuntu 22 and plan values were rechecked.
- Internal linking implemented: homepage and VPS with Control Panel -> FASTPANEL VPS Hosting; FASTPANEL page -> homepage, sizing, Managed vs Unmanaged, control-panel parent, WordPress, Multiple Websites and Migration.
- Guides menu includes FASTPANEL VPS Hosting.
- Final preview build after OS-compatibility closure succeeded. Preview artifact: 2d71b3dd5ed7fafa2fd368de466f4a32ce64f7a7.
- Generated checks: Title=H1, one H1, preview noindex/nofollow, no preview canonical, 2 JSON-LD blocks, functional checker, all 4 verified VDSina price tiers, 2 partner links with matching sponsored/nofollow/noopener attributes, all intended routes present.
- Browser visual review completed for the top of the page and fit checker; both render in native Hugoplate styling.
- SERP Audit.txt now marks FASTPANEL VPS Hosting as BUILT / FROZEN.
- Next work item: deepen VPS with Control Panel so the generic parent and FASTPANEL child are cleanly separated.


### 2026-10-13 — FASTPANEL VPS Hosting frozen
- Completed the final dense audit of /fastpanel-vps-hosting/ against the exact SERP research and page specification.
- Closed all researched G1-G11 items: panel minimum vs production sizing, VDSina Ubuntu 22 path, control-panel-vs-management boundary, multi-site user isolation, panel overhead, first-site workflow, SSH/root boundary, backup/recovery distinction, migration scope, WordPress scope, and negative qualification.
- Added the final missing comparison block: FASTPANEL vs other control panels, keeping generic panel selection owned by /vps-with-control-panel/.
- Added FAQ clarification that FASTPANEL currently presents the panel as free while the installation flow still uses a license step; current terms must be rechecked before future rewrites.
- Final preview build for source commit bdc3effec56833b12f3dbe3149e1c25ff2534931 succeeded. Preview artifact 6fc064d15c52df99bc6ba9cc10e73f0b99b32131 was visually checked.
- Final generated checks: Title=H1=FASTPANEL VPS Hosting, one H1, preview noindex/nofollow, no preview canonical, WebPage + BreadcrumbList JSON-LD, fit checker rendered, two sponsored affiliate CTAs, homepage return link, and intended sibling links.
- Homepage and VPS with Control Panel generated HTML both link to /fastpanel-vps-hosting/.
- SERP Audit.txt now marks FASTPANEL VPS Hosting BUILT / FROZEN.
- Next work item: deepen VPS with Control Panel so generic panel selection and the FASTPANEL child remain cleanly separated.


### 2026-10-13 — VPS with Control Panel frozen
- Re-ran the page-level SERP for VPS with Control Panel / VPS Hosting with Control Panel / VPS Control Panel / best VPS control panel. Kept the existing exact owner: Title = H1 = VPS with Control Panel; URL /vps-with-control-panel/.
- Fresh SERP research saved at research/vps-with-control-panel-serp-2026-10-13.md.
- Rebuilt the page as the generic parent for panel choice, not as a duplicate FASTPANEL page.
- Closed G1-G13: provider-dashboard vs hosting-panel ambiguity; panel-or-no-panel decision; panel classes; OS compatibility; licensing economics; panel resource overhead; mail/DNS; multi-site/client isolation; panel vs management; backup/restore; migration/exit cost; functional panel-fit checker; and current VDSina truth.
- Added representative panel map for FASTPANEL, HestiaCP, cPanel & WHM, Plesk, DirectAdmin and CloudPanel without turning the page into a ranking list.
- Current VDSina official Standard page was rechecked: preconfigured Web hosting control panel block lists FASTPANEL on Ubuntu 22, HestiaCP on Ubuntu 22 and BitrixVM 9.0. The page does not claim cPanel/Plesk/DirectAdmin/CloudPanel are bundled.
- Added contextual link from VPS for Multiple Websites back to VPS with Control Panel; homepage and FASTPANEL page already link to the generic parent.
- Final preview build for source commit 2da198bcd15c55d574f7de3d1ffa65a2221d6c96 succeeded. Preview artifact e0f752a0c4962c9675beaf69bcc67f5108b0ab8a visually checked at the top, fit checker and representative panel map.
- Generated checks: exact Title/H1, one H1, preview noindex/nofollow, no preview canonical, WebPage + BreadcrumbList JSON-LD, functional panel-fit checker, two sponsored partner CTAs, all intended internal links, and inbound links from homepage/FASTPANEL/Multiple Websites.
- SERP Audit.txt now marks VPS with Control Panel BUILT / FROZEN.
- Next planned item: fresh exact-query SERP then build How to host a website on VPS, with the no-control-panel/manual path merged into that page.


### 2026-10-13 — VPS with Control Panel control audit confirmed
- Rechecked the frozen page against the stored G1-G13 SERP gap list and current generated preview. All planned content gaps are closed.
- Verified current generated output: Title=H1=VPS with Control Panel, one H1, preview noindex/nofollow, no preview canonical, two JSON-LD blocks, functional panel-fit checker, representative panel map, current VDSina FASTPANEL/HestiaCP/BitrixVM truth boundary, two sponsored affiliate CTAs, and all planned contextual links.
- Corrected SERP Audit.txt bookkeeping: removed duplicated DONE/FROZEN block and restored the intended next work order beginning with a fresh exact-query SERP for How to host a website on VPS.


### 2026-10-13 — How to host a website on VPS frozen
- Ran a fresh exact-query SERP across How to host a website on VPS / host website on VPS / without control panel / VPS setup variants. Exact owner locked: Title = H1 = How to host a website on VPS; URL /how-to-host-a-website-on-vps/.
- Fresh research saved at research/how-to-host-a-website-on-vps-serp-2026-10-13.md. Current exact/near-exact SERP includes Hostinger, Fasthosts, Hyperswitches, Server Manager, CWP.sg, ScalaHosting, DCHost, Namecheap, RoyaleHosting, Linux Junkies and Virteche.
- Merged the old VPS without Control Panel intent into this page as planned; no separate no-panel URL will be created.
- Implemented a functional Deployment Path Checker for static/manual, PHP/WordPress, Node/Python/reverse-proxy and control-panel paths.
- Closed all planned G1-G15 gaps: manual/panel/managed branch, stack branch before install, no-panel path, secure first SSH access, pre-DNS testing, DNS+hostname dual requirement, HTTPS ordering, static/PHP/app differences, non-root permissions/secrets, repeatable deployment methods, production acceptance, reboot validation, basic resource validation, negative qualification and functional path checker.
- VDSina current pure OS templates were rechecked on the Standard page; page uses Ubuntu/Debian as documentation examples without calling them universally best.
- Internal links added: homepage pure-Linux branch -> this guide; VPS with Control Panel manual/no-panel sections -> this guide; new page -> homepage, sizing, control panel, FASTPANEL, managed-vs-unmanaged, migration, WordPress and Multiple Websites.
- Guides menu includes Host Website on VPS.
- Final preview build for source commit 709a05f1436e1b50915806bec13c19d50ead6e04 succeeded. Preview artifact d59925531c458870dbeb777f0e86ea802340b820 was visually checked at the top, deployment checker and pre-DNS testing area.
- Generated verification: exact Title/H1, one H1, preview noindex/nofollow, no preview canonical, two JSON-LD blocks, two sponsored affiliate CTAs, all intended internal links, deployment checker, pre-DNS test, no-panel negative qualification, reboot test and production acceptance checklist.
- SERP Audit.txt now marks How to host a website on VPS BUILT / FROZEN.
- Next planned item: deep fresh SERP + rewrite of VPS vs Shared Hosting.


### 2026-10-13 — VPS vs Shared Hosting frozen
- Ran a fresh page-level SERP for VPS vs Shared Hosting / shared hosting vs VPS / when to move from shared hosting to VPS. Exact owner retained: Title = H1 = VPS vs Shared Hosting; URL /vps-vs-shared-hosting/.
- Research saved at research/vps-vs-shared-hosting-serp-2026-10-13.md.
- Rebuilt the page around evidence-based stay / optimize / move / move-with-admin-help decisions rather than a generic feature comparison.
- Added a functional Shared Hosting vs VPS decision checker using recurring limits, custom-software/root need, optimization status, admin readiness, business criticality and current shared-host stability.
- Closed G1-G15: three/four-way outcome logic, site-vs-host bottleneck, shared metrics != VPS specs, capability triggers, VPS-not-automatically-faster, administration delta, bundled-service loss, total operating cost, isolation nuance, traffic/concurrency caveat, middle paths, migration readiness, functional decision checker, email/DNS/panel transition, and SEO truth.
- Added explicit security/backups/monitoring ownership section after control audit.
- Internal links cover homepage, sizing, managed-vs-unmanaged, control panel, migration and post-purchase hosting guide.
- Final preview build for source commit 396760461e71d5aef95cc8b5310c898fd0224d01 succeeded. Preview artifact e705f52dd5eb3558bcc515fb542cdbde606a53c9 visually checked at the top and decision checker.
- Generated verification: exact Title/H1, one H1, preview noindex/nofollow, no preview canonical, WebPage + BreadcrumbList JSON-LD, functional checker including business criticality, one sponsored affiliate CTA and all required internal links.
- SERP Audit.txt now marks VPS vs Shared Hosting BUILT / FROZEN.
- Next planned item: deep fresh SERP + rewrite of VPS for WordPress.


### 2026-10-13 — VPS for WordPress frozen
- Ran a fresh page-level SERP for VPS for WordPress / WordPress VPS hosting / WordPress VPS 2026. Exact owner retained: Title = H1 = VPS for WordPress; URL /vps-for-wordpress/.
- Research saved at research/vps-for-wordpress-serp-2026-10-13.md.
- Rebuilt the page around WordPress-specific workload rather than generic VPS sizing: uncached PHP concurrency, PHP-FPM worker memory, database demand, layered caching, Redis/persistent object cache, plugin/background work, WP-Cron, staging/backups, management path and WooCommerce boundary.
- Official WordPress requirements were rechecked: PHP 8.3+, MariaDB 10.11+ or MySQL 8.0+, HTTPS; Apache or Nginx recommended. Page explicitly separates compatibility requirements from production VPS sizing.
- Added a functional WordPress VPS Fit Checker with STAY/OPTIMIZE FIRST, 2 GB, 4 GB, 8 GB/recheck architecture and WooCommerce-route outcomes.
- Current VDSina Standard tiers/prices were rechecked; page does not claim preinstalled WordPress because the current Standard visible template/application groups do not list it.
- Closed all planned G1-G15 gaps: official requirements vs VPS sizing, uncached concurrency, worker RAM budget, cache layers, persistent object cache, DB bottleneck, WP-Cron/system scheduler, plugin/background workload, honest 1/2/4/8 GB mapping, panel/management fork, staging/backup headroom, WooCommerce boundary, functional fit checker, upgrade triggers and negative qualification.
- Internal links cover homepage, sizing, VPS vs Shared, WooCommerce, Control Panel, FASTPANEL, Managed/Unmanaged, Migration, Multiple Websites and manual deployment guide.
- Preview build for source commit edbddcff85e3e48b10f6c94f7b86832f094d285c succeeded. Preview artifact a56a819f0b0f1534bdbcdf6f6a8a60630977a446 visually checked at the top and WordPress VPS Fit Checker.
- Generated verification: exact Title/H1, one H1, preview noindex/nofollow, no preview canonical, WebPage + BreadcrumbList JSON-LD, one sponsored affiliate CTA, official WordPress requirement text, caching/cron sections and all intended internal links.
- SERP Audit.txt now marks VPS for WordPress BUILT / FROZEN.
- Next planned item: deep fresh SERP + rewrite of VPS for WooCommerce.


### 2026-10-13 — VPS for WooCommerce frozen
- Ran a fresh page-level SERP for VPS for WooCommerce / WooCommerce VPS hosting / best VPS for WooCommerce 2026. Exact owner retained: Title = H1 = VPS for WooCommerce; URL /vps-for-woocommerce/.
- Research saved at research/vps-for-woocommerce-serp-2026-10-13.md.
- Current SERP confirms a distinct transactional WooCommerce workload: cart/checkout/account, order/stock writes, payment callbacks, Action Scheduler, integrations and campaign peaks.
- Official WooCommerce facts rechecked: current recommendations include WordPress 6.9+, PHP 8.3+, MySQL 8.0+ or MariaDB 10.6+, HTTPS and 256 MB+ WordPress memory limit; the page explicitly states that 256 MB application memory is not VPS RAM.
- Official WooCommerce caching guidance rechecked: Cart, Checkout and My Account remain dynamic and must be excluded from full-page cache.
- HPOS coverage is accurate: dedicated order tables, enabled by default for new installs since WooCommerce 8.2, with compatibility/testing still required for existing stores/extensions.
- Action Scheduler is treated as a first-class workload and operational signal, including failed/past-due queues.
- Added a functional WooCommerce VPS Fit Checker covering store criticality, measured VPS constraints, external gateway/API bottlenecks, checkout concurrency, catalog/search load, background jobs/integrations, DB activity, panel/mail, sale spikes and operations ownership.
- Checker outputs now include MANAGED/SHARED MAY STILL FIT, DIAGNOSE EXTERNAL/APPLICATION FIRST, LEAN 2 GB, PRACTICAL 4 GB, 8 GB/RECHECK ARCHITECTURE and managed/admin-help path.
- Current VDSina Standard tiers/prices were rechecked; page does not claim a dedicated preinstalled WooCommerce image because the current visible application/template groups do not list one.
- Closed all planned G1-G16 gaps: official requirements vs production sizing, dynamic checkout/account cache boundary, checkout concurrency, 2 GB foundation vs 4 GB practical baseline, DB writes, HPOS, Action Scheduler, Woo-aware cache layers, payment/webhook reliability, sale peaks, transaction-aware backups/RPO, external service bottlenecks, functional fit checker, migration live-write boundary, upgrade triggers and negative qualification.
- Internal links cover homepage, WordPress parent, sizing, Managed/Unmanaged, Control Panel, FASTPANEL, migration and manual deployment.
- Final preview build for source commit 31773d1b52178199df037286a02a306f020359ea succeeded. Preview artifact 4ce66bddb3ef8bf23db6039b464e5ed3e3b4101d visually checked at the top and fit checker.
- Generated verification: exact Title/H1, one H1, preview noindex/nofollow, no preview canonical, WebPage + BreadcrumbList JSON-LD, one sponsored affiliate CTA, official WooCommerce requirement/caching/HPOS/Action Scheduler sections and intended internal links.
- SERP Audit.txt now marks VPS for WooCommerce BUILT / FROZEN.
- Next planned item: deep fresh SERP + rewrite of VPS for Multiple Websites.


### 2026-10-13 — VPS for Multiple Websites frozen
- Ran a fresh page-level SERP for VPS for Multiple Websites / host multiple websites on one VPS / agency multi-site VPS. Exact owner retained: Title = H1 = VPS for Multiple Websites; URL /vps-for-multiple-websites/.
- Research saved at research/vps-for-multiple-websites-serp-2026-10-13.md.
- Current SERP confirms a distinct multi-site architecture intent around domain-count myths, name-based virtual hosting, site/user isolation, combined peaks, backups, blast radius and when to split workloads.
- Rebuilt the page around combined peak load and failure-domain design rather than a fixed "number of websites" claim.
- Added a functional Multi-site VPS Architecture Checker with outcomes ONE VPS / LIGHT PORTFOLIO, ONE VPS + STRONGER ISOLATION, SPLIT THE CRITICAL SITE and SPLIT WORKLOAD / RECHECK ARCHITECTURE.
- Closed all planned G1-G16 gaps: domain count is not capacity; one-IP/SNI hosting; explicit per-site isolation; folder-only isolation warning; combined peaks; mixed workloads; internal noisy-neighbor risk; one-VPS blast radius; backup/restore granularity; manual/panel/container operating models; agency/client ownership; functional architecture checker; measurable split criteria; per-site/server monitoring; separate-IP nuance; honest 2/4/8 GB mapping.
- Added explicit operations-ownership and portfolio-migration links to Managed vs Unmanaged VPS and Website migration to VPS during the final control audit.
- Current VDSina Standard tiers/prices remain mapping examples only; no fixed website-count guarantees are made.
- Final preview build for source commit a977b947f56c6bb98b3a01066e63b84983b8ffae succeeded. Preview artifact a602593b2a223fd495ec35e3e0cd15f897ec3bd9.
- Generated verification: exact Title/H1, one H1, preview noindex/nofollow, no preview canonical, WebPage + BreadcrumbList JSON-LD, functional architecture checker, one sponsored affiliate CTA, same-IP/SNI explanation, isolation/blast-radius/agency/split coverage and all intended contextual links.
- SERP Audit.txt now marks VPS for Multiple Websites BUILT / FROZEN.
- Next planned item: fresh page-level SERP + build of VPS Security Checklist.


### 2026-10-13 — VPS Security Checklist built; visual QA pending
- Ran a fresh exact-query SERP for VPS Security Checklist / VPS hardening 2026 / how to secure a VPS. Exact owner locked: Title = H1 = VPS Security Checklist; URL /vps-security-checklist/.
- Fresh research saved at research/vps-security-checklist-serp-2026-10-13.md. Current results include HostMyCode, Contabo, Server Warden, Defensia, ArgoEye, HostAccent, VPS.app, Kage System, Varnox and VPSDEN.
- Authority sources added: Ubuntu OpenSSH, UFW/firewall and unattended-upgrades docs; CISA StopRansomware guidance for least privilege, offline/encrypted backups, restore testing and incident response.
- Implemented a functional VPS Security Baseline Checker with CRITICAL GAPS, BASELINE INCOMPLETE and PRODUCTION BASELINE READY outcomes; it explicitly does not claim a server is fully secure.
- Closed researched G1-G19 in source: lockout-safe recovery order, service inventory, SSH-key/root/password policy, firewall layers, private DB/Redis/internal services, patch/restart/reboot ownership, least privilege, secrets, Fail2ban/CrowdSec as defense-in-depth, panel/admin UI security, backup/restore, logs/alerts, DDoS scope, TLS boundary, application-layer patching, compromise response, functional checker and recurring review.
- VDSina truth rechecked: Standard advertises free DDoS protection; public QA states the free DDoS service is L3-L4 and has no SLA. Page explicitly says this does not replace application/guest-OS security.
- Added inbound links from How to host a website on VPS and Managed vs Unmanaged VPS; Guides menu now includes VPS Security Checklist.
- Final Hugo preview build for source commit ad76712e6eef1f92d459fd1ddc115e6fb7d88375 succeeded. Generated preview checks: exact Title/H1, one H1, preview noindex/nofollow, no preview canonical, WebPage + BreadcrumbList JSON-LD, functional security checker, one sponsored affiliate CTA, DDoS scope, backup/incident sections and all intended internal links.
- Browser visual QA could not be completed because Opera Browser Connector is currently disconnected, and Desktop Commander remote-use quota is exhausted. Do not mark the page FROZEN until the actual rendered page is visually checked.
- SERP Audit.txt status is BUILT / FINAL VISUAL QA PENDING.
- Next continuation point: visually open /vps-security-checklist/ in preview, confirm top/checker/table rendering, then mark FROZEN; after that build VPS Backup Strategy.


### 2026-10-13 — VPS Security Checklist frozen after visual QA
- Browser Connector connection restored and the rendered VPS Security Checklist preview was visually checked.
- Visual QA passed for the first screen, VPS Security Baseline Checker, and Production security checklist table in native Hugoplate styling. No layout/overflow defect was observed in the checked desktop preview.
- Final preview artifact used for QA: 6f5133ee37d1fe01a3f4096031b766b2ce016714.
- Page status is now BUILT / FROZEN. All G1-G19 remain closed; no new P0/P1 content or visual defect was found.
- SERP Audit.txt updated accordingly.
- Next planned item: fresh page-level SERP + build of VPS Backup Strategy.


### 2026-10-13 — VPS Backup Strategy frozen
- Ran a fresh exact-query SERP for VPS Backup Strategy / 3-2-1 / RPO-RTO / snapshot-vs-backup / restore-testing variants. Exact owner locked: Title = H1 = VPS Backup Strategy; URL /vps-backup-strategy/.
- Fresh research saved at research/vps-backup-strategy-serp-2026-10-13.md. Current 2026 SERP includes HostMyCode, LuckVM, ServerExpress, Advika, StoicVPS, DotMoose, VDS Panel, All-VPS and related recovery-strategy guides.
- Authority basis: NIST SP 800-34 RPO/RTO definitions; NIST SP 1339 regular backup creation/testing/recovery exercises; Ubuntu restic/Borg tooling references.
- Implemented a functional VPS Backup Strategy Checker using workload type, RPO, RTO, independent offsite copy, DB-consistent method, restore test, separated credentials/keys and retention history.
- Checker outputs: CRITICAL BACKUP GAPS, BASIC RECOVERY STRATEGY, TRANSACTIONAL / FREQUENT-DB-BACKUP PATH, and LOW-RTO / RECHECK DR ARCHITECTURE.
- Closed all planned G1-G20 gaps: RPO/RTO-first design, provider image vs file/DB backup vs replication, rebuildable-vs-stateful inventory, DB consistency, RPO-driven frequency, low-RTO architecture, practical 3-2-1, credential separation, encryption/key recovery, retention, restore granularity, restore drills, measured RTO, multi-site restore, transactional RPO, production-disk impact, backup CPU/I/O impact, VDSina portability, functional checker and recovery runbook.
- VDSina official backup facts rechecked: manual and scheduled backup copies; restore; create new server from backup; cloning; downloadable backup image in .img.gz form. VDSina Terms explicitly place backup responsibility on the customer and recommend periodic restore testing.
- Page truth boundary: provider image is treated as one recovery layer, not a complete backup strategy; no guarantee of portability to every hypervisor is claimed.
- Added inbound contextual links from VPS Security Checklist, Managed vs Unmanaged VPS, VPS for WooCommerce and VPS for Multiple Websites; Guides menu includes VPS Backup Strategy.
- Hugo preview build succeeded. Preview artifact f5cab165f695db299994b671a6088bff8a8f5161 was visually checked at the first screen, Backup Strategy Checker, VDSina section and VPS backup checklist table.
- Generated checks: exact Title/H1, one H1, preview noindex/nofollow, no preview canonical, WebPage + BreadcrumbList JSON-LD, functional checker, one sponsored affiliate CTA and intended contextual links.
- SERP Audit.txt now marks VPS Backup Strategy BUILT / FROZEN.
- Next planned item: fresh exact-query SERP and build of VPS Monitoring.


### 2026-10-13 — VPS Monitoring frozen
- Ran a fresh exact-query SERP across VPS Monitoring / VPS Monitoring Guide / VPS Server Monitoring / monitoring-tools variants. Exact owner locked: Title = H1 = VPS Monitoring; URL /vps-monitoring/.
- Fresh research saved at research/vps-monitoring-serp-2026-10-13.md. Current 2026 SERP includes LuckVM, Simple Observability, HostMyCode, thueVPS, VPS.DO, Hostinger, ZEROX HOST, VPSWala, HostAccent and AsiaGB.
- Exact-key decision: VPS Monitoring retained as the clean head-term owner; VPS Monitoring Guide is a secondary informational variant; VPS Server Monitoring is redundant and noisier.
- Built the page around five monitoring layers: external availability, host metrics, service/application health, logs/events, and alerting/ownership.
- Added a functional VPS Monitoring Baseline Checker with outcomes BLIND SPOTS, BASIC MONITORING, ALERTING / OWNERSHIP INCOMPLETE and PRODUCTION MONITORING BASELINE.
- Closed all planned G1-G22: external-vs-internal monitoring; real-time diagnostics vs retained history; CPU/load/steal context; RAM/swap/OOM; disk capacity/inodes/I/O; network; service/app health; HTTP-content checks; TLS/DNS; DB health; cron/queues/jobs; backup freshness; logs+metrics correlation; non-universal thresholds; alert severity/debounce/grouping; independent notification path; alert owner/runbook; capacity trends; monitoring overhead/security; multi-site two-level monitoring; functional checker.
- Technical references include Prometheus Node Exporter and Alertmanager plus the official Uptime Kuma project.
- Added inbound links from VPS Security Checklist, VPS Backup Strategy, VPS sizing for website and VPS for Multiple Websites; Guides menu includes VPS Monitoring.
- Hugo preview build for source head bda0506c4bdfa0f7383712e98f5893503099153d succeeded. Preview artifact 1fd2cb79c84963065a501b49f63ff76917144222.
- Generated verification: exact Title/H1, one H1, preview noindex/nofollow, no preview canonical, WebPage + BreadcrumbList JSON-LD, functional checker, one sponsored affiliate CTA and intended contextual links.
- Visual QA passed for the first screen, Monitoring Baseline Checker and VPS monitoring checklist table in native Hugoplate styling.
- SERP Audit.txt now marks VPS Monitoring BUILT / FROZEN.
- Next planned item: fresh exact-query SERP and build of How to Choose VPS Location.


### 2026-10-13 — VPS Monitoring re-audit correction

- Re-read persistent project context, `SERP Audit.txt`, SEO buffer, architecture audit and `research/vps-monitoring-serp-2026-10-13.md` before editing.
- Corrected an accidental Title/H1 regression: VPS Monitoring must follow the project exact-query rule. Final owner is Title/H1 `VPS Monitoring`, URL `/vps-monitoring/`.
- Re-audited the implementation against monitoring gaps G1-G22; all are closed.
- Added the remaining current SERP nuance: provider-native CPU/RAM/disk/network dashboards are useful as a starting host-level layer but do not replace independent external uptime or application-level monitoring.
- Verified inbound links to VPS Monitoring from Security, Backup, Sizing and Multiple Websites.
- Preview SEO is intentionally noindex/nofollow; production canonical/hreflang are conditionally emitted by the shared head partial.
- Live GitHub Pages deployment is currently blocked outside page content: the build job succeeds, but `actions/deploy-pages@v4` returns 404 because GitHub Pages is not enabled for the repository. Preview build remains the review path until Pages is enabled.


### 2026-10-13 — Preview URL rewrite fix

- Browser QA of VPS Monitoring exposed duplicated `raw.githack.com` in breadcrumb/base-derived preview URLs.
- Root cause: preview workflow performed a blind replacement of `/agurkin2021-gif/vpsforwebsite/preview/` even inside URLs that were already absolute RawGitHack URLs.
- `.github/workflows/pages.yml` now replaces only prefixes not already preceded by `https://raw.githack.com`, preserving already-correct absolute preview URLs.
- This is preview-only infrastructure; production BaseURL remains `https://vpsforwebsite.com/`.

- Preview rewrite regex was rechecked after commit and corrected to the effective pattern `(?<!https://raw\.githack\.com)`; the earlier over-escaped intermediate pattern must not be restored.


### 2026-10-13 — Deterministic preview publishing

- Rapid sequential commits exposed a preview race: older workflow runs could finish later and overwrite the `preview` branch with stale generated HTML.
- `.github/workflows/pages.yml` now uses concurrency group `hugo-preview` with `cancel-in-progress: true`.
- A freshness check fetches `origin/main` and publishes only when `GITHUB_SHA` still equals the current main commit; stale runs skip the preview publish step.
- Keep this guard. It is required for deterministic visual QA when many SEO/content commits are made quickly.


### 2026-10-13 — Core 14 pages complete

- Built and froze the final planned core page: `How to Choose VPS Location` at `/how-to-choose-vps-location/`.
- Fresh SERP confirmed the exact decision-guide query; Title/H1 remain exact with no tail per project rule.
- Page includes the VPS Location Decision Checker and closes the saved G1-G14 gap set.
- Added the page to Guides navigation and contextual inbound links from homepage, VPS sizing and Website migration.
- Browser QA on direct RawGitHack preview passed visually in the stock Hugoplate system.
- The 14-page core architecture recorded in `SERP Audit.txt` is now fully BUILT / FROZEN.
- Next continuation point: perform the cluster-wide overlap, cannibalization and internal-link audit across the homepage + all 14 core pages. Do not start a HOLD candidate until that audit is complete.
- Live GitHub Pages deployment remains an infrastructure blocker unrelated to page content: production build succeeds but deploy-pages returns 404 while GitHub Pages is not enabled for the repository.


### 2026-10-13 — Cluster-wide audit complete

- Completed full cannibalization, overlap and internal-link audit across homepage + all 14 core pages.
- No core merges are required. No confirmed HIGH-risk cannibalization remains after remediation.
- Fixed the only exact FAQ collision found: generic sizing no longer owns `Is 4 GB RAM enough for WordPress?`; that subquery remains with `VPS for WordPress`.
- Fixed stale planned/future-page references, strengthened homepage routing to Security/Backup/Monitoring, fixed one broken Location section anchor, clarified page-specific H2 ownership and made Guides weights deterministic.
- All 14 supporting pages are reachable contextually from the homepage; every supporting page returns to the homepage; no core orphan remains.
- Full audit is stored in `research/cluster-overlap-internal-link-audit-2026-10-13.md`.
- Next continuation point: do not create another core page by default. Any expansion starts with a fresh SERP/volume/ownership check against the frozen cluster. Live GitHub Pages remains separately blocked until Pages is enabled.


### 2026-10-13 — Homepage re-audit and optimization complete

- Re-audited the homepage from the current English Google SERP for `VPS for website`.
- Current SERP intent is commercial investigation + informational validation, not a purely informational guide.
- Main homepage owner remains exact: Title/H1 `VPS for website`, URL `/`.
- Implemented:
  - working VPS Fit / Readiness Checker;
  - second hero commercial CTA;
  - Standard VPS comparison table with current daily/monthly pricing;
  - provider-selection checklist;
  - evidence-first methodology/trust block;
  - direct FAQs for best VPS, monthly price, $5 VPS, downsides, domain/email;
  - mixed website + automation/worker example;
  - local intent-specific SVG illustrations replacing external theme demo images;
  - WebSite + homepage WebPage schema;
  - bottom CTA rewrite away from bonus-first messaging.
- Final generated homepage QA: one H1; exact Title/H1; preview noindex; schema present; all current plan values present; no broken internal routes/anchors; only VDSina affiliate destination is externally clickable; all 3 affiliate links carry sponsored/nofollow/noopener.
- Audit ledger: `research/homepage-vps-for-website-rerun-2026-10-13.md`.
- Next page-by-page re-audit should proceed to `VPS sizing for website`, not restart the homepage.


### 2026-10-13 — Staged homepage visual QA

- Homepage visual QA is now intentionally split into separate section-level passes rather than one full-page check.
- Pass 1 completed: header + hero + two CTAs + hero illustration.
- Checked at fixed 390 px and 1280 px widths.
- Hero structure, spacing, responsive stacking and illustration scale passed.
- Only issue found: secondary CTA border was too weak in dark mode; fixed with explicit dark-mode white border/text.
- Temporary QA wrapper files were removed after the pass.
- Next visual pass: `Do you actually need a VPS?` + VPS Fit / Readiness Checker.


### 2026-10-13 — Homepage final QA complete

- Homepage `VPS for website` has now completed both previously open final gates:
  1. visual QA at exact 1280 px and 390 px, section by section;
  2. production HTML SEO verification from the production Hugo build.
- Responsive visual fixes made during QA:
  - stronger dark-mode secondary hero CTA;
  - sticky-header scroll offsets;
  - full-width Fit Checker below the fit feature row;
  - checker = 2-column desktop / 1-column mobile;
  - full-width pricing module;
  - pricing cards = 4-column desktop / 1-column mobile;
  - compact configuration CTA;
  - stable anchors for plan cards, methodology and final CTA.
- All homepage sections passed both visual widths.
- Production assertion step passes index/follow, canonical, en/x-default hreflang, WebSite/WebPage JSON-LD and exact single H1.
- Generated preview still has only the VDSina affiliate destination as an external user-visible link.
- Temporary QA wrapper/render files were removed.
- Homepage content/SEO/visual/production-output QA can now be considered CLOSED.
- Separate infrastructure blocker remains: GitHub Pages is not enabled, so deploy-pages cannot publish the production artifact even though the production build itself passes.
- Next page-by-page re-audit target remains `VPS sizing for website`.


### 2026-10-13 — Open Source Pledge-inspired dark design system

- Visual reference: `https://opensourcepledge.com/` and its public source repository. Use the reference as a design-system inspiration, not as branding: do not copy their logo, member marks, photos or proprietary font files.
- Site is now DARK ONLY. `theme_switcher = false`, `theme_default = "dark"`, and the `dark` class is forced before first paint. Do not reintroduce a light-theme switcher unless explicitly requested.
- Core palette:
  - background `#080e17`;
  - deepest background `#02060f`;
  - light dark surface `#16212d`;
  - mid dark surface `#0d131b`;
  - primary green `#2dde74`;
  - secondary violet `#9e86ff`;
  - muted border `#37485c`;
  - headings `#ffffff`;
  - body text `#c9d3df`.
- Typography: use open-source equivalents `Fraunces` for display/headings and `Inter` for body/UI. The reference site's proprietary font files are NOT copied or stored.
- Local theme token overrides live in:
  - `data/theme.json`;
  - `assets/css/generated-theme.css`;
  - `assets/css/custom.css`.
- Homepage visual structure:
  - split editorial hero (copy left, VPS visual right);
  - green eyebrow `Fit · Size · Deploy`;
  - green primary CTA + outlined green secondary CTA;
  - subtle organic gradient accents;
  - dark card/panel image treatment;
  - horizontal workflow strip: Fit → Size → Locate → Migrate → Secure → Back up → Monitor;
  - alternating dark section surfaces, green checks/links, OSP-like compact borders/radii.
- Internal pages:
  - left-aligned editorial page header;
  - `VPS guide` eyebrow;
  - large Fraunces H1;
  - dark bordered header panel with restrained gradient accent;
  - green breadcrumbs/links;
  - H2 section separators with green rule;
  - dark tables, code blocks, blockquotes, FAQ/details and CTA styling.
- Homepage SVG palette and favicon were aligned to the same dark/green system while keeping VPSforWebsite-specific illustrations.
- Visual QA passed:
  - homepage at 1280 px and 390 px;
  - representative internal page `VPS sizing for website` at 1280 px and 390 px.
- Responsive result:
  - desktop hero is two-column;
  - mobile hero stacks cleanly;
  - workflow strip scrolls horizontally with scrollbar hidden;
  - navigation collapses to hamburger;
  - internal headers and body copy remain within viewport.
- SEO/content ownership was not changed by the design pass: homepage remains exact `VPS for website`; supporting Title/H1 owners remain frozen.
- User-visible external link invariant remains unchanged: homepage external destination is only the VDSina affiliate URL.
- GitHub Pages deploy remains a separate repository-setting blocker; production build/SEO assertions pass before deploy.

### 2026-10-14 — Production VPS and V favicon

- The active production review URL is now `https://vpsforwebsite.com/`, served by Nginx on the user's VPS through Cloudflare. HTTPS and automatic certificate renewal were verified during deployment. Use this URL for user review; older preview-only hosting notes above are historical.
- The user rejected the server-rack favicon and requested a clean, attractive replacement. The replacement is a bold geometric V with green `#2dde74` and mint `#72e5a2` faces on the existing midnight `#080e17` rounded square.
- The vector source is `static/favicon.svg` (240 bytes), with no fonts, scripts, external assets or filters. Raster rendering was visually reviewed at 16, 32 and 48 px on light and dark browser surfaces.
- Compatibility assets: multi-size ICO (16/32/48), 180 px Apple touch icon, 192/512 px app icons, and a separate 512 px maskable icon with an opaque background and the mark inside the safe area.
- Shared favicon and manifest partials now use `v=20261014-v` so browsers and Cloudflare can fetch the replacement immediately. The local manifest partial also avoids the upstream white theme-color metadata; the existing dark theme-color in the head remains authoritative.
- The change is limited to icon assets and head metadata. Page bodies, layouts, content, titles, H1s, canonical URLs, stylesheets and scripts retain their current behavior.
- Production is updated separately from GitHub Pages: keep these source assets/partials in future Hugo builds so exporting or redeploying the site retains the new icon. Do not add a Hugo build toolchain to the VPS for static icon changes.
- Verification after publication: all 19 production HTML pages reference the versioned icons and manifest; all seven icon/manifest resources return HTTP 200 with matching file hashes; the manifest has `application/manifest+json`. Production page bodies remain byte-for-byte unchanged. SEOimpuls on the shared VPS still returns HTTP 200.
- Source commit `e0fffc754f03a32da907fee9fd5303515659b7ee` passed the complete Hugo preview workflow (run `38619994659`), and the production Hugo compilation also succeeded.
- Existing separate Pages CI defect remains: the `github.io` build intentionally emits preview noindex/no canonical, while `live-pages.yml` expects production index/follow, canonical and hreflang. The same SEO assertion failure existed before this favicon change (baseline run `38603546540`, favicon run `38619994500`). It does not affect the deployed custom-domain site. Do not remove preview noindex as part of an icon change; handle this workflow mismatch as its own deployment task.

### 2026-10-14 — Google Analytics 4

- Installed the user's Google tag with measurement ID `G-J6X9FNRMH5` on the production site, in the head of all 19 HTML pages. Each page has exactly one async gtag.js loader and one matching config call.
- The source of truth is `[services.googleAnalytics].ID` in `hugo.toml`, rendered by the local `layouts/_partials/google_analytics.html` through the existing shared head integration. Google Tag Manager remains unset; do not add a second installation through GTM or custom_script.
- The existing preview detection now also excludes Google Analytics from github.io/raw.githack.com preview builds, keeping preview visits out of the production property.
- Public verification passed for all 19 pages; the Google script URL, sitemap and SEOimpuls on the shared VPS returned HTTP 200. The initialization code queues one js event and one config command for the requested ID. Page bodies and other site assets are unchanged.
- Analytics-dashboard event receipt was not inspected because no Google Analytics account session was available. Published tag installation is verified; no claim of confirmed dashboard data is made.

### 2026-10-14 — Nu HTML Checker fixes

- Fixed the user's W3C validation report for the live homepage and audited all 19 published HTML pages with Nu Html Checker 26.10.12, the same version as validator.w3.org.
- The basic SEO partial now runs before any link/script output, placing the existing page-specific base element in the required position without changing its URL. Removed itemprop from the rel=canonical link while preserving the canonical href.
- Removed the non-standard x-dns-prefetch-control meta http-equiv; retained the valid font preconnect links.
- Named informational groups (homepage workflow, WordPress factors, multiple-site examples) now have role=group. Pricing-card headings use h3 after the section h2; the existing card font-size selector follows h3 to retain its appearance.
- Added a local list template using a neutral div wrapper for the headingless list container, removing the About/Contact section warnings while retaining the existing classes and content.
- Production result: all 19 publicly fetched HTML documents have zero Nu errors, warnings or informational messages. The online W3C checker also reports an empty message list for https://vpsforwebsite.com/.
- Full Hugo source build passes validation for all 22 generated English/Spanish HTML documents, including the currently present localization work. Published scope was the 19 existing production documents and one newly fingerprinted CSS asset. Other source changes on main were preserved.
- Text, link destinations, IDs, canonical/base URLs and script contents were checked for preservation during publication. GA4 G-J6X9FNRMH5, the V favicon, sitemap and SEOimpuls remain operational. The old fingerprinted CSS is retained for already-open/cached pages; the HTML points to the new CSS with its matching SRI hash.


### 2026-10-14 — PageSpeed / loading and accessibility improvements

- Resolved the report's missing Swiper exception, low-contrast text in the shared-hosting diagram, inline links distinguished only by color, and visible-text/aria-label mismatches. Kept the heading fixes from the earlier W3C pass.
- Replaced the two used Font Awesome glyphs with small inline SVG icons and removed the unused icon-font styles, search and cookie libraries. Native header/dropdown/FAQ/checker behavior remains available; remaining theme scripts are deferred and the optional Swiper initializer is guarded.
- Self-hosted subset Inter 400–700 and Fraunces 600–700 WOFF2 fonts (58,040 bytes total), with licenses and Spanish glyph coverage. Fingerprinted font preloads and font-display:optional prevent late font swaps. Slow connections can retain fallback fonts for that visit; no invisible text or late reflow is required.
- Added responsive 450/579 px WebP versions of the same transparent hero artwork, correct intrinsic dimensions, an image preload and high fetch priority. Mobile rendering uses the artwork's existing glow without continuously repainting CSS blur filters. Offscreen homepage sections use content-visibility:auto, with a print override.
- Added scripts/optimize-css.mjs after Hugo in npm build and both existing Pages workflows. Lightning CSS expands native Tailwind nesting; PurgeCSS keeps per-page rules, Tailwind class tokens, nested selectors, attribute selectors and JS states. Output has a new SHA-256 URL and matching SRI; unreferenced build aggregate CSS is removed. The homepage CSS is about 131 KB uncompressed versus 309 KB before, and the separate 30 KB transferred icon CSS / 159 KB font are gone.
- GA4 G-J6X9FNRMH5 is still enabled once per production page. The initialization/configuration queue is created immediately; gtag.js is requested on window load (immediately if already complete), so it does not compete for bandwidth with the first screen. There is no interaction requirement, fixed delay, user-agent detection or Lighthouse exception. Visits that end before the tag loads cannot be sent; the GA dashboard was not inspected.
- Nginx for this domain uses gzip level 6 and one-year cache lifetimes for fingerprinted CSS/JS/fonts/images. SEOimpuls and unrelated server settings remain unchanged. Old fingerprinted production files are retained for cached pages; backups are local.
- Validation: all 19 production HTML pages and all 22 current source-build HTML files pass Nu 26.10.12 without messages. Full-page axe checks include offscreen content; mobile navigation and the homepage fit checker passed. CSS parity was checked across all 19 production pages at 390/1280 px; only insignificant 0.1 px rounding in code spans remained. Page text, titles, H1s, canonical URLs and link destinations were preserved. Latest concurrent language-switcher work was retained in source; unpublished localization content was not pushed to the VPS.
- PageSpeed's public API and web measurement endpoint returned HTTP 429 in this environment, so no fresh Google-hosted PSI score is claimed. Final direct Lighthouse 13.5 reports include the enabled GA4 and Cloudflare beacon, default simulated mobile throttling and the actual desktop preset.
- Final direct Lighthouse results: mobile {"scores": {"performance": 93, "accessibility": 100, "best-practices": 100, "seo": 100}, "metrics": {"first-contentful-paint": "1.7 s", "largest-contentful-paint": "2.3 s", "total-blocking-time": "220 ms", "cumulative-layout-shift": "0", "speed-index": "1.7 s"}, "formFactor": "mobile"}; desktop {"scores": {"performance": 99, "accessibility": 100, "best-practices": 100, "seo": 100}, "metrics": {"first-contentful-paint": "0.5 s", "largest-contentful-paint": "1.0 s", "total-blocking-time": "10 ms", "cumulative-layout-shift": "0", "speed-index": "0.7 s"}, "formFactor": "desktop"}.
- The reported mobile score is the median of three consecutive final runs: [82, 94, 93]. Metrics are from that median run. Individual lab scores remain variable.
- GA network verification: [{"event": ["page_view"], "status": 204, "page": ["https://vpsforwebsite.com/"]}]. This confirms the browser request, not account-side processing.


### 2026-10-14 — Production validation and Pages publishing

- The older live-pages.yml also published to GitHub Pages and incorrectly required production indexing metadata on the intentionally noindex github.io preview. CI exposed that pre-existing conflict after the performance update; the optimized Hugo build itself passed.
- Keep pages.yml as the single GitHub Pages publisher, preserving the concurrent multilingual publishing setup. Convert live-pages.yml to a read-only production build/SEO check using https://vpsforwebsite.com as its base URL, with no Pages deployment or write permissions. This retains the production indexing/canonical/hreflang/H1 checks rather than relaxing them for a preview.
- Executed the same production metadata verifier against the final local Hugo build: every check passed. The VPS release and its content were not changed by this CI repair.


### 2026-10-14 — Stable first paint and owner-supplied hero image

- Follow-up Google PSI report l1jwnrugto showed mobile 82/100/100/100, FCP 1.7 s, LCP 4.4 s, TBT 50 ms, CLS 0. The load event could fire before the first visible frame, allowing the analytics library to enter the critical rendering path. This explains why the earlier on-load optimization still produced variable LCP results.
- GA4 initialization/configuration remains queued immediately. The library now starts after load and first-contentful-paint; an already recorded paint is recognized. Hidden tabs start on load, and a visible tab becoming hidden starts immediately. Unsupported/failed Paint Timing observers fall back to on-load loading. An exactly-once guard prevents duplicate tags. There are no fixed delays, interaction requirements, user-agent checks or Lighthouse exceptions.
- Verified the scheduling branches with a VM harness (load/paint ordering, already painted, hidden/visibility transition, unsupported/failed observer, exactly once). Live browser checks confirm the gtag request starts after the first visible paint, one GA page_view receives HTTP 204, and there are no JavaScript errors.
- The owner supplied vps-hero-transparent-50kb.webp and explicitly prohibited further quality reduction. The active asset is assets/images/home/vps-hero-transparent.webp, preserved byte-for-byte: 579x434 RGBA, 51,196 bytes, SHA-256 af91640a83f2564d6b91777550e9b9d6435eeca232b876473037c58f95346fb1. Both the preload and displayed image use its fingerprinted URL. No smaller lossy derivative is selected. The experimental compressed old image was discarded before deployment. Desktop and mobile placement/geometry are preserved.
- The existing Cloudflare HTML cache overrides the origin's no-cache header and still serves the earlier root page. The owner confirmed its two-hour expiry and manages Cloudflare personally; do not change or purge those settings. The fresh production release was verified via ?release=paint-20261014. The ordinary cached URL will update when its edge cache expires or the owner purges it.
- All 19 newly deployed production pages and 22 source-build HTML documents pass Nu without messages. Visible text, titles, H1s, canonical URLs and link destinations are unchanged. SEOimpuls was not modified.
- A fresh Google-hosted PSI request was attempted once and returned HTTP 429. The following are direct Lighthouse 13.5 measurements of the fresh production release with normal default throttling, GA4 and Cloudflare analytics enabled, not a new Google PSI report.
- Results: {"mobile": [{"url": "https://vpsforwebsite.com/?release=paint-20261014", "scores": {"performance": 93, "accessibility": 100, "best-practices": 100, "seo": 100}, "metrics": {"first-contentful-paint": "1.7 s", "largest-contentful-paint": "2.5 s", "total-blocking-time": "220 ms", "cumulative-layout-shift": "0"}}, {"url": "https://vpsforwebsite.com/?release=paint-20261014", "scores": {"performance": 93, "accessibility": 100, "best-practices": 100, "seo": 100}, "metrics": {"first-contentful-paint": "1.7 s", "largest-contentful-paint": "2.5 s", "total-blocking-time": "210 ms", "cumulative-layout-shift": "0"}}, {"url": "https://vpsforwebsite.com/?release=paint-20261014", "scores": {"performance": 93, "accessibility": 100, "best-practices": 100, "seo": 100}, "metrics": {"first-contentful-paint": "1.7 s", "largest-contentful-paint": "2.5 s", "total-blocking-time": "220 ms", "cumulative-layout-shift": "0"}}], "desktop": {"url": "https://vpsforwebsite.com/?release=paint-20261014", "scores": {"performance": 100, "accessibility": 100, "best-practices": 100, "seo": 100}, "metrics": {"first-contentful-paint": "0.5 s", "largest-contentful-paint": "0.6 s", "total-blocking-time": "0 ms", "cumulative-layout-shift": "0"}}}.

## Recovery audit and language restoration — 2026-10-19

- The original fully developed languages present in the emergency Cloudflare snapshot are `en, bn, pt-BR, fr, hi, id, ru, es, vi`. Korean (`ko`) was newly started and is **not** part of the restore-completeness target; it still has only a localized homepage and VPS-sizing page. Do not bulk-translate, remove or overwrite KO work.
- Emergency recovery source is `recovered-public/**`, independent of Hugo sources. It must remain preserved. Immutable recovery safety branch created: `backup/2026-10-19-cache-before-language-repair` (commit `4eeb0c273a80`).
- The fixed switcher order, reconstructed from the original cached markup, is English, বাংলা, Português (Brasil), Français, हिन्दी, Bahasa Indonesia, Русский, Español, Tiếng Việt, 한국어. The restoration script `scripts/restore-language-navigation.py` ensures generated and cached HTML switchers use the same order, preserving existing translated-page paths and fallback home destinations. `scripts/audit-language-recovery.py` prevents cached-page loss or missing language homes/switcher paths.
- Restored and checked Portuguese (Brazil) monitor: `recovered-public/pt-br/monitoramento-vps/index.html`. The complete page has 23 H2, 23 H3, localized hero, table, FAQ and preserved checker algorithm; the GitHub build succeeded and live URL `https://vpsforwebsite.com/pt-br/monitoramento-vps/` was checked in Opera. Indonesian privacy page: `recovered-public/id/kebijakan-privasi/index.html`. French/Portuguese contact pages are restored. Spanish homepage/menu routes, `/es/acerca-de/`, `/es/contacto/`, and a full 22-section Spanish VPS-backup guide have been restored. English privacy disclosure updated to describe production GA4 usage, not claim analytics disabled.
- Added a repeatable `scripts/audit-localized-pages.py` in the Cloudflare build, auditing all previously complete languages for HTML lang, Title/H1, canonical, hreflang, internal paths, locale homes and unlocalized fallback flags. Noindex contact pages and redirect aliases are intentionally exempt from irrelevant canonical/H1 tests but redirect targets remain checked.
- Verified GitHub Actions `Validate production Hugo build` and `Prepare Cloudflare static site` succeeded at recovery commit `e2ae9da57391`; the localized-content audit went from 59 issues before repair to **12 actual remaining issues from four English-only fallback pages**. Those four pages are: `bn/vps-backup-strategy/`, `bn/vps-vs-shared-hosting/`, `fr/strategie-sauvegarde-vps/`, and `fr/vps-pour-plusieurs-sites/`. Their title may be localized, but the principal body is still English. **Do not declare this recovery complete until each entire page is faithfully translated block by block, including diagrams, tables, checkers/JS text, FAQ, canonical, hreflang and partner links, and passed the same audit.** They were not present in the recoverable cache snapshot; do not invent cached original content.
- Latest completed change after that successful build: a small Portuguese monitoring hero-label correction `565647c8344d`, which may trigger another static build. Verify it before claiming final deployment ready.
- `.github/workflows/prepare-cloudflare-static.yml` now skips publishing stale generated commits if `main` advanced; do not force-push or rebase old generated HTML over fresh edits. It overlays only missing `recovered-public` files and commits `cloudflare-public`; edits belong in real source/recovered source, never the generated output. Preserve the Hugo/Hugoplate design and original referral URLs. Do not modify `vpsubuntu.com`.
- Next required localization work (one complete page per pass): Bengali VPS Backup Strategy, Bengali VPS vs Shared Hosting, French VPS Backup Strategy, French VPS for Multiple Websites. After that: run the localization audit in strict mode, build and check the live pages and language switchers on mobile and desktop; only then report full completion.

### Bengali restoration gate — 2026-10-19, completed

- Both formerly English-only Bengali guides are now complete in `recovered-public/bn/`: `vps-backup-strategy/index.html` (commit `a71f711d0081`), and `vps-vs-shared-hosting/index.html` (commit `6eaa02dc473b`). Original English meanings/sections, tables, all checker IDs/decision branches, FAQ and affiliate link counts preserved. The full Bengali index has 18 HTML pages.
- GitHub `Prepare Cloudflare static site` and `Validate production Hugo build` both succeeded for the second Bengali guide. Localization audit reports `bn {"affiliate_present":16,"noindex":1,"pages":18}` and zero Bengali issues. Remaining site-wide issues are exactly six on the two French fallback pages.
- Cloudflare Worker production deployments `6eaa02dc473b` and the generated static commit `36197a29ed7f` show Ready. Opera verified the public page `https://vpsforwebsite.com/bn/vps-vs-shared-hosting/` using a fresh query parameter: Bengali H1, navigation, translated main content and no remaining English fallback. An earlier browser tab had served stale English; fresh navigation confirmed the new deployment. 
- User instruction: **one language at a time and within each language one full page at a time; finish, deploy, check live, only then go to the next page**. Next language French, next page `fr/strategie-sauvegarde-vps/`, followed by `fr/vps-pour-plusieurs-sites/` only after the backup page passes.


### 2026-10-20 ? Restore the original language picker in Hugo source

- Owner approved restoring the original selector after EN/ES/KO had diverged from the recovered locales during the source-first Cloudflare rebuild. The original recovered design is the reference.
- Replaced the Hugo-only button/dropdown with the recovered native details/summary structure (`language-picker`, `lp-panel`, `lp-list`). Restored its green bordered trigger, 208 px panel, current-language highlighting, scrollable list and narrow-screen positioning.
- Added scoped `assets/css/language-picker.css` and `assets/js/language-picker.js`; the shared head emits the small style block before paint and loads the fingerprinted deferred script with SRI. CSS stays outside Tailwind/PurgeCSS so interactive picker styles survive rebuilding. Escape/focus return, outside click, focus departure, resize and mobile-menu closing preserve the original behavior. Native opening still works without JavaScript.
- Kept all ten language labels/order and the existing translated-page link restoration. `restore-language-navigation.py` already supports the recovered list markup; equivalent EN/ES/KO article routes and other recovered translations remain available. No recovered pages or generated cloudflare-public files were edited as source.
- Validation: Hugo 0.158.0 production build and CSS optimization passed; recovery audit preserved 159 cached HTML pages, 10 language homes and 164 selectors with zero errors; localized-page audit reports zero issues. Browser checks cover EN/ES/KO, RU reference and an English article at 320/390/1280 px, keyboard/outside-click/focus closing, scrolling to the last language, mobile-menu interaction, three translated-article transitions and no-JS opening. Desktop/mobile screenshots inspected.
- Deployment: source prepared for GitHub main -> automatic generated static commit -> Cloudflare; live verification pending at this entry. Publish only the two picker assets, shared head, picker template and this context entry.

- Deployment follow-up: source `c765d362d1c1b95ca23bb99d957dddfd494358d6` passed production validation, but the static publication guard correctly stopped on missing historical Bengali CSS. Recovered pages referenced 17 previously generated fingerprinted stylesheets without retaining them in recovery source. Preserved those exact existing Git blobs under `recovered-public/css/`; subsequent source CSS changes can no longer remove those dependencies. The same Bengali (18/18) and French (18/18) CSS/SRI checks now pass locally; no recovered HTML was rewritten.
- Separate pre-existing recovery debt observed: 17 older CSS URLs referenced by other cached inner pages were already absent from the baseline generated tree. This picker change does not introduce additional missing CSS; broader restoration of those unrelated pages is outside this change. Publication/live verification of the picker fix remains the next step.

- Publication completed and verified: picker source `c765d362d1c1b95ca23bb99d957dddfd494358d6`, retained-CSS source `041c36b43bb379991fc72dfa9d0868a9ee4a34b2`, generated static `722125871e022c34716e98670d53cd7600ed5d0d`. Actions 39417477423 (static) and 39417477457 (production validation) succeeded; the generated commit's Cloudflare Workers Builds check succeeded. All ten ordinary live homepage URLs return 200 with the original picker and ten options. Live browser verification passed EN/ES/KO at 390/1280 px, actual link navigation, Escape/focus behavior, panel bounds and loaded picker script; final English desktop/mobile screenshots inspected. This language-picker task is complete.


### 2026-10-20 - Align the affiliate disclosure on every guide locale

- Owner reported the disclosure row drifting far left beneath the guide hero, with `/fr/choisir-localisation-vps/` as the screenshot example. The row used the generic responsive container (1320 px on a 1920 px viewport), while guide heroes use a centered 1040 px container.
- Added the scoped `vps-affiliate-disclosure` class to the shared Hugo page-header partial and all 125 recovered guide HTML files. Both sources load `static/css/guide-disclosure.v1.css`, which matches the existing 1040 px hero width and its 40/36 px tablet/mobile gutters. Other containers, text, spacing, referral links and language-picker behavior are unchanged. Use a new versioned stylesheet URL for any future changes to this static asset.
- Full guide testing exposed the previously recorded missing-CSS recovery debt on 83 cached guide snapshots (69 actively recovered routes plus 14 English snapshots superseded by Hugo). Repointed only those missing critical CSS references to the existing stylesheet of the corresponding current English guide, with its matching SRI; retained the 14 exact CSS blobs under `recovered-public/css/` so later Hugo builds cannot remove those dependencies. These are original site styles, not a redesign. All guide CSS dependencies now resolve. The three unrelated missing stylesheet variants on non-guide cached pages remain outside this layout fix.
- Validation: Hugo 0.158.0 production build and per-page CSS optimization passed. Recovery audit preserves 159 cached pages, 10 language homes and 164 selectors; localized-page audit has zero issues. Bengali CSS gate: 18/18, French page/CSS gate: 18/18. Browser geometry checks pass 294 cases across 127 guide pages: all guides at 1920/390 px, plus representatives of all 10 locales at 320/768/1100/1280 px. Every disclosure aligns with its hero container, has its stylesheet loaded, and stays within the viewport. French desktop/mobile screenshots inspected. Recovered-page byte comparisons confirm changes are limited to the disclosure class/style link and repaired critical stylesheet references.
- Publication prepared for GitHub main -> generated static commit -> Cloudflare Worker. Live verification pending at this entry. QA files, incidental build/module changes and generated cloudflare-public files are not source edits.

- Publication completed: source `44d9a77c1c25dfc3e02d2e910bb71ba6b93a8d5e`; production validation run `39419787917` and static preparation run `39419787852` both succeeded. Generated static commit `17ed4f51f45ec3bc1783e9c528e1c0c8c35cdd2a` has a successful Cloudflare Workers Builds check. All 143 published source files were verified byte-for-byte against the tested changes. Live browser verification on ordinary URLs passed the same 294 layout checks across 127 guides and all 10 locales; no missing guide CSS or disclosure overflow. Final French desktop/mobile screenshots inspected. The disclosure alignment task is complete.


### 2026-10-20 - Complete availability audit of the nine original locales

- Owner requested a full audit/restoration of existing pages after migration, excluding Korean; follow-up specified auditing unavailable existing pages without needing an example URL. Inventory is 162 real pages (18 per en/bn/pt-BR/fr/hi/id/ru/es/vi), plus the existing `/en/` and `/es/about/` HTML redirect aliases. All 164 public URLs returned HTTP 200; all 162 real pages contain their main content. Every successful HTML path in the original recovery manifest is still present. No missing original article route was found.
- Confirmed 12 currently served service pages had 404 critical CSS: ES privacy; HI About/Contact/Privacy; ID About/Contact; RU About/Contact/Privacy; VI About/Contact/Privacy. Repointed these and the three superseded cached EN/ES snapshots to the matching existing English page stylesheet, preserving all body text, internal/affiliate links, scripts and metadata. Retained the three exact CSS blobs in recovered-public/css. This completes the three missing stylesheet variants left after the previous guide-only repair.
- Browser clicks found a real navigation failure: on 1280x800 screens the last guide links in BN/PT-BR/FR/RU were below the viewport and could not be clicked. Long translated labels exceeded the fixed header's dropdown height; page scrolling could not expose them. Added static/css/guide-navigation.v1.css to cap desktop menus to available viewport height and enable internal scrolling. Colors, widths, labels and order are preserved. Shared head includes it for Hugo, and restore-language-navigation.py adds the same link idempotently to recovered HTML during publication. No generated cloudflare-public source edits.
- The 404 template also linked to nonexistent /es/404.html and /ko/404.html; its language selector now goes to the corresponding homepages. Error pages emit noindex and omit nonexistent canonical/hreflang counterparts. Existing Korean content and routes are unchanged.
- Added scripts/audit-site-integrity.py and three fixture tests. The Cloudflare workflow now blocks missing internal links, relative asset paths, CSS font/image dependencies and invalid SRI across all published HTML, including recovered locales. This closes the gap where earlier locale audits checked HTML paths but missed asset loss. Baseline failed on the 12 missing CSS references and four erroneous 404 links; the corrected build has zero errors across 167 HTML files, 220 local targets and 44 referenced stylesheets.
- Local validation: Hugo 0.158.0 production build, CSS optimization, recovery audit (159 cached pages / 10 homes / 164 selectors), strict localized-page audit and all three integrity fixtures pass. Browser checks passed all nine homes plus the 12 repaired pages, with no missing assets or JS errors; 27 actual menu/translated-article navigation cases passed at 1280x800, 1280x520 and 390x800, including mouse-wheel scrolling to the last guide. Russian menu/About screenshots reviewed. Service-worker-enabled sequential navigation also passed; no SW change was needed.
- Separate content observation: existing Hugo-managed Spanish home/About/Contact/Backup output still contains English UI/diagram strings, whereas the cached Spanish homepage is more fully localized. This availability pass preserves page text; it is not evidence that Spanish translation parity is complete. Do not silently describe all localization content as fully restored.
- Publication prepared on main; generated build and live verification pending at this entry.

- Live publication verified: source `43a1783e5642dad8476a795c5c409e3e7280b622`; Actions `39423522324` (production build) and `39423522281` (static preparation) succeeded; generated static `4b619b761664711ebc55d732e071964df467deea` has a successful Cloudflare Workers Builds check. All 27 published source files match the tested local bytes. A fresh public crawl downloaded 222 URLs (all 167 HTML files and their linked assets), with zero bad responses or integrity/link errors. Live UI checks passed all 21 selected pages and all 27 guide-menu/language-navigation cases; no JavaScript errors or missing resources. Both HTML redirect aliases and an actual 404 response with working language-home navigation were verified. Final live screenshots inspected. The requested availability audit and its fixes are complete.

### 2026-10-20 - Prevent hero cards from covering translated titles

- Owner reported the WordPress diagram covering the H1 on `/es/vps-para-wordpress/`. Confirmed on the ordinary live page: desktop WordPress headings inherit `white-space: nowrap !important`, allowing text to extend outside the copy column and under the diagram. Several homepages have the same forced single-line rule. Long individual words also overflow narrow About, WooCommerce and Portuguese monitoring headers.
- Added `static/css/hero-layout.v1.css`, scoped to hero H1s in `.vps-page-header` and `.vps-home`. Titles now wrap and balance within their own column, with emergency word wrapping only when a word cannot fit. Font families, sizes, colors, column geometry, artwork and every title string remain unchanged. English homepage H1 may now wrap at widths where its former single line exceeded the column.
- Shared Hugo head loads the stylesheet; `restore-language-navigation.py` injects it idempotently for recovered pages alongside the existing guide-navigation stylesheet. Preserve fingerprinted recovered CSS; do not edit generated cloudflare-public or replace historical hashes. Use a new versioned URL for future changes to this static asset.
- Validation: Hugo 0.158.0 production build and CSS optimization pass; recovery audit preserves 159 cached pages, 10 homes and 164 selectors; strict localization audit has zero issues; integrity audit passes 167 HTML files, 221 local targets and 45 stylesheets. Browser testing covers all 164 real pages across all 10 available locales at 320, 390, 768, 900, 901, 1024, 1280 and 1920 CSS pixels: 1,312 cases. Baseline had 58 title-boundary failures on 16 pages (21 cases intersected the neighboring visual); corrected output has zero title overflow or card intersections, with the shared CSS loaded in every case. Desktop/mobile Spanish WordPress and English homepage screenshots reviewed. Existing decorative homepage image extension into its gutter is not a title collision.
- Publication prepared on main; generated build and live verification pending at this entry.

- Publication verified: source 504c9d82740ee463fd1d518feddab6c243b4f69b; Actions 39425879184 (production build) and 39425879138 (static preparation) succeeded. Generated static 78c0e773216651de686379ed6b4e89f26294c7ff has a successful Cloudflare Workers Builds check. All five published source files match the tested local bytes. Live browser checks on ordinary public URLs pass all 1,312 cases across 164 pages with zero title overflow, neighboring-card intersections, missing styles or navigation/load errors. Every live H1 string matches the baseline. Final Spanish WordPress desktop, breakpoint and mobile screenshots reviewed. This layout repair is complete.


### 2026-10-20 — Korean localization: WooCommerce (sixth primary page, pre-deployment)
- Owner-directed sequence after five published Korean pages: one page at a time; English remains the strict model; do not modify other locales or existing affiliate targets.
- Work branch `work/ko-woocommerce-20261020`: created `content/korean/vps-for-woocommerce.md` for query/Title/H1 **우커머스용 VPS**, slug `/ko/우커머스용-vps/`; Korean-only labels in WooCommerce hero block of `layouts/_partials/page-header.html`.
- Parity with English: 37 headings (10 FAQ), 28 table lines / three tables, 131 bullet items, seven numbered steps, 10 select controls / 25 values, 16 Markdown links, all 37 English original heading-anchor IDs preserved, six checker results localized. Unmodified JS decision logic and affiliate destination; English labels remain in Hugo else branches.
- No source modifications to English or Spanish pages. Hugo production build, Actions, Cloudflare and live responsive layout pending at this entry. WordPress page mobile visual test was not completed before beginning WooCommerce.
- Detail and ongoing gate tracking: `research/korean-localization-2026-10-19.md`.

### 2026-10-20 — Korean localization page 8: VPS for Multiple Websites (working branch)
- User-directed sequence: one Korean article per pass, translated English-reference blocks separately. Page 7 VPS vs Shared Hosting is finished and live-browser verified; page 8 is `VPS for Multiple Websites`.
- Working branch: `work/ko-multiple-websites-20261020`, source `content/korean/vps-for-multiple-websites.md`. Korean target/Title/H1: `여러 웹사이트용 VPS`; slug `/ko/여러-웹사이트용-vps/`. This intent is consolidation, cross-site combined peaks, isolation, agency administration, shared failure risk, and split triggers; it is not the generic homepage buying query or ordinary sizing.
- Three page-by-block changes prepared: intro/plan/form/network; per-site isolation and administration; recovery/monitoring/checklists/FAQ. English reference matched at 38 headings (19 H2/19 H3), 4 tables/36 Markdown table rows, 110 bullet items, 4 numbered steps, 7 select inputs/18 option values, 10 FAQ, 18 Markdown links, one body affiliate destination. The full decision JavaScript after replacing only the user-visible outcome strings matches English byte for byte; all original heading anchors were kept explicitly.
- The multi-site shared hero in `layouts/_partials/page-header.html` has 16 narrow `ko`-only conditional translations; English strings are intact in the `else` branch. Affiliate URL/rel, diagram geometry, and surrounding templates are unchanged.
- A separate branch-only `.github/workflows/qa-ko-multiple-websites.yml` compiles Hugo 0.158.0, renders the page at 390/1280px, checks SEO/anchors/tables/sponsor attributes, runs 18 actual browser form combinations, and produces screenshots. Preview QA and release verification MUST pass before marking page 8 complete. Do not edit other languages or generated `cloudflare-public/**` by hand.

### 2026-10-20 — French restored-page audit corrections (working branch)

- Owner requested repairs following a full audit of the 18 French routes. Working branch: `work/fr-audit-remediation-20261020`; publication must be verified after merge, not assumed from branch commits.
- `recovered-public/fr/strategie-sauvegarde-vps/index.html`: restored English-reference checklist rows (25 table rows vs 25 in EN) and the original 179 body list points (179 vs 179 in EN) by expanding the French guidance and splitting previously conflated items. All 22 H2, 22 H3, 8 selects/22 options, original heading anchor IDs, single checker and partner links remain unchanged. Translated the residual English hero labels “Restore drill / Prove RTO in practice.” Existing French paragraph layout remains different from EN; do not falsely claim word-for-word or paragraph-count equality.
- `recovered-public/fr/vps-pour-plusieurs-sites/index.html`: restored the original workload-to-starter-plan comparison in the quick-answer table, a site-specific backup row in the isolation table, and full English-reference multisite launch checklist. French now matches EN in body list points (116/116), table rows (32/32), four tables, 19 H2, 19 H3, form options/IDs and affiliate placements. Translated the 1-vCPU/1-GB/10-GB/1-TB reference tier and 32-TB transfer terms with explicit original check date 2026-10-13; readers are told to recheck current terms. English paragraphs are sometimes compressed in French; semantic review may still be needed.
- `recovered-public/fr/politique-de-confidentialite/index.html`: aligned the French disclosures to the existing English policy, removing an unverified specific Cloudflare Web Analytics claim and overly categorical GA cookie behavior statements, retaining factual Cloudflare hosting/edge-processing context, and updating the review date to 2026-10-19.
- `recovered-public/fr/supervision-vps/index.html`: corrected three French technical headings (cron tasks, historical monitoring vs live diagnostics, independent alert channel), preserving IDs and headings hierarchy.
- Added `scripts/audit-french-parity.py` and its blocking step in `.github/workflows/prepare-cloudflare-static.yml` to compare English and French page H1–H3, list item/table cell counts, heading IDs, checker options, script/form elements and sponsor links before publication. The guard intentionally does not claim equivalence of paragraph counts, prose length or complete human translation review.
- No English, Korean, other recovered-language content, production Worker settings, old URLs, CSS, live Cloudflare assets or partner destinations were changed. French Contact remains noindex intentionally; its sitemap/reciprocity issue is pre-existing and shared with the English noindex contact policy. Do not change slugs without a redirect plan.

### 2026-10-20 — French repair production verification

- Merged PR #18 as source commit `72938326c6f82d05cdd18ebded292ff31667f0bb`. GitHub Action `Validate production Hugo build` run 39509386557 and `Prepare Cloudflare static site` run 39509386352 both completed successfully. The new French parity step and French CSS step passed.
- Generated static commit `0c00b946ee7725010947379bacae0e9fb6cf42f6` contains exactly four `cloudflare-public/fr/**/index.html` replacements. Its `Workers Builds: vpsforwebsite` check completed successfully.
- Opera opened all four refreshed live French URLs with a distinct `?fr-fix=72938326` query: the backup page exposed translated restoration vocabulary and extended checklist; multi-site exposed the 1-To / 32-To reference terms and restored architecture rows; privacy displayed the 19 October review date without the unverified Cloudflare Web Analytics claim; monitoring displayed the three corrected headings. Each page had visible main content and an FR language selector. No responsive geometry/screenshots were tested in this repair run.
- Publication completed; the remaining difference from the English reference is paragraph grouping/prose form, which requires a separate in-depth bilingual proofreading pass. No user-facing URL, canonical or referral target changed.

### 2026-10-20 — French responsive visual regression and repair

- User identified that the previous French audit had been closed without responsive browser QA. A real Chromium/Playwright test was added at `scripts/qa-french-responsive.cjs` with workflow `.github/workflows/qa-french-responsive.yml`.
- Baseline production run 39510766725 checked all 18 French URLs at 320, 360, 390, 430, 768, 1024, 1280, and 1920 px: **144 cases, 16 actual form submissions**. Four failures were limited to the French homepage at widths 320–430: pricing-plan H3 elements extended to x=455; a long CTA reached x=468.7; other headings and CTA edges exceeded viewport at 320 and 360. The homepage's overflow:hidden concealed those clipped boxes despite matching document scrollWidth.
- Added `static/css/fr-home-responsive.v1.css` scoped to `html:lang(fr) .vps-home`, loaded only by `recovered-public/fr/index.html`. Under 768 px it allows grid/flex children to shrink, makes pricing-plan cards one fluid column, keeps heading widths and CTAs within the content column, and allows long text to wrap. No translated text, navigation destination, Title/H1, SEO owner, affiliate URL, other locale or global CSS was changed.
- Branch QA run 39511266323 tested the candidate stylesheet in Chromium without modifying the live site. **144/144 responsive cases and 16/16 form submissions passed**, with no tested horizontal document overflow, critical-content box escape, table-scroll defect, JS exception, missing CSS, broken anchor or switcher-panel overflow.
- The production QA workflow runs its main-branch job only on generated static publication commits and waits for the matching Cloudflare Workers Builds check to report success; the working branch injects CSS for prepublication preview only. It emits downloadable screenshots and a JSON report to the GitHub Actions run.
- Source branch `work/fr-responsive-qa-20261020`: production release, main-branch Chromium rerun and live visual verification remain necessary before marking this finished.

### 2026-10-20 — French responsive repair published and independently verified

- PR #19 merged as source commit `2285cbb205554d456ab5b4ce29b1b84f7debc446`. Production Hugo run 39511787152 and Cloudflare static preparation 39511787157 completed successfully. Generated static commit `6d299c9064b11a87ecaa8800c19047c2f9960f33` touched only the French homepage output and `/css/fr-home-responsive.v1.css`; Cloudflare Workers Builds completed successfully.
- After the Worker reported success, run **39512070347** tested the actual published French site without any candidate CSS injection. All 18 routes at eight viewports (320, 360, 390, 430, 768, 1024, 1280, 1920 px) passed: **144/144 cases, 0 issues**, including geometry, headings, critical CSS, anchors, language-switcher bounds, table scroll wrappers, page JS errors, and **16/16 successful live form submissions**. GitHub Actions uploaded a report and screenshots.
- Retained a French-only mobile CSS patch linked only from `recovered-public/fr/index.html`; no English/KO/other-language source files, slugs, SEO metadata, VDSina URLs, CSS for other locales or live Worker settings were changed.
- Follow-up fixed a workflow scheduling problem: GitHub Actions pushes made with GITHUB_TOKEN do not ordinarily trigger a separate push workflow, so the French live QA now uses `workflow_run` after a successful Cloudflare static preparation; it skips unrelated generated commits and waits for the matching Worker success check before testing. `scripts/qa-french-responsive.cjs` no longer has a test-only CSS injection path. Future regressions are tested against truly deployed styles.
- Adaptive implementation and live browser gates for French are closed. The independent line-by-line French linguistic equivalence audit remains distinct from responsive work.
