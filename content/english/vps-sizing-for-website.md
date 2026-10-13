---
title: "VPS sizing for website"
description: "VPS sizing for website: calculate CPU, RAM and storage from real workload, shared-hosting limits, PHP workers, database demand and peak traffic."
image: "https://raw.githubusercontent.com/zeon-studio/hugoplate/4acb4365d7a86703357a9f216db149f55210fa09/exampleSite/assets/images/banner.png"
---

VPS sizing for a website should start with the workload that reaches the origin server, not with a monthly visitor count. Cacheability, simultaneous dynamic requests, PHP or application workers, database activity, background jobs, control-panel overhead and storage growth determine how much CPU, RAM and disk the website actually needs.

For the broader purchase decision, see [VPS for website]({{< relref "_index.md" >}}).

[Jump to RAM sizing](#ram-budget) · [Shared-hosting diagnostic](#shared-hosting-to-vps-diagnostic) · [Plan match](#match-the-result-to-a-vps) · [FAQ](#faq)

## Quick sizing answer

These current VDSina Standard configurations are useful reference tiers, but the workload should choose the tier — not the other way around. Provider values below were checked on October 13, 2026.

| Website workload | Starting VPS example | What to verify |
|---|---:|---|
| Very light site, test environment, aggressively cached project | 1 vCPU / 1 GB RAM / 10 GB — $0.07/day, 1 TB/month transfer | Memory headroom, database size, swap use |
| Small site or lean CMS | 1 vCPU / 2 GB RAM / 40 GB — $0.50/day, 32 TB/month transfer | PHP workers, panel overhead, database memory |
| Business site or typical dynamic WordPress workload | 2 vCPU / 4 GB RAM / 80 GB — $0.67/day, 32 TB/month transfer | Uncached concurrency, cron jobs, database latency |
| Heavier dynamic site, larger database or several active sites | 4 vCPU / 8 GB RAM / 160 GB — $1.34/day, 32 TB/month transfer | Sustained CPU, worker memory, peak overlap |

These are sizing directions, not traffic guarantees. Two websites with the same visitor count can require very different servers. Prices, transfer allowances and other provider terms can change, so verify the current offer before ordering.

<p>
  <a class="btn btn-primary" href="https://www.vdsina.com/?partner=ni8gzrvz75" target="_blank" rel="sponsored nofollow noopener">Check current VPS configurations</a>
</p>
<p><small>Affiliate disclosure: this site may earn a commission if you order through this partner link. The sizing recommendation is based on workload, not commission.</small></p>

## The sizing model: reserve resources before counting traffic

A useful VPS budget separates the server into resource consumers.

### RAM budget

Total RAM must cover:

1. the operating system and system services;
2. the web server or reverse proxy;
3. PHP-FPM, Node.js, Python or another application runtime;
4. the database;
5. cache services such as Redis when used;
6. the control panel and its services;
7. monitoring, security and backup processes;
8. concurrent application workers;
9. safety headroom for bursts, deployments and maintenance.

Do not treat a CMS memory limit as the server's RAM requirement. A 256 MB PHP memory limit does not mean that a 1 GB VPS can safely run four simultaneous 256 MB PHP processes plus Linux, the database and every other service.

A practical model is:

**required RAM = baseline services + database working memory + concurrent worker memory + background-job memory + headroom**

Measure the real processes whenever possible. Estimates are useful for choosing a starting tier; measurements decide whether the tier is actually sufficient.

### RAM budget estimator

Use this estimator to expose the assumptions instead of guessing from visitor count. It estimates the RAM tier only; CPU, storage and I/O still need separate validation. Enter your own measurements; the placeholders mirror the worked example below and are not universal defaults.

<div class="rounded-2xl bg-light p-6 dark:bg-darkmode-light">
<form id="ram-budget-estimator">
  <div class="mb-6">
    <label for="ram-baseline" class="form-label">Baseline OS + web services, MB</label>
    <input id="ram-baseline" class="form-input" type="number" min="0" step="1" placeholder="450" required>
  </div>
  <div class="mb-6">
    <label for="ram-database" class="form-label">Database working memory, MB</label>
    <input id="ram-database" class="form-input" type="number" min="0" step="1" placeholder="500" required>
  </div>
  <div class="mb-6">
    <label for="ram-workers" class="form-label">Concurrent application workers</label>
    <input id="ram-workers" class="form-input" type="number" min="0" step="1" placeholder="6" required>
  </div>
  <div class="mb-6">
    <label for="ram-worker-mb" class="form-label">Average memory per worker, MB</label>
    <input id="ram-worker-mb" class="form-input" type="number" min="0" step="1" placeholder="120" required>
  </div>
  <div class="mb-6">
    <label for="ram-background" class="form-label">Panel, cache and background jobs, MB</label>
    <input id="ram-background" class="form-input" type="number" min="0" step="1" placeholder="300" required>
  </div>
  <div class="mb-6">
    <label for="ram-headroom" class="form-label">Safety headroom, %</label>
    <input id="ram-headroom" class="form-input" type="number" min="0" max="100" step="1" value="25" required>
  </div>
  <button class="btn btn-primary" type="submit">Estimate RAM tier</button>
</form>
<p id="ram-budget-result" class="mt-6 rounded border border-border p-4 dark:border-darkmode-border" role="status" aria-live="polite">Enter your measurements and calculate the budget.</p>
</div>

<script>
document.addEventListener("DOMContentLoaded", function () {
  var form = document.getElementById("ram-budget-estimator");
  if (!form) return;
  form.addEventListener("submit", function (event) {
    event.preventDefault();
    function number(id) {
      var value = Number(document.getElementById(id).value);
      return Number.isFinite(value) && value >= 0 ? value : 0;
    }
    var baseline = number("ram-baseline");
    var database = number("ram-database");
    var workers = number("ram-workers");
    var workerMb = number("ram-worker-mb");
    var background = number("ram-background");
    var headroom = number("ram-headroom");
    var subtotal = baseline + database + (workers * workerMb) + background;
    var required = subtotal * (1 + headroom / 100);
    var requiredGb = Math.round((required / 1024) * 10) / 10;
    var tier;
    if (required <= 1024) tier = "1 GB RAM";
    else if (required <= 2048) tier = "2 GB RAM";
    else if (required <= 4096) tier = "4 GB RAM";
    else if (required <= 8192) tier = "8 GB RAM";
    else tier = "more than 8 GB RAM or a split architecture";
    document.getElementById("ram-budget-result").textContent =
      "Estimated coexistence budget: about " + requiredGb + " GB including headroom. RAM-only starting tier: " + tier +
      ". Validate real process memory and CPU before ordering.";
  });
});
</script>

Worked example: 450 MB of baseline services + 500 MB for the database + 6 workers × 120 MB + 300 MB for panel/cache/background jobs = 1,970 MB before headroom. With 25% headroom, the budget is about 2.4 GB. A 2 GB VPS is therefore too tight for those assumptions; 4 GB is the safer starting tier.

When measuring PHP-FPM or similar workers, remember that raw RSS can double-count shared pages and libraries across processes. Treat process measurements as evidence, not as perfectly additive accounting.

### CPU budget

CPU demand depends on how much work must be executed at the same time. Static files served from cache can be inexpensive. Dynamic requests that execute application code, query the database, generate pages, resize images, run imports or perform API work can consume much more CPU.

Look for:

- sustained CPU saturation during legitimate traffic;
- long application request times while CPU is busy;
- several expensive dynamic requests arriving together;
- cron jobs, backups or imports overlapping with user traffic;
- database queries consuming CPU because of inefficient indexes or excessive work.

A short CPU spike is not automatically a reason to upgrade. Persistent saturation that delays legitimate work is stronger evidence.

A practical concurrency estimate is:

**active dynamic requests ≈ dynamic requests per second × request duration**

Example: 6 uncached dynamic requests per second at 0.8 seconds p95 duration imply roughly 4.8 active requests at that moment. If the application needs one worker per active request, plan for about five busy workers plus queue/headroom. If each request consumes 0.12 CPU-seconds, 6 requests per second represent roughly 0.72 CPU-seconds of work per second before headroom. This is a workload estimate, not a universal vCPU guarantee: CPU generation, contention and provider scheduling differ.

## Website workload examples

The same traffic number can produce very different VPS requirements because the amount of work that reaches the origin changes by workload.

| Workload | Typical pressure | Sizing implication |
|---|---|---|
| Mostly static or aggressively cached website | low application CPU, low worker concurrency, mostly file delivery | start small, but still budget for OS, logs, backups and unexpected uncached requests |
| Small WordPress site | PHP workers, database reads, plugin/cron activity | RAM and worker headroom usually matter more than raw monthly visits |
| WooCommerce or another transactional site | uncached cart, checkout, account sessions, scheduled actions and more database writes | prioritize dynamic concurrency, database latency and peak overlap; avoid treating 1–2 GB as a default production target |
| Multiple websites | combined PHP/application workers, databases, cron jobs and overlapping peaks | size from aggregate peak demand and consider isolation when one site can starve the others |
| Background-worker or automation-heavy site | queues, imports, exports, API calls, image processing, scheduled jobs | reserve CPU/RAM outside the user-facing request path and separate workers when bursty jobs disturb the website |

These are workload patterns, not platform guarantees. Use real measurements where available.

## Translate shared-hosting limits into VPS requirements

If the website already runs on shared hosting, the most useful sizing evidence may already exist in the hosting dashboard.

Collect:

- CPU usage and CPU-limit events;
- physical memory usage;
- entry processes or concurrent request limits;
- process count;
- disk I/O and IOPS pressure;
- database size and growth;
- storage use;
- traffic peaks by hour rather than only monthly visits;
- PHP worker or application-process behavior where visible.

### Shared-hosting-to-VPS diagnostic

Use the fault pattern to identify what to investigate before selecting a tier. The tool deliberately does not convert a CloudLinux limit directly into vCPU or RAM.

On cPanel hosting with CloudLinux, start with the Resource Usage history rather than a single live reading. Capture repeated faults and the time they happen, then compare them with traffic, cron, backup, import and admin activity.

<div class="rounded-2xl bg-light p-6 dark:bg-darkmode-light">
<form id="shared-hosting-diagnostic">
  <div class="mb-6">
    <label for="diag-evidence" class="form-label">Quality of your evidence</label>
    <select id="diag-evidence" class="form-input">
      <option value="measured">Dashboard history / measured metrics</option>
      <option value="partial">Some measured metrics</option>
      <option value="traffic">Visitor count or impressions only</option>
    </select>
  </div>
  <div class="mb-6">
    <label for="diag-memory" class="form-label">Memory faults / PMEM events</label>
    <select id="diag-memory" class="form-input"><option value="0">None</option><option value="1">Occasional</option><option value="2">Repeated</option></select>
  </div>
  <div class="mb-6">
    <label for="diag-cpu" class="form-label">CPU limit events</label>
    <select id="diag-cpu" class="form-input"><option value="0">None</option><option value="1">Occasional</option><option value="2">Repeated</option></select>
  </div>
  <div class="mb-6">
    <label for="diag-ep" class="form-label">Entry-process / worker saturation</label>
    <select id="diag-ep" class="form-input"><option value="0">None</option><option value="1">Occasional</option><option value="2">Repeated</option></select>
  </div>
  <div class="mb-6">
    <label for="diag-nproc" class="form-label">Process-count / NPROC saturation</label>
    <select id="diag-nproc" class="form-input"><option value="0">None</option><option value="1">Occasional</option><option value="2">Repeated</option></select>
  </div>
  <div class="mb-6">
    <label for="diag-io" class="form-label">I/O / IOPS pressure</label>
    <select id="diag-io" class="form-input"><option value="0">None</option><option value="1">Occasional</option><option value="2">Repeated</option></select>
  </div>
  <button class="btn btn-primary" type="submit">Diagnose the bottleneck</button>
</form>
<p id="shared-hosting-result" class="mt-6 rounded border border-border p-4 dark:border-darkmode-border" role="status" aria-live="polite">Choose the signals you actually observe.</p>
</div>

<script>
document.addEventListener("DOMContentLoaded", function () {
  var form = document.getElementById("shared-hosting-diagnostic");
  if (!form) return;
  form.addEventListener("submit", function (event) {
    event.preventDefault();
    function value(id) { return Number(document.getElementById(id).value); }
    var memory = value("diag-memory");
    var cpu = value("diag-cpu");
    var ep = value("diag-ep");
    var nproc = value("diag-nproc");
    var io = value("diag-io");
    var evidence = document.getElementById("diag-evidence").value;
    var confidence = evidence === "measured" ? "High" : (evidence === "partial" ? "Medium" : "Low");
    var repeated = [memory, cpu, ep, nproc, io].filter(function (v) { return v === 2; }).length;
    var findings = [];
    if (memory >= 1) findings.push("memory pressure: check worker memory, database working set, swap/OOM and background jobs");
    if (cpu >= 1) findings.push("CPU pressure: profile dynamic requests and database work before adding vCPU");
    if (ep >= 1) findings.push("worker/concurrency pressure: reduce request duration and measure uncached concurrency");
    if (nproc >= 1) findings.push("process-count pressure: find runaway or excessive PHP, cron and background processes before buying capacity");
    if (io >= 1) findings.push("storage pressure: inspect database I/O, backups, logs and imports; more RAM alone may not solve it");
    var decision;
    if (findings.length === 0) decision = "No strong capacity signal. Stay on the current plan or optimize first until measurements show a real constraint.";
    else if (repeated >= 2) decision = "MOVE / SIZE FROM MEASUREMENTS: multiple repeated limits justify a VPS sizing pass after obvious software inefficiencies are removed.";
    else decision = "OPTIMIZE FIRST, THEN RECHECK: there is a likely bottleneck, but one hosting limit is not a direct VPS specification.";
    document.getElementById("shared-hosting-result").textContent =
      decision + " Confidence: " + confidence + ". " + (findings.length ? findings.join("; ") + "." : "");
  });
});
</script>

Do not copy a shared-hosting limit directly into a VPS specification. A CloudLinux CPU percentage, entry-process limit or memory cap describes the current hosting environment; it is evidence about the bottleneck, not a one-to-one VPS conversion.

Use the pattern instead:

**Repeated memory-limit events with normal CPU:** investigate worker memory, database memory and background jobs before adding vCPU.

**Repeated CPU-limit events during legitimate dynamic work:** profile the application and database, then consider additional CPU if the work is genuinely necessary.

**Entry-process or worker saturation:** measure dynamic concurrency and request duration. Faster requests may solve the queue without a larger server.

**I/O pressure:** identify backups, logs, database activity, imports or storage-heavy plugins before assuming more RAM will solve it.

This separates a real capacity problem from a hosting-plan limit that may be triggered by one inefficient component.

| Symptom | Verify | Optimize first | Scale when |
|---|---|---|---|
| Memory faults, swap or OOM | process memory, DB working set, concurrent workers | leaks, oversized workers, cache/database settings | optimized workload still exhausts RAM |
| CPU throttling | sustained CPU plus request/DB timing | slow code, uncached work, expensive queries | legitimate work remains CPU-bound |
| EP/worker queue | dynamic concurrency and request duration | caching, slow endpoints, worker tuning | queue remains after request cost is reduced |
| I/O wait / IOPS faults | database, logs, backups, imports | scheduling, indexes, log/backup behavior | storage path remains the bottleneck under normal work |



## VPS or website optimization?

A larger VPS is justified when legitimate workload repeatedly exhausts a resource after obvious application problems have been addressed.

Optimize first when the pressure comes from:

- one slow plugin or extension;
- an unindexed or pathological database query;
- broken page or object caching;
- abusive bots;
- runaway cron jobs;
- oversized image processing;
- backup or malware scans scheduled during peak traffic;
- memory leaks;
- excessive logging.

Increase server resources when measurements show that the optimized workload still needs more capacity.

The distinction matters economically. Moving inefficient code from shared hosting to a larger VPS can hide the bottleneck temporarily without removing it.

## Size PHP and application workers from concurrency

Monthly visits are weak sizing data because servers experience requests concurrently.

For dynamic PHP workloads, each active PHP worker consumes memory and CPU while processing a request. Worker capacity therefore depends on both average memory per worker and how long requests stay busy.

A simplified RAM check is:

**worker RAM budget = usable RAM after baseline services × the share safely available to workers**

Then compare that budget with measured worker memory. Do not configure the theoretical maximum number of workers if doing so would leave no memory for the database, cache or operating system.

Caching changes this calculation. A cached anonymous page may bypass PHP entirely, while checkout, logged-in sessions, wp-admin, APIs and personalized pages still reach the application.

For WordPress-specific behavior, see [VPS for WordPress]({{< relref "vps-for-wordpress.md" >}}). For transactional workloads, see [VPS for WooCommerce]({{< relref "vps-for-woocommerce.md" >}}).

## Database demand can set the server size

A website can appear CPU-limited when the underlying problem is database work.

Check:

- slow-query patterns;
- database working-set size;
- query concurrency;
- missing indexes;
- large autoloaded data or equivalent application metadata;
- expensive search, filtering or reporting operations;
- imports and maintenance jobs;
- storage latency.

More RAM can help when the database legitimately needs a larger working set, but it does not repair inefficient queries. More CPU can increase throughput, but it can also allow more expensive queries to compete at once.

## Plan for peak traffic, not average traffic

Sizing from an average hides the periods when users actually experience failure.

Identify the busiest realistic window: campaign launches, sales, newsletter sends, product drops, scheduled imports, backups or cron bursts. Estimate which requests remain dynamic during that window and which can be absorbed by page cache or a CDN.

Keep headroom for the combination of:

- normal user traffic;
- dynamic peak traffic;
- administrative activity;
- scheduled jobs;
- deployments and cache warm-up;
- monitoring and backup processes.

A CDN can reduce static delivery and some origin requests. It does not remove dynamic application or database work that still reaches the VPS.

Peak example: if a site receives 20 requests/s and 90% are served from cache/CDN, the origin sees about 2 dynamic requests/s. A campaign that doubles total traffic to 40 requests/s at the same cache ratio sends about 4 dynamic requests/s to the application. At 0.8 seconds p95 duration, that is roughly 3.2 simultaneously active dynamic requests before administrative jobs or checkout/API bursts are added.

## Storage sizing

Disk capacity is not only the current website directory.

Include:

- website files;
- database;
- uploaded media;
- logs;
- temporary files;
- package and application caches;
- staging copies if kept locally;
- backup files if backups are temporarily created on the VPS;
- expected growth.

Do not fill the filesystem close to its limit. Databases, updates, logs and backup operations need working space.

A practical capacity budget is:

**required disk = current files + database + temporary operation space + local backup staging + expected growth + free working headroom**

Example: 18 GB currently used + 8 GB temporary migration/update space + 18 GB temporary local backup staging + 6 GB expected growth already exceeds a 40 GB disk before safety headroom. In that scenario, an 80 GB tier is the safer starting point. Capacity is separate from IOPS and storage latency: a larger disk does not automatically make a slow database faster.

## Bandwidth and monthly transfer sizing

Monthly transfer is different from CPU, RAM and port speed. A server can have plenty of compute headroom and still exceed a transfer allowance if it delivers large files or uncached media directly.

A rough estimate is:

**monthly origin transfer ≈ average bytes sent from the VPS per request × origin requests per month + backups/exports/other outbound traffic**

For a more useful estimate, separate cacheable and dynamic traffic:

**origin transfer ≈ total requested bytes × (1 - CDN/cache offload share) + uncached dynamic responses + non-web outbound traffic**

Example: if users request 2 TB of assets/pages in a month and a CDN serves 80% of those bytes without going back to the origin, the VPS may deliver roughly 400 GB of that cacheable traffic, plus dynamic pages, API responses, backups, exports and any cache misses.

Do not assume a CDN makes origin transfer zero. Logged-in pages, checkout, APIs, cache misses, purge events, large downloads and origin-to-CDN fills can still consume transfer. Also keep **monthly transfer allowance** separate from **network port speed**: a fast port describes potential throughput, while the allowance describes how much data can be sent over the billing period.

## Multiple websites change the calculation

Several websites on one VPS share the same CPU, RAM, storage and process capacity. Their peaks can overlap even if each site is small individually.

Size the server from the combined workload and reserve enough headroom that one site's background job does not starve the others. If isolation, failure impact or resource contention becomes important, splitting workloads can be more useful than continuing to enlarge one server.

See [VPS for multiple websites]({{< relref "vps-for-multiple-websites.md" >}}) for the multi-site decision.

## Control-panel and mail overhead belong in the budget

A control panel simplifies domains, SSL, databases, PHP versions and account administration, but it also runs services of its own. Reserve memory and storage for the panel rather than sizing only for the website.

Mail services can add another persistent resource layer: SMTP, IMAP/POP, spam filtering, antivirus scanning, queues, logs and mailbox storage. If the VPS will host website + email, include that overhead in the RAM, CPU, storage and backup budget instead of assuming mail is free.

For a small website, moving mail to a managed email provider can reduce server load and operational risk. If mail remains on the VPS, verify deliverability requirements such as DNS records and provider/IP constraints separately; a larger VPS does not solve sender reputation.

If you prefer panel-based administration, compare the trade-offs in [VPS with control panel]({{< relref "vps-with-control-panel.md" >}}).

## A repeatable VPS sizing workflow

1. **Measure the current workload.** Record CPU, memory, dynamic concurrency, database behavior, storage and peak periods.
2. **Identify the bottleneck.** Separate CPU, RAM, worker, database, I/O and software-limit problems.
3. **Remove obvious inefficiency.** Fix caching, runaway jobs, pathological queries and abusive traffic before buying capacity.
4. **Build the resource budget.** Reserve RAM for baseline services, database, application workers, panel and background work.
5. **Choose a starting tier with headroom.** Avoid both zero-headroom sizing and speculative overprovisioning.
6. **Reproduce a realistic peak.** Validate the configuration under representative dynamic load, not only an idle homepage.
7. **Monitor after migration.** Adjust from measurements instead of assuming the initial estimate is permanent.

Once the destination is sized, use [Website migration to VPS]({{< relref "website-migration-to-vps.md" >}}) to plan the inventory, private test, final data sync, DNS cutover and rollback path.

## Evidence-based recommendation

A useful VPS recommendation should state both the configuration and the reason for it.

For example:

**2 vCPU / 4 GB RAM / 80 GB** may be a reasonable starting point when a business website runs a database-backed CMS, has meaningful uncached PHP activity, needs a control panel and requires operating headroom. It is not a guarantee that the server supports a specific number of monthly visitors.

Confidence should be lower when the only input is visitor count. Confidence becomes higher when CPU history, memory pressure, concurrent dynamic requests, worker memory, database behavior and storage growth are known.

Use a simple confidence label:

- **Low confidence:** visitor count, CMS name and rough storage only.
- **Medium confidence:** some real CPU/RAM history plus workload type and peak pattern.
- **High confidence:** time-series CPU/RAM/I/O, uncached concurrency, worker memory, request duration, database behavior and storage growth.

A higher confidence label means the assumptions are better, not that future traffic is guaranteed.

## Match the result to a VPS

Use the RAM estimate, CPU evidence, storage budget and peak behavior together. These VDSina Standard configurations are examples for mapping the result; verify current provider terms before ordering.

| Configuration | Good starting fit | Avoid / recheck when | Main validation | Action |
|---|---|---|---|---|
| 1 vCPU / 1 GB / 10 GB — $0.07/day, 1 TB/month | test site, very light cached site, minimal services | panel + database + several dynamic workers, production store | RAM headroom and disk | <a href="https://www.vdsina.com/?partner=ni8gzrvz75" target="_blank" rel="sponsored nofollow noopener">Check current plan</a> |
| 1 vCPU / 2 GB / 40 GB — $0.50/day, 32 TB/month | lean small site or CMS with controlled dynamic work | sustained CPU, several active sites, heavy panel/mail stack | worker memory, DB memory, storage growth | <a href="https://www.vdsina.com/?partner=ni8gzrvz75" target="_blank" rel="sponsored nofollow noopener">Check current plan</a> |
| 2 vCPU / 4 GB / 80 GB — $0.67/day, 32 TB/month | dynamic business CMS, moderate uncached PHP, panel headroom | heavy WooCommerce, large imports, high DB pressure, noisy multi-site peaks | CPU saturation, DB latency, peak overlap | <a href="https://www.vdsina.com/?partner=ni8gzrvz75" target="_blank" rel="sponsored nofollow noopener">Check current plan</a> |
| 4 vCPU / 8 GB / 160 GB — $1.34/day, 32 TB/month | heavier dynamic workload, larger DB, several active sites | strict HA, very high write load, workload needing independent scaling | whether one VPS is still the right architecture | <a href="https://www.vdsina.com/?partner=ni8gzrvz75" target="_blank" rel="sponsored nofollow noopener">Check current plan</a> |

A 1 GB or 2 GB tier should not be treated as a default production recommendation merely because the website can boot there. Ecommerce, large databases, several dynamic sites, mail services and control panels can consume headroom quickly.

<p>
  <a class="btn btn-primary" href="https://www.vdsina.com/?partner=ni8gzrvz75" target="_blank" rel="sponsored nofollow noopener">Choose your VPS</a>
</p>

## Before buying the VPS

Check the infrastructure terms that sizing alone does not answer: transfer allowance, storage type and capacity, IP terms, server location, backup policy, upgrade path, management scope, control-panel licensing and current billing terms.

If the current website is still on shared hosting, compare the operational change in [VPS vs shared hosting]({{< relref "vps-vs-shared-hosting.md" >}}) before moving.

## Technical references

- [cPanel: hardware requirements for a server](https://support.cpanel.net/hc/en-us/articles/360054297474-What-Are-the-Hardware-Requirements-For-My-Server)
- [cPanel: how to determine how much RAM, CPU and disk to add](https://support.cpanel.net/hc/en-us/articles/1500005235562-How-to-determine-how-much-RAM-CPU-and-DISK-resources-I-should-add-when-upgrading-a-server)
- [VDSina Standard VPS configurations](https://www.vdsina.com/pricing/standard)

<p>
  <a class="btn btn-primary" href="https://www.vdsina.com/?partner=ni8gzrvz75" target="_blank" rel="sponsored nofollow noopener">Check the current VPS offer</a>
</p>
<p><small>Affiliate disclosure: partner links are marked sponsored. Provider pricing, transfer and other commercial terms can change; verify them on the provider site before ordering.</small></p>

## FAQ

### How much RAM does a website VPS need?

There is no reliable universal amount. A lean cached site can use little memory, while a dynamic CMS with a database, panel and concurrent application workers can require substantially more. Calculate RAM from the processes that must coexist and leave headroom.

### Is 2 GB RAM enough for a website VPS?

It can be enough for a small, lean workload. It becomes restrictive when a control panel, database, several PHP workers, background jobs or multiple sites must run together. Measure memory pressure rather than relying on the RAM number alone.

### Is 4 GB RAM enough for WordPress?

For many business WordPress workloads, 4 GB is a practical starting point because it provides more room for Linux, the database, PHP workers and caching. Heavy plugins, WooCommerce, imports, large databases or high dynamic concurrency can require more.

### How many visitors can a VPS handle?

Visitor count alone cannot answer this. Cache hit rate, concurrent requests, application execution time, database work and background jobs can change capacity by orders of magnitude between two sites with similar traffic.

### Should I add RAM or CPU first?

Add the resource that measurements show is constrained. Memory pressure, swap activity or OOM events point toward RAM or memory optimization. Sustained CPU saturation during legitimate optimized work points toward CPU. Database and I/O bottlenecks need separate diagnosis.

### Does a CDN reduce VPS requirements?

It can reduce static-file delivery and cacheable origin requests. Dynamic application requests and database work that reach the origin still consume VPS resources.

### Should I size for average or peak traffic?

Size for a realistic peak with operating headroom. Average traffic can conceal short periods where concurrency, scheduled jobs and dynamic requests overlap.
