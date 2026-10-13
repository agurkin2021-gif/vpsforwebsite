---
title: "How to host a website on VPS"
description: "How to host a website on VPS: choose the deployment path, secure first access, install the right web stack, connect the domain, enable HTTPS, test reboot recovery and verify production readiness."
image: "https://raw.githubusercontent.com/zeon-studio/hugoplate/4acb4365d7a86703357a9f216db149f55210fa09/exampleSite/assets/images/banner.png"
---

How to host a website on VPS depends on the application you are deploying. A static site needs a web server and DNS. WordPress or another PHP CMS also needs PHP and a database. A Node.js or Python application usually runs behind a reverse proxy. You can build those pieces manually on a clean VPS or use a control panel to manage them through a browser.

This guide owns the **fresh-VPS-to-live-website** workflow. If you are moving an existing production site with live data, use [Website migration to VPS]({{< relref "website-migration-to-vps.md" >}}) for the cutover and rollback process.

For the broader buying decision, see [VPS for website]({{< relref "_index.md" >}}).

[Quick sequence](#quick-deployment-sequence) · [Choose a path](#choose-manual-panel-or-managed) · [Path checker](#deployment-path-checker) · [Manual path](#manual--no-control-panel-path) · [DNS](#point-the-domain-to-the-vps) · [Production checklist](#production-acceptance-checklist) · [FAQ](#faq)

## Quick deployment sequence

A reliable first deployment follows this order:

1. **Choose and size the VPS.**
2. **Choose manual, control-panel or managed administration.**
3. **Provision a clean operating system or current provider panel image.**
4. **Secure first access and create a non-root administrative path.**
5. **Update the operating system.**
6. **Install only the web stack the application needs.**
7. **Configure the site/application before public DNS cutover where practical.**
8. **Deploy files/code and configure ownership, secrets and database access.**
9. **Point the domain to the VPS.**
10. **Enable HTTPS after the hostname reaches the server.**
11. **Restrict the firewall to required services.**
12. **Verify cron/workers, logs, backups and external monitoring.**
13. **Reboot once and confirm every required service returns automatically.**
14. **Only then call the deployment production-ready.**

Do not install PHP, MySQL, mail or a control panel merely because a generic VPS guide includes them. Install the components your website actually needs.

## Choose manual, panel or managed

There are three distinct operating paths.

### Manual / no control panel

Choose a clean Linux VPS and administer the stack through SSH.

Good fit when:

- you understand the application stack;
- you want a minimal service footprint;
- you need custom Nginx/Apache/runtime configuration;
- you use scripts, Git or infrastructure-as-code;
- you do not need a traditional hosting-account interface.

This is the merged owner for the old **VPS without Control Panel** idea. We are not creating another competing URL for the same intent.

### Control panel

Use a hosting panel when browser-based site, domain, PHP, database, mail or user management removes meaningful repetitive work.

See [VPS with Control Panel]({{< relref "vps-with-control-panel.md" >}}). If FASTPANEL is already your choice, use [FASTPANEL VPS Hosting]({{< relref "fastpanel-vps-hosting.md" >}}).

### Managed administration

A panel and management are different. If nobody on your side owns patching, security, backups, monitoring and incidents, decide that before launch.

See [Managed vs Unmanaged VPS]({{< relref "managed-vs-unmanaged-vps.md" >}}).

## Deployment path checker

This tool identifies the stack path to investigate. It does not replace application documentation.

<div class="rounded-2xl bg-light p-6 dark:bg-darkmode-light">
<form id="deployment-path-checker">
  <div class="mb-6">
    <label for="deploy-type" class="form-label">Website / application type</label>
    <select id="deploy-type" class="form-input">
      <option value="static">Static HTML / generated static site</option>
      <option value="php">WordPress / PHP CMS</option>
      <option value="app">Node.js / Python / custom application</option>
    </select>
  </div>
  <div class="mb-6">
    <label for="deploy-panel" class="form-label">Prefer a hosting control panel?</label>
    <select id="deploy-panel" class="form-input"><option value="no">No / manual</option><option value="yes">Yes</option></select>
  </div>
  <div class="mb-6">
    <label for="deploy-db" class="form-label">Does the application require a local database?</label>
    <select id="deploy-db" class="form-input"><option value="no">No</option><option value="yes">Yes</option></select>
  </div>
  <div class="mb-6">
    <label for="deploy-mail" class="form-label">Host mailboxes on the same VPS?</label>
    <select id="deploy-mail" class="form-input"><option value="no">No / external mail</option><option value="yes">Yes</option></select>
  </div>
  <div class="mb-6">
    <label for="deploy-sites" class="form-label">Number of active websites</label>
    <select id="deploy-sites" class="form-input"><option value="1">1</option><option value="few">2–5</option><option value="many">6+</option></select>
  </div>
  <button class="btn btn-primary" type="submit">Choose deployment path</button>
</form>
<p id="deployment-path-result" class="mt-6 rounded border border-border p-4 dark:border-darkmode-border" role="status" aria-live="polite">Select the workload and operating preference.</p>
</div>

<script>
document.addEventListener("DOMContentLoaded", function () {
  var form = document.getElementById("deployment-path-checker");
  if (!form) return;

  form.addEventListener("submit", function (event) {
    event.preventDefault();

    var type = document.getElementById("deploy-type").value;
    var panel = document.getElementById("deploy-panel").value === "yes";
    var db = document.getElementById("deploy-db").value === "yes";
    var mail = document.getElementById("deploy-mail").value === "yes";
    var sites = document.getElementById("deploy-sites").value;

    var result;

    if (panel) {
      result = "CONTROL PANEL PATH: choose the panel before the final OS image. Verify OS compatibility, panel overhead, users/site isolation, mail/DNS needs, backups and management responsibility.";
    } else if (type === "static" && !db && !mail) {
      result = "STATIC MANUAL PATH: clean Linux + SSH + Nginx or Apache + site files + DNS + HTTPS. Do not install PHP or a database unless the site actually needs them.";
    } else if (type === "php") {
      result = "PHP / WORDPRESS MANUAL PATH: Linux + SSH + Nginx/Apache + PHP-FPM + database if required + DNS + HTTPS. Budget RAM for PHP workers and the database.";
    } else if (type === "app") {
      result = "APP + REVERSE PROXY PATH: run the application under its own non-root service/process manager, usually on localhost, then put Nginx/Apache in front for the public hostname and HTTPS.";
    } else {
      result = "CUSTOM MANUAL PATH: start from the application's documented runtime and install only required services.";
    }

    if (sites === "many") {
      result += " With 6+ sites, add explicit per-site users/permissions and combined workload planning.";
    }
    if (mail) {
      result += " Local mail adds SMTP/IMAP, DNS reputation, storage, backup and security work; reconsider whether managed external mail is simpler.";
    }

    document.getElementById("deployment-path-result").textContent = result;
  });
});
</script>

## Prerequisites

Before touching the server, have:

- a VPS sized for the workload;
- the server IP address;
- SSH credentials or key access;
- a working provider console/VNC/recovery path;
- a registered domain and DNS access;
- the website files or application repository;
- the required runtime versions;
- database requirements;
- a plan for secrets/environment variables;
- a backup location;
- an external way to test website availability.

Use [VPS sizing for website]({{< relref "vps-sizing-for-website.md" >}}) before deployment if the resource requirement is still uncertain.

VDSina's current Standard VPS page lists pure OS templates including Ubuntu 26.04/24.04/22.04/20.04, Debian 13/12/11/10, AlmaLinux, Rocky, CentOS, Oracle Linux and ArchLinux. This guide uses Ubuntu/Debian-style examples because the current web-server documentation and package flow are easy to follow; the architecture applies to other supported Linux distributions with different package/service commands.

<p>
  <a class="btn btn-primary" href="https://www.vdsina.com/?partner=ni8gzrvz75" target="_blank" rel="sponsored nofollow noopener">Choose a VPS for the website</a>
</p>
<p><small>Affiliate disclosure: this site may earn a commission if you order through this partner link. Choose the server size and operating model from the workload, not from commission.</small></p>

## Choose the operating system

For a manual website server, choose an operating system that:

- is supported by the application/runtime;
- is still maintained;
- your administrator understands;
- has current packages/documentation for the web stack;
- matches any panel requirement if you later use one.

Do not choose the OS only because it is newest. Application compatibility and administrator familiarity matter more.

For a simple current Linux example, Ubuntu 24.04 LTS or Debian 12 are reasonable documentation targets. If your application vendor specifies another supported distribution, follow that requirement.

## Secure first SSH access

A new VPS gives you administrative access, but production work should not happen permanently as root.

A safe first-access sequence is:

1. connect using the credentials/key provided by the VPS provider;
2. confirm the server/IP is the one you intended to create;
3. keep the provider console/VNC/recovery route working;
4. create a named administrative user;
5. grant only the required sudo/admin rights;
6. add SSH-key authentication where practical;
7. verify the new login in a second session **before** disabling or restricting the original access method.

Example on Ubuntu/Debian:

```bash
ssh root@SERVER_IP
adduser deploy
usermod -aG sudo deploy
```

Do not lock out the only working administrative path while "hardening" the server.

Deep SSH/firewall hardening belongs to the future **VPS Security Checklist** page; this guide keeps only the minimum needed for deployment.

## Update the server before installing the stack

On Ubuntu/Debian:

```bash
sudo apt update
sudo apt upgrade -y
```

Reboot if the update requires it, then verify you can reconnect.

Do not postpone security updates until after the website is public.

## Manual / no-control-panel path

A manual VPS should contain only the services the application needs.

The common choices are:

### Static website

Needed:

- Nginx or Apache;
- website files;
- DNS;
- HTTPS.

Not automatically needed:

- PHP;
- MySQL/MariaDB/PostgreSQL;
- local mail server.

### PHP / WordPress website

Usually needed:

- Nginx or Apache;
- PHP-FPM / PHP modules;
- database;
- website files/uploads;
- DNS;
- HTTPS.

For WordPress resource behavior, use [VPS for WordPress]({{< relref "vps-for-wordpress.md" >}}).

### Node.js / Python / custom application

Usually:

- application runtime;
- dedicated non-root application user;
- process manager/systemd service;
- application bound to localhost/private socket where practical;
- Nginx/Apache reverse proxy;
- database only when required;
- DNS;
- HTTPS.

Do not expose a development server directly to the public internet as the production architecture.

## Install the web server

Ubuntu's current server documentation supports both Nginx and Apache. Neither is universally "better".

For the Nginx example:

```bash
sudo apt update
sudo apt install nginx
sudo systemctl enable --now nginx
sudo systemctl status nginx
```

At this point the server IP should return the default Nginx page if network/firewall rules allow HTTP.

Use Apache instead when the application, team or existing configuration fits Apache better.

## Configure the website hostname

DNS and web-server configuration are two halves of the same job.

The DNS provider must point the hostname to the VPS, **and** the web server must know which site should answer that hostname.

For Nginx, create a server block for the domain. Conceptually:

```nginx
server {
    listen 80;
    listen [::]:80;

    server_name example.com www.example.com;
    root /var/www/example.com/public;
    index index.html index.htm;

    location / {
        try_files $uri $uri/ =404;
    }
}
```

On Ubuntu/Debian, site-specific configurations commonly live under:

- `/etc/nginx/sites-available/`
- `/etc/nginx/sites-enabled/`

After changes:

```bash
sudo nginx -t
sudo systemctl reload nginx
```

Always test configuration syntax before reloading.

For a reverse-proxy app, the server block instead proxies requests to the local application port/socket.

## Deploy files or application code

Choose a repeatable deployment method.

### SFTP/SCP

Good for:

- small sites;
- infrequent manual deployments;
- first-time simple projects.

Risk: it is easy for the production directory to drift away from the source repository.

### rsync over SSH

Useful for repeatable file synchronization and efficient incremental updates.

### Git-based deployment

Useful when production releases should correspond to repository commits.

### CI/CD

Useful when deployment is frequent enough to justify automated build/test/release steps.

Whatever method you use:

- do not deploy as root unless the task genuinely requires root;
- keep application files owned by an appropriate deployment/application user;
- grant the web server only the access it needs;
- keep secrets outside public document roots;
- do not use world-writable permissions as a shortcut.

## PHP / WordPress path

For a PHP site on Ubuntu/Debian, install the current supported PHP-FPM packages and required extensions for the application.

Typical architecture:

**browser -> Nginx/Apache -> PHP-FPM -> database**

Do not copy a random extension list from another CMS. Install what the application actually requires.

For WordPress:

- create a database and dedicated DB user;
- configure PHP upload/memory/execution limits from measured need;
- keep `wp-config.php` secrets protected;
- configure the site hostname;
- enable HTTPS;
- validate wp-cron/background jobs;
- add caching based on the workload.

Use [VPS for WordPress]({{< relref "vps-for-wordpress.md" >}}) for sizing and performance rather than duplicating it here.

## Node.js / Python / custom-app path

Do not run the development command manually in a terminal and call it production.

Use:

- a dedicated application user;
- environment/config file with restricted permissions;
- systemd or an appropriate production process manager;
- automatic restart on failure/reboot;
- local/private application listener;
- Nginx/Apache reverse proxy;
- application logs;
- health checks.

Typical flow:

**browser -> HTTPS/Nginx -> application on 127.0.0.1:PORT -> database/external services**

Verify the framework's own production deployment guidance.

## Database: install only when required

A static website needs no database.

For a dynamic application that needs one:

- install the supported database engine;
- create a dedicated database;
- create an application-specific user;
- grant only needed privileges;
- keep credentials out of the web root;
- do not expose the database port publicly unless there is a specific secured architecture requiring it;
- include the database in backup and monitoring plans.

Database work can become the real VPS bottleneck even when the web server is almost idle.

## File ownership, permissions and secrets

Avoid two common mistakes:

1. running the website as root;
2. making application directories world-writable to "fix" permission errors.

Instead:

- use a deployment/application user;
- understand which process needs read vs write access;
- give uploads/cache directories only the write access they require;
- protect environment files and credentials;
- do not commit production secrets to Git;
- keep private keys outside public document roots.

Exact ownership depends on the application and web-server model; use the application's documentation rather than copying a universal `chmod 777` recipe.

## Point the domain to the VPS

At the DNS provider, configure the records that should reach this server.

Typical IPv4 setup:

| Name | Type | Value |
|---|---|---|
| `@` | A | VPS IPv4 address |
| `www` | CNAME | root domain |

An A record for `www` is also possible.

Add an AAAA record only if IPv6 is actually configured and reachable on the VPS. A broken AAAA record can make some visitors fail even when IPv4 works.

DNS alone does not make the website work: the Nginx/Apache site configuration must also have the matching hostname.

If you are moving an existing live site, DNS cutover and final-write handling belong to [Website migration to VPS]({{< relref "website-migration-to-vps.md" >}}).

## Add HTTPS after DNS resolves

Obtain a trusted certificate only after the public hostname resolves to the server that will answer the validation request.

For Nginx/Apache, an ACME client such as Certbot can request and renew Let's Encrypt certificates. Follow the current Certbot/OS instructions rather than copying an old package command blindly.

Verify:

- certificate covers root and `www` variants you use;
- HTTP redirects to HTTPS as intended;
- certificate renewal is automated;
- renewal can pass through the firewall/CDN configuration;
- the application generates the correct HTTPS URLs.

Do not enable an HTTPS redirect before you know the certificate path works.

## Configure the firewall

Keep administrative access working while changing firewall rules.

A basic public website commonly needs:

- SSH from the required administration source/path;
- TCP 80 for HTTP/ACME/redirects;
- TCP 443 for HTTPS.

Do not expose MySQL/PostgreSQL, Redis or internal application ports publicly just because they listen locally by default.

On a server using UFW, allow the required SSH path **before** enabling restrictive rules.

Deep firewall/hardening details belong to the future VPS Security Checklist.

## Cron jobs, queues and workers

Dynamic websites often fail after deployment because only the web request path was configured.

Inventory:

- cron jobs;
- queue workers;
- scheduled actions;
- imports/exports;
- email jobs;
- cache warmers;
- background processors.

Make them:

- run as the correct non-root user;
- start automatically when required;
- write to known logs;
- avoid overlapping in ways that exhaust CPU/RAM;
- survive server reboot.

## Logs and basic observability

Before production traffic, know where to look when the site fails.

At minimum identify:

- Nginx/Apache access log;
- Nginx/Apache error log;
- application log;
- PHP-FPM/runtime log;
- database log/status;
- system journal;
- disk usage;
- memory/CPU pressure.

Add an external HTTP(S) uptime check so a server failure is visible even when nobody is logged into the VPS.

Deep threshold/alert design belongs to the planned VPS Monitoring page.

## Reboot validation

A surprising number of first VPS deployments work until the first reboot.

Before calling the server ready:

```bash
sudo reboot
```

After it returns, confirm:

- SSH access;
- Nginx/Apache;
- PHP-FPM or app service;
- database;
- cron/queue workers;
- HTTPS;
- website pages/forms;
- monitoring;
- backup schedule.

If the application only returns after somebody manually launches a command, the deployment is not complete.

## Production acceptance checklist

| Check | Pass condition |
|---|---|
| Server access | named admin can log in; recovery console remains available |
| Updates | current security/system updates applied |
| Web server | starts automatically and config test passes |
| Site hostname | root/`www` behavior intentional |
| DNS | A/AAAA/CNAME resolve to the intended server/path |
| HTTPS | trusted certificate, correct names, renewal path understood |
| Application | representative pages, login/forms/uploads work |
| Database | application user works; DB port not unintentionally public |
| Files | correct ownership; no `777` workaround |
| Jobs | cron/workers start and log correctly |
| Reboot | required services recover automatically |
| Logs | operator knows where web/app/system failures appear |
| Backup | required files/database are included; restore path defined |
| Monitoring | external website check plus basic resource visibility |
| Capacity | CPU/RAM/disk checked under real workload |

A website is not production-ready merely because the homepage returns HTTP 200.

## Backups and monitoring handoff

This page only establishes the minimum handoff.

Before relying on the site:

- schedule backups;
- keep an independent/off-server copy;
- include the database and configuration/secrets required for recovery;
- verify restoreability;
- monitor website availability;
- monitor disk growth;
- watch CPU/RAM/database pressure;
- watch certificate renewal.

The deeper recovery design belongs to the future **VPS Backup Strategy** page. Monitoring thresholds and alert design belong to the future **VPS Monitoring** page.

## Multiple websites

For several sites:

- use a separate server block/virtual host per hostname;
- separate document roots;
- use separate application/database credentials;
- use separate system users where the trust model requires it;
- avoid one site's cron/import/backups starving the others;
- account for combined peak load;
- understand that all sites still share one VPS failure domain.

Use [VPS for Multiple Websites]({{< relref "vps-for-multiple-websites.md" >}}) for capacity and isolation planning.

## Technical references

- [Ubuntu Server: install Nginx](https://ubuntu.com/server/docs/how-to-install-nginx/)
- [Ubuntu Server: configure Nginx](https://ubuntu.com/server/docs/how-to/web-services/configure-nginx/)
- [Ubuntu Server: web services](https://ubuntu.com/server/docs/how-to/web-services/)
- [VDSina Standard VPS — current pure OS templates](https://www.vdsina.com/pricing/standard)

<p>
  <a class="btn btn-primary" href="https://www.vdsina.com/?partner=ni8gzrvz75" target="_blank" rel="sponsored nofollow noopener">Choose a VPS for your website</a>
</p>
<p><small>Affiliate disclosure: partner links are marked sponsored. Verify current VPS pricing, operating-system availability and provider terms before ordering.</small></p>

## FAQ

### Can I host a website on a VPS without a control panel?

Yes. A clean Linux VPS can host a website with SSH plus the web server/runtime/database components the application needs. That no-panel intent is part of this guide rather than a separate competing page.

### Do I need Nginx to host a website on VPS?

No. Nginx and Apache are both common choices. Use the web server that fits the application, configuration and administrator experience.

### Does every VPS website need a database?

No. Static websites do not need one. Install MySQL/MariaDB/PostgreSQL only when the application requires a database.

### Should I use root to host the website?

No. Root is for administration. Run/deploy the website under appropriate non-root users and services with only the permissions they need.

### When should I use a control panel?

Use one when browser-based management of sites, domains, PHP, databases, users, mail or backups removes enough repetitive administration to justify the overhead and constraints.

### Can I host WordPress on a VPS without cPanel?

Yes. WordPress needs a compatible web server, PHP, a database, the WordPress files, correct permissions, DNS and HTTPS. A panel is optional.

### When should I point DNS to the VPS?

For a new site, once the server is ready to answer the real hostname. For an existing production site, test first and use a controlled migration/cutover plan.

### Why does my domain point to the VPS but show the wrong site?

DNS only sends the hostname to the server IP. Nginx/Apache must also have a matching server block/virtual host for that hostname.

### When should I enable HTTPS?

After the public hostname resolves to the server and the validation path works. Then issue the certificate, verify root/`www` coverage and configure the intended HTTP-to-HTTPS redirect.

### What should I check after rebooting the VPS?

Confirm the web server, application service/PHP-FPM, database, workers, HTTPS, monitoring and website all return without manual intervention.
