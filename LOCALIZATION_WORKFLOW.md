# Localization workflow — persistent agent instructions

## Scope
- Repository: agurkin2021-gif/vpsforwebsite.
- Hugo source: content/english/; Spanish: content/spanish/.
- **ONE page per complete pass**. Current priority: Spanish homepage content/spanish/_index.md. Do not move to another page until the homepage is rendered and reviewed.
- English stays unchanged. Never deploy to the production domain, VPS, DNS or Cloudflare.
- Preview is built by .github/workflows/pages.yml. Use GitHub Pages /es/ when available and the separate preview branch only as a fallback. Do not claim a page is published without checking the built HTML and URL.

## Translation quality
- Native, technical Spanish (es-ES) with idiomatic hosting and sysadmin vocabulary. Preserve all meaning, sections, paragraphs, lists, tables, FAQ, CTA, JSON-LD-visible text, UI labels and accessible labels. No paraphrase that omits facts.
- Never alter CPU/RAM/disk values, USD prices, providers, images, JavaScript control flow, identifiers, CSS classes or business claims.
- Preserve each affiliate URL **byte for byte**, including partner=ni8gzrvz75, its frequency, button/link placement and rel=sponsored/nofollow attributes.
- Localize page title, meta description, headings, visible strings and navigation. Existing links to pages not yet translated should continue to resolve to an existing English page. Do not generate broken /es/ paths.
- Preserve existing noindex settings until explicitly asked to change them.

## One-pass procedure
1. Read the English source, existing Spanish target, header and language config from main.
2. Make a translation plan by sections. Translate into a complete draft locally, not as multiple partial GitHub commits.
3. Run `python3 scripts/translation_audit.py <english> <spanish> --json`. Fix genuine mismatches. Where localized internal URLs intentionally differ, review and document the exception instead of blindly disabling checks.
4. Run Hugo build with the same version and baseURL as .github/workflows/pages.yml. Check errors, source vs rendered sections, and language menu EN/ES.
5. Check 390px and 1280px layouts, language switcher navigation, all CTAs and referral destinations. Confirm robots, canonical and hreflang.
6. Commit the **finished page** and only necessary supporting localization changes to main.
7. Verify the preview workflow and published HTML. Report one clickable, verified rendered page URL and commit SHA, not only the Markdown source link.

## Efficiency
- Fetch source once and keep it in working memory or a temporary file.
- Translate section-by-section into a single local buffer; validate before committing.
- Avoid giant inline scripts that mix long translations with connector calls. Use short, testable stages.
- Never invent passing test results. If a build or browser cannot be run, report that limitation and do not claim full completion.
- Preserve this file and scripts/translation_audit.py for future sessions.
