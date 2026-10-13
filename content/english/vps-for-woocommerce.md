---
title: "VPS for WooCommerce"
description: "Choose VPS resources for WooCommerce by checkout concurrency, PHP workers, database writes, background jobs and store growth."
---

WooCommerce adds dynamic cart, checkout, account and order-processing work to WordPress. Size the VPS for simultaneous PHP and database activity, not just monthly visits.

## Practical starting points

- **1 vCPU / 2 GB RAM / 40 GB** — only for a small, lean store.
- **2 vCPU / 4 GB RAM / 80 GB** — practical baseline for a modest WooCommerce store.
- **4 vCPU / 8 GB RAM / 160 GB** — heavier store, more integrations or more concurrent dynamic work.

## Checkout is not a cached brochure page

Cart, checkout and account requests create live PHP and database work. They should not be sized from the same assumptions used for fully cached public content.

Watch concurrent PHP workers and uncached response time during real checkout peaks.

## Database work is customer-facing

Orders, sessions, carts, products and extensions create frequent database reads and writes.

Identify slow queries before buying more CPU. Give the database enough memory and avoid running large imports or backups during the busiest checkout window.

## Scheduled actions and integrations

Emails, imports, exports, inventory feeds, webhooks and maintenance can collide with customer traffic.

Stagger heavy jobs and review failed or backed-up scheduled actions.

## Caching

Cache public catalog content where appropriate, but do not full-page cache user-specific cart, checkout or account state.

Object caching can help some workloads, but measure whether it improves the actual database behavior.

## When to upgrade

Move to a larger VPS when monitoring shows sustained memory pressure, CPU saturation during legitimate dynamic work, request queues or database performance limited by the current server resources.
