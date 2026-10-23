# Persian localization — complete and live-verified

### Persian complete localization — 2026-10-23 (published and live-verified)

- Owner authorization: add the complete Persian version using English as the reference, page by page, adaptive titles, URLs and all content, all phases in one pass without questions. This supersedes historical Spanish-only, preview-only and one-page-per-turn limits. German and Italian were already complete and were preserved.
- Scope delivered: all 20 English source files, 18 public pages plus localized 404, 4,699 manually reviewed content units and all 507 shared UI/hero entries; all 16 interactive forms and every result branch translated. `fa` / `fa-IR`, native `فارسی`, semantic RTL, native Persian URLs and exact query = Title = H1; homepage `/fa/`, no duplicate keyword-slug home.
- Original Hugo/Hugoplate design retained. Self-hosted Vazirmatn v33.003 with upstream SIL OFL 1.1; Persian-only responsive styles, proper form-label font, LTR code/numeric inputs, 58 semantic bidi wrappers for unchanged Latin table specifications/prices. Mobile and desktop home, tables, forms, code and 404 visually inspected. Original owner hero WebP remains byte-identical (51,196 bytes; SHA-256 `af91640a83f2564d6b91777550e9b9d6435eeca232b876473037c58f95346fb1`); its embedded English lettering is the explicit artwork-preservation exception. Separate CTA SVG and image alt text localized.
- Content/SEO parity: original numbers, USD amounts, dates, code, heading IDs, form IDs/options/algorithms and affiliate URLs/attributes/positions retained. Contact stays noindex and outside the sitemap. Brand/software names, technical specifications and exact external admin-menu paths remain intentional Latin tokens. All 219 pre-existing main page contents are unchanged; recovery retains 159 cached pages and all 13 locale homes. Final merged output: 240 HTML pages, 234 language switchers, 223 sitemap URLs.
- Local verification: complete source/rendered audit, strict locale/site-integrity/recovery/French/German/Italian checks pass. Browser: 18 pages, 90 cases at 320/390/768/1280/1920, 16 forms and 18,736 exhaustive English-compared input states, zero findings. Final typography delta independently passed all 90 geometry/font/bidi cases and preserved every form/script. Project-prefix preview: 19 pages including 404, 380 menu links, 247 language-picker links, 200 article links, 149 assets; noindex, no production canonical/hreflang or analytics, zero findings.
- Publication: source `a5d9d5af28e675a81ac1be260cf26a28da73db5f` -> successful [Prepare Cloudflare static site run 40035524745](https://github.com/agurkin2021-gif/vpsforwebsite/actions/runs/40035524745) -> generated static `b3df10069d38d08a1ac6f1c1220aa370a5d56acf` -> Cloudflare Worker build `e3c3e948-bee6-48a2-9580-3c454bcf9346` success on that generated commit. CI repeats German, Italian and Persian matrices; each passes 18 pages / 90 geometry / 16 forms / 18,736 states with zero failures. No generated output or Worker assets were manually edited.
- Actual live verification: all 18 routes HTTP 200, exact titles/H1, native self canonicals, EN/FA/x-default equivalence, complete body/control parity with final local build; 360 menu links, 313 internal Persian links and 114 anchors checked. Sitemap contains exactly 17 indexable Persian routes. 54 robots checks pass; actual missing Persian URL returns localized HTTP 404. Owner hero bytes match. Live Chromium: 36 mobile/desktop geometry cases, all 16 forms / 18,736 English-compared states, language roundtrips, zero findings. The final Persian-only theme-font override also passes a separate live 90-case audit including every heading and form label; English content and calculators are unchanged. Live completion: `2026-10-23T22:51:22.779Z`.
- Evidence is retained locally in the isolated `vpsforwebsite-persian/qa-output/`: `persian-audit.json`, `persian-browser/report.json`, `persian-release-geometry/report.json`, `persian-preview.json`, `existing-locale-regression.json`, `release-delta.json`, `deployment-evidence.json`, `live-seo/`, `live-browser/`, `live-final-fonts/`, `font-release-delta.json`, `visual/`. Persistent source/route and RTL reference notes: `research/persian-localization-2026-10-23.md`. Translation, publication and live gates are complete; no requested Persian pages remain pending.

## Route ownership


| English source | Persian query / Title / H1 | URL |

| --- | --- | --- |

| `_index.md` | سرور مجازی برای سایت | `/fa/` |

| `about/_index.md` | درباره ما | `/fa/درباره-ما/` |

| `contact/_index.md` | تماس با ما | `/fa/تماس-با-ما/` |

| `privacy-policy.md` | سیاست حفظ حریم خصوصی | `/fa/سیاست-حفظ-حریم-خصوصی/` |

| `vps-sizing-for-website.md` | تعیین منابع سرور مجازی برای سایت | `/fa/تعیین-منابع-سرور-مجازی-برای-سایت/` |

| `website-migration-to-vps.md` | انتقال سایت به سرور مجازی | `/fa/انتقال-سایت-به-سرور-مجازی/` |

| `managed-vs-unmanaged-vps.md` | سرور مجازی مدیریت شده یا مدیریت نشده | `/fa/سرور-مجازی-مدیریت-شده-یا-مدیریت-نشده/` |

| `vps-for-wordpress.md` | سرور مجازی برای وردپرس | `/fa/سرور-مجازی-برای-وردپرس/` |

| `vps-for-woocommerce.md` | سرور مجازی برای ووکامرس | `/fa/سرور-مجازی-برای-ووکامرس/` |

| `vps-vs-shared-hosting.md` | سرور مجازی یا هاست اشتراکی | `/fa/سرور-مجازی-یا-هاست-اشتراکی/` |

| `vps-for-multiple-websites.md` | سرور مجازی برای چند سایت | `/fa/سرور-مجازی-برای-چند-سایت/` |

| `vps-with-control-panel.md` | سرور مجازی با کنترل پنل | `/fa/سرور-مجازی-با-کنترل-پنل/` |

| `fastpanel-vps-hosting.md` | میزبانی سرور مجازی با FASTPANEL | `/fa/میزبانی-سرور-مجازی-با-fastpanel/` |

| `how-to-host-a-website-on-vps.md` | نحوه میزبانی سایت روی سرور مجازی | `/fa/نحوه-میزبانی-سایت-روی-سرور-مجازی/` |

| `vps-security-checklist.md` | چک لیست امنیت سرور مجازی | `/fa/چک-لیست-امنیت-سرور-مجازی/` |

| `vps-backup-strategy.md` | استراتژی پشتیبان گیری سرور مجازی | `/fa/استراتژی-پشتیبان-گیری-سرور-مجازی/` |

| `vps-monitoring.md` | مانیتورینگ سرور مجازی | `/fa/مانیتورینگ-سرور-مجازی/` |

| `how-to-choose-vps-location.md` | نحوه انتخاب موقعیت سرور مجازی | `/fa/نحوه-انتخاب-موقعیت-سرور-مجازی/` |


## RTL implementation references


- [HTML dir semantics](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Global_attributes/dir).

- [Vazirmatn v33.003](https://github.com/rastikerdar/vazirmatn/tree/v33.003), SIL Open Font License 1.1. Self-hosted, Persian-only; no runtime font service.
