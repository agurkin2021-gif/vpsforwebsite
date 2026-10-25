# Turkish page-by-page localization

### Turkish localization — 2026-10-25 (validated locally; publication pending)

- Owner requested Turkish (`tr`) with every page individually adapted: 20 English source files, 18 public pages, native 404, 4,699 content units, 507 shared UI/hero entries and 16 interactive forms. Homepage query = Title = H1 is `Web sitesi için VPS`, canonical `/tr/`. All other titles match their native intent and ASCII-transliterated Turkish URL phrase; inventory is in `research/turkish-localization-2026-10-25.md` and `data/turkish_review.json`.
- Each complete page was translated and reviewed against English. Article depth, commands, technical values, USD prices/check dates, anchors, form inputs/options/algorithms and affiliate destinations/attributes/placement are preserved. About renders its complete source. Contact remains noindex, excluded from the sitemap, without invented contact details or forms. No Turkey data-center inventory, lira pricing, market ranking or traffic guarantees were added. Internal editorial planning notes in multisite, panel, FASTPANEL and deployment articles became reader-facing explanations. Native 7/24 is equivalent to English 24/7.
- Complete local Chromium validation passed: all 18 pages at 320, 360, 390, 430, 768, 1024, 1280 and 1920 px (144 geometry cases); all 16 forms and 18,736 input states compared against English branch outcomes/numbers; actual pointer submissions; all equivalent EN/TR roundtrips. Zero findings. Screenshots were visually reviewed, including long desktop titles, mobile homepage, CTA, sizing tables and localized 404.
- Visual review identified cramped four/five-column sizing tables. Both now use the existing keyboard-focusable table-scroll shortcode, native labels/hints and scoped CSS. A separate final-build geometry run repeated all 144 cases and 18 roundtrips with zero findings. Every rendered script is byte-identical before/after this table-only change, preserving the completed exhaustive form evidence.
- Final production-like static validation passed all 20 Turkish source files, 18 rendered pages and 16 forms, including title/H1/slug identity, canonical/hreflang, full structure, command examples, prices, links and affiliate parity. DE/IT/FA/AR/JA static regression audits each passed all 18 pages. Recovery: 159 preserved cached HTML pages, 16 locale homes, 288 selectors, zero errors. Integrity: 297 HTML pages, 420 local targets, 116 stylesheets, zero errors; three integrity unit tests passed. Sitemap: 274 URLs, 17 Turkish indexable pages.
- Preview-prefix build under `https://preview.example.test/preview/` passed all 18 Turkish pages and 155 targets, including assets, canonical, hreflang and navigation. This is a local fixture, not a published preview.
- Original Inter/Fraunces design families now have Turkish-complete local subsets (43,944 / 31,380 bytes; 229 / 222 glyphs), pinned upstream hashes and SIL OFL licenses. `scripts/build-turkish-fonts.py` verifies source hashes and Turkish coverage and generates the outlined native CTA. Only Turkish uses these font variants; font partial cache varies by language. Owner hero remains unchanged: SHA-256 `af91640a83f2564d6b91777550e9b9d6435eeca232b876473037c58f95346fb1`.
- `data/turkish_review.json` seals reviewed source/UI/font/CTA hashes. CI adds Turkish static and complete browser gates plus seven-day evidence artifacts, retaining existing DE/IT/FA/AR/JA gates. Local helpers and QA output are excluded from source commits.
- Publication is authorized through main → Prepare generated static commit → Cloudflare Worker. Baseline `beddb96fc3fd406c1122930dfc6e7b2a0e81c65e`; isolated checkout `vpsforwebsite-turkish`. Source publication, CI/generated output, Cloudflare readiness and ordinary live verification are pending. Never edit generated output or dashboard assets manually, or advance main during an active Prepare run.

## Page intent and URL ownership

| English source | Turkish query / Title / H1 | URL |
| --- | --- | --- |
| `_index.md` | Web sitesi için VPS | `/tr/` |
| `vps-for-wordpress.md` | WordPress için VPS | `/tr/wordpress-icin-vps/` |
| `vps-for-woocommerce.md` | WooCommerce için VPS | `/tr/woocommerce-icin-vps/` |
| `vps-sizing-for-website.md` | Web sitesi için VPS kaynak seçimi | `/tr/web-sitesi-icin-vps-kaynak-secimi/` |
| `vps-vs-shared-hosting.md` | VPS ve paylaşımlı hosting karşılaştırması | `/tr/vps-ve-paylasimli-hosting-karsilastirmasi/` |
| `vps-for-multiple-websites.md` | Birden fazla web sitesi için VPS | `/tr/birden-fazla-web-sitesi-icin-vps/` |
| `vps-with-control-panel.md` | Kontrol panelli VPS | `/tr/kontrol-panelli-vps/` |
| `managed-vs-unmanaged-vps.md` | Yönetilen ve yönetilmeyen VPS karşılaştırması | `/tr/yonetilen-ve-yonetilmeyen-vps-karsilastirmasi/` |
| `fastpanel-vps-hosting.md` | FASTPANEL ile VPS hosting | `/tr/fastpanel-ile-vps-hosting/` |
| `how-to-host-a-website-on-vps.md` | VPS üzerinde web sitesi yayınlama | `/tr/vps-uzerinde-web-sitesi-yayinlama/` |
| `website-migration-to-vps.md` | Web sitesini VPS sunucuya taşıma | `/tr/web-sitesini-vps-sunucuya-tasima/` |
| `vps-security-checklist.md` | VPS güvenlik kontrol listesi | `/tr/vps-guvenlik-kontrol-listesi/` |
| `vps-backup-strategy.md` | VPS yedekleme stratejisi | `/tr/vps-yedekleme-stratejisi/` |
| `vps-monitoring.md` | VPS izleme | `/tr/vps-izleme/` |
| `how-to-choose-vps-location.md` | VPS sunucu konumu seçimi | `/tr/vps-sunucu-konumu-secimi/` |
| `about/_index.md` | Hakkımızda | `/tr/hakkimizda/` |
| `contact/_index.md` | İletişim | `/tr/iletisim/` |
| `privacy-policy.md` | Gizlilik politikası | `/tr/gizlilik-politikasi/` |
