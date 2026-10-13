---
title: "VPS for WordPress"
description: "Choose VPS CPU, RAM and storage for WordPress by PHP workload, plugins, database demand, caching and growth."
---

A WordPress VPS should be sized around the work that bypasses cache: PHP workers, database queries, plugin activity, admin tasks, cron jobs and background processing.

## Practical starting points

- **1 vCPU / 2 GB RAM / 40 GB** — lean, well-cached WordPress site.
- **2 vCPU / 4 GB RAM / 80 GB** — practical baseline for a business WordPress site.
- **4 vCPU / 8 GB RAM / 160 GB** — heavier WordPress, several sites or more background work.

These are sizing directions, not guaranteed traffic capacities.

## RAM matters before visitor count

The WordPress or PHP memory limit is not the same as total server RAM. The VPS also needs memory for Linux, the web server, the database, cache, control panel and concurrent PHP workers.

A 2 GB VPS can work for a lean setup, but 4 GB gives materially more operating headroom for updates, admin activity and plugin jobs.

## PHP workers and uncached requests

Each uncached request can occupy a PHP worker. Logged-in users, wp-admin, API traffic and dynamic plugins can raise concurrency even when public pages are well cached.

Keep worker limits aligned with the RAM available to the whole server.

## Database workload

Slow or excessive queries can make WordPress CPU-bound or latency-bound before bandwidth becomes relevant.

Profile slow requests, remove unnecessary extensions and keep enough RAM available for the database working set.

## Background jobs

Backups, malware scans, imports, image processing and scheduled actions can overlap with live traffic. Stagger heavy work instead of letting every job run during the same peak period.

## When to upgrade

Upgrade after measuring a real constraint:

- sustained memory pressure or OOM events;
- CPU saturation during legitimate local processing;
- database latency caused by resource limits;
- storage growth that cleanup cannot solve.

A VPS gives WordPress more control. It does not automatically make inefficient code fast.
