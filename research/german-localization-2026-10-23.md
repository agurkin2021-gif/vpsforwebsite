# Complete German localization — 2026-10-23

## Status and reference

English reference: the clean `vpsforwebsite-german` checkout at commit `bc66649`. **The complete German release is published and live-verified at 2026-10-23T03:34:31.715Z.** Complete source/rendered parity, project-prefix preview, production build, automated deployment and actual live browser/SEO checks pass. The final section records commit IDs, workflow evidence and verified scope.

The implementation follows the existing English information architecture and source content. It adds the German locale to the Hugo source and established generated-output deployment pipeline. No generated recovery output is used as an editable source, and no existing English content is rewritten.

## Coverage

| Item | Verified scope |
|---|---:|
| English Markdown sources | 20 |
| Matching German Markdown sources | 20 |
| German content pages | 18 |
| Complete German guides | 14 |
| Homepage | 1 |
| Support pages: About, Contact, Privacy | 3 |
| Non-page shared section sources | 2 |
| Rendered interactive forms | 16 |
| Guide H2/H3 anchors retained from English | 522 |
| German dictionary keys | 507 |

The two shared section sources preserve their nonrendering/nonlisting configuration and are not counted as public content pages. A separately localized 404 template is also present. The 16 forms comprise the homepage checker, two sizing-page tools, and one checker on each of the other 13 guides.

Each English source was read completely before translation. Complete paragraphs, lists, tables, FAQ answers, metadata, disclosures, form labels/options, initial messages and JavaScript result messages are retained. The homepage preserves all seven feature groups, four VPS configurations and thirteen FAQ answers. About, Contact and Privacy retain their complete source meaning; German About and Contact deliberately render source bodies that the inherited English templates historically hid.

## German queries, titles and routes

The page topic is expressed as a natural German query or task. The accepted target phrase, rendered Title and single H1 match exactly. Guide filenames remain the English translation keys, while German `slug` or explicit section `url` fields supply readable German routes. Umlauts are retained in visible text and transliterated where needed in URLs.

These are editorial localization choices, **not measured search-volume or ranking claims**. No search-demand numbers, German-market billing terms, EUR conversions, new provider locations, German support promises or certifications were invented. Existing USD amounts, resource values, source dates and provider qualifications remain authoritative. Visible billing units are translated to `/Tag`, `/Monat` and `/Jahr` without changing their intervals.

| English route | German Title / H1 | German route |
|---|---|---|
| `/` | VPS für Websites | `/de/` |
| `/about/` | Über VPSforWebsite.com | `/de/ueber-vpsforwebsite-com/` |
| `/contact/` | Kontakt | `/de/kontakt/` |
| `/fastpanel-vps-hosting/` | VPS-Hosting mit FASTPANEL | `/de/vps-hosting-mit-fastpanel/` |
| `/how-to-choose-vps-location/` | VPS-Standort auswählen | `/de/vps-standort-auswaehlen/` |
| `/how-to-host-a-website-on-vps/` | Website auf einem VPS hosten | `/de/website-auf-einem-vps-hosten/` |
| `/managed-vs-unmanaged-vps/` | Managed VPS vs. Unmanaged VPS | `/de/managed-vps-vs-unmanaged-vps/` |
| `/privacy-policy/` | Datenschutzerklärung | `/de/datenschutzerklaerung/` |
| `/vps-backup-strategy/` | VPS-Backup-Strategie | `/de/vps-backup-strategie/` |
| `/vps-for-multiple-websites/` | VPS für mehrere Websites | `/de/vps-fuer-mehrere-websites/` |
| `/vps-for-woocommerce/` | VPS für WooCommerce | `/de/vps-fuer-woocommerce/` |
| `/vps-for-wordpress/` | VPS für WordPress | `/de/vps-fuer-wordpress/` |
| `/vps-monitoring/` | VPS-Monitoring | `/de/vps-monitoring/` |
| `/vps-security-checklist/` | VPS-Sicherheitscheckliste | `/de/vps-sicherheitscheckliste/` |
| `/vps-sizing-for-website/` | VPS für Websites dimensionieren | `/de/vps-fuer-websites-dimensionieren/` |
| `/vps-vs-shared-hosting/` | VPS vs. Shared Hosting | `/de/vps-vs-shared-hosting/` |
| `/vps-with-control-panel/` | VPS mit Control Panel | `/de/vps-mit-control-panel/` |
| `/website-migration-to-vps/` | Website auf einen VPS umziehen | `/de/website-auf-einen-vps-umziehen/` |

## Translation and integration stages

1. Reviewed the repository instructions, current context and localization workflow against the current user-authorized full German scope. Used the clean English source as the master rather than an older working tree.
2. Translated all 20 source counterparts in page-sized units, preserving complete content and existing technical distinctions. The tone consistently uses formal **Sie**; labels and diagram steps use natural German wording while established product names and technical identifiers remain recognizable.
3. Compared structure and executable behavior with English. Explicit Markdown anchors preserve the actual rendered English IDs, including punctuation-derived double hyphens. The six-guide, seven-guide and multi-site reviews account for all 522 guide IDs. Two inherited Korean-reference discrepancies were corrected by checking the English rendered baseline directly.
4. Registered `de`, `Deutsch`, `de-DE`, `content/german`, localized menus and publisher metadata. Added 248/248 English dictionary keys, 257 guide/diagram strings and two upstream fallback-search messages, totaling 507 keys. Search remains disabled. Deutsch is the eleventh language-selector entry.
5. Extended existing shared hero/header conditions with German branches while preserving the English and Korean branches. Added translated guide diagrams, complete support-page rendering, a German 404 and a text-localized CTA SVG.
6. Built the complete production-origin Hugo output, applied the existing recovery-overlay/navigation workflow, and ran source/rendered audits. Separately built the project-prefix preview and fixed its German-only navigation normalization defects.
7. Completed final real-browser checks for all pages and forms, rebuilt production after the routing and final copy fixes, published the source through the existing pipeline and verified the actual live release. The final section contains the complete evidence.

## Preserved content and behavior

- All 522 guide heading IDs match the actual English rendered baseline in sequence. Table structures, ordered/unordered list counts, complete fenced command/configuration blocks and source links remain intact.
- Form-control IDs, classes, names, option values, defaults, numeric limits and JavaScript decision algorithms are preserved. Source-level script comparisons isolate changes to user-facing strings rather than replacing the logic. All 16 rendered forms match the English form/control structure.
- Dollar amounts, CPU/RAM/storage specifications, dates, ports, addresses, software-version references and dynamic computed values are preserved. Two English thousands separators are removed to avoid German decimal ambiguity: `1,970 MB` → `1970 MB`, and `86,400 seconds` → `86400 Sekunden`.
- Every affiliate target remains `https://www.vdsina.com/?partner=ni8gzrvz75`, with matching occurrences and `sponsored nofollow noopener` attributes. Disclosures and the support-versus-management and panel-versus-management distinctions remain intact.
- Contact retains `noindex: true`, exclusion from the sitemap and the statement that no public contact form is available. Privacy retains its review date, policy URL, GA4 measurement ID, logging/affiliate statements and no-contact-form statement.
- German-only responsive CSS permits long compound words to wrap. The wide sizing comparison uses the established horizontal table-scroll wrapper with a localized accessibility hint; every original table cell remains. Fonts, colors and overall layout are preserved, and code blocks retain their own horizontal scrolling.
- Existing English, Korean and Spanish main text and main-element structure/attributes matched the exact baseline on all 41 pages in the recorded regression comparison. That recorded comparison used the intermediate complete-locale integration output; final release-wide results are recorded separately below.

The generic `translation_audit.py` CLI reports deliberate slug/URL additions, localized billing-period suffixes, the localized CTA SVG and the sizing accessibility hint as literal differences. These were reviewed explicitly; the complete German audit normalizes only the documented exceptions. Its inherited warning mentioning Spanish is generic checker text, not a finding about German coverage.

## Artwork preservation exception

The owner-provided homepage WebP remains byte-identical. Its SHA-256 is:

`af91640a83f2564d6b91777550e9b9d6435eeca232b876473037c58f95346fb1`

The German home uses that exact fingerprinted asset with German alt text **VPS für Websites**. English lettering embedded in this original owner artwork is an explicit preservation exception, consistent with the Korean implementation. The artwork was not regenerated, re-encoded or reduced in quality.

The separate German CTA SVG is localized text in the existing vector artwork: every original element, attribute, dimension and resource value is preserved. This is distinct from the unchanged owner WebP.

## Completed validation evidence

| Check | Recorded result | Evidence |
|---|---|---|
| Full German source/rendered audit | PASS: 20 matching sources, 18 pages, 16 forms, no errors | `qa-output/german-audit.json` |
| Guide group one | Six complete guides; 197 anchors, controls, numbers and source structure preserved | `research/german-first-seven-qa.md` |
| Guide group two | Seven complete guides; 287 anchors, complete script parity excluding visible strings, identical command blocks and numeric sequence | `research/german-last-seven-qa.md` |
| Root-owned pages and multi-site guide | Independent full-source review; no unresolved material omission or functional regression | `research/german-root-pages-review.md` |
| Shared integration | Dictionary coverage, source-branch preservation, SVG parity and navigation fixtures PASS | `research/german-integration-qa.md` |
| Existing-locale baseline regression | 41/41 EN/KO/ES pages PASS for main text and structure/attributes | `qa-output/german-existing-locale-regression.json` |
| Recovered localized-page audit | `ISSUE_COUNT 0` across eight recovered locales | `qa-output/localized-pages-report.json` |
| Project-prefix preview | PASS for all 18 German content pages plus 404 | `research/german-preview-qa.md` |
| Final real-browser run | PASS: 18 pages, 90 viewport cases, 16 forms, 18,736 input states, zero findings | `qa-output/browser-final/report.json` |

The complete German audit verifies matching page Title/H1, German descriptions, production self-canonical and EN/DE/x-default alternates on indexable pages, Contact's noindex behavior, unique IDs, form/control parity, rendered structure, anchor targets, affiliate attributes and local-link existence. It preserves the intentionally different support-page rendering described above.

Executed source-functional checks include **12,947** actual EN/DE JavaScript comparisons for the first six guides (seven forms), including all select combinations and 50 sizing numeric/default/boundary samples. The multi-site guide separately passes **576/576** select combinations covering 12 outputs. These used the actual handlers with strict DOM stubs; they do not substitute for browser-native validation or the final all-form browser run.

The recovery integration discovers real EN↔DE page pairs rather than inventing equivalent translations. A picker fallback to `/de/` is not advertised as an article equivalent in hreflang. Noindex detection uses parsed attributes, including a regression for reversed attribute order; the five affected recovered Contact documents pass the recorded review. Existing locale order and the source-driven overlay workflow remain intact.

### Merged-output integrity and recovery

The coordinator's completed command output records the following results before the final post-prefix-fix production rebuild:

| Check | Result |
|---|---|
| `audit-site-integrity.py qa-output/build` | 202 HTML files, 280 local targets, 70 stylesheet references, zero errors |
| `audit-language-recovery.py` | 159 cached HTML snapshots preserved, 11 locale homes, 198 switchers, zero errors |
| `audit-french-parity.py` | Both guides PASS |
| Bengali critical CSS | 18/18 pages PASS |
| French page audit | 18 pages, zero errors |
| Rebuilt merged sitemap | 189 URLs |
| `test-site-integrity.py` | Three tests PASS |

The earlier orchestration session exited 1 only because a final reporting step tried to parse a UTF-16 text log as JSON; the preceding audit commands passed. The final post-prefix-fix production rebuild repeated every command successfully with exit 0 and saved UTF-8 output to `qa-output/final-local-validation.log`. All totals above were reconfirmed. Every one of the **202 HTML files is byte-identical** to the fully browser-tested build (`qa-output/final-html-diff.json`, changed: 0).

### Final browser run

The actual browser run completed with exit 0. The saved report records **18 pages**, **90 geometry cases** at **320, 390, 768, 1280 and 1920 px**, **16 forms**, **18,736 German input states compared with the actual English outputs**, and **zero findings**. This supersedes intermediate browser runs made while some German pages were still being added.

The coordinator also visually reviewed WooCommerce at 390 px and the Control Panel page at 1280 px, with homepage 390/1280 px views reviewed earlier. Screenshots and detailed form outcomes are retained under `qa-output/browser-final/`. A final text sweep then localized two remaining labels: Contact's primary CTA and Monitoring's CPU/RAM/storage/network diagram caption. Each production rebuild and all audits passed, with sequential hash comparisons showing only those two German HTML files changed. Independent real Chromium checks of both pages at five widths passed **10/10**, without clipping, JavaScript errors or missing resources; four 390/1280 hero screenshots were visually reviewed. Evidence: `qa-output/browser-targeted/report.json` and screenshots. No form code changed. These are local-rendered results; they are not a claim that production has already been updated.

### Project-prefix preview

Built with Hugo v0.158.0 at `https://preview.github.io/vpsforwebsite/`. All 19 German HTML documents have `de-DE` and `noindex,nofollow`, with no head canonical/hreflang links and no GA4 loader/calls. The Privacy article's explanatory measurement-ID text is not an active analytics loader.

The initial preview exposed already-prefixed menu URLs failing source-path translation lookup and fallback language links losing the base path. German-only normalization fixes were rebuilt and independently checked: **380 header/footer links**, **209 picker links**, **200 main-content internal links**, and **265 HTML asset references** pass. Explicit About, Contact and Privacy routes resolve correctly. Seven recovered-only language placeholders require the separate overlay stage; their 133 picker links have the correct preview prefix, but their file existence is not claimed for a bare Hugo preview.

## Final verification and publication

The complete source, automated publication and actual live-site checks have passed. Local and production evidence are distinguished below.

- **Final production rebuild and integrity/recovery command logs:** PASS, exit 0, all listed totals reconfirmed; UTF-8 log `qa-output/final-local-validation.log`, source/HTML report `qa-output/german-audit.json`. The preview-only fixes preserved all 202 HTML hashes. Subsequent sequential builds changed only German Contact and Monitoring for the two final copy fixes, both separately browser-verified.
- **Final existing-locale check:** all existing-language HTML hashes remained unchanged in every final rebuild, preserving the independent 41-page EN/KO/ES visible-content and structure regression result. No additional form logic changes followed the exhaustive browser pass.
- **Source commit and push:** `1cb67568f28920751bf886c28a1c520f2adf38ce` published to `main`; reviewed tree SHA `342046cd2acf67172f84f1243c05de44d8d4270c` exactly matched the Git index. All 49 uploaded Git blobs were SHA-verified.
- **Generated deployment workflow:** [Run 39894681997](https://github.com/agurkin2021-gif/vpsforwebsite/actions/runs/39894681997) **success**, generated commit `2ff6c42d8911e438c4fe2eb0d768c4c042d9d47a`; German CI summary 18 pages / 90 geometry / 16 forms / 18,736 cases / zero failures. Cloudflare Workers deployment succeeded with build and version IDs recorded below.
- **Production/live verification:** completed at `2026-10-23T03:34:31.715Z`; all 18 routes HTTP 200 with exact translated content, SEO/menu/anchor/sitemap parity, plus separate live Chromium at 390/1280 and exhaustive form checks. Full evidence follows.

- **Published and live-verified at 2026-10-23T03:34:31.715Z.** Source `main` commit `1cb67568f28920751bf886c28a1c520f2adf38ce`; generated deployment commit `2ff6c42d8911e438c4fe2eb0d768c4c042d9d47a`. [Prepare Cloudflare static site](https://github.com/agurkin2021-gif/vpsforwebsite/actions/runs/39894681997) completed **success**, including the final-source German run: 18 pages, 90 geometry cases, 16 forms, 18,736 input states, zero findings. [Browser reports/screenshots](https://github.com/agurkin2021-gif/vpsforwebsite/actions/runs/39894681997/artifacts/12475648879) are retained for seven days. Production Hugo validation, Korean link routing and Korean multi-site browser checks also succeeded.
- Cloudflare **Workers Builds: vpsforwebsite** succeeded for the generated commit: build `668cb30d-a5e8-4799-869d-61a246321b0b`, deployed version `ca86803c-7296-4876-b7fd-1dcb8fa312a1`. No manual Worker/static asset changes were made.
- The existing [French responsive Chromium audit](https://github.com/agurkin2021-gif/vpsforwebsite/actions/runs/39894883021) also completed successfully. Actual live `robots.txt` allows the German routes, and the fetched owner hero is HTTP 200, 51,196 bytes, with the exact original SHA-256 `af91640a83f2564d6b91777550e9b9d6435eeca232b876473037c58f95346fb1` (`qa-output/live-seo/robots-hero.json`).
- Independent actual live HTTPS/SEO verification passed **18/18 HTTP 200** routes with German Title/H1 and content matching the final build; 360 menu/footer links, 313 internal German links and 114 anchors pass. Sitemap contains exactly 17 indexable German routes; Contact remains noindex without canonical/hreflang. Separate actual live Chromium passed **36 viewport cases (390/1280), all 16 forms and all 18,736 input states against live English, zero findings**, plus actual pointer submissions and equivalent-language roundtrips. Evidence is under `qa-output/live-seo/` and `qa-output/browser-live/` in the isolated checkout.
- The complete German cluster is published at **https://vpsforwebsite.com/de/**. No German page or publication gate remains pending. English reference and other-language prose, original code/price values and owner artwork remain preserved.
