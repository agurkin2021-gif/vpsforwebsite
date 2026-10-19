# AGENTS.md — vpsforwebsite.com

Before making any change in this repository:

1. Read `CHATGPT_PROJECT_CONTEXT.md` completely.
2. Read `CHATGPT_SEO_AUDIT_BUFFER.md` before SEO, content, homepage, supporting-page, or internal-linking work.
3. Treat both files as the persistent project context / SEO decision log.
4. Inspect the current repository state; do not rely only on remembered chat context.
5. Preserve all non-negotiable rules unless the user explicitly changes them.
6. After every substantive repository change, update `CHATGPT_PROJECT_CONTEXT.md`; after substantive SEO/content changes, also update `CHATGPT_SEO_AUDIT_BUFFER.md` in the same work session.

Critical SEO rule:
- The primary target query must match `Title` exactly.
- `H1` must be identical to `Title`.
- The URL slug must use the same keyword phrase in URL form.
- Do not add tails or extra words to `Title` or `H1`.
- Homepage target query: `VPS for website`.
- Homepage remains at `/`; do not create a duplicate `/vps-for-website/` homepage.

Critical design rule:
- Hugo + original Hugoplate visual system.
- Do not replace it with a custom design unless explicitly requested.

Deployment / source-of-truth contract:
- GitHub repository `main` is the only place for site management and edits.
- Do not edit the live Cloudflare Worker code or uploaded assets manually in the Cloudflare dashboard.
- Do not edit `cloudflare-public/**` as source content. It is generated deploy output and can be overwritten by automation.
- For Hugo-managed pages, edit `content/**`, `layouts/**`, `assets/**`, `static/**`, `config/**`, `i18n/**`, or `data/**`.
- English and Spanish are currently Hugo-source-managed.
- Cache-recovered languages/pages that do not yet exist in Hugo source remain under `recovered-public/**`; edit those files in GitHub until that language/page is migrated into Hugo source.
- `.github/workflows/prepare-cloudflare-static.yml` builds Hugo, preserves Hugo output over the recovery snapshot, restores known cache-miss fallback pages, rebuilds the deployment sitemap from the actual deployable HTML, and commits the generated `cloudflare-public/**`.
- Cloudflare is connected to GitHub `main` and deploys the generated `cloudflare-public/**` through Worker `vpsforwebsite`.
- After a production content change, verify: GitHub Action success -> generated static commit -> Cloudflare deployment Ready -> target live URL.
