---
title: "VPS Security Checklist"
description: "VPS Security Checklist: harden administrative access, firewall exposed services, keep software patched, protect secrets, verify backups and prepare for incident response without locking yourself out."
image: "images/home/vps-for-website-hero.webp"
---

VPS Security Checklist is a prioritized hardening pass for an internet-facing self-managed server. The goal is not to make a VPS “100% secure.” The goal is to remove avoidable attack surface, protect privileged access, keep software maintained, make recovery possible and verify that somebody actually owns the security work.

The safest order matters: **preserve a recovery path first, verify a second administrative login, inventory exposed services, then tighten SSH and firewall rules**.

If nobody on your side owns patching, firewall policy, backup verification, monitoring and incidents, resolve the operating model first: see [Managed vs Unmanaged VPS]({{< relref "managed-vs-unmanaged-vps.md" >}}).

For the broader server decision, see [VPS for website]({{< relref "_index.md" >}}).

[Baseline](#security-baseline-in-order) · [Checker](#vps-security-baseline-checker) · [SSH](#harden-administrative-access) · [Firewall](#firewall-only-the-services-you-need) · [Updates](#patching-and-automatic-security-updates) · [Backups](#backups-are-a-security-control) · [Incident response](#after-a-suspected-compromise) · [FAQ](#faq)

## Security baseline in order

For a typical public Linux VPS:

1. **Keep provider console/recovery access available.**
2. **Create and test a named non-root administrative user.**
3. **Add SSH-key authentication and verify a second login session.**
4. **Inventory every listening service and public port.**
5. **Restrict SSH/root/password policy only after key access works.**
6. **Apply a default-deny firewall policy and open only required ports.**
7. **Keep databases, Redis and internal application ports private by default.**
8. **Apply OS/package security updates and define reboot/restart ownership.**
9. **Keep control panels, CMS, plugins, runtimes and dependencies patched too.**
10. **Protect secrets and use least-privilege users/DB accounts.**
11. **Add brute-force/rate-limit controls as defense-in-depth.**
12. **Use HTTPS for public websites and protect admin interfaces.**
13. **Keep independent backups and test restoration.**
14. **Enable logs/alerts that can reveal security and recovery failures.**
15. **Define what happens after a suspected compromise.**
16. **Repeat the audit regularly.**

Do not harden remote access by blindly pasting commands. A security change that locks the legitimate administrator out is an outage.

## VPS Security Baseline Checker

Use this checker to identify baseline gaps. It does not certify the server as secure.

<div class="rounded-2xl bg-light p-6 dark:bg-darkmode-light">
<form id="vps-security-checker">
  <div class="mb-6">
    <label for="sec-recovery" class="form-label">Provider console / recovery path tested?</label>
    <select id="sec-recovery" class="form-input"><option value="no">No / unknown</option><option value="yes">Yes</option></select>
  </div>
  <div class="mb-6">
    <label for="sec-admin" class="form-label">Named non-root admin with tested SSH-key login?</label>
    <select id="sec-admin" class="form-input"><option value="no">No</option><option value="yes">Yes</option></select>
  </div>
  <div class="mb-6">
    <label for="sec-firewall" class="form-label">Firewall policy is active and only required public ports are allowed?</label>
    <select id="sec-firewall" class="form-input"><option value="no">No / unknown</option><option value="yes">Yes</option></select>
  </div>
  <div class="mb-6">
    <label for="sec-services" class="form-label">Listening services / exposed ports have been inventoried?</label>
    <select id="sec-services" class="form-input"><option value="no">No</option><option value="yes">Yes</option></select>
  </div>
  <div class="mb-6">
    <label for="sec-updates" class="form-label">OS/app security-update ownership and restart/reboot process defined?</label>
    <select id="sec-updates" class="form-input"><option value="no">No</option><option value="yes">Yes</option></select>
  </div>
  <div class="mb-6">
    <label for="sec-backup" class="form-label">Independent backup exists and restore has been tested?</label>
    <select id="sec-backup" class="form-input"><option value="no">No</option><option value="yes">Yes</option></select>
  </div>
  <div class="mb-6">
    <label for="sec-logs" class="form-label">Security/recovery failures can trigger logs or alerts somebody reads?</label>
    <select id="sec-logs" class="form-input"><option value="no">No</option><option value="yes">Yes</option></select>
  </div>
  <div class="mb-6">
    <label for="sec-app" class="form-label">CMS/panel/runtime/dependency updates have an owner?</label>
    <select id="sec-app" class="form-input"><option value="no">No</option><option value="yes">Yes</option></select>
  </div>
  <div class="mb-6">
    <label for="sec-owner" class="form-label">A named person/team owns security incidents?</label>
    <select id="sec-owner" class="form-input"><option value="no">No</option><option value="yes">Yes</option></select>
  </div>
  <button class="btn btn-primary" type="submit">Check security baseline</button>
</form>
<p id="vps-security-result" class="mt-6 rounded border border-border p-4 dark:border-darkmode-border" role="status" aria-live="polite">Mark only controls that are actually implemented and tested.</p>
</div>

<script>
document.addEventListener("DOMContentLoaded", function () {
  var form = document.getElementById("vps-security-checker");
  if (!form) return;

  form.addEventListener("submit", function (event) {
    event.preventDefault();

    var ids = [
      "sec-recovery",
      "sec-admin",
      "sec-firewall",
      "sec-services",
      "sec-updates",
      "sec-backup",
      "sec-logs",
      "sec-app",
      "sec-owner"
    ];

    var missing = ids.filter(function (id) {
      return document.getElementById(id).value !== "yes";
    });

    var critical = ["sec-recovery", "sec-admin", "sec-firewall", "sec-updates", "sec-backup", "sec-owner"];
    var criticalMissing = critical.filter(function (id) {
      return document.getElementById(id).value !== "yes";
    });

    var result;

    if (criticalMissing.length >= 2) {
      result = "CRITICAL GAPS: privileged access, firewall/patching, recovery or incident ownership is incomplete. Do not treat this VPS as a finished production security baseline.";
    } else if (missing.length > 0) {
      result = "BASELINE INCOMPLETE: core controls exist, but " + missing.length + " checklist item(s) remain unresolved. Close them and verify the controls, not only the configuration files.";
    } else {
      result = "PRODUCTION BASELINE READY: the listed baseline controls are implemented and tested. This is not a guarantee of security; continue patching, monitoring, backup tests and recurring audits.";
    }

    document.getElementById("vps-security-result").textContent = result;
  });
});
</script>

## Keep a recovery path before changing access

Before restricting SSH or enabling a strict firewall, confirm you can recover from a bad rule.

Keep at least one out-of-band option available, such as the provider's browser console/VNC/recovery interface.

Then:

1. create the named admin user;
2. add the SSH public key;
3. open a **second** terminal session;
4. verify login and sudo/admin rights;
5. keep the working session open while testing the new policy;
6. only then restrict old access methods.

The important security control is not “disable root as quickly as possible.” It is **replace risky access with a tested safer path without creating a lockout**.

The first-deployment flow is covered in [How to host a website on VPS]({{< relref "how-to-host-a-website-on-vps.md" >}}).

## Inventory exposed services before blocking

Do not guess which ports are open.

On Linux, inspect listening sockets with tools such as:

```bash
sudo ss -lntup
```

For each listener, decide:

- does the service need to exist?
- does it need to listen on all interfaces?
- does it need to be public?
- can it bind only to localhost or a private network?
- which source networks should reach it?
- who owns its updates and logs?

Typical public website ports may include:

- SSH/admin access;
- HTTP 80;
- HTTPS 443.

That does **not** mean every server should expose all three to the whole internet.

Remove unused services rather than relying only on the firewall to hide them.

## Harden administrative access

Ubuntu's OpenSSH documentation supports public-key authentication and recommends modern key algorithms such as Ed25519.

A baseline administrative model is:

- named admin account;
- SSH-key authentication;
- passphrase-protected private key where practical;
- sudo only for users who need it;
- no application running as root;
- direct root/password SSH restricted after safer access is verified.

For environments with higher assurance requirements, OpenSSH also supports stronger authentication models including FIDO/U2F or TOTP-based two-factor authentication.

### Root login and password authentication

Do not blindly set these options before verifying key access and console recovery.

After the safer path works, review:

- `PermitRootLogin`;
- `PasswordAuthentication`;
- `AllowUsers` / `AllowGroups`;
- idle/session policy where needed.

The exact policy depends on the environment.

Changing SSH from port 22 can reduce scanner noise, but it is **not** a substitute for keys, least privilege, firewall policy and maintained software.

## Firewall: only the services you need

Ubuntu's default host-firewall frontend is UFW.

A secure baseline is conceptually:

- default deny unsolicited inbound traffic;
- allow the administrative path you actually use;
- allow HTTP/HTTPS for a public web server;
- keep databases/internal services private;
- review IPv4 and IPv6 behavior.

Before enabling restrictive rules, preserve SSH access.

Example inspection:

```bash
sudo ufw status verbose
```

Do not copy a generic “allow 22/80/443” list if your architecture differs.

### Provider firewall and host firewall

A provider/network firewall can block traffic before it reaches the VM.

A host firewall controls what the guest OS accepts.

Using both can provide useful defense-in-depth, but only when the rules are documented and do not contradict one another.

## Keep databases and internal services private by default

Do not expose MySQL/MariaDB/PostgreSQL, Redis, internal Node/Python application ports or control sockets to the public internet merely because the service is listening.

Prefer:

- localhost for same-server services;
- private network interfaces for multi-server architecture;
- source-IP restrictions when remote administration is necessary;
- SSH/VPN/bastion access for administrative workflows.

Open a database port publicly only when the architecture specifically requires it and the access is strongly restricted.

## Patching and automatic security updates

A supported OS with an unowned patch process becomes stale.

Ubuntu Server uses `unattended-upgrades` for automatic security updates by default on supported installations.

That is helpful, but the security process also needs to answer:

- which repositories are covered?
- are third-party packages/apps updated?
- did a service need restart?
- is a reboot required?
- who verifies failed updates?
- when can production services safely restart?

Ubuntu documentation notes that service restarts and sometimes a reboot may be needed for updated code to actually take effect.

Do not treat “automatic updates enabled” as the entire patch-management process.

## Fail2ban, CrowdSec and rate limiting

Brute-force protection tools can reduce repeated abusive attempts.

They are **defense-in-depth**, not the primary authentication model.

Use them after:

- privileged access is protected;
- strong authentication is in place;
- exposed services are intentionally public;
- logs are available.

A ban tool does not make a weak password, an unpatched panel or an exposed database safe.

## Least privilege for applications and databases

Least privilege applies to the whole stack.

Prefer:

- separate deployment/admin users;
- separate application users;
- separate DB users per application;
- only required DB privileges;
- separate users for unrelated client sites;
- writable directories limited to what the app needs.

Avoid:

- running web apps as root;
- sharing the DB root/admin account with applications;
- `chmod 777` as a permission fix;
- one Unix user for unrelated customer sites when stronger separation is practical.

For multi-site isolation, see [VPS for Multiple Websites]({{< relref "vps-for-multiple-websites.md" >}}).

## Protect secrets and credentials

Keep production credentials out of:

- public Git repositories;
- web-accessible document roots;
- debug pages;
- screenshots/tickets/chat;
- shell history where avoidable;
- broadly readable environment files.

Protect:

- database passwords;
- API keys;
- SMTP credentials;
- payment/webhook secrets;
- backup-storage credentials;
- panel/admin credentials;
- SSH private keys.

Rotate credentials when staff/contractors leave or after suspected compromise.

## Control panels and admin interfaces

A control panel is a privileged management application.

Audit:

- current panel version;
- panel administrator accounts;
- 2FA where the panel supports it;
- exposed admin ports/hostnames;
- source-IP restrictions where operationally practical;
- plugin/extension inventory;
- backup/restore behavior;
- panel logs and failed-login activity.

Do not assume that installing a panel makes the VPS secure or managed.

For panel selection, see [VPS with Control Panel]({{< relref "vps-with-control-panel.md" >}}). For the branded panel path, see [FASTPANEL VPS Hosting]({{< relref "fastpanel-vps-hosting.md" >}}).

## Application, CMS and runtime updates

A fully patched operating system can still host a vulnerable application.

Security ownership must include:

- PHP/Node/Python/runtime;
- framework;
- WordPress core;
- plugins/themes;
- WooCommerce/extensions;
- web server;
- control panel;
- libraries/dependencies.

Remove abandoned components that no longer receive security updates.

For WordPress-specific operations, see [VPS for WordPress]({{< relref "vps-for-wordpress.md" >}}). For transactional stores, see [VPS for WooCommerce]({{< relref "vps-for-woocommerce.md" >}}).

## HTTPS protects transport, not the whole server

HTTPS is required for production websites that handle logins or sensitive data and is a normal baseline for public sites.

It protects data in transit between client and server.

It does not fix:

- vulnerable plugins;
- weak SSH;
- public databases;
- leaked API keys;
- stale packages;
- unsafe file permissions;
- missing backups.

Verify certificate renewal and watch for expiry/failure.

## DDoS protection is not application security

VDSina currently advertises free DDoS protection on Standard VPS.

Its public QA states that the free service covers **L3-L4 channel/network-layer attacks** and is **not governed by an SLA**.

That protection is useful at the infrastructure/network layer, but it does not replace:

- SSH hardening;
- firewall policy;
- web application security;
- application-layer rate limiting;
- WAF/bot controls where appropriate;
- patching;
- incident response.

Do not describe network-layer DDoS mitigation as a complete website-security service.

<p>
  <a class="btn btn-primary" href="https://www.vdsina.com/?partner=ni8gzrvz75" target="_blank" rel="sponsored nofollow noopener">Check current VPS infrastructure</a>
</p>
<p><small>Disclosure: the editor has a professional relationship with VDSina, and this site may earn a commission if you order through this partner link. Provider DDoS protection and technical support do not replace guest-OS/application hardening or administration.</small></p>

## Backups are a security control

Security includes the ability to recover after compromise, ransomware, bad updates and accidental deletion.

At minimum:

- keep a copy outside the running VPS;
- do not rely only on one snapshot/image;
- protect backup credentials;
- keep backups unavailable to the application where practical;
- monitor failed backup jobs;
- test restoration;
- know how much data can be lost between restore points.

CISA recommends maintaining offline/encrypted backups of critical data and regularly testing restoration in a disaster-recovery scenario.

The deeper RPO/RTO, retention and backup-topology design is covered in [VPS Backup Strategy]({{< relref "vps-backup-strategy.md" >}}).

## Logs, alerts and audit trail

A secure configuration you never observe can fail silently.

At minimum watch for:

- repeated SSH/auth failures;
- unexpected new admin/sudo users;
- panel login failures;
- firewall changes;
- new listening ports;
- service crashes/restarts;
- disk-full events;
- application/web-server 5xx spikes;
- backup failures;
- certificate-renewal failures;
- malware/security-tool alerts where used.

Keep logs long enough to investigate incidents.

The deeper threshold/alert design is covered in [VPS Monitoring]({{< relref "vps-monitoring.md" >}}).

## After a suspected compromise

If you suspect privileged/root compromise, do not immediately trust an ad-hoc “cleanup” as proof the server is safe.

A safer response is:

1. **contain** the affected VPS/network path;
2. preserve relevant logs/evidence where possible;
3. identify what credentials/secrets may have been exposed;
4. rotate those credentials from a clean trusted system;
5. determine the known-good application/data restore point;
6. rebuild the server from known-good OS/configuration sources where appropriate;
7. restore validated data rather than blindly restoring compromised executables/configuration;
8. review the initial-access cause before reconnecting production traffic.

CISA's incident-response guidance emphasizes isolation, evidence/log review and recovery from validated backups.

For a business-critical system, involve a qualified incident-response/security professional.

## Repeat the checklist

Security is not a one-time provisioning task.

Recheck on a defined cadence:

- admin users and SSH keys;
- sudo privileges;
- open/listening ports;
- firewall rules;
- unsupported packages/OS versions;
- pending security updates;
- control-panel/CMS/plugin versions;
- backup success and restore tests;
- certificate expiry/renewal;
- logs and alerts;
- unused accounts/services;
- exposed secrets;
- incident contacts.

Also rerun the checklist after major migrations, panel changes, new services or architecture changes.

## Production security checklist

| Control | Pass condition |
|---|---|
| Recovery access | provider console/recovery route works |
| Admin login | named non-root admin + tested key login |
| SSH policy | root/password policy deliberately configured after safe replacement access |
| Services | listening ports inventoried and justified |
| Firewall | default-deny/least exposure; required admin/web access tested |
| Internal services | DB/cache/app ports not public without explicit need |
| Patching | OS + application update owners defined; restart/reboot path understood |
| Least privilege | apps/DB/users have only required access |
| Secrets | not public, web-accessible or broadly readable |
| Panel/admin UI | patched; admin access and 2FA/restrictions reviewed |
| TLS | valid HTTPS + renewal path |
| Brute-force controls | used as defense-in-depth where useful |
| Backups | independent copy + restore test |
| Logging | auth/admin/service/backup failures observable |
| DDoS | provider/network protection scope understood |
| Incident response | owner, containment and clean-recovery path defined |
| Recurring audit | next review date/process exists |

## Technical references

- Ubuntu Server — OpenSSH
- Ubuntu Server — firewall/UFW
- Ubuntu Server — automatic updates
- CISA — StopRansomware Guide
- VDSina Standard VPS
- VDSina QA — DDoS protection scope

## FAQ

### What should I secure first on a new VPS?

Preserve console/recovery access, create and test a named non-root admin with SSH-key login, inventory listening services, then tighten SSH and firewall policy. Avoid making multiple lockout-prone changes before verifying access.

### Should I disable SSH password login?

Key-based admin authentication is stronger for typical VPS administration, but verify the key login and recovery console first. Do not disable the only working access path.

### Should I change the SSH port?

It can reduce scanner/log noise, but it is not a primary security control. Strong authentication, least privilege, firewall policy and patching matter more.

### Do I need Fail2ban?

Not always, but it can be useful defense-in-depth against repeated login abuse. It does not replace SSH keys, patching or correct service exposure.

### Which ports should be open on a VPS?

Only ports required by the architecture. A public web server commonly needs HTTP/HTTPS plus a controlled admin path. Databases and internal application services should normally remain private.

### Does a firewall protect a vulnerable application?

No. A firewall limits network exposure. A publicly reachable web application still needs secure code, supported dependencies, updates and application-level controls.

### Are automatic security updates enough?

No. They help with supported OS packages, but third-party applications/dependencies may need separate updates, and service restarts or reboots may still need operational handling.

### Is HTTPS enough to secure a VPS?

No. HTTPS protects transport. It does not fix weak SSH, exposed databases, vulnerable plugins, stale packages, leaked secrets or missing backups.

### Is VDSina DDoS protection enough to secure the website?

No. VDSina currently advertises free DDoS protection, and its public QA describes the free protection as L3-L4 with no SLA. You still need guest-OS, access, application and recovery security.

### What should I do if I suspect the VPS was compromised?

Contain it, preserve relevant evidence/logs, rotate exposed credentials from a clean system and prefer rebuilding from known-good sources plus validated backups when privileged compromise is suspected. For critical systems, involve an incident-response professional.
