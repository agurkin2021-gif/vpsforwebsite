# Cannibalization audit — 2026-10-14

Repository: agurkin2021-gif/vpsforwebsite
Scope: English homepage + 14 core indexable supporting pages
Goal: strict one-query-cluster / one-owner architecture before Google indexing.

## Final status after remediation

- Duplicate core Titles: 0
- Exact primary-query H2/H3 collisions across pages: 0
- Exact cross-page FAQ duplicates: 0
- Meaningful repeated 12-word content fragments across core pages: 0
- Confirmed HIGH-risk cannibalization pairs: 0
- Core pages requiring merge/redirect: 0

Google `site:vpsforwebsite.com` returned no indexed results during the 2026-10-14 check, so this audit validates architecture and on-page ownership rather than query-level URL switching in Search Console.

## Intent ownership

| Page | Primary owner |
|---|---|
| / | VPS for website — broad commercial decision, configurations and routing hub |
| /vps-sizing-for-website/ | generic CPU/RAM/storage/concurrency sizing |
| /vps-vs-shared-hosting/ | stay / optimize / move decision |
| /managed-vs-unmanaged-vps/ | operations and administration responsibility |
| /vps-with-control-panel/ | whether a panel is needed and which panel class |
| /fastpanel-vps-hosting/ | FASTPANEL-specific VPS use case |
| /vps-for-wordpress/ | WordPress-specific workload |
| /vps-for-woocommerce/ | WooCommerce transactional workload |
| /vps-for-multiple-websites/ | multi-site capacity, isolation and blast radius |
| /how-to-host-a-website-on-vps/ | fresh VPS -> live website deployment |
| /website-migration-to-vps/ | existing live-site migration / cutover / rollback |
| /vps-security-checklist/ | hardening and security baseline |
| /vps-backup-strategy/ | recovery, RPO/RTO, retention and restore |
| /vps-monitoring/ | metrics, uptime checks, alerts and capacity evidence |
| /how-to-choose-vps-location/ | audience, latency, routing, CDN and location decision |

## 2026-10-14 remediation

### Homepage vs VPS sizing
Homepage sizing-oriented H2 was retargeted from:
- "Which VPS fits your website workload?"

to:
- "VPS configurations for common website workloads"

Homepage copy now treats configurations as a commercial comparison and delegates resource calculation to /vps-sizing-for-website/.

### Homepage vs Multiple Websites
Removed the homepage FAQ:
- "How many websites can one VPS host?"

This query belongs to /vps-for-multiple-websites/.

Homepage replacement:
- "Can I upgrade a VPS later?"

### Homepage vs Control Panel
Removed the homepage FAQ:
- "Do I need a control panel?"

This query belongs to /vps-with-control-panel/.

Homepage replacement:
- "What should I check before paying for a VPS?"

### Control Panel vs Managed VPS
Removed the duplicated FAQ owner from /vps-with-control-panel/:
- "Does a control panel make the VPS managed?"

The management-status query remains owned by /managed-vs-unmanaged-vps/.

Control-panel replacement:
- "What tasks does a VPS control panel simplify?"

### Shared Hosting vs homepage commercial FAQ
Retargeted:
- "Does VPS include email?"

to:
- "How does email hosting differ between shared hosting and VPS?"

This keeps /vps-vs-shared-hosting/ comparative instead of competing for a broad purchase-inclusion query.

### Control Panel vs Multiple Websites
Retargeted:
- "Can I host multiple websites with one control panel?"

to:
- "What multi-site features should I compare in a VPS control panel?"

The control-panel page now owns panel feature selection; /vps-for-multiple-websites/ owns server capacity and multi-site architecture.

## Expected semantic overlap that must remain

These are parent/child or handoff relationships, not cannibalization:

- VPS for WordPress <-> VPS for WooCommerce
  - WordPress = general CMS workload.
  - WooCommerce = checkout/cart/order/write-heavy workload.

- VPS sizing for website <-> WordPress/WooCommerce
  - Generic sizing = cross-stack capacity model.
  - Child pages = application-specific interpretation.

- VPS with Control Panel <-> FASTPANEL VPS Hosting
  - Generic panel selection vs branded FASTPANEL deployment/sizing.

- How to host a website on VPS <-> Website migration to VPS
  - Fresh deployment vs existing production cutover.

- Security <-> Backup <-> Monitoring
  - Hardening vs recovery vs observation/alerts.

Do not remove normal shared vocabulary such as RAM, CPU, PHP workers, database, backups or monitoring merely to reduce text similarity. Intent ownership matters more than raw term overlap.

## Guardrails for future pages

Do not create a separate indexable page for these phrases unless a fresh SERP proves a distinct owner:

- website VPS hosting
- VPS hosting for websites
- VPS for a website
- VPS for High Traffic Website
- VPS for Agency Websites
- VPS with FASTPANEL
- VPS without Control Panel
- VPS Maintenance Checklist

Current owners:
- broad website VPS variants -> homepage
- high traffic / concurrency -> VPS sizing for website
- agency / client portfolios -> VPS for Multiple Websites
- FASTPANEL variant -> FASTPANEL VPS Hosting
- no-panel route -> How to host a website on VPS
- maintenance tasks -> split across Security / Backup / Monitoring

## Technical duplicate-URL hardening

- Homepage internal links were normalized from `/page/index.html` variants to clean canonical `/page/` URLs.
- No remaining core content links target `index.html`, raw `.md` paths or unsafe relative child paths.
- Live pages use one self-referencing canonical emitted by the local head partial.
- The upstream Basic SEO partial emits a canonical only when a page explicitly defines `.Params.canonical`; the project defines no competing canonical parameters.
- Taxonomy and term pages are disabled globally.
- `content/english/sections/_index.md` is excluded from rendering, listings and sitemap.
- `content/english/sections/call-to-action.md` is now independently protected with `noindex`, `render: never`, `list: never`, `publishResources: false` and `sitemap.disable: true`.
- Page-specific header rendering uses an `if / else if` chain, so each indexable page receives one H1 owner.

## Homepage commercial-intent hardening

Homepage meta description no longer claims the detailed CPU/RAM sizing job. It now owns the broad purchase decision, configuration comparison, management, location, migration, recovery and upgrade-path checks. Detailed resource calculation remains assigned to `/vps-sizing-for-website/`.

## Future validation after indexing

Once Google Search Console has query data, validate cannibalization by query, not impressions alone.

Flag a query when:
1. two core URLs both receive material impressions for the same query;
2. the dominant URL alternates over time;
3. neither URL has a clearly different SERP intent;
4. rankings or CTR weaken because Google is uncertain about the owner.

Do not merge pages merely because two URLs both receive impressions for adjacent long-tail variants.
