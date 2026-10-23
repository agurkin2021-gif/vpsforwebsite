---
title: "VPS-Sicherheitscheckliste"
slug: "vps-sicherheitscheckliste"
description: "VPS-Sicherheitscheckliste: Administratorzugriff absichern, Dienste per Firewall schützen, Software aktuell halten, Geheimnisse schützen, Backups prüfen und auf Vorfälle vorbereitet sein, ohne sich auszusperren."
image: "images/home/vps-for-website-hero.webp"
---

Die VPS-Sicherheitscheckliste ist ein nach Priorität geordneter Härtungsdurchgang für einen selbst verwalteten, aus dem Internet erreichbaren Server. Ziel ist kein „100 % sicherer“ VPS. Ziel ist es, vermeidbare Angriffsflächen zu entfernen, privilegierte Zugänge zu schützen, Software zu pflegen, Wiederherstellung zu ermöglichen und sicherzustellen, dass jemand die Sicherheitsarbeit tatsächlich verantwortet.

Die sichere Reihenfolge ist entscheidend: **Zuerst einen Wiederherstellungszugang erhalten, eine zweite Administratoranmeldung prüfen und erreichbare Dienste erfassen; erst danach SSH und Firewall-Regeln verschärfen**.

Wenn auf Ihrer Seite niemand Patches, Firewall-Regeln, Backup-Prüfung, Monitoring und Vorfälle verantwortet, klären Sie zuerst das Betriebsmodell: siehe [Managed vs. Unmanaged VPS]({{< relref "managed-vs-unmanaged-vps.md" >}}).

Die grundsätzliche Serverentscheidung behandelt [VPS für Websites]({{< relref "_index.md" >}}).

[Grundschutz](#security-baseline-in-order) · [Check](#vps-security-baseline-checker) · [SSH](#harden-administrative-access) · [Firewall](#firewall-only-the-services-you-need) · [Updates](#patching-and-automatic-security-updates) · [Backups](#backups-are-a-security-control) · [Vorfallreaktion](#after-a-suspected-compromise) · [FAQ](#faq)

## Sicherheitsgrundschutz in der richtigen Reihenfolge {#security-baseline-in-order}

Für einen typischen öffentlichen Linux-VPS:

1. **Konsole und Wiederherstellungszugriff des Anbieters verfügbar halten.**
2. **Einen namentlich zugeordneten Administratorbenutzer ohne direkte Root-Anmeldung anlegen und testen.**
3. **SSH-Schlüsselauthentifizierung ergänzen und eine zweite Anmeldung prüfen.**
4. **Alle lauschenden Dienste und öffentlichen Ports erfassen.**
5. **SSH-, Root- und Passwortrichtlinien erst einschränken, wenn der Schlüsselzugriff funktioniert.**
6. **Eine standardmäßig sperrende Firewall-Regelung anwenden und nur erforderliche Ports öffnen.**
7. **Datenbanken, Redis und interne Anwendungsports standardmäßig privat halten.**
8. **Sicherheitsupdates für Betriebssystem und Pakete installieren und Zuständigkeiten für Dienst-/Serverneustarts festlegen.**
9. **Auch Control Panels, CMS, Plugins, Laufzeiten und Abhängigkeiten aktuell halten.**
10. **Geheimnisse schützen und Nutzer-/Datenbankkonten mit minimalen Rechten verwenden.**
11. **Brute-Force-Schutz und Ratenbegrenzung als zusätzliche Schutzschicht ergänzen.**
12. **HTTPS für öffentliche Websites verwenden und Administrationsoberflächen schützen.**
13. **Unabhängige Backups aufbewahren und Wiederherstellung testen.**
14. **Protokolle und Alarme aktivieren, die Sicherheits- und Wiederherstellungsfehler erkennbar machen.**
15. **Vorgehen bei Verdacht auf eine Kompromittierung festlegen.**
16. **Die Prüfung regelmäßig wiederholen.**

Härten Sie Fernzugriffe nicht durch ungeprüftes Einfügen von Befehlen. Eine Sicherheitsänderung, die den berechtigten Administrator aussperrt, ist ein Ausfall.

## VPS-Sicherheitsgrundschutz prüfen {#vps-security-baseline-checker}

Dieser Check hilft, Lücken im Grundschutz zu erkennen. Er bescheinigt nicht, dass der Server sicher ist.

<div class="rounded-2xl bg-light p-6 dark:bg-darkmode-light">
<form id="vps-security-checker">
  <div class="mb-6">
    <label for="sec-recovery" class="form-label">Anbieterkonsole / Wiederherstellungszugang getestet?</label>
    <select id="sec-recovery" class="form-input"><option value="no">Nein / unbekannt</option><option value="yes">Ja</option></select>
  </div>
  <div class="mb-6">
    <label for="sec-admin" class="form-label">Zugeordneter Administrator ohne direkte Root-Anmeldung und mit getesteter SSH-Schlüsselanmeldung?</label>
    <select id="sec-admin" class="form-input"><option value="no">Nein</option><option value="yes">Ja</option></select>
  </div>
  <div class="mb-6">
    <label for="sec-firewall" class="form-label">Firewall-Regeln aktiv und nur erforderliche öffentliche Ports erlaubt?</label>
    <select id="sec-firewall" class="form-input"><option value="no">Nein / unbekannt</option><option value="yes">Ja</option></select>
  </div>
  <div class="mb-6">
    <label for="sec-services" class="form-label">Lauschende Dienste / erreichbare Ports erfasst?</label>
    <select id="sec-services" class="form-input"><option value="no">Nein</option><option value="yes">Ja</option></select>
  </div>
  <div class="mb-6">
    <label for="sec-updates" class="form-label">Zuständigkeit für Betriebssystem-/Anwendungsupdates und Ablauf für Dienst-/Serverneustarts festgelegt?</label>
    <select id="sec-updates" class="form-input"><option value="no">Nein</option><option value="yes">Ja</option></select>
  </div>
  <div class="mb-6">
    <label for="sec-backup" class="form-label">Unabhängiges Backup vorhanden und Wiederherstellung getestet?</label>
    <select id="sec-backup" class="form-input"><option value="no">Nein</option><option value="yes">Ja</option></select>
  </div>
  <div class="mb-6">
    <label for="sec-logs" class="form-label">Werden Sicherheits-/Wiederherstellungsfehler protokolliert oder gemeldet und von jemandem geprüft?</label>
    <select id="sec-logs" class="form-input"><option value="no">Nein</option><option value="yes">Ja</option></select>
  </div>
  <div class="mb-6">
    <label for="sec-app" class="form-label">Verantwortliche für CMS-/Panel-/Laufzeit-/Abhängigkeitsupdates benannt?</label>
    <select id="sec-app" class="form-input"><option value="no">Nein</option><option value="yes">Ja</option></select>
  </div>
  <div class="mb-6">
    <label for="sec-owner" class="form-label">Verantwortet eine benannte Person oder ein Team Sicherheitsvorfälle?</label>
    <select id="sec-owner" class="form-input"><option value="no">Nein</option><option value="yes">Ja</option></select>
  </div>
  <button class="btn btn-primary" type="submit">Sicherheitsgrundschutz prüfen</button>
</form>
<p id="vps-security-result" class="mt-6 rounded border border-border p-4 dark:border-darkmode-border" role="status" aria-live="polite">Bestätigen Sie nur Maßnahmen, die tatsächlich umgesetzt und getestet sind.</p>
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
      result = "KRITISCHE LÜCKEN: Privilegierter Zugriff, Firewall/Patches, Wiederherstellung oder Zuständigkeit für Vorfälle sind unvollständig. Betrachten Sie den Sicherheitsgrundschutz dieses VPS nicht als fertig für den Produktivbetrieb.";
    } else if (missing.length > 0) {
      result = "GRUNDSCHUTZ UNVOLLSTÄNDIG: Zentrale Maßnahmen bestehen, aber noch " + missing.length + " Checklistenpunkte sind offen. Schließen Sie diese und prüfen Sie die tatsächliche Wirksamkeit, nicht nur die Konfigurationsdateien.";
    } else {
      result = "GRUNDSCHUTZ FÜR DEN PRODUKTIVBETRIEB VORBEREITET: Die aufgeführten Maßnahmen sind umgesetzt und getestet. Das ist keine Sicherheitsgarantie; setzen Sie Patches, Monitoring, Backup-Tests und wiederkehrende Prüfungen fort.";
    }

    document.getElementById("vps-security-result").textContent = result;
  });
});
</script>

## Vor Zugriffsänderungen einen Wiederherstellungsweg sichern {#keep-a-recovery-path-before-changing-access}

Bevor Sie SSH einschränken oder eine strenge Firewall aktivieren, prüfen Sie, ob Sie eine fehlerhafte Regel rückgängig machen können.

Halten Sie mindestens einen unabhängigen Verwaltungszugang verfügbar, etwa die Browserkonsole, VNC oder die Wiederherstellungsoberfläche des Anbieters.

Danach:

1. den zugeordneten Administratorbenutzer anlegen;
2. den öffentlichen SSH-Schlüssel hinzufügen;
3. eine **zweite** Terminalsitzung öffnen;
4. Anmeldung und sudo-/Administratorrechte prüfen;
5. die funktionierende Sitzung während des Tests der neuen Richtlinie geöffnet lassen;
6. erst dann alte Zugriffsmethoden einschränken.

Die entscheidende Sicherheitsmaßnahme lautet nicht „Root so schnell wie möglich deaktivieren“, sondern **riskanten Zugriff durch einen getesteten sichereren Weg ersetzen, ohne sich auszusperren**.

Den Ablauf der ersten Bereitstellung beschreibt [Website auf einem VPS hosten]({{< relref "how-to-host-a-website-on-vps.md" >}}).

## Erreichbare Dienste vor dem Sperren erfassen {#inventory-exposed-services-before-blocking}

Raten Sie nicht, welche Ports offen sind.

Unter Linux prüfen Sie lauschende Sockets mit Werkzeugen wie:

```bash
sudo ss -lntup
```

Klären Sie für jeden Listener:

- Muss der Dienst überhaupt vorhanden sein?
- Muss er auf allen Schnittstellen lauschen?
- Muss er öffentlich erreichbar sein?
- Kann er nur an localhost oder ein privates Netzwerk gebunden werden?
- Aus welchen Quellnetzen soll er erreichbar sein?
- Wer verantwortet seine Updates und Protokolle?

Typische öffentliche Website-Ports können umfassen:

- SSH-/Administratorzugriff;
- HTTP 80;
- HTTPS 443.

Das bedeutet **nicht**, dass jeder Server alle drei für das gesamte Internet öffnen sollte.

Entfernen Sie ungenutzte Dienste, statt sie nur hinter der Firewall zu verbergen.

## Administratorzugriff härten {#harden-administrative-access}

Die OpenSSH-Dokumentation von Ubuntu unterstützt die Authentifizierung mit öffentlichen Schlüsseln und empfiehlt moderne Schlüsselalgorithmen wie Ed25519.

Ein grundlegendes Administrationsmodell umfasst:

- ein zugeordnetes Administratorkonto;
- SSH-Schlüsselauthentifizierung;
- nach Möglichkeit einen durch Passphrase geschützten privaten Schlüssel;
- sudo nur für Nutzer, die es benötigen;
- keine als Root ausgeführte Anwendung;
- eingeschränkte direkte Root-/Passwortanmeldung per SSH, nachdem der sicherere Zugang geprüft wurde.

Für Umgebungen mit höheren Sicherheitsanforderungen unterstützt OpenSSH auch stärkere Authentifizierungsmodelle, darunter FIDO/U2F oder TOTP-basierte Zwei-Faktor-Authentifizierung.

### Root-Anmeldung und Passwortauthentifizierung {#root-login-and-password-authentication}

Setzen Sie diese Optionen nicht ungeprüft, bevor Schlüsselzugriff und Wiederherstellungskonsole getestet sind.

Nachdem der sicherere Weg funktioniert, prüfen Sie:

- `PermitRootLogin`;
- `PasswordAuthentication`;
- `AllowUsers` / `AllowGroups`;
- bei Bedarf Regeln für Leerlauf und Sitzungen.

Die genaue Richtlinie hängt von der Umgebung ab.

Eine Verlegung von SSH weg von Port 22 kann Scannerrauschen verringern. Sie ersetzt jedoch **nicht** Schlüssel, minimale Rechte, Firewall-Regeln und gepflegte Software.

## Firewall: nur benötigte Dienste freigeben {#firewall-only-the-services-you-need}

UFW ist die standardmäßige Oberfläche für die Host-Firewall unter Ubuntu.

Ein sicherer Grundschutz umfasst konzeptionell:

- unaufgeforderten eingehenden Datenverkehr standardmäßig sperren;
- den tatsächlich verwendeten Administrationszugang erlauben;
- HTTP/HTTPS für einen öffentlichen Webserver erlauben;
- Datenbanken und interne Dienste privat halten;
- IPv4- und IPv6-Verhalten prüfen.

Sichern Sie den SSH-Zugriff, bevor Sie einschränkende Regeln aktivieren.

Beispiel zur Prüfung:

```bash
sudo ufw status verbose
```

Übernehmen Sie keine allgemeine Liste „22/80/443 erlauben“, wenn Ihre Architektur davon abweicht.

### Anbieter-Firewall und Host-Firewall {#provider-firewall-and-host-firewall}

Eine Anbieter-/Netzwerk-Firewall kann Datenverkehr sperren, bevor er die virtuelle Maschine erreicht.

Eine Host-Firewall steuert, was das Gastbetriebssystem annimmt.

Beide gemeinsam können zusätzliche Schutzschichten bieten, aber nur, wenn die Regeln dokumentiert sind und sich nicht widersprechen.

## Datenbanken und interne Dienste standardmäßig privat halten {#keep-databases-and-internal-services-private-by-default}

Veröffentlichen Sie MySQL/MariaDB/PostgreSQL, Redis, interne Node-/Python-Anwendungsports oder Steuerungssockets nicht allein deshalb im Internet, weil der Dienst auf Verbindungen wartet.

Bevorzugen Sie:

- localhost für Dienste auf demselben Server;
- private Netzwerkschnittstellen für Architekturen mit mehreren Servern;
- Beschränkung auf Quell-IP-Adressen, wenn Fernadministration notwendig ist;
- SSH-/VPN-/Bastion-Zugriff für Administrationsabläufe.

Öffnen Sie einen Datenbankport nur dann öffentlich, wenn die Architektur dies ausdrücklich erfordert und der Zugriff stark eingeschränkt ist.

## Patches und automatische Sicherheitsupdates {#patching-and-automatic-security-updates}

Ein unterstütztes Betriebssystem veraltet, wenn niemand den Patch-Prozess verantwortet.

Ubuntu Server verwendet auf unterstützten Installationen standardmäßig `unattended-upgrades` für automatische Sicherheitsupdates.

Das hilft, aber der Sicherheitsprozess muss auch folgende Fragen beantworten:

- Welche Paketquellen werden erfasst?
- Werden Pakete und Anwendungen von Drittanbietern aktualisiert?
- Musste ein Dienst neu gestartet werden?
- Ist ein Serverneustart erforderlich?
- Wer prüft fehlgeschlagene Updates?
- Wann können produktive Dienste sicher neu gestartet werden?

Die Ubuntu-Dokumentation weist darauf hin, dass Dienstneustarts und manchmal ein Serverneustart nötig sein können, damit aktualisierter Code tatsächlich wirksam wird.

Betrachten Sie „automatische Updates aktiviert“ nicht als vollständigen Patch-Management-Prozess.

## Fail2ban, CrowdSec und Ratenbegrenzung {#fail2ban-crowdsec-and-rate-limiting}

Werkzeuge zum Brute-Force-Schutz können wiederholte missbräuchliche Versuche verringern.

Sie sind eine **zusätzliche Schutzschicht**, nicht das primäre Authentifizierungsmodell.

Setzen Sie sie ein, nachdem:

- privilegierter Zugriff geschützt ist;
- starke Authentifizierung eingerichtet ist;
- erreichbare Dienste bewusst öffentlich sind;
- Protokolle verfügbar sind.

Ein Sperrwerkzeug macht weder ein schwaches Passwort noch ein ungepatchtes Panel oder eine öffentlich erreichbare Datenbank sicher.

## Minimale Rechte für Anwendungen und Datenbanken {#least-privilege-for-applications-and-databases}

Das Prinzip minimaler Rechte gilt für den gesamten Stack.

Bevorzugen Sie:

- getrennte Deployment- und Administratorbenutzer;
- eigene Anwendungsbenutzer;
- eigene Datenbankbenutzer pro Anwendung;
- nur erforderliche Datenbankrechte;
- getrennte Nutzer für unabhängige Kunden-Websites;
- schreibbare Verzeichnisse nur dort, wo die Anwendung sie benötigt.

Vermeiden Sie:

- Webanwendungen als Root auszuführen;
- Anwendungen das Root-/Administratorkonto der Datenbank zu geben;
- `chmod 777` als Lösung für Berechtigungsprobleme;
- einen gemeinsamen Unix-Benutzer für unabhängige Kunden-Websites, wenn stärkere Trennung praktikabel ist.

Die Trennung mehrerer Websites behandelt [VPS für mehrere Websites]({{< relref "vps-for-multiple-websites.md" >}}).

## Geheimnisse und Zugangsdaten schützen {#protect-secrets-and-credentials}

Halten Sie produktive Zugangsdaten fern von:

- öffentlichen Git-Repositories;
- über das Web erreichbaren Dokumentverzeichnissen;
- Debug-Seiten;
- Screenshots, Tickets und Chats;
- nach Möglichkeit dem Shell-Verlauf;
- allgemein lesbaren Umgebungsdateien.

Schützen Sie:

- Datenbankpasswörter;
- API-Schlüssel;
- SMTP-Zugangsdaten;
- Zahlungs-/Webhook-Geheimnisse;
- Zugangsdaten zum Backup-Speicher;
- Panel-/Administratorzugangsdaten;
- private SSH-Schlüssel.

Erneuern Sie Zugangsdaten, wenn Mitarbeiter oder Auftragnehmer ausscheiden oder eine Kompromittierung vermutet wird.

## Control Panels und Administrationsoberflächen {#control-panels-and-admin-interfaces}

Ein Control Panel ist eine privilegierte Verwaltungsanwendung.

Prüfen Sie:

- aktuelle Panel-Version;
- Panel-Administratorkonten;
- 2FA, sofern vom Panel unterstützt;
- erreichbare Administrationsports und -hostnamen;
- Einschränkungen auf Quell-IP-Adressen, soweit betrieblich praktikabel;
- Bestand an Plugins und Erweiterungen;
- Backup-/Wiederherstellungsverhalten;
- Panel-Protokolle und fehlgeschlagene Anmeldungen.

Gehen Sie nicht davon aus, dass die Installation eines Panels den VPS sicher oder verwaltet macht.

Zur Panel-Auswahl siehe [VPS mit Control Panel]({{< relref "vps-with-control-panel.md" >}}). Den konkreten FASTPANEL-Weg behandelt [VPS-Hosting mit FASTPANEL]({{< relref "fastpanel-vps-hosting.md" >}}).

## Anwendungs-, CMS- und Laufzeitupdates {#application-cms-and-runtime-updates}

Ein vollständig gepatchtes Betriebssystem kann dennoch eine verwundbare Anwendung hosten.

Die Sicherheitsverantwortung muss auch Folgendes umfassen:

- PHP/Node/Python/Laufzeit;
- Framework;
- WordPress-Kern;
- Plugins/Themes;
- WooCommerce/Erweiterungen;
- Webserver;
- Control Panel;
- Bibliotheken/Abhängigkeiten.

Entfernen Sie aufgegebene Komponenten, die keine Sicherheitsupdates mehr erhalten.

WordPress-spezifischen Betrieb behandelt [VPS für WordPress]({{< relref "vps-for-wordpress.md" >}}). Für transaktionsbasierte Shops siehe [VPS für WooCommerce]({{< relref "vps-for-woocommerce.md" >}}).

## HTTPS schützt den Transport, nicht den ganzen Server {#https-protects-transport-not-the-whole-server}

HTTPS ist für produktive Websites mit Anmeldungen oder sensiblen Daten erforderlich und gehört zum üblichen Grundschutz öffentlicher Websites.

Es schützt Daten während der Übertragung zwischen Client und Server.

Es behebt nicht:

- verwundbare Plugins;
- schwache SSH-Absicherung;
- öffentliche Datenbanken;
- offengelegte API-Schlüssel;
- veraltete Pakete;
- unsichere Dateiberechtigungen;
- fehlende Backups.

Prüfen Sie die Zertifikatserneuerung und überwachen Sie Ablauf sowie Fehler.

## DDoS-Schutz ist keine Anwendungssicherheit {#ddos-protection-is-not-application-security}

VDSina wirbt derzeit bei Standard-VPS mit kostenlosem DDoS-Schutz.

Die öffentlich zugänglichen Fragen und Antworten beschreiben den kostenlosen Dienst als Schutz gegen **L3-L4-Angriffe auf Kanal-/Netzwerkebene** und ausdrücklich **ohne SLA**.

Dieser Schutz ist auf Infrastruktur- und Netzwerkebene hilfreich, ersetzt aber nicht:

- SSH-Härtung;
- Firewall-Regeln;
- Webanwendungssicherheit;
- Ratenbegrenzung auf Anwendungsebene;
- gegebenenfalls WAF-/Bot-Schutz;
- Patches;
- Reaktion auf Sicherheitsvorfälle.

Beschreiben Sie DDoS-Abwehr auf Netzwerkebene nicht als vollständigen Website-Sicherheitsdienst.

<p>
  <a class="btn btn-primary" href="https://www.vdsina.com/?partner=ni8gzrvz75" target="_blank" rel="sponsored nofollow noopener">Aktuelle VPS-Infrastruktur prüfen</a>
</p>
<p><small>Offenlegung: Der Herausgeber steht in einer beruflichen Beziehung zu VDSina. Diese Website kann eine Provision erhalten, wenn Sie über diesen Partnerlink bestellen. DDoS-Schutz und technischer Support des Anbieters ersetzen weder Härtung von Gastbetriebssystem und Anwendung noch Administration.</small></p>

## Backups sind eine Sicherheitsmaßnahme {#backups-are-a-security-control}

Zur Sicherheit gehört die Fähigkeit, nach Kompromittierung, Ransomware, fehlerhaften Updates oder versehentlichem Löschen wiederherzustellen.

Mindestens erforderlich:

- eine Kopie außerhalb des laufenden VPS aufbewahren;
- sich nicht allein auf einen Snapshot oder ein Image verlassen;
- Backup-Zugangsdaten schützen;
- Backups nach Möglichkeit dem Zugriff der Anwendung entziehen;
- fehlgeschlagene Backup-Aufträge überwachen;
- Wiederherstellung testen;
- wissen, wie viele Daten zwischen Wiederherstellungspunkten verloren gehen können.

CISA empfiehlt, kritische Daten offline und verschlüsselt zu sichern sowie die Wiederherstellung regelmäßig in einem Notfallwiederherstellungsszenario zu testen.

Die ausführliche Planung von RPO/RTO, Aufbewahrung und Backup-Architektur behandelt die [VPS-Backup-Strategie]({{< relref "vps-backup-strategy.md" >}}).

## Protokolle, Alarme und Nachvollziehbarkeit {#logs-alerts-and-audit-trail}

Eine sichere Konfiguration, die nie beobachtet wird, kann unbemerkt versagen.

Achten Sie mindestens auf:

- wiederholte SSH-/Authentifizierungsfehler;
- unerwartete neue Administrator-/sudo-Nutzer;
- fehlgeschlagene Panel-Anmeldungen;
- Firewall-Änderungen;
- neue lauschende Ports;
- Dienstabstürze und -neustarts;
- volle Datenträger;
- Spitzen bei 5xx-Fehlern von Anwendung und Webserver;
- Backup-Fehler;
- Fehler bei der Zertifikatserneuerung;
- Meldungen von Malware-/Sicherheitswerkzeugen, sofern eingesetzt.

Bewahren Sie Protokolle lange genug für die Untersuchung von Vorfällen auf.

Das vertiefte Schwellenwert- und Alarmkonzept behandelt [VPS-Monitoring]({{< relref "vps-monitoring.md" >}}).

## Bei Verdacht auf eine Kompromittierung {#after-a-suspected-compromise}

Wenn Sie eine Kompromittierung mit privilegierten oder Root-Rechten vermuten, vertrauen Sie einer spontanen „Bereinigung“ nicht sofort als Beleg für einen sicheren Server.

Ein sichereres Vorgehen:

1. den betroffenen VPS beziehungsweise Netzwerkzugang **isolieren**;
2. relevante Protokolle und Beweise nach Möglichkeit sichern;
3. feststellen, welche Zugangsdaten und Geheimnisse offengelegt worden sein könnten;
4. diese Zugangsdaten von einem sauberen, vertrauenswürdigen System aus erneuern;
5. einen nachweislich sauberen Wiederherstellungspunkt für Anwendung und Daten bestimmen;
6. den Server gegebenenfalls aus nachweislich sauberen Betriebssystem- und Konfigurationsquellen neu aufbauen;
7. geprüfte Daten wiederherstellen, statt kompromittierte ausführbare Dateien oder Konfigurationen ungeprüft zurückzuspielen;
8. die Ursache des Erstzugriffs untersuchen, bevor produktiver Datenverkehr wieder zugelassen wird.

Die CISA-Hinweise zur Vorfallreaktion betonen Isolation, Prüfung von Beweisen und Protokollen sowie Wiederherstellung aus validierten Backups.

Ziehen Sie bei geschäftskritischen Systemen eine qualifizierte Fachkraft für Vorfallreaktion und Sicherheit hinzu.

## Die Checkliste wiederholen {#repeat-the-checklist}

Sicherheit ist keine einmalige Aufgabe bei der Bereitstellung.

Prüfen Sie in festgelegten Abständen:

- Administratorbenutzer und SSH-Schlüssel;
- sudo-Berechtigungen;
- offene/lauschende Ports;
- Firewall-Regeln;
- nicht mehr unterstützte Pakete und Betriebssystemversionen;
- ausstehende Sicherheitsupdates;
- Control-Panel-/CMS-/Plugin-Versionen;
- erfolgreiche Backups und Wiederherstellungstests;
- Zertifikatsablauf und -erneuerung;
- Protokolle und Alarme;
- ungenutzte Konten und Dienste;
- offengelegte Geheimnisse;
- Kontakte für Sicherheitsvorfälle.

Wiederholen Sie die Checkliste außerdem nach größeren Migrationen, Panel-Wechseln, neuen Diensten oder Architekturänderungen.

## Sicherheitscheckliste für den Produktivbetrieb {#production-security-checklist}

| Maßnahme | Erfolgskriterium |
|---|---|
| Wiederherstellungszugriff | Anbieterkonsole/Wiederherstellungszugang funktioniert |
| Administratoranmeldung | zugeordneter Benutzer ohne direkte Root-Anmeldung und getestete Schlüsselanmeldung |
| SSH-Regeln | Root-/Passwortregeln nach sicherem Ersatzzugang bewusst konfiguriert |
| Dienste | lauschende Ports erfasst und begründet |
| Firewall | standardmäßig sperrend, minimale Erreichbarkeit; notwendiger Administrator-/Webzugriff getestet |
| Interne Dienste | Datenbank-/Cache-/Anwendungsports ohne ausdrücklichen Bedarf nicht öffentlich |
| Patches | Verantwortliche für Betriebssystem und Anwendungen benannt; Dienst-/Serverneustarts geklärt |
| Minimale Rechte | Anwendungen, Datenbanken und Nutzer erhalten nur notwendigen Zugriff |
| Geheimnisse | weder öffentlich noch über das Web oder allgemein lesbar |
| Panel-/Administrationsoberfläche | gepatcht; Administratorzugriff, 2FA und Einschränkungen geprüft |
| TLS | gültiges HTTPS und funktionierender Erneuerungsweg |
| Brute-Force-Schutz | dort als zusätzliche Schutzschicht eingesetzt, wo sinnvoll |
| Backups | unabhängige Kopie und Wiederherstellungstest |
| Protokollierung | Authentifizierungs-, Administrator-, Dienst- und Backup-Fehler erkennbar |
| DDoS | Umfang des Anbieter-/Netzwerkschutzes verstanden |
| Vorfallreaktion | Verantwortliche, Isolation und saubere Wiederherstellung festgelegt |
| Wiederkehrende Prüfung | nächster Prüfungstermin beziehungsweise Ablauf festgelegt |

## Technische Referenzen {#technical-references}

- Ubuntu Server — OpenSSH
- Ubuntu Server — Firewall/UFW
- Ubuntu Server — automatische Updates
- CISA — StopRansomware-Leitfaden
- VDSina Standard VPS
- VDSina Fragen und Antworten — Umfang des DDoS-Schutzes

## FAQ {#faq}

### Was sollte ich bei einem neuen VPS zuerst absichern? {#what-should-i-secure-first-on-a-new-vps}

Erhalten Sie den Konsolen-/Wiederherstellungszugriff, legen Sie einen zugeordneten Administratorbenutzer mit SSH-Schlüsselanmeldung statt direkter Root-Anmeldung an und testen Sie ihn. Erfassen Sie lauschende Dienste und verschärfen Sie erst danach SSH- und Firewall-Regeln. Vermeiden Sie mehrere Änderungen mit Aussperrungsrisiko, bevor der Zugriff geprüft wurde.

### Sollte ich die SSH-Passwortanmeldung deaktivieren? {#should-i-disable-ssh-password-login}

Schlüsselbasierte Administratorauthentifizierung ist für typische VPS-Administration stärker. Prüfen Sie jedoch zuerst Schlüsselanmeldung und Wiederherstellungskonsole. Deaktivieren Sie nicht den einzigen funktionierenden Zugang.

### Sollte ich den SSH-Port ändern? {#should-i-change-the-ssh-port}

Das kann Scanner- und Protokollrauschen verringern, ist aber keine primäre Sicherheitsmaßnahme. Starke Authentifizierung, minimale Rechte, Firewall-Regeln und Patches sind wichtiger.

### Brauche ich Fail2ban? {#do-i-need-fail2ban}

Nicht immer, aber es kann eine nützliche zusätzliche Schutzschicht gegen wiederholten Anmeldemissbrauch sein. SSH-Schlüssel, Patches und korrekt begrenzte Diensterreichbarkeit ersetzt es nicht.

### Welche Ports sollten auf einem VPS offen sein? {#which-ports-should-be-open-on-a-vps}

Nur die von der Architektur benötigten Ports. Ein öffentlicher Webserver braucht gewöhnlich HTTP/HTTPS und einen kontrollierten Administrationszugang. Datenbanken und interne Anwendungsdienste sollten normalerweise privat bleiben.

### Schützt eine Firewall eine verwundbare Anwendung? {#does-a-firewall-protect-a-vulnerable-application}

Nein. Eine Firewall begrenzt die Netzwerkerreichbarkeit. Eine öffentlich erreichbare Webanwendung benötigt weiterhin sicheren Code, unterstützte Abhängigkeiten, Updates und Schutzmaßnahmen auf Anwendungsebene.

### Reichen automatische Sicherheitsupdates aus? {#are-automatic-security-updates-enough}

Nein. Sie helfen bei unterstützten Betriebssystempaketen. Anwendungen und Abhängigkeiten von Drittanbietern können gesonderte Updates benötigen; auch Dienst- oder Serverneustarts müssen unter Umständen weiterhin betrieblich organisiert werden.

### Reicht HTTPS zur Absicherung eines VPS? {#is-https-enough-to-secure-a-vps}

Nein. HTTPS schützt die Übertragung. Es behebt keine schwache SSH-Absicherung, öffentlichen Datenbanken, verwundbaren Plugins, veralteten Pakete, offengelegten Geheimnisse oder fehlenden Backups.

### Reicht der DDoS-Schutz von VDSina zur Absicherung der Website? {#is-vdsina-ddos-protection-enough-to-secure-the-website}

Nein. VDSina wirbt derzeit mit kostenlosem DDoS-Schutz. Die öffentlichen Fragen und Antworten beschreiben diesen als L3-L4-Schutz ohne SLA. Gastbetriebssystem, Zugriff, Anwendung und Wiederherstellung müssen weiterhin abgesichert werden.

### Was sollte ich bei Verdacht auf eine VPS-Kompromittierung tun? {#what-should-i-do-if-i-suspect-the-vps-was-compromised}

Isolieren Sie das System, sichern Sie relevante Beweise und Protokolle und erneuern Sie offengelegte Zugangsdaten von einem sauberen System aus. Bei Verdacht auf privilegierte Kompromittierung ist ein Neuaufbau aus nachweislich sauberen Quellen mit geprüften Backups vorzuziehen. Ziehen Sie bei kritischen Systemen eine Fachkraft für Vorfallreaktion hinzu.
