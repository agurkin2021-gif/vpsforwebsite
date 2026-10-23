---
title: "VPS für WordPress"
description: "VPS für WordPress: CPU und RAM anhand von PHP-Workern, Datenbanklast, Caching, Plugins und Hintergrundaufgaben dimensionieren und Verwaltung sowie Migration planen."
image: "images/home/vps-for-website-hero.webp"
slug: "vps-fuer-wordpress"
---

Ein VPS für WordPress ist sinnvoll, wenn WordPress mehr Kontrolle, Isolation oder Serverfunktionen benötigt, als Shared Hosting bietet. Die Dimensionierung sollte sich an **ungecachter PHP-Arbeit, Datenbankbedarf, Plugins, Hintergrundaufgaben, Speicherwachstum und den zusätzlich zu WordPress laufenden Diensten** orientieren, nicht an einer monatlichen Besucherzahl.

Für die übergreifende Serverentscheidung lesen Sie [VPS für Websites]({{< relref "_index.md" >}}).

[Kurzantwort](#quick-answer) · [Eignung prüfen](#wordpress-vps-fit-checker) · [PHP-Worker](#php-workers-and-ram) · [Caching](#wordpress-caching-layers) · [Datenbank](#database-demand) · [WP-Cron](#wp-cron-and-background-jobs) · [FAQ](#faq)

## Kurzantwort {#quick-answer}

Dies sind praktische Einstiegskonfigurationen der aktuellen VDSina-Standard-Tarife, keine Garantien für bestimmte Besucherzahlen.

| WordPress-Lastprofil | Praktischer Einstieg | Wichtigster zu prüfender Engpass |
|---|---:|---|
| Labor-/Testwebsite oder extrem schlankes gecachtes WordPress | **1 vCPU / 1 GB / 10 GB** | sehr wenig RAM- und Speicherreserve; kein Standardziel für den Produktivbetrieb |
| Kleine, gut gecachte WordPress-Website | **1 vCPU / 2 GB / 40 GB** | PHP-Worker, Datenbankspeicher, Plugin-/Hintergrundlast |
| Unternehmenswebsite mit WordPress | **2 vCPU / 4 GB / 80 GB** | ungecachte Parallelität, Datenbanklatenz, Cron/Plugins |
| Anspruchsvolleres dynamisches WordPress, große Datenbank oder mehrere aktive Websites | **4 vCPU / 8 GB / 160 GB** | anhaltende CPU-Last, PHP-Warteschlange, aktiver DB-Datenbestand, überlappende Aufgaben |

Aktuelle VDSina-Standard-Preise, erneut geprüft am 13. Oktober 2026:

- 1 vCPU / 1 GB / 10 GB / 1 TB monatlicher Datentransfer – **$0.07/Tag**;
- 1 vCPU / 2 GB / 40 GB / 32 TB – **$0.50/Tag**;
- 2 vCPU / 4 GB / 80 GB / 32 TB – **$0.67/Tag**;
- 4 vCPU / 8 GB / 160 GB / 32 TB – **$1.34/Tag**.

Ist die Website ein echter Shop mit dynamischem Warenkorb, Checkout, Kundenkonto, Bestellungen oder Lagerbestand, nutzen Sie [VPS für WooCommerce]({{< relref "vps-for-woocommerce.md" >}}), statt sie wie gewöhnliches gecachtes WordPress zu behandeln.

Für eine tiefergehende, stackübergreifende Ressourcenberechnung nutzen Sie [VPS für Websites dimensionieren]({{< relref "vps-sizing-for-website.md" >}}).

## WordPress-Anforderungen sind keine VPS-Dimensionierung {#wordpress-requirements-are-not-vps-sizing}

WordPress.org empfiehlt derzeit einen Host mit Unterstützung für:

- **PHP 8.3 oder neuer**;
- **MariaDB 10.11+ oder MySQL 8.0+**;
- **HTTPS**;
- Apache oder Nginx als empfohlene Webserver.

Diese Anforderungen beantworten **„Kann dieser Server WordPress ausführen?“** Sie beantworten nicht **„Wie groß muss der VPS für diese produktive Last sein?“**

Ein produktiver VPS benötigt außerdem RAM, CPU und Speicher für:

- Linux;
- Nginx/Apache;
- PHP-FPM-Worker;
- MySQL/MariaDB;
- OPcache;
- Seiten-/Objektcache, sofern genutzt;
- Control Panel;
- E-Mail bei lokalem Betrieb;
- Backups;
- Cronjobs;
- Schadsoftware-/Sicherheitsscans;
- Importe/Exporte;
- Monitoring;
- Betriebsreserve.

Verwenden Sie die WordPress-Softwareanforderungen nicht als Ressourcenempfehlung für den Produktivbetrieb.

## Eignung eines VPS für WordPress prüfen {#wordpress-vps-fit-checker}

Nutzen Sie diese Prüfung als Ausgangspunkt. Sie ersetzt keine tatsächlichen CPU-, RAM- und Datenbankmessungen.

<div class="rounded-2xl bg-light p-6 dark:bg-darkmode-light">
<form id="wordpress-vps-fit-checker-form">
  <div class="mb-6">
    <label for="wp-limits" class="form-label">Zeigt das aktuelle Hosting wiederholt Grenzen bei berechtigter Last oder fehlt eine Funktion?</label>
    <select id="wp-limits" class="form-input">
      <option value="no">Nein / nicht gemessen</option>
      <option value="some">Gelegentliche Engpässe</option>
      <option value="yes">Wiederholte Grenzen oder nur per VPS verfügbare Funktion nötig</option>
    </select>
  </div>
  <div class="mb-6">
    <label for="wp-type" class="form-label">WordPress-Lastprofil</label>
    <select id="wp-type" class="form-input">
      <option value="content">Überwiegend gecachte Inhalte / Präsentationswebsite / Blog</option>
      <option value="business">Unternehmens-CMS mit Formularen, Plugins und Admin-Aktivität</option>
      <option value="membership">Mitgliederbereich / angemeldete Nutzer / personalisierte Website</option>
      <option value="store">WooCommerce / transaktionsbasierter Shop</option>
    </select>
  </div>
  <div class="mb-6">
    <label for="wp-dynamic" class="form-label">Intensität von ungecachtem PHP, Administration und API</label>
    <select id="wp-dynamic" class="form-input">
      <option value="low">Gering</option>
      <option value="medium">Mittel</option>
      <option value="high">Hoch</option>
    </select>
  </div>
  <div class="mb-6">
    <label for="wp-jobs" class="form-label">Aufwendige Plugins, Importe, Scans, Backups oder Hintergrundaufgaben?</label>
    <select id="wp-jobs" class="form-input"><option value="no">Nein</option><option value="yes">Ja</option></select>
  </div>
  <div class="mb-6">
    <label for="wp-db" class="form-label">Datenbankgröße und -aktivität</label>
    <select id="wp-db" class="form-input">
      <option value="small">Klein / gering</option>
      <option value="medium">Mittel</option>
      <option value="large">Groß / viele aufwendige Abfragen</option>
    </select>
  </div>
  <div class="mb-6">
    <label for="wp-panel" class="form-label">Control Panel oder lokale E-Mail auf demselben VPS?</label>
    <select id="wp-panel" class="form-input"><option value="no">Nein</option><option value="yes">Ja</option></select>
  </div>
  <div class="mb-6">
    <label for="wp-sites" class="form-label">Wie viele aktive WordPress-Websites?</label>
    <select id="wp-sites" class="form-input"><option value="1">1</option><option value="few">2–5</option><option value="many">6+</option></select>
  </div>
  <button class="btn btn-primary" type="submit">Passenden WordPress-VPS abschätzen</button>
</form>
<p id="wordpress-vps-fit-result" class="mt-6 rounded border border-border p-4 dark:border-darkmode-border" role="status" aria-live="polite">Verwenden Sie möglichst echte Messwerte der Last.</p>
</div>

<script>
document.addEventListener("DOMContentLoaded", function () {
  var form = document.getElementById("wordpress-vps-fit-checker-form");
  if (!form) return;

  form.addEventListener("submit", function (event) {
    event.preventDefault();

    var limits = document.getElementById("wp-limits").value;
    var type = document.getElementById("wp-type").value;
    var dynamic = document.getElementById("wp-dynamic").value;
    var jobs = document.getElementById("wp-jobs").value === "yes";
    var db = document.getElementById("wp-db").value;
    var panel = document.getElementById("wp-panel").value === "yes";
    var sites = document.getElementById("wp-sites").value;

    var score = 0;
    if (type === "business") score += 2;
    if (type === "membership") score += 4;
    if (type === "store") score += 5;
    if (dynamic === "medium") score += 2;
    if (dynamic === "high") score += 4;
    if (jobs) score += 2;
    if (db === "medium") score += 1;
    if (db === "large") score += 3;
    if (panel) score += 1;
    if (sites === "few") score += 2;
    if (sites === "many") score += 4;

    var result;

    if (limits === "no" && type === "content" && dynamic === "low" && score <= 1) {
      result = "ZUERST BLEIBEN / OPTIMIEREN: Es gibt noch kein starkes Signal für einen VPS. Gutes Shared Hosting oder Managed WordPress Hosting kann einfacher sein, bis tatsächliche Grenzen oder eine benötigte Serverfunktion auftreten.";
    } else if (type === "store") {
      result = "WOOCOMMERCE-WEG: Planen Sie erst nach Messung der dynamischen Checkout-, Konto- und Bestelllast einen Einstieg bei etwa 4 GB RAM oder mehr. Nutzen Sie den eigenen Ratgeber VPS für WooCommerce; Shopzugriffe entsprechen nicht gewöhnlichen gecachten WordPress-Zugriffen.";
    } else if (score <= 2) {
      result = "SCHLANKER EINSTIEG MIT 2 GB: 1 vCPU / 2 GB / 40 GB können für eine kleine, gut gecachte WordPress-Website passen. Beobachten Sie PHP-Worker-Speicher, Datenbank-RAM sowie Plugins und Hintergrundaufgaben.";
    } else if (score <= 7) {
      result = "PRAKTISCHER EINSTIEG MIT 4 GB: 2 vCPU / 4 GB / 80 GB bieten mehr Reserve für eine Unternehmenswebsite mit WordPress, PHP-Worker, Datenbank, Cache und regelmäßige Hintergrundaufgaben.";
    } else {
      result = "8 GB ODER ARCHITEKTUR PRÜFEN: 4 vCPU / 8 GB / 160 GB sind ein stärkerer Ausgangspunkt für anspruchsvolleres dynamisches WordPress oder mehrere Websites. Dominiert eine Website oder Aufgabe die Ressourcen, erwägen Sie eine Trennung der Lasten statt nur eines größeren VPS.";
    }

    if (limits === "no" && type !== "store" && score > 1) {
      result += " Wenn das aktuelle Hosting die Website tatsächlich nicht begrenzt, optimieren und messen Sie vor einer Migration.";
    }

    document.getElementById("wordpress-vps-fit-result").textContent = result;
  });
});
</script>

## Wann WordPress tatsächlich einen VPS braucht {#when-wordpress-actually-needs-vps}

Ein VPS kann für eine WordPress-Website auch ohne riesige Zugriffszahlen gerechtfertigt sein.

Häufige Gründe:

- wiederholte CPU-, Speicher- oder Prozessgrenzen bei berechtigter Last;
- Bedarf an einer individuellen PHP-/Laufzeitkonfiguration;
- Bedarf an Redis/Memcached oder einem anderen serverseitigen Dienst;
- echter System-Cron statt besuchergesteuerter Zeitplanung;
- lange laufende Hintergrundaufgaben;
- individuelles Nginx-/Apache-Verhalten;
- mehrere Websites in einer gemeinsam kontrollierten Umgebung;
- stärkere Isolation von Lasten oder Konten;
- Anforderungen an serverweites Monitoring oder Firewall-Regeln.

Ist das einzige Symptom „Die Website ist langsam“, vergleichen Sie zuerst [VPS vs. Shared Hosting]({{< relref "vps-vs-shared-hosting.md" >}}) und prüfen Sie, ob WordPress selbst den Engpass verursacht.

## Wann WordPress keinen VPS braucht {#when-wordpress-does-not-need-vps}

Bleiben Sie bei gutem Shared Hosting oder Managed WordPress Hosting, wenn:

- die Website schlank und stabil ist;
- Caching funktioniert;
- die Ressourcenanzeigen des Hosts keine wiederholten Grenzen zeigen;
- weder individuelle Dienste noch Root-Zugriff nötig sind;
- das Team Linux nicht warten möchte;
- der Anbieter Backups, Sicherheit, Updates oder Staging bereits ausreichend gut abdeckt;
- der VPS vor allem einen einfachen Hostingdienst durch mehr Betriebsarbeit ersetzen würde.

Ein VPS ist nicht automatisch schneller. Ein schlecht dimensionierter oder unzureichend abgestimmter VPS kann WordPress schlechter betreiben als eine gute Managed-Plattform.

## PHP-Worker und RAM {#php-workers-and-ram}

Bei ungecachten Anfragen begrenzen PHP-FPM-Worker wesentlich die Parallelität.

Jeder aktive Worker belegt während der Bearbeitung einer Anfrage Speicher. Mehr Worker können mehr gleichzeitige dynamische Anfragen bearbeiten. Eine höhere Worker-Zahl ohne größeres RAM-Budget kann jedoch Folgendes verursachen:

- Auslagerung in Swap;
- Speicherdruck;
- OOM-Abbrüche;
- Speichermangel für die Datenbank;
- Serverinstabilität.

Ein praktisches Modell lautet:

**WordPress-RAM = Betriebssystem + Webserver + Datenbank + Cache + PHP-Worker + Panel/E-Mail/Aufgaben + Reserve**

Anschließend:

**PHP-Worker-Budget = sicher für PHP verfügbarer RAM / gemessener durchschnittlicher Worker-Speicher**

Konfigurieren Sie nicht die theoretisch maximale Worker-Zahl, wenn dadurch kein Speicher für MySQL/MariaDB, Cache oder Betriebssystem übrig bleibt.

Angemeldete Nutzer, wp-admin, REST-/API-Anfragen, Suche, Formulare, Vorschauen und personalisierte Seiten umgehen häufiger den vollständigen Seitencache und belegen PHP-Worker.

## Caching-Ebenen bei WordPress {#wordpress-caching-layers}

Caching ist keine einzelne Funktion.

| Ebene | Gespeicherte Inhalte | Hauptwirkung |
|---|---|---|
| **PHP OPcache** | kompilierter PHP-Bytecode | vermeidet erneutes Kompilieren von PHP-Skripten bei jeder Anfrage |
| **Seitencache** | fertig gerendertes HTML | lässt viele anonyme Seitenaufrufe ohne WordPress-/PHP-Verarbeitung ausliefern |
| **Persistenter Objektcache** | wiederverwendbare Objekte/Abfrageergebnisse | reduziert wiederholte Datenbank- und Anwendungsarbeit |
| **Browser-/CDN-Cache** | statische oder am Netzwerkrand auslieferbare Inhalte | reduziert wiederholten Datentransfer und Anfragen zum Ursprungsserver |

Die WordPress-eigene Optimierungsdokumentation empfiehlt Caching als wichtiges Leistungswerkzeug. Diese Ebenen lösen jedoch unterschiedliche Probleme.

Bezeichnen Sie Redis nicht als Seitencache. Redis dient häufig als Backend für einen persistenten Objektcache; vollständiges Seiten-Caching ist eine separate Ebene.

## Persistenter Objektcache und Redis {#persistent-object-cache-and-redis}

WordPress enthält eine Objektcache-API, doch der Standardcache ist **nicht über einzelne Anfragen hinweg persistent**.

Persistentes Objekt-Caching benötigt ein externes Backend/Drop-in wie Redis oder Memcached sowie die passende WordPress-Integration.

Das kann helfen, wenn die Website wiederholt aufwendige Datenbank- oder Objektoperationen ausführt, ist aber kein automatischer Beschleunigungsknopf.

Bevor Sie Redis hinzufügen:

- bestätigen Sie den Nutzen für die Website-/Datenbanklast;
- prüfen Sie, ob genügend RAM für PHP und Datenbank bleibt;
- überwachen Sie Trefferquote und Speicher;
- entscheiden Sie separat über Seiten-Caching.

Eine Website mit effizientem vollständigem Seiten-Caching und geringer Datenbanklast profitiert möglicherweise weniger von Redis als eine dynamische Mitgliederwebsite oder eine Website mit aufwendigen Abfragen.

## Datenbankbedarf {#database-demand}

Die WordPress-Leistung kann bereits durch die Datenbank begrenzt sein, bevor eine sichtbare CPU-Sättigung auftritt.

Prüfen Sie:

- langsame Abfragen;
- große Options-Tabellen oder automatisch geladene Daten;
- Plugin-Metadaten;
- Such-, Filter- und Berichtsabfragen;
- Lasten mit intensiver Nutzung von postmeta;
- den aktiven Datenbestand der Datenbank;
- gleichzeitige Schreibvorgänge;
- Importe/Exporte;
- Speicherlatenz.

Mehr CPU repariert keine problematische Abfrage. Mehr RAM kann helfen, wenn die Datenbank tatsächlich einen größeren aktiven Datenbestand vorhalten muss; es ersetzt jedoch keine Arbeit an Indizes, Abfragen oder Plugins.

Erst messen, dann skalieren.

## Plugins, Themes und Hintergrundaufgaben {#plugins-themes-and-background-jobs}

Ein Plugin benötigt nicht nur Festplattenspeicher.

Plugins und Themes können Folgendes hinzufügen:

- PHP-Arbeit;
- Datenbankabfragen;
- externe API-Aufrufe;
- geplante Aufgaben;
- Cache-Invalidierung;
- Admin-AJAX;
- Bildverarbeitung;
- Sicherheitsscans;
- Backups;
- Importe/Exporte;
- Analysen und Protokollierung.

Aufwendige Aufgaben können mit echten Besucherzugriffen zusammenfallen.

Planen Sie Backups, Scans, Importe und Bildverarbeitung möglichst außerhalb der Spitzenzeiten. Verursacht ein einzelnes Plugin oder eine Aufgabe die Lastspitze, beheben oder verlegen Sie diese zuerst, bevor Sie den VPS für zu klein halten.

## WP-Cron und Hintergrundaufgaben {#wp-cron-and-background-jobs}

WP-Cron wird durch WordPress-Anfragen ausgelöst und läuft nicht wie ein System-Scheduler kontinuierlich.

Für gewöhnliche Websites kann das ausreichen. Für zeitkritische oder stark ausgelastete Anwendungen beschreibt die WordPress-Entwicklerdokumentation die Nutzung des Betriebssystem-Schedulers, um WordPress-Cron in kontrollierten Intervallen aufzurufen.

Wenn Sie auf einen System-Scheduler wechseln:

- richten Sie zuerst den Ersatz-Auslöser ein;
- prüfen Sie seine Funktion;
- deaktivieren Sie erst danach das normale besuchergesteuerte WP-Cron-Verhalten, sofern das vorgesehen ist;
- protokollieren und überwachen Sie fehlgeschlagene Aufgaben.

Deaktivieren Sie WP-Cron nicht ohne einen anderen Scheduler.

## Speicher, Medien, Staging und Backups {#storage-media-staging-and-backups}

Die Speicherplanung muss mehr als den WordPress-Kern berücksichtigen.

Planen Sie Platz für:

- Uploads/Medien;
- Datenbank;
- Plugins/Themes;
- Protokolle;
- Cache-Dateien;
- temporäre Update-Dateien;
- temporären Speicher für Bildverarbeitung;
- Staging-Kopie;
- Backup-Archive vor ihrer Übertragung auf einen anderen Server;
- erwartetes Wachstum.

Eine Website, die heute 20 GB belegt, kann beim Klonen, Wiederherstellen, Aktualisieren eines Plugins oder Komprimieren eines Backups deutlich mehr temporären Speicher benötigen.

Bewahren Sie das einzige Backup nicht auf dem VPS auf.

## Manuell, Control Panel oder FASTPANEL? {#manual-control-panel-or-fastpanel}

WordPress kann problemlos ohne cPanel oder ein anderes Panel laufen.

### Manuell verwaltetes Linux {#manual-linux}

Gut geeignet, wenn Sie Folgendes möchten:

- einen minimalen Stack;
- Administration per SSH;
- individuelle Nginx-/Apache-/PHP-/Datenbankkonfiguration;
- automatisierte oder Git-basierte Bereitstellung.

Für den manuellen Bereitstellungsweg nutzen Sie [Website auf einem VPS hosten]({{< relref "how-to-host-a-website-on-vps.md" >}}).

### Allgemeines Control Panel {#generic-control-panel}

Sinnvoll, wenn die browsergestützte Verwaltung von Domains, SSL, PHP, Datenbanken, Benutzern, E-Mail oder Backups genügend Routinearbeit abnimmt.

Lesen Sie [VPS mit Control Panel]({{< relref "vps-with-control-panel.md" >}}).

### FASTPANEL {#fastpanel}

Der offizielle FASTPANEL-Ablauf unterstützt die Erstellung von WordPress-Websites. VDSina führt FASTPANEL auf Ubuntu 22 derzeit als vorkonfigurierte Panel-Option.

Für Einrichtung und Dimensionierung dieses Produkts nutzen Sie [VPS-Hosting mit FASTPANEL]({{< relref "fastpanel-vps-hosting.md" >}}).

Ein Control Panel vereinfacht die Administration, macht den VPS aber nicht zu einem Managed VPS.

## Managed oder selbst verwalteter WordPress-VPS {#managed-vs-self-managed-wordpress-vps}

Bei einem selbst verwalteten VPS muss jemand Folgendes verantworten:

- Betriebssystem-/Paket-Updates;
- SSH/Firewall;
- PHP-/Webserver-Updates;
- Datenbankadministration;
- WordPress-/Plugin-/Theme-Updates;
- Backups und Wiederherstellungstests;
- Monitoring;
- Störungen.

Wenn niemand diese Aufgaben übernimmt, wählen Sie betreute Administration, statt anzunehmen, WordPress oder ein Control Panel werde den Server verwalten.

Lesen Sie [Managed VPS vs. Unmanaged VPS]({{< relref "managed-vs-unmanaged-vps.md" >}}).

## WooCommerce hat ein anderes WordPress-Lastprofil {#woocommerce-is-a-different-wordpress-workload}

WooCommerce nutzt den WordPress-Stack, verhält sich unter echten Shopzugriffen jedoch anders.

Warenkorb, Checkout, Kundenkonto, Bestellungen, Lagerbestand und viele geplante Aktionen sind dynamisch und lassen sich nicht wie anonyme gecachte Blogseiten behandeln.

Wenn Shoptransaktionen wichtig sind, nutzen Sie [VPS für WooCommerce]({{< relref "vps-for-woocommerce.md" >}}) für das passende Dimensionierungs- und Betriebsmodell.

## Mehrere WordPress-Websites {#multiple-wordpress-sites}

Mehrere WordPress-Websites teilen sich:

- CPU;
- RAM;
- Datenbankdienst;
- PHP-Worker/-Pools;
- Speicher;
- Zeitfenster für Cron- und Hintergrundaufgaben;
- Backup-Zeit;
- einen gemeinsamen Ausfallbereich.

Zehn ruhige gecachte Websites können weniger Last erzeugen als eine einzige stark genutzte dynamische Mitgliederwebsite.

Nutzen Sie gegebenenfalls separate Benutzer und Datenbankzugänge und dimensionieren Sie anhand der **gemeinsamen Spitzenlast**, nicht nach der Domainanzahl.

Lesen Sie [VPS für mehrere Websites]({{< relref "vps-for-multiple-websites.md" >}}).

## Wann ein WordPress-VPS ein Upgrade braucht {#wordpress-vps-upgrade-triggers}

Führen Sie ein Upgrade erst durch, nachdem Sie einen tatsächlichen Engpass gemessen haben.

Deutliche Signale:

- anhaltender RAM-Druck, Swap-Nutzung oder OOM-Ereignisse;
- wiederholte Warteschlangen oder Sättigung der PHP-Worker;
- anhaltende CPU-Sättigung nach Cache-, Abfrage- und Plugin-Optimierung;
- Datenbanklatenz durch einen tatsächlich zu großen aktiven Datenbestand;
- Speicherwachstum über eine sichere Betriebsreserve hinaus;
- Hintergrundaufgaben, die wiederholt mit Besucherzugriffen kollidieren;
- mehrere aktive Websites, die die gemeinsamen Ressourcen aufbrauchen.

Ist die Website langsam, während diese Signale unauffällig bleiben, ist ein größerer VPS möglicherweise nicht die Lösung.

## Checkliste für den Start eines WordPress-VPS {#wordpress-vps-launch-checklist}

| Prüfung | Erfüllte Bedingung |
|---|---|
| WordPress-Laufzeit | unterstützte PHP-/DB-Versionen und HTTPS |
| PHP | FPM/Laufzeit konfiguriert; Worker-Zahl passt zum RAM |
| Datenbank | eigene Zugangsdaten; Risiken langsamer Abfragen und des aktiven Datenbestands bekannt |
| Cache | Seiten-, Objekt- und OPcache-Ebenen bewusst gewählt |
| Cron | WP-Cron/System-Zeitplan funktioniert und wird überwacht |
| Dateien | korrekte Eigentümer; Uploads ohne `777` beschreibbar |
| HTTPS | vertrauenswürdiges Zertifikat und Erneuerungsweg |
| Backups | Dateien und DB enthalten; externe Kopie und Wiederherstellungsweg |
| Updates | Betriebssystem, WordPress, Plugins und Themes haben einen Verantwortlichen |
| Monitoring | externe Erreichbarkeit sowie Einblick in CPU/RAM/Festplatte/Protokolle |
| Neustart | Web/PHP/DB/Cron starten automatisch wieder |
| Kapazität | unter repräsentativer ungecachter/dynamischer Last gemessen |

Für eine bestehende produktive Website nutzen Sie [Website auf einen VPS umziehen]({{< relref "website-migration-to-vps.md" >}}) für Umschaltung, letzte Schreibvorgänge, DNS und Rollback.

## Aktuelle Beispiele für WordPress-VPS {#current-wordpress-vps-examples}

Diese VDSina-Standard-Konfigurationen sind aktuelle Beispiele, keine Garantien für WordPress-Zugriffszahlen.

| VPS | Geeigneter Einstieg | Erneut prüfen bei |
|---|---|---|
| 1 vCPU / 1 GB / 10 GB – $0.07/Tag | Labor/Test oder extrem schlankes gecachtes WordPress | produktiver DB, mehreren PHP-Workern und Panel/E-Mail |
| 1 vCPU / 2 GB / 40 GB – $0.50/Tag | schlanke kleine WordPress-Website | aufwendigen Plugins, mehreren aktiven Websites, anhaltender dynamischer Last |
| 2 vCPU / 4 GB / 80 GB – $0.67/Tag | praktische Basis für eine Unternehmenswebsite mit WordPress | anspruchsvollem Mitgliederbereich/WooCommerce, großer DB, überlappenden Aufgaben |
| 4 vCPU / 8 GB / 160 GB – $1.34/Tag | anspruchsvolleres dynamisches WordPress / größere DB / mehrere Websites | Bedarf an unabhängiger Skalierung oder stärkerer Isolation |

Die aktuelle Standard-Seite von VDSina führt WordPress in den sichtbaren Vorlagen- und Anwendungsgruppen nicht als eigene vorinstallierte Anwendung auf. Nutzen Sie ein reines Betriebssystem mit manueller Einrichtung oder einen aktuell kompatiblen Control-Panel-Weg, statt ein WordPress-Image mit einem Klick vorauszusetzen.

<p>
  <a class="btn btn-primary" href="https://www.vdsina.com/?partner=ni8gzrvz75" target="_blank" rel="sponsored nofollow noopener">Aktuelle WordPress-VPS-Optionen prüfen</a>
</p>
<p><small>Offenlegung: Der Herausgeber steht in einer beruflichen Beziehung zu VDSina. Diese Website kann eine Provision erhalten, wenn Sie über diesen Partnerlink bestellen. Prüfen Sie vor der Bestellung die aktuellen VPS-Preise sowie die Verfügbarkeit von Vorlagen und Panels.</small></p>

## Technische Referenzen {#technical-references}

- WordPress.org – aktuelle Anforderungen
- WordPress Developer Handbook – Caching
- WordPress Developer – Objektcache
- WordPress Developer – System-Scheduler und WP-Cron
- VDSina Standard VPS

## FAQ {#faq}

### Wie viel RAM braucht WordPress auf einem VPS? {#how-much-ram-does-wordpress-need-on-a-vps}

Der WordPress-Kern legt keinen RAM-Bedarf für einen produktiven VPS fest. RAM muss Linux, Webserver, PHP-Worker, Datenbank, Caches, Panel/E-Mail/Hintergrundaufgaben und Reserve abdecken. Eine schlanke Website kann mit 2 GB auskommen; 4 GB sind eine solidere praktische Basis für eine Unternehmenswebsite.

### Reicht 1 GB RAM für einen WordPress-VPS? {#is-1-gb-ram-enough-for-wordpress-vps}

Eine sehr schlanke WordPress- oder Testinstallation kann damit laufen, es bleibt aber wenig Reserve für Datenbank, PHP-Worker und Hintergrundarbeit. Das sollte nicht als normale Empfehlung für den Produktivbetrieb gelten.

### Reichen 2 GB RAM für WordPress? {#is-2-gb-ram-enough-for-wordpress}

Für eine kleine, gut gecachte Website mit schlankem Stack kann das reichen. Überwachen Sie PHP-Worker-Speicher, Datenbank-RAM, Plugins und Hintergrundaufgaben.

### Reichen 4 GB RAM für WordPress? {#is-4-gb-ram-enough-for-wordpress}

Für viele Unternehmenswebsites mit WordPress sind 4 GB ein praktischer Einstieg. Aufwendige Plugins, Mitgliederzugriffe, WooCommerce, große Datenbanken, Importe oder mehrere aktive Websites können mehr benötigen.

### Wie viele Besucher kann ein WordPress-VPS verarbeiten? {#how-many-visitors-can-a-wordpress-vps-handle}

Es gibt keine verlässliche allgemeingültige Besucherzahl. Cache-Trefferquote, ungecachte Parallelität, PHP-Anfragedauer, Plugin-Aufwand, Datenbankarbeit und Hintergrundaufgaben bestimmen die Kapazität.

### Brauche ich Redis für WordPress auf einem VPS? {#do-i-need-redis-for-wordpress-on-vps}

Nein. Redis kann persistentes Objekt-Caching bereitstellen, wenn das Lastprofil von wiederholtem Objekt-/Datenbank-Caching profitiert. Es ist aber nicht für jede WordPress-Website nötig und ersetzt kein vollständiges Seiten-Caching.

### Sollte ich Nginx oder Apache für einen WordPress-VPS nutzen? {#should-i-use-nginx-or-apache-for-wordpress-vps}

Beide sind geeignet. WordPress.org empfiehlt Apache oder Nginx als robuste Optionen. Nutzen Sie den Stack, den Ihre Anwendung und Ihr Administrator zuverlässig betreiben können.

### Sollte ich WP-Cron durch System-Cron ersetzen? {#should-i-replace-wp-cron-with-system-cron}

Nur wenn ein kontrollierter Scheduler für die Last sinnvoll ist und Sie einen funktionierenden Ersatz einrichten. Deaktivieren Sie WP-Cron nicht ohne einen anderen Auslöser.

### Braucht ein WordPress-VPS ein Control Panel? {#does-wordpress-vps-need-a-control-panel}

Nein. WordPress kann auf einem manuell verwalteten Linux-VPS laufen. Ein Panel ist optional und sollte wegen der einfacheren Administration gewählt werden, nicht als Leistungsvoraussetzung.

### Ist WordPress bei VDSina vorinstalliert? {#does-vdsina-include-wordpress-preinstalled}

Die aktuelle Standard-VPS-Seite führt WordPress in den sichtbaren Vorlagen- und Anwendungsgruppen nicht als eigene vorinstallierte Anwendung auf. Prüfen Sie die aktuelle Bestellmaske, bevor Sie die Verfügbarkeit einer Vorlage voraussetzen.
