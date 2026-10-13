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
