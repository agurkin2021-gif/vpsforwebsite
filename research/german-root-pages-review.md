# Independent review of root-owned German pages

Scope: `content/german/vps-for-multiple-websites.md` and six home/support files: `_index.md`, `about/_index.md`, `contact/_index.md`, `privacy-policy.md`, `sections/_index.md`, `sections/call-to-action.md`. Every English source and German counterpart was read completely. Review is against the current English master in the clean `bc66649` checkout, not the older working copy.

**Result: no unresolved material omissions, factual changes or functional regressions found in these seven source files.** Three small language improvements were reported to root and are now present in the files. This review did not modify product content.

## Completeness and natural German

The multi-site guide preserves all **38 headings, 36 table rows, 110 bullet items and 4 numbered steps**, including the complete architecture checker, operational responsibilities, isolation boundaries, one-IP/SNI explanation, combined peak examples, client exit procedures, restore granularity, split criteria, monitoring, launch checklist and all ten FAQ answers. The affiliate disclosure and the source's explicit warning against fixed website-count promises remain intact. Its source/translation lengths are 517/518 lines; the extra line is the German slug.

The homepage retains all seven feature groups, four VPS configurations, methodology items, navigation/button destinations and thirteen FAQ questions with full answers. Its YAML hierarchy/list shape matches English. No section is shortened into a summary or replaced with unsupported regional claims.

About retains all seven sections and nine methodology bullets. Contact retains the exact operational position that there is currently no public contact form, and preserves `noindex: true` and the disabled sitemap entry. Privacy retains all nine sections, the GA4 measurement ID `G-J6X9FNRMH5`, the review date, the external Google policy URL, affiliate disclosure, log-processing statement and no-contact-form statement. The shared sections retain their nonrendering/nonlisting/noindex configuration. CTA meaning and partner URL are preserved in full.

The translation consistently uses formal **Sie**, idiomatic German sentence structure and recognisable technical product names. Three minor wording findings have been corrected by the owner and reread:

- Multi-site agency paragraph: `Verschiedene Kundeneigentümer` → `Websites verschiedener Kunden`.
- Homepage WooCommerce bullet: `Kassiervorgänge` → `Checkout-Vorgänge`.
- Homepage first FAQ: `mit zugewiesener CPU, RAM und Speicherplatz` → `mit zugewiesenen CPU-, RAM- und Speicherressourcen`.

## Anchors, numbers and links

- All **38 multi-site H2/H3 IDs match the rendered English baseline in order**, including punctuation-derived double hyphens such as `manual-server-blocks--virtual-hosts`, `static--cached-sites` and `woocommerce--membership--transactional-sites`.
- All **9 privacy H2 IDs** match its rendered English baseline in order.
- About's seven explicit IDs correspond to the English source headings. The baseline English About template does not render its Markdown body, so that older rendered page does not provide equivalent H2 IDs for a rendered-ID comparison. This is an inherited English-template limitation, not a missing German section.
- Across all seven files, **the complete multiset of numeric tokens is unchanged** after excluding the added explicit Markdown anchor syntax. This is stricter than checking only CPU/RAM/storage units: dates, PHP-related identifiers, network speeds, port numbers, GA4 identifier components, dollar amounts and all other digit tokens are preserved.
- Existing translation audit confirms unchanged affiliate occurrence counts, href targets, internal Markdown link counts, HTML IDs, heading levels, table row counts and script count, with only the reviewed exceptions below.
- All multi-site input/select/option opening tags are byte-identical to English: seven selects and eighteen options retain their IDs, values, order, classes and other attributes.

## Executed multi-site checker verification

The JavaScript has **exactly seven changed string literals**, all user-facing: four decision messages and three administration-model suffixes. All remaining string literals and the complete string-masked executable logic match English.

Executed the actual EN and DE submit handlers under Node.js `v24.15.0` using a strict DOM stub that rejects missing IDs. Tested **all 576 select combinations**, covering **12 distinct outputs**. The actual German output was normalized through the reviewed display-string correspondence and compared with actual English output. **576/576 PASS**; branch decisions, concatenated suffixes and option handling match. The script was executed as written, not replaced by a reimplementation.

The homepage contains YAML data rather than an inline script; common home checker implementation and dictionary wiring belong to the shared-integration review and root's browser tests.

## Existing audit output and accepted exceptions

Ran `scripts/translation_audit.py` for every file pair:

| File | Reported differences | Review |
|---|---|---|
| Multi-site | `prices`, extra `slug` | Daily units translated `/day` → `/Tag`; amounts/occurrences unchanged. Accepted German route. |
| Home | `prices` | `/day` → `/Tag`, `/month` → `/Monat`; daily/monthly intervals and all USD amounts unchanged. |
| About | extra `url` | Accepted `/de/ueber-vpsforwebsite-com/` route. |
| Contact | extra `url` | Accepted `/de/kontakt/` route; noindex/sitemap settings unchanged. |
| Privacy | extra `slug` | Accepted `datenschutzerklaerung` route. |
| Sections index | none | Literal audit PASS. |
| Shared CTA | image path | Intentional localized `vps-cta-de.svg` in place of English `vps-cta.svg`. |

No audit produced a JavaScript logic warning. The checker's generic “natural Spanish” disclaimer is inherited script wording and does not describe the target language of this review.

## Owner artwork exception

The original owner-provided hero artwork remains byte-identical, as required by project context. Its SHA-256 is:

`af91640a83f2564d6b91777550e9b9d6435eeca232b876473037c58f95346fb1`

The current built German home references that exact fingerprinted WebP and has German alt text **VPS für Websites**. Any English lettering embedded in the original owner artwork is an explicit preservation exception, consistent with the Korean implementation; it is not an overlooked prose translation. This review did not re-encode, regenerate or change image quality.

## Limits

This is an independent content/source-functional review, with a read-only check of the current built hero reference. It does not substitute for root's final all-page build, browser responsiveness, live deployment, canonical/hreflang/schema and asset rendering checks. No production access or deployment was performed here.
