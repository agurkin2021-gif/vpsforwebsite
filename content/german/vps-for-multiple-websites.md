---
title: "VPS für mehrere Websites"
description: "VPS für mehrere Websites: gemeinsame Lastspitzen berechnen, Benutzer und Datenbanken trennen und entscheiden, wann Websites oder Dienste einen eigenen Server brauchen."
image: "images/home/vps-for-website-hero.webp"
slug: "vps-fuer-mehrere-websites"
---

Ein VPS für mehrere Websites eignet sich, wenn die Websites einen gemeinsamen Ressourcenpool, ein Verwaltungsmodell und dasselbe Ausfallrisiko sicher teilen können. Entscheidend ist nicht die Zahl der Domains, sondern die **gleichzeitige Spitzenlast aller Websites bei CPU, RAM, PHP-/Anwendungs-Workern, Datenbankzugriffen, Speicher, Hintergrundaufgaben und Backups**.

Die übergeordnete Kaufentscheidung behandelt [VPS für Websites]({{< relref "_index.md" >}}).

[Schnelle Orientierung](#quick-answer) · [Architektur prüfen](#multi-site-vps-architecture-checker) · [Kapazität](#count-workload-not-domains) · [Isolation](#isolate-each-site-deliberately) · [Eine IP-Adresse](#one-ip-can-host-many-websites) · [Kriterien für eine Aufteilung](#when-to-split-sites-or-workloads) · [FAQ](#faq)

## Schnelle Orientierung {#quick-answer}

Diese Einstiegskonfigurationen beziehen sich auf die aktuellen VDSina-Standardtarife. Sie garantieren keine feste Anzahl von Websites.

| Website-Bestand | Praktischer Einstieg | Was Sie prüfen sollten |
|---|---:|---|
| Einige kleine statische oder gecachte Websites | **1 vCPU / 2 GB / 40 GB** | Gemeinsamer RAM- und Speicherbedarf, Backups und gelegentliche dynamische Anfragen |
| Mehrere kleinere WordPress- oder Unternehmenswebsites | **2 vCPU / 4 GB / 80 GB** | PHP-Pools, Datenbankspeicher, gleichzeitige Cronjobs und Backup-Zeitfenster |
| Anspruchsvollerer gemischter Bestand oder mehr dynamische Websites | **4 vCPU / 8 GB / 160 GB** | Gleichzeitige Lastspitzen, Datenbankkonflikte, ressourcenintensive Einzelwebsites und Speicherwachstum |
| Kritische, schreibintensive oder unabhängig skalierende Anwendungen | **Architektur aufteilen** | Fehlerisolation, unabhängige Skalierung und inkompatible Softwareumgebungen |

Aktuelle VDSina-Standardpreise, erneut geprüft am 13. Oktober 2026:

- 1 vCPU / 1 GB / 10 GB / 1 TB monatliches Transfervolumen — **$0.07/Tag**;
- 1 vCPU / 2 GB / 40 GB / 32 TB — **$0.50/Tag**;
- 2 vCPU / 4 GB / 80 GB / 32 TB — **$0.67/Tag**;
- 4 vCPU / 8 GB / 160 GB / 32 TB — **$1.34/Tag**.

Lesen Sie diese Stufen nicht als „2 GB = X Websites“ oder „8 GB = Y Websites“. Zehn gecachte Unternehmenspräsentationen können weniger Last erzeugen als ein gut besuchter WooCommerce-Shop.

Für die Berechnung des Ressourcenbedarfs verschiedener Softwareumgebungen nutzen Sie [VPS für Websites dimensionieren]({{< relref "vps-sizing-for-website.md" >}}).

## VPS-Architektur für mehrere Websites prüfen {#multi-site-vps-architecture-checker}

Mit dieser Prüfung entscheiden Sie, ob ein gemeinsamer VPS und sein gemeinsames Ausfallrisiko noch zu Ihrem Website-Bestand passen.

<div class="rounded-2xl bg-light p-6 dark:bg-darkmode-light">
<form id="multi-site-architecture-checker">
  <div class="mb-6">
    <label for="ms-count" class="form-label">Wie viele aktive Websites betreiben Sie?</label>
    <select id="ms-count" class="form-input">
      <option value="few">2–5</option>
      <option value="medium">6–15</option>
      <option value="many">16+</option>
    </select>
  </div>
  <div class="mb-6">
    <label for="ms-heavy" class="form-label">Anspruchsvollste Anwendung im Bestand</label>
    <select id="ms-heavy" class="form-input">
      <option value="light">Statische / gecachte Firmenwebsite / kleiner Blog</option>
      <option value="wordpress">Dynamisches WordPress / Unternehmens-CMS</option>
      <option value="store">WooCommerce / Transaktionen / Mitgliederbereich</option>
      <option value="app">Individuelle Anwendung / Dienst mit vielen Workern</option>
    </select>
  </div>
  <div class="mb-6">
    <label for="ms-clients" class="form-label">Websites voneinander unabhängiger Kunden?</label>
    <select id="ms-clients" class="form-input"><option value="no">Nein</option><option value="yes">Ja</option></select>
  </div>
  <div class="mb-6">
    <label for="ms-critical" class="form-label">Gibt es eine Website, deren Ausfall geschäftskritisch wäre?</label>
    <select id="ms-critical" class="form-input"><option value="no">Nein</option><option value="yes">Ja</option></select>
  </div>
  <div class="mb-6">
    <label for="ms-mixed" class="form-label">Unterschiedliche Laufzeitumgebungen oder unvereinbare Wartungs- bzw. Sicherheitsanforderungen?</label>
    <select id="ms-mixed" class="form-input"><option value="no">Nein</option><option value="yes">Ja</option></select>
  </div>
  <div class="mb-6">
    <label for="ms-peaks" class="form-label">Überschneiden sich Lastspitzen, Importe, Backups oder Cronjobs häufig?</label>
    <select id="ms-peaks" class="form-input"><option value="no">Selten</option><option value="yes">Ja</option></select>
  </div>
  <div class="mb-6">
    <label for="ms-panel" class="form-label">Verwaltungsmodell</label>
    <select id="ms-panel" class="form-input">
      <option value="panel">Hosting-Control-Panel / Oberfläche für mehrere Benutzer</option>
      <option value="manual">Manuell per SSH / Nginx oder Apache</option>
      <option value="containers">Container / Anwendungsisolation</option>
    </select>
  </div>
  <button class="btn btn-primary" type="submit">Architektur prüfen</button>
</form>
<p id="multi-site-architecture-result" class="mt-6 rounded border border-border p-4 dark:border-darkmode-border" role="status" aria-live="polite">Wählen Sie die Merkmale aus, die tatsächlich auf Ihren Website-Bestand zutreffen.</p>
</div>

<script>
document.addEventListener("DOMContentLoaded", function () {
  var form = document.getElementById("multi-site-architecture-checker");
  if (!form) return;

  form.addEventListener("submit", function (event) {
    event.preventDefault();

    function val(id) { return document.getElementById(id).value; }

    var count = val("ms-count");
    var heavy = val("ms-heavy");
    var clients = val("ms-clients") === "yes";
    var critical = val("ms-critical") === "yes";
    var mixed = val("ms-mixed") === "yes";
    var peaks = val("ms-peaks") === "yes";
    var panel = val("ms-panel");

    var score = 0;
    if (count === "medium") score += 2;
    if (count === "many") score += 4;
    if (heavy === "wordpress") score += 2;
    if (heavy === "store") score += 4;
    if (heavy === "app") score += 4;
    if (clients) score += 2;
    if (mixed) score += 3;
    if (peaks) score += 2;

    var result;

    if (critical) {
      result = "KRITISCHE WEBSITE TRENNEN: Eine geschäftskritische Anwendung sollte das Ausfallrisiko nicht mit unabhängigen oder weniger wichtigen Websites teilen, sofern das Unternehmen diese möglichen Auswirkungen nicht ausdrücklich akzeptiert.";
    } else if (mixed || score >= 9) {
      result = "DIENSTE TRENNEN / ARCHITEKTUR PRÜFEN: Unterschiedliche Softwareumgebungen oder eine hohe Gesamtlast sprechen dafür, die dominante Website, Datenbank, Worker oder Kundengruppen zu trennen, statt nur einen einzelnen VPS zu vergrößern.";
    } else if (clients || score >= 5) {
      result = "EIN VPS MIT STÄRKERER ISOLATION: Ein gemeinsamer Server kann weiterhin passen. Verwenden Sie jedoch getrennte Benutzer, Webverzeichnisse, PHP-/Anwendungsprozesse, Datenbankzugänge, Protokolle und Wiederherstellungswege. Überwachen Sie die Auswirkungen jeder Website.";
    } else {
      result = "EIN VPS FÜR EINEN KLEINEN BESTAND: Ein VPS ist eine sinnvolle Ausgangsarchitektur. Halten Sie die Websites sauber getrennt, planen Sie Reserven ein und überwachen Sie die gemeinsame Spitzenlast statt nur die Anzahl der Domains.";
    }

    if (panel === "panel") {
      result += " Prüfen Sie, ob das Panel das benötigte Modell zur Benutzer- und Kontentrennung bietet.";
    } else if (panel === "manual") {
      result += " Richten Sie die Isolation ausdrücklich über getrennte Systembenutzer, Serverblöcke bzw. virtuelle Hosts, PHP-Pools oder Anwendungsdienste, Datenbankzugänge und Protokolle ein.";
    } else {
      result += " Container können Prozesse und Abhängigkeiten besser isolieren, erhöhen aber die Komplexität von Orchestrierung, Backups und Monitoring. Setzen Sie sie ein, wenn die Anwendung davon profitiert, nicht pauschal.";
    }

    document.getElementById("multi-site-architecture-result").textContent = result;
  });
});
</script>

## Arbeitslast statt Domains zählen {#count-workload-not-domains}

Auf die Frage „Wie viele Websites kann ein VPS hosten?“ gibt es keine verlässliche pauschale Antwort.

Ein brauchbares Kapazitätsmodell lautet:

**Gesamtlast mehrerer Websites = gemeinsamer Normalbetrieb + überlagerte dynamische Lastspitzen + Datenbanken + Cronjobs/Worker + Backups/Importe + Panel/E-Mail/Monitoring + Reserve**

Beispiele:

- Zehn statische oder konsequent gecachte Websites benötigen möglicherweise sehr wenig PHP- und Datenbankkapazität.
- Drei WordPress-Unternehmenswebsites können deutlich mehr RAM brauchen, weil jede PHP-Worker und Datenbankarbeit mitbringt.
- Ein einzelner WooCommerce-Shop kann den gesamten Server während des Checkouts oder einer Verkaufsaktion auslasten.
- Ein einzelner Bildimport, ein Backup oder ein Sicherheitsscan kann vorübergehend mehr CPU und I/O beanspruchen als mehrere ruhige Websites zusammen.

Bemessen Sie die anspruchsvollste **gleichzeitig auftretende** Last, nicht die Anzahl der Domains im Control Panel.

## Wie viele Websites kann ein VPS hosten? {#how-many-websites-can-one-vps-host}

Nutzen Sie die Website-Anzahl nur zur Bestandsaufnahme.

Die Kapazität hängt ab von:

- der Cache-Trefferrate;
- gleichzeitig eintreffenden ungecachten Anfragen;
- dem Speicherbedarf der PHP-/Anwendungs-Worker;
- der Bearbeitungsdauer von Anfragen;
- dem aktiven Datenbestand der Datenbank;
- der Schreibintensität;
- geplanten Aufgaben und Hintergrundjobs;
- Bot-Traffic;
- dem Wachstum von Dateien und Medien;
- Backup-Zeitfenstern;
- dem Zusatzbedarf von Panel und E-Mail;
- der eingeplanten Reserve.

Wenn Sie die größten Ressourcenverbraucher nicht benennen können, ist jede Schätzung nach dem Muster „N Websites“ wenig belastbar.

WordPress-spezifische Anforderungen behandelt [VPS für WordPress]({{< relref "vps-for-wordpress.md" >}}). Einen transaktionsorientierten Shop sollten Sie gesondert betrachten; siehe [VPS für WooCommerce]({{< relref "vps-for-woocommerce.md" >}}).

## Eine IP-Adresse kann viele Websites bedienen {#one-ip-can-host-many-websites}

Übliche moderne Websites benötigen keine eigene öffentliche IP-Adresse pro Domain.

Beim namensbasierten virtuellen Hosting:

1. Verweisen die DNS-Einträge mehrerer Domains auf dieselbe VPS-IP.
2. Übermittelt der Browser den angeforderten Hostnamen.
3. Ordnet Nginx oder Apache diesen Hostnamen dem passenden Serverblock bzw. virtuellen Host zu.
4. Verwendet TLS die Erweiterung SNI, damit der Server für jeden Hostnamen das passende Zertifikat ausliefern kann.

Deshalb können sich viele voneinander unabhängige HTTPS-Websites die Ports 80/443 einer IP-Adresse teilen.

Eine zusätzliche IP kann bei besonderen Netzwerkrichtlinien, Altsystemen, E-Mail-Reputation oder Diensten außerhalb des Webhostings sinnvoll sein. Für jede einzelne Website ist sie üblicherweise nicht erforderlich.

## Jede Website gezielt isolieren {#isolate-each-site-deliberately}

Unterschiedliche Ordner schaffen Ordnung, aber noch keine starke Isolation.

Für voneinander unabhängige Websites oder Kundenprojekte sollten Sie möglichst getrennte Bereiche einrichten:

| Trennung | Warum sie wichtig ist |
|---|---|
| **System- oder Panel-Benutzer** | Verringert den gegenseitigen Zugriff auf Dateien und Zugangsdaten unabhängiger Websites |
| **Webverzeichnis (Document Root)** | Trennt Anwendungsdateien und Bereitstellungspfade |
| **PHP-FPM-Pool / Anwendungsprozess** | Ermöglicht eigene Benutzer- und Prozesseinstellungen pro Website |
| **Datenbank und Datenbankbenutzer** | Begrenzt Zugriffsrechte sowie den Umfang von Sicherung und Wiederherstellung |
| **Protokolle** | Erleichtert die Fehlersuche und Zuordnung von Vorfällen |
| **Geheimnisse und Umgebungsdateien** | Verhindert, dass eine Anwendung die Zugangsdaten einer anderen liest |
| **Backup-Satz** | Ermöglicht die Wiederherstellung einer Website, ohne den gesamten Bestand zurückzusetzen |

Ein häufiger Fehler ist, alle PHP-Websites unter demselben Unix-Benutzer mit gegenseitig lesbaren Konfigurationsdateien auszuführen. Ein kompromittiertes Plugin kann dann auch die anderen Websites gefährden.

Die Sicherheitsempfehlungen von FASTPANEL sehen getrennte FASTPANEL-Benutzer für unterschiedliche Websites vor. Für die Wahl einer Hosting-Oberfläche lesen Sie [VPS mit Control Panel]({{< relref "vps-with-control-panel.md" >}}). Den konkreten FASTPANEL-Ablauf beschreibt [VPS-Hosting mit FASTPANEL]({{< relref "fastpanel-vps-hosting.md" >}}).

## PHP-Pools, Anwendungsdienste und Datenbankzugänge trennen {#separate-php-pools-app-services-and-database-credentials}

Getrennte PHP-FPM-Pools helfen bei PHP-Websites, folgende Einstellungen voneinander abzugrenzen:

- Unix-Benutzer und -Gruppe;
- Worker-Limits;
- PHP-Konfiguration;
- Protokolle;
- Sockets;
- Ressourcenverhalten.

Für Node.js-, Python- und individuelle Anwendungen verwenden Sie getrennte Anwendungsbenutzer und Dienste sowie lokale Ports oder Sockets.

Für Datenbanken gilt:

- Verwenden Sie getrennte Datenbanken.
- Verwenden Sie getrennte Zugangsdaten.
- Vergeben Sie nur die Berechtigungen, die die jeweilige Anwendung benötigt.
- Geben Sie nicht allen Websites denselben Root- oder Administrationszugang zur Datenbank.

Damit entsteht keine vollständige, harte Mandantentrennung. Die Begrenzung von Schäden und die Fehlersuche werden jedoch erheblich verbessert.

## Unterschiedliche Anwendungen brauchen eigene Ressourcenbudgets {#mixed-workloads-need-different-budgets}

Bemessen Sie einen gemischten Website-Bestand nicht so, als wären alle Websites gleich.

### Statische oder gecachte Websites {#static--cached-sites}

Beanspruchen meist wenig Anwendungs-CPU und Datenbankressourcen.

### WordPress {#wordpress}

Benötigt Ressourcen für PHP-Worker, Datenbank, Cache und Cronjobs.

### WooCommerce, Mitgliederbereiche und Transaktions-Websites {#woocommerce--membership--transactional-sites}

Brauchen mehr Reserven für dynamische PHP- und Datenbankarbeit sowie eine sorgfältige Planung der Hintergrundaufgaben.

### Individuelle Anwendungen {#custom-apps}

Können dauerhaft laufende Prozesse, Warteschlangen, Container, verschiedene Laufzeitumgebungen oder eigene Ports benötigen.

Die anspruchsvollste Website entscheidet oft darüber, ob der gesamte VPS größer werden muss oder ob diese Website besser auf einen eigenen Server umzieht.

## Auch eigene Websites können sich gegenseitig ausbremsen {#your-own-sites-can-become-noisy-neighbors}

Ein VPS verringert die Abhängigkeit von fremden Shared-Hosting-Kunden. Wenn Sie mehrere Websites zusammenlegen, entstehen jedoch **interne Ressourcenkonflikte zwischen Ihren eigenen Projekten**.

Eine einzelne Website kann übermäßig viele Ressourcen beanspruchen durch:

- eine Traffic-Spitze;
- ein fehlerhaftes Plugin oder eine ungünstige Abfrage;
- einen Bot-Angriff;
- Bildverarbeitung;
- einen Import oder Export;
- einen Sicherheitsscan;
- Backup-Komprimierung;
- einen außer Kontrolle geratenen Cronjob;
- stark wachsende Protokolldateien;
- Datenbanksperren oder hohe I/O-Last.

Beobachten Sie den Ressourcenverbrauch während dieser Ereignisse, nicht nur im Leerlauf des Servers.

Wenn Ihre Softwareumgebung es unterstützt, können Worker- oder Prozesslimits pro Website sowie Container- oder cgroup-Limits verhindern, dass eine Anwendung sämtliche Ressourcen verbraucht. Gehen Sie aber nicht davon aus, dass ein Control Panel automatisch feste CPU- und RAM-Quoten erzwingt, sofern dies nicht dokumentiert ist.

## Gleichzeitige Spitzen sind wichtiger als die Durchschnittslast {#combined-peaks-matter-more-than-average-usage}

Server mit mehreren Websites geraten an ihre Grenzen, wenn unabhängige Lastspitzen zusammenfallen.

Ein Beispiel:

- Website A erhält nach einer Kampagne besonders viele Anfragen.
- Website B führt einen Datenbankimport aus.
- Website C beginnt mit einem vollständigen Backup.
- Website D startet einen Malware-Scan.
- Das Control Panel rotiert die Protokolle.
- Der Datenbankpuffer belegt bereits viel Speicher.

Einzeln betrachtet kann jede Website klein wirken. Gemeinsam können sie CPU, RAM oder I/O vollständig auslasten.

Planen Sie Wartung und Hintergrundaufgaben für den gesamten Website-Bestand, nicht für jedes Projekt unabhängig voneinander.

## Manuell, mit Control Panel oder mit Containern? {#manual-control-panel-or-containers}

### Serverblöcke und virtuelle Hosts manuell verwalten {#manual-server-blocks--virtual-hosts}

Diese Variante passt, wenn:

- eine fachkundige Person den Server betreut;
- die Zahl der Websites überschaubar ist;
- die Softwareumgebungen ähnlich sind;
- Automatisierung und Skripte für eine einheitliche Konfiguration sorgen.

Den allgemeinen Bereitstellungsablauf beschreibt [Website auf einem VPS hosten]({{< relref "how-to-host-a-website-on-vps.md" >}}).

### Hosting-Control-Panel {#hosting-control-panel}

Ein Panel ist hilfreich, wenn:

- viele Domains und Benutzer regelmäßig verwaltet werden müssen;
- Kunden oder beauftragte Personen eigene Zugänge benötigen;
- Sie eine Oberfläche für SSL, PHP, Datenbanken, Backups und E-Mail wünschen.

Das **Benutzer- und Kontenmodell** des Panels ist wichtiger als die beworbene Zahl unterstützter Domains.

### Container {#containers}

Container sind sinnvoll, wenn:

- die Isolation von Abhängigkeiten und Laufzeitumgebungen wichtig ist;
- die Anwendungen unterschiedliche Softwareumgebungen verwenden;
- die Bereitstellung bereits auf Containern basiert;
- das Team mit dem Containerbetrieb vertraut ist.

Container machen den Betrieb nicht automatisch einfacher. Sie bringen zusätzliche Aufgaben bei Image-Pflege, Netzwerk, persistenten Volumes, Backups und Monitoring mit sich.

## Websites von Agenturen und Kunden {#agency-and-client-websites}

Für Agenturen ist der Betrieb mehrerer Websites auf einem Server naheliegend. Websites verschiedener Kunden erhöhen jedoch die Anforderungen an die Trennung.

Legen Sie fest:

- wem Domain und DNS-Verwaltung gehören;
- welche getrennten Panel- und Systemkonten eingerichtet werden;
- welche eigenen Datenbankzugänge verwendet werden;
- wie Zugriffe delegiert werden;
- wer die Backups pro Kunde verantwortet;
- wie gezielt sich einzelne Bestandteile wiederherstellen lassen;
- wie Migration und Export beim Weggang eines Kunden funktionieren;
- wer Anwendungsupdates übernimmt;
- ob ein Vorfall auf einer Kundenwebsite andere Websites beeinträchtigen darf.

Versprechen Sie kein „isoliertes Hosting“, wenn alle Kundenwebsites unter demselben Unix-Benutzer laufen und dasselbe Ausfallrisiko teilen.

Das frühere Seitenthema **VPS für Agentur-Websites** bleibt in diesem Leitfaden enthalten, solange eine künftige Prüfung der Suchergebnisse und des Suchvolumens kein klar eigenständiges Thema belegt.

Wenn niemand im Team Betriebssystemupdates, Sicherheit, Backup-Prüfungen, Monitoring und Störungsbehebung für den gemeinsamen Server übernimmt, klären Sie diese Verantwortung vor der Zusammenlegung. Dazu dient [Managed VPS vs. Unmanaged VPS]({{< relref "managed-vs-unmanaged-vps.md" >}}).

Beim Umzug eines bestehenden Website-Bestands auf einen VPS sollten Sie nicht alle Websites kopieren und sämtliche DNS-Einträge auf einmal ändern. Bereiten Sie den Wechsel vor, testen Sie ihn und stellen Sie mit einem Rückweg um. Den Ablauf beschreibt [Website auf einen VPS umziehen]({{< relref "website-migration-to-vps.md" >}}).

## Backups und gezielte Wiederherstellung {#backups-and-restore-granularity}

Auf einem gemeinsamen VPS können mehrere Websites gleichzeitig ausfallen.

Ein brauchbares Backup-Konzept beantwortet folgende Fragen:

- Kann ich nur Website A wiederherstellen?
- Kann ich nur deren Datenbank wiederherstellen?
- Kann ich nach einem Datenträger- oder Serververlust den gesamten VPS wiederherstellen?
- Gibt es eine Kopie außerhalb des Servers?
- Wie viele Daten dürfen zwischen zwei Sicherungen verloren gehen?
- Kann ich eine Wiederherstellung testen, ohne andere Websites zu überschreiben?

Ein vollständiges Server-Image hilft bei der Wiederherstellung nach einem größeren Ausfall. Es sollte jedoch nicht die einzige Möglichkeit sein, wenn die Reparatur einer kompromittierten Website alle anderen Projekte auf einen älteren Stand zurücksetzen würde. Aufbewahrung, externe Kopien, RPO/RTO und Wiederherstellungstests behandelt die [VPS-Backup-Strategie]({{< relref "vps-backup-strategy.md" >}}).

## Ein VPS bedeutet ein gemeinsames Ausfallrisiko {#one-vps-is-one-failure-domain}

Die Zusammenlegung senkt Kosten und doppelte Verwaltungsarbeit, vergrößert aber die Auswirkungen eines einzelnen Vorfalls.

Ein Ereignis kann alle Websites treffen:

- ein VPS-Ausfall;
- ein volles Dateisystem;
- ein fehlerhaftes Betriebssystem- oder Webserver-Update;
- ein Datenbankausfall;
- eine falsche Firewall-Regel;
- ein kompromittiertes Administrationskonto;
- Malware oder ein kompromittierter Root-Zugang;
- versehentliches Löschen;
- ein Backup-Job, der Speicherplatz oder I/O vollständig beansprucht.

Dieses Risiko besteht grundsätzlich. Entscheidend ist, ob das Unternehmen es akzeptiert.

## Wann Sie Websites oder Dienste aufteilen sollten {#when-to-split-sites-or-workloads}

Teilen Sie den Betrieb auf, wenn es dafür messbare betriebliche Gründe gibt.

Klare Auslöser sind:

- Eine Website beansprucht wiederholt den Großteil von CPU, RAM oder I/O.
- Eine geschäftskritische Website darf das Ausfallrisiko nicht mit weniger wichtigen Projekten teilen.
- Ein WooCommerce-Shop oder anderer Shop beeinträchtigt ansonsten ruhige Websites.
- Betriebssystem-, Laufzeit- oder Sicherheitsanforderungen sind unvereinbar.
- Eine Datenbank benötigt eigene RAM- und I/O-Ressourcen oder unabhängige Skalierung.
- Hintergrund-Worker oder Jobs dominieren den Ressourcenverbrauch.
- Wartungszeitfenster unterscheiden sich.
- Kunden- oder Compliance-Anforderungen verlangen eine stärkere Trennung.
- Ressourcenkonflikte bleiben trotz Optimierung und abgestimmter Zeitpläne bestehen.

Mögliche Aufteilungen:

- Kritische Website -> eigener VPS;
- Webserver -> separater Datenbank-VPS;
- Webserver -> separater VPS für Hintergrund-Worker;
- Agentur -> getrennte Kundengruppen;
- Produktivbetrieb -> separate Staging-Umgebung;
- Schreibintensive Anwendung oder Shop -> eigener Server.

Teilen Sie nicht pauschal auf: Jeder zusätzliche VPS erweitert die Aufgaben für Monitoring, Backups, Updates, Netzwerk und Störungsbehebung.

## Monitoring für einen VPS mit mehreren Websites {#monitoring-a-multi-site-vps}

Überwachen Sie zwei Ebenen.

### Serverebene {#server-level}

- CPU;
- RAM, Swap und OOM-Ereignisse;
- Speicherplatzbelegung;
- I/O-Wartezeit;
- Datenbankzustand;
- Netzwerk;
- Prozess- und Dienstzustand.

### Website-Ebene {#site-level}

- Externe HTTP(S)-Prüfungen für jeden wichtigen Hostnamen;
- Antwortzeit;
- 5xx-Fehler;
- PHP- und Anwendungsprotokolle;
- Traffic und Worker-Auslastung pro Website, soweit messbar;
- Fehler bei Cronjobs und Warteschlangen;
- Wachstum von Datenbanken, Protokollen und Speicherbedarf.

Ein Server kann erreichbar sein, obwohl ein virtueller Host, ein Zertifikat oder eine Anwendung nicht funktioniert. Das vollständige Überwachungs- und Alarmierungskonzept für Server und einzelne Hostnamen beschreibt [VPS-Monitoring]({{< relref "vps-monitoring.md" >}}).

## Checkliste für den Start mehrerer Websites {#multi-site-launch-checklist}

| Prüfung | Voraussetzung für den Start |
|---|---|
| Kapazität | Anhand der gemeinsamen Spitzenlast bemessen, nicht anhand der Domainzahl |
| DNS | Jeder Hostname verweist gezielt auf den Server |
| HTTPS | Zertifikat und Erneuerung funktionieren für jeden Hostnamen |
| Zuordnung | Passender Nginx-Serverblock bzw. Apache-vHost pro Domain |
| Benutzer | Unabhängige Websites und Kundenprojekte verwenden möglichst getrennte Konten |
| Dateien | Getrennte Webverzeichnisse und Berechtigungen |
| PHP und Anwendungen | Bei Bedarf getrennte Pools und Dienste |
| Datenbanken | Getrennte Datenbanken und Zugangsdaten; kein gemeinsames Administrationskonto |
| Protokolle | Protokolle lassen sich der jeweiligen Website zuordnen |
| Jobs | Backups, Importe und Cronjobs sind so geplant, dass problematische Überschneidungen vermieden werden |
| Backups | Externe Kopie und Wiederherstellung einzelner Websites möglich |
| Monitoring | Server und wichtige Websites werden getrennt geprüft |
| Ausfallfolgen | Das Unternehmen akzeptiert die Auswirkungen eines gemeinsamen VPS-Ausfalls |
| Anlass zur Aufteilung | Klare Kriterien für den Umzug einer Website oder eines Dienstes auf einen eigenen Server |

## Aktuelle VPS-Beispiele für mehrere Websites {#current-multi-site-vps-examples}

Diese VDSina-Standardtarife dienen ausschließlich als Beispiele zur Einordnung.

| VPS | Sinnvoller Einstieg für | Erneut prüfen bei |
|---|---|---|
| 1 vCPU / 2 GB / 40 GB — $0.50/Tag | Einige kleine gecachte oder statische Websites | Gleichzeitiger dynamischer PHP-/Datenbanklast, Panel, E-Mail und Backups |
| 2 vCPU / 4 GB / 80 GB — $0.67/Tag | Mehrere kleinere Unternehmens- oder WordPress-Websites | Shop-Betrieb, vielen aktiven Jobs und Datenbankengpässen |
| 4 vCPU / 8 GB / 160 GB — $1.34/Tag | Anspruchsvollerem gemischtem Bestand oder mehr gleichzeitiger Aktivität | Kritischen Anwendungen mit gemeinsamem Ausfallrisiko oder einer Anwendung, die unabhängig skalieren muss |

Die Stufe mit 1 GB kann für Tests oder extrem kleine Websites nützlich sein. Sie ist hier keine allgemeine Empfehlung für den produktiven Betrieb mehrerer Websites.

<p>
  <a class="btn btn-primary" href="https://www.vdsina.com/?partner=ni8gzrvz75" target="_blank" rel="sponsored nofollow noopener">Aktuelle VPS-Angebote für mehrere Websites prüfen</a>
</p>
<p><small>Offenlegung: Der Betreiber unterhält eine berufliche Beziehung zu VDSina. Diese Website kann eine Provision erhalten, wenn Sie über diesen Partnerlink bestellen. Prüfen Sie die aktuellen VPS-Preise und wählen Sie die Architektur anhand der gemessenen Last und des akzeptablen Ausfallrisikos.</small></p>

## Häufige Fragen {#faq}

### Wie viele Websites kann ich auf einem VPS hosten? {#how-many-websites-can-i-host-on-one-vps}

Es gibt keine verlässliche feste Anzahl. Maßgeblich ist die gemeinsame Spitzenlast aller Websites bei CPU, RAM, PHP-/Anwendungs-Workern, Datenbankzugriffen, Speicher und Hintergrundaufgaben.

### Brauchen mehrere Websites getrennte IP-Adressen? {#do-multiple-websites-need-separate-ip-addresses}

In der Regel nicht. Namensbasiertes virtuelles Hosting und TLS SNI ermöglichen mehreren HTTPS-Domains, eine öffentliche IP zu teilen. Für besondere Netzwerk-, E-Mail- oder Altsoftware-Anforderungen können getrennte IPs dennoch sinnvoll sein.

### Können sich mehrere WordPress-Websites einen VPS teilen? {#can-several-wordpress-sites-share-one-vps}

Ja. Verwenden Sie getrennte Benutzer und Zugangsdaten und bemessen Sie den Server anhand der gemeinsamen PHP-, Datenbank- und Hintergrundlast. Mehrere kleine WordPress-Websites können gut zusammenpassen; eine anspruchsvolle dynamische Website kann dagegen den gesamten Server beanspruchen.

### Sollte jede Website einen eigenen PHP-FPM-Pool haben? {#should-every-site-have-a-separate-php-fpm-pool}

Bei unabhängigen PHP-Websites oder Kundenprojekten verbessern getrennte Pools die Prozess- und Benutzerisolation und erleichtern Anpassungen und Protokollierung pro Website. Die genaue Umsetzung hängt vom Panel und der Webumgebung ab.

### Kann ein WooCommerce-Shop einen VPS mit anderen Websites teilen? {#can-one-woocommerce-store-share-a-vps-with-other-sites}

Das ist möglich. Lastspitzen bei Checkout, Datenbank und Hintergrundaufgaben können jedoch den gesamten Betrieb dominieren. Ist der Shop geschäftskritisch oder verdrängt er wiederholt andere Websites, sollte er einen eigenen Server erhalten.

### Ist ein Control Panel für mehrere Websites besser? {#is-a-control-panel-better-for-hosting-multiple-websites}

Für die Verwaltung häufig ja. Ein Panel vereinfacht Domains, Benutzer, SSL, PHP, Datenbanken und Backups. Prüfen Sie aber das Modell zur Benutzer- und Kontentrennung sowie den zusätzlichen Ressourcenbedarf.

### Sind Container für mehrere Websites erforderlich? {#are-containers-required-for-multiple-websites}

Nein. Virtuelle Hosts in Nginx oder Apache mit getrennten Benutzern und Prozessen können viele Websites bedienen. Container sind hilfreich, wenn die Isolation von Abhängigkeiten und Prozessen die zusätzliche Betriebskomplexität rechtfertigt.

### Was ist das größte Risiko mehrerer Websites auf einem VPS? {#what-is-the-main-risk-of-hosting-many-websites-on-one-vps}

Die gemeinsamen Ausfallfolgen. Eine Störung, ein fehlerhaftes Update, ein voller Datenträger oder ein kompromittierter Server kann alle darauf betriebenen Websites treffen.

### Sollten Agenturen alle Kunden auf einem VPS unterbringen? {#should-agencies-put-all-clients-on-one-vps}

Nur wenn die Agentur das gemeinsame Ausfallrisiko akzeptiert und eine wirksame Trennung von Konten, Dateien und Datenbanken sowie Backups, Monitoring und geregelte Ausstiegsverfahren umsetzt. Kritische Kundenprojekte oder inkompatible Anforderungen können eigene Server rechtfertigen.

### Wann sollte ich auf mehrere VPS-Server aufteilen? {#when-should-i-split-into-multiple-vps-servers}

Teilen Sie auf, wenn eine Anwendung die Ressourcen dominiert, eine kritische Website unabhängig von anderen Ausfällen bleiben muss, Softwareumgebungen oder Sicherheitsanforderungen nicht zusammenpassen oder Datenbank und Worker unabhängig skalieren müssen.
