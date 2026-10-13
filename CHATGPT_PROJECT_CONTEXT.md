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
