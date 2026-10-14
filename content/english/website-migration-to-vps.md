---
title: "Website migration to VPS"
description: "Website migration to VPS: inventory the current stack, test the new server, control final writes, switch DNS safely, preserve email and SEO, and keep a rollback path."
image: "images/home/vps-for-website-hero.webp"
---

Website migration to VPS is safest when the new server is built and tested while the old host is still serving traffic. Inventory the current stack, size the destination, copy and validate the site, control the final data changes, switch DNS last, then monitor both environments until the old host can be retired.

This page assumes the domain and public URL structure stay the same. If the domain or paths also change, URL mapping and permanent redirects become a separate migration job.

For the broader hosting decision, see [VPS for website]({{< relref "_index.md" >}}).

[Quick plan](#quick-migration-plan) · [Preflight checker](#migration-cutover-preflight) · [Final sync](#control-new-writes-and-the-final-sync) · [DNS cutover](#switch-dns-deliberately) · [SEO checks](#preserve-seo-when-urls-stay-the-same) · [FAQ](#faq)

## Quick migration plan

A controlled move follows this order:

1. **Inventory the source.** Record the application, runtime, database, files, DNS, mail, cron jobs, workers, webhooks and external dependencies.
2. **Size the destination.** Choose CPU, RAM and disk from real workload and migration headroom.
3. **Create a recoverable backup.** Keep a copy outside the source server and verify that the database and files you need are actually present.
4. **Build the VPS in parallel.** Install the web stack or control panel and match the application requirements before traffic moves.
5. **Copy the first full dataset.** Transfer files and import the database while the old site remains live.
6. **Test privately.** Use a hosts-file override, controlled preview hostname or equivalent method to exercise the new server before DNS changes.
7. **Control the final writes.** For stores, memberships, forms and other changing sites, plan a short write freeze or an application-appropriate final delta sync.
8. **Switch DNS last.** Change only the records that need to move and keep mail/verification records intact.
9. **Monitor both servers.** Verify traffic, errors, forms, orders, cron jobs, webhooks, email, HTTPS and search crawling.
10. **Retire the old host only after acceptance.** Keep it available through the rollback window.

There is no honest universal promise of zero downtime. The goal is a controlled cutover with the smallest practical interruption and no unplanned data loss.

## Define what is actually moving

"Move the website" can include several different systems. Decide the scope before copying anything.

| Component | Questions to answer before the move |
|---|---|
| Website / application | CMS or framework, document root, uploads, hidden files, cache, writable directories |
| Runtime | PHP/Node/Python version, extensions/modules, web server, process manager |
| Database | engine/version, size, users/permissions, character set, scheduled maintenance |
| DNS | provider, A/AAAA/CNAME records, www/root behavior, TTL, verification records |
| Email | where mail is hosted, MX, SPF, DKIM, DMARC, mailboxes, forwarders, SMTP |
| Scheduled work | cron, queues, workers, imports, exports, backups, scheduled actions |
| External systems | payment webhooks, APIs, IP allowlists, CDN/WAF, analytics, Search Console |
| Security / secrets | environment variables, API keys, SSH keys, TLS, firewall rules |

Avoid combining unrelated changes without a reason. A host move is easier to diagnose when the domain, URL structure, application version and major software upgrades are not all changed at the same time.

## Migration cutover preflight

Use this checker before changing DNS. It does not guarantee a successful migration; it exposes missing prerequisites that should be resolved first.

<div class="rounded-2xl bg-light p-6 dark:bg-darkmode-light">
<form id="migration-preflight">
  <div class="mb-6">
    <label for="mig-backup" class="form-label">Independent backup exists and a restore/import was tested</label>
    <select id="mig-backup" class="form-input"><option value="no">Not ready</option><option value="yes">Ready</option></select>
  </div>
  <div class="mb-6">
    <label for="mig-sizing" class="form-label">Destination CPU, RAM and disk were sized with headroom</label>
    <select id="mig-sizing" class="form-input"><option value="no">Not ready</option><option value="yes">Ready</option></select>
  </div>
  <div class="mb-6">
    <label for="mig-runtime" class="form-label">Runtime, database and required extensions are compatible</label>
    <select id="mig-runtime" class="form-input"><option value="no">Not ready</option><option value="yes">Ready</option></select>
  </div>
  <div class="mb-6">
    <label for="mig-test" class="form-label">The new site was tested privately before DNS cutover</label>
    <select id="mig-test" class="form-input"><option value="no">Not ready</option><option value="yes">Ready</option></select>
  </div>
  <div class="mb-6">
    <label for="mig-dns" class="form-label">DNS records are documented and TTL/cutover are planned</label>
    <select id="mig-dns" class="form-input"><option value="no">Not ready</option><option value="yes">Ready</option></select>
  </div>
  <div class="mb-6">
    <label for="mig-mail" class="form-label">Email location and MX/SPF/DKIM/DMARC handling are decided</label>
    <select id="mig-mail" class="form-input"><option value="no">Not ready</option><option value="yes">Ready</option><option value="na">Not applicable / email is separate and unchanged</option></select>
  </div>
  <div class="mb-6">
    <label for="mig-writes" class="form-label">Final write/data-sync plan exists for orders, forms, members or uploads</label>
    <select id="mig-writes" class="form-input"><option value="no">Not ready</option><option value="yes">Ready / site is effectively read-only</option></select>
  </div>
  <div class="mb-6">
    <label for="mig-tls" class="form-label">HTTPS/TLS can work on the destination with the real hostname</label>
    <select id="mig-tls" class="form-input"><option value="no">Not ready</option><option value="yes">Ready</option></select>
  </div>
  <div class="mb-6">
    <label for="mig-jobs" class="form-label">Cron, workers, webhooks and IP allowlists are documented and controlled</label>
    <select id="mig-jobs" class="form-input"><option value="no">Not ready</option><option value="yes">Ready</option><option value="na">Not applicable</option></select>
  </div>
  <div class="mb-6">
    <label for="mig-rollback" class="form-label">Rollback trigger is defined and the old host will remain available</label>
    <select id="mig-rollback" class="form-input"><option value="no">Not ready</option><option value="yes">Ready</option></select>
  </div>
  <button class="btn btn-primary" type="submit">Check cutover readiness</button>
</form>
<p id="migration-preflight-result" class="mt-6 rounded border border-border p-4 dark:border-darkmode-border" role="status" aria-live="polite">Mark the items that are actually ready.</p>
</div>

<script>
document.addEventListener("DOMContentLoaded", function () {
  var form = document.getElementById("migration-preflight");
  if (!form) return;

  form.addEventListener("submit", function (event) {
    event.preventDefault();

    var items = [
      ["mig-backup", "independent backup"],
      ["mig-sizing", "destination sizing"],
      ["mig-runtime", "runtime/database compatibility"],
      ["mig-test", "private destination testing"],
      ["mig-dns", "DNS/TTL plan"],
      ["mig-mail", "email/DNS-mail plan"],
      ["mig-writes", "final write/data-sync plan"],
      ["mig-tls", "HTTPS/TLS readiness"],
      ["mig-jobs", "cron/workers/webhooks/allowlists"],
      ["mig-rollback", "rollback plan"]
    ];

    function isComplete(id) {
      var value = document.getElementById(id).value;
      return value === "yes" || value === "na";
    }

    var missing = items.filter(function (item) {
      return !isComplete(item[0]);
    }).map(function (item) {
      return item[1];
    });

    var result;
    if (missing.length === 0) {
      result = "READY FOR A CONTROLLED CUTOVER: all required items are marked ready or explicitly not applicable. Recheck the final data sync and rollback trigger immediately before DNS changes.";
    } else {
      result = "NOT READY FOR CUTOVER: close these gaps first: " + missing.join(", ") + ".";
    }

    document.getElementById("migration-preflight-result").textContent = result;
  });
});
</script>

## Inventory the current website

Create a migration record before touching the destination.

Record:

- domain and every active subdomain;
- application/CMS/framework version;
- PHP, Node.js, Python or other runtime version;
- database engine/version, size and credentials model;
- document root and directories outside it;
- uploads/media and writable directories;
- redirects and rewrite rules;
- cron jobs, queues, workers and scheduled tasks;
- caching services such as Redis where used;
- SSL/TLS configuration;
- DNS records;
- mailboxes, forwarders and outbound SMTP path;
- payment gateways, webhooks and API callbacks;
- third-party IP allowlists;
- CDN/WAF/origin restrictions;
- Search Console/analytics verification;
- current storage usage and growth.

The inventory is also the acceptance checklist after the move: every item should either work on the VPS or be deliberately left on an external service.

## Size and prepare the destination VPS

Do not migrate first and ask whether the VPS is large enough afterward.

Use the current workload, database behavior, storage growth, panel/mail overhead and migration working space to select the destination. The migration itself can need temporary disk for archives, database dumps, logs and local backup staging.

Use [VPS sizing for website]({{< relref "vps-sizing-for-website.md" >}}) for the resource calculation instead of duplicating it here.

A migration is also a management-path decision. If the old host hid most server administration, first decide who will operate the destination after cutover: compare [Managed vs Unmanaged VPS]({{< relref "managed-vs-unmanaged-vps.md" >}}). Then decide whether the destination will use a control panel or a manually managed Linux stack; see [VPS with Control Panel]({{< relref "vps-with-control-panel.md" >}}) for that choice.

<p>
  <a class="btn btn-primary" href="https://www.vdsina.com/?partner=ni8gzrvz75" target="_blank" rel="sponsored nofollow noopener">Choose the destination VPS</a>
</p>
<p><small>Disclosure: the editor has a professional relationship with VDSina, and this site may earn a commission if you order through this partner link. Migration guidance and sizing criteria do not change based on commission.</small></p>

## Create a rollback-capable backup

A backup is useful only if it contains the data you need and can be restored.

Before migration:

1. create a fresh copy of website files;
2. export every required database;
3. store a copy outside the source hosting account;
4. record configuration files and environment variables securely;
5. record DNS and mail records separately;
6. restore the backup into a disposable/test environment where practical, or at minimum perform a real database import and verify representative files instead of only checking that the archive opens;
7. confirm the restored copy contains the expected data and can start far enough to support rollback;
8. write down the rollback sequence before changing DNS.

For a dynamic site, the first backup is not the final production dataset. Orders, form submissions, comments, memberships or uploads can continue changing after the first copy. Plan the final delta separately.

## Build the destination before DNS changes

The destination must be able to run the site before public traffic arrives.

Match or deliberately validate:

- web server behavior;
- PHP/Node/Python version;
- required extensions/modules;
- database engine/version;
- file ownership and permissions;
- upload/body-size limits;
- scheduled-job environment;
- cache services;
- rewrite/redirect rules;
- environment variables and secrets;
- SMTP/outbound network needs;
- firewall rules;
- application-specific paths.

Do not use the migration itself as the moment to upgrade every runtime or rewrite the stack unless that change is required. Fewer simultaneous changes make rollback and diagnosis easier.

## Copy files and database

The exact transfer method depends on source access.

Typical source paths include:

- cPanel/File Manager + phpMyAdmin exports;
- SFTP/FTP when shell access is unavailable;
- SSH/rsync when both sides allow it;
- application-aware migration tools for CMS-specific moves;
- provider export/backup tools.

Preserve hidden configuration files such as rewrite rules where the application needs them. After import, verify the database user, privileges, character set/collation assumptions and application connection settings.

For large datasets, compare sizes, row counts or checksums where practical instead of assuming "transfer completed" means "dataset is identical."

## Test privately before cutover

Do not point DNS at an untested server.

Test the destination with a hosts-file override, controlled preview hostname or another private method that exercises the real application stack.

Check:

- homepage and representative internal pages;
- admin login;
- user login;
- images, CSS, JavaScript and downloads;
- search;
- forms and delivery;
- uploads;
- redirects;
- API endpoints;
- checkout and payment callbacks;
- cron/scheduled actions;
- queues/workers;
- outbound mail;
- application, web-server and database logs;
- mobile layout and navigation.

A temporary public hostname should not become an accidental duplicate in search. If it is publicly reachable during testing, keep it out of the index and remove temporary blocking from the real production hostname before cutover.

## Control new writes and the final sync

This is the most important difference between a brochure site and a transactional site.

If both old and new databases can accept writes during DNS transition, they can diverge. An order saved on the old server does not automatically appear on the new one.

For changing sites:

1. choose a low-risk cutover window;
2. pause or control new writes on the source when practical;
3. stop or control cron jobs and queue workers that could write data twice;
4. run the final database sync and copy changed uploads/files;
5. record the final source-of-truth time;
6. switch traffic;
7. verify that new writes now land only on the destination.

For [VPS for WooCommerce]({{< relref "vps-for-woocommerce.md" >}}), include checkout, orders, payment webhooks, stock, scheduled actions and transactional email in the acceptance test. A static/cached site may need only a final file comparison.

Do not call a migration "zero downtime" unless the application and synchronization method truly support it.

## Switch DNS deliberately

DNS is the traffic switch, not the first migration step.

Before cutover:

- export or record the current zone;
- identify exactly which A/AAAA/CNAME/origin records must change;
- lower the relevant TTL at least one full previous-TTL interval before the intended cutover when possible; for example, if the current TTL is 86,400 seconds, reduce it more than 24 hours before the switch;
- remember that lowering TTL now does not erase caches that already stored the older, longer TTL;
- preserve MX, SPF, DKIM, DMARC, verification TXT, SRV, CAA and other records that are not moving;
- verify both root and www behavior.

Changing an A/AAAA record is usually lower risk than replacing nameservers when the DNS provider itself is not changing. If nameservers do change, recreate the complete required zone first.

After the switch, verify public DNS from more than one resolver/network and watch traffic move from the old server to the new one.

## Keep email from breaking

Website migration and email migration are separate jobs even when the old shared-hosting account bundled them together.

Choose one path before cutover:

- keep mail with the current/managed provider and preserve the existing MX/TXT records;
- move mail to another managed provider;
- move mail onto the VPS and rebuild mailboxes, routing, authentication and deliverability controls.

If mail moves, account for:

- MX priorities;
- SPF;
- DKIM;
- DMARC;
- reverse DNS/PTR where applicable;
- mailbox data;
- aliases/forwarders;
- SMTP credentials;
- spam filtering;
- backups and sender reputation.

Do not replace an entire DNS zone just to move the website unless the mail records and all other dependencies are reproduced.

## Verify HTTPS, CDN and external services

If the destination region is still undecided, resolve that before cutover with [How to Choose VPS Location]({{< relref "how-to-choose-vps-location.md" >}}). Changing regions later can mean another IP/DNS migration.

A destination that works by IP can still fail under the real hostname.

Verify:

- TLS certificate covers the required hostnames;
- HTTP → HTTPS redirect is correct;
- root ↔ www canonical behavior is unchanged;
- HSTS assumptions are understood;
- CDN/WAF points to or permits the new origin;
- real client IP handling still works if proxied;
- payment webhooks reach the new origin;
- API providers that allowlist the old server IP are updated;
- SMTP/API credentials are valid from the new server.

Keep temporary firewall/WAF exceptions narrow and remove them after acceptance.

## Preserve SEO when URLs stay the same

A pure hosting change normally keeps the same public URLs. In that case, the SEO job is mostly **parity**, not redirect mapping.

Before and after cutover compare:

- HTTP status codes;
- canonical URLs;
- robots.txt;
- meta robots / accidental noindex;
- sitemap URLs;
- internal links;
- structured data where important;
- page content and rendered assets;
- Search Console verification;
- server responses to Googlebot and normal users.

Google Search Central recommends preparing and testing the new hosting, changing DNS only when ready, monitoring both old and new hosting, and retiring the old infrastructure after traffic has moved. It also recommends lowering DNS TTL in advance and keeping Search Console verification working.

If only the hosting infrastructure changes and the domain/URLs stay the same, **do not use Google Search Console's Change of Address tool**. That tool is for domain moves, not a same-URL hosting migration.

If the domain or URL paths change too, use an old-to-new URL map and permanent server-side redirects. That is a different site-move problem from a same-URL VPS migration.

## Cutover checklist

Immediately before DNS change:

| Check | Pass condition |
|---|---|
| Backup | independent copy exists; restore/import was tested and representative data was verified |
| Destination | correct runtime, database, permissions and secrets |
| Private test | pages, forms, login, checkout/API as applicable pass |
| Final data | final database/uploads delta complete; source-of-truth time recorded |
| Jobs | old cron/workers controlled; new jobs start at the intended time |
| DNS | exact records to change identified; mail/verification records preserved |
| HTTPS | destination can serve the real hostname securely |
| External services | webhooks, allowlists, CDN/WAF and SMTP accounted for |
| SEO parity | canonical/robots/sitemap/status behavior matches intent |
| Rollback | trigger, responsible action and old-host availability defined |

Do not switch because "the files copied." Switch because the destination passed the acceptance criteria.

## Post-migration acceptance and rollback

After DNS changes:

- monitor access/error logs on both old and new servers;
- confirm new user activity is reaching the destination database;
- test forms, checkout, logins and uploads again;
- verify cron, queues and scheduled actions;
- verify outbound email and inbound mail routing if relevant;
- watch CPU, RAM, disk and database behavior;
- confirm HTTPS and CDN/WAF behavior;
- check important URLs for 200/redirect parity;
- monitor Search Console crawling/indexing signals;
- keep the old environment available through the agreed stability window.

### Rollback has a data boundary

Early rollback can be as simple as pointing DNS back **only while the old server is still a valid source of truth**.

Once orders, registrations, comments or uploads are written to the new server, a DNS-only rollback can lose those new changes. At that point rollback requires data reconciliation or another planned sync.

Define rollback triggers before the migration, for example:

- widespread 5xx errors;
- checkout/payment failure;
- database corruption or missing writes;
- severe runtime incompatibility;
- broken authentication;
- critical mail/webhook failure that cannot be fixed inside the agreed window.

## WordPress, WooCommerce and custom application notes

### WordPress

Check PHP version/extensions, database compatibility, uploads, rewrite rules, wp-cron behavior, caching, SMTP/contact forms and admin login. Avoid blind search/replace operations that can damage serialized data; use application-aware tooling where required.

For resource behavior, see [VPS for WordPress]({{< relref "vps-for-wordpress.md" >}}).

### WooCommerce and other transactional sites

Treat orders, stock, payment callbacks, sessions, scheduled actions and transactional emails as live data. Plan a final database/write cutover rather than relying on the first copy.

See [VPS for WooCommerce]({{< relref "vps-for-woocommerce.md" >}}).

### Custom applications

Document environment variables, secrets, background workers, queues, build/runtime versions, object storage, file paths, webhooks, API allowlists and deployment/startup behavior. Test the real hostname behavior, not only an IP response.

## Technical references

- Google Search Central: Changing your web hosting and SEO
- Google Search Central: Site moves with URL changes

<p>
  <a class="btn btn-primary" href="https://www.vdsina.com/?partner=ni8gzrvz75" target="_blank" rel="sponsored nofollow noopener">Choose a VPS for the migration</a>
</p>
<p><small>Disclosure: the editor has a professional relationship with VDSina. Partner links are marked sponsored. VPS pricing, transfer allowances and other provider terms can change; verify the current offer before ordering.</small></p>

## FAQ

### Can I migrate a website to a VPS without changing the domain?

Yes. A hosting migration can keep the same domain and public URLs. Build and test the destination first, then change the DNS records to send traffic to the new server.

### Do I need 301 redirects when moving a website to a VPS?

Not when the public URLs stay the same. Redirects are needed when URLs actually change, such as a new domain, protocol/path change or restructured content.

### How do I reduce downtime during a VPS migration?

Prepare the destination in parallel, lower the relevant DNS TTL in advance, test privately, control final writes, run a final data sync, switch DNS only after acceptance and keep the old host available during propagation.

### Should I move email to the VPS too?

Not automatically. Keeping email on a managed mail service can reduce migration and deliverability risk. If email moves, plan MX, SPF, DKIM, DMARC, mailbox data, reverse DNS where relevant and backups separately.

### What should I test before changing DNS?

Test representative pages, login, forms, uploads, search, checkout/payment callbacks where relevant, scheduled jobs, API/webhooks, outbound email, HTTPS, redirects and application/server logs.

### How long should I keep the old hosting after migration?

Keep it until DNS traffic has moved, the new server is stable, new writes are verified and the agreed rollback window has passed. Use logs rather than a fixed universal number of hours or days.

### Can I migrate WooCommerce without losing orders?

Yes, but not by relying on a single old database copy. Control writes during cutover and perform an application-appropriate final sync so orders and stock changes are not split between two writable databases.

### Does moving hosting hurt SEO?

A same-URL hosting change should preserve the site's search signals when the destination serves the same content, status codes, canonicals and crawlability. Monitor Search Console and server logs after the move; temporary crawl-rate changes can occur during a hosting infrastructure change.
