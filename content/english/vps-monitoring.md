---
title: "VPS Monitoring"
description: "Monitor a VPS with external uptime checks, CPU/RAM/disk/network metrics, service health, logs and actionable alerts. Includes tools, thresholds and a practical checklist."
image: "images/home/vps-for-website-hero.webp"
---

VPS Monitoring should answer more than “is the server up?” A production monitoring baseline needs **external availability checks, historical host metrics, service/application health, logs, actionable alerts and a named response owner**.

A VPS can respond to ping while Nginx is broken, the database is stalled, the disk is full or the TLS certificate is about to expire. Monitoring therefore has to cover both the server and the user-facing website.

For the broader server decision, see [VPS for website]({{< relref "_index.md" >}}).

[Quick answer](#quick-answer) · [Checker](#vps-monitoring-baseline-checker) · [Host metrics](#monitor-cpu-memory-disk-and-network) · [Application health](#monitor-services-and-application-health) · [Alerts](#build-actionable-alerts) · [Capacity](#use-trends-for-capacity-planning) · [FAQ](#faq)

## Quick answer

A practical VPS monitoring stack has five layers:

| Layer | What it tells you | Typical failure it catches |
|---|---|---|
| **External availability** | whether users can reach the site from outside the VPS | VPS/network/site is unreachable |
| **Host metrics** | CPU, RAM, swap, disk, inodes, I/O and network trends | memory leak, disk fill, sustained CPU pressure |
| **Service/application health** | whether web server, runtime, DB and critical endpoints actually work | Nginx/PHP/DB/app failure while server remains online |
| **Logs/events** | what changed or failed | 5xx spike, OOM, failed worker, DB error |
| **Alerting + ownership** | whether the right person is notified and can act | silent outage or ignored dashboard |

Do not make the only uptime monitor run on the same VPS it is supposed to watch. If that VPS or its network path fails completely, the monitor can disappear with it.

## VPS Monitoring Baseline Checker

Use this checker to find blind spots. It does not guarantee uptime.

<div class="rounded-2xl bg-light p-6 dark:bg-darkmode-light">
<form id="vps-monitoring-checker">
  <div class="mb-6">
    <label for="mon-workload" class="form-label">Main workload</label>
    <select id="mon-workload" class="form-input">
      <option value="static">Static / simple website</option>
      <option value="cms">WordPress / CMS</option>
      <option value="transactional">WooCommerce / transactional site</option>
      <option value="multi">Multiple websites / mixed portfolio</option>
    </select>
  </div>
  <div class="mb-6">
    <label for="mon-external" class="form-label">External HTTP(S) uptime check from outside this VPS?</label>
    <select id="mon-external" class="form-input"><option value="no">No</option><option value="yes">Yes</option></select>
  </div>
  <div class="mb-6">
    <label for="mon-metrics" class="form-label">Historical CPU/RAM/disk/network metrics retained?</label>
    <select id="mon-metrics" class="form-input"><option value="no">No / only ad-hoc top/htop</option><option value="yes">Yes</option></select>
  </div>
  <div class="mb-6">
    <label for="mon-disk" class="form-label">Disk capacity, inodes and storage pressure monitored?</label>
    <select id="mon-disk" class="form-input"><option value="no">No / only free GB</option><option value="yes">Yes</option></select>
  </div>
  <div class="mb-6">
    <label for="mon-app" class="form-label">Critical service/application health checks configured?</label>
    <select id="mon-app" class="form-input"><option value="no">No / only ping</option><option value="yes">Yes</option></select>
  </div>
  <div class="mb-6">
    <label for="mon-jobs" class="form-label">DB / queue / cron / backup freshness monitored where applicable?</label>
    <select id="mon-jobs" class="form-input"><option value="no">No / unknown</option><option value="yes">Yes</option><option value="na">Not applicable</option></select>
  </div>
  <div class="mb-6">
    <label for="mon-alerts" class="form-label">Automatic alerts configured with useful severity/duration rules?</label>
    <select id="mon-alerts" class="form-input"><option value="no">No / dashboard only</option><option value="yes">Yes</option></select>
  </div>
  <div class="mb-6">
    <label for="mon-notify" class="form-label">Notification path survives failure of this VPS?</label>
    <select id="mon-notify" class="form-input"><option value="no">No / same VPS only</option><option value="yes">Yes</option></select>
  </div>
  <div class="mb-6">
    <label for="mon-owner" class="form-label">Named owner and first-response runbook exist?</label>
    <select id="mon-owner" class="form-input"><option value="no">No</option><option value="yes">Yes</option></select>
  </div>
  <button class="btn btn-primary" type="submit">Check monitoring baseline</button>
</form>
<p id="vps-monitoring-result" class="mt-6 rounded border border-border p-4 dark:border-darkmode-border" role="status" aria-live="polite">Mark only monitoring that is actually collecting data and delivering alerts.</p>
</div>

<script>
document.addEventListener("DOMContentLoaded", function () {
  var form = document.getElementById("vps-monitoring-checker");
  if (!form) return;

  form.addEventListener("submit", function (event) {
    event.preventDefault();

    function yes(id) { return document.getElementById(id).value === "yes"; }
    var workload = document.getElementById("mon-workload").value;
    var external = yes("mon-external");
    var metrics = yes("mon-metrics");
    var disk = yes("mon-disk");
    var app = yes("mon-app");
    var jobsValue = document.getElementById("mon-jobs").value;
    var jobs = jobsValue === "yes" || jobsValue === "na";
    var alerts = yes("mon-alerts");
    var notify = yes("mon-notify");
    var owner = yes("mon-owner");

    var result;

    if (!external || !metrics || !app || !disk) {
      result = "BLIND SPOTS: the monitoring stack cannot yet see one or more fundamental failure modes. Add independent availability checks, retained host metrics, disk/inode visibility and real service/application health checks.";
    } else if (!alerts || !notify || !owner) {
      result = "ALERTING / OWNERSHIP INCOMPLETE: the data may exist, but an incident can still remain unnoticed or unowned. Add actionable alerts, an independent notification path and a named response runbook.";
    } else if (!jobs && (workload === "transactional" || workload === "cms" || workload === "multi")) {
      result = "BASIC MONITORING: infrastructure monitoring is present, but application jobs/database/backup freshness are still a blind spot for this workload.";
    } else {
      result = "PRODUCTION MONITORING BASELINE: external availability, retained metrics, service health, alerts and response ownership are present. Continue tuning thresholds from real baselines; this is not a guarantee of uptime.";
    }

    document.getElementById("vps-monitoring-result").textContent = result;
  });
});
</script>

## Monitor the website from outside the VPS

An internal command can tell you that Nginx is running. It cannot prove that a real user on the internet can reach the website.

Use an external monitor for important hostnames.

Useful checks include:

- HTTP/HTTPS availability;
- expected status code;
- response time;
- keyword/content check;
- DNS resolution;
- TLS certificate status/expiry;
- TCP port checks where relevant.

Where false positives matter, require repeated failures or confirmation from more than one location before paging somebody.

Self-hosted tools such as Uptime Kuma can perform HTTP(S), keyword, TCP, ping and DNS checks, but place the monitor outside the failure domain of the production VPS.

A monitoring server that shares the same VPS, provider network or DNS failure can be useful for dashboards, but it is not an independent availability check.

## Real-time diagnostics are not historical monitoring

Commands such as:

```bash
top
htop
free -h
df -h
ss -s
```

are useful when you are already investigating a problem.

They do not tell you:

- what happened at 03:12;
- whether RAM grew steadily for six hours;
- whether disk latency spiked during a backup;
- whether the website was down for ten minutes;
- whether a problem is getting worse week by week.

Retain time-series history for the signals that affect uptime and capacity.

For a single VPS, a lightweight monitoring agent may be enough. For a fleet or longer retention/custom dashboards, Prometheus + Node Exporter + Grafana is a common architecture.

Prometheus Node Exporter exposes host/kernel metrics that Prometheus can scrape, including CPU, filesystem and network data.

## Monitor CPU, memory, disk and network

### CPU

Do not alert on every short spike.

Watch:

- sustained CPU utilization;
- load average relative to vCPU count;
- per-process CPU;
- CPU steal time where exposed by the virtualization stack;
- application/request latency at the same time.

A brief 100% burst during cache warm-up or a cron task can be harmless. Sustained CPU saturation plus growing latency/queues is stronger evidence of a real bottleneck.

### Memory, swap and OOM

Linux often uses spare RAM for filesystem cache, so “90% RAM used” is not automatically a failure.

Watch:

- available memory;
- swap activity;
- swap growth;
- OOM-killer events;
- process memory growth;
- PHP/app worker memory;
- database memory.

A memory leak may look normal at noon and kill the process overnight. Historical trend data is what exposes it.

### Disk capacity

Watch filesystem utilization before it reaches the point where databases, logs or package updates fail.

An illustrative starting warning/critical pair might be **80% / 90% used**, but this is not a universal SLA. A rapidly growing database may need much earlier action.

Also monitor free working space required by:

- backups;
- database maintenance;
- package updates;
- uploads;
- logs;
- staging/import jobs.

### Inodes

A filesystem can run out of inodes while many GB remain free.

This can happen with:

- cache directories;
- sessions;
- mail queues;
- huge numbers of tiny files;
- runaway temporary files.

Track inode use separately from disk GB.

### Disk I/O and latency

Disk can become the bottleneck before capacity is full.

Watch:

- I/O wait;
- read/write latency;
- queue depth where available;
- database response time;
- backup/import windows.

A larger disk capacity does not automatically fix slow storage I/O.

### Network

Track more than total bandwidth:

- inbound/outbound throughput;
- sudden traffic changes;
- connection errors;
- packet loss/latency where measurable;
- unusual outbound traffic;
- interface errors.

Network metrics help separate application slowness from provider/path problems.

## Monitor services and application health

A VPS can be reachable while the website is broken.

Monitor important services such as:

- Nginx/Apache;
- PHP-FPM;
- Node/Python application service;
- MySQL/MariaDB/PostgreSQL;
- Redis where used;
- queue workers;
- scheduled-job service;
- control panel where business-critical.

On systemd-based Linux, `systemctl --failed` is useful during diagnosis, but continuous monitoring should alert on failed or repeatedly restarting required services.

Do not stop at “process exists.” A process can be alive but unable to serve valid requests.

## HTTP 200 is not always healthy

An application can return HTTP 200 with:

- maintenance page;
- database error rendered inside a template;
- empty/incorrect content;
- broken login flow;
- stale cache.

For critical sites, use the narrowest useful check:

- expected keyword/text;
- health endpoint;
- API response;
- critical public URL;
- synthetic login/transaction only when the business value justifies the complexity.

Do not make synthetic checks mutate production data unless they are specifically designed to do so safely.

## Monitor TLS and DNS

The VPS can be healthy while the website is unavailable because of certificate or DNS failure.

Track:

- certificate expiration;
- certificate hostname mismatch;
- failed renewal;
- DNS resolution;
- accidental record changes where tooling supports it.

A useful example is to warn well before certificate expiry, such as **14 days**, then escalate closer to expiry, such as **7 days**. The exact window should match how quickly somebody can fix renewal.

## Monitor the database as an application dependency

For database-backed websites, monitor enough to tell whether the DB is the bottleneck or failed dependency.

Depending on the engine/workload, useful signals include:

- service availability;
- connection count;
- connection errors;
- query latency;
- locks/contention symptoms;
- slow-query activity;
- memory pressure;
- storage growth;
- replication/backup status where used.

Do not alert on every DB metric. Alert on conditions tied to user impact or a known failure mode.

For WordPress workload behavior, see [VPS for WordPress]({{< relref "vps-for-wordpress.md" >}}). For transactional store workload, see [VPS for WooCommerce]({{< relref "vps-for-woocommerce.md" >}}).

## Monitor cron, queues and background jobs

A green homepage does not prove background work is healthy.

Track jobs that matter to the application:

- cron;
- queue workers;
- scheduled imports;
- webhooks;
- email jobs;
- WordPress WP-Cron/system cron;
- WooCommerce Action Scheduler;
- subscriptions/renewals;
- inventory sync.

Useful signals:

- last successful run;
- queue depth/backlog;
- failed jobs;
- oldest pending job;
- repeated retries;
- worker stopped/restarting.

For WooCommerce, a growing failed/past-due Action Scheduler queue can be an operational problem even if catalog pages still load.

## Monitor backup freshness

A backup job belongs to the recovery strategy, but **backup freshness is a monitoring signal**.

Alert when:

- scheduled backup fails;
- latest successful backup is older than the defined RPO;
- DB dump fails;
- offsite upload fails;
- repository credentials expire;
- backup size changes suspiciously;
- prune/retention job fails.

Do not treat “cron ran” as proof that a usable backup exists.

For RPO/RTO, retention, independent copies and restore drills, use [VPS Backup Strategy]({{< relref "vps-backup-strategy.md" >}}).

## Correlate logs with metrics

Metrics tell you **what changed**. Logs often tell you **why**.

Correlate the same time window across:

- Nginx/Apache access/error logs;
- PHP-FPM/runtime logs;
- application logs;
- database logs;
- system journal;
- authentication logs;
- backup/job logs.

Example:

- CPU spikes at 14:03;
- 5xx rises at 14:03;
- application log shows DB timeouts;
- DB log shows lock contention.

That is more actionable than a generic “CPU high” alert.

Keep enough log retention to investigate incidents, but do not let logs fill the production filesystem.

## Build actionable alerts

An alert should tell the operator what failed and what to check first.

Prefer:

- **warning** — investigate before user impact;
- **critical** — user impact or imminent failure;
- duration/debounce — avoid paging on one-second spikes;
- grouping/deduplication — avoid 40 notifications for one outage;
- clear affected host/service;
- link to dashboard/log/runbook;
- known first action/escalation.

Prometheus Alertmanager is an example of a system designed to group, deduplicate and route alerts.

### Avoid universal thresholds

Thresholds should match the workload.

Examples of reasonable starting logic:

- CPU: sustained high utilization + latency/queue symptoms rather than isolated spike;
- RAM: low available memory + swap/OOM rather than “used RAM > 80%” alone;
- disk: early warning while enough operating headroom remains;
- TLS: warn days before expiry;
- HTTP: repeated failure or multi-location confirmation where false positives matter;
- backup: latest success older than RPO;
- 5xx/latency: sustained deviation from the application's normal baseline.

Tune after observing normal production behavior.

## Keep the notification path independent

An alert is useless if its delivery system dies in the same incident.

Where practical, send important alerts through a path outside the VPS:

- external email provider;
- external chat/notification service;
- hosted incident tool;
- a monitoring instance in another failure domain.

Do not rely only on an SMTP server or dashboard hosted on the same broken VPS.

## Every alert needs an owner and runbook

Before creating an alert, answer:

- who receives it?
- who is allowed to act?
- what is the first diagnostic step?
- what dashboard/log should be opened?
- when is it escalated?
- when is it safe to silence?
- what happens outside business hours?

If nobody owns the response, the monitoring system has only converted an outage into a notification.

For the broader operations-responsibility decision, see [Managed vs Unmanaged VPS]({{< relref "managed-vs-unmanaged-vps.md" >}}).

## Choose the monitoring stack by complexity

Do not deploy a large observability platform because it is popular.

### Provider dashboard as a starting layer

If the VPS provider exposes CPU, RAM, disk or network history, use it as a convenient host-level starting layer.

Do not confuse provider-side infrastructure charts with complete website monitoring. They may not verify the public HTTP(S) path from outside the provider, application content, database health, background jobs, TLS renewal or alert ownership.

Treat provider monitoring as one source of evidence, then add the external and application-level checks required by the workload.

### Lightweight single-VPS path

A practical small setup can combine:

- external uptime monitor;
- Netdata or another host-metric agent/dashboard;
- system/application logs;
- notifications.

Good when one operator manages one or a few VPS instances.

### Prometheus / Grafana path

Useful when you need:

- multi-server metrics;
- longer historical retention;
- custom queries;
- service/exporter metrics;
- shared dashboards;
- structured alert rules.

Node Exporter supplies Linux host metrics; Prometheus stores/queries them; Grafana visualizes them; Alertmanager can route/group/deduplicate alerts.

### Hosted monitoring path

Useful when:

- the monitor must be independent of your VPS/provider;
- you want less monitoring infrastructure to operate;
- managed notifications/on-call integrations are valuable.

The monitoring system itself is production infrastructure. Keep its complexity proportional to the risk it reduces.

## Secure the monitoring stack

Monitoring agents and dashboards can expose sensitive operational data.

Protect:

- dashboards;
- exporters;
- metrics endpoints;
- API tokens;
- notification webhooks;
- log backends.

Do not expose Prometheus, Node Exporter, Grafana or admin dashboards openly to the internet without an explicit secured access model.

Use firewall/private-network/reverse-proxy authentication as appropriate.

Monitoring does not replace hardening; use [VPS Security Checklist]({{< relref "vps-security-checklist.md" >}}) for the server baseline.

## Monitoring overhead matters

Monitoring consumes:

- RAM;
- CPU;
- disk for metrics/log retention;
- network;
- backup capacity.

A small agent is usually cheap, but long-retention metrics/logs can become a real storage workload.

Watch the monitoring stack itself:

- agent/service health;
- scrape failures;
- storage growth;
- retention;
- notification delivery.

Do not let observability fill the disk it is supposed to protect.

## Use trends for capacity planning

Historical monitoring is the best evidence for the next sizing decision.

Use trends to answer:

- is CPU saturation sustained or occasional?
- is available RAM shrinking over weeks?
- is swap/OOM appearing under legitimate load?
- how quickly is disk growing?
- does DB latency rise during peak traffic?
- do PHP/app queues form?
- are backup/import jobs creating predictable contention?

Do not upgrade merely because one dashboard briefly turned red.

Scale when the **optimized legitimate workload** repeatedly exhausts a resource or when the architecture needs independent scaling.

Use [VPS sizing for website]({{< relref "vps-sizing-for-website.md" >}}) to translate monitoring evidence into a resource decision.

<p>
  <a class="btn btn-primary" href="https://www.vdsina.com/?partner=ni8gzrvz75" target="_blank" rel="sponsored nofollow noopener">Check current VPS configurations</a>
</p>
<p><small>Disclosure: the editor has a professional relationship with VDSina, and this site may earn a commission if you order through this partner link. Monitoring data should drive the sizing decision; this page does not claim that VDSina provides the monitoring tools described above as a managed service.</small></p>

## Monitor multiple websites at two levels

On a multi-site VPS, monitor:

### Server level

- CPU/RAM/swap;
- disk/inodes/I/O;
- database;
- network;
- core services.

### Site level

- each important hostname;
- TLS;
- response time;
- 5xx;
- app/job failures;
- per-site logs or worker pressure where available.

A server can be healthy while one virtual host, certificate or website is broken.

Use [VPS for Multiple Websites]({{< relref "vps-for-multiple-websites.md" >}}) for the consolidation/failure-domain decision.

## VPS monitoring checklist

| Signal | Pass condition |
|---|---|
| External uptime | important hostname checked from outside the VPS |
| HTTP health | expected status/content/health endpoint validated |
| CPU | sustained utilization/load/per-process history retained |
| RAM | available memory, swap and OOM visible |
| Disk | capacity + growth monitored |
| Inodes | inode exhaustion monitored separately |
| I/O | latency/I/O wait visible when storage matters |
| Network | throughput/errors/path symptoms observable |
| Services | web/runtime/DB/worker health monitored |
| Database | availability/latency/connections relevant to app visible |
| Jobs | cron/queue/background failures or backlog observable |
| TLS/DNS | expiry and resolution failures detectable |
| Backups | latest-success age and job failures monitored |
| Logs | web/app/DB/system logs available for incident correlation |
| Alerts | warning/critical + duration/debounce rules configured |
| Notification | important alerts leave the VPS failure domain |
| Ownership | named responder + first-action runbook |
| Retention | enough metric/log history for trend and root-cause analysis |
| Security | monitoring endpoints/dashboards not unintentionally public |
| Capacity | trends feed the next optimize/scale decision |

## Technical references

- Prometheus — monitoring Linux host metrics with Node Exporter
- Prometheus — Alertmanager
- Uptime Kuma — official project
- [VPS Backup Strategy]({{< relref "vps-backup-strategy.md" >}})
- [VPS Security Checklist]({{< relref "vps-security-checklist.md" >}})

## FAQ

### What should I monitor on a VPS?

At minimum monitor external website availability, CPU, available RAM/swap/OOM, disk capacity, inodes, core services, application health, TLS expiry, backup freshness and alert delivery.

### Is CPU over 80% always bad?

No. Short high-CPU bursts can be normal. Investigate sustained utilization together with load, request latency, queues and the process doing the work.

### Why is Linux RAM almost full?

Linux uses free memory for cache. Monitor available memory, swap activity, OOM events and process growth rather than alarming on used percentage alone.

### What should I monitor for disk problems?

Monitor filesystem capacity, inode use, storage growth and I/O latency/wait. Free GB alone does not cover every disk failure mode.

### Is ping enough for uptime monitoring?

No. Ping can succeed while the website, database or TLS path is broken. Use HTTP(S) and application/service checks for user-facing health.

### Should the uptime monitor run on the same VPS?

Not as the only monitor. A complete VPS or network failure can take the monitor down with the website. Keep at least the critical availability/notification path outside that failure domain.

### Which VPS monitoring tool is best?

There is no universal best tool. A single VPS may need only external uptime plus a lightweight host-metric agent. A fleet may justify Prometheus, Grafana and Alertmanager. Choose by required visibility, retention and operating complexity.

### Do I need Prometheus and Grafana for one VPS?

Not necessarily. They are powerful when you need long-term metrics, custom queries and multiple servers, but a lightweight agent plus external uptime monitoring can be enough for a small deployment.

### How should I monitor backups?

Alert on failed jobs and on the age of the latest successful backup compared with the RPO. Then verify recoverability separately with restore tests.

### When should monitoring trigger a VPS upgrade?

When historical evidence shows that an optimized legitimate workload repeatedly exhausts CPU, RAM, storage/I/O or another resource. One isolated spike is not enough evidence.
