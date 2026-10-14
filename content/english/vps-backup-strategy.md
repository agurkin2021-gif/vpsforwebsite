---
title: "VPS Backup Strategy"
description: "VPS Backup Strategy: define RPO and RTO, combine provider images with independent offsite backups, protect databases and secrets, set retention, and prove recovery with restore tests."
image: "images/home/vps-for-website-hero.webp"
---

VPS Backup Strategy is not “turn on snapshots once a day.” A usable recovery plan defines **how much data you can lose (RPO), how long recovery may take (RTO), which data must survive, where independent copies live, how long versions are retained, and whether anybody has actually restored them**.

A strong VPS plan usually combines fast provider-side recovery with an independent off-server copy and application-aware database backups. The exact mix depends on how quickly the data changes and how costly downtime is.

Backup strategy also needs a named owner. If nobody is responsible for job failures, restore tests and recovery decisions, resolve that operating model first: see [Managed vs Unmanaged VPS]({{< relref "managed-vs-unmanaged-vps.md" >}}).

For the broader server decision, see [VPS for website]({{< relref "_index.md" >}}).

[Quick answer](#quick-answer) · [Checker](#vps-backup-strategy-checker) · [RPO / RTO](#start-with-rpo-and-rto) · [Backup layers](#snapshot-image-file-backup-and-replication-are-different) · [3-2-1](#a-practical-3-2-1-model-for-vps) · [Restore tests](#test-restores-and-measure-real-rto) · [VDSina](#how-vdsina-backups-fit-the-strategy) · [FAQ](#faq)

## Quick answer

A practical VPS recovery design has several layers:

| Layer | Main job | What it does not prove |
|---|---|---|
| **Provider backup image / snapshot** | fast full-server rollback or rebuild | independent recovery if the provider account/storage is unavailable |
| **Database-consistent backup** | recover application state and recent writes | complete server configuration by itself |
| **File/config backup** | restore uploads, configs, app data and selected files | fast whole-server recovery |
| **Independent offsite copy** | survive primary provider/account/server failure | low RTO unless restore is rehearsed |
| **Restore drill** | prove the copies, keys and runbook actually work | future backups will keep working unless monitored |

For many ordinary website VPS deployments, a good baseline is:

- provider-side image/snapshot for fast rollback;
- encrypted independent backup of files/config/database to another failure domain;
- multiple restore points;
- database backup frequency chosen from acceptable data loss;
- regular restore tests.

That is more useful than relying on one “successful backup” status.

## VPS Backup Strategy Checker

This checker identifies the recovery architecture you need. It does not guarantee recovery.

<div class="rounded-2xl bg-light p-6 dark:bg-darkmode-light">
<form id="vps-backup-strategy-checker-form">
  <div class="mb-6">
    <label for="bk-workload" class="form-label">Workload type</label>
    <select id="bk-workload" class="form-input">
      <option value="static">Static / brochure / rarely changing site</option>
      <option value="cms">WordPress / CMS / business website</option>
      <option value="transactional">WooCommerce / orders / membership / frequent writes</option>
    </select>
  </div>
  <div class="mb-6">
    <label for="bk-rpo" class="form-label">Maximum acceptable data loss (RPO)</label>
    <select id="bk-rpo" class="form-input">
      <option value="24">Up to 24 hours</option>
      <option value="4">Up to 4 hours</option>
      <option value="1">Up to 1 hour</option>
      <option value="lt1">Less than 1 hour</option>
    </select>
  </div>
  <div class="mb-6">
    <label for="bk-rto" class="form-label">Maximum acceptable downtime (RTO)</label>
    <select id="bk-rto" class="form-input">
      <option value="24">Up to 24 hours</option>
      <option value="4">Up to 4 hours</option>
      <option value="1">Around 1 hour</option>
      <option value="lt1">Less than 1 hour</option>
    </select>
  </div>
  <div class="mb-6">
    <label for="bk-offsite" class="form-label">Independent off-server / offsite copy exists?</label>
    <select id="bk-offsite" class="form-input"><option value="no">No</option><option value="yes">Yes</option></select>
  </div>
  <div class="mb-6">
    <label for="bk-db" class="form-label">Database-consistent backup method verified?</label>
    <select id="bk-db" class="form-input">
      <option value="na">Not applicable / no database</option>
      <option value="no">No / unknown</option>
      <option value="yes">Yes</option>
    </select>
  </div>
  <div class="mb-6">
    <label for="bk-restore" class="form-label">Recent restore test completed successfully?</label>
    <select id="bk-restore" class="form-input"><option value="no">No</option><option value="yes">Yes</option></select>
  </div>
  <div class="mb-6">
    <label for="bk-creds" class="form-label">Backup credentials / encryption recovery key are separated from the VPS?</label>
    <select id="bk-creds" class="form-input"><option value="no">No / unknown</option><option value="yes">Yes</option></select>
  </div>
  <div class="mb-6">
    <label for="bk-versions" class="form-label">Multiple restore points / retention history available?</label>
    <select id="bk-versions" class="form-input"><option value="no">Only latest / unknown</option><option value="yes">Yes</option></select>
  </div>
  <button class="btn btn-primary" type="submit">Check backup strategy</button>
</form>
<p id="vps-backup-strategy-result" class="mt-6 rounded border border-border p-4 dark:border-darkmode-border" role="status" aria-live="polite">Choose the recovery requirements that actually apply.</p>
</div>

<script>
document.addEventListener("DOMContentLoaded", function () {
  var form = document.getElementById("vps-backup-strategy-checker-form");
  if (!form) return;

  form.addEventListener("submit", function (event) {
    event.preventDefault();

    function val(id) { return document.getElementById(id).value; }

    var workload = val("bk-workload");
    var rpo = val("bk-rpo");
    var rto = val("bk-rto");
    var offsite = val("bk-offsite") === "yes";
    var db = val("bk-db");
    var restore = val("bk-restore") === "yes";
    var creds = val("bk-creds") === "yes";
    var versions = val("bk-versions") === "yes";

    var criticalGap = !offsite || !restore || !creds || !versions || (db === "no");
    var result;

    if (criticalGap) {
      result = "CRITICAL BACKUP GAPS: the strategy still depends on an unproven or non-independent recovery path. Add offsite/independent copies, multiple restore points, separated recovery credentials/keys, database-consistent backup where required, and a real restore test.";
    } else if (rto === "lt1" || rto === "1") {
      result = "LOW-RTO / RECHECK DR ARCHITECTURE: backups may be correct, but a manual rebuild can still miss a one-hour recovery target. Time a full recovery drill and consider automation, prebuilt images, warm standby or workload separation if the measured RTO is too slow.";
    } else if (workload === "transactional" || rpo === "lt1" || rpo === "1") {
      result = "TRANSACTIONAL / FREQUENT-DB-BACKUP PATH: keep the independent recovery layers, but set database protection frequency to meet the required RPO. A nightly backup cannot satisfy a one-hour data-loss target.";
    } else {
      result = "BASIC RECOVERY STRATEGY: the core layers are present. Keep provider recovery points plus independent offsite backups, monitor job failures, retain multiple versions and repeat timed restore drills.";
    }

    document.getElementById("vps-backup-strategy-result").textContent = result;
  });
});
</script>

## Start with RPO and RTO

Two numbers should drive the strategy.

### Recovery Point Objective — RPO

RPO answers:

**How much recent data can the business afford to lose?**

If the RPO is:

- **24 hours** — a daily successful recovery point may be acceptable;
- **4 hours** — daily backups are insufficient;
- **1 hour** — the changing application/database state needs protection at least that frequently;
- **minutes** — ordinary scheduled backups alone may not be enough.

RPO is about **data loss**, not downtime.

### Recovery Time Objective — RTO

RTO answers:

**How long may the website/service remain unavailable?**

A backup can meet the RPO and still fail the RTO.

Example:

- database copied every hour;
- most recent data loss is under one hour;
- but reprovisioning the VPS, downloading data, restoring the DB and validating the site takes six hours.

That strategy may satisfy a one-hour RPO but has an actual RTO near six hours.

NIST contingency-planning guidance defines RPO as the recovery point in time and RTO as the maximum acceptable unavailability window. Use those targets before choosing tools.

## What should be backed up?

Classify the server into **rebuildable** and **stateful/irreplaceable** parts.

### Rebuildable

Often reproducible from code or automation:

- base operating system;
- packages;
- application code already stored safely in Git;
- container images that can be rebuilt/pulled;
- standard web-server packages.

### Stateful / difficult to recreate

Usually higher priority:

- databases;
- user uploads/media;
- mailboxes if hosted locally;
- configuration;
- environment/secrets required for recovery;
- TLS/private keys where replacement is not trivial;
- application-generated data;
- control-panel/site configuration;
- cron/worker configuration;
- DNS zone data if DNS is hosted on the VPS;
- custom scripts not stored elsewhere.

Do not waste backup capacity blindly copying caches, temporary files and rebuildable artifacts while forgetting the database or secrets needed to start the site.

## Snapshot, image, file backup and replication are different

Do not treat these as interchangeable.

### Provider snapshot / server image

Useful for:

- fast rollback after a risky update;
- full-server recovery;
- cloning/recreating the VM.

Weaknesses:

- may live in the same provider/account failure domain;
- may not provide granular file/site restore;
- application/database consistency must still be understood;
- one latest image gives little history.

### File-level backup

Useful for:

- uploads;
- configuration;
- selected application data;
- granular restore.

Tools such as restic or Borg can store encrypted versioned backups on remote repositories.

### Database backup

Use an engine-aware method:

- logical dump;
- native backup tool;
- application-consistent snapshot/process.

Do not assume copying live database files produces a usable database backup.

### Replication / standby

Replication can reduce recovery time or data loss, but it is not historical backup by itself.

A bad delete, corruption or application error can be replicated too.

Use replication/standby for availability/RTO when required, and keep versioned backups for historical recovery.

## A practical 3-2-1 model for VPS

The common 3-2-1 model means:

- **3 copies** of important data;
- **2 different storage/failure modes**;
- **1 copy offsite / outside the main failure domain**.

For a VPS, a practical interpretation might be:

1. production data on the VPS;
2. provider backup image for fast recovery;
3. encrypted offsite file/database backup in an independent destination.

The goal is not to satisfy a slogan literally. The goal is to avoid one event destroying production and every recovery copy.

Examples of failure domains:

- the VPS filesystem;
- provider backup storage;
- the provider account;
- a separate object-storage account/provider;
- an offline or immutable copy.

If an attacker who controls the VPS can delete every backup using the same credentials, the copies are not meaningfully independent.

## Database-consistent backups

Database state changes while the site is live.

A valid strategy should know how the DB engine is protected.

For WordPress/MySQL/MariaDB this may be:

- logical dumps;
- native DB backup tooling;
- coordinated snapshots;
- backup software that explicitly handles database consistency.

For PostgreSQL, use PostgreSQL-aware backup/PITR methods where the RPO requires them.

The point is not the exact tool. The point is that the restored DB must be internally coherent and usable.

For WordPress-specific application state and operations, see [VPS for WordPress]({{< relref "vps-for-wordpress.md" >}}).

Test:

- dump/backup completes;
- file is non-empty;
- restore/import succeeds;
- representative tables/records exist;
- application can connect and perform critical reads/writes.

## Transactional sites need a different RPO

A brochure site may tolerate a day-old copy.

A transactional store may not.

For WooCommerce, membership, billing or order systems, define how much recent state may be lost:

- orders;
- payments;
- stock;
- customers;
- memberships;
- form submissions;
- uploads.

If a store receives orders every hour, a nightly DB backup can lose many transactions.

Use [VPS for WooCommerce]({{< relref "vps-for-woocommerce.md" >}}) for the store workload. The backup schedule here should be chosen from the acceptable transaction-loss window.

## Backup frequency and retention

Backup frequency should be no slower than the RPO for the data class it protects.

Different data can use different schedules:

- DB: frequent;
- uploads: frequent or event-driven;
- OS/config: after important changes + scheduled;
- full provider image: less frequent but useful around risky changes.

Retention protects against failures discovered late.

One illustrative pattern might keep:

- recent hourly restore points;
- several daily copies;
- several weekly copies;
- selected monthly copies.

The exact retention should come from:

- business recovery needs;
- storage cost;
- data-change rate;
- compliance/legal requirements;
- how long corruption or compromise may remain unnoticed.

Do not keep only “latest”.

## Keep an independent off-server destination

A backup on the same VPS disk does not protect against:

- disk/filesystem loss;
- server deletion;
- root compromise;
- ransomware;
- account mistake;
- provider-side loss of that VM.

Move or stream recovery data outside the VPS.

Possible destinations:

- object storage;
- another backup service/provider;
- another VPS used only for backups;
- offline/controlled storage.

Separate provider/account credentials where practical.

## Encrypt backups — and protect the recovery key

Encrypt sensitive backup data in transit and at rest where appropriate.

But encryption creates another recovery dependency.

Do not store the **only** backup password/key:

- only on the VPS;
- only in the same password vault/account that might be unavailable;
- only inside the encrypted backup itself.

Keep recovery credentials/keys in a secure independent location and include key availability in restore drills.

## Separate backup credentials and deletion rights

A production-server compromise should not automatically give an attacker permission to erase every recovery copy.

Prefer:

- scoped backup credentials;
- write access without broad delete privileges where the storage supports it;
- separate administrative credentials;
- retention lock/immutability where appropriate;
- offline/air-gapped copy for high-value data.

The exact design depends on the storage service.

This is one reason backups are also a security control; see [VPS Security Checklist]({{< relref "vps-security-checklist.md" >}}).

## Monitor backup jobs

Automation reduces forgotten backups, but failed automation can fail silently.

Monitor:

- last successful backup time;
- failed/partial jobs;
- repository/storage availability;
- credential expiry;
- free disk before local staging;
- offsite storage quota;
- DB dump failures;
- backup duration changes;
- unusually small backup size;
- retention/prune failures.

A green cron/service status proves the command ran. It does not prove the restore works.

Broader server/service alert design belongs to [VPS Monitoring]({{< relref "vps-monitoring.md" >}}); backup-job health remains part of the recovery strategy itself.

## Test restores and measure real RTO

A backup becomes credible when it restores.

Run recovery drills into an isolated clean destination.

Test enough of the full sequence:

1. provision a fresh VPS/test environment;
2. retrieve the correct backup point;
3. retrieve encryption/repository credentials;
4. restore files/configuration;
5. restore/import the database;
6. restore required secrets/certificates;
7. configure services/networking;
8. start the application;
9. test important pages and transactions;
10. verify background jobs/integrations;
11. measure elapsed recovery time.

Record the measured result.

If the business RTO is four hours and the test takes eight, the backup strategy has failed the business requirement even if every file restored successfully.

NIST guidance emphasizes regular backup creation, restoration testing and recovery exercises.

## Restore granularity matters

A good strategy supports the failure you actually have.

### Single-file/site recovery

Needed for:

- deleted upload;
- broken config;
- one compromised site;
- one bad database/table recovery.

### Full-server recovery

Needed for:

- dead/deleted VPS;
- filesystem failure;
- severe compromise;
- provider/server replacement.

If the only backup is a full disk image, restoring one file may be inconvenient.

If the only backup is selected files, rebuilding the complete VPS may take too long.

Layer the methods.

## Multiple websites need site-level restore

On a multi-site VPS, do not design recovery so that fixing Site A automatically rolls Site B/C/D back to yesterday.

Prefer backups that let you restore:

- one document root;
- one database;
- one panel/user;
- one set of uploads;
- the full VPS only when required.

For the architecture/failure-domain decision, see [VPS for Multiple Websites]({{< relref "vps-for-multiple-websites.md" >}}).

## Backups can cause outages too

Backup work consumes resources.

Potential impact:

- DB dump CPU;
- compression CPU;
- read I/O;
- temporary disk usage;
- object-storage upload bandwidth;
- cache eviction;
- backup overlap with imports/scans/traffic peaks.

Avoid building a 30 GB local archive when the VPS has only 10 GB free.

Where practical:

- stream backups directly off-server;
- monitor temporary disk usage;
- schedule heavy backup work outside traffic peaks;
- rate-limit where the tool supports it;
- measure backup duration.

## How VDSina backups fit the strategy

VDSina's public documentation currently describes several useful recovery functions:

- manual server backup copies;
- scheduled backups;
- restore a backup to the server it came from;
- create a new server from a backup;
- clone a server;
- download a backup image.

The download documentation shows a backup filename in the form:

`vXXX.backup.hosted-by-vdsina.com.img.gz`

That downloadable image is a useful portability layer because a recovery copy does not have to remain only inside the provider panel.

However:

- treat the provider image as **one layer**, not the entire strategy;
- test how your chosen recovery environment uses the downloaded image;
- do not assume every hypervisor can consume it directly without conversion;
- keep application/file/database backups for granular recovery;
- keep an independent failure-domain copy where the risk justifies it.

VDSina's own Terms explicitly state that the customer is responsible for backups and recommends a routine backup process plus periodic restore testing.

When creating a new VDSina server from a provider backup, their QA notes that the backup/new server must meet provider constraints such as data-center placement and sufficient disk quota; network settings may also require adjustment after restoration.

Do not confuse backup with migration. A backup can be part of a migration safety net, but live cutover, final writes, DNS and rollback are separate concerns; see [Website migration to VPS]({{< relref "website-migration-to-vps.md" >}}).

<p>
  <a class="btn btn-primary" href="https://www.vdsina.com/?partner=ni8gzrvz75" target="_blank" rel="sponsored nofollow noopener">Check current VPS backup options</a>
</p>
<p><small>Disclosure: the editor has a professional relationship with VDSina, and this site may earn a commission if you order through this partner link. Provider backup features do not replace an independent recovery strategy or restore testing.</small></p>

## Recovery runbook

Write down the recovery process before the outage.

At minimum record:

- backup destinations;
- restore-point naming/retention;
- repository credentials;
- encryption-key recovery location;
- which data is DB/files/config;
- fresh-server provisioning steps;
- software/runtime versions;
- restore order;
- DNS/network steps;
- external integrations/webhooks;
- acceptance tests;
- who makes the recovery/rollback decision.

Keep the runbook somewhere available even when the VPS itself is unavailable.

## VPS backup checklist

| Control | Pass condition |
|---|---|
| RPO | maximum acceptable data-loss window defined |
| RTO | maximum acceptable downtime defined |
| Data inventory | DB, uploads, config, secrets and other state classified |
| Provider recovery | image/snapshot schedule understood |
| Database | engine-aware, restorable DB backup method |
| Offsite copy | independent recovery copy outside VPS failure domain |
| Credentials | backup account scoped/separated from production |
| Encryption | sensitive backups encrypted where appropriate |
| Key recovery | recovery key/password stored outside failed VPS |
| Retention | multiple historical restore points |
| Monitoring | failed/partial/stale backup jobs detected |
| Disk/I/O | backup process cannot silently fill/overload production |
| Granularity | file/site/DB restore possible where needed |
| Full recovery | complete VPS/service rebuild path exists |
| Restore test | isolated restore completed successfully |
| Measured RTO | actual recovery duration recorded and within target |
| Runbook | recovery order, credentials, DNS and acceptance tests documented |
| Owner | named person/team owns backup and restore work |

## Technical references

- NIST SP 800-34 Rev.1 — RPO/RTO and contingency planning
- NIST SP 1339 — backup creation, testing and recovery exercises
- Ubuntu — restic backup/restore tool
- Ubuntu — BorgBackup
- VDSina Terms — customer backup responsibility
- VDSina — server backup / restore / new server from backup
- VDSina — scheduled backups
- VDSina — download and use a server backup

## FAQ

### What is a good VPS backup strategy?

Define RPO/RTO, keep independent recovery copies, protect databases with an application-consistent method, retain multiple versions, monitor failed jobs and regularly restore into a clean test environment.

### Is a VPS snapshot enough?

Not as the only recovery layer. A provider snapshot/image is useful for fast rollback and full-server recovery, but it may share the same provider/account failure domain and is less convenient for granular restores.

### What does 3-2-1 mean for a VPS?

Keep the live data plus multiple recovery copies using independent storage/failure domains, with at least one copy outside the primary VPS/provider failure path.

### How often should I back up a VPS?

Choose frequency from the RPO of each data type. A static site may tolerate daily copies; a transactional database may require hourly or more frequent protection.

### What is the difference between RPO and RTO?

RPO is the maximum acceptable recent data loss. RTO is the maximum acceptable downtime until the service is restored.

### Should I back up the whole VPS or only website files?

Usually both layers are useful. A server image speeds full recovery; file/database backups make granular and application-consistent restores easier.

### How do I back up MySQL or PostgreSQL safely?

Use an engine-aware logical/native backup or coordinated application-consistent method, then prove it by restoring/importing into an isolated test environment.

### Should backups be encrypted?

Sensitive recovery data should be encrypted where appropriate, but keep the recovery password/key safely outside the failed VPS.

### Is replication a backup?

Not by itself. Replication can copy accidental deletion, corruption or malicious changes. Keep historical/versioned backups in addition to replication/standby.

### Does VDSina provide VPS backups?

VDSina documents manual and scheduled backup copies, restore/create-server-from-backup functions and downloadable backup images. Their Terms still place backup responsibility on the customer and recommend periodic restore testing.

### How often should I test restores?

On a defined schedule and after meaningful backup/architecture changes. High-value or rapidly changing systems should be tested often enough that the measured recovery process remains trustworthy.

### What if my RTO is under one hour?

A backup-only design may be too slow. Time a full recovery drill and consider automation, prebuilt recovery images, warm standby or architecture changes if the measured RTO misses the target.
