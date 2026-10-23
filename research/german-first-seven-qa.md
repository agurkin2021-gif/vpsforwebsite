# German guide localization: assigned first group

Completed: **6/6 assigned guides**. The original assignment contained seven; root took `vps-for-multiple-websites.md` before work on that file began and owns its separate translation/QA. This report intentionally retains the agreed filename.

English reference: clean `vpsforwebsite-german` checkout at `bc66649`. Each English guide was read completely before its translation. `AGENTS.md`, the complete historical SEO buffer and current context/update instructions were reviewed before editing. Existing English files were not modified (`git diff --stat -- content/english` returned no changes during this check).

## Completed pages

| Source filename retained for Hugo translations | German title/H1 | German slug | H2/H3 anchors | Table rows | Bullet / numbered items |
|---|---|---|---:|---:|---:|
| `vps-sizing-for-website.md` | VPS für Websites dimensionieren | `vps-fuer-websites-dimensionieren` | 29 | 25 | 52 / 16 |
| `website-migration-to-vps.md` | Website auf einen VPS umziehen | `website-auf-einen-vps-umziehen` | 31 | 22 | 106 / 25 |
| `managed-vs-unmanaged-vps.md` | Managed VPS vs. Unmanaged VPS | `managed-vps-vs-unmanaged-vps` | 36 | 40 | 118 / 16 |
| `vps-for-wordpress.md` | VPS für WordPress | `vps-fuer-wordpress` | 34 | 32 | 113 / 0 |
| `vps-for-woocommerce.md` | VPS für WooCommerce | `vps-fuer-woocommerce` | 37 | 28 | 131 / 7 |
| `vps-vs-shared-hosting.md` | VPS vs. Shared Hosting | `vps-vs-shared-hosting` | 30 | 13 | 133 / 6 |

All paragraphs, sections, tables, lists, FAQ answers, disclosure text, descriptions, navigation labels, form labels, option captions, initial messages and JavaScript result messages are translated. No guide was shortened into a summary. The guides consistently address readers as **Sie**. Established technical/product terms such as WordPress, WooCommerce, VPS, PHP-FPM, OPcache, HPOS, Action Scheduler and Control Panel remain identifiable.

## Structural and anchor checks

Ran the existing `scripts/translation_audit.py` separately for all six source/translation pairs. All reports require review rather than a literal exit-code PASS because of the intended localization differences below. **There are no unresolved structural errors or JavaScript-logic warnings.** The script's generic warning still mentions Spanish; it is inherited checker wording, not an indication that German was omitted.

Verified separately:

- All **197 H2/H3 IDs**, including their order, match the actual rendered English pages in `qa-output/baseline/<english-route>/index.html` exactly. Explicit `{#...}` IDs preserve original anchors. Two inherited Korean reference discrepancies in Managed were corrected to the actual English IDs: `custom-application--unusual-stack` and `is-247-support-the-same-as-managed-vps`.
- All **653 bullet items and 70 numbered items** remain, with matching per-page counts.
- Every input/select/option opening tag is byte-identical to English: IDs, values, defaults, limits, classes and other attributes are unchanged. This covers **47 selects, 118 options and 6 numeric inputs** across seven forms.
- Heading levels, all table row counts, HTML IDs, image paths, internal link counts/targets, external/affiliate URLs and affiliate occurrence counts match.
- Numeric resource specifications and their occurrence counts match the existing audit. Dollar amounts and daily billing intervals are preserved.
- All seven script blocks retain their executable structure. A separate comparison of string literals confirmed that only displayed text changed; element identifiers, option values, event names and decision constants remain unchanged.

## Reviewed intentional audit differences

1. **Added `slug` frontmatter** on all six pages. These are the accepted German SEO routes. Filenames remain the English translation keys.
2. **`/day` → `/Tag`** on sizing, WordPress and WooCommerce. The audit's price expression recognizes only English period words, so it reports a price difference even though amounts, occurrences, currency and daily interval are unchanged. Sizing and WordPress each retain two occurrences of `$0.07`, `$0.50`, `$0.67`, `$1.34`; WooCommerce retains one `$0.07` and two of each other amount. No conversion to EUR or invented regional offer was introduced.
3. **Sizing comparison table accessibility:** the existing `table-scroll` shortcode wraps the wide five-column tier table, with a German accessible label and one German `<p class="vps-table-scroll-hint">` hint. The extra opening/closing `p` explains the HTML-tag count difference. Cells, links and headings are unchanged. This follows the existing Korean implementation and the responsive issue confirmed by root/GUI review.
4. **Unambiguous thousands formatting:** `1,970 MB` becomes `1970 MB` in the sizing example and `86,400 seconds` becomes `86400 Sekunden` in migration. Values are unchanged; removing the English thousands comma avoids implying German decimal numbers. Technical decimal examples and dollar notation otherwise retain source values.

Provider price/source dates, support-versus-management distinction, panel-versus-management distinction, no guaranteed visitor capacities, WooCommerce cache exclusions, HPOS compatibility warnings, WordPress/WooCommerce software versions, RPO/restore cautions and migration final-write/rollback requirements are preserved from English. No new German datacenter, billing, support or certification claims were added.

## Executed form equivalence check

Ran the actual English and German JavaScript blocks under Node.js `v24.15.0` with a strict DOM stub. Missing referenced IDs throw. Each submit handler executed with the same input values. Actual German output was mapped back through the reviewed paired display-string dictionary and compared to actual English output, including computed values and concatenated diagnostics. Decision logic was not replaced or mocked.

| Page / form | Cases compared | Result |
|---|---:|---|
| Sizing RAM estimator | 50 numeric/default/boundary samples | PASS |
| Sizing shared-host diagnostic | 729, every select combination | PASS |
| Migration preflight | 2304, every select combination | PASS |
| Managed/unmanaged fit | 576, every select combination | PASS |
| WordPress fit | 1296, every select combination | PASS |
| WooCommerce fit | 7776, every select combination | PASS |
| Shared hosting vs. VPS | 216, every select combination | PASS |
| **Total** | **12947** | **PASS** |

The numeric samples also check algorithm parity outside normal browser field constraints; this is not a claim that browser-native validity checks were exercised by the DOM stub.

## Limits and handoff

This report establishes complete source translation, unchanged content structure and form behavior equivalence. Root/GUI own Hugo build, actual browser layout/accessibility, common navigation/hero/CTA localization, cross-language links, production canonical/hreflang/schema, deployment and live verification. No commit, push, deployment or production change was performed by this subtask.
