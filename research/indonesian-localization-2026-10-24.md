# Indonesian adaptation: individual page review and verification

The owner's current request is careful Indonesian commercial localization, with natural titles and URLs, full page-by-page review and responsive verification. Indonesian already has 18 recovered pages; this is a quality and completeness pass over that existing version, not a new duplicate language or a bulk rewrite. Source stays in `recovered-public/id/` until an explicit Hugo migration is needed. Do not remove functioning existing URLs.

For each page: individually review Indonesian meaning and terminology against the English reference and primary technical documentation; preserve section/anchor/form/affiliate parity and verify responsive behavior. Review the next page while prior publication checks run. Only checked sources are published from main; wait for generated static and Cloudflare success and verify every ordinary live URL. Release grouping does not replace individual editorial review.

## Language and search intent

- Homepage query = Title = H1: **VPS untuk Website**, canonical `/id/`. This is the purchase/evaluation intent for website hosting. Do not substitute `VPS Indonesia`, which can imply a server physically located in Indonesia, or add an unverified `terbaik`/`termurah` claim. No keyword-volume or ranking claims have been measured.
- Indonesian industry usage was checked against [Rumahweb VPS](https://www.rumahweb.com/vps-indonesia/) and [Biznet Gio NEO Lite](https://www.biznetgio.com/product/neo-lite), 24 October 2026. Retain recognizable technical terms where useful: VPS, hosting, WordPress, WooCommerce, PHP worker, cache, backup, runtime, database, managed/unmanaged. Explain operational concepts in ordinary Indonesian rather than translating their English words literally.
- Use `spesifikasi` or `kapasitas` for server sizing, `pengelolaan` for administration, `kendala migrasi` for blockers, `seleksi penyedia` for shortlist, and `ketentuan pemesanan` for order terms. Use consistent polite `Anda` language and clear buying actions.
- Prices remain in USD, with Indonesian decimal commas and an explicit currency note. The four homepage Standard configurations, daily/monthly amounts, transfer allowances and public-port speed were rechecked on [VDSina Standard](https://www.vdsina.com/pricing/standard) on 24 October 2026. The published last-checked date may therefore advance on this page. Do not infer Indonesian datacenters or convert prices into a guaranteed rupiah amount.

## Page 1: homepage

- Reviewed all 477 visible main-content text fragments, the seven decision sections, four configuration cards, 13 FAQ answers, six select controls/15 options, five calculator outcome branches and accessibility labels.
- Refined 125 text-node occurrences and two result messages. Replaced literal or misleading phrasing around sizing, provider selection, management responsibilities, migration blockers, workload separation and recovery. Preserved all original explanations and decision paths. Title/H1 and `/id/` stay unchanged; description/Open Graph/JSON-LD descriptions now use a concise buying-oriented Indonesian summary.
- All original anchor IDs, links, sponsor attributes/placements, technical specifications, calculator controls/values/logic and owner image remain intact. The homepage's 9 H2, 6 H3, 40 list items, 13 FAQ details and one form are preserved.
- Browser baseline exposed clipped plan-card headings, a fixed-width CTA and narrow-screen section overflow; document scrollWidth alone hid the defect. `static/css/id-home-responsive.v1.css` scopes the known corrective pattern to the Indonesian homepage at widths below 768 px and is linked only by that page.
- Homepage published: source `323049765d75134cb5c78cc0671a461f4abee7c3` -> successful Prepare static run `40152556847` -> generated `96cdfb180175f4dfbd32bd6bced611c7d8ba1554` -> successful Cloudflare Workers check. Ordinary live `/id/`: 8 viewport widths, 216 English-compared calculator states, pointer submission and language roundtrip passed without findings (2026-10-25T02:02Z UTC / 24 October local). Live scroll checks show no vertical overlap of calculator, plan cards or FAQ; screenshot-only clipping was lazy content-visibility measurement, not a fixed height in production.

## Page 2: WordPress

- Query/Title/H1 `VPS untuk WordPress`, `/id/vps-untuk-wordpress/`: existing title and slug match natural Indonesian hosting-selection intent. Retained without unnecessary redirect.
- Reviewed all 418 fragments and compared the complete English page. Refined 146 text-node occurrences and three calculator messages. Kept all four tables, 10 FAQ answers, seven select controls, 20 options, links/IDs and decision logic. Corrected literal phrasing around long-running tasks, persistent cache, worker concurrency, headroom, deployment and management. Clear purchase CTA: `Lihat pilihan paket VPS WordPress`.
- Primary technical checks: [WordPress requirements](https://wordpress.org/about/requirements/), [caching](https://developer.wordpress.org/advanced-administration/performance/cache/), [object cache](https://developer.wordpress.org/reference/classes/wp_object_cache/), [system scheduler](https://developer.wordpress.org/plugins/cron/hooking-wp-cron-into-the-system-task-scheduler/), and [VDSina Standard](https://www.vdsina.com/pricing/standard). Specifications and logic preserved; reviewed price/date fields advanced, explicit USD currency note added.
- Local Chromium: 8 viewport widths, 1,296 exhaustive English-compared states, actual submit and EN↔ID roundtrip, zero findings. Title does not collide with the adjacent illustration; screenshots reviewed. Published and live-verified: source d4a1486df23801d15480f09ff161bc70c328f0e5, generated 17b931b71c6ddda1d79f2f4013328ef93201c163; full live browser checks passed.

## Pages 3–7: individually reviewed guides

### /id/vps-untuk-woocommerce/

- Reviewed 458 visible fragments; refined 129 text-node occurrences and 3 calculator messages. Checkout/account concurrency, cache exclusions, payment callbacks, scheduled actions, HPOS and transaction-aware migration. Official WooCommerce requirements/cache/HPOS/Action Scheduler and historic scaling baseline checked.
- Eight viewport widths, 7776 English-compared input states, all final checks passed. Main structure, controls, numbers, hrefs and anchors retained.

### /id/menentukan-spesifikasi-vps/

- Reviewed 374 visible fragments; refined 93 text-node occurrences and 2 calculator messages. Query/Title/H1 shortened to Menentukan Spesifikasi VPS, matching the existing slug without redirect. Clarified resource budgets, CloudLinux limits, worker concurrency and total cost. Both calculators preserve their algorithms; QA normalizes Indonesian decimal comma 2,4 against English 2.4, without dropping numeric assertions.
- Eight viewport widths, 740 English-compared input states, all final checks passed. Main structure, controls, numbers, hrefs and anchors retained.

### /id/vps-vs-shared-hosting/

- Reviewed 381 visible fragments; refined 90 text-node occurrences and 0 calculator messages. Natural purchase comparison: management duties, actual hosting limits, root/runtime needs, bundled services, ongoing costs and migration readiness. Six decision outcomes unchanged.
- Eight viewport widths, 216 English-compared input states, all final checks passed. Main structure, controls, numbers, hrefs and anchors retained.

### /id/vps-untuk-banyak-website/

- Reviewed 409 visible fragments; refined 89 text-node occurrences and 1 calculator messages. Clarified shared outage risk, per-client isolation, combined peak usage and per-site recovery. Replaced an exposed internal SEO-planning aside with useful agency/hosting guidance. One calculator suffix clarified; all branches preserved.
- Eight viewport widths, 576 English-compared input states, all final checks passed. Main structure, controls, numbers, hrefs and anchors retained.

### /id/hosting-vps-fastpanel/

- Reviewed 318 visible fragments; refined 82 text-node occurrences and 0 calculator messages. Query/Title/H1 now Hosting VPS FASTPANEL, matching the existing slug. Clarified clean OS installation, panel minimum versus production capacity, setup and operations. Verified Standard free license and paid Extended features including Node.js; accurate licensing nuance added from official documentation.
- Eight viewport widths, 36 English-compared input states, all final checks passed. Main structure, controls, numbers, hrefs and anchors retained.

Primary additional sources: [WooCommerce scaling baseline](https://developer.woocommerce.com/2024/08/22/scaling-with-woocommerce/), [server requirements](https://woocommerce.com/document/server-requirements/), [cache exclusions](https://developer.woocommerce.com/docs/best-practices/performance/configuring-caching-plugins/), [HPOS](https://developer.woocommerce.com/docs/features/orders/high-performance-order-storage/), [scheduled actions](https://woocommerce.com/document/understanding-the-woocommerce-system-status-report/scheduled-actions/), [FASTPANEL installation](https://kb.fastpanel.direct/quick_start/how-to-install-fastpanel/), [free Standard license](https://kb.fastpanel.direct/quick_start/license-order/), [Extended licenses](https://kb.fastpanel.direct/licenses/intro/). WooCommerce docs scaling URL failed through the web extractor but direct HTTPS returned 200; original working reference retained.

## Pages 8–18: individual completion review

### /id/vps-dengan-panel-kontrol/

- Reviewed 422 existing visible fragments, with any missing body restored explicitly. Panel choice, license costs, server dashboard versus website panel, operating duties and practical buying criteria.
- Eight viewport cases, 288 English-compared form states, final local checks passed.

### /id/vps-managed-vs-unmanaged/

- Reviewed 439 existing visible fragments, with any missing body restored explicitly. Management scope, contract responsibilities, recovery ownership and total operating cost.
- Eight viewport cases, 576 English-compared form states, final local checks passed.

### /id/cara-hosting-website-di-vps/

- Reviewed 519 existing visible fragments, with any missing body restored explicitly. Deployment sequence, SSH, file permissions, DNS, TLS, services and reboot checks. Every code block preserved.
- Eight viewport cases, 72 English-compared form states, final local checks passed.

### /id/migrasi-website-ke-vps/

- Reviewed 378 existing visible fragments, with any missing body restored explicitly. Final writes, private testing, DNS, email records, serialized WordPress data, rollback synchronization and SEO continuity.
- Eight viewport cases, 2304 English-compared form states, final local checks passed.

### /id/checklist-keamanan-vps/

- Reviewed 439 existing visible fragments, with any missing body restored explicitly. SSH recovery sequence, public ports, least privilege, credentials and incident recovery. Also translated 37 English labels injected by the visual-diagram script; no algorithm changes.
- Eight viewport cases, 512 English-compared form states, final local checks passed.

### /id/strategi-backup-vps/

- Reviewed 500 existing visible fragments, with any missing body restored explicitly. RPO versus RTO, database consistency, off-server copies, encryption keys, retention, restore drills and correct 3-2-1 definition.
- Eight viewport cases, 2304 English-compared form states, final local checks passed.

### /id/monitoring-vps/

- Reviewed 514 existing visible fragments, with any missing body restored explicitly. External checks, historical metrics, application health, useful alert thresholds, independent notifications and capacity decisions.
- Eight viewport cases, 1536 English-compared form states, final local checks passed.

### /id/cara-memilih-lokasi-vps/

- Reviewed 501 existing visible fragments, with any missing body restored explicitly. User and dependency locations, routing tests, dynamic requests, CDN, geographical labels and real placement constraints. No Indonesian datacenter claim added.
- Eight viewport cases, 288 English-compared form states, final local checks passed.

### /id/tentang/

- Reviewed 21 existing visible fragments, with any missing body restored explicitly. Restored seven missing editorial/disclosure sections from content/english/about/_index.md. Preserved historical English review date. Title/H1 Tentang matches existing slug. Scoped article-body CSS fixes alignment and heading contrast in the recovered stylesheet.
- Eight viewport cases, 0 English-compared form states, final local checks passed.

### /id/kontak/

- Reviewed 22 existing visible fragments, with any missing body restored explicitly. Restored the two missing contact-policy paragraphs from English source. Removed obsolete preview language. Preserved noindex and no public form; no contact channel invented. Verified EN/ID contact switcher pair fixed without adding SEO alternates.
- Eight viewport cases, 0 English-compared form states, final local checks passed.

### /id/kebijakan-privasi/

- Reviewed 47 existing visible fragments, with any missing body restored explicitly. Reviewed against actual delayed GA4 implementation, English policy and Google policy. Refined browser/device and cookie descriptions; translated remaining schema author description. No consent features or retention promises invented.
- Eight viewport cases, 0 English-compared form states, final local checks passed.

Additional primary references: [Ubuntu OpenSSH](https://ubuntu.com/server/docs/how-to/security/openssh-server/), [Ubuntu firewall](https://ubuntu.com/server/docs/how-to/security/firewalls/), [CISA 3-2-1 backup rule](https://www.cisa.gov/sites/default/files/publications/data_backup_options.pdf), [Prometheus Node Exporter](https://prometheus.io/docs/guides/node-exporter/), [Alertmanager](https://prometheus.io/docs/alerting/latest/alertmanager/), [Uptime Kuma](https://github.com/louislam/uptime-kuma), [Google international sites](https://developers.google.com/search/docs/specialty/international/managing-multi-regional-sites), [Google privacy policy](https://policies.google.com/privacy). Full articles were manually reviewed; scripts apply reviewed per-page text edits and assert unchanged links, IDs, form controls, code blocks and calculator logic. About/Contact body restoration is the documented structural exception.

Re-run browser checks with Playwright and Chromium installed: `node scripts/qa-indonesian.cjs cloudflare-public research/indonesian-routes.json qa-output/indonesian`. Default widths: 320, 360, 390, 430, 768, 1024, 1280, 1920. Set `CHROME_PATH` if using installed Chrome; set `INDONESIAN_QA_LIVE=1` for ordinary production URLs.

## Final production verification

Final release: source `bcfbe0603cf5162ddd265fbff66116c32a877c58` -> Prepare run `40155389753` successful -> generated `891cfd8a5e70267a6b20f72f6512826565423473` -> Cloudflare Workers success. Full live browser run completed 2026-10-25T02:54:22.574Z: **18 pages, 144 viewport cases, 16 forms, 18,736 input states, zero findings**, with actual form submissions and EN/ID roundtrips for every page. All ordinary URLs returned 200; full main text and metadata match source. Seventeen indexable routes are in the sitemap; noindex Contact is excluded. Structured evidence is in `indonesian-validation-2026-10-24.json`.

## Completed page inventory

| Page | Existing route | Status |
| --- | --- | --- |
| VPS untuk Website | `/id/` | Published and live-verified |
| VPS untuk WordPress | `/id/vps-untuk-wordpress/` | Published and live-verified |
| VPS untuk WooCommerce | `/id/vps-untuk-woocommerce/` | Published and live-verified |
| Menentukan Spesifikasi VPS | `/id/menentukan-spesifikasi-vps/` | Published and live-verified |
| VPS vs Shared Hosting | `/id/vps-vs-shared-hosting/` | Published and live-verified |
| VPS untuk Banyak Website | `/id/vps-untuk-banyak-website/` | Published and live-verified |
| Hosting VPS FASTPANEL | `/id/hosting-vps-fastpanel/` | Published and live-verified |
| VPS dengan Panel Kontrol | `/id/vps-dengan-panel-kontrol/` | Published and live-verified |
| VPS Managed vs Unmanaged | `/id/vps-managed-vs-unmanaged/` | Published and live-verified |
| Cara Hosting Website di VPS | `/id/cara-hosting-website-di-vps/` | Published and live-verified |
| Migrasi Website ke VPS | `/id/migrasi-website-ke-vps/` | Published and live-verified |
| Checklist Keamanan VPS | `/id/checklist-keamanan-vps/` | Published and live-verified |
| Strategi Backup VPS | `/id/strategi-backup-vps/` | Published and live-verified |
| Monitoring VPS | `/id/monitoring-vps/` | Published and live-verified |
| Cara Memilih Lokasi VPS | `/id/cara-memilih-lokasi-vps/` | Published and live-verified |
| Tentang | `/id/tentang/` | Published and live-verified |
| Kontak | `/id/kontak/` | Published and live-verified |
| Kebijakan Privasi | `/id/kebijakan-privasi/` | Published and live-verified |

The initial inventory confirms matching rendered H2/H3/list/table/control counts on all 18 pages. Structural parity is not evidence of completed linguistic review. About requires the full English Markdown source as reference because its existing English public template omits body sections.
