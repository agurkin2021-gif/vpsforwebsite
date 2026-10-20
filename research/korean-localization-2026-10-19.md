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

## Queue

Complete each page with its own intent review, full translation (including forms/scripts/hero diagrams), link mapping, rendered SEO, responsive checks and publication verification. Do not mark the whole Korean section complete after the homepage.

1. Homepage `/ko/` — implementation and local checks complete; publication verification recorded in the project context.
2. VPS sizing for website — next.
3. Website migration to VPS.
4. Managed vs Unmanaged VPS.
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
