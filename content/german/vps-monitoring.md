---
title: "VPS-Monitoring"
slug: "vps-monitoring"
description: "VPS mit externen Erreichbarkeitsprüfungen, CPU-/RAM-/Datenträger-/Netzwerkmetriken, Dienstprüfungen, Protokollen und handlungsorientierten Alarmen überwachen. Mit Werkzeugen, Schwellenwerten und Checkliste."
image: "images/home/vps-for-website-hero.webp"
---

VPS-Monitoring sollte mehr beantworten als „Läuft der Server?“. Ein grundlegendes Monitoring für den Produktivbetrieb benötigt **externe Erreichbarkeitsprüfungen, historische Host-Metriken, Dienst- und Anwendungsprüfungen, Protokolle, handlungsorientierte Alarme und eine benannte Person für die Reaktion**.

Ein VPS kann auf Ping antworten, während Nginx ausgefallen ist, die Datenbank hängt, der Datenträger voll ist oder das TLS-Zertifikat bald abläuft. Monitoring muss deshalb sowohl den Server als auch die für Nutzer sichtbare Website abdecken.

Die grundsätzliche Serverentscheidung behandelt [VPS für Websites]({{< relref "_index.md" >}}).

[Kurzantwort](#quick-answer) · [Check](#vps-monitoring-baseline-checker) · [Host-Metriken](#monitor-cpu-memory-disk-and-network) · [Anwendungszustand](#monitor-services-and-application-health) · [Alarme](#build-actionable-alerts) · [Kapazität](#use-trends-for-capacity-planning) · [FAQ](#faq)

## Kurzantwort {#quick-answer}

Ein praktischer VPS-Monitoring-Stack umfasst fünf Ebenen:

| Ebene | Was sie zeigt | Typischer erkannter Fehler |
|---|---|---|
| **Externe Erreichbarkeit** | ob Nutzer die Website von außerhalb des VPS erreichen können | VPS, Netzwerk oder Website nicht erreichbar |
| **Host-Metriken** | Trends bei CPU, RAM, Swap, Datenträger, Inodes, I/O und Netzwerk | Speicherleck, voller Datenträger, anhaltender CPU-Engpass |
| **Dienst-/Anwendungszustand** | ob Webserver, Laufzeit, Datenbank und wichtige Endpunkte tatsächlich funktionieren | Nginx-/PHP-/Datenbank-/Anwendungsfehler bei weiterhin erreichbarem Server |
| **Protokolle/Ereignisse** | was sich geändert hat oder fehlgeschlagen ist | 5xx-Spitze, OOM, ausgefallener Worker, Datenbankfehler |
| **Alarmierung und Verantwortung** | ob die richtige Person benachrichtigt wird und handeln kann | unbemerkter Ausfall oder unbeachtetes Dashboard |

Betreiben Sie den einzigen Verfügbarkeitsmonitor nicht auf demselben VPS, den er überwachen soll. Fällt dieser VPS oder sein Netzwerkzugang vollständig aus, kann der Monitor mit ihm verschwinden.

## VPS-Monitoring-Grundlage prüfen {#vps-monitoring-baseline-checker}

Dieser Check findet Überwachungslücken. Er garantiert keine Verfügbarkeit.

<div class="rounded-2xl bg-light p-6 dark:bg-darkmode-light">
<form id="vps-monitoring-checker">
  <div class="mb-6">
    <label for="mon-workload" class="form-label">Hauptsächlicher Workload</label>
    <select id="mon-workload" class="form-input">
      <option value="static">Statische / einfache Website</option>
      <option value="cms">WordPress / CMS</option>
      <option value="transactional">WooCommerce / transaktionsbasierte Website</option>
      <option value="multi">Mehrere Websites / gemischtes Portfolio</option>
    </select>
  </div>
  <div class="mb-6">
    <label for="mon-external" class="form-label">Externe HTTP(S)-Erreichbarkeitsprüfung von außerhalb dieses VPS?</label>
    <select id="mon-external" class="form-input"><option value="no">Nein</option><option value="yes">Ja</option></select>
  </div>
  <div class="mb-6">
    <label for="mon-metrics" class="form-label">Werden historische CPU-/RAM-/Datenträger-/Netzwerkmetriken aufbewahrt?</label>
    <select id="mon-metrics" class="form-input"><option value="no">Nein / nur gelegentlich top/htop</option><option value="yes">Ja</option></select>
  </div>
  <div class="mb-6">
    <label for="mon-disk" class="form-label">Werden Speicherplatz, Inodes und Speicherengpässe überwacht?</label>
    <select id="mon-disk" class="form-input"><option value="no">Nein / nur freie GB</option><option value="yes">Ja</option></select>
  </div>
  <div class="mb-6">
    <label for="mon-app" class="form-label">Zustandsprüfungen wichtiger Dienste und Anwendungen eingerichtet?</label>
    <select id="mon-app" class="form-input"><option value="no">Nein / nur Ping</option><option value="yes">Ja</option></select>
  </div>
  <div class="mb-6">
    <label for="mon-jobs" class="form-label">Werden Datenbank, Warteschlangen, Cronjobs und Backup-Aktualität bei Bedarf überwacht?</label>
    <select id="mon-jobs" class="form-input"><option value="no">Nein / unbekannt</option><option value="yes">Ja</option><option value="na">Nicht zutreffend</option></select>
  </div>
  <div class="mb-6">
    <label for="mon-alerts" class="form-label">Automatische Alarme mit sinnvollen Schweregrad- und Dauerregeln eingerichtet?</label>
    <select id="mon-alerts" class="form-input"><option value="no">Nein / nur Dashboard</option><option value="yes">Ja</option></select>
  </div>
  <div class="mb-6">
    <label for="mon-notify" class="form-label">Bleibt der Benachrichtigungsweg bei Ausfall dieses VPS verfügbar?</label>
    <select id="mon-notify" class="form-input"><option value="no">Nein / nur derselbe VPS</option><option value="yes">Ja</option></select>
  </div>
  <div class="mb-6">
    <label for="mon-owner" class="form-label">Verantwortlicher und Ablaufplan für die erste Reaktion vorhanden?</label>
    <select id="mon-owner" class="form-input"><option value="no">Nein</option><option value="yes">Ja</option></select>
  </div>
  <button class="btn btn-primary" type="submit">Monitoring-Grundlage prüfen</button>
</form>
<p id="vps-monitoring-result" class="mt-6 rounded border border-border p-4 dark:border-darkmode-border" role="status" aria-live="polite">Bestätigen Sie nur Monitoring, das tatsächlich Daten erfasst und Alarme zustellt.</p>
</div>

<script>
document.addEventListener("DOMContentLoaded", function () {
  var form = document.getElementById("vps-monitoring-checker");
  if (!form) return;

  form.addEventListener("submit", function (event) {
    event.preventDefault();

    function yes(id) { return document.getElementById(id).value === "yes"; }
    var workload = document.getElementById("mon-workload").value;
    var external = yes("mon-external");
    var metrics = yes("mon-metrics");
    var disk = yes("mon-disk");
    var app = yes("mon-app");
    var jobsValue = document.getElementById("mon-jobs").value;
    var jobs = jobsValue === "yes" || jobsValue === "na";
    var alerts = yes("mon-alerts");
    var notify = yes("mon-notify");
    var owner = yes("mon-owner");

    var result;

    if (!external || !metrics || !app || !disk) {
      result = "ÜBERWACHUNGSLÜCKEN: Der Monitoring-Stack erkennt noch nicht alle grundlegenden Fehlerarten. Ergänzen Sie unabhängige Erreichbarkeitsprüfungen, aufbewahrte Host-Metriken, Transparenz zu Datenträger und Inodes sowie echte Dienst- und Anwendungsprüfungen.";
    } else if (!alerts || !notify || !owner) {
      result = "ALARMIERUNG / VERANTWORTUNG UNVOLLSTÄNDIG: Daten können vorhanden sein, während ein Vorfall dennoch unbemerkt oder ohne Zuständigen bleibt. Ergänzen Sie handlungsorientierte Alarme, einen unabhängigen Benachrichtigungsweg und einen Reaktionsplan mit benannter Verantwortung.";
    } else if (!jobs && (workload === "transactional" || workload === "cms" || workload === "multi")) {
      result = "GRUNDLEGENDES MONITORING: Infrastrukturüberwachung ist vorhanden. Anwendungsaufgaben, Datenbank und Backup-Aktualität bleiben für diesen Workload aber noch eine Überwachungslücke.";
    } else {
      result = "MONITORING-GRUNDLAGE FÜR DEN PRODUKTIVBETRIEB: Externe Erreichbarkeit, aufbewahrte Metriken, Dienstzustand, Alarme und Reaktionsverantwortung sind abgedeckt. Passen Sie Schwellenwerte weiter an reale Normalwerte an; dies ist keine Verfügbarkeitsgarantie.";
    }

    document.getElementById("vps-monitoring-result").textContent = result;
  });
});
</script>

## Website von außerhalb des VPS überwachen {#monitor-the-website-from-outside-the-vps}

Ein interner Befehl kann zeigen, dass Nginx läuft. Er belegt nicht, dass ein echter Nutzer im Internet die Website erreichen kann.

Nutzen Sie für wichtige Hostnamen einen externen Monitor.

Sinnvolle Prüfungen umfassen:

- HTTP-/HTTPS-Erreichbarkeit;
- erwarteten Statuscode;
- Antwortzeit;
- Schlüsselwort-/Inhaltsprüfung;
- DNS-Auflösung;
- Zustand und Ablauf des TLS-Zertifikats;
- TCP-Portprüfungen, sofern relevant.

Wo Fehlalarme problematisch sind, verlangen Sie wiederholte Fehler oder Bestätigung von mehreren Standorten, bevor jemand alarmiert wird.

Selbst gehostete Werkzeuge wie Uptime Kuma können HTTP(S)-, Schlüsselwort-, TCP-, Ping- und DNS-Prüfungen durchführen. Platzieren Sie den Monitor aber außerhalb der Ausfallumgebung des produktiven VPS.

Ein Monitoring-Server, der vom selben VPS-, Anbieternetz- oder DNS-Ausfall betroffen ist, kann für Dashboards nützlich sein, stellt aber keine unabhängige Erreichbarkeitsprüfung dar.

## Echtzeitdiagnose ist kein historisches Monitoring {#real-time-diagnostics-are-not-historical-monitoring}

Befehle wie:

```bash
top
htop
free -h
df -h
ss -s
```

sind hilfreich, wenn Sie ein Problem bereits untersuchen.

Sie zeigen nicht:

- was um 03:12 geschah;
- ob der RAM-Verbrauch sechs Stunden lang stetig wuchs;
- ob die Speicherlatenz während eines Backups anstieg;
- ob die Website zehn Minuten lang ausgefallen war;
- ob sich ein Problem von Woche zu Woche verschärft.

Bewahren Sie Zeitreihen der Signale auf, die Verfügbarkeit und Kapazität beeinflussen.

Für einen einzelnen VPS kann ein schlanker Monitoring-Agent genügen. Für mehrere Server, längere Aufbewahrung oder eigene Dashboards ist Prometheus + Node Exporter + Grafana eine verbreitete Architektur.

Prometheus Node Exporter stellt Host- und Kernelmetriken bereit, die Prometheus abrufen kann, darunter CPU-, Dateisystem- und Netzwerkdaten.

## CPU, Arbeitsspeicher, Datenträger und Netzwerk überwachen {#monitor-cpu-memory-disk-and-network}

### CPU {#cpu}

Alarmieren Sie nicht bei jeder kurzen Spitze.

Beobachten Sie:

- anhaltende CPU-Auslastung;
- durchschnittliche Last im Verhältnis zur vCPU-Anzahl;
- CPU-Verbrauch pro Prozess;
- CPU-Steal-Zeit, soweit von der Virtualisierung bereitgestellt;
- gleichzeitig auftretende Anwendungs-/Anfragelatenz.

Eine kurze 100%-Spitze beim Cache-Aufwärmen oder einem Cronjob kann harmlos sein. Anhaltende CPU-Sättigung zusammen mit wachsenden Latenzen oder Warteschlangen ist ein stärkeres Indiz für einen echten Engpass.

### Arbeitsspeicher, Swap und OOM {#memory-swap-and-oom}

Linux verwendet freien RAM häufig als Dateisystem-Cache. „90 % RAM belegt“ ist daher nicht automatisch ein Fehler.

Beobachten Sie:

- verfügbaren Arbeitsspeicher;
- Swap-Aktivität;
- Wachstum der Swap-Belegung;
- OOM-Killer-Ereignisse;
- Speicherwachstum einzelner Prozesse;
- Speicher von PHP-/Anwendungs-Workern;
- Datenbankspeicherbedarf.

Ein Speicherleck kann mittags unauffällig wirken und nachts den Prozess beenden. Historische Trends machen es sichtbar.

### Speicherplatz {#disk-capacity}

Überwachen Sie die Dateisystembelegung, bevor Datenbanken, Protokolle oder Paketupdates daran scheitern.

Ein beispielhafter erster Warn-/Kritisch-Schwellenwert könnte bei **80 % / 90 % Belegung** liegen. Das ist jedoch kein universelles SLA. Eine schnell wachsende Datenbank kann deutlich früheres Handeln erfordern.

Überwachen Sie außerdem freien Arbeitsspeicherplatz auf dem Datenträger für:

- Backups;
- Datenbankwartung;
- Paketupdates;
- Uploads;
- Protokolle;
- Staging-/Importaufgaben.

### Inodes {#inodes}

Einem Dateisystem können die Inodes ausgehen, obwohl noch viele GB frei sind.

Das kann entstehen durch:

- Cache-Verzeichnisse;
- Sitzungsdateien;
- Mail-Warteschlangen;
- sehr viele winzige Dateien;
- unkontrolliert wachsende temporäre Dateien.

Überwachen Sie die Inode-Belegung getrennt vom Speicherplatz in GB.

### Datenträger-I/O und Latenz {#disk-io-and-latency}

Der Datenträger kann zum Engpass werden, bevor seine Kapazität ausgeschöpft ist.

Beobachten Sie:

- I/O-Wartezeit;
- Lese-/Schreiblatenz;
- Warteschlangentiefe, sofern verfügbar;
- Datenbank-Antwortzeit;
- Backup-/Importzeitfenster.

Mehr Speicherkapazität behebt langsame Speicher-I/O nicht automatisch.

### Netzwerk {#network}

Erfassen Sie mehr als die gesamte Bandbreite:

- ein- und ausgehenden Durchsatz;
- plötzliche Änderungen des Datenverkehrs;
- Verbindungsfehler;
- Paketverlust/Latenz, soweit messbar;
- ungewöhnlichen ausgehenden Datenverkehr;
- Schnittstellenfehler.

Netzwerkmetriken helfen, langsame Anwendungen von Anbieter- oder Verbindungsproblemen zu unterscheiden.

## Dienste und Anwendungszustand überwachen {#monitor-services-and-application-health}

Ein VPS kann erreichbar sein, obwohl die Website defekt ist.

Überwachen Sie wichtige Dienste wie:

- Nginx/Apache;
- PHP-FPM;
- Node-/Python-Anwendungsdienst;
- MySQL/MariaDB/PostgreSQL;
- Redis, sofern verwendet;
- Warteschlangen-Worker;
- Dienst für geplante Aufgaben;
- Control Panel, sofern geschäftskritisch.

Unter systemd-basiertem Linux ist `systemctl --failed` bei der Diagnose hilfreich. Kontinuierliches Monitoring sollte aber selbst auf ausgefallene oder ständig neu startende benötigte Dienste hinweisen.

Bleiben Sie nicht bei „Prozess vorhanden“ stehen. Ein Prozess kann laufen und dennoch keine gültigen Anfragen beantworten.

## HTTP 200 bedeutet nicht immer einen gesunden Zustand {#http-200-is-not-always-healthy}

Eine Anwendung kann HTTP 200 zurückgeben und dabei Folgendes ausliefern:

- Wartungsseite;
- im Template dargestellten Datenbankfehler;
- leeren oder falschen Inhalt;
- fehlerhaften Anmeldeablauf;
- veralteten Cache.

Nutzen Sie bei kritischen Websites die gezielteste sinnvolle Prüfung:

- erwartetes Schlüsselwort beziehungsweise erwarteten Text;
- Zustandsendpunkt;
- API-Antwort;
- wichtige öffentliche URL;
- synthetische Anmeldung oder Transaktion nur dann, wenn der geschäftliche Nutzen die Komplexität rechtfertigt.

Lassen Sie synthetische Prüfungen keine Produktivdaten verändern, sofern sie nicht ausdrücklich für eine sichere Veränderung ausgelegt sind.

## TLS und DNS überwachen {#monitor-tls-and-dns}

Der VPS kann gesund sein, während die Website wegen eines Zertifikats- oder DNS-Fehlers nicht verfügbar ist.

Erfassen Sie:

- Zertifikatsablauf;
- nicht zum Hostnamen passendes Zertifikat;
- fehlgeschlagene Erneuerung;
- DNS-Auflösung;
- versehentliche Eintragsänderungen, soweit Werkzeuge dies unterstützen.

Ein sinnvolles Beispiel ist eine frühzeitige Warnung vor Zertifikatsablauf, etwa **14 Tage** vorher, mit Eskalation näher am Ablauf, etwa **7 Tage** vorher. Das genaue Zeitfenster sollte dazu passen, wie schnell jemand die Erneuerung reparieren kann.

## Datenbank als Anwendungsabhängigkeit überwachen {#monitor-the-database-as-an-application-dependency}

Bei datenbankgestützten Websites sollte das Monitoring erkennen lassen, ob die Datenbank der Engpass oder eine ausgefallene Abhängigkeit ist.

Je nach Engine und Workload sind folgende Signale nützlich:

- Dienstverfügbarkeit;
- Anzahl der Verbindungen;
- Verbindungsfehler;
- Abfragelatenz;
- Anzeichen von Sperren und Ressourcenkonflikten;
- langsame Abfragen;
- Speicherengpässe;
- Speicherplatzwachstum;
- Replikations-/Backup-Status, sofern verwendet.

Alarmieren Sie nicht bei jeder Datenbankmetrik. Alarmieren Sie bei Zuständen mit Nutzerwirkung oder Bezug zu einer bekannten Fehlerart.

Das Workload-Verhalten von WordPress behandelt [VPS für WordPress]({{< relref "vps-for-wordpress.md" >}}). Für transaktionsbasierte Shops siehe [VPS für WooCommerce]({{< relref "vps-for-woocommerce.md" >}}).

## Cronjobs, Warteschlangen und Hintergrundaufgaben überwachen {#monitor-cron-queues-and-background-jobs}

Eine erreichbare Startseite belegt nicht, dass Hintergrundarbeit gesund läuft.

Erfassen Sie für die Anwendung wichtige Aufgaben:

- Cronjobs;
- Warteschlangen-Worker;
- geplante Importe;
- Webhooks;
- E-Mail-Aufgaben;
- WordPress WP-Cron/System-Cron;
- WooCommerce Action Scheduler;
- Abonnements/Verlängerungen;
- Bestandsabgleich.

Nützliche Signale:

- letzte erfolgreiche Ausführung;
- Warteschlangenlänge/Rückstand;
- fehlgeschlagene Aufgaben;
- älteste ausstehende Aufgabe;
- wiederholte Ausführungsversuche;
- gestoppter oder neu startender Worker.

Bei WooCommerce kann eine wachsende Warteschlange fehlgeschlagener oder überfälliger Action-Scheduler-Aufgaben ein Betriebsproblem sein, obwohl Katalogseiten weiterhin laden.

## Backup-Aktualität überwachen {#monitor-backup-freshness}

Ein Backup-Auftrag gehört zur Wiederherstellungsstrategie, aber **Backup-Aktualität ist ein Monitoring-Signal**.

Alarmieren Sie, wenn:

- ein geplantes Backup fehlschlägt;
- das letzte erfolgreiche Backup älter ist als die festgelegte RPO;
- ein Datenbank-Dump fehlschlägt;
- der externe Upload scheitert;
- Repository-Zugangsdaten ablaufen;
- sich die Backup-Größe verdächtig verändert;
- Bereinigung oder Aufbewahrungsverwaltung fehlschlägt.

Betrachten Sie „Cron wurde ausgeführt“ nicht als Beweis für ein verwendbares Backup.

Für RPO/RTO, Aufbewahrung, unabhängige Kopien und Wiederherstellungsübungen nutzen Sie die [VPS-Backup-Strategie]({{< relref "vps-backup-strategy.md" >}}).

## Protokolle mit Metriken zusammenführen {#correlate-logs-with-metrics}

Metriken zeigen, **was sich geändert hat**. Protokolle zeigen häufig, **warum**.

Vergleichen Sie dasselbe Zeitfenster in:

- Nginx-/Apache-Zugriffs- und Fehlerprotokollen;
- PHP-FPM-/Laufzeitprotokollen;
- Anwendungsprotokollen;
- Datenbankprotokollen;
- Systemjournal;
- Authentifizierungsprotokollen;
- Backup-/Aufgabenprotokollen.

Beispiel:

- CPU-Spitze um 14:03;
- Anstieg von 5xx-Fehlern um 14:03;
- Anwendungsprotokoll zeigt Datenbank-Zeitüberschreitungen;
- Datenbankprotokoll zeigt konkurrierende Sperren.

Das ist handlungsrelevanter als ein allgemeiner Alarm „CPU hoch“.

Bewahren Sie Protokolle lange genug für die Vorfalluntersuchung auf, lassen Sie sie aber nicht das Produktivdateisystem füllen.

## Handlungsorientierte Alarme einrichten {#build-actionable-alerts}

Ein Alarm sollte dem Betreiber mitteilen, was ausgefallen ist und was zuerst geprüft werden muss.

Bevorzugen Sie:

- **Warnung** — untersuchen, bevor Nutzer betroffen sind;
- **kritisch** — Nutzer betroffen oder Ausfall unmittelbar bevorstehend;
- Mindestdauer/Entprellung — keine Alarmierung wegen einsekündiger Spitzen;
- Gruppierung/Deduplizierung — keine 40 Meldungen für einen Ausfall;
- eindeutige Angabe des betroffenen Hosts/Dienstes;
- Verknüpfung zu Dashboard, Protokoll oder Ablaufplan;
- bekannte erste Maßnahme und Eskalation.

Prometheus Alertmanager ist ein Beispiel für ein System zum Gruppieren, Deduplizieren und Weiterleiten von Alarmen.

### Keine universellen Schwellenwerte {#avoid-universal-thresholds}

Schwellenwerte sollten zum Workload passen.

Beispiele für sinnvolle erste Regeln:

- CPU: anhaltend hohe Nutzung plus Latenz-/Warteschlangensymptome statt einer einzelnen Spitze;
- RAM: wenig verfügbarer Speicher plus Swap/OOM statt nur „RAM-Belegung > 80 %“;
- Datenträger: früh warnen, solange genügend Betriebsreserve bleibt;
- TLS: Tage vor dem Ablauf warnen;
- HTTP: wiederholter Fehler oder Bestätigung mehrerer Standorte, wenn Fehlalarme relevant sind;
- Backup: letzter Erfolg älter als RPO;
- 5xx/Latenz: anhaltende Abweichung vom normalen Anwendungsniveau.

Passen Sie die Regeln an, nachdem Sie das normale Produktivverhalten beobachtet haben.

## Benachrichtigungsweg unabhängig halten {#keep-the-notification-path-independent}

Ein Alarm ist nutzlos, wenn sein Zustellsystem bei demselben Vorfall ausfällt.

Versenden Sie wichtige Alarme nach Möglichkeit über einen Weg außerhalb des VPS:

- externer E-Mail-Anbieter;
- externer Chat-/Benachrichtigungsdienst;
- gehostetes Werkzeug für Vorfallmanagement;
- Monitoring-Instanz in einer anderen Ausfallumgebung.

Verlassen Sie sich nicht ausschließlich auf einen SMTP-Server oder ein Dashboard auf demselben ausgefallenen VPS.

## Jeder Alarm braucht Verantwortung und Ablaufplan {#every-alert-needs-an-owner-and-runbook}

Beantworten Sie vor dem Anlegen eines Alarms:

- Wer erhält ihn?
- Wer darf handeln?
- Was ist der erste Diagnoseschritt?
- Welches Dashboard oder Protokoll soll geöffnet werden?
- Wann wird eskaliert?
- Wann kann er gefahrlos stummgeschaltet werden?
- Was geschieht außerhalb der Geschäftszeiten?

Wenn niemand die Reaktion verantwortet, hat das Monitoring-System lediglich einen Ausfall in eine Benachrichtigung umgewandelt.

Die übergreifende Entscheidung zur Betriebsverantwortung behandelt [Managed vs. Unmanaged VPS]({{< relref "managed-vs-unmanaged-vps.md" >}}).

## Monitoring-Stack nach Komplexität wählen {#choose-the-monitoring-stack-by-complexity}

Installieren Sie keine große Observability-Plattform nur deshalb, weil sie populär ist.

### Anbieter-Dashboard als erste Ebene {#provider-dashboard-as-a-starting-layer}

Stellt der VPS-Anbieter historische CPU-, RAM-, Datenträger- oder Netzwerkdaten bereit, nutzen Sie diese als bequemen Ausgangspunkt auf Host-Ebene.

Verwechseln Sie Infrastrukturdiagramme des Anbieters nicht mit vollständigem Website-Monitoring. Sie prüfen möglicherweise weder den öffentlichen HTTP(S)-Zugang von außerhalb des Anbieters noch Anwendungsinhalte, Datenbankzustand, Hintergrundaufgaben, TLS-Erneuerung oder Alarmverantwortung.

Betrachten Sie Anbieter-Monitoring als eine Informationsquelle und ergänzen Sie externe und anwendungsbezogene Prüfungen entsprechend dem Workload.

### Schlanker Weg für einen einzelnen VPS {#lightweight-single-vps-path}

Eine praktische kleine Konfiguration kann kombinieren:

- externen Verfügbarkeitsmonitor;
- Netdata oder einen anderen Host-Metrik-Agenten mit Dashboard;
- System-/Anwendungsprotokolle;
- Benachrichtigungen.

Gut geeignet, wenn eine Person einen oder wenige VPS verwaltet.

### Prometheus-/Grafana-Weg {#prometheus--grafana-path}

Nützlich, wenn Sie Folgendes benötigen:

- Metriken mehrerer Server;
- längere historische Aufbewahrung;
- eigene Abfragen;
- Dienst-/Exporter-Metriken;
- gemeinsame Dashboards;
- strukturierte Alarmregeln.

Node Exporter liefert Linux-Host-Metriken; Prometheus speichert und durchsucht sie; Grafana visualisiert sie; Alertmanager kann Alarme weiterleiten, gruppieren und deduplizieren.

### Gehostetes Monitoring {#hosted-monitoring-path}

Nützlich, wenn:

- der Monitor unabhängig von Ihrem VPS oder Anbieter sein muss;
- Sie weniger eigene Monitoring-Infrastruktur betreiben möchten;
- verwaltete Benachrichtigungen und Bereitschaftsdienst-Integrationen wertvoll sind.

Das Monitoring-System selbst ist Produktivinfrastruktur. Halten Sie seine Komplexität im Verhältnis zum verringerten Risiko.

## Monitoring-Stack absichern {#secure-the-monitoring-stack}

Monitoring-Agenten und Dashboards können sensible Betriebsdaten offenlegen.

Schützen Sie:

- Dashboards;
- Exporter;
- Metrik-Endpunkte;
- API-Token;
- Benachrichtigungs-Webhooks;
- Protokoll-Backends.

Veröffentlichen Sie Prometheus, Node Exporter, Grafana oder Administrationsdashboards nicht offen im Internet, ohne ein ausdrücklich abgesichertes Zugriffsmodell.

Verwenden Sie passend zur Umgebung Firewall-Regeln, private Netzwerke oder Authentifizierung am Reverse Proxy.

Monitoring ersetzt keine Härtung; nutzen Sie die [VPS-Sicherheitscheckliste]({{< relref "vps-security-checklist.md" >}}) für den Servergrundschutz.

## Monitoring-Ressourcenbedarf berücksichtigen {#monitoring-overhead-matters}

Monitoring verbraucht:

- RAM;
- CPU;
- Datenträgerspeicher für Metrik- und Protokollaufbewahrung;
- Netzwerkressourcen;
- Backup-Kapazität.

Ein kleiner Agent ist meist sparsam. Lange aufbewahrte Metriken und Protokolle können jedoch eine erhebliche Speicherlast erzeugen.

Beobachten Sie den Monitoring-Stack selbst:

- Agenten-/Dienstzustand;
- Fehler beim Metrikabruf;
- Speicherwachstum;
- Aufbewahrung;
- Zustellung von Benachrichtigungen.

Lassen Sie die Beobachtungswerkzeuge nicht den Datenträger füllen, den sie schützen sollen.

## Trends für die Kapazitätsplanung nutzen {#use-trends-for-capacity-planning}

Historisches Monitoring ist die beste Grundlage für die nächste Dimensionierungsentscheidung.

Beantworten Sie anhand von Trends:

- Ist die CPU dauerhaft oder nur gelegentlich ausgelastet?
- Sinkt der verfügbare RAM über Wochen?
- Treten Swap-Nutzung oder OOM unter legitimer Last auf?
- Wie schnell wächst die Datenträgerbelegung?
- Steigt die Datenbanklatenz bei Besucherspitzen?
- Bilden sich PHP-/Anwendungswarteschlangen?
- Verursachen Backup-/Importaufträge vorhersehbare Ressourcenkonflikte?

Rüsten Sie nicht auf, nur weil ein Dashboard kurz rot wurde.

Skalieren Sie, wenn der **optimierte legitime Workload** wiederholt eine Ressource erschöpft oder die Architektur unabhängige Skalierung benötigt.

Nutzen Sie [VPS-Dimensionierung für Websites]({{< relref "vps-sizing-for-website.md" >}}), um Monitoring-Erkenntnisse in eine Ressourcenentscheidung zu übersetzen.

<p>
  <a class="btn btn-primary" href="https://www.vdsina.com/?partner=ni8gzrvz75" target="_blank" rel="sponsored nofollow noopener">Aktuelle VPS-Konfigurationen prüfen</a>
</p>
<p><small>Offenlegung: Der Herausgeber steht in einer beruflichen Beziehung zu VDSina. Diese Website kann eine Provision erhalten, wenn Sie über diesen Partnerlink bestellen. Monitoring-Daten sollten die Dimensionierung bestimmen. Diese Seite behauptet nicht, dass VDSina die beschriebenen Monitoring-Werkzeuge als verwalteten Dienst bereitstellt.</small></p>

## Mehrere Websites auf zwei Ebenen überwachen {#monitor-multiple-websites-at-two-levels}

Überwachen Sie auf einem VPS mit mehreren Websites:

### Serverebene {#server-level}

- CPU/RAM/Swap;
- Datenträger/Inodes/I/O;
- Datenbank;
- Netzwerk;
- zentrale Dienste.

### Website-Ebene {#site-level}

- jeden wichtigen Hostnamen;
- TLS;
- Antwortzeit;
- 5xx-Fehler;
- Anwendungs-/Aufgabenfehler;
- Protokolle oder Worker-Engpässe pro Website, soweit verfügbar.

Ein Server kann gesund sein, obwohl ein einzelner virtueller Host, ein Zertifikat oder eine Website defekt ist.

Die Entscheidung über Zusammenlegung und gemeinsame Ausfallrisiken behandelt [VPS für mehrere Websites]({{< relref "vps-for-multiple-websites.md" >}}).

## VPS-Monitoring-Checkliste {#vps-monitoring-checklist}

| Signal | Erfolgskriterium |
|---|---|
| Externe Erreichbarkeit | wichtiger Hostname von außerhalb des VPS geprüft |
| HTTP-Zustand | erwarteter Status, Inhalt oder Zustandsendpunkt geprüft |
| CPU | Verlauf anhaltender Auslastung, Last und Prozessnutzung aufbewahrt |
| RAM | verfügbarer Speicher, Swap und OOM sichtbar |
| Datenträger | Kapazität und Wachstum überwacht |
| Inodes | Inode-Erschöpfung separat überwacht |
| I/O | Latenz und I/O-Wartezeit sichtbar, wenn Speicherleistung relevant ist |
| Netzwerk | Durchsatz, Fehler und Verbindungssymptome beobachtbar |
| Dienste | Zustand von Webserver, Laufzeit, Datenbank und Workern überwacht |
| Datenbank | anwendungsrelevante Verfügbarkeit, Latenz und Verbindungen sichtbar |
| Aufgaben | Fehler und Rückstände von Cronjobs, Warteschlangen und Hintergrundaufgaben erkennbar |
| TLS/DNS | Ablauf- und Auflösungsfehler erkennbar |
| Backups | Alter des letzten Erfolgs und Auftragsfehler überwacht |
| Protokolle | Web-, Anwendungs-, Datenbank- und Systemprotokolle für Vorfallanalyse verfügbar |
| Alarme | Warn-/Kritisch-Stufen sowie Dauer-/Entprellregeln eingerichtet |
| Benachrichtigung | wichtige Alarme verlassen die VPS-Ausfallumgebung |
| Verantwortung | benannte zuständige Person und Plan für erste Maßnahmen |
| Aufbewahrung | genügend Metrik-/Protokollhistorie für Trends und Ursachenanalyse |
| Sicherheit | Monitoring-Endpunkte und Dashboards nicht versehentlich öffentlich |
| Kapazität | Trends fließen in die nächste Optimierungs-/Skalierungsentscheidung ein |

## Technische Referenzen {#technical-references}

- Prometheus — Linux-Host-Metriken mit Node Exporter überwachen
- Prometheus — Alertmanager
- Uptime Kuma — offizielles Projekt
- [VPS-Backup-Strategie]({{< relref "vps-backup-strategy.md" >}})
- [VPS-Sicherheitscheckliste]({{< relref "vps-security-checklist.md" >}})

## FAQ {#faq}

### Was sollte ich auf einem VPS überwachen? {#what-should-i-monitor-on-a-vps}

Mindestens externe Website-Erreichbarkeit, CPU, verfügbaren RAM/Swap/OOM, Speicherplatz, Inodes, zentrale Dienste, Anwendungszustand, TLS-Ablauf, Backup-Aktualität und Alarmzustellung.

### Ist CPU-Auslastung über 80 % immer schlecht? {#is-cpu-over-80-always-bad}

Nein. Kurze CPU-Spitzen können normal sein. Untersuchen Sie anhaltende Auslastung zusammen mit Last, Anfragelatenz, Warteschlangen und dem ausführenden Prozess.

### Warum ist der Linux-RAM fast voll? {#why-is-linux-ram-almost-full}

Linux nutzt freien Speicher als Cache. Überwachen Sie verfügbaren Speicher, Swap-Aktivität, OOM-Ereignisse und Prozesswachstum, statt allein beim belegten Prozentwert zu alarmieren.

### Was sollte ich bei Datenträgerproblemen überwachen? {#what-should-i-monitor-for-disk-problems}

Überwachen Sie Dateisystemkapazität, Inode-Nutzung, Speicherwachstum sowie I/O-Latenz und -Wartezeit. Freie GB allein decken nicht alle Datenträger-Fehlerarten ab.

### Reicht Ping für Verfügbarkeitsmonitoring? {#is-ping-enough-for-uptime-monitoring}

Nein. Ping kann erfolgreich sein, während Website, Datenbank oder TLS-Verbindung defekt sind. Nutzen Sie HTTP(S) und Anwendungs-/Dienstprüfungen für den nutzerseitigen Zustand.

### Sollte der Verfügbarkeitsmonitor auf demselben VPS laufen? {#should-the-uptime-monitor-run-on-the-same-vps}

Nicht als einziger Monitor. Ein vollständiger VPS- oder Netzwerkausfall kann den Monitor zusammen mit der Website abschalten. Halten Sie mindestens den kritischen Verfügbarkeits- und Benachrichtigungsweg außerhalb dieser Ausfallumgebung.

### Welches VPS-Monitoring-Werkzeug ist am besten? {#which-vps-monitoring-tool-is-best}

Es gibt kein universell bestes Werkzeug. Ein einzelner VPS benötigt möglicherweise nur externe Erreichbarkeitsprüfungen und einen schlanken Host-Metrik-Agenten. Mehrere Server können Prometheus, Grafana und Alertmanager rechtfertigen. Wählen Sie anhand benötigter Transparenz, Aufbewahrung und Betriebskomplexität.

### Brauche ich Prometheus und Grafana für einen VPS? {#do-i-need-prometheus-and-grafana-for-one-vps}

Nicht zwingend. Sie sind leistungsfähig, wenn langfristige Metriken, eigene Abfragen und mehrere Server gebraucht werden. Ein schlanker Agent plus externes Verfügbarkeitsmonitoring kann für eine kleine Bereitstellung ausreichen.

### Wie sollte ich Backups überwachen? {#how-should-i-monitor-backups}

Alarmieren Sie bei fehlgeschlagenen Aufträgen und wenn das Alter des letzten erfolgreichen Backups die RPO überschreitet. Prüfen Sie die Wiederherstellbarkeit anschließend gesondert durch Wiederherstellungstests.

### Wann sollte Monitoring zu einem VPS-Upgrade führen? {#when-should-monitoring-trigger-a-vps-upgrade}

Wenn historische Daten zeigen, dass ein optimierter legitimer Workload wiederholt CPU, RAM, Speicher/I/O oder eine andere Ressource erschöpft. Eine einzelne Spitze ist kein ausreichender Beleg.
