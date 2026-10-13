# Powerful uncovered intents — VPS sizing for website
Date: 2026-10-12
Status: second discovery pass; candidate gaps, not proof of zero competing coverage or search volume.

## Evidence
- cPanel official hardware requirements: https://support.cpanel.net/hc/en-us/articles/360054297474-What-Are-the-Hardware-Requirements-For-My-Server — per-request cost × concurrency + base services; hardware minimum is not production sizing.
- cPanel upgrade sizing: https://support.cpanel.net/hc/en-us/articles/1500005235562-How-to-determine-how-much-RAM-CPU-and-DISK-resources-I-should-add-when-upgrading-a-server — CPU/iowait, memory/swap/OOM, disk I/O, network, time-series growth.
- cPanel UI: https://docs.cpanel.net/cpanel/the-cpanel-interface/the-cpanel-interface/126/ — CPU, memory, entry-process counters when CloudLinux enabled.
- VPSMetrics: https://vpsmetrics.com/tools/vps-advisor — cache-aware workload estimator, requires login for results.
- ServerCalc: https://servercalc.com/vps-for/website/ — three tiers, provider matching, price filters; generic use-case.
- Web server sizing calculator: https://thehomeserverblog.com/web-server-sizing-calculator/ — detailed no-login CPU, worker, memory, transfer and node count calculator. This disproves any broad claim that free calculators do not exist.
- PHP worker calculator: https://www.paidhosting.com/php-worker-calculator/ — worker and caching model.
- Eka Sunucu: https://www.ekasunucu.com/en/website-cpu-ram-vps-requirements — technically substantive sizing guide.

## Ranked candidate opportunities
P1 — Shared-hosting-to-VPS translator: accept cPanel/CloudLinux fault events, peak CPU, physical memory, entry processes, I/O and actual workload; explain optimize-first vs VPS and produce tier plus uncertainty. More distinctive than generic visitor calculator. Constraint: these metrics are often account limits, not direct equivalent VPS CPU/RAM consumption; do not convert them mechanically.
P1 — Evidence-based RAM and worker budget: estimate OS + panel + DB + app workers + queue + headroom; show where actual measurements should replace presets; warn about RSS double counting.
P1 — Confidence-aware recommendation: label input quality (measured vs estimated), assumptions, best/worst-case, reason for selected tier, when recommendation fails; avoids false precision.
P1 — Optimize-first diagnosis: differentiate memory exhaustion, PHP queue, slow DB, bot attacks, cache misses and storage latency before selling a larger VPS.
P2 — Peak-event planner: flash sales, campaigns, product launches; estimate origin dynamic RPS and worker/DB bottlenecks, fail-safe thresholds and temporary scaling.
P2 — VPS true cost per website: VPS + panel/license + backups + admin + monitoring + email; meaningful commercial buyer intent but likely deserves a later dedicated page.
P2 — One VPS vs split architecture: website + database + workers + staging; separate failure domain, availability and scaling. Existing project homepage covers it briefly; consider future standalone planner after demand/overlap validation.
P2 — Migration risk-aware sizing: temporary disk for exports, compatibility and parallel cutover; detailed migration belongs to /website-migration-to-vps/.
HOLD — Generic PHP worker calculator and generic web-server sizing calculator: strong existing competitors; integrate relevant elements rather than claim novelty.
HOLD — 'VPS for 100k visitors' landing pages: misleading capacity claims and cannibalization risk.

## On-page consequence
The primary page /vps-sizing-for-website/ should own all resource calculation and the cPanel translator as its flagship diagnostic module. No separate indexable calculator URL until Google SERP overlap and query volume support it. Link to homepage and existing specific workloads.
Do not claim search volumes or top-10 ranking positions: neither was verified in this pass.
