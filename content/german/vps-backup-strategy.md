---
title: "VPS-Backup-Strategie"
slug: "vps-backup-strategie"
description: "VPS-Backup-Strategie: RPO und RTO festlegen, Anbieter-Images mit unabhängigen externen Backups kombinieren, Datenbanken und Geheimnisse schützen, Aufbewahrung planen und Wiederherstellung testen."
image: "images/home/vps-for-website-hero.webp"
---

Eine VPS-Backup-Strategie bedeutet nicht „einmal täglich Snapshots einschalten“. Ein brauchbarer Wiederherstellungsplan legt fest, **wie viel Datenverlust akzeptabel ist (RPO), wie lange die Wiederherstellung dauern darf (RTO), welche Daten erhalten bleiben müssen, wo unabhängige Kopien liegen, wie lange Versionen aufbewahrt werden und ob sie tatsächlich schon wiederhergestellt wurden**.

Ein solider Plan für VPS kombiniert gewöhnlich schnelle Wiederherstellung beim Anbieter mit einer unabhängigen Kopie außerhalb des Servers und anwendungsbewussten Datenbank-Backups. Die genaue Kombination hängt davon ab, wie schnell sich Daten ändern und wie teuer Ausfallzeiten sind.

Auch die Backup-Strategie braucht einen benannten Verantwortlichen. Wenn niemand fehlgeschlagene Aufträge, Wiederherstellungstests und Wiederherstellungsentscheidungen verantwortet, klären Sie zuerst dieses Betriebsmodell: siehe [Managed vs. Unmanaged VPS]({{< relref "managed-vs-unmanaged-vps.md" >}}).

Die grundsätzliche Serverentscheidung behandelt [VPS für Websites]({{< relref "_index.md" >}}).

[Kurzantwort](#quick-answer) · [Check](#vps-backup-strategy-checker) · [RPO / RTO](#start-with-rpo-and-rto) · [Backup-Ebenen](#snapshot-image-file-backup-and-replication-are-different) · [3-2-1](#a-practical-3-2-1-model-for-vps) · [Wiederherstellungstests](#test-restores-and-measure-real-rto) · [VDSina](#how-vdsina-backups-fit-the-strategy) · [FAQ](#faq)

## Kurzantwort {#quick-answer}

Ein praktisches Wiederherstellungskonzept für VPS umfasst mehrere Ebenen:

| Ebene | Hauptaufgabe | Was sie nicht belegt |
|---|---|---|
| **Backup-Image / Snapshot des Anbieters** | schnelles Zurücksetzen oder Neuaufbauen des gesamten Servers | unabhängige Wiederherstellung, wenn Anbieterkonto oder -speicher nicht verfügbar sind |
| **Datenbankkonsistentes Backup** | Anwendungszustand und jüngste Schreibvorgänge wiederherstellen | vollständige Serverkonfiguration allein durch dieses Backup |
| **Datei-/Konfigurationsbackup** | Uploads, Konfigurationen, Anwendungsdaten und ausgewählte Dateien wiederherstellen | schnelle Wiederherstellung des gesamten Servers |
| **Unabhängige externe Kopie** | Ausfall des primären Anbieters, Kontos oder Servers überstehen | niedrige RTO ohne eingeübte Wiederherstellung |
| **Wiederherstellungsübung** | nachweisen, dass Kopien, Schlüssel und Ablaufplan tatsächlich funktionieren | dass auch zukünftige Backups ohne Überwachung weiter funktionieren |

Für viele gewöhnliche Website-VPS ist ein guter Ausgangspunkt:

- Anbieter-Image/Snapshot für schnelles Zurücksetzen;
- verschlüsseltes unabhängiges Backup von Dateien, Konfiguration und Datenbank in einer anderen Ausfallumgebung;
- mehrere Wiederherstellungspunkte;
- Datenbank-Backup-Häufigkeit nach akzeptablem Datenverlust;
- regelmäßige Wiederherstellungstests.

Das ist hilfreicher, als sich auf einen einzelnen Status „Backup erfolgreich“ zu verlassen.

## VPS-Backup-Strategie prüfen {#vps-backup-strategy-checker}

Dieser Check bestimmt die benötigte Wiederherstellungsarchitektur. Er garantiert keine erfolgreiche Wiederherstellung.

<div class="rounded-2xl bg-light p-6 dark:bg-darkmode-light">
<form id="vps-backup-strategy-checker-form">
  <div class="mb-6">
    <label for="bk-workload" class="form-label">Workload-Typ</label>
    <select id="bk-workload" class="form-input">
      <option value="static">Statische Website / Unternehmenspräsentation / seltene Änderungen</option>
      <option value="cms">WordPress / CMS / geschäftliche Website</option>
      <option value="transactional">WooCommerce / Bestellungen / Mitgliederbereich / häufige Schreibvorgänge</option>
    </select>
  </div>
  <div class="mb-6">
    <label for="bk-rpo" class="form-label">Maximal akzeptabler Datenverlust (RPO)</label>
    <select id="bk-rpo" class="form-input">
      <option value="24">Bis zu 24 Stunden</option>
      <option value="4">Bis zu 4 Stunden</option>
      <option value="1">Bis zu 1 Stunde</option>
      <option value="lt1">Weniger als 1 Stunde</option>
    </select>
  </div>
  <div class="mb-6">
    <label for="bk-rto" class="form-label">Maximal akzeptable Ausfallzeit (RTO)</label>
    <select id="bk-rto" class="form-input">
      <option value="24">Bis zu 24 Stunden</option>
      <option value="4">Bis zu 4 Stunden</option>
      <option value="1">Etwa 1 Stunde</option>
      <option value="lt1">Weniger als 1 Stunde</option>
    </select>
  </div>
  <div class="mb-6">
    <label for="bk-offsite" class="form-label">Unabhängige Kopie außerhalb des Servers / Standorts vorhanden?</label>
    <select id="bk-offsite" class="form-input"><option value="no">Nein</option><option value="yes">Ja</option></select>
  </div>
  <div class="mb-6">
    <label for="bk-db" class="form-label">Datenbankkonsistente Backup-Methode überprüft?</label>
    <select id="bk-db" class="form-input">
      <option value="na">Nicht zutreffend / keine Datenbank</option>
      <option value="no">Nein / unbekannt</option>
      <option value="yes">Ja</option>
    </select>
  </div>
  <div class="mb-6">
    <label for="bk-restore" class="form-label">Kürzlich einen Wiederherstellungstest erfolgreich abgeschlossen?</label>
    <select id="bk-restore" class="form-input"><option value="no">Nein</option><option value="yes">Ja</option></select>
  </div>
  <div class="mb-6">
    <label for="bk-creds" class="form-label">Backup-Zugangsdaten / Wiederherstellungsschlüssel getrennt vom VPS aufbewahrt?</label>
    <select id="bk-creds" class="form-input"><option value="no">Nein / unbekannt</option><option value="yes">Ja</option></select>
  </div>
  <div class="mb-6">
    <label for="bk-versions" class="form-label">Mehrere Wiederherstellungspunkte / ältere Versionen verfügbar?</label>
    <select id="bk-versions" class="form-input"><option value="no">Nur neuester Stand / unbekannt</option><option value="yes">Ja</option></select>
  </div>
  <button class="btn btn-primary" type="submit">Backup-Strategie prüfen</button>
</form>
<p id="vps-backup-strategy-result" class="mt-6 rounded border border-border p-4 dark:border-darkmode-border" role="status" aria-live="polite">Wählen Sie die tatsächlich geltenden Wiederherstellungsanforderungen.</p>
</div>

<script>
document.addEventListener("DOMContentLoaded", function () {
  var form = document.getElementById("vps-backup-strategy-checker-form");
  if (!form) return;

  form.addEventListener("submit", function (event) {
    event.preventDefault();

    function val(id) { return document.getElementById(id).value; }

    var workload = val("bk-workload");
    var rpo = val("bk-rpo");
    var rto = val("bk-rto");
    var offsite = val("bk-offsite") === "yes";
    var db = val("bk-db");
    var restore = val("bk-restore") === "yes";
    var creds = val("bk-creds") === "yes";
    var versions = val("bk-versions") === "yes";

    var criticalGap = !offsite || !restore || !creds || !versions || (db === "no");
    var result;

    if (criticalGap) {
      result = "KRITISCHE BACKUP-LÜCKEN: Die Strategie hängt noch von einem unbewiesenen oder nicht unabhängigen Wiederherstellungsweg ab. Ergänzen Sie unabhängige externe Kopien, mehrere Wiederherstellungspunkte, getrennte Wiederherstellungszugänge und Schlüssel, bei Bedarf datenbankkonsistente Backups sowie einen echten Wiederherstellungstest.";
    } else if (rto === "lt1" || rto === "1") {
      result = "NIEDRIGE RTO / NOTFALLARCHITEKTUR PRÜFEN: Backups können korrekt sein, während ein manueller Neuaufbau das Wiederherstellungsziel von einer Stunde dennoch verfehlt. Messen Sie eine vollständige Wiederherstellungsübung. Erwägen Sie Automatisierung, vorbereitete Images, eine betriebsbereite Reserve oder Workload-Trennung, wenn die gemessene RTO zu hoch ist.";
    } else if (workload === "transactional" || rpo === "lt1" || rpo === "1") {
      result = "TRANSAKTIONEN / HÄUFIGE DATENBANK-BACKUPS: Behalten Sie die unabhängigen Wiederherstellungsebenen bei, richten Sie die Häufigkeit des Datenbankschutzes aber an der geforderten RPO aus. Ein nächtliches Backup kann ein Datenverlustziel von einer Stunde nicht erfüllen.";
    } else {
      result = "GRUNDLEGENDE WIEDERHERSTELLUNGSSTRATEGIE: Die zentralen Ebenen sind vorhanden. Behalten Sie Wiederherstellungspunkte beim Anbieter und unabhängige externe Backups bei, überwachen Sie fehlgeschlagene Aufträge, bewahren Sie mehrere Versionen auf und wiederholen Sie zeitlich gemessene Wiederherstellungsübungen.";
    }

    document.getElementById("vps-backup-strategy-result").textContent = result;
  });
});
</script>

## Mit RPO und RTO beginnen {#start-with-rpo-and-rto}

Zwei Kennzahlen sollten die Strategie bestimmen.

### Recovery Point Objective — RPO {#recovery-point-objective--rpo}

RPO beantwortet:

**Wie viele der zuletzt entstandenen Daten darf das Unternehmen verlieren?**

Bei einer RPO von:

- **24 Stunden** kann ein täglicher erfolgreicher Wiederherstellungspunkt akzeptabel sein;
- **4 Stunden** reichen tägliche Backups nicht aus;
- **1 Stunde** muss der veränderliche Anwendungs-/Datenbankzustand mindestens so häufig geschützt werden;
- **Minuten** reichen gewöhnliche zeitgesteuerte Backups allein möglicherweise nicht aus.

RPO betrifft **Datenverlust**, nicht Ausfallzeit.

### Recovery Time Objective — RTO {#recovery-time-objective--rto}

RTO beantwortet:

**Wie lange darf die Website beziehungsweise der Dienst nicht verfügbar sein?**

Ein Backup kann die RPO erfüllen und trotzdem die RTO verfehlen.

Beispiel:

- die Datenbank wird stündlich kopiert;
- der jüngste Datenverlust liegt unter einer Stunde;
- aber VPS-Neubereitstellung, Datendownload, Datenbankwiederherstellung und Website-Prüfung dauern sechs Stunden.

Diese Strategie kann eine RPO von einer Stunde erfüllen, hat aber tatsächlich eine RTO von etwa sechs Stunden.

Die NIST-Leitlinien zur Notfallplanung definieren RPO als zeitlichen Wiederherstellungspunkt und RTO als maximal akzeptables Zeitfenster der Nichtverfügbarkeit. Legen Sie diese Ziele fest, bevor Sie Werkzeuge auswählen.

## Was sollte gesichert werden? {#what-should-be-backed-up}

Teilen Sie den Server in **wiederaufbaubare** und **zustandsbehaftete/unersetzliche** Bestandteile ein.

### Wiederaufbaubar {#rebuildable}

Häufig aus Code oder Automatisierung reproduzierbar:

- Basisbetriebssystem;
- Pakete;
- Anwendungscode, der bereits sicher in Git liegt;
- Container-Images, die neu gebaut oder heruntergeladen werden können;
- Standard-Webserver-Pakete.

### Zustandsbehaftet / schwer wiederherzustellen {#stateful--difficult-to-recreate}

Gewöhnlich mit höherer Priorität:

- Datenbanken;
- Nutzer-Uploads/Medien;
- lokal gehostete Postfächer;
- Konfiguration;
- für die Wiederherstellung nötige Umgebungsdaten und Geheimnisse;
- TLS-/private Schlüssel, deren Ersatz nicht trivial ist;
- von Anwendungen erzeugte Daten;
- Control-Panel-/Website-Konfiguration;
- Cron-/Worker-Konfiguration;
- DNS-Zonendaten, wenn DNS auf dem VPS läuft;
- individuelle Skripte, die nirgendwo sonst gespeichert sind.

Verschwenden Sie Backup-Kapazität nicht durch blindes Kopieren von Caches, temporären Dateien und wiederaufbaubaren Artefakten, während Datenbank oder Startgeheimnisse der Website fehlen.

## Snapshot, Image, Dateibackup und Replikation unterscheiden sich {#snapshot-image-file-backup-and-replication-are-different}

Behandeln Sie diese Methoden nicht als austauschbar.

### Anbieter-Snapshot / Server-Image {#provider-snapshot--server-image}

Hilfreich für:

- schnelles Zurücksetzen nach einem riskanten Update;
- vollständige Serverwiederherstellung;
- Klonen oder Neuerstellen der virtuellen Maschine.

Schwächen:

- kann derselben Anbieter-/Kontoausfallumgebung unterliegen;
- bietet möglicherweise keine gezielte Datei-/Website-Wiederherstellung;
- Anwendungs- und Datenbankkonsistenz müssen trotzdem geklärt sein;
- ein einziges aktuelles Image bietet wenig Versionshistorie.

### Backup auf Dateiebene {#file-level-backup}

Hilfreich für:

- Uploads;
- Konfiguration;
- ausgewählte Anwendungsdaten;
- gezielte Wiederherstellung.

Werkzeuge wie restic oder Borg können verschlüsselte, versionierte Backups in entfernten Repositories speichern.

### Datenbank-Backup {#database-backup}

Verwenden Sie eine zur Datenbank-Engine passende Methode:

- logischer Dump;
- natives Backup-Werkzeug;
- anwendungskonsistenter Snapshot beziehungsweise Prozess.

Gehen Sie nicht davon aus, dass das Kopieren laufender Datenbankdateien ein verwendbares Datenbank-Backup ergibt.

### Replikation / Reservesystem {#replication--standby}

Replikation kann Wiederherstellungszeit oder Datenverlust reduzieren, ist für sich allein aber kein historisches Backup.

Auch falsche Löschungen, Beschädigungen oder Anwendungsfehler können repliziert werden.

Setzen Sie Replikation und Reservesysteme bei Bedarf für Verfügbarkeit und RTO ein und behalten Sie versionierte Backups zur Wiederherstellung älterer Zustände.

## Ein praktisches 3-2-1-Modell für VPS {#a-practical-3-2-1-model-for-vps}

Das verbreitete 3-2-1-Modell bedeutet:

- **3 Kopien** wichtiger Daten;
- **2 unterschiedliche Speicher-/Ausfallarten**;
- **1 Kopie extern / außerhalb der primären Ausfallumgebung**.

Für einen VPS kann eine praktische Auslegung so aussehen:

1. Produktivdaten auf dem VPS;
2. Backup-Image des Anbieters für schnelle Wiederherstellung;
3. verschlüsseltes externes Datei-/Datenbank-Backup an einem unabhängigen Ziel.

Es geht nicht darum, ein Schlagwort buchstabengetreu zu erfüllen. Es geht darum, zu verhindern, dass ein einziges Ereignis Produktivsystem und sämtliche Wiederherstellungskopien zerstört.

Beispiele für Ausfallumgebungen:

- das VPS-Dateisystem;
- der Backup-Speicher des Anbieters;
- das Anbieterkonto;
- ein separates Objektspeicherkonto beziehungsweise ein anderer Anbieter;
- eine Offline- oder unveränderliche Kopie.

Kann ein Angreifer mit Kontrolle über den VPS sämtliche Backups mit denselben Zugangsdaten löschen, sind die Kopien nicht wirksam unabhängig.

## Datenbankkonsistente Backups {#database-consistent-backups}

Der Datenbankzustand ändert sich, während die Website läuft.

Eine tragfähige Strategie muss festlegen, wie die Datenbank-Engine geschützt wird.

Für WordPress/MySQL/MariaDB kommen beispielsweise infrage:

- logische Dumps;
- native Datenbank-Backup-Werkzeuge;
- koordinierte Snapshots;
- Backup-Software, die Datenbankkonsistenz ausdrücklich berücksichtigt.

Nutzen Sie für PostgreSQL geeignete PostgreSQL-Backup-/PITR-Verfahren, sofern die RPO sie verlangt.

Entscheidend ist nicht das konkrete Werkzeug. Entscheidend ist, dass die wiederhergestellte Datenbank intern konsistent und verwendbar ist.

WordPress-spezifischen Anwendungszustand und Betrieb behandelt [VPS für WordPress]({{< relref "vps-for-wordpress.md" >}}).

Testen Sie:

- Dump/Backup wird abgeschlossen;
- die Datei ist nicht leer;
- Wiederherstellung/Import gelingt;
- repräsentative Tabellen und Datensätze sind vorhanden;
- die Anwendung kann sich verbinden und wichtige Lese-/Schreibvorgänge ausführen.

## Transaktionsbasierte Websites brauchen eine andere RPO {#transactional-sites-need-a-different-rpo}

Eine reine Unternehmenspräsentation kann eine einen Tag alte Kopie verkraften.

Ein transaktionsbasierter Shop möglicherweise nicht.

Definieren Sie bei WooCommerce, Mitglieder-, Abrechnungs- oder Bestellsystemen, wie viel des jüngsten Zustands verloren gehen darf:

- Bestellungen;
- Zahlungen;
- Lagerbestand;
- Kunden;
- Mitgliedschaften;
- Formulareinsendungen;
- Uploads.

Erhält ein Shop stündlich Bestellungen, kann ein nächtliches Datenbank-Backup viele Transaktionen verlieren.

Den Shop-Workload behandelt [VPS für WooCommerce]({{< relref "vps-for-woocommerce.md" >}}). Der Backup-Zeitplan sollte hier aus dem akzeptablen Zeitfenster für Transaktionsverlust abgeleitet werden.

## Backup-Häufigkeit und Aufbewahrung {#backup-frequency-and-retention}

Das Backup-Intervall darf nicht länger sein als die RPO der geschützten Datenklasse.

Unterschiedliche Daten können unterschiedliche Zeitpläne verwenden:

- Datenbank: häufig;
- Uploads: häufig oder ereignisgesteuert;
- Betriebssystem/Konfiguration: nach wichtigen Änderungen und nach Zeitplan;
- vollständiges Anbieter-Image: seltener, aber rund um riskante Änderungen nützlich.

Aufbewahrung schützt vor spät erkannten Fehlern.

Ein beispielhaftes Muster könnte aufbewahren:

- aktuelle stündliche Wiederherstellungspunkte;
- mehrere tägliche Kopien;
- mehrere wöchentliche Kopien;
- ausgewählte monatliche Kopien.

Die genaue Aufbewahrung richtet sich nach:

- geschäftlichen Wiederherstellungsanforderungen;
- Speicherkosten;
- Änderungsrate der Daten;
- Compliance- und rechtlichen Anforderungen;
- der möglichen Dauer unbemerkter Beschädigung oder Kompromittierung.

Bewahren Sie nicht nur den „neuesten Stand“ auf.

## Ein unabhängiges Ziel außerhalb des Servers vorhalten {#keep-an-independent-off-server-destination}

Ein Backup auf demselben VPS-Datenträger schützt nicht vor:

- Verlust von Datenträger oder Dateisystem;
- Löschen des Servers;
- Root-Kompromittierung;
- Ransomware;
- Fehlern im Konto;
- Verlust dieser virtuellen Maschine beim Anbieter.

Übertragen oder streamen Sie Wiederherstellungsdaten aus dem VPS heraus.

Mögliche Ziele:

- Objektspeicher;
- anderer Backup-Dienst beziehungsweise Anbieter;
- ein weiterer, ausschließlich für Backups genutzter VPS;
- Offline-Speicher oder kontrollierter Speicher.

Trennen Sie nach Möglichkeit Anbieter- und Kontozugangsdaten.

## Backups verschlüsseln und Wiederherstellungsschlüssel schützen {#encrypt-backups--and-protect-the-recovery-key}

Verschlüsseln Sie sensible Backup-Daten bei Übertragung und Speicherung, wo angemessen.

Verschlüsselung schafft jedoch eine weitere Voraussetzung für die Wiederherstellung.

Speichern Sie das **einzige** Backup-Passwort beziehungsweise den einzigen Schlüssel nicht:

- ausschließlich auf dem VPS;
- ausschließlich im selben Passworttresor oder Konto, das möglicherweise nicht verfügbar ist;
- ausschließlich im verschlüsselten Backup selbst.

Bewahren Sie Wiederherstellungszugangsdaten und Schlüssel an einem sicheren unabhängigen Ort auf und prüfen Sie ihre Verfügbarkeit bei Wiederherstellungsübungen.

## Backup-Zugangsdaten und Löschrechte trennen {#separate-backup-credentials-and-deletion-rights}

Eine Kompromittierung des Produktivservers sollte einem Angreifer nicht automatisch erlauben, sämtliche Wiederherstellungskopien zu löschen.

Bevorzugen Sie:

- eingeschränkte Backup-Zugangsdaten;
- Schreibzugriff ohne weitreichende Löschrechte, sofern der Speicher das unterstützt;
- separate Administratorzugangsdaten;
- Aufbewahrungssperren beziehungsweise Unveränderlichkeit, wo angemessen;
- Offline-/physisch getrennte Kopien für besonders wertvolle Daten.

Die genaue Ausgestaltung hängt vom Speicherdienst ab.

Das ist ein Grund, warum Backups auch eine Sicherheitsmaßnahme sind; siehe [VPS-Sicherheitscheckliste]({{< relref "vps-security-checklist.md" >}}).

## Backup-Aufträge überwachen {#monitor-backup-jobs}

Automatisierung verhindert vergessene Backups. Fehlerhafte Automatisierung kann jedoch unbemerkt scheitern.

Überwachen Sie:

- Zeitpunkt des letzten erfolgreichen Backups;
- fehlgeschlagene oder unvollständige Aufträge;
- Verfügbarkeit von Repository und Speicher;
- Ablauf von Zugangsdaten;
- freien Speicherplatz vor lokaler Zwischenspeicherung;
- externes Speicherkontingent;
- Fehler bei Datenbank-Dumps;
- Veränderungen der Backup-Dauer;
- ungewöhnlich kleine Backups;
- Fehler bei Aufbewahrung und Bereinigung.

Ein grüner Cron-/Dienststatus belegt, dass der Befehl ausgeführt wurde. Er belegt nicht, dass die Wiederherstellung funktioniert.

Das übergreifende Alarmkonzept für Server und Dienste gehört zu [VPS-Monitoring]({{< relref "vps-monitoring.md" >}}). Der Zustand der Backup-Aufträge bleibt Teil der Wiederherstellungsstrategie selbst.

## Wiederherstellung testen und tatsächliche RTO messen {#test-restores-and-measure-real-rto}

Ein Backup wird vertrauenswürdig, wenn es sich wiederherstellen lässt.

Führen Sie Wiederherstellungsübungen an einem isolierten, sauberen Ziel durch.

Testen Sie den vollständigen Ablauf in ausreichendem Umfang:

1. einen neuen VPS beziehungsweise eine Testumgebung bereitstellen;
2. den richtigen Backup-Stand abrufen;
3. Verschlüsselungs- und Repository-Zugangsdaten beschaffen;
4. Dateien und Konfiguration wiederherstellen;
5. Datenbank wiederherstellen/importieren;
6. erforderliche Geheimnisse und Zertifikate wiederherstellen;
7. Dienste und Netzwerk konfigurieren;
8. Anwendung starten;
9. wichtige Seiten und Transaktionen testen;
10. Hintergrundaufgaben und Integrationen prüfen;
11. verstrichene Wiederherstellungszeit messen.

Dokumentieren Sie das gemessene Ergebnis.

Beträgt die geschäftliche RTO vier Stunden und dauert der Test acht, verfehlt die Backup-Strategie die Geschäftsanforderung, selbst wenn jede Datei erfolgreich wiederhergestellt wurde.

NIST-Leitlinien betonen regelmäßige Backup-Erstellung, Wiederherstellungstests und Notfallübungen.

## Die Granularität der Wiederherstellung zählt {#restore-granularity-matters}

Eine gute Strategie unterstützt den tatsächlich aufgetretenen Fehlerfall.

### Einzelne Datei oder Website wiederherstellen {#single-filesite-recovery}

Benötigt bei:

- gelöschtem Upload;
- fehlerhafter Konfiguration;
- einer kompromittierten Website;
- notwendiger Wiederherstellung einer einzelnen beschädigten Datenbank oder Tabelle.

### Vollständigen Server wiederherstellen {#full-server-recovery}

Benötigt bei:

- ausgefallenem oder gelöschtem VPS;
- Dateisystemfehler;
- schwerer Kompromittierung;
- Austausch von Anbieter oder Server.

Ist das einzige Backup ein vollständiges Datenträger-Image, kann die Wiederherstellung einer einzelnen Datei umständlich sein.

Besteht das einzige Backup aus ausgewählten Dateien, kann der vollständige VPS-Neuaufbau zu lange dauern.

Kombinieren Sie die Methoden.

## Mehrere Websites brauchen Wiederherstellung pro Website {#multiple-websites-need-site-level-restore}

Planen Sie die Wiederherstellung auf einem VPS mit mehreren Websites nicht so, dass eine Reparatur von Website A automatisch Website B/C/D auf gestern zurücksetzt.

Bevorzugen Sie Backups, mit denen sich Folgendes wiederherstellen lässt:

- ein Dokumentverzeichnis;
- eine Datenbank;
- ein Panel/Benutzer;
- ein Satz Uploads;
- der gesamte VPS nur bei Bedarf.

Die Architekturentscheidung und gemeinsame Ausfallrisiken behandelt [VPS für mehrere Websites]({{< relref "vps-for-multiple-websites.md" >}}).

## Auch Backups können Ausfälle verursachen {#backups-can-cause-outages-too}

Backup-Arbeit verbraucht Ressourcen.

Mögliche Auswirkungen:

- CPU-Last durch Datenbank-Dumps;
- CPU-Last durch Komprimierung;
- Lese-I/O;
- temporärer Speicherplatzbedarf;
- Upload-Bandbreite zum Objektspeicher;
- Verdrängung von Cache-Inhalten;
- Überschneidung mit Importen, Scans oder Lastspitzen.

Erstellen Sie kein lokales Archiv von 30 GB, wenn auf dem VPS nur 10 GB frei sind.

Wo praktikabel:

- Backups direkt nach außerhalb des Servers streamen;
- temporäre Speicherplatzbelegung überwachen;
- aufwendige Backup-Arbeit außerhalb von Besucherspitzen planen;
- Übertragungs- oder Verarbeitungsrate begrenzen, sofern das Werkzeug es unterstützt;
- Backup-Dauer messen.

## Wie VDSina-Backups in die Strategie passen {#how-vdsina-backups-fit-the-strategy}

Die öffentliche VDSina-Dokumentation beschreibt derzeit mehrere nützliche Wiederherstellungsfunktionen:

- manuelle Server-Backup-Kopien;
- geplante Backups;
- Backup auf dem ursprünglichen Server wiederherstellen;
- neuen Server aus einem Backup erstellen;
- Server klonen;
- Backup-Image herunterladen.

Die Download-Dokumentation zeigt einen Backup-Dateinamen in folgender Form:

`vXXX.backup.hosted-by-vdsina.com.img.gz`

Dieses herunterladbare Image bietet eine nützliche zusätzliche Ebene der Übertragbarkeit, weil die Wiederherstellungskopie nicht ausschließlich im Anbieter-Panel verbleiben muss.

Allerdings:

- behandeln Sie das Anbieter-Image als **eine Ebene**, nicht als gesamte Strategie;
- testen Sie, wie Ihre gewählte Wiederherstellungsumgebung das heruntergeladene Image verwendet;
- nehmen Sie nicht an, dass jeder Hypervisor es ohne Konvertierung direkt nutzen kann;
- behalten Sie Anwendungs-, Datei- und Datenbank-Backups für gezielte Wiederherstellung;
- halten Sie eine Kopie in einer unabhängigen Ausfallumgebung vor, wenn das Risiko es rechtfertigt.

Die eigenen Geschäftsbedingungen von VDSina weisen die Backup-Verantwortung ausdrücklich dem Kunden zu und empfehlen einen regelmäßigen Backup-Prozess sowie wiederkehrende Wiederherstellungstests.

Beim Anlegen eines neuen VDSina-Servers aus einem Anbieter-Backup weisen die Fragen und Antworten darauf hin, dass Backup und neuer Server Anbietervorgaben erfüllen müssen, etwa zum Rechenzentrum und zu ausreichendem Speicherplatz. Auch Netzwerkeinstellungen können nach der Wiederherstellung angepasst werden müssen.

Verwechseln Sie Backup nicht mit Migration. Ein Backup kann Teil der Absicherung einer Migration sein. Produktive Umstellung, letzte Schreibvorgänge, DNS und Rollback sind jedoch eigene Themen; siehe [Website auf VPS umziehen]({{< relref "website-migration-to-vps.md" >}}).

<p>
  <a class="btn btn-primary" href="https://www.vdsina.com/?partner=ni8gzrvz75" target="_blank" rel="sponsored nofollow noopener">Aktuelle VPS-Backup-Optionen prüfen</a>
</p>
<p><small>Offenlegung: Der Herausgeber steht in einer beruflichen Beziehung zu VDSina. Diese Website kann eine Provision erhalten, wenn Sie über diesen Partnerlink bestellen. Backup-Funktionen des Anbieters ersetzen weder eine unabhängige Wiederherstellungsstrategie noch Wiederherstellungstests.</small></p>

## Ablaufplan für die Wiederherstellung {#recovery-runbook}

Dokumentieren Sie den Wiederherstellungsprozess vor dem Ausfall.

Halten Sie mindestens fest:

- Backup-Ziele;
- Benennung und Aufbewahrung von Wiederherstellungspunkten;
- Repository-Zugangsdaten;
- Aufbewahrungsort des Wiederherstellungsschlüssels;
- Zuordnung der Daten zu Datenbank, Dateien und Konfiguration;
- Schritte zur Bereitstellung eines neuen Servers;
- Software-/Laufzeitversionen;
- Wiederherstellungsreihenfolge;
- DNS-/Netzwerkschritte;
- externe Integrationen/Webhooks;
- Abnahmetests;
- wer über Wiederherstellung beziehungsweise Rollback entscheidet.

Bewahren Sie den Ablaufplan an einem Ort auf, der auch dann erreichbar bleibt, wenn der VPS selbst nicht verfügbar ist.

## VPS-Backup-Checkliste {#vps-backup-checklist}

| Maßnahme | Erfolgskriterium |
|---|---|
| RPO | maximal akzeptables Datenverlustfenster festgelegt |
| RTO | maximal akzeptable Ausfallzeit festgelegt |
| Dateninventar | Datenbank, Uploads, Konfiguration, Geheimnisse und weitere Zustandsdaten klassifiziert |
| Anbieter-Wiederherstellung | Image-/Snapshot-Zeitplan verstanden |
| Datenbank | zur Engine passende, wiederherstellbare Datenbank-Backup-Methode |
| Externe Kopie | unabhängige Wiederherstellungskopie außerhalb der VPS-Ausfallumgebung |
| Zugangsdaten | Backup-Konto eingeschränkt und von der Produktion getrennt |
| Verschlüsselung | sensible Backups angemessen verschlüsselt |
| Schlüsselwiederherstellung | Wiederherstellungsschlüssel/-passwort außerhalb des ausgefallenen VPS gespeichert |
| Aufbewahrung | mehrere historische Wiederherstellungspunkte |
| Monitoring | fehlgeschlagene, unvollständige oder veraltete Backups erkannt |
| Datenträger/I/O | Backup-Prozess kann Produktion nicht unbemerkt füllen oder überlasten |
| Granularität | Datei-/Website-/Datenbankwiederherstellung bei Bedarf möglich |
| Vollständige Wiederherstellung | Weg zum vollständigen VPS-/Dienstneuaufbau vorhanden |
| Wiederherstellungstest | isolierte Wiederherstellung erfolgreich abgeschlossen |
| Gemessene RTO | tatsächliche Wiederherstellungsdauer dokumentiert und innerhalb des Zielwerts |
| Ablaufplan | Wiederherstellungsreihenfolge, Zugangsdaten, DNS und Abnahmetests dokumentiert |
| Verantwortung | benannte Person oder Team verantwortet Backup und Wiederherstellung |

## Technische Referenzen {#technical-references}

- NIST SP 800-34 Rev.1 — RPO/RTO und Notfallplanung
- NIST SP 1339 — Backup-Erstellung, Tests und Wiederherstellungsübungen
- Ubuntu — restic-Werkzeug für Backup/Wiederherstellung
- Ubuntu — BorgBackup
- VDSina Geschäftsbedingungen — Backup-Verantwortung des Kunden
- VDSina — Server-Backup / Wiederherstellung / neuer Server aus Backup
- VDSina — geplante Backups
- VDSina — Server-Backup herunterladen und verwenden

## FAQ {#faq}

### Was ist eine gute VPS-Backup-Strategie? {#what-is-a-good-vps-backup-strategy}

RPO/RTO festlegen, unabhängige Wiederherstellungskopien aufbewahren, Datenbanken mit einer anwendungskonsistenten Methode schützen, mehrere Versionen vorhalten, fehlgeschlagene Aufträge überwachen und regelmäßig in einer sauberen Testumgebung wiederherstellen.

### Reicht ein VPS-Snapshot aus? {#is-a-vps-snapshot-enough}

Nicht als einzige Wiederherstellungsebene. Ein Anbieter-Snapshot oder -Image ist für schnelles Zurücksetzen und vollständige Serverwiederherstellung nützlich. Es kann aber derselben Anbieter-/Kontoausfallumgebung unterliegen und ist für gezielte Wiederherstellungen weniger bequem.

### Was bedeutet 3-2-1 für einen VPS? {#what-does-3-2-1-mean-for-a-vps}

Bewahren Sie neben den Live-Daten mehrere Wiederherstellungskopien auf unabhängigen Speichern beziehungsweise in unabhängigen Ausfallumgebungen auf. Mindestens eine Kopie sollte außerhalb des primären VPS-/Anbieterausfallpfads liegen.

### Wie oft sollte ich einen VPS sichern? {#how-often-should-i-back-up-a-vps}

Wählen Sie die Häufigkeit anhand der RPO jedes Datentyps. Eine statische Website kann tägliche Kopien verkraften; eine transaktionsbasierte Datenbank benötigt möglicherweise stündlichen oder noch häufigeren Schutz.

### Was ist der Unterschied zwischen RPO und RTO? {#what-is-the-difference-between-rpo-and-rto}

RPO ist der maximal akzeptable Verlust jüngster Daten. RTO ist die maximal akzeptable Ausfallzeit bis zur Wiederherstellung des Dienstes.

### Sollte ich den gesamten VPS oder nur Website-Dateien sichern? {#should-i-back-up-the-whole-vps-or-only-website-files}

Gewöhnlich sind beide Ebenen nützlich. Ein Server-Image beschleunigt die vollständige Wiederherstellung; Datei- und Datenbank-Backups erleichtern gezielte und anwendungskonsistente Rücksicherungen.

### Wie sichere ich MySQL oder PostgreSQL zuverlässig? {#how-do-i-back-up-mysql-or-postgresql-safely}

Verwenden Sie ein zur Engine passendes logisches oder natives Backup beziehungsweise ein koordiniertes anwendungskonsistentes Verfahren. Belegen Sie seine Wirksamkeit anschließend durch Wiederherstellung oder Import in einer isolierten Testumgebung.

### Sollten Backups verschlüsselt sein? {#should-backups-be-encrypted}

Sensible Wiederherstellungsdaten sollten angemessen verschlüsselt werden. Bewahren Sie Wiederherstellungspasswort und Schlüssel aber sicher außerhalb des ausgefallenen VPS auf.

### Ist Replikation ein Backup? {#is-replication-a-backup}

Nicht für sich allein. Replikation kann versehentliche Löschungen, Beschädigungen oder bösartige Änderungen kopieren. Bewahren Sie zusätzlich zu Replikation und Reservesystem historische, versionierte Backups auf.

### Bietet VDSina VPS-Backups an? {#does-vdsina-provide-vps-backups}

VDSina dokumentiert manuelle und geplante Backup-Kopien, Funktionen zur Wiederherstellung und zum Erstellen neuer Server aus Backups sowie herunterladbare Backup-Images. Die Geschäftsbedingungen belassen die Backup-Verantwortung beim Kunden und empfehlen regelmäßige Wiederherstellungstests.

### Wie oft sollte ich Wiederherstellungen testen? {#how-often-should-i-test-restores}

Nach einem festgelegten Zeitplan und nach wesentlichen Änderungen an Backup oder Architektur. Hochwertige oder schnell veränderliche Systeme sollten so häufig getestet werden, dass der gemessene Wiederherstellungsprozess verlässlich bleibt.

### Was gilt bei einer RTO unter einer Stunde? {#what-if-my-rto-is-under-one-hour}

Ein Konzept allein auf Backup-Basis kann zu langsam sein. Messen Sie eine vollständige Wiederherstellungsübung und erwägen Sie Automatisierung, vorbereitete Wiederherstellungs-Images, eine betriebsbereite Reserve oder Architekturänderungen, wenn die gemessene RTO das Ziel verfehlt.
