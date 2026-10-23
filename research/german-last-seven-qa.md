# German localization: final seven guides

Source reference: English at bc66649. These are source-level checks; rendered Hugo/browser/deployment checks belong to the shared integration pass. No publication claim is made here.

## vps-with-control-panel.md

- Full English source read and all prose, metadata, tables, form labels/options and seven JavaScript outcome messages translated.
- Target/Title/H1: `VPS mit Control Panel`; slug: `vps-mit-control-panel`.
- Preserved 36 original heading anchors (from the verified Korean counterpart), 22 table lines, 123 bullets, 12 numbered lines, 7 selects and 16 options.
- `translation_audit.py` reports only the intentional added `slug` frontmatter key; all other checks pass. The script's generic Spanish warning is not a language result.
- Full JavaScript is byte-identical after replacing only the seven `result` message literals. All HTML IDs/classes/values/for/type/role/aria-live attributes match English exactly.
- Affiliate URLs, link targets, images and source numeric specifications unchanged.

## fastpanel-vps-hosting.md

- Complete source translated: body, metadata, all form strings and three JS outcomes.
- Target/Title/H1: `VPS-Hosting mit FASTPANEL`; slug: `vps-hosting-mit-fastpanel`.
- Preserved source counts: {"headings": 31, "table_lines": 6, "bullets": 83, "numbered": 17, "selects": 4, "options": 10}. All heading anchors retained from KO.
- Audit flags the intentional added `slug` key and localized visible price suffix `/Tag`; all other checks pass. Full JavaScript matches byte-for-byte after masking only three result literals; HTML control attributes match exactly.
- Exact USD amounts, specifications, affiliate placements and all internal targets retained.

## how-to-host-a-website-on-vps.md

- Full source translated, including metadata, every checklist/form string and five JS outcomes plus two conditional suffixes.
- Target/Title/H1: `Website auf einem VPS hosten`; slug: `website-auf-einem-vps-hosten`.
- Preserved source counts: {"headings": 48, "table_lines": 21, "bullets": 156, "numbered": 24, "selects": 5, "options": 12, "code_blocks": 6}. All original heading anchors explicit.
- Audit only flags added `slug`; all other checks pass. JS matches byte-for-byte after masking only `result` assignments/appends. All six fenced command/config examples and HTML control attributes are identical to EN.
- Every affiliate URL, internal target, IP/port and numeric value retained.

## vps-security-checklist.md

- Complete source translated, including all controls and three result branches (four string fragments around the unchanged dynamic missing-item count).
- Target/Title/H1: `VPS-Sicherheitscheckliste`; slug: `vps-sicherheitscheckliste`.
- Preserved counts: {"headings": 34, "table_lines": 19, "bullets": 128, "numbered": 30, "selects": 9, "options": 18, "code_blocks": 2}. All original anchors explicit.
- Audit only flags added `slug`. Full JS matches after masking only visible result literals; dynamic expression and logic unchanged. Both command blocks and HTML control attributes match EN exactly.

### Price-unit localization clarification

Per integration instruction, visible FASTPANEL prices now use `/Tag` instead of `/day`, while every exact USD amount is preserved. The stock translation audit flags this literal price-unit difference; the shared German audit accepts the documented semantic equivalent. No numeric or currency conversion.

## vps-backup-strategy.md

- Complete body, metadata, tables, controls and all four JS outcomes translated.
- Target/Title/H1: `VPS-Backup-Strategie`; slug: `vps-backup-strategie`.
- Preserved counts: {"headings": 44, "table_lines": 27, "bullets": 163, "numbered": 14, "selects": 8, "options": 22}. Original anchors retained explicitly.
- Audit only flags added `slug`; remaining checks pass. Full JS byte parity after masking four result literals. IDs/classes/options/attributes, numeric examples and affiliate links unchanged.

## vps-monitoring.md

- Full source translated, including metadata, all form text and four JS outcomes.
- Target/Title/H1: `VPS-Monitoring`; slug: `vps-monitoring`.
- Preserved counts: {"headings": 46, "table_lines": 29, "bullets": 188, "numbered": 0, "selects": 9, "options": 21, "code_blocks": 1}. All original anchors explicit.
- Audit only flags added `slug`. Full JS matches after masking four result literals; all control attributes and the complete diagnostic command block match English exactly.

## how-to-choose-vps-location.md

- All 700 source lines translated without omitting sections, including metadata, tables, controls and six JS outcomes; German has 701 lines because of the added slug.
- Target/Title/H1: `VPS-Standort auswählen`; slug: `vps-standort-auswaehlen`.
- Preserved counts: {"headings": 48, "table_lines": 34, "bullets": 140, "numbered": 11, "selects": 6, "options": 16, "code_blocks": 6}.
- All heading anchors compared directly to the rendered English `qa-output/baseline/how-to-choose-vps-location/index.html`; every ID and its order match.
- Audit only flags added `slug`. Full JS matches after masking only the six result literals; all control attributes and all six command blocks match EN exactly.

## Final source verification, all seven guides

- Ran the actual `python -B scripts/translation_audit.py SOURCE TRANSLATION --json` CLI for each page. Each exits 1 solely for reviewed localization differences: the added `slug` key on all seven, and `/day` → `/Tag` price suffix on FASTPANEL. There are no other reported structural differences.
- Re-ran the audit in memory after removing only the added slug and mapping localized price suffixes back to source spellings: seven of seven PASS. Source files were not altered for this check.
- Independently parsed headings from each page's rendered English baseline HTML with `HTMLParser`. All 287 original heading IDs are preserved in the German source, in the same order. No reliance on Korean IDs alone remains.
- Compared the complete JavaScript of each page after masking only visible `result` assignment/appended message literals: seven of seven byte-identical. Form IDs, classes, option values, `for`, `type`, `role` and `aria-live` attributes also match exactly and in order.
- Every fenced command/configuration block matches English byte-for-byte. Full ordered numeric-token sequences match after removing added explicit heading IDs; amounts, dates, resource numbers, addresses, ports and numeric JS behavior remain unchanged.
- `git diff --stat -- content/english` is empty. No English content or shared source changed by this translation assignment.
- Rendered responsiveness, exhaustive browser form outcomes, canonical/hreflang and publication are covered by the separate shared integration review; this note does not claim publication.
