---
title: "VPS für Websites dimensionieren"
description: "VPS für Websites dimensionieren: CPU, RAM und Speicher anhand realer Last, Shared-Hosting-Limits, PHP-Worker, Datenbankbedarf und Lastspitzen berechnen."
image: "images/home/vps-for-website-hero.webp"
slug: "vps-fuer-websites-dimensionieren"
---

Die Dimensionierung eines VPS für eine Website beginnt mit der Last, die den Ursprungsserver tatsächlich erreicht, nicht mit der monatlichen Besucherzahl. Cache-Nutzung, gleichzeitige dynamische Anfragen, PHP- oder Anwendungs-Worker, Datenbankaktivität, Hintergrundaufgaben, der Eigenbedarf des Control Panels und das Datenwachstum bestimmen, wie viel CPU, RAM und Speicherplatz die Website wirklich benötigt.

Die übergeordnete Kaufentscheidung behandelt [VPS für Websites]({{< relref "_index.md" >}}).

[Zur RAM-Berechnung](#ram-budget) · [Shared-Hosting-Diagnose](#shared-hosting-to-vps-diagnostic) · [Passenden Tarif finden](#match-the-result-to-a-vps) · [FAQ](#faq)

## Schnelle Orientierung zur Dimensionierung {#quick-sizing-answer}

Diese VDSina-Standard-Konfigurationen dienen als Referenz. Die tatsächliche Last sollte die Tarifwahl bestimmen. Die folgenden Anbieterangaben wurden am 13. Oktober 2026 geprüft.

| Website-Last | Beispiel für den Einstieg | Was zu prüfen ist |
|---|---:|---|
| Sehr schlanke Website, Testumgebung, konsequent gecachtes Projekt | 1 vCPU / 1 GB RAM / 10 GB — $0.07/Tag, 1 TB/Monat Datentransfer | Freie RAM-Reserve, Datenbankgröße, Swap-Nutzung |
| Kleine Website oder schlankes CMS | 1 vCPU / 2 GB RAM / 40 GB — $0.50/Tag, 32 TB/Monat Datentransfer | PHP-Worker, Panel-Eigenbedarf, Datenbankspeicher |
| Unternehmenswebsite oder typische dynamische WordPress-Last | 2 vCPU / 4 GB RAM / 80 GB — $0.67/Tag, 32 TB/Monat Datentransfer | Gleichzeitige ungecachte Anfragen, Cronjobs, Datenbanklatenz |
| Anspruchsvollere dynamische Website, größere Datenbank oder mehrere aktive Websites | 4 vCPU / 8 GB RAM / 160 GB — $1.34/Tag, 32 TB/Monat Datentransfer | Anhaltende CPU-Last, Worker-Speicher, überlagerte Lastspitzen |

Das sind Orientierungshilfen, keine garantierten Besuchergrenzen. Zwei Websites mit derselben Besucherzahl können sehr unterschiedliche Server benötigen. Preise, Transferkontingente und andere Anbieterbedingungen können sich ändern. Prüfen Sie deshalb vor der Bestellung das aktuelle Angebot.

<p>
  <a class="btn btn-primary" href="https://www.vdsina.com/?partner=ni8gzrvz75" target="_blank" rel="sponsored nofollow noopener">Aktuelle VPS-Konfigurationen prüfen</a>
</p>
<p><small>Offenlegung: Der Herausgeber steht in einer beruflichen Beziehung zu VDSina. Diese Website kann eine Provision erhalten, wenn Sie über diesen Partnerlink bestellen. Die Größenempfehlung richtet sich nach der Last, nicht nach der Provision.</small></p>

## Das Größenmodell: Ressourcen einplanen, bevor Besucher gezählt werden {#the-sizing-model-reserve-resources-before-counting-traffic}

Ein brauchbares VPS-Budget betrachtet die einzelnen Ressourcenverbraucher des Servers.

### RAM-Budget {#ram-budget}

Der gesamte Arbeitsspeicher muss Folgendes abdecken:

1. Betriebssystem und Systemdienste;
2. Webserver oder Reverse Proxy;
3. PHP-FPM, Node.js, Python oder eine andere Anwendungslaufzeit;
4. die Datenbank;
5. Cache-Dienste wie Redis, sofern verwendet;
6. das Control Panel und seine Dienste;
7. Monitoring-, Sicherheits- und Backup-Prozesse;
8. gleichzeitig aktive Anwendungs-Worker;
9. eine Sicherheitsreserve für Lastspitzen, Deployments und Wartung.

Verwechseln Sie das Speicherlimit eines CMS nicht mit dem RAM-Bedarf des Servers. Ein PHP-Speicherlimit von 256 MB bedeutet nicht, dass ein VPS mit 1 GB vier gleichzeitige PHP-Prozesse mit jeweils 256 MB sowie Linux, die Datenbank und alle weiteren Dienste sicher betreiben kann.

Ein praktikables Modell lautet:

**Benötigter RAM = Basisdienste + Arbeitsspeicher der Datenbank + Speicher gleichzeitiger Worker + Speicher für Hintergrundaufgaben + Reserve**

Messen Sie nach Möglichkeit die tatsächlichen Prozesse. Schätzungen helfen bei der Wahl eines Einstiegstarifs; Messwerte zeigen, ob dieser wirklich ausreicht.

### RAM-Budget-Rechner {#ram-budget-estimator}

Dieser Rechner macht die Annahmen sichtbar, statt aus Besucherzahlen zu raten. Er schätzt nur die RAM-Klasse; CPU, Speicher und I/O müssen separat geprüft werden. Tragen Sie eigene Messwerte ein. Die Platzhalter entsprechen dem Rechenbeispiel weiter unten und sind keine allgemeingültigen Vorgaben.

<div class="rounded-2xl bg-light p-6 dark:bg-darkmode-light">
<form id="ram-budget-estimator-form">
  <div class="mb-6">
    <label for="ram-baseline" class="form-label">Basisbedarf von Betriebssystem und Webdiensten, MB</label>
    <input id="ram-baseline" class="form-input" type="number" min="0" step="1" placeholder="450" required>
  </div>
  <div class="mb-6">
    <label for="ram-database" class="form-label">Arbeitsspeicher der Datenbank, MB</label>
    <input id="ram-database" class="form-input" type="number" min="0" step="1" placeholder="500" required>
  </div>
  <div class="mb-6">
    <label for="ram-workers" class="form-label">Gleichzeitig aktive Anwendungs-Worker</label>
    <input id="ram-workers" class="form-input" type="number" min="0" step="1" placeholder="6" required>
  </div>
  <div class="mb-6">
    <label for="ram-worker-mb" class="form-label">Durchschnittlicher Speicher pro Worker, MB</label>
    <input id="ram-worker-mb" class="form-input" type="number" min="0" step="1" placeholder="120" required>
  </div>
  <div class="mb-6">
    <label for="ram-background" class="form-label">Panel, Cache und Hintergrundaufgaben, MB</label>
    <input id="ram-background" class="form-input" type="number" min="0" step="1" placeholder="300" required>
  </div>
  <div class="mb-6">
    <label for="ram-headroom" class="form-label">Sicherheitsreserve, %</label>
    <input id="ram-headroom" class="form-input" type="number" min="0" max="100" step="1" value="25" required>
  </div>
  <button class="btn btn-primary" type="submit">RAM-Klasse berechnen</button>
</form>
<p id="ram-budget-result" class="mt-6 rounded border border-border p-4 dark:border-darkmode-border" role="status" aria-live="polite">Messwerte eingeben und den Speicherbedarf berechnen.</p>
</div>

<script>
document.addEventListener("DOMContentLoaded", function () {
  var form = document.getElementById("ram-budget-estimator-form");
  if (!form) return;
  form.addEventListener("submit", function (event) {
    event.preventDefault();
    function number(id) {
      var value = Number(document.getElementById(id).value);
      return Number.isFinite(value) && value >= 0 ? value : 0;
    }
    var baseline = number("ram-baseline");
    var database = number("ram-database");
    var workers = number("ram-workers");
    var workerMb = number("ram-worker-mb");
    var background = number("ram-background");
    var headroom = number("ram-headroom");
    var subtotal = baseline + database + (workers * workerMb) + background;
    var required = subtotal * (1 + headroom / 100);
    var requiredGb = Math.round((required / 1024) * 10) / 10;
    var tier;
    if (required <= 1024) tier = "1 GB RAM";
    else if (required <= 2048) tier = "2 GB RAM";
    else if (required <= 4096) tier = "4 GB RAM";
    else if (required <= 8192) tier = "8 GB RAM";
    else tier = "mehr als 8 GB RAM oder eine aufgeteilte Architektur";
    document.getElementById("ram-budget-result").textContent =
      "Geschätzter Speicherbedarf gleichzeitig laufender Dienste: etwa " + requiredGb + " GB einschließlich Reserve. Einstiegsklasse allein nach RAM: " + tier +
      ". Prüfen Sie vor der Bestellung den tatsächlichen Prozessspeicher und die CPU-Last.";
  });
});
</script>

Rechenbeispiel: 450 MB für Basisdienste + 500 MB für die Datenbank + 6 Worker × 120 MB + 300 MB für Panel, Cache und Hintergrundaufgaben = 1970 MB vor der Reserve. Mit 25% Reserve ergibt sich ein Budget von etwa 2.4 GB. Ein VPS mit 2 GB wäre unter diesen Annahmen zu knapp; 4 GB ist die sicherere Einstiegsklasse.

Bei Messungen von PHP-FPM oder ähnlichen Workern kann der rohe RSS-Wert gemeinsam genutzte Speicherseiten und Bibliotheken über mehrere Prozesse hinweg doppelt zählen. Prozessmessungen sind deshalb Anhaltspunkte, keine perfekt addierbare Speicherabrechnung.

### CPU-Budget {#cpu-budget}

Der CPU-Bedarf hängt davon ab, wie viel Arbeit gleichzeitig ausgeführt werden muss. Statische Dateien aus dem Cache können wenig Rechenleistung erfordern. Dynamische Anfragen, die Anwendungscode ausführen, Datenbanken abfragen, Seiten erzeugen, Bilder skalieren, Importe durchführen oder APIs ansprechen, können wesentlich mehr CPU beanspruchen.

Achten Sie auf:

- anhaltende CPU-Sättigung bei legitimen Zugriffen;
- lange Anwendungsantwortzeiten bei ausgelasteter CPU;
- mehrere aufwendige dynamische Anfragen zur selben Zeit;
- Cronjobs, Backups oder Importe, die mit Besucherzugriffen zusammenfallen;
- CPU-intensive Datenbankabfragen aufgrund ineffizienter Indizes oder unnötiger Arbeit.

Eine kurze CPU-Spitze rechtfertigt nicht automatisch ein Upgrade. Aussagekräftiger ist eine anhaltende Sättigung, die legitime Arbeit verzögert.

Eine praktische Schätzung der Parallelität lautet:

**Aktive dynamische Anfragen ≈ dynamische Anfragen pro Sekunde × Anfragedauer**

Beispiel: 6 ungecachte dynamische Anfragen pro Sekunde bei einer p95-Dauer von 0.8 Sekunden entsprechen ungefähr 4.8 gleichzeitig aktiven Anfragen. Benötigt die Anwendung einen Worker pro aktiver Anfrage, planen Sie etwa fünf beschäftigte Worker plus Warteschlangenreserve ein. Verbraucht jede Anfrage 0.12 CPU-Sekunden, entsprechen 6 Anfragen pro Sekunde vor der Reserve ungefähr 0.72 CPU-Sekunden Arbeit pro Sekunde. Das ist eine Lastschätzung, keine allgemeingültige vCPU-Zusage: CPU-Generation, Ressourcenkonkurrenz und die Zuteilung durch den Anbieter unterscheiden sich.

## Beispiele für unterschiedliche Website-Lasten {#website-workload-examples}

Dieselbe Besucherzahl kann sehr unterschiedliche VPS-Anforderungen erzeugen, weil je nach Anwendung unterschiedlich viel Arbeit am Ursprungsserver anfällt.

| Lastprofil | Typische Belastung | Konsequenz für die Dimensionierung |
|---|---|---|
| Überwiegend statische oder konsequent gecachte Website | geringe Anwendungs-CPU-Last, wenige gleichzeitige Worker, hauptsächlich Dateiauslieferung | klein beginnen, aber Betriebssystem, Logs, Backups und unerwartete ungecachte Anfragen berücksichtigen |
| Kleine WordPress-Website | PHP-Worker, Datenbanklesezugriffe, Plugin- und Cron-Aktivität | RAM und Worker-Reserve sind meist wichtiger als die reine monatliche Besucherzahl |
| WooCommerce oder andere transaktionsorientierte Website | ungecachter Warenkorb, Checkout, Kontositzungen, geplante Aktionen und mehr Datenbankschreibvorgänge | dynamische Parallelität, Datenbanklatenz und überlagerte Spitzen priorisieren; 1–2 GB nicht als pauschalen Produktionsstandard behandeln |
| Mehrere Websites | gemeinsam laufende PHP-/Anwendungs-Worker, Datenbanken, Cronjobs und überlagerte Spitzen | nach der gesamten Spitzenlast dimensionieren und trennen, wenn eine Website den anderen Ressourcen entziehen kann |
| Website mit vielen Hintergrund-Workern oder Automatisierungen | Warteschlangen, Importe, Exporte, API-Aufrufe, Bildverarbeitung, geplante Aufgaben | CPU/RAM außerhalb der Besucheranfragen reservieren und Worker auslagern, wenn sprunghafte Joblast die Website stört |

Das sind typische Lastprofile, keine Plattformgarantien. Nutzen Sie reale Messwerte, soweit sie vorliegen.

## Shared-Hosting-Limits in VPS-Anforderungen übersetzen {#translate-shared-hosting-limits-into-vps-requirements}

Läuft die Website bereits auf Shared Hosting, liegen die nützlichsten Anhaltspunkte für die Dimensionierung möglicherweise schon im Hosting-Dashboard.

Erfassen Sie:

- CPU-Nutzung und Ereignisse beim Erreichen des CPU-Limits;
- Nutzung des physischen Arbeitsspeichers;
- Entry Processes oder Grenzen gleichzeitiger Anfragen;
- Prozessanzahl;
- Belastung von Datenträger-I/O und IOPS;
- Datenbankgröße und -wachstum;
- belegten Speicherplatz;
- stündliche Lastspitzen statt nur monatlicher Besucherzahlen;
- Verhalten von PHP-Workern oder Anwendungsprozessen, sofern sichtbar.

### Diagnose vor dem Wechsel von Shared Hosting zum VPS {#shared-hosting-to-vps-diagnostic}

Das Muster der Limitüberschreitungen zeigt, was vor der Tarifwahl untersucht werden sollte. Das Werkzeug rechnet ein CloudLinux-Limit bewusst nicht direkt in vCPU oder RAM um.

Beginnen Sie bei cPanel-Hosting mit CloudLinux mit dem Verlauf unter Resource Usage statt mit einem einzelnen Live-Wert. Erfassen Sie wiederholte Überschreitungen und deren Zeitpunkt. Vergleichen Sie diese mit Besucherzugriffen, Cronjobs, Backups, Importen und administrativen Arbeiten.

<div class="rounded-2xl bg-light p-6 dark:bg-darkmode-light">
<form id="shared-hosting-diagnostic">
  <div class="mb-6">
    <label for="diag-evidence" class="form-label">Qualität Ihrer Datengrundlage</label>
    <select id="diag-evidence" class="form-input">
      <option value="measured">Dashboard-Verlauf / gemessene Kennzahlen</option>
      <option value="partial">Einige gemessene Kennzahlen</option>
      <option value="traffic">Nur Besucherzahlen oder Schätzungen</option>
    </select>
  </div>
  <div class="mb-6">
    <label for="diag-memory" class="form-label">Speicherlimit-Überschreitungen / PMEM-Ereignisse</label>
    <select id="diag-memory" class="form-input"><option value="0">Keine</option><option value="1">Gelegentlich</option><option value="2">Wiederholt</option></select>
  </div>
  <div class="mb-6">
    <label for="diag-cpu" class="form-label">CPU-Limit-Überschreitungen</label>
    <select id="diag-cpu" class="form-input"><option value="0">Keine</option><option value="1">Gelegentlich</option><option value="2">Wiederholt</option></select>
  </div>
  <div class="mb-6">
    <label for="diag-ep" class="form-label">Ausgeschöpfte Entry-Process- / Worker-Kapazität</label>
    <select id="diag-ep" class="form-input"><option value="0">Keine</option><option value="1">Gelegentlich</option><option value="2">Wiederholt</option></select>
  </div>
  <div class="mb-6">
    <label for="diag-nproc" class="form-label">Ausgeschöpftes Prozesslimit / NPROC</label>
    <select id="diag-nproc" class="form-input"><option value="0">Keine</option><option value="1">Gelegentlich</option><option value="2">Wiederholt</option></select>
  </div>
  <div class="mb-6">
    <label for="diag-io" class="form-label">I/O- / IOPS-Engpässe</label>
    <select id="diag-io" class="form-input"><option value="0">Keine</option><option value="1">Gelegentlich</option><option value="2">Wiederholt</option></select>
  </div>
  <button class="btn btn-primary" type="submit">Engpass diagnostizieren</button>
</form>
<p id="shared-hosting-result" class="mt-6 rounded border border-border p-4 dark:border-darkmode-border" role="status" aria-live="polite">Wählen Sie die tatsächlich beobachteten Anzeichen aus.</p>
</div>

<script>
document.addEventListener("DOMContentLoaded", function () {
  var form = document.getElementById("shared-hosting-diagnostic");
  if (!form) return;
  form.addEventListener("submit", function (event) {
    event.preventDefault();
    function value(id) { return Number(document.getElementById(id).value); }
    var memory = value("diag-memory");
    var cpu = value("diag-cpu");
    var ep = value("diag-ep");
    var nproc = value("diag-nproc");
    var io = value("diag-io");
    var evidence = document.getElementById("diag-evidence").value;
    var confidence = evidence === "measured" ? "Hoch" : (evidence === "partial" ? "Mittel" : "Niedrig");
    var repeated = [memory, cpu, ep, nproc, io].filter(function (v) { return v === 2; }).length;
    var findings = [];
    if (memory >= 1) findings.push("Speicherdruck: Worker-Speicher, Arbeitssatz der Datenbank, Swap/OOM und Hintergrundaufgaben prüfen");
    if (cpu >= 1) findings.push("CPU-Engpass: dynamische Anfragen und Datenbankarbeit analysieren, bevor weitere vCPU hinzugefügt werden");
    if (ep >= 1) findings.push("Worker-/Parallelitätsengpass: Anfragedauer reduzieren und gleichzeitige ungecachte Anfragen messen");
    if (nproc >= 1) findings.push("Prozesslimit: ausufernde oder übermäßig viele PHP-, Cron- und Hintergrundprozesse finden, bevor zusätzliche Kapazität gekauft wird");
    if (io >= 1) findings.push("Speicher-I/O-Engpass: Datenbank-I/O, Backups, Logs und Importe untersuchen; mehr RAM allein hilft möglicherweise nicht");
    var decision;
    if (findings.length === 0) decision = "Kein deutliches Kapazitätssignal. Bleiben Sie beim aktuellen Tarif oder optimieren Sie zunächst, bis Messungen eine tatsächliche Grenze zeigen.";
    else if (repeated >= 2) decision = "WECHSELN / NACH MESSWERTEN DIMENSIONIEREN: Mehrere wiederholt erreichte Limits rechtfertigen eine VPS-Dimensionierung, nachdem offensichtliche Softwareineffizienzen beseitigt wurden.";
    else decision = "ZUERST OPTIMIEREN, DANN ERNEUT PRÜFEN: Ein Engpass ist wahrscheinlich, aber ein einzelnes Hosting-Limit ist keine direkte VPS-Spezifikation.";
    document.getElementById("shared-hosting-result").textContent =
      decision + " Aussagekraft: " + confidence + ". " + (findings.length ? findings.join("; ") + "." : "");
  });
});
</script>

Übernehmen Sie ein Shared-Hosting-Limit nicht direkt als VPS-Spezifikation. Ein CloudLinux-CPU-Prozentsatz, ein Entry-Process-Limit oder eine Speichergrenze beschreibt die bestehende Hosting-Umgebung. Das sind Hinweise auf den Engpass, keine Eins-zu-eins-Umrechnung in VPS-Ressourcen.

Nutzen Sie stattdessen das beobachtete Muster:

**Wiederholte Speicherlimit-Ereignisse bei normaler CPU-Last:** Untersuchen Sie Worker-Speicher, Datenbankspeicher und Hintergrundaufgaben, bevor Sie vCPU hinzufügen.

**Wiederholte CPU-Limit-Ereignisse bei notwendiger dynamischer Arbeit:** Analysieren Sie Anwendung und Datenbank. Ziehen Sie anschließend zusätzliche CPU-Ressourcen in Betracht, wenn die Arbeit tatsächlich erforderlich ist.

**Ausgeschöpfte Entry-Process- oder Worker-Kapazität:** Messen Sie dynamische Parallelität und Anfragedauer. Schnellere Anfragen können die Warteschlange auch ohne größeren Server beseitigen.

**I/O-Engpass:** Finden Sie Backups, Logs, Datenbankaktivität, Importe oder speicherintensive Plugins, bevor Sie davon ausgehen, dass mehr RAM das Problem löst.

So unterscheiden Sie ein tatsächliches Kapazitätsproblem von einer Tarifgrenze, die möglicherweise nur durch eine ineffiziente Komponente ausgelöst wird.

| Symptom | Prüfen | Zuerst optimieren | Skalieren, wenn |
|---|---|---|---|
| Speicherlimit-Ereignisse, Swap oder OOM | Prozessspeicher, DB-Arbeitssatz, gleichzeitige Worker | Speicherlecks, übergroße Worker, Cache-/Datenbankeinstellungen | die optimierte Last den RAM weiterhin ausschöpft |
| CPU-Drosselung | anhaltende CPU-Last zusammen mit Anfrage-/DB-Laufzeiten | langsamer Code, ungecachte Arbeit, aufwendige Abfragen | notwendige Arbeit weiterhin CPU-begrenzt bleibt |
| EP-/Worker-Warteschlange | dynamische Parallelität und Anfragedauer | Caching, langsame Endpunkte, Worker-Abstimmung | die Warteschlange trotz geringerem Aufwand pro Anfrage bestehen bleibt |
| I/O-Wartezeit / IOPS-Limit-Ereignisse | Datenbank, Logs, Backups, Importe | Zeitplanung, Indizes, Log-/Backup-Verhalten | der Speicherpfad bei normaler Arbeit der Engpass bleibt |



## VPS erweitern oder Website optimieren? {#vps-or-website-optimization}

Ein größerer VPS ist gerechtfertigt, wenn notwendige Arbeit wiederholt eine Ressource ausschöpft, obwohl offensichtliche Anwendungsprobleme bereits behoben wurden.

Optimieren Sie zuerst, wenn die Last durch Folgendes entsteht:

- ein langsames Plugin oder eine Erweiterung;
- eine Datenbankabfrage ohne passenden Index oder mit problematischem Ausführungsverhalten;
- fehlerhaftes Seiten- oder Objekt-Caching;
- missbräuchliche Bots;
- ausufernde Cronjobs;
- überdimensionierte Bildverarbeitung;
- Backups oder Malware-Scans während der Hauptzugriffszeit;
- Speicherlecks;
- übermäßige Protokollierung.

Erhöhen Sie die Serverressourcen, wenn Messungen zeigen, dass die optimierte Last weiterhin mehr Kapazität benötigt.

Diese Unterscheidung ist auch wirtschaftlich relevant. Ineffizienter Code kann nach dem Umzug vom Shared Hosting auf einen größeren VPS zunächst unauffällig wirken, obwohl der Engpass weiterhin besteht.

## PHP- und Anwendungs-Worker nach Parallelität dimensionieren {#size-php-and-application-workers-from-concurrency}

Monatliche Besucherzahlen sind eine schwache Grundlage, weil Server Anfragen gleichzeitig verarbeiten.

Bei dynamischen PHP-Anwendungen verbraucht jeder aktive PHP-Worker während der Anfrageverarbeitung Speicher und CPU. Die Worker-Kapazität hängt deshalb sowohl vom durchschnittlichen Speicherbedarf pro Worker als auch davon ab, wie lange die Anfragen die Worker belegen.

Eine vereinfachte RAM-Prüfung lautet:

**RAM-Budget für Worker = nutzbarer RAM nach Abzug der Basisdienste × sicher für Worker verfügbarer Anteil**

Vergleichen Sie dieses Budget mit dem gemessenen Worker-Speicher. Konfigurieren Sie nicht die theoretisch größtmögliche Worker-Anzahl, wenn dadurch kein Speicher für Datenbank, Cache oder Betriebssystem übrig bliebe.

Caching verändert diese Rechnung. Eine gecachte Seite für anonyme Besucher kann PHP vollständig umgehen. Checkout, angemeldete Sitzungen, wp-admin, APIs und personalisierte Seiten erreichen dagegen weiterhin die Anwendung.

WordPress-spezifisches Verhalten behandelt [VPS für WordPress]({{< relref "vps-for-wordpress.md" >}}). Für transaktionsorientierte Lasten lesen Sie [VPS für WooCommerce]({{< relref "vps-for-woocommerce.md" >}}).

## Der Datenbankbedarf kann die Servergröße bestimmen {#database-demand-can-set-the-server-size}

Eine Website kann CPU-begrenzt erscheinen, obwohl die eigentliche Ursache in der Datenbank liegt.

Prüfen Sie:

- Muster langsamer Abfragen;
- die Größe des Datenbank-Arbeitssatzes;
- gleichzeitig ausgeführte Abfragen;
- fehlende Indizes;
- umfangreiche automatisch geladene Daten oder vergleichbare Anwendungsmetadaten;
- aufwendige Such-, Filter- oder Berichtsfunktionen;
- Importe und Wartungsaufgaben;
- Speicherlatenz.

Mehr RAM kann helfen, wenn die Datenbank tatsächlich einen größeren Arbeitssatz benötigt. Ineffiziente Abfragen werden dadurch nicht repariert. Mehr CPU kann den Durchsatz erhöhen, zugleich aber auch mehr aufwendige Abfragen gleichzeitig um Ressourcen konkurrieren lassen.

## Für Lastspitzen planen, nicht für den Durchschnitt {#plan-for-peak-traffic-not-average-traffic}

Eine Dimensionierung anhand des Durchschnitts verdeckt die Zeiträume, in denen Nutzer tatsächlich Probleme erleben.

Bestimmen Sie das realistisch stärkste Lastfenster: Kampagnenstarts, Verkaufsaktionen, Newsletter-Versand, Produkteinführungen, geplante Importe, Backups oder Cron-Spitzen. Schätzen Sie ab, welche Anfragen in dieser Zeit dynamisch bleiben und welche ein Seiten-Cache oder CDN abfangen kann.

Planen Sie Reserve für das gemeinsame Auftreten von:

- normalen Besucherzugriffen;
- dynamischen Lastspitzen;
- administrativen Arbeiten;
- geplanten Aufgaben;
- Deployments und Cache-Aufwärmung;
- Monitoring- und Backup-Prozessen.

Ein CDN kann die Auslieferung statischer Inhalte und einen Teil der Anfragen an den Ursprung reduzieren. Dynamische Anwendungs- und Datenbankarbeit, die den VPS weiterhin erreicht, entfällt dadurch nicht.

Beispiel für eine Lastspitze: Erhält eine Website 20 Anfragen/s und werden 90% aus Cache/CDN bedient, erreichen den Ursprung ungefähr 2 dynamische Anfragen/s. Verdoppelt eine Kampagne den Gesamtverkehr bei derselben Cache-Quote auf 40 Anfragen/s, kommen ungefähr 4 dynamische Anfragen/s bei der Anwendung an. Bei einer p95-Dauer von 0.8 Sekunden sind das rund 3.2 gleichzeitig aktive dynamische Anfragen, noch bevor administrative Aufgaben oder Checkout-/API-Spitzen hinzukommen.

## Speicherplatz dimensionieren {#storage-sizing}

Die benötigte Datenträgerkapazität umfasst mehr als das aktuelle Website-Verzeichnis.

Berücksichtigen Sie:

- Website-Dateien;
- die Datenbank;
- hochgeladene Medien;
- Logs;
- temporäre Dateien;
- Paket- und Anwendungscaches;
- lokal aufbewahrte Staging-Kopien;
- Backup-Dateien, falls Sicherungen vorübergehend auf dem VPS entstehen;
- erwartetes Wachstum.

Füllen Sie das Dateisystem nicht bis knapp an seine Grenze. Datenbanken, Updates, Logs und Backup-Vorgänge benötigen Arbeitsraum.

Ein praktisches Kapazitätsbudget lautet:

**Benötigter Speicherplatz = aktuelle Dateien + Datenbank + temporärer Arbeitsraum + lokale Backup-Zwischenablage + erwartetes Wachstum + freie Arbeitsreserve**

Beispiel: 18 GB aktuelle Belegung + 8 GB temporärer Platz für Migration/Updates + 18 GB lokale Backup-Zwischenablage + 6 GB erwartetes Wachstum überschreiten bereits ohne Sicherheitsreserve eine 40 GB große Festplatte. In diesem Fall ist ein Tarif mit 80 GB der sicherere Einstieg. Kapazität ist von IOPS und Speicherlatenz zu unterscheiden: Ein größerer Datenträger macht eine langsame Datenbank nicht automatisch schneller.

## Bandbreite und monatlichen Datentransfer berechnen {#bandwidth-and-monthly-transfer-sizing}

Monatlicher Datentransfer ist etwas anderes als CPU, RAM oder Portgeschwindigkeit. Ein Server kann ausreichend Rechenreserve besitzen und trotzdem sein Transferkontingent überschreiten, wenn er große Dateien oder ungecachte Medien direkt ausliefert.

Eine grobe Schätzung lautet:

**Monatlicher Datentransfer am Ursprung ≈ durchschnittlich vom VPS gesendete Bytes pro Anfrage × Ursprungsanfragen pro Monat + Backups/Exporte/sonstiger ausgehender Verkehr**

Für eine aussagekräftigere Schätzung trennen Sie cachebare und dynamische Zugriffe:

**Datentransfer am Ursprung ≈ insgesamt angeforderte Bytes × (1 - durch CDN/Cache abgefangener Anteil) + ungecachte dynamische Antworten + ausgehender Verkehr anderer Dienste**

Beispiel: Fordern Nutzer im Monat 2 TB an Dateien und Seiten an und liefert ein CDN 80% dieser Bytes ohne Rückgriff auf den Ursprung aus, muss der VPS ungefähr 400 GB dieses cachebaren Verkehrs bedienen. Hinzu kommen dynamische Seiten, API-Antworten, Backups, Exporte und Cache-Misses.

Gehen Sie nicht davon aus, dass ein CDN den Datentransfer am Ursprung auf null reduziert. Angemeldete Seiten, Checkout, APIs, Cache-Misses, Cache-Löschungen, große Downloads und das Befüllen des CDN-Caches vom Ursprung können weiterhin Transfer verursachen. Trennen Sie außerdem das **monatliche Transferkontingent** von der **Netzwerk-Portgeschwindigkeit**: Ein schneller Port beschreibt den möglichen Durchsatz, das Kontingent hingegen die über den Abrechnungszeitraum übertragbare Datenmenge.

## Mehrere Websites verändern die Rechnung {#multiple-websites-change-the-calculation}

Mehrere Websites auf einem VPS teilen sich CPU, RAM, Speicher und Prozesskapazität. Ihre Lastspitzen können sich überschneiden, auch wenn jede einzelne Website klein ist.

Dimensionieren Sie den Server anhand der gemeinsamen Last. Halten Sie genügend Reserve vor, damit die Hintergrundaufgaben einer Website den anderen keine Ressourcen entziehen. Werden Isolation, Ausfallfolgen oder Ressourcenkonkurrenz wichtig, kann eine Aufteilung sinnvoller sein, als einen einzelnen Server immer weiter zu vergrößern.

Die Entscheidung behandelt [VPS für mehrere Websites]({{< relref "vps-for-multiple-websites.md" >}}).

## Control Panel und Maildienste gehören ins Ressourcenbudget {#control-panel-and-mail-overhead-belong-in-the-budget}

Ein Control Panel vereinfacht die Verwaltung von Domains, SSL, Datenbanken, PHP-Versionen und Benutzerkonten. Es betreibt aber auch eigene Dienste. Reservieren Sie dafür RAM und Speicherplatz, statt nur die Website zu berücksichtigen.

Maildienste können eine weitere dauerhaft laufende Ressourcenschicht bilden: SMTP, IMAP/POP, Spamfilter, Virenscanner, Warteschlangen, Logs und Postfachspeicher. Soll der VPS Website und E-Mail hosten, berücksichtigen Sie diesen Bedarf bei RAM, CPU, Speicher und Backups. E-Mail läuft nicht ohne zusätzlichen Aufwand mit.

Für eine kleine Website kann ein verwalteter E-Mail-Dienst Serverlast und Betriebsrisiko reduzieren. Bleibt E-Mail auf dem VPS, prüfen Sie Zustellanforderungen wie DNS-Einträge und Anbieter-/IP-Beschränkungen separat. Ein größerer VPS löst keine Probleme mit der Absenderreputation.

Wenn Sie die Verwaltung per Panel bevorzugen, vergleichen Sie die Vor- und Nachteile unter [VPS mit Control Panel]({{< relref "vps-with-control-panel.md" >}}).

## Ein wiederholbarer Ablauf zur VPS-Dimensionierung {#a-repeatable-vps-sizing-workflow}

1. **Aktuelle Last messen.** Erfassen Sie CPU, Speicher, dynamische Parallelität, Datenbankverhalten, Speicherplatz und Spitzenzeiten.
2. **Den Engpass bestimmen.** Unterscheiden Sie CPU-, RAM-, Worker-, Datenbank-, I/O- und Softwarelimit-Probleme.
3. **Offensichtliche Ineffizienz beseitigen.** Beheben Sie Cache-Probleme, ausufernde Jobs, problematische Abfragen und missbräuchliche Zugriffe, bevor Sie Kapazität kaufen.
4. **Das Ressourcenbudget aufstellen.** Reservieren Sie RAM für Basisdienste, Datenbank, Anwendungs-Worker, Panel und Hintergrundarbeit.
5. **Eine Einstiegsklasse mit Reserve wählen.** Vermeiden Sie sowohl eine Auslegung ohne Spielraum als auch vorsorglich überdimensionierte Ressourcen ohne Datengrundlage.
6. **Eine realistische Spitze nachbilden.** Prüfen Sie die Konfiguration unter repräsentativer dynamischer Last, nicht nur mit einer kaum ausgelasteten Startseite.
7. **Nach der Migration überwachen.** Passen Sie die Ressourcen anhand von Messungen an, statt die erste Schätzung als dauerhaft richtig anzusehen. Die Betriebsgrundlage beschreibt [VPS-Monitoring]({{< relref "vps-monitoring.md" >}}).

Ist das Zielsystem dimensioniert, planen Sie mit [Website auf einen VPS umziehen]({{< relref "website-migration-to-vps.md" >}}) die Bestandsaufnahme, private Tests, letzte Datensynchronisierung, DNS-Umschaltung und Rückfallmöglichkeit.

## Eine Empfehlung auf Grundlage von Messwerten {#evidence-based-recommendation}

Eine hilfreiche VPS-Empfehlung nennt sowohl die Konfiguration als auch deren Begründung.

Zum Beispiel:

**2 vCPU / 4 GB RAM / 80 GB** können ein sinnvoller Einstieg sein, wenn eine Unternehmenswebsite ein datenbankgestütztes CMS betreibt, nennenswerte ungecachte PHP-Arbeit ausführt, ein Control Panel benötigt und Betriebsreserve braucht. Das garantiert keine bestimmte Anzahl monatlicher Besucher.

Die Aussagekraft ist geringer, wenn nur Besucherzahlen vorliegen. Sie steigt, wenn CPU-Verlauf, Speicherdruck, gleichzeitige dynamische Anfragen, Worker-Speicher, Datenbankverhalten und Datenwachstum bekannt sind.

Nutzen Sie eine einfache Einstufung:

- **Niedrige Aussagekraft:** nur Besucherzahl, CMS-Name und grober Speicherplatzbedarf.
- **Mittlere Aussagekraft:** einige echte CPU-/RAM-Verlaufsdaten sowie Lastprofil und Spitzenmuster.
- **Hohe Aussagekraft:** CPU-/RAM-/I/O-Zeitreihen, ungecachte Parallelität, Worker-Speicher, Anfragedauer, Datenbankverhalten und Datenwachstum.

Eine höhere Einstufung bedeutet bessere Annahmen, keine Garantie für zukünftige Zugriffszahlen.

## Das Ergebnis einem VPS-Tarif zuordnen {#match-the-result-to-a-vps}

Betrachten Sie RAM-Schätzung, CPU-Messwerte, Speicherbudget und Spitzenverhalten gemeinsam. Diese VDSina-Standard-Konfigurationen sind Beispiele für die Zuordnung. Prüfen Sie vor der Bestellung die aktuellen Anbieterbedingungen.

<p class="vps-table-scroll-hint">Auf kleinen Bildschirmen können Sie die Tabelle seitlich verschieben, um alle Spalten zu sehen.</p>

{{< table-scroll label="VPS-Konfigurationen und ihre Eignung vergleichen" >}}
| Konfiguration | Geeigneter Einstieg für | Vermeiden / erneut prüfen bei | Wichtigste Prüfung | Aktion |
|---|---|---|---|---|
| 1 vCPU / 1 GB / 10 GB — $0.07/Tag, 1 TB/Monat | Testwebsite, sehr schlanke gecachte Website, minimale Dienste | Panel + Datenbank + mehrere dynamische Worker, produktiver Shop | RAM-Reserve und Speicherplatz | <a href="https://www.vdsina.com/?partner=ni8gzrvz75" target="_blank" rel="sponsored nofollow noopener">Aktuellen Tarif prüfen</a> |
| 1 vCPU / 2 GB / 40 GB — $0.50/Tag, 32 TB/Monat | schlanke kleine Website oder CMS mit begrenzter dynamischer Arbeit | anhaltender CPU-Last, mehreren aktiven Websites, umfangreichem Panel-/Mail-Stack | Worker-Speicher, DB-Speicher, Datenwachstum | <a href="https://www.vdsina.com/?partner=ni8gzrvz75" target="_blank" rel="sponsored nofollow noopener">Aktuellen Tarif prüfen</a> |
| 2 vCPU / 4 GB / 80 GB — $0.67/Tag, 32 TB/Monat | dynamisches Unternehmens-CMS, mäßige ungecachte PHP-Last, Panel-Reserve | anspruchsvollem WooCommerce, großen Importen, hoher DB-Last, konkurrierenden Multi-Site-Spitzen | CPU-Sättigung, DB-Latenz, überlagerte Spitzen | <a href="https://www.vdsina.com/?partner=ni8gzrvz75" target="_blank" rel="sponsored nofollow noopener">Aktuellen Tarif prüfen</a> |
| 4 vCPU / 8 GB / 160 GB — $1.34/Tag, 32 TB/Monat | anspruchsvollerer dynamischer Last, größerer DB, mehreren aktiven Websites | strengen Hochverfügbarkeitsanforderungen, sehr hoher Schreiblast, Bedarf an unabhängiger Skalierung | ob ein einzelner VPS weiterhin die passende Architektur ist | <a href="https://www.vdsina.com/?partner=ni8gzrvz75" target="_blank" rel="sponsored nofollow noopener">Aktuellen Tarif prüfen</a> |

{{< /table-scroll >}}

Ein Tarif mit 1 GB oder 2 GB ist nicht schon deshalb eine allgemeine Produktionsempfehlung, weil die Website darauf startet. E-Commerce, große Datenbanken, mehrere dynamische Websites, Maildienste und Control Panels können die Reserve schnell aufbrauchen.

<p>
  <a class="btn btn-primary" href="https://www.vdsina.com/?partner=ni8gzrvz75" target="_blank" rel="sponsored nofollow noopener">VPS auswählen</a>
</p>

## Vor dem VPS-Kauf {#before-buying-the-vps}

Prüfen Sie die Infrastrukturbedingungen, die eine Größenberechnung allein nicht beantwortet: Transferkontingent, Speichertyp und -kapazität, IP-Bedingungen, Backup-Regeln, Upgrade-Möglichkeiten, Verwaltungsumfang, Control-Panel-Lizenzen und aktuelle Abrechnung. Wählen Sie die Region separat mit [VPS-Standort auswählen]({{< relref "how-to-choose-vps-location.md" >}}), denn CPU und RAM bestimmen nicht den besten Netzwerkpfad.

Läuft die Website derzeit auf Shared Hosting, vergleichen Sie vor dem Wechsel die betrieblichen Unterschiede unter [VPS vs. Shared Hosting]({{< relref "vps-vs-shared-hosting.md" >}}).

## Technische Referenzen {#technical-references}

- cPanel: Hardwareanforderungen an einen Server
- cPanel: Ermittlung des zusätzlichen Bedarfs an RAM, CPU und Speicherplatz
- VDSina-Standard-VPS-Konfigurationen

<p>
  <a class="btn btn-primary" href="https://www.vdsina.com/?partner=ni8gzrvz75" target="_blank" rel="sponsored nofollow noopener">Aktuelles VPS-Angebot prüfen</a>
</p>
<p><small>Offenlegung: Der Herausgeber steht in einer beruflichen Beziehung zu VDSina. Partnerlinks sind als sponsored gekennzeichnet. Preise, Transferkontingente und andere Geschäftsbedingungen des Anbieters können sich ändern. Prüfen Sie diese vor der Bestellung auf der Website des Anbieters.</small></p>

## FAQ {#faq}

### Wie viel RAM benötigt ein VPS für eine Website? {#how-much-ram-does-a-website-vps-need}

Es gibt keine verlässliche allgemeingültige Größe. Eine schlanke gecachte Website kann wenig Speicher benötigen, während ein dynamisches CMS mit Datenbank, Panel und gleichzeitigen Anwendungs-Workern erheblich mehr braucht. Berechnen Sie den RAM anhand der Prozesse, die gleichzeitig laufen müssen, und halten Sie Reserve frei.

### Reichen 2 GB RAM für einen Website-VPS? {#is-2-gb-ram-enough-for-a-website-vps}

Für eine kleine, schlanke Last kann das ausreichen. Knapp wird es, wenn Control Panel, Datenbank, mehrere PHP-Worker, Hintergrundaufgaben oder mehrere Websites gleichzeitig laufen müssen. Messen Sie den Speicherdruck, statt sich allein auf die RAM-Zahl zu verlassen.

### Wofür eignet sich ein VPS mit 4 GB? {#what-does-a-4-gb-vps-tier-fit}

Ein VPS mit 4 GB ist für viele Unternehmens-CMS ein praktischer Einstieg, weil mehr Platz für Linux, Datenbank, Anwendungs-/PHP-Worker und Caching bleibt. Die genaue Eignung hängt von dynamischer Parallelität, Datenbankbedarf, Hintergrundarbeit und Panel-Eigenbedarf ab. Die WordPress-spezifische Entscheidung behandelt [VPS für WordPress]({{< relref "vps-for-wordpress.md" >}}).

### Wie viele Besucher kann ein VPS bedienen? {#how-many-visitors-can-a-vps-handle}

Die Besucherzahl allein beantwortet das nicht. Cache-Trefferquote, gleichzeitige Anfragen, Ausführungszeit der Anwendung, Datenbankarbeit und Hintergrundaufgaben können die benötigte Kapazität selbst bei ähnlich besuchten Websites um Größenordnungen verändern.

### Sollte ich zuerst RAM oder CPU erweitern? {#should-i-add-ram-or-cpu-first}

Erweitern Sie die Ressource, deren Begrenzung durch Messungen belegt ist. Speicherdruck, Swap-Aktivität oder OOM-Ereignisse sprechen für mehr RAM oder Speicheroptimierung. Anhaltende CPU-Sättigung bei notwendiger, bereits optimierter Arbeit spricht für mehr CPU. Datenbank- und I/O-Engpässe benötigen eine eigene Diagnose.

### Senkt ein CDN die VPS-Anforderungen? {#does-a-cdn-reduce-vps-requirements}

Es kann die Auslieferung statischer Dateien und cachebare Anfragen an den Ursprung reduzieren. Dynamische Anwendungsanfragen und Datenbankarbeit, die den Ursprung erreichen, verbrauchen weiterhin VPS-Ressourcen.

### Sollte ich nach Durchschnittslast oder Spitzenlast dimensionieren? {#should-i-size-for-average-or-peak-traffic}

Dimensionieren Sie für eine realistische Spitze mit Betriebsreserve. Durchschnittswerte können kurze Zeiträume verdecken, in denen gleichzeitige Zugriffe, geplante Aufgaben und dynamische Anfragen zusammentreffen.
