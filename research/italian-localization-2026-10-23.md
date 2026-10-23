# Italian localization — published and live-verified

English is the reference. The owner authorized the entire Italian cluster, adaptive titles and full content, all stages without questions. Baseline: `ac18c1bf920ba1a738c264751f21a9722b9fc243`. No guide was accepted from machine translation: all prose and shared UI were manually translated/reviewed against English. An early homepage draft was fully rewritten. Technical names, literal external interface names, code and owner artwork are preservation exceptions, not untranslated prose.

## Release state and evidence

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

## Exact query = Title = H1 inventory

Home is `/it/` without a duplicate keyword-slug page. Contact is noindex. Titles, metadata, full prose, tables, FAQs, diagrams, controls, outcomes, accessibility copy, menus and footer are localized.

| Exact query / Title / H1 | Route |
| --- | --- |
| VPS per siti web | `/it/` |
| Chi siamo | `/it/chi-siamo/` |
| Contatti | `/it/contatti/` |
| Hosting VPS con FASTPANEL | `/it/hosting-vps-con-fastpanel/` |
| Come scegliere la posizione del VPS | `/it/come-scegliere-la-posizione-del-vps/` |
| Come ospitare un sito web su VPS | `/it/come-ospitare-un-sito-web-su-vps/` |
| VPS gestito o non gestito | `/it/vps-gestito-o-non-gestito/` |
| Informativa sulla privacy | `/it/informativa-sulla-privacy/` |
| Strategia di backup VPS | `/it/strategia-di-backup-vps/` |
| VPS per più siti web | `/it/vps-per-piu-siti-web/` |
| VPS per WooCommerce | `/it/vps-per-woocommerce/` |
| VPS per WordPress | `/it/vps-per-wordpress/` |
| Monitoraggio VPS | `/it/monitoraggio-vps/` |
| Checklist di sicurezza VPS | `/it/checklist-di-sicurezza-vps/` |
| Dimensionamento VPS per siti web | `/it/dimensionamento-vps-per-siti-web/` |
| VPS o hosting condiviso | `/it/vps-o-hosting-condiviso/` |
| VPS con pannello di controllo | `/it/vps-con-pannello-di-controllo/` |
| Migrazione di un sito web su VPS | `/it/migrazione-di-un-sito-web-su-vps/` |

## Manual content review coverage

| English-relative source | Reviewed content units |
| --- | ---: |
| `_index.md` | 110 |
| `about/_index.md` | 33 |
| `contact/_index.md` | 4 |
| `privacy-policy.md` | 23 |
| `sections/_index.md` | 1 |
| `sections/call-to-action.md` | 3 |
| `vps-sizing-for-website.md` | 258 |
| `website-migration-to-vps.md` | 292 |
| `managed-vs-unmanaged-vps.md` | 311 |
| `vps-for-wordpress.md` | 292 |
| `vps-for-woocommerce.md` | 337 |
| `vps-vs-shared-hosting.md` | 288 |
| `vps-for-multiple-websites.md` | 294 |
| `vps-with-control-panel.md` | 307 |
| `fastpanel-vps-hosting.md` | 225 |
| `how-to-host-a-website-on-vps.md` | 395 |
| `vps-security-checklist.md` | 332 |
| `vps-backup-strategy.md` | 397 |
| `vps-monitoring.md` | 404 |
| `how-to-choose-vps-location.md` | 393 |

All 507 shared UI/hero entries were also manually reviewed. All 522 guide heading IDs are retained; About and Privacy add 16 original source anchors. Source parity checks compare structure, original facts, code, script decisions, controls and affiliate links. About/Contact render the full English source bodies although the historical English template hides those bodies; this is a reviewed rendering exception.

## Final evidence artifacts (local, not deployed)

- `qa-output/italian-publication-audit.json`: final source/render audit, 20/18/16, passed.
- `qa-output/italian-browser-final/report.json`: complete release-build Chromium matrix, 18 pages/90 geometry cases/16 forms/18,736 states, zero findings.
- `qa-output/italian-panel-final/report.json`: final shortened license option, five widths/288 states, zero findings. Option value and decision logic unchanged.
- `qa-output/final-copy-sweep.json`: final build changes only Italian Control Panel HTML compared with the full-browser release build; remaining shared English strings are technical names/specifications, not prose.
- `qa-output/integration-checks.log`: integrity, recovery, restored locales, French and German checks pass.
- `qa-output/existing-locale-regression.json`: main content of all 200 pre-existing HTML pages unchanged against published German baseline; original hero SHA-256 unchanged.
- `qa-output/release-html-delta.json`: prior grammar refinement affected only Italian Multiple Websites; full browser run used the refined release build.
- `qa-output/italian-preview.json`: 19 preview documents, 380 menu links, 228 picker links, 200 article links, 149 assets, zero findings.
- `.qa-tools/navigation-fixture.py`: native DE/IT translated-slug routing, reverse links, Contact noindex with reversed meta attributes, home fallback without false hreflang, unchanged body, semantic idempotence all pass.
- `qa-output/visual/` and browser screenshots: representative mobile/desktop visual proofreading, including tables/forms/Contact/404. A long mobile Control Panel option was shortened and retested.

Publication and independent actual live verification are complete. The exact source/generated commits, Actions/Cloudflare result and live evidence are recorded above.
