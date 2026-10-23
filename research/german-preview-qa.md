# German project-prefix preview verification

Build command: `powershell.exe -NoProfile -ExecutionPolicy Bypass -File .qa-tools/build.ps1 -Destination qa-output/preview -BaseURL https://preview.github.io/vpsforwebsite/`.

The isolated Hugo v0.158.0 production build and CSS optimization completed successfully (exit 0). This pass reads only generated preview HTML and source templates. No product source was changed by the reviewer; no publication is claimed.

## Initial preview findings

Checked all 18 German content HTML documents plus the German 404 document.

- All 19 have `noindex,nofollow`; none has a canonical link or alternate hreflang link in the head. Contact has two matching noindex tags, which is harmless.
- All use `lang="de-DE"`. No Google Analytics/Tag Manager loader, `gtag` call or `dataLayer` code appears in their scripts. The measurement ID in the Privacy article is explanatory visible text, not an active loader.
- All 265 HTML asset references use the `/vpsforwebsite/` prefix and resolve to generated files. The 200 internal links in main content also preserve the prefix and point to German destinations. No prefixed target was missing.
- Explicit About and Contact routes exist at `/vpsforwebsite/de/ueber-vpsforwebsite-com/` and `/vpsforwebsite/de/kontakt/`; links within content resolve to them correctly.
- **Menu defect reported to integration:** on all 19 documents, the 15 main-menu links and three footer links retain the preview prefix but resolve to English source routes. For example, the German WordPress menu label links to `/vpsforwebsite/vps-for-wordpress/`; footer About links to `/vpsforwebsite/about/`. The likely cause is Hugo passing already-prefixed menu URLs to `site.GetPage`, so the translation lookup misses the source path.
- **Language-picker fallback defect reported:** untranslated-language fallback links such as `/bn/`, `/pt-br/`, `/fr/`, `/hi/`, `/id/`, `/ru/` and `/vi/` omit the project prefix on all 19 documents. Spanish fallback `/es/` omits it on 15 documents. The 404 picker also omits it for `/`, `/ko/` and `/de/`. These are active anchors, not disabled controls.

## Corrected preview verification — PASS

After integration applied the German-only source-path normalization and language-picker fallback prefix fixes, rebuilt the isolated preview with the same command. Hugo and CSS optimization again exited 0.

- Rechecked all 18 German content documents and the 404 document: correct `de-DE`, `noindex,nofollow`, no head canonical/hreflang links and no analytics loaders/calls.
- All 380 header/footer internal anchors now point to German paths under `/vpsforwebsite/de/`, including the home link and explicit About, Contact and Privacy routes.
- All 209 language-picker anchors retain `/vpsforwebsite/`, including the 404 fallbacks and Spanish fallback where the equivalent ES article is unavailable.
- All 200 main-content internal anchors and all 265 HTML asset references retain the project prefix. Every referenced generated target exists. Open Graph and Twitter image/site URLs also use the preview origin and prefix.
- No remaining wrong-language menu route, lost prefix or missing generated target was found.

Scope limit: this isolated output is the bare Hugo build. Seven other-language placeholder routes (`bn`, `pt-br`, `fr`, `hi`, `id`, `ru`, `vi`) are supplied by the separate existing overlay step, so their file existence is not asserted here. Their 133 picker links now have the correct preview prefix. The requested German pages and all configured-language Hugo destinations exist. Parent integration owns overlay and browser verification.
