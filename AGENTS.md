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
