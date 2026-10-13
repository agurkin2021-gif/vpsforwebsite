---
title: "VPS for WordPress"
description: "VPS for WordPress: size CPU and RAM from PHP workers, database load, caching, plugins and background jobs, then choose the right management and migration path."
image: "https://raw.githubusercontent.com/zeon-studio/hugoplate/4acb4365d7a86703357a9f216db149f55210fa09/exampleSite/assets/images/banner.png"
---

VPS for WordPress is useful when WordPress needs more control, isolation or server-level features than shared hosting can provide. The VPS should be sized around **uncached PHP work, database demand, plugins, background jobs, storage growth and the services that run beside WordPress**, not around a monthly visitor number.

For the broader server decision, see [VPS for website]({{< relref "_index.md" >}}).

[Quick answer](#quick-answer) · [Fit checker](#wordpress-vps-fit-checker) · [PHP workers](#php-workers-and-ram) · [Caching](#wordpress-caching-layers) · [Database](#database-demand) · [WP-Cron](#wp-cron-and-background-jobs) · [FAQ](#faq)

## Quick answer

These are practical starting points for the current VDSina Standard tiers, not visitor guarantees.

| WordPress workload | Practical starting point | Main constraint to verify |
|---|---:|---|
| Lab/test site or extremely lean cached WordPress | **1 vCPU / 1 GB / 10 GB** | very little RAM/storage headroom; not a default production target |
| Small, well-cached WordPress site | **1 vCPU / 2 GB / 40 GB** | PHP workers, database memory, plugin/background load |
| Business WordPress site | **2 vCPU / 4 GB / 80 GB** | uncached concurrency, database latency, cron/plugins |
| Heavier dynamic WordPress, large DB or several active sites | **4 vCPU / 8 GB / 160 GB** | sustained CPU, PHP queue, DB working set, overlapping jobs |

Current VDSina Standard prices rechecked on October 13, 2026:

- 1 vCPU / 1 GB / 10 GB / 1 TB monthly transfer — **$0.07/day**;
- 1 vCPU / 2 GB / 40 GB / 32 TB — **$0.50/day**;
- 2 vCPU / 4 GB / 80 GB / 32 TB — **$0.67/day**;
- 4 vCPU / 8 GB / 160 GB / 32 TB — **$1.34/day**.

If the site is a real store with dynamic cart, checkout, account, orders or stock, use [VPS for WooCommerce]({{< relref "vps-for-woocommerce.md" >}}) rather than treating it like normal cached WordPress.

For a deeper cross-stack resource calculation, use [VPS sizing for website]({{< relref "vps-sizing-for-website.md" >}}).

## WordPress requirements are not VPS sizing

WordPress.org currently recommends a host that supports:

- **PHP 8.3 or greater**;
- **MariaDB 10.11+ or MySQL 8.0+**;
- **HTTPS**;
- Apache or Nginx as recommended web-server choices.

Those requirements answer **"can this server run WordPress?"** They do not answer **"how much VPS does this production workload need?"**

A production VPS also needs RAM/CPU/storage for:

- Linux;
- Nginx/Apache;
- PHP-FPM workers;
- MySQL/MariaDB;
- OPcache;
- page/object cache where used;
- control panel;
- mail if hosted locally;
- backups;
- cron jobs;
- malware/security scans;
- imports/exports;
- monitoring;
- operating headroom.

Do not use the WordPress software requirements as a production resource recommendation.

## WordPress VPS Fit Checker

Use this checker as a starting point. It does not replace real CPU/RAM/database measurements.

<div class="rounded-2xl bg-light p-6 dark:bg-darkmode-light">
<form id="wordpress-vps-fit-checker">
  <div class="mb-6">
    <label for="wp-limits" class="form-label">Does the current hosting show repeated legitimate limits or a capability gap?</label>
    <select id="wp-limits" class="form-input">
      <option value="no">No / not measured</option>
      <option value="some">Occasional pressure</option>
      <option value="yes">Repeated limits or VPS-only capability needed</option>
    </select>
  </div>
  <div class="mb-6">
    <label for="wp-type" class="form-label">WordPress workload</label>
    <select id="wp-type" class="form-input">
      <option value="content">Mostly cached content / brochure / blog</option>
      <option value="business">Business CMS with forms/plugins/admin activity</option>
      <option value="membership">Membership / logged-in / personalized site</option>
      <option value="store">WooCommerce / transactional store</option>
    </select>
  </div>
  <div class="mb-6">
    <label for="wp-dynamic" class="form-label">Uncached PHP / admin / API intensity</label>
    <select id="wp-dynamic" class="form-input">
      <option value="low">Low</option>
      <option value="medium">Moderate</option>
      <option value="high">High</option>
    </select>
  </div>
  <div class="mb-6">
    <label for="wp-jobs" class="form-label">Heavy plugins, imports, scans, backups or background jobs?</label>
    <select id="wp-jobs" class="form-input"><option value="no">No</option><option value="yes">Yes</option></select>
  </div>
  <div class="mb-6">
    <label for="wp-db" class="form-label">Database size/activity</label>
    <select id="wp-db" class="form-input">
      <option value="small">Small / modest</option>
      <option value="medium">Moderate</option>
      <option value="large">Large / query-heavy</option>
    </select>
  </div>
  <div class="mb-6">
    <label for="wp-panel" class="form-label">Control panel or local mail on the same VPS?</label>
    <select id="wp-panel" class="form-input"><option value="no">No</option><option value="yes">Yes</option></select>
  </div>
  <div class="mb-6">
    <label for="wp-sites" class="form-label">How many active WordPress sites?</label>
    <select id="wp-sites" class="form-input"><option value="1">1</option><option value="few">2–5</option><option value="many">6+</option></select>
  </div>
  <button class="btn btn-primary" type="submit">Estimate WordPress VPS fit</button>
</form>
<p id="wordpress-vps-fit-result" class="mt-6 rounded border border-border p-4 dark:border-darkmode-border" role="status" aria-live="polite">Use real workload evidence where possible.</p>
</div>

<script>
document.addEventListener("DOMContentLoaded", function () {
  var form = document.getElementById("wordpress-vps-fit-checker");
  if (!form) return;

  form.addEventListener("submit", function (event) {
    event.preventDefault();

    var limits = document.getElementById("wp-limits").value;
    var type = document.getElementById("wp-type").value;
    var dynamic = document.getElementById("wp-dynamic").value;
    var jobs = document.getElementById("wp-jobs").value === "yes";
    var db = document.getElementById("wp-db").value;
    var panel = document.getElementById("wp-panel").value === "yes";
    var sites = document.getElementById("wp-sites").value;

    var score = 0;
    if (type === "business") score += 2;
    if (type === "membership") score += 4;
    if (type === "store") score += 5;
    if (dynamic === "medium") score += 2;
    if (dynamic === "high") score += 4;
    if (jobs) score += 2;
    if (db === "medium") score += 1;
    if (db === "large") score += 3;
    if (panel) score += 1;
    if (sites === "few") score += 2;
    if (sites === "many") score += 4;

    var result;

    if (limits === "no" && type === "content" && dynamic === "low" && score <= 1) {
      result = "STAY / OPTIMIZE FIRST: there is no strong VPS signal yet. Good shared or managed WordPress hosting may be simpler until real limits or a required server capability appear.";
    } else if (type === "store") {
      result = "WOOCOMMERCE PATH: start around 4 GB RAM or higher only after measuring dynamic checkout/account/order workload. Use the dedicated VPS for WooCommerce guide; store traffic is not normal cached WordPress traffic.";
    } else if (score <= 2) {
      result = "LEAN 2 GB START: 1 vCPU / 2 GB / 40 GB can suit a small, well-cached WordPress site. Watch PHP worker memory, DB RAM and plugin/background jobs.";
    } else if (score <= 7) {
      result = "PRACTICAL 4 GB START: 2 vCPU / 4 GB / 80 GB gives healthier headroom for a business WordPress site, PHP workers, database, cache and routine background work.";
    } else {
      result = "8 GB OR RECHECK ARCHITECTURE: 4 vCPU / 8 GB / 160 GB is a stronger starting point for heavier dynamic or multi-site WordPress. If one site/job dominates resources, consider workload separation instead of only enlarging one VPS.";
    }

    if (limits === "no" && type !== "store" && score > 1) {
      result += " If the current host is not actually limiting the site, optimize and measure before migrating.";
    }

    document.getElementById("wordpress-vps-fit-result").textContent = result;
  });
});
</script>

## When WordPress actually needs VPS

A WordPress site can justify VPS even without huge traffic.

Common reasons:

- repeated CPU/memory/process limits under legitimate load;
- need for a custom PHP/runtime configuration;
- need for Redis/Memcached or another server-side service;
- real system cron instead of visitor-triggered scheduling;
- long-running background jobs;
- custom Nginx/Apache behavior;
- several sites that need one controlled environment;
- stronger workload/account isolation;
- server-level monitoring or firewall requirements.

If the only symptom is "the site is slow," first compare [VPS vs Shared Hosting]({{< relref "vps-vs-shared-hosting.md" >}}) and verify that WordPress itself is not the bottleneck.

## When WordPress does not need VPS

Stay on good shared or managed WordPress hosting when:

- the site is light and stable;
- caching works;
- the host's resource meters are not showing repeated limits;
- no custom service/root access is required;
- the team does not want to maintain Linux;
- the provider already handles backups, security, updates or staging well enough;
- the VPS would mainly replace a simple hosting service with more operational work.

VPS is not automatically faster. A poorly sized or untuned VPS can run WordPress worse than a good managed platform.

## PHP workers and RAM

For uncached requests, PHP-FPM workers are a major concurrency limit.

Each active worker consumes memory while processing a request. More workers can handle more simultaneous dynamic requests, but increasing the worker count without increasing the RAM budget can cause:

- swap;
- memory pressure;
- OOM kills;
- database starvation;
- server instability.

A practical model is:

**WordPress RAM = OS + web server + database + cache + PHP workers + panel/mail/jobs + headroom**

Then:

**PHP worker budget = RAM safely available to PHP / measured average worker memory**

Do not configure the theoretical maximum number of workers if doing so leaves no memory for MySQL/MariaDB, cache or the operating system.

Logged-in users, wp-admin, REST/API requests, search, forms, preview and personalized pages are more likely to bypass full-page cache and consume PHP workers.

## WordPress caching layers

Caching is not one feature.

| Layer | What it caches | Main effect |
|---|---|---|
| **PHP OPcache** | compiled PHP bytecode | avoids recompiling PHP scripts on every request |
| **Page cache** | rendered HTML | lets many anonymous page views bypass WordPress/PHP work |
| **Persistent object cache** | reusable objects/query results | reduces repeated database/application work |
| **Browser/CDN cache** | static/edge-deliverable content | reduces repeated origin transfer and requests |

WordPress's own optimization documentation recommends caching as a major performance tool. But these layers solve different problems.

Do not call Redis a page cache. Redis is commonly used as a persistent object-cache backend; full-page caching is a separate layer.

## Persistent object cache and Redis

WordPress includes an object-cache API, but the default cache is **not persistent across requests**.

Persistent object caching requires an external backend/drop-in such as Redis or Memcached plus the appropriate WordPress integration.

It can help when the site repeatedly performs expensive database/object work, but it is not an automatic speed button.

Before adding Redis:

- confirm the site/database workload benefits;
- verify enough RAM remains for PHP and the database;
- monitor hit rate and memory;
- keep page caching as a separate decision.

A site with efficient full-page caching and light database work may gain less from Redis than a dynamic membership or query-heavy site.

## Database demand

WordPress performance can become database-limited before CPU is visibly saturated.

Check:

- slow queries;
- large options/autoloaded data;
- plugin metadata;
- search/filter/reporting queries;
- postmeta-heavy workloads;
- database working set;
- concurrent writes;
- imports/exports;
- storage latency.

More CPU does not repair a pathological query. More RAM can help when the database legitimately needs a larger working set, but it does not replace indexing/query/plugin work.

Measure first, then scale.

## Plugins, themes and background jobs

A plugin is not only disk space.

Plugins/themes can add:

- PHP work;
- database queries;
- external API calls;
- scheduled tasks;
- cache invalidation;
- admin AJAX;
- image processing;
- security scanning;
- backups;
- imports/exports;
- analytics/logging.

Heavy tasks can collide with real traffic.

Schedule backups, scans, imports and image-processing jobs away from peak periods where practical. If one plugin or job causes the resource spike, fix or reschedule it before assuming the VPS is too small.

## WP-Cron and background jobs

WP-Cron is triggered by WordPress requests rather than running continuously like a system scheduler.

That can be acceptable for ordinary sites. For time-sensitive or busy workloads, WordPress's own developer documentation describes using the operating system's scheduler to call WordPress cron on a controlled interval.

If you move to a system scheduler:

- create the replacement trigger first;
- verify it works;
- only then disable the normal visitor-triggered WP-Cron behavior if that is part of the plan;
- log and monitor failed jobs.

Do not disable WP-Cron without another scheduler.

## Storage, media, staging and backups

Disk planning must include more than WordPress core.

Budget for:

- uploads/media;
- database;
- plugins/themes;
- logs;
- cache files;
- temporary update files;
- image-processing temp space;
- staging copy;
- backup archives before they are moved off-server;
- expected growth.

A site using 20 GB today can need materially more temporary space during a clone, restore, plugin update or backup compression job.

Do not keep the only backup on the VPS.

## Manual, control panel or FASTPANEL?

WordPress can run perfectly well without cPanel or another panel.

### Manual Linux

Good fit when you want:

- minimal stack;
- SSH administration;
- custom Nginx/Apache/PHP/database configuration;
- automation or Git-based deployment.

Use [How to host a website on VPS]({{< relref "how-to-host-a-website-on-vps.md" >}}) for the manual deployment path.

### Generic control panel

Useful when browser-based domains, SSL, PHP, databases, users, mail or backups remove enough repetitive work.

Use [VPS with Control Panel]({{< relref "vps-with-control-panel.md" >}}).

### FASTPANEL

FASTPANEL's official workflow supports WordPress site creation. VDSina currently lists FASTPANEL on Ubuntu 22 as a preconfigured panel option.

Use [FASTPANEL VPS Hosting]({{< relref "fastpanel-vps-hosting.md" >}}) for the branded setup/sizing path.

A control panel simplifies administration; it does not make the VPS managed.

## Managed vs self-managed WordPress VPS

On a self-managed VPS, somebody must own:

- OS/package updates;
- SSH/firewall;
- PHP/web-server updates;
- database administration;
- WordPress/plugin/theme updates;
- backups and restore tests;
- monitoring;
- incidents.

If nobody owns those jobs, choose managed administration rather than assuming WordPress or a control panel will manage the server.

See [Managed vs Unmanaged VPS]({{< relref "managed-vs-unmanaged-vps.md" >}}).

## WooCommerce is a different WordPress workload

WooCommerce shares the WordPress stack but behaves differently under real store traffic.

Cart, checkout, account, orders, stock and many scheduled actions are dynamic and cannot be treated like anonymous cached blog pages.

If store transactions matter, use [VPS for WooCommerce]({{< relref "vps-for-woocommerce.md" >}}) for the dedicated sizing/operations model.

## Multiple WordPress sites

Several WordPress sites share:

- CPU;
- RAM;
- database service;
- PHP workers/pools;
- storage;
- cron/background-job windows;
- backup time;
- failure domain.

Ten quiet cached sites can be lighter than one busy dynamic membership site.

Use separate users/database credentials where appropriate, and size from the **combined peak**, not the domain count.

See [VPS for Multiple Websites]({{< relref "vps-for-multiple-websites.md" >}}).

## Upgrade triggers

Upgrade only after measuring a real constraint.

Strong triggers:

- sustained RAM pressure, swap or OOM events;
- repeated PHP worker queue/saturation;
- sustained CPU saturation after cache/query/plugin optimization;
- database latency caused by legitimate working-set pressure;
- storage growth beyond safe operating headroom;
- background jobs repeatedly colliding with live traffic;
- multiple active sites exhausting shared resources.

If the website is slow while these signals remain healthy, a larger VPS may not be the fix.

## WordPress VPS launch checklist

| Check | Pass condition |
|---|---|
| WordPress runtime | supported PHP/DB versions and HTTPS |
| PHP | FPM/runtime configured; worker count fits RAM |
| Database | dedicated credentials; slow-query/working-set risk understood |
| Cache | page/object/OPcache layers deliberately chosen |
| Cron | WP-Cron/system schedule works and is monitored |
| Files | correct ownership; uploads writable without `777` |
| HTTPS | trusted certificate and renewal path |
| Backups | files + DB included; off-server copy and restore path |
| Updates | OS + WordPress + plugins/themes have an owner |
| Monitoring | external uptime + CPU/RAM/disk/log visibility |
| Reboot | web/PHP/DB/cron return automatically |
| Capacity | measured under representative uncached/dynamic workload |

For an existing production site, use [Website migration to VPS]({{< relref "website-migration-to-vps.md" >}}) for cutover, final writes, DNS and rollback.

## Current VPS examples

These VDSina Standard configurations are current examples, not WordPress traffic guarantees.

| VPS | Good starting fit | Recheck when |
|---|---|---|
| 1 vCPU / 1 GB / 10 GB — $0.07/day | lab/test or extremely lean cached WordPress | production DB + several PHP workers + panel/mail |
| 1 vCPU / 2 GB / 40 GB — $0.50/day | lean small WordPress | heavy plugins, multiple active sites, sustained dynamic work |
| 2 vCPU / 4 GB / 80 GB — $0.67/day | practical business WordPress baseline | heavy membership/WooCommerce, large DB, overlapping jobs |
| 4 vCPU / 8 GB / 160 GB — $1.34/day | heavier dynamic WordPress / larger DB / several sites | workload needs independent scaling or stronger isolation |

VDSina's current Standard page does not list WordPress as a dedicated preinstalled application in its visible template/application groups. Use a pure OS/manual path or a current compatible control-panel path instead of assuming a one-click WordPress image.

<p>
  <a class="btn btn-primary" href="https://www.vdsina.com/?partner=ni8gzrvz75" target="_blank" rel="sponsored nofollow noopener">Check current WordPress VPS options</a>
</p>
<p><small>Affiliate disclosure: this site may earn a commission if you order through this partner link. Verify current VPS pricing, templates and panel availability before ordering.</small></p>

## Technical references

- [WordPress.org — current requirements](https://wordpress.org/about/requirements/)
- [WordPress Developer Handbook — caching](https://developer.wordpress.org/advanced-administration/performance/cache/)
- [WordPress Developer — object cache](https://developer.wordpress.org/reference/classes/wp_object_cache/)
- [WordPress Developer — system scheduler and WP-Cron](https://developer.wordpress.org/plugins/cron/hooking-wp-cron-into-the-system-task-scheduler/)
- [VDSina Standard VPS](https://www.vdsina.com/pricing/standard)

## FAQ

### How much RAM does WordPress need on a VPS?

WordPress core does not define a production VPS RAM requirement. RAM must cover Linux, the web server, PHP workers, database, caches, panel/mail/background jobs and headroom. A lean site may fit 2 GB; 4 GB is a stronger practical baseline for a business site.

### Is 1 GB RAM enough for WordPress VPS?

It can run a very lean/test WordPress setup, but leaves little headroom for the database, PHP workers and background work. It should not be treated as the normal production recommendation.

### Is 2 GB RAM enough for WordPress?

It can be enough for a small, well-cached site with a lean stack. Monitor PHP worker memory, database RAM, plugins and background jobs.

### Is 4 GB RAM enough for WordPress?

For many business WordPress sites, 4 GB is a practical starting point. Heavy plugins, membership traffic, WooCommerce, large databases, imports or several active sites can require more.

### How many visitors can a WordPress VPS handle?

There is no reliable universal visitor number. Cache hit rate, uncached concurrency, PHP request duration, plugin cost, database work and background jobs determine capacity.

### Do I need Redis for WordPress on VPS?

No. Redis can provide persistent object caching when the workload benefits from repeated object/database caching, but it is not required for every WordPress site and does not replace full-page caching.

### Should I use Nginx or Apache for WordPress VPS?

Both are valid. WordPress.org recommends Apache or Nginx as robust choices. Use the stack your application and administrator can operate reliably.

### Should I replace WP-Cron with system cron?

Only when the workload benefits from a controlled scheduler and you configure a working replacement. Do not disable WP-Cron without another trigger.

### Does WordPress VPS need a control panel?

No. WordPress can run on a manually managed Linux VPS. A panel is optional and should be chosen for administration convenience, not as a performance requirement.

### Does VDSina include WordPress preinstalled?

The current Standard VPS page does not list WordPress as a dedicated preinstalled application in the visible template/application groups. Verify the live order screen before assuming any template availability.
