# Korean localization — page-by-page ledger

## Scope and approach

The owner requested Korean (`ko`) with natural commercial search language, careful technical translation, and individual page passes. Start with the homepage and complete its source, UI, build, responsive review and publication checks before translating another page. Do not create abbreviated translations of the entire cluster.

The current deployment contract in AGENTS.md supersedes the old Spanish-only preview/VPS deployment instructions: edit source on GitHub main; let the existing Action generate cloudflare-public; do not edit Cloudflare manually. English and Spanish source content remains unchanged.

## Page 1: homepage `/ko/`

- Exact Korean Title and H1: **웹사이트용 VPS 호스팅**.
- Primary intent: selecting a VPS to host a website. Supporting natural terms: `VPS 호스팅`, `웹사이트용 VPS`, `VPS 사양`, `VPS 요금`, `가상 서버`, `자체 관리형 VPS`.
- This is Korean-language content, not a claim of Korean/Seoul server availability. Do not target `한국 VPS` or promise Korean support, KRW billing, local payment methods or domestic server locations without provider evidence.
- Preserve the distinction between infrastructure technical support and paid server administration. Use `관리형` versus `자체 관리형`, with responsibility explained in context.
- Keep WordPress, WooCommerce, FASTPANEL and protocol names identifiable; use 워드프레스/우커머스 naturally in prose and navigation.
- Preserve all seven feature sections, 13 FAQs, the four plan configurations, all 16 rendered affiliate placements, the diagnostic inputs and decision logic, and the final CTA/disclosure.
- The 228 originally hardcoded homepage/CTA/switcher strings now have English fallback and reviewed Korean i18n values. This includes diagrams, form labels, accessible labels and all five diagnostic outcomes.
- Keep the owner's original WebP byte-for-byte. Its baked-in English image labels are an intentional retained asset; do not regenerate/recompress it. All HTML diagrams are localized.
- Links to pages awaiting their individual pass resolve to real English pages. Navigation and guide buttons identify these destinations as 영문. No placeholder Korean articles or broken Korean routes are generated.
- The homepage retains the language-root exception to the exact-keyword URL rule: `/ko/`, with no duplicate keyword-slug homepage.

## Terminology and factual evidence checked 2026-10-19

- [Hostinger Korean VPS page](https://www.hostinger.com/kr/vps-hosting): evidence for commercial usage of VPS 호스팅 and 자체 관리형. Used for terminology, not copied marketing prose or its pricing.
- [Google Cloud Korean VPS explanation](https://cloud.google.com/learn/what-is-a-virtual-private-server?hl=ko): evidence for 가상 사설 서버 and hosting terminology.
- [AWS Korean VPS explanation](https://aws.amazon.com/ko/what-is/vps/): additional terminology cross-check.
- [VDSina Standard](https://www.vdsina.com/pricing/standard): rechecked all four displayed tiers, daily/monthly USD prices, monthly transfer, 10 Gbit/s public port, daily billing and support. Prices unchanged; Korean check date is 2026-10-19. Do not convert USD to KRW or invent tax-inclusive/local billing promises.
- No keyword-volume dataset was available. These are intent/terminology decisions, not claims of measured Korean search volume or ranking.

## Verification of the first completed draft

- Hugo **0.158.0 extended**, matching CI, plus the repository CSS optimization step: production and project-path preview builds pass.
- Production: one exact Title/H1, one self-canonical, index/follow, one en/es/ko/x-default alternate each, Korean WebSite/WebPage JSON-LD and unchanged affiliate destinations/rel attributes.
- Removed upstream duplicate hreflang output; the shared head now emits it once, with the corresponding English page as x-default. Preview remains noindex, with no canonical/hreflang or GA script.
- All homepage internal links and anchors resolve in the source build; Korean navigation falls back to English until a real translation exists. Markdown links respect the GitHub project-path preview.
- The original translation audit detects only two reviewed normalization categories: `/day` and `/month` became Korean units, and its ASCII-style word-boundary assumption misses units immediately followed by Korean particles (e.g. `GB의`). Numeric price/spec values, plan rows, section/list counts, images and affiliate URLs were separately compared and preserved. Do not alter correct Korean to satisfy that regex.
- All **216** combinations of the fit checker compared against the pre-change English JavaScript: **5** localized outcomes, identical decisions, no browser JavaScript errors.
- At **390 px and 1280 px**, inspected hero, all seven feature/diagram sections, pricing, methodology, FAQ and final CTA. No page-width overflow. Korean word wrapping and Hangul system-font fallbacks are scoped to ko. Shorter pricing labels and nonbreaking monthly prices prevent narrow-column fragmentation. FAQ line-height/width explicitly accommodates Hangul.
- Language switching EN → KO → EN and mobile navigation tested. English/Spanish homepage visible word sequences are unchanged, excluding the new KO language option.


## Page 2: VPS sizing — `웹사이트용 VPS 사양`

- Query/Title/H1: `웹사이트용 VPS 사양`; slug `/ko/웹사이트용-vps-사양/`. This owns resource selection and sizing, separately from the homepage hosting-purchase intent. No search-volume claim.
- Full translation preserves all 29 headings (explicit original anchors), four tables, seven FAQs, two interactive tools, worked RAM/CPU/storage/transfer examples, caveats and nine rendered sponsored partner links.
- RAM terminology: 여유 용량, 동시 실행 워커, 데이터베이스 작업 집합. The UI explains that RAM alone does not determine CPU/I/O suitability; no visitor-capacity guarantee.
- All 729 diagnostic combinations match the English decision logic. Nine RAM boundaries and the 450+500+6×120+300 MB / 25% example pass (2.4 GB estimate, 4 GB starting tier).
- Clarified the transfer formula's first term as cacheable requested bytes so dynamic responses are not counted twice. Preserved the original example values. VDSina prices remain USD and were checked with the homepage on 2026-10-19.
- Four table row counts, form IDs/values/constraints, section anchors, affiliate URLs/rel attributes and English rendered text match the source. Rendered Korean has no untranslated prose; retained Latin tokens are technical names/specs.
- The first supporting-page pass exposed a shared English disclosure and `/ko/about/` fallback; localized the disclosure and resolved it to the actual English About page until a Korean About page exists.
- Hugo identifies translations through matching content paths. Do not add an explicit translationKey on only one side: this separates it from the English page's implicit key. Korean slug differs; source filename stays the same.
- Production: exact Title/H1, self canonical, en/ko/x-default pointing to corresponding articles, Korean WebPage/BreadcrumbList, valid internal links/anchors. Homepage/menu links automatically resolve to the completed Korean article.
- Production and project-path preview builds pass with Hugo 0.158.0. At 390/1280 px: no page overflow, readable hero/diagrams/forms/FAQ, equivalent-page language switching. The five-column plan table has an accessible horizontally scrollable region and a mobile instruction; its purchase links remain readable. Scope is Korean only.
- Homepage publication verified: source `37b43069c4156856731cce5fc759ab83ca932c1a`; generated `efc4b33376a3e6a0da20f5f57c2087631f3ebd71`; both GitHub Actions and Cloudflare Workers Builds succeeded; live `/ko/` HTTP 200 with correct Title/H1/canonical/hreflang and deployment sitemap entry.
- Sizing source/QA complete; its own source commit, generated output and live publication must be recorded after deployment.

## Page 3: Website migration to VPS — 2026-10-20

- Korean query, Title and H1: **웹사이트 VPS 이전**; slug: \`/ko/웹사이트-vps-이전/\`. This article owns the cutover/migration intent, not VPS purchase selection or WordPress-specific resource sizing. Korean query volume not verified.
- Full English article translated individually: all **31 original headings** retained as anchored sections, both Markdown tables (**22 table lines**), **25 numbered steps**, **106 bullet points** and all **8 FAQ items** preserved in the same order.
- Ten-field interactive preflight form preserves field IDs, option values, readiness conditions, CSS classes and submit behavior; labels, both outcomes and all missing-item names are Korean. **All 2,304 distinct field-value combinations** were simulated against the unchanged English decision logic; zero category mismatches.
- All eight internal link targets and two article affiliate URLs with their \`rel="sponsored nofollow noopener"\` attributes preserved. Hugo rejects relref for untranslated Korean targets, so the guide now uses the existing Korean-aware Markdown link renderer: completed targets resolve to Korean, others to working English pages.
- Dedicated migration hero translated for Korean via narrowly scoped Hugo language conditionals. Original English visible labels, markup and links remain untouched. Korean nav will resolve to this guide once generated.
- Production validation workflow `39439557832` and Cloudflare static preparation workflow `39439558022` passed after the fallback-link fix in source `24ee5c9775c9dbe6107e474e9ecddc9bb0877f04`. Static commit `69b1bbc2eaec9e77d457fda5bdd5f250d285e5ab` passed Cloudflare Workers Builds. Rendered Korean URL has one matching Title/H1, self-canonical, index/follow, valid hreflang and sitemap inclusion; four affiliate placements with correct sponsored attributes. The ordinary live page was opened in Opera, displaying the localized hero, body and checker instead of 404. Resized mobile and desktop layout geometry was not separately tested in this session.
- Next individual page after publication validation: **Managed vs Unmanaged VPS**.

## Page 4: Managed vs Unmanaged VPS — 2026-10-20

- Korean query, exact Title and H1: **관리형 VPS와 비관리형 VPS**; slug `/ko/관리형-vps와-비관리형-vps/`. Scope: management and operational task ownership; Korean search volume has not been verified.
- Full article translated page by page in the work branch. Parity audit: **36 headings (17 H2, 19 H3), 40 table lines, 118 unordered bullets, 16 numbered items, nine FAQ, one form with eight selects, 18 option values, one body VDSina affiliate link**; all match English. Original HTML IDs, values and DOM elements preserved, 36 stable section anchors added.
- Interactive Management Fit Checker preserves the exact English conditional decision tree and returns four complete Korean messages. Removing only the result strings makes its JavaScript identical to English. Relevant internal links point to completed Korean pages, or existing English pages for untranslated guides.
- Shared managed hero's 14 labels, calls to action, accessible label and diagram captions translated in Korean-only Hugo branches. Existing English strings and other hero layouts unchanged.
- Hugo production validation `39443264213` and Cloudflare static preparation `39443264612` passed. Source `06478c9d49740bd1b36fdce2f0eb647210e144bd`; generated static `674030133f94b8800ddc5073194c3c75b0c62a8c`; Cloudflare Workers Builds: success. Live ordinary URL `/ko/관리형-vps와-비관리형-vps/` opened in Opera with Korean title, hero and interactive checker. Generated HTML: one exact H1/Title, four tables, eight select fields, 18 values, four localized result messages, self-canonical, index/follow, complete hreflang, working Korean/English internal fallbacks and three sponsored affiliate placements. Browser screenshot/mobile geometry and actual submit UI testing remain unverified because browser screenshot access disconnected and Desktop Commander monthly quota was reached.

## Page 5: VPS for WordPress — 2026-10-20

- Korean commercial query, exact Title/H1: **워드프레스용 VPS**; slug `/ko/워드프레스용-vps/`. Covers WordPress-specific server selection, PHP workers, caches and plugin/database capacity, distinct from the homepage's broad VPS-for-website purchase intent. Natural Korean usage cross-checked with FDC Servers Korean WordPress VPS material and Cafe24's WordPress VPS category; no measured keyword-volume claim.
- Source: `content/korean/vps-for-wordpress.md`. Full English-content structural parity checked on working branch `work/ko-wordpress-20261020`: 21 H2 + 13 H3 = **34 anchored headings**, **four tables / 32 table lines**, **113 unordered bullets**, **10 FAQ**, **seven form selects / 20 original option values**, 18 Markdown links, one original article affiliate destination. All counts match English. The four VDSina sample tier specifications and eight occurrences of USD/day prices retain their numeric values; Korean unit display is localized.
- WordPress VPS Fit Checker keeps original seven control IDs, 20 option values, score thresholds and conditional branches. Comparison of English/Korean JavaScript after removing localized result strings is byte-identical; five result texts plus conditional addendum are in Korean. No visitor-capacity claims were introduced.
- All guide destinations are preserved with working English fallbacks for untranslated articles and Korean equivalents for completed guides through the Korean link renderer. All 34 English section-anchor IDs retained, including the special requirements/PHP wrappers used by the existing hero script.
- The shared WordPress hero/diagram's 18 user-facing string placements localized with `ko`-only Hugo conditionals, retaining English and Spanish source text without changes. Affiliate URL and `rel="sponsored nofollow noopener"` preserved.
- Source and static audit complete on the working branch; main-branch Hugo CI, Cloudflare publication, live URL and responsive geometry remain to be checked, and must not be marked verified before actual successful results.

## Queue

Complete each page with its own intent review, full translation (including forms/scripts/hero diagrams), link mapping, rendered SEO, responsive checks and publication verification. Do not mark the whole Korean section complete after the homepage.

1. Homepage `/ko/` — implementation and local checks complete; publication verification recorded in the project context.
2. VPS sizing for website — implementation and local QA complete; publication gate pending.
3. Website migration to VPS — source/build/Cloudflare/live publication verified 2026-10-20.
4. Managed vs Unmanaged VPS — full translation and source/build/Cloudflare/live page verified; mobile visual QA pending.
5. VPS for WordPress.
6. VPS for WooCommerce.
7. VPS vs Shared Hosting.
8. VPS for Multiple Websites.
9. VPS with Control Panel.
10. FASTPANEL VPS Hosting.
11. How to host a website on VPS.
12. VPS Security Checklist.
13. VPS Backup Strategy.
14. VPS Monitoring.
15. How to Choose VPS Location.
16. About, Contact and Privacy: separate final supporting-page passes; preserve factual disclosure and current collection behavior.

The supporting-page Korean queries/slugs must be locked when their individual pass starts, not generated as a bulk transliteration list.
