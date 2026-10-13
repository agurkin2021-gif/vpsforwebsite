# Cluster-wide cannibalization, overlap and internal-link audit
Date: 2026-10-13
Scope: homepage + 14 frozen core pages
Repository: agurkin2021-gif/vpsforwebsite

## Executive verdict

After the audit and remediation pass, there is **no confirmed HIGH-risk cannibalization remaining in the 15-page core cluster**.

The architecture is coherent:
- homepage owns the broad commercial query `VPS for website`;
- each supporting page owns one distinct decision, workload or operational job;
- the strongest semantic overlaps are intentional parent/child or handoff relationships;
- no core page is orphaned;
- exact primary-query headings do not appear as competing H2/H3 owners on another core page;
- the one exact FAQ collision found between generic sizing and WordPress was removed;
- stale "planned/future page" references were replaced with live contextual links;
- homepage now routes contextually into Security, Backup and Monitoring in addition to the commercial/decision pages;
- one broken Location-page section anchor was fixed;
- Guides navigation order is now deterministic.

## Intent ownership map

| Owner | Primary job | Do not let it own |
|---|---|---|
| Homepage — VPS for website | broad VPS-for-website commercial decision and routing hub | deep sizing, migration, security, backup, monitoring, panel or location detail |
| VPS sizing for website | CPU/RAM/storage/concurrency sizing | WordPress-only or WooCommerce-only exact subqueries, location choice |
| Website migration to VPS | existing-site cutover, data sync, DNS, rollback, acceptance | fresh-server deployment tutorial |
| Managed vs Unmanaged VPS | who owns operations/support/admin work | panel selection, stay-on-shared decision |
| VPS for WordPress | WordPress-specific workload and operations | WooCommerce transactional intent, generic cross-stack sizing |
| VPS for WooCommerce | cart/checkout/order/database transactional workload | normal cached WordPress intent |
| VPS vs Shared Hosting | stay/optimize/move decision | detailed managed-vs-unmanaged responsibility matrix |
| VPS for Multiple Websites | combined workloads, isolation, blast radius, agency/client portfolio | generic sizing or generic panel selection |
| VPS with Control Panel | whether a panel is needed and which panel class | FASTPANEL branded use case, management ownership |
| FASTPANEL VPS Hosting | FASTPANEL-specific deployment/sizing/use case | generic panel comparison |
| How to host a website on VPS | fresh VPS -> live website deployment | live-site migration/cutover, deep hardening, deep monitoring |
| VPS Security Checklist | hardening and recurring security baseline | recovery architecture, monitoring/alert design |
| VPS Backup Strategy | RPO/RTO, copies, retention, restore | security hardening, broad monitoring |
| VPS Monitoring | metrics, external checks, alerts, history, capacity evidence | backup architecture, security hardening |
| How to Choose VPS Location | audience/routing/CDN/dependency/data-location decision | CPU/RAM sizing or generic provider-location catalog |

## Pair audit

### MEDIUM overlap — valid, strict ownership retained

#### VPS with Control Panel <-> FASTPANEL VPS Hosting
Similarity is expected because FASTPANEL is one member of the generic panel category.
Verdict: KEEP BOTH.
- Generic page owns panel need/class/OS/licensing/overhead.
- FASTPANEL page owns branded workflow, VDSina verified deployment option, FASTPANEL sizing and site management.
- Both pages explicitly hand off to the other instead of pretending to own the entire topic.
- Repeated contextual links are acceptable in these long parent/child pages; no separate "VPS with FASTPANEL" page should be created.

#### VPS sizing for website <-> VPS for WordPress
Verdict: KEEP BOTH; one collision REMEDIATED.
- Generic sizing owns cross-stack resource calculation.
- WordPress owns PHP workers, plugins, WP-Cron, cache and WordPress operations.
- Found exact duplicate FAQ `Is 4 GB RAM enough for WordPress?` on both pages.
- Fixed by retargeting the generic page FAQ to `What does a 4 GB VPS tier fit?` and delegating WordPress-specific interpretation to `VPS for WordPress`.

#### How to host a website on VPS <-> VPS Security Checklist
Verdict: KEEP BOTH.
- Deployment page owns minimum first-access and launch baseline.
- Security page owns deep/recurring hardening.
- Deployment page explicitly says deep SSH/firewall hardening belongs to Security.
- No primary-query collision.

#### VPS for WordPress <-> VPS for WooCommerce
Verdict: KEEP BOTH.
- WordPress owns ordinary CMS/cached workload.
- WooCommerce owns cart/checkout/account/orders/payment callbacks/scheduled actions and write-heavy DB behavior.
- WordPress page explicitly routes stores to WooCommerce.
- Generic repeated section names were contextualized: WordPress/WooCommerce upgrade triggers and current VPS examples now include the page-specific subject.

#### Website migration to VPS <-> How to host a website on VPS
Verdict: KEEP BOTH.
- Migration owns existing live-site inventory, final sync, DNS cutover and rollback.
- Deployment owns a fresh VPS-to-live path.
- Deployment intro explicitly delegates existing production moves to Migration.
- Repeated migration links inside deployment are contextual at cutover/testing points and are not separate intent ownership.

#### Managed vs Unmanaged VPS <-> VPS vs Shared Hosting
Verdict: KEEP BOTH.
- Shared comparison owns whether to stay/optimize/move.
- Managed comparison owns who operates the VPS after the infrastructure choice.
- Shared page hands off responsibility detail to Managed.

#### VPS Security Checklist <-> VPS Backup Strategy <-> VPS Monitoring
Verdict: KEEP ALL THREE.
- Security = hardening.
- Backup = recovery.
- Monitoring = observation/alerts/trends.
- Cross-links are intentional handoffs, not duplicated ownership.

#### VPS sizing for website <-> VPS for Multiple Websites
Verdict: KEEP BOTH.
- Sizing owns aggregate resource calculation.
- Multiple Websites owns isolation, virtual hosts/users/DB separation, client/agency blast radius and split decisions.

### LOW overlap — safe

- Homepage <-> all supporting pages: hub stays summary-level and routes deeper.
- Location <-> Sizing: page itself explicitly separates "where" from "how large".
- Location <-> Monitoring: pre-purchase route choice vs post-deploy measurement/alerting.
- Backup <-> Migration: recovery copies vs cutover execution.
- FASTPANEL <-> Deployment: branded panel route vs broad manual/panel deployment.
- Control Panel <-> Managed: administration UI vs responsibility ownership.

## Exact-query collision audit

Result after remediation: **0 primary-query heading collisions**.

No page uses another core page's exact primary query as a competing H2/H3 owner.

Remaining repeated headings are generic and context-scoped:
- `WordPress` in migration/multi-site notes;
- `Backups` in management/FASTPANEL sub-sections;
- `Server level` / `Site level` inside separate multi-site/monitoring parents.

These do not justify merges or renames.

## Internal-link graph audit

### Hub behavior
Every supporting page links back to the homepage once in the core content path.

Homepage now routes into:
- VPS vs Shared Hosting;
- VPS sizing for website;
- WordPress;
- WooCommerce;
- Multiple Websites;
- control-panel path / FASTPANEL;
- deployment;
- managed vs unmanaged;
- VPS location;
- VPS Security Checklist;
- VPS Backup Strategy;
- VPS Monitoring.

This closes the previous authority-page routing weakness without adding a generic all-pages directory block.

### Orphans
Core orphan pages: **0**.

### Weakest inbound owners before remediation
The weakest content-link owners were:
- VPS vs Shared Hosting;
- VPS Security Checklist;
- VPS Monitoring;
- How to Choose VPS Location.

Shared Hosting already has a direct homepage CTA and correct contextual links from sizing/WordPress.
Security/Backup/Monitoring now also receive direct contextual homepage routing.
Location receives homepage + sizing + migration links, which is sufficient for its narrow decision role.

### Duplicate contextual links
Some long pages link to the same sibling more than once:
- Control Panel -> FASTPANEL;
- FASTPANEL -> Control Panel;
- Deployment -> Migration;
- Monitoring -> Backup/Security.

These were reviewed manually. They occur at materially different decision points and are not treated as a link-farm defect. Do not add sitewide all-to-all body links.

## Broken-link / anchor audit

Generated preview routes for homepage + 14 core pages were checked.

Content-route result:
- no missing core page route detected;
- one broken section anchor found on `How to Choose VPS Location` because Hugo slugified the `+` in `One origin + CDN` as a double hyphen;
- fixed top-of-page anchor to `#global-audience-one-origin--cdn-or-multi-region`.

The preview manifest reference is a shared theme/build artifact issue and not a content-cluster internal-link failure.

## Stale build-state references

Found and fixed:
- FASTPANEL page still called `How to host a website on VPS` a planned guide.
- Deployment page still called Monitoring planned and Backup/Monitoring future pages.

All three now link to the built pages.

## Navigation audit

Guides menu contains the complete core guide set.
Previously the final three items had no explicit weight.
Fixed:
- VPS vs Shared Hosting = weight 10
- Multiple Websites = weight 11
- Control Panel = weight 12

Location remains weight 9. Ordering is now deterministic.

## Cannibalization guardrails

Do not add these standalone pages without a fresh SERP proving a separate owner:
- VPS without Control Panel -> remains merged into deployment;
- VPS Maintenance Checklist -> remains split across Security/Backup/Monitoring;
- VPS for High Traffic Website -> remains inside sizing/concurrency;
- VPS for Agency Websites -> remains inside Multiple Websites;
- website VPS hosting / VPS hosting for websites / VPS for a website -> remain homepage semantic variants;
- VPS with FASTPANEL -> remains semantic variant of FASTPANEL VPS Hosting.

## Final status

Cluster status after remediation:
- HIGH cannibalization: 0 confirmed
- unresolved exact-query collisions: 0
- core orphan pages: 0
- stale planned/future core-page references: 0
- known broken core content anchors: 0 after Location fix
- architecture merges required: 0
- new core page required: 0

Next SEO expansion should not start from phrase collection alone. Any HOLD candidate must first prove a distinct SERP intent and low ownership overlap with this frozen cluster.
