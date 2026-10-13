# CHATGPT PROJECT CONTEXT — vpsforwebsite.com

> READ THIS FILE FIRST IN EVERY NEW CHATGPT SESSION BEFORE CHANGING THE REPOSITORY.
> This file is the persistent project context and decision log for the site.

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
