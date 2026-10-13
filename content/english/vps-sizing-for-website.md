---
title: "VPS Sizing for Website"
description: "VPS sizing for website: calculate CPU, RAM and storage from real workload, shared-hosting limits, PHP workers, database demand and peak traffic."
---

VPS sizing for a website should start with the workload that reaches the origin server, not with a monthly visitor count. Cacheability, simultaneous dynamic requests, PHP or application workers, database activity, background jobs, control-panel overhead and storage growth determine how much CPU, RAM and disk the website actually needs.

## Quick sizing answer

Use these configurations as starting points, then validate them against the workload:

| Website workload | Starting VPS | What to verify |
|---|---:|---|
| Very light site, test environment, aggressively cached project | 1 vCPU / 1 GB RAM / 10 GB | Memory headroom, database size, swap use |
| Small site or lean CMS | 1 vCPU / 2 GB RAM / 40 GB | PHP workers, panel overhead, database memory |
| Business site or typical dynamic WordPress workload | 2 vCPU / 4 GB RAM / 80 GB | Uncached concurrency, cron jobs, database latency |
| Heavier dynamic site, larger database or several active sites | 4 vCPU / 8 GB RAM / 160 GB | Sustained CPU, worker memory, peak overlap |

These are sizing directions, not traffic guarantees. Two websites with the same visitor count can require very different servers.

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

### CPU budget

CPU demand depends on how much work must be executed at the same time. Static files served from cache can be inexpensive. Dynamic requests that execute application code, query the database, generate pages, resize images, run imports or perform API work can consume much more CPU.

Look for:

- sustained CPU saturation during legitimate traffic;
- long application request times while CPU is busy;
- several expensive dynamic requests arriving together;
- cron jobs, backups or imports overlapping with user traffic;
- database queries consuming CPU because of inefficient indexes or excessive work.

A short CPU spike is not automatically a reason to upgrade. Persistent saturation that delays legitimate work is stronger evidence.

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

Do not copy a shared-hosting limit directly into a VPS specification. A CloudLinux CPU percentage, entry-process limit or memory cap describes the current hosting environment; it is evidence about the bottleneck, not a one-to-one VPS conversion.

Use the pattern instead:

**Repeated memory-limit events with normal CPU:** investigate worker memory, database memory and background jobs before adding vCPU.

**Repeated CPU-limit events during legitimate dynamic work:** profile the application and database, then consider additional CPU if the work is genuinely necessary.

**Entry-process or worker saturation:** measure dynamic concurrency and request duration. Faster requests may solve the queue without a larger server.

**I/O pressure:** identify backups, logs, database activity, imports or storage-heavy plugins before assuming more RAM will solve it.

This separates a real capacity problem from a hosting-plan limit that may be triggered by one inefficient component.

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

For WordPress-specific behavior, see [VPS for WordPress](/vps-for-wordpress/). For transactional workloads, see [VPS for WooCommerce](/vps-for-woocommerce/).

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

## Multiple websites change the calculation

Several websites on one VPS share the same CPU, RAM, storage and process capacity. Their peaks can overlap even if each site is small individually.

Size the server from the combined workload and reserve enough headroom that one site's background job does not starve the others. If isolation, failure impact or resource contention becomes important, splitting workloads can be more useful than continuing to enlarge one server.

See [VPS for multiple websites](/vps-for-multiple-websites/) for the multi-site decision.

## Control-panel overhead belongs in the budget

A control panel simplifies domains, SSL, databases, PHP versions and account administration, but it also runs services of its own. Reserve memory and storage for the panel rather than sizing only for the website.

If you prefer panel-based administration, compare the trade-offs in [VPS with control panel](/vps-with-control-panel/).

## A repeatable VPS sizing workflow

1. **Measure the current workload.** Record CPU, memory, dynamic concurrency, database behavior, storage and peak periods.
2. **Identify the bottleneck.** Separate CPU, RAM, worker, database, I/O and software-limit problems.
3. **Remove obvious inefficiency.** Fix caching, runaway jobs, pathological queries and abusive traffic before buying capacity.
4. **Build the resource budget.** Reserve RAM for baseline services, database, application workers, panel and background work.
5. **Choose a starting tier with headroom.** Avoid both zero-headroom sizing and speculative overprovisioning.
6. **Reproduce a realistic peak.** Validate the configuration under representative dynamic load, not only an idle homepage.
7. **Monitor after migration.** Adjust from measurements instead of assuming the initial estimate is permanent.

## Evidence-based recommendation

A useful VPS recommendation should state both the configuration and the reason for it.

For example:

**2 vCPU / 4 GB RAM / 80 GB** may be a reasonable starting point when a business website runs a database-backed CMS, has meaningful uncached PHP activity, needs a control panel and requires operating headroom. It is not a guarantee that the server supports a specific number of monthly visitors.

Confidence should be lower when the only input is visitor count. Confidence becomes higher when CPU history, memory pressure, concurrent dynamic requests, worker memory, database behavior and storage growth are known.

## Before buying the VPS

Check the infrastructure terms that sizing alone does not answer: transfer allowance, storage type and capacity, IP terms, server location, backup policy, upgrade path, management scope, control-panel licensing and current billing terms.

If the current website is still on shared hosting, compare the operational change in [VPS vs shared hosting](/vps-vs-shared-hosting/) before moving.

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
