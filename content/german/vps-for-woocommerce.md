---
title: "VPS für WooCommerce"
description: "VPS für WooCommerce: CPU und RAM nach parallelen Checkouts, PHP-Workern, Datenbankschreiblast, Action Scheduler, Integrationen und Verkaufsspitzen planen und das Verwaltungsmodell wählen."
image: "images/home/vps-for-website-hero.webp"
slug: "vps-fuer-woocommerce"
---

Ein VPS für WooCommerce muss für die Shopbereiche dimensioniert werden, die nicht wie ein gecachter Blog funktionieren können: **Warenkorb, Checkout, Kundenkonto, Bestellungen, Lagerbestand, Zahlungsrückmeldungen, geplante Aktionen und Datenbankschreibvorgänge**. Monatliche Besuche oder die Produktanzahl allein sagen nicht, wie viel Serverleistung der Shop benötigt.

Für das allgemeine WordPress-Lastprofil lesen Sie [VPS für WordPress]({{< relref "vps-for-wordpress.md" >}}). Den zentralen Weg zur Serverauswahl finden Sie unter [VPS für Websites]({{< relref "_index.md" >}}).

[Kurzantwort](#quick-answer) · [Eignung prüfen](#woocommerce-vps-fit-checker) · [Checkout-Last](#checkout-and-account-traffic-stay-dynamic) · [Datenbank](#database-demand-and-hpos) · [Geplante Aktionen](#action-scheduler-and-background-work) · [Verkaufsspitzen](#size-for-sale-and-campaign-peaks) · [FAQ](#faq)

## Kurzantwort {#quick-answer}

Dies sind praktische Einstiegskonfigurationen der aktuellen VDSina-Standard-Tarife, keine Garantien für Bestell- oder Besucherzahlen.

| WooCommerce-Lastprofil | Praktischer Einstieg | Wichtigster zu prüfender Engpass |
|---|---:|---|
| Labor-/Testshop oder extrem schlanke Umgebung mit geringem Volumen | **1 vCPU / 2 GB / 40 GB** | sehr wenig Reserve für den Produktivbetrieb, sobald PHP, DB und Hintergrundaufgaben zusammenkommen |
| Kleiner geschäftlich genutzter Shop | **2 vCPU / 4 GB / 80 GB** | parallele Checkouts, PHP-Worker, DB-Latenz, geplante Aktionen |
| Anspruchsvollerer Shop, größerer Katalog/größere DB, mehr Integrationen oder Verkaufsspitzen | **4 vCPU / 8 GB / 160 GB** | anhaltende CPU-Last, PHP-Warteschlange, aktiver DB-Datenbestand, Action Scheduler, Speicherwachstum |
| Höhere Transaktionslast, die einen einzelnen VPS mit 8 GB übersteigt | **Architektur erneut prüfen** | DB/Worker/Dienste trennen oder eine leistungsfähigere Cloud-/Managed-Architektur nutzen, statt nur einen einzelnen Server zu vergrößern |

Die WooCommerce-eigenen Skalierungshinweise haben **1 vCPU + mindestens 2 GB RAM** als grundlegende selbst gehostete Konfiguration mit OPcache, CDN und Unterstützung für persistenten Cache genannt. Das ist eine Einstiegsuntergrenze, kein Versprechen, dass ein produktiver Shop dort dauerhaft ausreichend Reserve hat.

Aktuelle VDSina-Standard-Preise, erneut geprüft am 13. Oktober 2026:

- 1 vCPU / 1 GB / 10 GB / 1 TB monatlicher Datentransfer – **$0.07/Tag**;
- 1 vCPU / 2 GB / 40 GB / 32 TB – **$0.50/Tag**;
- 2 vCPU / 4 GB / 80 GB / 32 TB – **$0.67/Tag**;
- 4 vCPU / 8 GB / 160 GB / 32 TB – **$1.34/Tag**.

Für viele echte Geschäftsshops sind **4 GB der praktischere Einstieg**, weil Betriebssystem, Datenbank, PHP-Worker, Cache, Hintergrundaufgaben und Betriebsreserve gleichzeitig auf dem VPS Platz finden müssen.

Für eine tiefergehende, stackübergreifende Dimensionierung nutzen Sie [VPS für Websites dimensionieren]({{< relref "vps-sizing-for-website.md" >}}).

## WooCommerce-Anforderungen sind keine Dimensionierung für einen produktiven VPS {#woocommerce-requirements-are-not-production-vps-sizing}

Die aktuellen Serverempfehlungen für WooCommerce 10.8+ nennen:

- **WordPress 6.9+**;
- **PHP 8.3+**;
- **MySQL 8.0+ oder MariaDB 10.6+**;
- **HTTPS**;
- **WordPress-Speicherlimit 256 MB+**;
- Apache oder Nginx als empfohlene Webserver.

Diese Werte beantworten **„Erfüllt die Umgebung die grundlegenden Softwareanforderungen von WooCommerce?“**

Sie beantworten nicht:

- wie viele PHP-Worker Sie benötigen;
- wie viel RAM der gesamte VPS braucht;
- ob der aktive Datenbestand der DB in den Arbeitsspeicher passt;
- ob beim Checkout unter Last Warteschlangen entstehen;
- ob geplante Aktionen verspätet ausgeführt werden;
- ob Backups und Importe mit Kundenaktivität kollidieren;
- ob Zahlungs-/Webhook-Integrationen Anfragen verzögern.

Ein **WordPress-/PHP-Speicherlimit von 256 MB entspricht nicht 256 MB VPS-RAM**. Der gesamte Serverspeicher muss zusätzlich Linux, Webserver, DB, PHP-Worker, Cache, Aufgaben, Panel/E-Mail und Reserve abdecken.

## Eignung eines VPS für WooCommerce prüfen {#woocommerce-vps-fit-checker}

Nutzen Sie dies als erste Entscheidungshilfe, nicht als Leistungsgarantie.

<div class="rounded-2xl bg-light p-6 dark:bg-darkmode-light">
<form id="woocommerce-vps-fit-checker-form">
  <div class="mb-6">
    <label for="wc-stage" class="form-label">Shopphase / geschäftliche Bedeutung</label>
    <select id="wc-stage" class="form-input">
      <option value="test">Test / vor dem Start / geringe geschäftliche Auswirkungen</option>
      <option value="small">Kleiner laufender Shop</option>
      <option value="business">Geschäftskritischer Shop</option>
    </select>
  </div>
  <div class="mb-6">
    <label for="wc-limits" class="form-label">Zeigt das aktuelle Hosting wiederholt Ressourcengrenzen oder fehlt eine Funktion?</label>
    <select id="wc-limits" class="form-input">
      <option value="no">Nein / nicht gemessen</option>
      <option value="yes">Ja</option>
    </select>
  </div>
  <div class="mb-6">
    <label for="wc-external" class="form-label">Wurde der Hauptfehler oder die Hauptverzögerung bereits auf einen Zahlungs-, Versand-, Steuer-, SMTP- oder anderen externen Dienst zurückgeführt?</label>
    <select id="wc-external" class="form-input">
      <option value="no">Nein / nicht bekannt</option>
      <option value="yes">Ja</option>
    </select>
  </div>
  <div class="mb-6">
    <label for="wc-checkout" class="form-label">Gleichzeitige Checkout- und Kontoaktivität</label>
    <select id="wc-checkout" class="form-input">
      <option value="low">Gering</option>
      <option value="medium">Mittel</option>
      <option value="high">Hoch / kampagnengetrieben</option>
    </select>
  </div>
  <div class="mb-6">
    <label for="wc-catalog" class="form-label">Last durch Katalog, Suche und Filter</label>
    <select id="wc-catalog" class="form-input">
      <option value="light">Gering</option>
      <option value="medium">Mittel</option>
      <option value="heavy">Groß / aufwendige Abfragen</option>
    </select>
  </div>
  <div class="mb-6">
    <label for="wc-jobs" class="form-label">Aufwendige Plugins, Importe, Webhooks, Abonnements oder geplante Aufgaben?</label>
    <select id="wc-jobs" class="form-input"><option value="no">Nein</option><option value="yes">Ja</option></select>
  </div>
  <div class="mb-6">
    <label for="wc-db" class="form-label">Datenbank- und Bestellaktivität</label>
    <select id="wc-db" class="form-input">
      <option value="small">Klein / gering</option>
      <option value="medium">Mittel</option>
      <option value="heavy">Viele Schreibvorgänge und Abfragen</option>
    </select>
  </div>
  <div class="mb-6">
    <label for="wc-panel" class="form-label">Control Panel oder lokale E-Mail auf demselben VPS?</label>
    <select id="wc-panel" class="form-input"><option value="no">Nein</option><option value="yes">Ja</option></select>
  </div>
  <div class="mb-6">
    <label for="wc-spikes" class="form-label">Regelmäßige Spitzen durch Verkaufsaktionen, Newsletter oder Werbung?</label>
    <select id="wc-spikes" class="form-input"><option value="no">Nein</option><option value="yes">Ja</option></select>
  </div>
  <div class="mb-6">
    <label for="wc-operator" class="form-label">Kann jemand den VPS betreiben?</label>
    <select id="wc-operator" class="form-input">
      <option value="no">Nein</option>
      <option value="help">Nur mit Managed-Service / bezahlter Administration</option>
      <option value="yes">Ja</option>
    </select>
  </div>
  <button class="btn btn-primary" type="submit">Passenden WooCommerce-VPS abschätzen</button>
</form>
<p id="woocommerce-vps-fit-result" class="mt-6 rounded border border-border p-4 dark:border-darkmode-border" role="status" aria-live="polite">Wählen Sie das Lastprofil, das Ihrem Shop am nächsten kommt.</p>
</div>

<script>
document.addEventListener("DOMContentLoaded", function () {
  var form = document.getElementById("woocommerce-vps-fit-checker-form");
  if (!form) return;

  form.addEventListener("submit", function (event) {
    event.preventDefault();

    function val(id) { return document.getElementById(id).value; }

    var stage = val("wc-stage");
    var limits = val("wc-limits") === "yes";
    var external = val("wc-external") === "yes";
    var checkout = val("wc-checkout");
    var catalog = val("wc-catalog");
    var jobs = val("wc-jobs") === "yes";
    var db = val("wc-db");
    var panel = val("wc-panel") === "yes";
    var spikes = val("wc-spikes") === "yes";
    var operator = val("wc-operator");

    var score = 0;
    if (stage === "small") score += 1;
    if (stage === "business") score += 3;
    if (checkout === "medium") score += 2;
    if (checkout === "high") score += 4;
    if (catalog === "medium") score += 1;
    if (catalog === "heavy") score += 3;
    if (jobs) score += 2;
    if (db === "medium") score += 1;
    if (db === "heavy") score += 3;
    if (panel) score += 1;
    if (spikes) score += 2;

    var result;

    if (external) {
      result = "ZUERST EXTERNEN DIENST / ANWENDUNG UNTERSUCHEN: Der Hauptfehler wurde bereits außerhalb der VPS-Ressourcen lokalisiert. Beheben oder messen Sie den Gateway-, API-, SMTP- oder Integrationsweg, bevor Sie mehr CPU oder RAM kaufen.";
    } else if (!limits && stage !== "business" && score <= 2) {
      result = "MANAGED / SHARED KANN WEITERHIN PASSEN: Es gibt noch keinen gemessenen Engpass, der einen VPS erfordert. Behalten Sie das einfachere Hostingmodell bei oder optimieren Sie zuerst, bis ein echter Ressourcen- oder Funktionsgrund vorliegt.";
    } else if (stage === "business" && operator !== "yes") {
      result = "MANAGED-SERVICE / ADMINISTRATIONSHILFE: Der Shop ist geschäftskritisch, der Serverbetrieb hat aber keinen vollständig zuständigen internen Verantwortlichen. Organisieren Sie Managed-Service oder bezahlte Administration, bevor Sie einen reinen Unmanaged VPS wählen.";
    } else if (score <= 2) {
      result = "SCHLANKER EINSTIEG MIT 2 GB / KLEINER SHOP: 1 vCPU / 2 GB / 40 GB können ein grundlegender Ausgangspunkt für einen sehr leichten Shop sein. Prüfen Sie Checkout, PHP-Worker-Speicher, DB-Latenz und geplante Aktionen, bevor Sie ihn als produktionsbereit ansehen.";
    } else if (score <= 7) {
      result = "PRAKTISCHER EINSTIEG MIT 4 GB: 2 vCPU / 4 GB / 80 GB bieten mehr Reserve für einen kleinen geschäftlichen WooCommerce-Shop mit dynamischem Checkout, DB-Schreibvorgängen und normalen Hintergrundaufgaben.";
    } else {
      result = "8 GB ODER ARCHITEKTUR PRÜFEN: 4 vCPU / 8 GB / 160 GB sind ein stärkerer Einstieg für anspruchsvollere Shops oder Verkaufsspitzen. Dominieren DB, Aufgaben oder Integrationen, erwägen Sie eine Lasttrennung oder eine leistungsfähigere Managed-/Cloud-Architektur.";
    }

    document.getElementById("woocommerce-vps-fit-result").textContent = result;
  });
});
</script>

## Wann WooCommerce tatsächlich einen VPS braucht {#when-woocommerce-actually-needs-vps}

Ein VPS kann für einen WooCommerce-Shop gerechtfertigt sein, wenn:

- Shared Hosting bei berechtigter Last wiederholt CPU-, Speicher-, Prozess- oder I/O-Grenzen erreicht;
- Checkout-/Kontoanfragen unter echter Last in Warteschlangen landen;
- der aktive DB-Datenbestand oder die Schreiblast mehr Kontrolle erfordert;
- Erweiterungen Dienste benötigen, die das aktuelle Hosting nicht erlaubt;
- Redis/Memcached oder individuelle Serverkonfiguration nötig sind;
- Action Scheduler oder Hintergrundaufgaben zuverlässiger ausgeführt werden müssen;
- Produktimporte, Feeds oder Bestandsabgleich mit Kundenaktivität kollidieren;
- individuelle PHP-, Laufzeit- oder Webservereinstellungen nötig sind;
- Staging oder shopspezifische Betriebskontrolle erforderlich sind.

Ist der Shop klein, stabil und bei einem Managed-WooCommerce-/WordPress-Host gut betreut, ist ein VPS nicht automatisch die bessere Wahl.

## Wann Managed WooCommerce Hosting besser passen kann {#when-managed-woocommerce-hosting-may-be-better}

Ein selbst verwalteter VPS passt schlecht, wenn:

- niemand Betriebssystem- und Sicherheitsupdates verantwortet;
- niemand die Checkout-Verfügbarkeit oder Serveralarme überwacht;
- Backups existieren, die Wiederherstellung aber ungetestet ist;
- Ausfälle bei Zahlungen oder Bestellungen geschäftskritisch sind;
- das Team WordPress-/WooCommerce-Hilfe statt Linux-Administration möchte;
- die vorhandene Managed-Plattform Leistung und Skalierung bereits ausreichend abdeckt.

Ein VPS bietet mehr Kontrolle, bringt aber auch mehr mögliche Fehlerquellen in Ihre Verantwortung.

Lesen Sie [Managed VPS vs. Unmanaged VPS]({{< relref "managed-vs-unmanaged-vps.md" >}}), bevor Sie einen umsatzkritischen Shop auf einem selbst verwalteten Server betreiben.

## Checkout- und Kontozugriffe bleiben dynamisch {#checkout-and-account-traffic-stay-dynamic}

Die WooCommerce-eigenen Caching-Hinweise verlangen, **Warenkorb, Mein Konto und Checkout** vom vollständigen Seitencache auszunehmen, weil sie kundenspezifischen Zustand enthalten.

Das ist wichtig, weil gerade die wirtschaftlich entscheidenden Anfragen weiterhin Folgendes ausführen können:

- PHP;
- Sitzungs- und Warenkorblogik;
- Versand- und Steuerlogik;
- Code der Zahlungsintegration;
- Datenbank-Lese- und Schreibvorgänge;
- Bestellerstellung;
- Bestandsaktualisierungen;
- Hooks und Erweiterungen.

Ein Shop kann deshalb eine gecachte Produktseite schnell ausliefern, während beim Checkout dennoch Warteschlangen entstehen.

Dimensionieren Sie WooCommerce nicht allein anhand der Cache-Trefferquote des Katalogs.

## PHP-Worker und dynamische Parallelität {#php-workers-and-dynamic-concurrency}

Bei dynamischen WooCommerce-Anfragen bestimmen PHP-Worker, wie viele Anfragen gleichzeitig ausgeführt werden können.

Eine nützliche Näherung lautet:

**aktive dynamische Anfragen ≈ ungecachte Anfragen pro Sekunde × Anfragedauer**

Benötigen Checkout-/Konto-/API-Anfragen in der Spitze durchschnittlich 0.8 Sekunden und erreichen 5 dynamische Anfragen pro Sekunde PHP, können ungefähr vier Worker gleichzeitig beschäftigt sein – noch ohne Administration, Webhooks und Hintergrundaufgaben.

Jeder Worker verbraucht Speicher. Eine höhere Worker-Zahl ohne RAM-Budget kann der Datenbank Speicher entziehen oder den Server in Swap-Nutzung beziehungsweise OOM treiben.

Rechnen Sie mit:

**WooCommerce-RAM = Betriebssystem + Webserver + DB + Cache + PHP-Worker + Aufgaben + Panel/E-Mail + Reserve**

Prüfen Sie anschließend den durchschnittlichen und maximalen Worker-Speicher, statt eine allgemeine Worker-Zahl zu kopieren.

## WooCommerce richtig cachen {#cache-woocommerce-correctly}

WooCommerce benötigt eine mehrschichtige Cache-Strategie.

### Vollständiger Seitencache {#full-page-cache}

Sinnvoll für cachefähige Katalog- und Inhaltsseiten.

Cachen Sie **nicht** pauschal:

- Warenkorb;
- Checkout;
- Mein Konto;
- kunden- oder sitzungsspezifische Antworten.

Die offiziellen WooCommerce-Caching-Hinweise schließen diese Seiten ausdrücklich aus.

### OPcache {#opcache}

Speichert kompilierten PHP-Bytecode und verringert wiederholte PHP-Kompilierung.

### Persistenter Objektcache {#persistent-object-cache}

Redis oder Memcached können wiederholte Datenbank- und Objektarbeit reduzieren, wenn das Lastprofil davon profitiert.

Das ersetzt weder vollständiges Seiten-Caching noch behebt es automatisch ineffiziente Abfragen.

### Browser / CDN {#browser--cdn}

Sinnvoll für statische Dateien und Inhalte, die am Netzwerkrand ausgeliefert werden können.

Ein CDN kann statische Anfragen an den Ursprungsserver reduzieren, beseitigt aber keine dynamische Checkout- oder Datenbankarbeit.

## Datenbankbedarf und HPOS {#database-demand-and-hpos}

WooCommerce erzeugt intensivere Datenbank-Lese- und Schreiblast als eine typische gecachte WordPress-Website.

Wichtige Datenbankaufgaben können sein:

- Erstellen und Aktualisieren von Bestellungen;
- Kunden- und Kontodaten;
- Bestandsänderungen;
- Produkt- und Katalogabfragen;
- Sitzungen;
- Metadaten von Erweiterungen;
- Berichte und Analysen;
- Suche und Filter;
- geplante Aufgaben.

WooCommerce **High-Performance Order Storage (HPOS)** speichert Bestelldaten in eigenen Tabellen und ist seit WooCommerce 8.2 bei Neuinstallationen standardmäßig aktiviert.

HPOS ist eine wichtige Architekturverbesserung, ersetzt aber nicht:

- kompatible Erweiterungen und eigenen Code;
- Prüfung von Abfragen und Indizes;
- ausreichend Datenbankspeicher;
- geringe Speicherlatenz;
- Monitoring;
- Staging und Tests vor größeren Änderungen.

Für bestehende große Shops empfiehlt WooCommerce, die HPOS-Migration und kritische Abläufe vor der produktiven Umschaltung zu testen.

## Action Scheduler und Hintergrundarbeit {#action-scheduler-and-background-work}

WooCommerce nutzt **Action Scheduler** für Hintergrundaufgaben wie:

- Bestellbenachrichtigungen;
- zahlungsbezogene Verarbeitung;
- Webhooks;
- Abonnements und Verlängerungen;
- Erweiterungsaufgaben;
- Importe und Synchronisation.

WooCommerce zeigt diese unter **WooCommerce > Status > Geplante Aktionen** an.

Achten Sie auf:

- fehlgeschlagene Aktionen;
- überfällige Aktionen;
- dauerhaft aufgelaufene ausstehende Aufgaben;
- lange laufende Aufgaben;
- Warteschlangen, die während Kundenspitzen wachsen.

Action Scheduler hängt standardmäßig von der WordPress-Zeitplanung ab. Serverseitiger Cron kann daher sinnvoll sein, wenn eine zuverlässige zeitliche Ausführung erforderlich ist.

Ein Shop mit schnellen gecachten Seiten kann trotzdem Betriebsprobleme haben, wenn seine Aufgabenwarteschlange fehlschlägt.

## Zahlungen, Webhooks, E-Mail und Integrationen {#payments-webhooks-email-and-integrations}

Ein größerer VPS kann nicht jeden Checkout-Fehler beheben.

Externe Abhängigkeiten können sein:

- Zahlungs-Gateways;
- Steuer-APIs;
- Versand-APIs;
- Bestands-/ERP-Abgleich;
- CRM;
- Transaktions-E-Mails;
- Betrugsprüfungen;
- Webhooks;
- externe Such- und andere Dienste.

Messen Sie, ob eine Verzögerung auf Ihrem VPS oder beim externen Dienst entsteht.

Überwachen Sie:

- fehlgeschlagene Zahlungsrückmeldungen;
- Webhook-Zustellung;
- E-Mail-Warteschlangen;
- API-Zeitüberschreitungen;
- Wiederholungs- und Backoff-Verhalten;
- Action-Scheduler-Fehler.

Kaufen Sie keine CPU-Leistung, um einen Engpass bei einer fremden API zu lösen.

## Katalog, Suche und Filter {#catalog-search-and-filtering}

Große Kataloge erzeugen Last nicht allein durch die Anzahl ihrer Produkte.

Der tatsächliche Druck entsteht durch:

- komplexe Such- und Filterabfragen;
- Attribut- und Taxonomieabfragen;
- Produkt-Nachschlagetabellen;
- die Anzahl der Varianten;
- Preis- und Bestandsregeln;
- Erweiterungen mit zusätzlichen SQL-Abfragen oder externen Aufrufen;
- ungecachte personalisierte Ergebnisse.

Messen Sie Such- und Filterendpunkte getrennt vom gewöhnlichen Aufrufen von Produktseiten.

Persistenter Cache kann bei einigen wiederholten Abfragen helfen, die Datenbank- und Abfragegestaltung bleibt dennoch wichtig.

## Für Verkaufs- und Kampagnenspitzen dimensionieren {#size-for-sale-and-campaign-peaks}

WooCommerce-Spitzenlast vereint häufig mehrere Dinge gleichzeitig:

- Newsletter- und Werbezugriffe;
- Katalogaufrufe;
- Hinzufügen zum Warenkorb;
- Checkout;
- Zahlungsrückmeldungen;
- Bestell-E-Mails;
- Bestandsaktualisierungen;
- Administration und Bestellverarbeitung;
- Webhooks;
- geplante Aktionen;
- Analysen und Protokollierung.

Dimensionieren Sie für ein **repräsentatives Spitzenzeitfenster**, nicht für den Durchschnittstag.

Vor einer größeren Werbeaktion:

1. Testen Sie repräsentative Checkout-Zugriffe.
2. Prüfen Sie die Reserve der PHP-Worker.
3. Prüfen Sie DB-Latenz und Verbindungen.
4. Prüfen Sie den Rückstand im Action Scheduler.
5. Pausieren oder verlegen Sie Importe, Backups und Scans.
6. Prüfen Sie externe Zahlungs-, Versand- und Steuer-APIs.
7. Beobachten Sie während der Aktion Protokolle und Ressourcenmetriken.

## Speicher, Backups und Staging {#storage-backups-and-staging}

Ein WooCommerce-Backup muss sowohl Dateien als auch Transaktionsdaten schützen.

Nehmen Sie auf:

- WordPress-/WooCommerce-Dateien;
- Uploads und Produktmedien;
- Datenbank- und Bestelldaten;
- für die Wiederherstellung erforderliche Konfiguration und Geheimnisse;
- Plugins, Themes und eigenen Code;
- Integrationseinstellungen.

### Wiederherstellung mit Blick auf Transaktionen {#transaction-aware-recovery}

Gehen fortlaufend Bestellungen ein, bestimmt die Backup-Häufigkeit den möglichen Verlust von Bestelldaten.

Ein tägliches DB-Backup kann bedeuten, dass bis zu einem Tag aktueller Transaktionen außerhalb dieses Wiederherstellungspunkts liegen.

Wählen Sie die Backup-Häufigkeit nach dem akzeptablen **Recovery Point Objective (RPO)**, nicht nach Bequemlichkeit.

Die ausführliche Backup-Architektur behandelt [VPS-Backup-Strategie]({{< relref "vps-backup-strategy.md" >}}).

### Staging {#staging}

Testen Sie Änderungen an PHP, WooCommerce, Plugins, Themes, HPOS und Zahlungen nach Möglichkeit zuerst in einer Staging-Umgebung.

Staging-Kopien verbrauchen ebenfalls Festplattenspeicher und mitunter DB-, RAM- und Backup-Ressourcen. Berücksichtigen Sie sie deshalb in der Kapazitätsplanung.

## Control Panel, FASTPANEL oder manueller Stack {#control-panel-fastpanel-or-manual-stack}

WooCommerce kann auf einem manuell verwalteten Linux-VPS oder über ein Hosting-Control-Panel laufen.

Für die allgemeine Panel-Auswahl lesen Sie [VPS mit Control Panel]({{< relref "vps-with-control-panel.md" >}}).

Für den speziellen VDSina-FASTPANEL-Weg lesen Sie [VPS-Hosting mit FASTPANEL]({{< relref "fastpanel-vps-hosting.md" >}}).

Für die manuelle Linux-Bereitstellung lesen Sie [Website auf einem VPS hosten]({{< relref "how-to-host-a-website-on-vps.md" >}}).

Ein Control Panel vereinfacht Routineaufgaben; es übernimmt nicht die Verantwortung für zuverlässige Checkouts, WooCommerce-/Plugin-Updates, DB-Abstimmung, Backups oder Störungen.

## Die Migration eines laufenden Shops braucht eine klare Datengrenze {#live-store-migration-has-a-data-boundary}

Eine WooCommerce-Migration ist mehr als „Dateien und DB kopieren“.

Bestellungen, Lagerbestand, Warenkörbe, Kunden und geplante Aktionen können sich ändern, während der Shop läuft.

Für die Migration:

- bauen und testen Sie zuerst das Zielsystem;
- kontrollieren Sie die letzten Schreibvorgänge;
- synchronisieren Sie Datenbank und Uploads abschließend;
- vermeiden Sie zwei beschreibbare produktive Shops mit auseinanderlaufenden Daten;
- prüfen Sie Zahlungs- und Webhook-Endpunkte;
- erhalten Sie E-Mail und DNS;
- halten Sie einen Rollback-Plan bereit.

Den vollständigen Umschaltprozess beschreibt [Website auf einen VPS umziehen]({{< relref "website-migration-to-vps.md" >}}).

## Wann ein WooCommerce-VPS ein Upgrade braucht {#woocommerce-vps-upgrade-triggers}

Skalieren oder ändern Sie die Architektur, wenn Messungen Folgendes zeigen:

- wiederholte PHP-Worker-Warteschlangen;
- anhaltende CPU-Sättigung nach Cache-, Abfrage- und Plugin-Optimierung;
- RAM-Druck, Swap-Nutzung oder OOM;
- DB-Latenz oder Speicherdruck durch den aktiven DB-Datenbestand;
- kapazitätsbedingte Action-Scheduler-Rückstände oder -Fehler;
- Checkout-/Zahlungsfehler unter berechtigter Spitzenlast;
- Speicherwachstum, das sichere Reserven verringert;
- Backup-, Import- oder Scan-Aufgaben, die mit Kundenaktivität kollidieren;
- mehrere Shops oder Dienste, die um einen VPS konkurrieren.

Ist der Checkout langsam, während die Serverressourcen unauffällig sind, untersuchen Sie Zahlungs-, API-, Plugin- und Datenbankursachen, bevor Sie einen größeren VPS kaufen.

## Checkliste für den Start eines WooCommerce-VPS {#woocommerce-vps-launch-checklist}

| Prüfung | Erfüllte Bedingung |
|---|---|
| WooCommerce-Laufzeit | aktuelle kompatible WordPress-/PHP-/DB-Versionen und HTTPS |
| PHP-Speicher | WooCommerce-/WordPress-Speicherlimit konfiguriert; gesamter VPS-RAM separat ausreichend |
| PHP-Worker | ausreichend für repräsentative parallele dynamische Checkout-/Kontoanfragen |
| Seitencache | Warenkorb, Checkout, Kundenkonto und sitzungsspezifische Abläufe ausgeschlossen |
| Objektcache/OPcache | Cache-Ebenen bewusst gewählt; Redis/Memcached nur, wo sinnvoll |
| Datenbank | Bestell-, Katalog- und Abfragelast überwacht; HPOS-Kompatibilität bekannt |
| Geplante Aktionen | kein unerklärter Rückstand fehlgeschlagener oder überfälliger Aktionen |
| Zahlungen | Tests für Bestellungen, Zahlungen, Erstattungen und Webhooks erfolgreich |
| Lagerbestand | Bestandsänderungen bleiben konsistent |
| E-Mail | Transaktionsnachrichten werden über einen zuverlässigen Weg zugestellt |
| Backups | Dateien, DB, RPO für neue Bestellungen und Wiederherstellungsweg festgelegt |
| Staging | kritische Updates außerhalb des Produktivsystems testbar |
| Monitoring | externe Checkout-/Website-Prüfungen sowie Einblick in CPU/RAM/Festplatte/DB |
| Neustart | Web/PHP/DB/Aufgaben starten automatisch wieder |
| Spitzenlast | repräsentative Verkaufs- oder Kampagnenlast geprüft |

## Aktuelle Beispiele für WooCommerce-VPS {#current-woocommerce-vps-examples}

Diese aktuellen VDSina-Standard-Tarife sind Zuordnungsbeispiele, keine Garantien für Shopkapazität.

| VPS | Geeigneter Einstieg | Erneut prüfen bei |
|---|---|---|
| 1 vCPU / 2 GB / 40 GB – $0.50/Tag | Labor, sehr leichter kleiner Shop oder kontrollierte Umgebung mit geringem Volumen | geschäftskritischem Checkout, aufwendigen Plugins, vielen Aufgaben |
| 2 vCPU / 4 GB / 80 GB – $0.67/Tag | praktische WooCommerce-Basis für kleine Unternehmen | starken Verkaufsspitzen, großer DB/großem Katalog, vielen Integrationen |
| 4 vCPU / 8 GB / 160 GB – $1.34/Tag | anspruchsvollerer Shop / mehr Reserve für DB, PHP und Hintergrundarbeit | einer Ein-Server-Architektur, die zum Engpass oder gemeinsamen Ausfallbereich wird |

Der Standard-Tarif mit 1 GB wird hier nicht als normale Option für einen produktiven WooCommerce-Shop dargestellt.

Die aktuelle Standard-Seite von VDSina führt in den sichtbaren Vorlagen- und Anwendungsgruppen **keine** eigene vorinstallierte WooCommerce-Anwendung auf. Nutzen Sie einen kompatiblen WordPress-, manuellen oder Panel-Weg, statt WooCommerce mit einem Klick vorauszusetzen.

<p>
  <a class="btn btn-primary" href="https://www.vdsina.com/?partner=ni8gzrvz75" target="_blank" rel="sponsored nofollow noopener">Aktuelle WooCommerce-VPS-Optionen prüfen</a>
</p>
<p><small>Offenlegung: Der Herausgeber steht in einer beruflichen Beziehung zu VDSina. Diese Website kann eine Provision erhalten, wenn Sie über diesen Partnerlink bestellen. Prüfen Sie vor der Bestellung die aktuellen VPS-Preise sowie die Verfügbarkeit von Vorlagen und Panels.</small></p>

## Technische Referenzen {#technical-references}

- WooCommerce – Serverempfehlungen
- WooCommerce Developer – Skalierung mit WooCommerce
- WooCommerce Developer – Caching-Plugins konfigurieren
- WooCommerce – Geplante Aktionen
- WooCommerce Developer – High Performance Order Storage
- VDSina Standard VPS

## FAQ {#faq}

### Wie viel RAM braucht WooCommerce auf einem VPS? {#how-much-ram-does-woocommerce-need-on-a-vps}

Es gibt keine allgemeingültige Zahl. Die WooCommerce-eigenen Skalierungshinweise haben 2 GB als grundlegende selbst gehostete Konfiguration genannt. Ein VPS mit 4 GB ist für viele Geschäftsshops der solidere praktische Einstieg, weil PHP-Worker, DB, Cache und Aufgaben gleichzeitig Ressourcen benötigen.

### Reichen 2 GB RAM für WooCommerce? {#is-2-gb-ram-enough-for-woocommerce}

Für einen sehr kleinen, schlanken Shop oder eine kontrollierte Umgebung mit geringem Volumen kann das reichen. Prüfen Sie parallele Checkouts, DB-Latenz, geplante Aktionen und Speicherdruck, bevor Sie die Umgebung als produktionsbereit ansehen.

### Reichen 4 GB RAM für WooCommerce? {#is-4-gb-ram-enough-for-woocommerce}

Für viele kleine Geschäftsshops sind 4 GB ein praktischer Einstieg. Hohe Zugriffszahlen, größere Kataloge und Datenbanken, viele Integrationen, Abonnements, Importe oder Verkaufsspitzen können mehr erfordern.

### Warum benötigt WooCommerce mehr Ressourcen als gewöhnliches WordPress? {#why-is-woocommerce-heavier-than-normal-wordpress}

Warenkorb, Checkout, Kundenkonto, Bestellungen, Lagerbestand und viele Integrationen sind dynamisch. Diese Anfragen führen weiterhin PHP- und Datenbankarbeit aus, selbst wenn öffentliche Katalog- und Inhaltsseiten gecacht sind.

### Kann ich den WooCommerce-Checkout cachen? {#can-i-cache-woocommerce-checkout}

Vollständiges Seiten-Caching sollte Warenkorb, Checkout und Mein Konto ausschließen, weil diese Seiten kundenspezifischen Zustand enthalten. Nutzen Sie andere Cache-Ebenen für dafür geeignete Daten und Inhalte.

### Braucht WooCommerce Redis? {#does-woocommerce-need-redis}

Nein. Redis oder Memcached können persistentes Objekt-Caching bereitstellen, wenn das Lastprofil davon profitiert. Sie ersetzen weder korrekte Seitencache-Ausnahmen noch effiziente Abfragen.

### Was ist HPOS? {#what-is-hpos}

High-Performance Order Storage speichert WooCommerce-Bestellungen in eigenen Tabellen. Seit WooCommerce 8.2 ist es bei Neuinstallationen standardmäßig aktiviert. Prüfen Sie bei Änderungen an einem bestehenden Shop die Kompatibilität von Erweiterungen und eigenem Code sowie kritische Shopabläufe.

### Was sind geplante Aktionen in WooCommerce? {#what-are-woocommerce-scheduled-actions}

Das sind vom Action Scheduler verwaltete Hintergrundaufgaben in einer Warteschlange, beispielsweise für Bestellbenachrichtigungen, zahlungsbezogene Verarbeitung, Webhooks und Erweiterungsaufgaben. Fehlgeschlagene oder überfällige Warteschlangen sind ein betriebliches Warnsignal.

### Ist WooCommerce bei VDSina vorinstalliert? {#does-vdsina-include-woocommerce-preinstalled}

Die aktuelle VDSina-Standard-Seite führt WooCommerce in den sichtbaren Vorlagen- und Anwendungsgruppen nicht als eigene vorinstallierte Anwendung auf. Prüfen Sie die aktuelle Bestelloberfläche, bevor Sie die Verfügbarkeit einer Vorlage voraussetzen.

### Ist ein VPS für WooCommerce immer besser als Managed Hosting? {#is-a-vps-always-better-for-woocommerce-than-managed-hosting}

Nein. Ein selbst verwalteter VPS ist sinnvoll, wenn Sie Kontrolle und Ressourcen benötigen und den Server betreiben können. Managed WooCommerce/WordPress Hosting kann sicherer sein, wenn der Shop geschäftskritisch ist und die Serveradministration keinen internen Verantwortlichen hat.
