# German shared-interface integration

Reference: `main` commit `bc66649`, English Hugo source. Work date: 2026-10-22. This report covers shared integration, not publication.

## Source integration

- Registered `de`, `Deutsch`, `de-DE`, `content/german`, and the German main/footer navigation. Existing locale order is preserved; Deutsch is the eleventh selector entry.
- `i18n/de.yaml` includes all **248/248** English dictionary keys, **257** additional German guide-hero/diagram strings, and the two fallback search messages emitted by the upstream module. Search remains disabled. All literal `T` references in local templates resolve in the German dictionary.
- Added German branches to **280** existing page-header conditions, retaining the English and Korean branches. A source comparison that removes only the inserted German branches reproduces the original page-header exactly (the existing KO-only code-block overflow rule is additionally enabled for DE).
- German homepage paragraphs, rendered Markdown links, navigation and footer use the existing translated-source-path resolver. The render hook retains the relref-shortcode placeholder guard, preventing protocol-relative `//de/...` links.
- German About and Contact render their complete section content, following the established Korean list-template behavior. The agreed translated service-page routes are resolved through Hugo rather than concatenating English slugs.
- Added a German-only 404 template using the upstream English template's structure and classes. Its title is localized and the return link targets the German homepage. German publisher metadata says `VPSforWebsite.com Redaktion`.
- The German CTA SVG preserves every original element, attribute, dimension and resource value. Only its title and text labels differ. The owner's homepage WebP is unchanged.
- The original brand name, product names, protocol identifiers, form-control IDs/values, checker decision algorithms, affiliate URL and sponsored-link attributes remain unchanged.

## Publication preparation

`restore-language-navigation.py` now discovers real EN↔DE page pairs from the generated Hugo alternates. On noindex service pages it reads Hugo's translated picker pairs. It then adds German counterparts to recovered-page menus and appropriate hreflang sets. An untranslated article may link to `/de/` in the picker, but that fallback is not advertised as an equivalent article in hreflang. German Contact keeps noindex and has no generated hreflang block. `audit-language-recovery.py` now requires all eleven locale homes and selector entries.

No `recovered-public` or generated `cloudflare-public` file is edited as source. The existing deployment workflow still builds Hugo, overlays only missing recovery files, repairs navigation, audits assets and links, rebuilds the sitemap and publishes generated output.

## Checks completed

- YAML/key coverage: **PASS**, 248 English keys present, 507 German keys total, no unresolved literal local-template keys.
- Page-header English/Korean source preservation: **PASS** after stripping only the new German branch instructions.
- CTA SVG geometry/attribute parity: **PASS**.
- Isolated navigation fixtures (`.qa/test-de-navigation.py`): **PASS**. Covered a German translated slug on a recovered French article, equivalent EN/DE targets, German noindex Contact, missing-translation fallback without false hreflang, retained article body, and semantic stability on a second pass. Absolute/relative forms of the same internal URL are normalized for that comparison; the inherited publisher may reorder head links.
- Final recovery review found that `noindex` detection depended on the order of the meta attributes. It now uses the existing HTML attribute parser. The reversed `content`/`name` regression fixture and all five actual affected recovered Contact documents (BN/HI/ID/RU/VI) pass. No recovered HTML/CSS source was changed.
- First compiled eight German pages: shared hero/CTA/menu and accessible attribute scan found no checked English UI markers. This was an intermediate build, before all guide sources were ready.
- Independent existing-locale regression: **41/41** baseline EN/KO/ES HTML pages retain identical main text and element structure/attributes, after removing script/style nodes only. Compared `qa-output/baseline` (exact `bc66649` build) with the intermediate `qa-output/build`; no original page is missing. Machine report: `qa-output/german-existing-locale-regression.json`.
- German wording review: direct address consistently uses **Sie**; labels and procedural diagram steps use neutral infinitives. Product names, established German technical terms (VPS, Shared Hosting, Control Panel, Worker, Snapshot), protocols and units are retained. Clarified named-account security labels as `Eigenes Benutzerkonto` / `Eigenes Admin-Konto`, and the dynamic-load form question as `verursacht sie viel dynamische Last`.
- Project-path preview regression: Hugo prefixes menu URLs with the BaseURL path, while `GetPage` requires source paths. The German resolver now removes only that known prefix before selecting the translated page; `.RelPermalink` restores the correct public prefix. German picker fallback homes also use relative `relURL` inputs. Root-domain production paths and other locale branches are unchanged. Rebuilt preview verification passes **380** German header/footer links and **209** picker targets across 18 content pages plus 404; SEO, local resources and article links also pass. See `research/german-preview-qa.md`. Availability of recovered-only locales is separately limited by the contents of a source-only Hugo preview.

## Responsive corrections

The first real Chromium run at 390 px found two German-text issues: the wide sizing comparison exceeded the page width (589 px), and a panel-guide compound heading extended to 478 px. `static/css/de-responsive.v1.css` is linked only on German pages and permits compound-word wrapping while preserving fonts, colors and layout. The existing Korean horizontal table-scroll rules are reused for German `.vps-table-scroll` wrappers; the content owner adds the wrapper to the wide sizing comparison. Code blocks retain their own horizontal scrollbar.

The final complete-page build, responsive measurements, all checker scenarios, complete merged-deployment audits and publication are tracked by the coordinating validation report. They are not implied by the intermediate source checks above.
