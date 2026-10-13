---
title: "VPS for Multiple Websites"
description: "Choose VPS resources for multiple websites by aggregate CPU, RAM, databases, PHP workers, backups and peak overlap."
---

One VPS can host several websites, but the useful limit is not a domain count. Size the server for the combined peak of every site sharing the machine.

## Count workload, not domains

Ten quiet sites can use fewer resources than one busy store.

Count:

- simultaneous PHP workers;
- database processes and caches;
- crawlers and scheduled jobs;
- backup and import activity;
- control-panel services;
- storage growth.

## Practical starting points

- **1 vCPU / 2 GB RAM / 40 GB** — several light sites with a lean stack.
- **2 vCPU / 4 GB RAM / 80 GB** — practical baseline for several modest business sites.
- **4 vCPU / 8 GB RAM / 160 GB** — heavier sites, stores or more background work.

## Web-server separation

Use separate virtual hosts or server blocks for each domain. Keep document roots, logs and certificates clear for every site.

Separate PHP pools can help when stronger process separation or different limits are useful.

## Databases

Use separate databases and credentials for separate applications even when one database server hosts them.

This makes permissions, backups and troubleshooting clearer.

## Recovery risk

Putting several sites on one VPS creates one failure domain. A server outage, storage problem or bad update can affect every hosted site.

Keep off-server backups and split critical workloads when one server failure would create unacceptable downtime.
