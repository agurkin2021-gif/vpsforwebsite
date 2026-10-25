# Indonesian adaptation: one complete page per release

The owner's current request is careful Indonesian commercial localization, with natural titles and URLs, full page-by-page review and responsive verification. Indonesian already has 18 recovered pages; this is a quality and completeness pass over that existing version, not a new duplicate language or a bulk rewrite. Source stays in `recovered-public/id/` until an explicit Hugo migration is needed. Do not remove functioning existing URLs.

For each page: compare the entire English reference, review Indonesian meaning and terminology, preserve section/anchor/form/affiliate parity, fix responsive defects within the Indonesian scope, publish from main, wait for the generated static commit and its successful Cloudflare build, then verify the ordinary live URL before starting the next page.

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
- Local and live publication evidence will be recorded here after the checks finish. Do not describe the remaining 17 pages as fully proofread from this initial inventory alone.

## Sequential queue

| Page | Existing route | Status |
| --- | --- | --- |
| VPS untuk Website | `/id/` | In review; publication pending |
| VPS untuk WordPress | `/id/vps-untuk-wordpress/` | Next |
| VPS untuk WooCommerce | `/id/vps-untuk-woocommerce/` | Pending |
| Menentukan Spesifikasi VPS untuk Website | `/id/menentukan-spesifikasi-vps/` | Pending title/slug review |
| VPS vs Shared Hosting | `/id/vps-vs-shared-hosting/` | Pending |
| VPS untuk Banyak Website | `/id/vps-untuk-banyak-website/` | Pending |
| Hosting VPS dengan FASTPANEL | `/id/hosting-vps-fastpanel/` | Pending title/slug review |
| VPS dengan Panel Kontrol | `/id/vps-dengan-panel-kontrol/` | Pending |
| VPS Managed vs Unmanaged | `/id/vps-managed-vs-unmanaged/` | Pending |
| Cara Hosting Website di VPS | `/id/cara-hosting-website-di-vps/` | Pending |
| Migrasi Website ke VPS | `/id/migrasi-website-ke-vps/` | Pending |
| Checklist Keamanan VPS | `/id/checklist-keamanan-vps/` | Pending |
| Strategi Backup VPS | `/id/strategi-backup-vps/` | Pending |
| Monitoring VPS | `/id/monitoring-vps/` | Pending |
| Cara Memilih Lokasi VPS | `/id/cara-memilih-lokasi-vps/` | Pending |
| Tentang VPSforWebsite.com | `/id/tentang/` | Pending full English-source body review |
| Kontak | `/id/kontak/` | Pending; preserve noindex |
| Kebijakan Privasi | `/id/kebijakan-privasi/` | Pending |

The initial inventory confirms matching rendered H2/H3/list/table/control counts on all 18 pages. Structural parity is not evidence of completed linguistic review. About requires the full English Markdown source as reference because its existing English public template omits body sections.
