---
title: "Website auf einen VPS umziehen"
description: "Website auf einen VPS umziehen: Bestand erfassen, Zielserver testen, letzte Schreibvorgänge kontrollieren, DNS sicher umstellen sowie E-Mail, SEO und Rückfallweg erhalten."
image: "images/home/vps-for-website-hero.webp"
slug: "website-auf-einen-vps-umziehen"
---

Am sichersten ziehen Sie eine Website auf einen VPS um, indem Sie den neuen Server aufbauen und testen, während der bisherige Host weiter Anfragen bedient. Erfassen Sie den bestehenden Software-Stack, dimensionieren Sie das Ziel, kopieren und prüfen Sie die Website, kontrollieren Sie die letzten Datenänderungen und stellen Sie DNS zuletzt um. Überwachen Sie anschließend beide Umgebungen, bis der bisherige Host außer Betrieb gehen kann.

Diese Anleitung setzt voraus, dass Domain und öffentliche URL-Struktur unverändert bleiben. Ändern sich auch Domain oder Pfade, sind URL-Zuordnung und permanente Weiterleitungen eine zusätzliche Migrationsaufgabe.

Die übergeordnete Hosting-Entscheidung behandelt [VPS für Websites]({{< relref "_index.md" >}}).

[Kurzplan](#quick-migration-plan) · [Vorabprüfung](#migration-cutover-preflight) · [Letzte Synchronisierung](#control-new-writes-and-the-final-sync) · [DNS-Umschaltung](#switch-dns-deliberately) · [SEO-Prüfungen](#preserve-seo-when-urls-stay-the-same) · [FAQ](#faq)

## Der Migrationsplan im Überblick {#quick-migration-plan}

Ein kontrollierter Umzug folgt dieser Reihenfolge:

1. **Das Quellsystem erfassen.** Dokumentieren Sie Anwendung, Laufzeit, Datenbank, Dateien, DNS, E-Mail, Cronjobs, Worker, Webhooks und externe Abhängigkeiten.
2. **Das Ziel dimensionieren.** Wählen Sie CPU, RAM und Speicher nach tatsächlicher Last und zusätzlichem Platzbedarf für die Migration.
3. **Ein wiederherstellbares Backup erstellen.** Bewahren Sie eine Kopie außerhalb des Quellservers auf und prüfen Sie, ob die benötigten Datenbanken und Dateien tatsächlich enthalten sind.
4. **Den VPS parallel aufbauen.** Installieren Sie Web-Stack oder Control Panel und erfüllen Sie die Anwendungsanforderungen, bevor Zugriffe umgeleitet werden.
5. **Den ersten vollständigen Datenbestand kopieren.** Übertragen Sie Dateien und importieren Sie die Datenbank, während die bisherige Website online bleibt.
6. **Nicht öffentlich testen.** Prüfen Sie den neuen Server vor DNS-Änderungen über einen lokalen hosts-Eintrag, einen kontrollierten Vorschau-Hostnamen oder ein vergleichbares Verfahren.
7. **Die letzten Schreibvorgänge kontrollieren.** Planen Sie für Shops, Mitgliederbereiche, Formulare und andere veränderliche Websites eine kurze Schreibpause oder eine zur Anwendung passende abschließende Synchronisierung der Änderungen.
8. **DNS zuletzt umstellen.** Ändern Sie nur die erforderlichen Einträge und erhalten Sie Mail- und Verifizierungseinträge.
9. **Beide Server überwachen.** Prüfen Sie Zugriffe, Fehler, Formulare, Bestellungen, Cronjobs, Webhooks, E-Mail, HTTPS und Suchmaschinen-Crawling.
10. **Den bisherigen Host erst nach Abnahme abschalten.** Halten Sie ihn während des vereinbarten Rückfallzeitraums verfügbar.

Eine pauschale Zusage ohne jede Ausfallzeit wäre nicht seriös. Das Ziel ist eine kontrollierte Umschaltung mit möglichst kurzer Unterbrechung und ohne ungeplanten Datenverlust.

## Festlegen, was tatsächlich umzieht {#define-what-is-actually-moving}

„Die Website umziehen“ kann mehrere unterschiedliche Systeme umfassen. Legen Sie den Umfang fest, bevor Sie etwas kopieren.

| Komponente | Vor dem Umzug zu klärende Fragen |
|---|---|
| Website / Anwendung | CMS oder Framework, Document Root, Uploads, versteckte Dateien, Cache, beschreibbare Verzeichnisse |
| Laufzeitumgebung | PHP-/Node-/Python-Version, Erweiterungen/Module, Webserver, Prozessmanager |
| Datenbank | System/Version, Größe, Benutzer/Berechtigungen, Zeichensatz, geplante Wartung |
| DNS | Anbieter, A-/AAAA-/CNAME-Einträge, Verhalten von www und Stammdomain, TTL, Verifizierungseinträge |
| E-Mail | Mail-Hosting, MX, SPF, DKIM, DMARC, Postfächer, Weiterleitungen, SMTP |
| Geplante Aufgaben | Cronjobs, Warteschlangen, Worker, Importe, Exporte, Backups, geplante Aktionen |
| Externe Systeme | Zahlungs-Webhooks, APIs, IP-Freigabelisten, CDN/WAF, Analytics, Search Console |
| Sicherheit / Zugangsdaten | Umgebungsvariablen, API-Schlüssel, SSH-Schlüssel, TLS, Firewall-Regeln |

Kombinieren Sie unabhängige Änderungen nicht ohne Grund. Ein Hosting-Umzug lässt sich leichter diagnostizieren, wenn nicht gleichzeitig Domain, URL-Struktur, Anwendungsversion und wesentliche Softwarekomponenten geändert werden.

## Vorabprüfung für die Umschaltung {#migration-cutover-preflight}

Nutzen Sie diese Prüfung vor der DNS-Änderung. Sie garantiert keine erfolgreiche Migration, zeigt aber fehlende Voraussetzungen, die zuerst geklärt werden sollten.

<div class="rounded-2xl bg-light p-6 dark:bg-darkmode-light">
<form id="migration-preflight">
  <div class="mb-6">
    <label for="mig-backup" class="form-label">Unabhängiges Backup vorhanden und Wiederherstellung/Import getestet</label>
    <select id="mig-backup" class="form-input"><option value="no">Nicht bereit</option><option value="yes">Bereit</option></select>
  </div>
  <div class="mb-6">
    <label for="mig-sizing" class="form-label">CPU, RAM und Speicher des Ziels mit Reserve dimensioniert</label>
    <select id="mig-sizing" class="form-input"><option value="no">Nicht bereit</option><option value="yes">Bereit</option></select>
  </div>
  <div class="mb-6">
    <label for="mig-runtime" class="form-label">Laufzeit, Datenbank und erforderliche Erweiterungen kompatibel</label>
    <select id="mig-runtime" class="form-input"><option value="no">Nicht bereit</option><option value="yes">Bereit</option></select>
  </div>
  <div class="mb-6">
    <label for="mig-test" class="form-label">Neue Website vor der DNS-Umschaltung in einer nicht öffentlichen Umgebung getestet</label>
    <select id="mig-test" class="form-input"><option value="no">Nicht bereit</option><option value="yes">Bereit</option></select>
  </div>
  <div class="mb-6">
    <label for="mig-dns" class="form-label">DNS-Einträge dokumentiert und TTL/Umschaltung geplant</label>
    <select id="mig-dns" class="form-input"><option value="no">Nicht bereit</option><option value="yes">Bereit</option></select>
  </div>
  <div class="mb-6">
    <label for="mig-mail" class="form-label">Mail-Hosting und Umgang mit MX/SPF/DKIM/DMARC festgelegt</label>
    <select id="mig-mail" class="form-input"><option value="no">Nicht bereit</option><option value="yes">Bereit</option><option value="na">Nicht zutreffend / E-Mail bleibt separat und unverändert</option></select>
  </div>
  <div class="mb-6">
    <label for="mig-writes" class="form-label">Plan für letzte Schreibvorgänge und Datensynchronisierung von Bestellungen, Formularen, Mitgliederdaten oder Uploads vorhanden</label>
    <select id="mig-writes" class="form-input"><option value="no">Nicht bereit</option><option value="yes">Bereit / Website wird praktisch nur gelesen</option></select>
  </div>
  <div class="mb-6">
    <label for="mig-tls" class="form-label">HTTPS/TLS funktioniert am Ziel mit dem tatsächlichen Hostnamen</label>
    <select id="mig-tls" class="form-input"><option value="no">Nicht bereit</option><option value="yes">Bereit</option></select>
  </div>
  <div class="mb-6">
    <label for="mig-jobs" class="form-label">Cronjobs, Worker, Webhooks und IP-Freigabelisten dokumentiert und kontrolliert</label>
    <select id="mig-jobs" class="form-input"><option value="no">Nicht bereit</option><option value="yes">Bereit</option><option value="na">Nicht zutreffend</option></select>
  </div>
  <div class="mb-6">
    <label for="mig-rollback" class="form-label">Auslöser für Rollback festgelegt und bisheriger Host bleibt verfügbar</label>
    <select id="mig-rollback" class="form-input"><option value="no">Nicht bereit</option><option value="yes">Bereit</option></select>
  </div>
  <button class="btn btn-primary" type="submit">Bereitschaft zur Umschaltung prüfen</button>
</form>
<p id="migration-preflight-result" class="mt-6 rounded border border-border p-4 dark:border-darkmode-border" role="status" aria-live="polite">Markieren Sie die Punkte, die tatsächlich erfüllt sind.</p>
</div>

<script>
document.addEventListener("DOMContentLoaded", function () {
  var form = document.getElementById("migration-preflight");
  if (!form) return;

  form.addEventListener("submit", function (event) {
    event.preventDefault();

    var items = [
      ["mig-backup", "unabhängiges Backup"],
      ["mig-sizing", "Dimensionierung des Ziels"],
      ["mig-runtime", "Kompatibilität von Laufzeit und Datenbank"],
      ["mig-test", "nicht öffentliche Tests des Ziels"],
      ["mig-dns", "DNS-/TTL-Plan"],
      ["mig-mail", "Plan für E-Mail und zugehörige DNS-Einträge"],
      ["mig-writes", "Plan für letzte Schreibvorgänge und Datensynchronisierung"],
      ["mig-tls", "HTTPS-/TLS-Bereitschaft"],
      ["mig-jobs", "Cronjobs/Worker/Webhooks/Freigabelisten"],
      ["mig-rollback", "Rollback-Plan"]
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
      result = "BEREIT FÜR EINE KONTROLLIERTE UMSCHALTUNG: Alle erforderlichen Punkte sind als bereit oder ausdrücklich nicht zutreffend markiert. Prüfen Sie unmittelbar vor der DNS-Änderung nochmals die letzte Datensynchronisierung und den Rollback-Auslöser.";
    } else {
      result = "NICHT BEREIT ZUR UMSCHALTUNG: Klären Sie zuerst diese offenen Punkte: " + missing.join(", ") + ".";
    }

    document.getElementById("migration-preflight-result").textContent = result;
  });
});
</script>

## Die bestehende Website erfassen {#inventory-the-current-website}

Legen Sie eine Migrationsdokumentation an, bevor Sie am Zielsystem arbeiten.

Dokumentieren Sie:

- Domain und jede aktive Subdomain;
- Version von Anwendung, CMS oder Framework;
- Version von PHP, Node.js, Python oder anderer Laufzeit;
- Datenbanksystem/-version, Größe und Berechtigungsmodell;
- Document Root und Verzeichnisse außerhalb davon;
- Uploads/Medien und beschreibbare Verzeichnisse;
- Weiterleitungen und Rewrite-Regeln;
- Cronjobs, Warteschlangen, Worker und geplante Aufgaben;
- verwendete Cache-Dienste wie Redis;
- SSL-/TLS-Konfiguration;
- DNS-Einträge;
- Postfächer, Weiterleitungen und ausgehenden SMTP-Pfad;
- Zahlungsanbieter, Webhooks und API-Callbacks;
- IP-Freigabelisten externer Dienste;
- CDN-/WAF-/Ursprungsbeschränkungen;
- Search-Console-/Analytics-Verifizierung;
- aktuelle Speicherbelegung und Wachstum.

Diese Bestandsaufnahme ist zugleich die Abnahmecheckliste nach dem Umzug: Jeder Punkt sollte auf dem VPS funktionieren oder bewusst bei einem externen Dienst verbleiben.

## Den Ziel-VPS dimensionieren und vorbereiten {#size-and-prepare-the-destination-vps}

Ziehen Sie nicht zuerst um, um erst danach zu fragen, ob der VPS groß genug ist.

Wählen Sie das Ziel anhand aktueller Last, Datenbankverhalten, Datenwachstum, Panel-/Mail-Eigenbedarf und Arbeitsraum für die Migration. Der Umzug selbst kann vorübergehend Speicher für Archive, Datenbank-Dumps, Logs und lokale Backup-Zwischenablagen benötigen.

Nutzen Sie zur Ressourcenberechnung [VPS für Websites dimensionieren]({{< relref "vps-sizing-for-website.md" >}}), statt diese hier zu wiederholen.

Eine Migration ist auch eine Entscheidung über den späteren Betrieb. Hat der bisherige Hoster den Großteil der Serververwaltung übernommen, klären Sie zuerst, wer das Ziel nach der Umschaltung betreibt: Vergleichen Sie [Managed VPS vs. Unmanaged VPS]({{< relref "managed-vs-unmanaged-vps.md" >}}). Entscheiden Sie anschließend zwischen Control Panel und manuell verwaltetem Linux-Stack; dabei hilft [VPS mit Control Panel]({{< relref "vps-with-control-panel.md" >}}).

<p>
  <a class="btn btn-primary" href="https://www.vdsina.com/?partner=ni8gzrvz75" target="_blank" rel="sponsored nofollow noopener">Ziel-VPS auswählen</a>
</p>
<p><small>Offenlegung: Der Herausgeber steht in einer beruflichen Beziehung zu VDSina. Diese Website kann eine Provision erhalten, wenn Sie über diesen Partnerlink bestellen. Migrationshinweise und Dimensionierungskriterien ändern sich nicht aufgrund einer Provision.</small></p>

## Ein Backup erstellen, das einen Rollback ermöglicht {#create-a-rollback-capable-backup}

Ein Backup ist nur nützlich, wenn es die benötigten Daten enthält und wiederhergestellt werden kann.

Vor der Migration:

1. eine aktuelle Kopie der Website-Dateien erstellen;
2. jede benötigte Datenbank exportieren;
3. eine Kopie außerhalb des bisherigen Hosting-Kontos speichern;
4. Konfigurationsdateien und Umgebungsvariablen sicher dokumentieren;
5. DNS- und Mail-Einträge separat festhalten;
6. das Backup nach Möglichkeit in einer temporären Testumgebung wiederherstellen oder zumindest einen echten Datenbankimport durchführen und repräsentative Dateien prüfen, statt nur das Öffnen des Archivs zu testen;
7. bestätigen, dass die wiederhergestellte Kopie die erwarteten Daten enthält und weit genug startet, um einen Rollback zu ermöglichen;
8. den Rollback-Ablauf vor jeder DNS-Änderung aufschreiben.

Bei einer dynamischen Website ist das erste Backup noch nicht der endgültige Produktionsdatenbestand. Bestellungen, Formulareingaben, Kommentare, Mitgliederdaten und Uploads können sich nach der ersten Kopie weiter ändern. Planen Sie die Übernahme dieser letzten Änderungen separat.

## Das Ziel vor der DNS-Änderung aufbauen {#build-the-destination-before-dns-changes}

Das Ziel muss die Website betreiben können, bevor öffentliche Zugriffe eintreffen.

Gleichen Sie Folgendes ab oder prüfen Sie Abweichungen gezielt:

- Webserver-Verhalten;
- PHP-/Node-/Python-Version;
- erforderliche Erweiterungen/Module;
- Datenbanksystem/-version;
- Dateieigentümer und Berechtigungen;
- Upload- und Request-Body-Größenlimits;
- Ausführungsumgebung geplanter Aufgaben;
- Cache-Dienste;
- Rewrite- und Weiterleitungsregeln;
- Umgebungsvariablen und Geheimnisse;
- Anforderungen an SMTP und ausgehende Netzwerkverbindungen;
- Firewall-Regeln;
- anwendungsspezifische Pfade.

Nutzen Sie die Migration nicht gleichzeitig für ein Upgrade aller Laufzeiten oder einen vollständigen Umbau des Stacks, sofern das nicht erforderlich ist. Weniger gleichzeitige Änderungen erleichtern Diagnose und Rollback.

## Dateien und Datenbank kopieren {#copy-files-and-database}

Das konkrete Übertragungsverfahren hängt vom Zugriff auf das Quellsystem ab.

Typische Möglichkeiten sind:

- cPanel/Dateimanager und phpMyAdmin-Exporte;
- SFTP/FTP, wenn kein Shell-Zugriff möglich ist;
- SSH/rsync, wenn beide Seiten dies erlauben;
- anwendungsspezifische Migrationswerkzeuge für CMS-Umzüge;
- Export- oder Backup-Werkzeuge des Anbieters.

Erhalten Sie versteckte Konfigurationsdateien, beispielsweise Rewrite-Regeln, wenn die Anwendung sie benötigt. Prüfen Sie nach dem Import Datenbankbenutzer, Berechtigungen, Zeichensatz-/Kollationsannahmen und die Verbindungseinstellungen der Anwendung.

Vergleichen Sie bei großen Datenbeständen nach Möglichkeit Größen, Zeilenanzahlen oder Prüfsummen. „Übertragung abgeschlossen“ bedeutet nicht automatisch „Datenbestand identisch“.

## Vor der Umschaltung nicht öffentlich testen {#test-privately-before-cutover}

Richten Sie DNS nicht auf einen ungetesteten Server.

Testen Sie das Ziel über einen lokalen hosts-Eintrag, einen kontrollierten Vorschau-Hostnamen oder ein anderes nicht öffentliches Verfahren, das den tatsächlichen Anwendungs-Stack durchläuft.

Prüfen Sie:

- Startseite und repräsentative Unterseiten;
- Administratoranmeldung;
- Benutzeranmeldung;
- Bilder, CSS, JavaScript und Downloads;
- Suche;
- Formulare und deren Zustellung;
- Uploads;
- Weiterleitungen;
- API-Endpunkte;
- Checkout und Zahlungs-Callbacks;
- Cronjobs/geplante Aktionen;
- Warteschlangen/Worker;
- ausgehende E-Mail;
- Anwendungs-, Webserver- und Datenbankprotokolle;
- mobiles Layout und Navigation.

Ein vorübergehender öffentlicher Hostname darf nicht versehentlich als Suchmaschinen-Duplikat erscheinen. Ist er während der Tests öffentlich erreichbar, halten Sie ihn aus dem Index heraus. Entfernen Sie vor der Umschaltung temporäre Sperren vom eigentlichen Produktions-Hostnamen.

## Neue Schreibvorgänge und die letzte Synchronisierung kontrollieren {#control-new-writes-and-the-final-sync}

Hier liegt der wichtigste Unterschied zwischen einer reinen Informationswebsite und einer transaktionsorientierten Website.

Können alte und neue Datenbank während der DNS-Umstellung Schreibvorgänge annehmen, können ihre Daten auseinanderlaufen. Eine Bestellung auf dem alten Server erscheint nicht automatisch auf dem neuen.

Für Websites mit laufenden Änderungen:

1. ein möglichst risikoarmes Umschaltfenster wählen;
2. neue Schreibvorgänge am Ursprung nach Möglichkeit pausieren oder kontrollieren;
3. Cronjobs und Queue-Worker stoppen oder kontrollieren, die Daten doppelt schreiben könnten;
4. die Datenbank abschließend synchronisieren und geänderte Uploads/Dateien kopieren;
5. den letzten maßgeblichen Datenstand mit Zeitpunkt festhalten;
6. Zugriffe umschalten;
7. prüfen, dass neue Schreibvorgänge nur noch am Ziel ankommen.

Beim Einsatz eines [VPS für WooCommerce]({{< relref "vps-for-woocommerce.md" >}}) gehören Checkout, Bestellungen, Zahlungs-Webhooks, Lagerbestand, geplante Aktionen und Transaktions-E-Mails in den Abnahmetest. Bei einer statischen oder gecachten Website kann ein abschließender Dateivergleich genügen.

Bezeichnen Sie einen Umzug nur dann als „ohne Ausfallzeit“, wenn Anwendung und Synchronisierungsverfahren das tatsächlich ermöglichen.

## DNS gezielt umstellen {#switch-dns-deliberately}

DNS schaltet die Zugriffe um. Es ist nicht der erste Migrationsschritt.

Vor der Umschaltung:

- die aktuelle Zone exportieren oder dokumentieren;
- genau bestimmen, welche A-/AAAA-/CNAME-/Ursprungseinträge geändert werden müssen;
- die relevante TTL nach Möglichkeit mindestens ein vollständiges Intervall der bisherigen TTL vor der geplanten Umschaltung reduzieren; beträgt die aktuelle TTL beispielsweise 86400 Sekunden, senken Sie sie mehr als 24 Stunden vor dem Wechsel;
- beachten, dass eine jetzt reduzierte TTL bereits vorhandene Cache-Einträge mit der früheren längeren TTL nicht löscht;
- MX, SPF, DKIM, DMARC, Verifizierungs-TXT, SRV, CAA und andere nicht umzuziehende Einträge erhalten;
- das Verhalten von Stammdomain und www prüfen.

Eine Änderung des A-/AAAA-Eintrags ist normalerweise risikoärmer als ein Nameserverwechsel, wenn der DNS-Anbieter derselbe bleibt. Müssen die Nameserver wechseln, legen Sie zuerst die vollständige erforderliche Zone neu an.

Prüfen Sie nach der Umschaltung die öffentliche DNS-Auflösung über mehrere Resolver oder Netze und beobachten Sie, wie Zugriffe vom alten auf den neuen Server wechseln.

## Den E-Mail-Betrieb erhalten {#keep-email-from-breaking}

Website-Migration und E-Mail-Migration sind getrennte Aufgaben, auch wenn das bisherige Shared-Hosting-Konto beides gebündelt hat.

Entscheiden Sie vor der Umschaltung zwischen diesen Wegen:

- E-Mail beim bisherigen oder einem verwalteten Anbieter belassen und bestehende MX-/TXT-Einträge erhalten;
- E-Mail zu einem anderen verwalteten Anbieter umziehen;
- E-Mail auf den VPS verlagern und Postfächer, Routing, Authentifizierung und Zustellkontrollen neu einrichten.

Wenn E-Mail umzieht, berücksichtigen Sie:

- MX-Prioritäten;
- SPF;
- DKIM;
- DMARC;
- Reverse DNS/PTR, soweit erforderlich;
- Postfachdaten;
- Aliasse/Weiterleitungen;
- SMTP-Zugangsdaten;
- Spamfilter;
- Backups und Absenderreputation.

Ersetzen Sie nicht die gesamte DNS-Zone nur für einen Website-Umzug, ohne Mail-Einträge und alle übrigen Abhängigkeiten vollständig nachzubilden.

## HTTPS, CDN und externe Dienste prüfen {#verify-https-cdn-and-external-services}

Steht die Zielregion noch nicht fest, klären Sie das vor der Umschaltung mit [VPS-Standort auswählen]({{< relref "how-to-choose-vps-location.md" >}}). Ein späterer Regionswechsel kann einen weiteren IP-/DNS-Umzug erfordern.

Ein Ziel, das über seine IP funktioniert, kann unter dem tatsächlichen Hostnamen trotzdem fehlschlagen.

Prüfen Sie:

- das TLS-Zertifikat deckt die benötigten Hostnamen ab;
- die Weiterleitung HTTP → HTTPS ist korrekt;
- das kanonische Verhalten zwischen Stammdomain und www bleibt unverändert;
- HSTS-Annahmen sind bekannt;
- CDN/WAF verweist auf den neuen Ursprung oder lässt ihn zu;
- die Ermittlung der echten Client-IP funktioniert bei Proxy-Nutzung weiterhin;
- Zahlungs-Webhooks erreichen den neuen Ursprung;
- API-Anbieter mit Freigabe der alten Server-IP wurden aktualisiert;
- SMTP-/API-Zugangsdaten funktionieren vom neuen Server aus.

Begrenzen Sie temporäre Firewall-/WAF-Ausnahmen eng und entfernen Sie sie nach der Abnahme.

## SEO bei gleichbleibenden URLs erhalten {#preserve-seo-when-urls-stay-the-same}

Bei einem reinen Hosting-Wechsel bleiben die öffentlichen URLs normalerweise erhalten. Dann geht es bei SEO hauptsächlich um **gleichbleibendes Verhalten**, nicht um die Zuordnung neuer Weiterleitungsziele.

Vergleichen Sie vor und nach der Umschaltung:

- HTTP-Statuscodes;
- kanonische URLs;
- robots.txt;
- Meta-Robots und versehentliches noindex;
- Sitemap-URLs;
- interne Links;
- strukturierte Daten, soweit relevant;
- Seiteninhalt und gerenderte Ressourcen;
- Search-Console-Verifizierung;
- Serverantworten an Googlebot und normale Nutzer.

Google Search Central empfiehlt, das neue Hosting vorzubereiten und zu testen, DNS erst bei vollständiger Bereitschaft umzustellen, altes und neues Hosting zu überwachen und die bisherige Infrastruktur erst nach dem Wechsel der Zugriffe abzuschalten. Empfohlen werden außerdem eine vorab reduzierte DNS-TTL und eine weiterhin funktionierende Search-Console-Verifizierung.

Ändert sich nur die Hosting-Infrastruktur und bleiben Domain und URLs gleich, **verwenden Sie nicht das Tool zur Adressänderung in der Google Search Console**. Dieses Tool dient Domainumzügen, nicht einem Hosting-Wechsel bei unveränderten URLs.

Ändern sich auch Domain oder URL-Pfade, benötigen Sie eine Zuordnung alter zu neuen URLs und permanente serverseitige Weiterleitungen. Das ist eine andere Art von Website-Umzug als eine VPS-Migration mit unveränderten URLs.

## Checkliste für die Umschaltung {#cutover-checklist}

Unmittelbar vor der DNS-Änderung:

| Prüfung | Erfüllungskriterium |
|---|---|
| Backup | unabhängige Kopie vorhanden; Wiederherstellung/Import getestet und repräsentative Daten geprüft |
| Ziel | richtige Laufzeit, Datenbank, Berechtigungen und Zugangsdaten |
| Nicht öffentlicher Test | Seiten, Formulare, Anmeldung sowie gegebenenfalls Checkout/API funktionieren |
| Letzte Daten | abschließende Datenbank-/Upload-Änderungen übertragen; Zeitpunkt des maßgeblichen Datenstands dokumentiert |
| Jobs | bisherige Cronjobs/Worker kontrolliert; neue Jobs starten zum vorgesehenen Zeitpunkt |
| DNS | exakt zu ändernde Einträge bestimmt; Mail-/Verifizierungseinträge erhalten |
| HTTPS | Ziel kann den tatsächlichen Hostnamen sicher bedienen |
| Externe Dienste | Webhooks, Freigabelisten, CDN/WAF und SMTP berücksichtigt |
| SEO-Gleichwertigkeit | Canonical-/Robots-/Sitemap-/Statusverhalten entspricht dem vorgesehenen Zustand |
| Rollback | Auslöser, verantwortliche Handlung und Verfügbarkeit des alten Hosts festgelegt |

Schalten Sie nicht allein deshalb um, weil „die Dateien kopiert wurden“. Schalten Sie um, wenn das Ziel die Abnahmekriterien erfüllt.

## Abnahme und Rollback nach der Migration {#post-migration-acceptance-and-rollback}

Nach der DNS-Änderung:

- Zugriffs- und Fehlerprotokolle auf altem und neuem Server überwachen;
- bestätigen, dass neue Nutzeraktivität in der Zieldatenbank ankommt;
- Formulare, Checkout, Anmeldung und Uploads erneut testen;
- Cronjobs, Warteschlangen und geplante Aktionen prüfen;
- ausgehende E-Mail und gegebenenfalls eingehendes Mail-Routing prüfen;
- CPU, RAM, Speicher und Datenbankverhalten beobachten;
- HTTPS- und CDN-/WAF-Verhalten bestätigen;
- bei wichtigen URLs gleichbleibende 200-/Weiterleitungsantworten prüfen;
- Crawling- und Indexierungssignale in der Search Console beobachten;
- die alte Umgebung während des vereinbarten Stabilitätszeitraums verfügbar halten.

### Beim Rollback ist der Datenstand entscheidend {#rollback-has-a-data-boundary}

Ein früher Rollback kann sich auf das Zurückstellen von DNS beschränken, **solange der alte Server noch einen gültigen maßgeblichen Datenstand enthält**.

Sobald Bestellungen, Registrierungen, Kommentare oder Uploads auf den neuen Server geschrieben werden, kann ein reiner DNS-Rollback diese Änderungen verlieren. Ab diesem Zeitpunkt erfordert der Rollback einen Datenabgleich oder eine weitere geplante Synchronisierung.

Legen Sie Rollback-Auslöser vor der Migration fest, beispielsweise:

- weitverbreitete 5xx-Fehler;
- Ausfall von Checkout oder Zahlungen;
- Datenbankbeschädigung oder fehlende Schreibvorgänge;
- schwerwiegende Laufzeitinkompatibilität;
- fehlerhafte Authentifizierung;
- kritischer Mail-/Webhook-Ausfall, der innerhalb des vereinbarten Zeitfensters nicht behoben werden kann.

## Hinweise zu WordPress, WooCommerce und eigenen Anwendungen {#wordpress-woocommerce-and-custom-application-notes}

### WordPress {#wordpress}

Prüfen Sie PHP-Version und -Erweiterungen, Datenbankkompatibilität, Uploads, Rewrite-Regeln, wp-cron-Verhalten, Caching, SMTP/Kontaktformulare und Administratoranmeldung. Vermeiden Sie ungezieltes Suchen und Ersetzen, das serialisierte Daten beschädigen kann. Verwenden Sie bei Bedarf Werkzeuge, die das Datenformat der Anwendung berücksichtigen.

Den Ressourcenbedarf behandelt [VPS für WordPress]({{< relref "vps-for-wordpress.md" >}}).

### WooCommerce und andere transaktionsorientierte Websites {#woocommerce-and-other-transactional-sites}

Behandeln Sie Bestellungen, Lagerbestand, Zahlungs-Callbacks, Sitzungen, geplante Aktionen und Transaktions-E-Mails als laufend veränderliche Daten. Planen Sie die endgültige Umschaltung von Datenbank und Schreibzugriffen, statt sich auf die erste Kopie zu verlassen.

Siehe [VPS für WooCommerce]({{< relref "vps-for-woocommerce.md" >}}).

### Eigene Anwendungen {#custom-applications}

Dokumentieren Sie Umgebungsvariablen, Geheimnisse, Hintergrund-Worker, Warteschlangen, Build-/Laufzeitversionen, Objektspeicher, Dateipfade, Webhooks, API-Freigabelisten sowie Deployment- und Startverhalten. Testen Sie das Verhalten unter dem tatsächlichen Hostnamen, nicht nur eine Antwort über die IP-Adresse.

## Technische Referenzen {#technical-references}

- Google Search Central: Webhosting wechseln und SEO
- Google Search Central: Websiteumzüge mit URL-Änderungen

<p>
  <a class="btn btn-primary" href="https://www.vdsina.com/?partner=ni8gzrvz75" target="_blank" rel="sponsored nofollow noopener">VPS für den Umzug auswählen</a>
</p>
<p><small>Offenlegung: Der Herausgeber steht in einer beruflichen Beziehung zu VDSina. Partnerlinks sind als sponsored gekennzeichnet. VPS-Preise, Transferkontingente und andere Anbieterbedingungen können sich ändern. Prüfen Sie vor der Bestellung das aktuelle Angebot.</small></p>

## FAQ {#faq}

### Kann ich eine Website ohne Domainwechsel auf einen VPS umziehen? {#can-i-migrate-a-website-to-a-vps-without-changing-the-domain}

Ja. Bei einer Hosting-Migration können Domain und öffentliche URLs unverändert bleiben. Bauen und testen Sie zuerst das Ziel. Ändern Sie anschließend die DNS-Einträge, damit Zugriffe den neuen Server erreichen.

### Brauche ich beim Umzug einer Website auf einen VPS 301-Weiterleitungen? {#do-i-need-301-redirects-when-moving-a-website-to-a-vps}

Nicht, wenn die öffentlichen URLs unverändert bleiben. Weiterleitungen werden benötigt, wenn sich URLs tatsächlich ändern, etwa durch eine neue Domain, einen Protokoll-/Pfadwechsel oder eine neue Inhaltsstruktur.

### Wie reduziere ich die Ausfallzeit bei einer VPS-Migration? {#how-do-i-reduce-downtime-during-a-vps-migration}

Bereiten Sie das Ziel parallel vor, reduzieren Sie die relevante DNS-TTL rechtzeitig, testen Sie nicht öffentlich, kontrollieren Sie letzte Schreibvorgänge und synchronisieren Sie die Daten abschließend. Schalten Sie DNS erst nach der Abnahme um und halten Sie den alten Host während der DNS-Verteilung verfügbar.

### Sollte E-Mail ebenfalls auf den VPS umziehen? {#should-i-move-email-to-the-vps-too}

Nicht automatisch. E-Mail bei einem verwalteten Maildienst zu belassen, kann Migrations- und Zustellrisiken reduzieren. Zieht E-Mail um, planen Sie MX, SPF, DKIM, DMARC, Postfachdaten, gegebenenfalls Reverse DNS und Backups separat.

### Was sollte ich vor der DNS-Änderung testen? {#what-should-i-test-before-changing-dns}

Testen Sie repräsentative Seiten, Anmeldung, Formulare, Uploads, Suche, gegebenenfalls Checkout/Zahlungs-Callbacks, geplante Aufgaben, APIs/Webhooks, ausgehende E-Mail, HTTPS, Weiterleitungen und Anwendungs-/Serverprotokolle.

### Wie lange sollte ich das alte Hosting nach der Migration behalten? {#how-long-should-i-keep-the-old-hosting-after-migration}

Bis DNS-Zugriffe umgezogen sind, der neue Server stabil läuft, neue Schreibvorgänge geprüft wurden und der vereinbarte Rückfallzeitraum abgelaufen ist. Orientieren Sie sich an Logs, nicht an einer pauschalen Anzahl von Stunden oder Tagen.

### Kann ich WooCommerce ohne verlorene Bestellungen umziehen? {#can-i-migrate-woocommerce-without-losing-orders}

Ja, aber nicht mit einer einzigen alten Datenbankkopie. Kontrollieren Sie Schreibvorgänge während der Umschaltung und führen Sie eine zur Anwendung passende abschließende Synchronisierung durch. So werden Bestellungen und Bestandsänderungen nicht auf zwei gleichzeitig beschreibbare Datenbanken verteilt.

### Schadet ein Hosting-Wechsel der Suchmaschinenoptimierung? {#does-moving-hosting-hurt-seo}

Bei gleichbleibenden URLs sollten die Suchsignale erhalten bleiben, wenn das Ziel dieselben Inhalte, Statuscodes, kanonischen URLs und dieselbe Crawlbarkeit bietet. Überwachen Sie nach dem Umzug Search Console und Serverlogs. Bei einem Wechsel der Hosting-Infrastruktur kann sich die Crawling-Rate vorübergehend ändern.
