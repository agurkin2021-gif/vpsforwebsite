---
title: "VPS 모니터링"
slug: "vps-모니터링"
draft: true
description: "외부 가용성 점검, CPU·RAM·디스크·네트워크 지표, 서비스 상태, 로그와 대응 가능한 알림을 통해 VPS를 모니터링하는 방법. 도구, 임계값과 실무 체크리스트를 다룹니다."
image: "images/home/vps-for-website-hero.webp"
---

VPS 모니터링은 단순히 “서버가 켜져 있는가?”에 답하는 데 그쳐서는 안 됩니다. 운영 환경의 기본 모니터링에는 **외부 가용성 점검, 과거 서버 지표, 서비스와 애플리케이션 상태, 로그, 대응 가능한 알림, 명확히 지정된 담당자**가 필요합니다.

Nginx에 장애가 생기거나 데이터베이스가 멈추고 디스크가 가득 찼거나 TLS 인증서가 만료 직전이어도 VPS는 ping에 응답할 수 있습니다. 따라서 모니터링은 서버 자체뿐 아니라 사용자가 접속하는 웹사이트도 확인해야 합니다.

서버 선택의 전반적인 기준은 [웹사이트용 VPS]({{< relref "_index.md" >}})를 참고하세요.

[핵심 요약](#quick-answer) · [진단 도구](#vps-monitoring-baseline-checker) · [서버 지표](#monitor-cpu-memory-disk-and-network) · [애플리케이션 상태](#monitor-services-and-application-health) · [알림](#build-actionable-alerts) · [용량 계획](#use-trends-for-capacity-planning) · [FAQ](#faq)

## 핵심 요약 {#quick-answer}

실용적인 VPS 모니터링 구성은 다섯 계층으로 이루어집니다.

| 계층 | 확인할 수 있는 사항 | 감지할 수 있는 대표적인 장애 |
|---|---|---|
| **외부 가용성** | 사용자가 VPS 외부에서 웹사이트에 접속할 수 있는지 | VPS·네트워크·웹사이트 접속 불가 |
| **서버 지표** | CPU, RAM, 스왑, 디스크, inode, I/O, 네트워크의 추세 | 메모리 누수, 디스크 포화, 지속적인 CPU 부하 |
| **서비스·애플리케이션 상태** | 웹 서버, 실행 환경, DB와 핵심 엔드포인트가 실제로 작동하는지 | 서버는 온라인이지만 Nginx·PHP·DB·앱에 장애가 발생하는 상황 |
| **로그·이벤트** | 무엇이 변경되거나 실패했는지 | 5xx 급증, OOM, 워커 실패, DB 오류 |
| **알림 및 담당자** | 적절한 담당자에게 통보되어 조치할 수 있는지 | 아무도 모르는 장애 또는 방치된 대시보드 |

가용성 확인 도구를 감시 대상과 동일한 VPS에서만 실행하지 마세요. VPS나 네트워크 경로가 완전히 장애를 일으키면 감시 도구도 함께 중단될 수 있습니다.

## VPS 모니터링 기본 구성 진단 {#vps-monitoring-baseline-checker}

이 진단 도구로 모니터링 사각지대를 찾을 수 있습니다. 가동 시간을 보장하는 도구는 아닙니다.

<div class="rounded-2xl bg-light p-6 dark:bg-darkmode-light">
<form id="vps-monitoring-checker">
  <div class="mb-6">
    <label for="mon-workload" class="form-label">주요 워크로드</label>
    <select id="mon-workload" class="form-input">
      <option value="static">정적 / 단순 웹사이트</option>
      <option value="cms">WordPress / CMS</option>
      <option value="transactional">WooCommerce / 거래 처리 웹사이트</option>
      <option value="multi">여러 웹사이트 / 혼합 운영 환경</option>
    </select>
  </div>
  <div class="mb-6">
    <label for="mon-external" class="form-label">VPS 외부에서 HTTP(S) 가용성을 확인하고 있나요?</label>
    <select id="mon-external" class="form-input"><option value="no">No</option><option value="yes">Yes</option></select>
  </div>
  <div class="mb-6">
    <label for="mon-metrics" class="form-label">CPU/RAM/디스크/네트워크의 과거 지표를 보존하나요?</label>
    <select id="mon-metrics" class="form-input"><option value="no">No / only ad-hoc top/htop</option><option value="yes">Yes</option></select>
  </div>
  <div class="mb-6">
    <label for="mon-disk" class="form-label">디스크 용량, inode와 스토리지 부하를 감시하나요?</label>
    <select id="mon-disk" class="form-input"><option value="no">No / only free GB</option><option value="yes">Yes</option></select>
  </div>
  <div class="mb-6">
    <label for="mon-app" class="form-label">핵심 서비스와 애플리케이션 상태 점검이 설정되어 있나요?</label>
    <select id="mon-app" class="form-input"><option value="no">No / only ping</option><option value="yes">Yes</option></select>
  </div>
  <div class="mb-6">
    <label for="mon-jobs" class="form-label">해당하는 경우 DB / 큐 / cron / 최근 백업 상태를 감시하나요?</label>
    <select id="mon-jobs" class="form-input"><option value="no">No / unknown</option><option value="yes">Yes</option><option value="na">Not applicable</option></select>
  </div>
  <div class="mb-6">
    <label for="mon-alerts" class="form-label">심각도와 지속 시간 조건을 적용한 자동 알림이 있나요?</label>
    <select id="mon-alerts" class="form-input"><option value="no">No / dashboard only</option><option value="yes">Yes</option></select>
  </div>
  <div class="mb-6">
    <label for="mon-notify" class="form-label">이 VPS가 중단되어도 알림 경로가 유지되나요?</label>
    <select id="mon-notify" class="form-input"><option value="no">No / same VPS only</option><option value="yes">Yes</option></select>
  </div>
  <div class="mb-6">
    <label for="mon-owner" class="form-label">지정된 담당자와 최초 대응 절차서가 있나요?</label>
    <select id="mon-owner" class="form-input"><option value="no">No</option><option value="yes">Yes</option></select>
  </div>
  <button class="btn btn-primary" type="submit">모니터링 기본 구성 점검</button>
</form>
<p id="vps-monitoring-result" class="mt-6 rounded border border-border p-4 dark:border-darkmode-border" role="status" aria-live="polite">실제로 데이터를 수집하고 알림을 전달하는 항목만 선택하세요.</p>
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
      result = "사각지대 발견: 기본적인 장애 유형 중 일부를 아직 감지할 수 없습니다. 독립적인 가용성 점검, 과거 서버 지표, 디스크와 inode 모니터링, 실제 서비스 및 애플리케이션 상태 점검을 추가하세요.";
    } else if (!alerts || !notify || !owner) {
      result = "알림 / 책임 체계 미흡: 지표를 수집하더라도 장애가 감지되지 않거나 담당자가 없을 수 있습니다. 대응 가능한 알림, 독립적인 알림 경로와 담당자가 명시된 대응 절차서를 마련하세요.";
    } else if (!jobs && (workload === "transactional" || workload === "cms" || workload === "multi")) {
      result = "기본 모니터링: 인프라 감시는 마련되어 있지만 이 워크로드의 애플리케이션 작업, 데이터베이스 또는 최근 백업 상태는 여전히 사각지대입니다.";
    } else {
      result = "운영 환경의 기본 모니터링 확보: 외부 가용성, 과거 지표, 서비스 상태, 알림과 대응 담당자가 마련되어 있습니다. 실제 정상 상태를 기준으로 임계값을 계속 조정하세요. 가동 시간을 보장하지는 않습니다.";
    }

    document.getElementById("vps-monitoring-result").textContent = result;
  });
});
</script>

## VPS 외부에서 웹사이트 모니터링 {#monitor-the-website-from-outside-the-vps}

내부 명령으로 Nginx가 실행 중인지 확인할 수는 있습니다. 하지만 인터넷의 실제 사용자가 웹사이트에 접속할 수 있는지는 증명하지 못합니다.

중요한 호스트 이름에는 외부 감시 도구를 사용하세요.

유용한 점검 항목은 다음과 같습니다.

- HTTP/HTTPS 가용성;
- 예상한 상태 코드;
- 응답 시간;
- 키워드·콘텐츠 점검;
- DNS 이름 해석;
- TLS 인증서 상태·만료일;
- 필요한 경우 TCP 포트 점검.

오탐의 영향이 크다면 담당자를 호출하기 전에 장애가 반복되는지 또는 둘 이상의 지역에서 동일한 문제가 확인되는지 검증하세요.

Uptime Kuma 같은 자체 호스팅 도구는 HTTP(S), 키워드, TCP, ping 및 DNS를 점검할 수 있습니다. 다만 감시 시스템은 운영 VPS와 독립된 장애 영역에 배치해야 합니다.

같은 VPS, 제공업체 네트워크 또는 DNS 장애에 영향을 받는 감시 서버는 대시보드 용도로 유용할 수 있지만 독립적인 가용성 점검으로 볼 수는 없습니다.

## 실시간 진단은 과거 지표 모니터링과 다릅니다 {#real-time-diagnostics-are-not-historical-monitoring}

다음과 같은 명령은:

```bash
top
htop
free -h
df -h
ss -s
```

이미 발생한 문제를 조사할 때 유용합니다.

그러나 다음 정보는 알려주지 못합니다.

- 03:12에 무슨 일이 있었는지;
- RAM 사용량이 6시간 동안 지속적으로 증가했는지;
- 백업 중 디스크 지연 시간이 급증했는지;
- 웹사이트가 10분 동안 중단되었는지;
- 문제가 주마다 악화되고 있는지.

가용성과 용량에 영향을 주는 지표는 시계열 이력을 보존하세요.

VPS 한 대라면 가벼운 모니터링 에이전트만으로 충분할 수 있습니다. 여러 서버, 장기 보존 또는 맞춤형 대시보드가 필요하면 Prometheus + Node Exporter + Grafana 구성이 흔히 사용됩니다.

Prometheus Node Exporter는 CPU, 파일시스템과 네트워크 데이터를 포함한 호스트·커널 지표를 Prometheus가 수집할 수 있도록 제공합니다.

## CPU, 메모리, 디스크와 네트워크 모니터링 {#monitor-cpu-memory-disk-and-network}

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
- DNS 이름 해석;
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
- 응답 시간;
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
