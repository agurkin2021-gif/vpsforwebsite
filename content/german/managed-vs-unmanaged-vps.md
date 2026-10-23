---
title: "Managed VPS vs. Unmanaged VPS"
description: "Managed VPS vs. Unmanaged VPS: Zuständigkeiten für Updates, Sicherheit, Backups, Monitoring und Störungen vergleichen, tatsächliche Betriebskosten berechnen und das passende Verwaltungsmodell wählen."
image: "images/home/vps-for-website-hero.webp"
slug: "managed-vps-vs-unmanaged-vps"
---

Bei Managed VPS vs. Unmanaged VPS geht es vor allem darum, **wer den Server nach seiner Bereitstellung betreibt**. Die virtuelle Maschine kann in beiden Fällen dieselbe CPU, denselben RAM und dieselbe Festplatte haben. Was sich ändert, ist die Zuständigkeit für Betriebssystem, Sicherheit, Web-Stack, Backups, Monitoring, Fehlerbehebung und Wiederherstellung.

Für die übergreifende Kaufentscheidung lesen Sie [VPS für Websites]({{< relref "_index.md" >}}).

[Kurzantwort](#quick-answer) · [Verantwortungsmatrix](#responsibility-matrix) · [Verwaltungsmodell prüfen](#management-fit-checker) · [Tatsächliche Kosten](#compare-total-operating-cost-not-only-server-price) · [VDSina-Leistungsumfang](#how-the-vdsina-offer-fits-this-decision) · [FAQ](#faq)

## Kurzantwort {#quick-answer}

| Wahl | Besser geeignet, wenn | Hauptrisiko |
|---|---|---|
| **Unmanaged / selbst verwalteter VPS** | Sie oder Ihr Team Linux/Windows administrieren, das Betriebssystem aktualisieren, den Server absichern, Backups prüfen, Dienste überwachen und auf Störungen reagieren können | der niedrigere Serverpreis kann teuer werden, wenn niemand den Betrieb verantwortet |
| **Managed VPS** | ein Anbieter oder beauftragter Administrator festgelegte Verwaltungsaufgaben übernehmen soll und Ausfälle geschäftlich teuer sind | „Managed“ kann ungenau sein; ausgeschlossene Aufgaben bleiben möglicherweise bei Ihnen |
| **Unmanaged + bezahlte Administration** | Sie Root-Zugriff, Kontrolle und niedrigere Infrastrukturkosten wünschen, aber nicht jede Wartungs- oder Störungsaufgabe selbst übernehmen wollen | auch zwischen bezahlten Einsätzen brauchen Sie klare Zuständigkeiten und einen Reaktionsprozess |

Die wichtigste Kaufregel ist einfach: **Kaufen Sie nicht das Wort „Managed“, sondern eine schriftliche Aufgabenliste mit klaren Zuständigkeitsgrenzen.**

## „Managed“ hat keine einheitliche Bedeutung {#managed-does-not-have-one-standard-meaning}

„Managed VPS“ ist keine allgemeingültige technische Spezifikation. Anbieter können damit sehr unterschiedliche Leistungsumfänge bezeichnen.

Ein Managed-Tarif enthält möglicherweise Betriebssystem-Updates, Firewall-Verwaltung, Monitoring und Wiederherstellungen. Ein anderer umfasst nur ein Panel, Einrichtungshilfe und Support-Tickets. Arbeiten auf Anwendungsebene – WordPress-Plugins, eigener Code, Datenbankabfragen, APIs oder Geschäftslogik – können weiterhin ausgeschlossen sein.

Klären Sie vor dem Preisvergleich:

- was der Anbieter proaktiv überwacht;
- was er automatisch oder auf Anfrage aktualisiert;
- welche Backup-Aufträge eingerichtet werden;
- ob Wiederherstellungstests und die eigentliche Wiederherstellung enthalten sind;
- welche Dienste abgedeckt sind: Nginx/Apache, PHP, Datenbank, E-Mail, Redis, Docker usw.;
- ob Fehlerbehebung an Anwendungen enthalten ist;
- ob Notfalleinsätze rund um die Uhr oder nur zu Geschäftszeiten erfolgen;
- welche Reaktionszeit und welcher Eskalationsweg vorgesehen sind;
- welche Änderungen die Verwaltungsleistungen einschränken oder ausschließen können;
- ob Root-Zugriff erlaubt ist und welche Folgen eigene Änderungen haben.

Ein Managed VPS ist nur dann wertvoll, wenn der schriftliche Leistungsumfang die tatsächlich benötigten Aufgaben abdeckt.

## Leistungsversprechen vor dem Kauf entschlüsseln {#decode-management-claims-before-paying}

Betrachten Sie Werbeaussagen als Anlass für Nachfragen, nicht als Nachweis einer übernommenen Zuständigkeit.

| Aussage auf der Tarifseite | Was Sie zusätzlich schriftlich brauchen |
|---|---|
| **24/7-Support** | ob jemand Ihren Server proaktiv überwacht, bei welchen Vorfällen ohne Ticket gehandelt wird und ob Arbeiten am Gastbetriebssystem oder an Anwendungen enthalten sind |
| **Fully Managed** | genaue Aufgaben für Betriebssystem, Firewall, Web-Stack, Datenbank, Backups, Monitoring und Störungen; unterstützte Software; Ausschlüsse |
| **Backups inklusive** | Häufigkeit, Aufbewahrung, Speicherort außerhalb des Servers, Überwachung fehlgeschlagener Jobs, Wiederherstellungstests und Zuständigkeit für Wiederherstellungen |
| **Monitoring inklusive** | überwachte Komponenten, Schwellenwerte, Alarmempfänger, Handlungsbefugnisse und Reaktion außerhalb der Geschäftszeiten |
| **Sicherheit wird verwaltet** | Update-Rhythmus, Firewall-Zuständigkeit, SSH/RDP-Richtlinien, Umgang mit verwundbaren Paketen und Reaktion auf Kompromittierungen |
| **Migration inklusive** | Dateien, Datenbank, DNS, E-Mail, letzte Schreibvorgänge, Rollback und Abdeckung anwendungsspezifischer Arbeiten |
| **Control Panel inklusive** | zunächst nur Panel/Lizenz; klären Sie separat die Zuständigkeit für Betriebssystem-Patches, Wiederherstellung, Monitoring und Störungen |

Kann ein Anbieter ein Schlagwort nicht in konkrete Zuständigkeiten übersetzen, rechnen Sie beim Tarifvergleich damit, dass die unklaren Aufgaben weiterhin bei Ihnen liegen.

## Verantwortungsmatrix {#responsibility-matrix}

Nutzen Sie diese Matrix als Ausgangspunkt und ersetzen Sie anschließend die Spalte „Managed“ durch den tatsächlichen schriftlichen Leistungsumfang des Anbieters.

| Aufgabe | Unmanaged VPS | Managed VPS |
|---|---|---|
| Physische Hardware, Strom, Netzwerk, Hypervisor | Anbieter | Anbieter |
| VPS-Bereitstellung / Betriebssystem-Image | Anbieter stellt meist Bereitstellungswerkzeuge | Anbieter, oft mit Einrichtungshilfe |
| Betriebssystem-Updates und Sicherheitspatches | **Sie** | Anbieter **nur, wenn enthalten** |
| Firewall-/SSH-/RDP-Absicherung | **Sie** | Anbieter **nur, wenn enthalten** |
| Webserver- und Laufzeitkonfiguration | **Sie** | für unterstützte Stacks eventuell enthalten |
| Datenbankadministration | **Sie** | eventuell teilweise enthalten; Grenzen prüfen |
| TLS-Zertifikate / Erneuerung | **Sie oder Ihre Automatisierung/Ihr Panel** | eventuell enthalten |
| Konfiguration von Backup-Aufträgen | **Sie** | eventuell enthalten |
| Wiederherstellungstests | **Sie** | häufig eine separate Zuständigkeit – prüfen |
| Monitoring / Alarme | **Sie** | eventuell enthalten |
| Reaktion auf einen Ausfall | **Sie / Ihr Administrator** | Anbieter nur innerhalb des Verwaltungsumfangs |
| WordPress-/Plugin-/Code-Probleme | **Sie / Entwickler** | häufig ausgeschlossen oder eingeschränkt |
| Dimensionierung und Skalierungsentscheidungen | **Sie** | oft gemeinsame Entscheidung; prüfen |
| DNS / E-Mail / Drittanbieter-Integrationen | **Sie, sofern nicht ausdrücklich abgedeckt** | Umfang sehr unterschiedlich |

Nennt ein Anbieter für eine Aufgabe keinen Verantwortlichen, gilt sie bis zur Bestätigung als nicht zuverlässig delegiert.

## Passendes Verwaltungsmodell prüfen {#management-fit-checker}

Dieses Werkzeug bewertet nicht Ihre technischen Fähigkeiten. Es prüft, ob die betrieblichen Aufgaben tatsächlich einen Verantwortlichen haben.

<div class="rounded-2xl bg-light p-6 dark:bg-darkmode-light">
<form id="management-fit-checker-form">
  <div class="mb-6">
    <label for="mg-skill" class="form-label">Erfahrung mit der Administration von Linux-/Windows-Servern</label>
    <select id="mg-skill" class="form-input">
      <option value="none">Wenig oder keine</option>
      <option value="basic">Grundkenntnisse in SSH/RDP und Panel-Nutzung</option>
      <option value="confident">Sicher in der Administration produktiver Server</option>
    </select>
  </div>
  <div class="mb-6">
    <label for="mg-patching" class="form-label">Eine benannte Person verantwortet Betriebssystem- und Sicherheitspatches</label>
    <select id="mg-patching" class="form-input"><option value="no">Nein</option><option value="yes">Ja</option></select>
  </div>
  <div class="mb-6">
    <label for="mg-backup" class="form-label">Eine benannte Person verantwortet Backups und Wiederherstellungstests</label>
    <select id="mg-backup" class="form-input"><option value="no">Nein</option><option value="yes">Ja</option></select>
  </div>
  <div class="mb-6">
    <label for="mg-monitor" class="form-label">Monitoring und Alarme sind eingerichtet und jemand reagiert darauf</label>
    <select id="mg-monitor" class="form-input"><option value="no">Nein</option><option value="yes">Ja</option></select>
  </div>
  <div class="mb-6">
    <label for="mg-incident" class="form-label">Jemand kann einen dringenden Servervorfall bearbeiten</label>
    <select id="mg-incident" class="form-input"><option value="no">Nein</option><option value="yes">Ja</option></select>
  </div>
  <div class="mb-6">
    <label for="mg-critical" class="form-label">Wie teuer sind Ausfälle dieser Website?</label>
    <select id="mg-critical" class="form-input">
      <option value="low">Geringe Kosten – Test/Hobby/unkritisch</option>
      <option value="medium">Mittlere Kosten – Unternehmenswebsite</option>
      <option value="high">Hohe Kosten – Umsatz/Betrieb hängen davon ab</option>
    </select>
  </div>
  <div class="mb-6">
    <label for="mg-custom" class="form-label">Brauchen Sie Root-Zugriff oder einen individuellen/nicht unterstützten Stack?</label>
    <select id="mg-custom" class="form-input"><option value="no">Nein</option><option value="yes">Ja</option></select>
  </div>
  <div class="mb-6">
    <label for="mg-adminhelp" class="form-label">Können Sie bei Bedarf Serveradministration beauftragen oder dauerhaft engagieren?</label>
    <select id="mg-adminhelp" class="form-input"><option value="no">Nein</option><option value="yes">Ja</option></select>
  </div>
  <button class="btn btn-primary" type="submit">Verwaltungsmodell prüfen</button>
</form>
<p id="management-fit-result" class="mt-6 rounded border border-border p-4 dark:border-darkmode-border" role="status" aria-live="polite">Antworten Sie danach, wer die Aufgaben tatsächlich ausführen wird.</p>
</div>

<script>
document.addEventListener("DOMContentLoaded", function () {
  var form = document.getElementById("management-fit-checker-form");
  if (!form) return;

  form.addEventListener("submit", function (event) {
    event.preventDefault();

    function val(id) {
      return document.getElementById(id).value;
    }

    var skill = val("mg-skill");
    var patching = val("mg-patching") === "yes";
    var backup = val("mg-backup") === "yes";
    var monitor = val("mg-monitor") === "yes";
    var incident = val("mg-incident") === "yes";
    var critical = val("mg-critical");
    var custom = val("mg-custom") === "yes";
    var adminHelp = val("mg-adminhelp") === "yes";

    var opsReady = patching && backup && monitor && incident;
    var result;

    if (skill === "confident" && opsReady) {
      result = "UNMANAGED PASST: Die zentralen Betriebsaufgaben haben einen Verantwortlichen. Behalten Sie schriftliche Betriebsanleitungen, Wiederherstellungstests und Monitoring bei; Unmanaged bedeutet weiterhin, dass Ihr Team den Produktivbetrieb verantwortet.";
    } else if (custom && adminHelp) {
      result = "UNMANAGED + ADMINISTRATIONSHILFE PASST: Sie benötigen Kontrolle und individuelle Anpassungen, einige Betriebsaufgaben sind intern jedoch nicht abgedeckt. Betreiben Sie den VPS nur dann selbst verwaltet, wenn der Leistungsumfang der bezahlten Administration/Bereitschaft die fehlenden Aufgaben ausdrücklich abdeckt; bei geschäftskritischen Lasten gehören Monitoring und Störungsreaktion dazu.";
    } else if (critical === "low" && skill !== "none" && adminHelp) {
      result = "LERN- / HYBRIDMODELL PASST: Für eine unkritische Anwendung kann Unmanaged sinnvoll sein, wenn Sie bewusst externe Administrationshilfe nutzen und den Server erst als produktionsbereit ansehen, sobald Patches, Backups, Monitoring und Störungsreaktion feste Verantwortliche haben.";
    } else {
      result = "MANAGED PASST: Wichtige Betriebsaufgaben haben derzeit keinen Verantwortlichen. Wählen Sie einen Managed-Service mit schriftlichem Leistungsumfang oder organisieren Sie eine gleichwertige Administration, bevor Sie eine geschäftskritische Website auf einem Unmanaged VPS betreiben.";
    }

    document.getElementById("management-fit-result").textContent = result;
  });
});
</script>

## Was ein Unmanaged VPS tatsächlich erfordert {#what-unmanaged-vps-really-requires}

Unmanaged bedeutet nicht „schlechter Support“. Es bedeutet, dass der Anbieter die Infrastruktur bereitstellt, während die Serveradministration bei Ihnen bleibt, sofern nichts anderes vereinbart wurde.

Bei einer produktiven Website muss jemand folgende Aufgaben verantworten:

- grundlegende Absicherung;
- SSH/RDP-Zugriff und Kontosicherheit;
- Betriebssystem-/Kernel-/Paket-Updates;
- Firewall und öffentlich erreichbare Dienste;
- Konfiguration von Webserver, PHP/Node/Python und Datenbank;
- TLS-Erneuerung;
- Protokollprüfung;
- Reaktion auf Schadsoftware/Missbrauch, soweit relevant;
- Überwachung des freien Speicherplatzes;
- CPU-/RAM-/Datenbank-Monitoring;
- Backup-Zeitpläne;
- Wiederherstellungstests;
- Störungsdiagnose;
- Wiederherstellung nach fehlgeschlagenen Updates oder Konfigurationsänderungen;
- Koordination von Anwendungsbereitstellungen.

Kann niemand die verantwortliche Person für diese Aufgaben nennen, ist der Server nicht wirklich „selbst verwaltet“, sondern schlicht **unverwaltet und ohne Betreiber**.

### Warnzeichen: Unmanaged passt schlecht zum Produktivbetrieb {#red-flags-unmanaged-is-a-poor-production-fit}

Betreiben Sie eine geschäftskritische Website noch nicht auf einem Unmanaged VPS, wenn mehrere dieser Punkte zutreffen:

- niemand verantwortet Betriebssystem- und Sicherheitspatches;
- Backups sind geplant, Wiederherstellungen wurden aber nie getestet;
- niemand beachtet Alarme zu Festplatte, CPU, Arbeitsspeicher, Datenbank oder Erreichbarkeit;
- niemand kann außerhalb der üblichen Arbeitszeiten auf eine Störung reagieren;
- nur ein Entwickler kennt den Server und es gibt keine Betriebsanleitung;
- das Team erwartet vom Anbietersupport die Behebung von Gastbetriebssystem-/Anwendungsproblemen außerhalb des Supportumfangs;
- ein Ausfall würde Verkäufe, Kundenzugänge oder Geschäftsabläufe stoppen.

Die Lösung muss nicht „Managed Hosting kaufen“ heißen. Entscheidend ist, jeder Betriebsaufgabe einen benannten Verantwortlichen zuzuweisen – Ihrem Team, einem Managed-Anbieter oder einer beauftragten Administration.

Für die Ressourcenauswahl nutzen Sie [VPS für Websites dimensionieren]({{< relref "vps-sizing-for-website.md" >}}).

## Was ein Managed VPS abdecken sollte {#what-managed-vps-should-cover}

Ein sinnvoller Managed-Service verringert die Betriebsarbeit, doch seine genauen Grenzen müssen ausdrücklich feststehen.

Verlangen Sie schriftliche Antworten auf diese Fragen:

- Wird der Server proaktiv überwacht?
- Werden Betriebssystem- und Sicherheitsupdates geplant und angewendet?
- Sind Firewall-Verwaltung und Absicherung enthalten?
- Welche Web-/Datenbank-Stacks werden unterstützt?
- Sind Backup-Aufträge enthalten?
- Wer testet Wiederherstellungen?
- Wer führt während einer Störung die Wiederherstellung durch?
- Werden Dienstausfälle automatisch untersucht oder erst nach einem Ticket?
- Ist Fehlerbehebung auf Anwendungsebene enthalten?
- Sind WordPress-/Plugin-Probleme abgedeckt?
- Sind Datenbank-Leistungsprobleme abgedeckt?
- Werden eigene Pakete, Docker und individuelle Dienste unterstützt?
- Welche Reaktionsziele gelten?
- Sind Störungseinsätze außerhalb der Geschäftszeiten enthalten?
- Ist eine Migration enthalten?
- Welche Arbeiten werden zusätzlich berechnet?

Leiten Sie diese Antworten nicht aus „Fully Managed“, „24/7-Support“ oder dem Vorhandensein eines Control Panels ab.

## Ein Control Panel ist keine Verwaltungsleistung {#control-panel-is-not-management}

Ein Control Panel kann Routineaufgaben erleichtern:

- Domains und virtuelle Hosts;
- TLS-Zertifikate;
- PHP-Versionen;
- Datenbanken;
- Benutzer;
- Postfächer;
- Dateiverwaltung;
- geplante Aufgaben.

Ein Panel übernimmt jedoch nicht automatisch:

- die Entscheidung, wann das Betriebssystem aktualisiert werden muss;
- Tests der Wiederherstellung aus Backups;
- die Untersuchung einer vollgelaufenen Festplatte;
- die Korrektur einer fehlerhaften Datenbankabfrage;
- die Reaktion auf kompromittierte Zugangsdaten;
- die Überwachung der Website um 3 Uhr morgens;
- die Wiederherstellung nach einer fehlgeschlagenen Bereitstellung.

Ein Panel ist ein Werkzeug. Verwaltung ist eine **Dienstleistung mit Zuständigkeit und Reaktion**.

Für die panelgestützte Administration lesen Sie [VPS mit Control Panel]({{< relref "vps-with-control-panel.md" >}}).

## Support ist keine Serveradministration {#support-is-not-server-administration}

Technischer Support und Serververwaltung überschneiden sich nur dort, wo der schriftliche Leistungsumfang des Anbieters das vorsieht.

Infrastruktursupport kann sinnvoll unterstützen bei:

- einer virtuellen Maschine, die nicht startet;
- Problemen mit der Netzwerkerreichbarkeit;
- Plattform-/Control-Panel-Problemen;
- Speicher- oder Virtualisierungsproblemen;
- Vorfällen auf Anbieterseite.

Serveradministration kann Folgendes umfassen:

- Aktualisieren des Gastbetriebssystems;
- Konfigurieren von Nginx/Apache;
- Reparieren von PHP-/Datenbankdiensten;
- Absichern von SSH und Firewall;
- Untersuchen von Protokollen;
- Wiederherstellen von Backups;
- Fehlerbehebung an individueller Software.

Das sind unterschiedliche Verantwortungsbereiche.

Diese Unterscheidung ist beim hier genannten Anbieter wichtig: VDSina bewirbt auf seiner Standard-Seite **technischen Support rund um die Uhr**, während die öffentlichen Fragen und Antworten die **Serveradministration als zusätzlich bestellbare Leistung** beschreiben. Setzen Sie deshalb „24/7-Support“ nicht mit „Fully Managed VPS“ gleich. Diese Anbieterseiten wurden am 13. Oktober 2026 erneut geprüft; verifizieren Sie den aktuellen Administrationsumfang und die Vertragsbedingungen, bevor Sie sich darauf verlassen.

## Gesamte Betriebskosten statt nur Serverpreis vergleichen {#compare-total-operating-cost-not-only-server-price}

Die tatsächlichen VPS-Kosten gehen über die Serverrechnung hinaus.

Rechnen Sie mit:

**Gesamte Betriebskosten = VPS + Panel/Lizenzen + Backups + Monitoring + Administrationszeit + bezahlter Support/Administrationsarbeiten + Störungs-/Wiederherstellungskosten**

Ein Unmanaged VPS kann die günstigste Wahl sein, wenn Serveradministration ohnehin zu den Aufgaben Ihres Teams gehört.

Er kann teuer werden, wenn:

- ein Entwickler produktive Arbeitsstunden mit Serverroutine verliert;
- Sicherheitsupdates aufgeschoben werden;
- Backups existieren, Wiederherstellungen aber fehlschlagen;
- niemand Engpässe bei Festplatte oder Datenbank bemerkt;
- ein Ausfall warten muss, bis die einzige technische Fachkraft aufwacht;
- sich ein Notfall-Dienstleister erst während der Störung in den Server einarbeiten muss.

Ein Managed-Service ist ebenfalls nicht automatisch günstiger. Wenn Sie bereits kompetentes Betriebspersonal haben und einen individuellen Stack benötigen, kann eine begrenzte externe Verwaltung zusätzliche Kosten verursachen, ohne nennenswert Arbeit abzunehmen.

Bewerten Sie die **Verantwortung**, nicht nur CPU und RAM.

Eine einfache Vergleichstabelle:

| Kosten- / Risikoposten | Unmanaged | Managed / beauftragte Administration |
|---|---|---|
| VPS-Infrastruktur | monatlicher Serverpreis | monatlicher Serverpreis |
| Panel / Lizenzen | bei Nutzung hinzurechnen | eventuell enthalten |
| Backup-Speicher / Werkzeuge | bei Nutzung hinzurechnen | prüfen, ob enthalten |
| Monitoring | eigene Werkzeuge/eigene Zeit | prüfen, ob enthalten |
| Regelmäßige Administration | Arbeitszeit Ihres Personals | Verwaltungs-/Administrationsgebühr |
| Störungen außerhalb der Geschäftszeiten | eigene Bereitschaftskosten / Verzögerungsrisiko | Abdeckung und Ausschlüsse prüfen |
| Wiederherstellungsarbeiten | Ihre Verantwortung | prüfen, ob die Ausführung enthalten ist |
| Fehlerbehebung an Anwendungen | Entwickler-/Administrationskosten | häufig weiterhin Kunden-/Entwickleraufgabe |

Die richtige Vergleichsfrage lautet nicht „Welche Monatsrechnung ist niedriger?“, sondern „Welches Modell gibt jeder erforderlichen Betriebsaufgabe einen Verantwortlichen bei akzeptablen Gesamtkosten und Risiken?“

## Sicherheit, Backups und Störungsreaktion {#security-backups-and-incident-response}

Diese drei Bereiche zeigen, ob das Verwaltungsmodell tatsächlich trägt.

### Sicherheit {#security}

Fragen Sie nach der Zuständigkeit für:

- Sicherheitsupdates;
- Firewall-Änderungen;
- SSH/RDP-Richtlinien;
- verwundbare Pakete;
- Untersuchungen von Schadsoftware oder Kompromittierungen;
- den Wechsel von Zugangsdaten.

Für eine konkrete Absicherungsgrundlage nutzen Sie die [VPS-Sicherheitscheckliste]({{< relref "vps-security-checklist.md" >}}).

### Backups {#backups}

Klären Sie einzeln:

- wer Backup-Aufträge erstellt;
- wo die Kopien gespeichert werden;
- wer fehlgeschlagene Aufträge überwacht;
- wer die Wiederherstellbarkeit testet;
- wer eine Wiederherstellung durchführt;
- wie aktuell die wiederhergestellten Daten sein werden.

„Backups inklusive“ beantwortet nicht alle sechs Fragen. Zu RPO/RTO, Aufbewahrung, externen Kopien und Wiederherstellungsarchitektur lesen Sie [VPS-Backup-Strategie]({{< relref "vps-backup-strategy.md" >}}).

### Störungsreaktion {#incident-response}

Legen Sie fest:

- was einen Alarm auslöst;
- wer ihn erhält;
- wer handeln darf;
- was außerhalb der Geschäftszeiten geschieht;
- was zur Anbieterinfrastruktur gehört und was zu Ihrem Gastbetriebssystem oder Ihrer Anwendung;
- welcher Eskalationsweg gilt.

Für Migrations- und Rollback-Planung lesen Sie [Website auf einen VPS umziehen]({{< relref "website-migration-to-vps.md" >}}).

## Root-Zugriff und Änderungskontrolle {#root-access-and-change-control}

Ein Unmanaged VPS bietet in der Regel maximale Freiheit: Root-/Administratorzugriff, eigene Pakete, eigene Firewall-Regeln und nicht unterstützte Dienste liegen in Ihrer Entscheidung.

Auch ein Managed VPS kann Root-Zugriff bieten, die Verwaltung kann jedoch Grenzen haben. Ein Anbieter kann die Verantwortung für Probleme ablehnen, die durch nicht unterstützte Pakete oder manuelle Änderungen entstanden sind.

Fragen Sie vor der Wahl eines Managed-Angebots:

- Behalte ich Root-/Administratorzugriff?
- Welche Änderungen werden unterstützt?
- Müssen Änderungen über den Support laufen?
- Darf der Anbieter nicht unterstützte Konfigurationen zurücksetzen?
- Verändert die Installation von Docker, eigenen Kerneln oder Drittanbieter-Panels den Verwaltungsumfang?
- Wer dokumentiert Änderungen?

Wenn uneingeschränkte Kontrolle unverzichtbar ist, kann Unmanaged mit kompetenter Administration besser passen als ein Managed-Tarif mit eng begrenztem unterstütztem Stack.

## Der Mittelweg: Unmanaged plus bezahlte Administration {#the-middle-ground-unmanaged-plus-paid-admin}

Die Auswahl beschränkt sich nicht auf „alles selbst machen“ oder „Fully Managed Hosting kaufen“.

Ein praktikabler Mittelweg ist:

- ein Unmanaged VPS;
- ein Control Panel, wo es sinnvoll ist;
- automatisiertes Monitoring;
- unabhängige Backups;
- ein dokumentierter Wiederherstellungsablauf;
- ein bezahlter oder bei Bedarf verfügbarer Administrator;
- ein Eskalationskontakt für Störungen.

Das funktioniert, wenn der laufende Betrieb beherrscht wird, Sie aber für Migrationen, Absicherung, Ausfälle oder komplexe Änderungen fachkundige Hilfe möchten.

Es scheitert, wenn niemand den Server überwacht und der Administrator erst nach einem langen Ausfall kontaktiert wird. Auch ein Hybridmodell braucht einen benannten Betriebsverantwortlichen.

## Wie das VDSina-Angebot in diese Entscheidung passt {#how-the-vdsina-offer-fits-this-decision}

Der hier verlinkte VDSina VPS sollte als Infrastrukturangebot zur Selbstverwaltung bewertet werden, sofern Sie keinen separaten Umfang für Serveradministration vereinbaren.

Die öffentlichen Anbieterinformationen nennen derzeit:

- technischen Support rund um die Uhr bei Standard VPS;
- Serversteuerungswerkzeuge und API;
- eine Funktion für Backup-Images;
- einen separaten Eintrag in den Fragen und Antworten, der die Administration von Kundenservern als zusätzlich bestellbare Leistung beschreibt.

Diese Kombination ist nützlich, entspricht aber **nicht der Zusage eines Fully Managed VPS**.

Entscheiden Sie bei diesem Weg vor dem Kauf, wer Betriebssystem-Updates, Absicherung, Monitoring, Wiederherstellungstests und Störungen verantwortet.

<p>
  <a class="btn btn-primary" href="https://www.vdsina.com/?partner=ni8gzrvz75" target="_blank" rel="sponsored nofollow noopener">Aktuelle VPS-Konfigurationen prüfen</a>
</p>
<p><small>Offenlegung: Der Herausgeber steht in einer beruflichen Beziehung zu VDSina. Diese Website kann eine Provision erhalten, wenn Sie über diesen Partnerlink bestellen. Diese Seite stellt den VPS nicht als Managed Hosting dar; prüfen Sie vor der Bestellung den aktuellen Support- und Administrationsumfang beim Anbieter.</small></p>

### Anbieterreferenzen {#provider-references}

- VDSina Standard VPS – aktuelle Tarifmerkmale und technischer Support
- VDSina QA – Serveradministration und Website-Umzugsservice

## Fragen vor dem Kauf eines Managed VPS {#questions-to-ask-before-paying-for-managed-vps}

Akzeptieren Sie kein Werbeschlagwort als Leistungsumfang. Lassen Sie diese Fragen beantworten:

1. Welche konkreten Aufgaben werden proaktiv ohne Support-Ticket erledigt?
2. Welche Betriebssysteme und Software-Stacks werden unterstützt?
3. Wer spielt Sicherheitsupdates ein und wie schnell?
4. Welches Monitoring ist enthalten?
5. Sind Backup-Aufträge enthalten?
6. Sind Wiederherstellungstests enthalten?
7. Wer führt Notfall-Wiederherstellungen durch?
8. Welche Vorfälle werden rund um die Uhr bearbeitet?
9. Welche Reaktionsziele gibt es?
10. Ist die Datenbank abgedeckt?
11. Sind WordPress-/Anwendungs-/Plugin-Probleme abgedeckt?
12. Ist E-Mail-Administration enthalten?
13. Ist die Migration enthalten?
14. Behalte ich Root-/Administratorzugriff?
15. Welche individuellen Änderungen werden nicht unterstützt?
16. Welche Aufgaben werden separat berechnet?

Kann der Anbieter das nicht klar beantworten, bewerten Sie den Tarif so, als blieben die unklaren Aufgaben bei Ihnen.

## Nach Lastprofil und Geschäftsrisiko wählen {#choose-by-workload-and-business-risk}

### Test-, Staging- oder Hobbyserver {#test-staging-or-hobby-server}

Unmanaged ist sinnvoll, wenn ein Ausfall geringe geschäftliche Folgen hat und die Umgebung auch dazu dient, den Serverbetrieb zu lernen.

### Unternehmenswebsite {#business-website}

Unmanaged kann gut funktionieren, wenn eine kompetente Person Patches, Backups, Monitoring und Störungen verantwortet. Andernfalls verringern Managed-Service oder bezahlte Administration das Betriebsrisiko.

### WooCommerce, Mitglieder- oder transaktionsbasierte Website {#woocommerce-membership-or-transactional-website}

Die Kosten eines versäumten Patches, einer fehlgeschlagenen Wiederherstellung oder eines langen Ausfalls können den monatlichen Preisunterschied schnell übersteigen. Betreibt das Team noch keine Server, ist ein klar definierter Verwaltungs-/Administrationsservice sinnvoller als die Hoffnung, der Support werde den Anwendungsbetrieb übernehmen.

### Mehrere Kundenwebsites {#multiple-client-websites}

Klären Sie, wer Störungen über alle Websites hinweg verantwortet und ob ein Serverausfall mehrere Kunden betrifft. Eine Agentur mit Systemadministration bevorzugt möglicherweise Unmanaged-Kontrolle; eine Agentur ohne Betriebspersonal braucht ein belastbares Verwaltungs- und Eskalationsmodell.

### Individuelle Anwendung / ungewöhnlicher Stack {#custom-application--unusual-stack}

Unmanaged bietet häufig mehr Freiheit, aber nur, wenn das Team die installierte Software auch betreiben kann. Ein Managed-Tarif kann nicht unterstützte Laufzeitumgebungen, Container oder individuelle Dienste ausschließen.

## FAQ {#faq}

### Ist Unmanaged VPS dasselbe wie selbst verwalteter VPS? {#is-unmanaged-vps-the-same-as-self-managed-vps}

In der Regel ja. Beide Begriffe bedeuten, dass der Kunde den Großteil der Administration innerhalb der virtuellen Maschine verantwortet, sofern keine separate Leistung etwas anderes vorsieht.

### Enthält ein Unmanaged VPS technischen Support? {#does-unmanaged-vps-include-technical-support}

Das ist möglich. Infrastruktur- und Kontosupport können weiterhin verfügbar sein. Technischer Support übernimmt jedoch nicht automatisch die Verantwortung für Betriebssystem, Sicherheit, Backups, Web-Stack oder Anwendung.

### Macht ein Control Panel einen VPS zu einem Managed VPS? {#does-a-control-panel-make-a-vps-managed}

Nein. Ein Panel erleichtert viele Aufgaben, doch Updates, Sicherheit, Backups, Monitoring und Störungsreaktion brauchen weiterhin einen Verantwortlichen.

### Ist ein Managed VPS sicherer? {#is-managed-vps-more-secure}

Nicht automatisch. Kompetente Administratoren, die den Server tatsächlich aktualisieren, absichern und überwachen, können das Betriebsrisiko verringern. Sicherheit hängt vom tatsächlichen Leistungsumfang und seiner Umsetzung ab, nicht von der Bezeichnung.

### Ist ein Managed VPS immer teurer? {#is-managed-vps-always-more-expensive}

Die Monatsrechnung ist meist höher, die gesamten Betriebskosten können jedoch niedriger sein, wenn wertvolle Administrationszeit eingespart oder teure Vorfälle verhindert werden. Vergleichen Sie Zeit, Werkzeuge, Backup-/Monitoring-Kosten und Wiederherstellungsrisiken.

### Kann ich auf einem Managed VPS Root-Zugriff nutzen? {#can-i-use-root-access-on-a-managed-vps}

Manchmal. Die Regeln unterscheiden sich. Fragen Sie, ob Root-/Administratorzugriff erhalten bleibt und ob eigene Änderungen die Verwaltungsverantwortung des Anbieters einschränken oder aufheben.

### Für wen eignet sich ein Unmanaged VPS? {#who-should-choose-unmanaged-vps}

Für Nutzer oder Teams, die Serverupdates, Absicherung, Backups, Wiederherstellungstests, Monitoring und Störungen zuverlässig verantworten können und vollständige Kontrolle über den Stack schätzen.

### Für wen eignet sich ein Managed VPS? {#who-should-choose-managed-vps}

Für Teams, die einen definierten Betriebsservice benötigen, weil ihnen Zeit, Fachkenntnisse oder Bereitschaftskapazitäten fehlen, um einen produktiven Server selbst zu betreiben.

### Ist 24/7-Support dasselbe wie ein Managed VPS? {#is-247-support-the-same-as-managed-vps}

Nein. Ein Anbieter kann technischen Support rund um die Uhr anbieten und Serveradministration trotzdem als separate Leistung behandeln. Lesen Sie den schriftlichen Leistungsumfang.
