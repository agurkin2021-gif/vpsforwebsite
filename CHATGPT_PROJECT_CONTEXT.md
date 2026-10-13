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
