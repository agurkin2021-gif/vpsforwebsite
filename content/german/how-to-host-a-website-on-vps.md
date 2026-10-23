---
title: "Website auf einem VPS hosten"
slug: "website-auf-einem-vps-hosten"
description: "Website auf einem VPS hosten: Bereitstellungsweg wählen, ersten Zugriff absichern, passenden Web-Stack installieren, Domain verbinden, HTTPS aktivieren, Neustart testen und Produktionsreife prüfen."
image: "images/home/vps-for-website-hero.webp"
---

Wie Sie eine Website auf einem VPS hosten, hängt von der bereitzustellenden Anwendung ab. Eine statische Website braucht einen Webserver und DNS. WordPress oder ein anderes PHP-CMS benötigt zusätzlich PHP und eine Datenbank. Eine Node.js- oder Python-Anwendung läuft gewöhnlich hinter einem Reverse Proxy. Sie können diese Komponenten manuell auf einem sauberen VPS einrichten oder sie mit einem Control Panel im Browser verwalten.

Diese Anleitung behandelt den Weg **vom neuen VPS zur erreichbaren Website**. Wenn Sie eine bestehende produktive Website mit laufend veränderten Daten umziehen, nutzen Sie [Website auf VPS umziehen]({{< relref "website-migration-to-vps.md" >}}) für Umstellung und Rollback.

Die grundsätzliche Kaufentscheidung behandelt [VPS für Websites]({{< relref "_index.md" >}}).

[Ablauf im Überblick](#quick-deployment-sequence) · [Weg wählen](#choose-manual-panel-or-managed) · [Bereitstellungscheck](#deployment-path-checker) · [Manueller Weg](#manual--no-control-panel-path) · [DNS](#point-the-domain-to-the-vps) · [Produktionscheckliste](#production-acceptance-checklist) · [FAQ](#faq)

## Bereitstellungsablauf im Überblick {#quick-deployment-sequence}

Eine zuverlässige erste Bereitstellung folgt dieser Reihenfolge:

1. **VPS auswählen und dimensionieren.**
2. **Manuelle, panelgestützte oder verwaltete Administration wählen.**
3. **Ein sauberes Betriebssystem oder ein aktuelles Panel-Image des Anbieters bereitstellen.**
4. **Den ersten Zugriff absichern und einen Administrationszugang ohne direkte Root-Anmeldung einrichten.**
5. **Das Betriebssystem aktualisieren.**
6. **Nur den Web-Stack installieren, den die Anwendung benötigt.**
7. **Website/Anwendung nach Möglichkeit vor der öffentlichen DNS-Umstellung konfigurieren.**
8. **Dateien/Code bereitstellen und Eigentümer, Geheimnisse sowie Datenbankzugriff konfigurieren.**
9. **Die Firewall einschränken, dabei SSH und erforderliche HTTP-/HTTPS-Zugriffe funktionsfähig halten.**
10. **Das Ziel vor der öffentlichen DNS-Umstellung testen.**
11. **Die Domain auf den VPS verweisen lassen.**
12. **HTTPS aktivieren, nachdem der Hostname den Server erreicht.**
13. **Cronjobs/Worker, Protokolle, Backups und externes Monitoring prüfen.**
14. **Einmal neu starten und prüfen, ob alle benötigten Dienste automatisch zurückkehren.**
15. **Erst danach gilt die Bereitstellung als produktionsreif.**

Installieren Sie PHP, MySQL, E-Mail-Dienste oder ein Control Panel nicht allein deshalb, weil eine allgemeine VPS-Anleitung diese enthält. Installieren Sie nur die Komponenten, die Ihre Website tatsächlich braucht.

## Manuell, mit Panel oder verwaltet {#choose-manual-panel-or-managed}

Es gibt drei unterschiedliche Betriebswege.

### Manuell / ohne Control Panel {#manual--no-control-panel}

Wählen Sie einen sauberen Linux-VPS und verwalten Sie den Stack per SSH.

Das passt gut, wenn:

- Sie den Anwendungs-Stack verstehen;
- Sie möglichst wenige Dienste betreiben möchten;
- Sie individuelle Nginx-/Apache-/Laufzeitkonfigurationen benötigen;
- Sie Skripte, Git oder Infrastructure as Code verwenden;
- Sie keine klassische Oberfläche für Hosting-Konten benötigen.

Hier ist das frühere Thema **VPS ohne Control Panel** integriert. Für dieselbe Suchabsicht wird keine weitere konkurrierende URL angelegt.

### Control Panel {#control-panel}

Nutzen Sie ein Hosting-Panel, wenn die browserbasierte Verwaltung von Websites, Domains, PHP, Datenbanken, E-Mail oder Nutzern spürbar wiederkehrende Arbeit abnimmt.

Siehe [VPS mit Control Panel]({{< relref "vps-with-control-panel.md" >}}). Wenn FASTPANEL bereits feststeht, nutzen Sie [VPS-Hosting mit FASTPANEL]({{< relref "fastpanel-vps-hosting.md" >}}).

### Verwaltete Administration {#managed-administration}

Panel und Management sind verschiedene Dinge. Wenn auf Ihrer Seite niemand Patches, Sicherheit, Backups, Monitoring und Störungen verantwortet, klären Sie das vor dem Start.

Siehe [Managed vs. Unmanaged VPS]({{< relref "managed-vs-unmanaged-vps.md" >}}).

## Bereitstellungsweg prüfen {#deployment-path-checker}

Dieses Werkzeug bestimmt den Stack-Weg, den Sie genauer untersuchen sollten. Es ersetzt nicht die Dokumentation der Anwendung.

<div class="rounded-2xl bg-light p-6 dark:bg-darkmode-light">
<form id="deployment-path-checker-form">
  <div class="mb-6">
    <label for="deploy-type" class="form-label">Website-/Anwendungstyp</label>
    <select id="deploy-type" class="form-input">
      <option value="static">Statisches HTML / generierte statische Website</option>
      <option value="php">WordPress / PHP-CMS</option>
      <option value="app">Node.js / Python / individuelle Anwendung</option>
    </select>
  </div>
  <div class="mb-6">
    <label for="deploy-panel" class="form-label">Bevorzugen Sie ein Hosting-Control-Panel?</label>
    <select id="deploy-panel" class="form-input"><option value="no">Nein / manuell</option><option value="yes">Ja</option></select>
  </div>
  <div class="mb-6">
    <label for="deploy-db" class="form-label">Benötigt die Anwendung eine lokale Datenbank?</label>
    <select id="deploy-db" class="form-input"><option value="no">Nein</option><option value="yes">Ja</option></select>
  </div>
  <div class="mb-6">
    <label for="deploy-mail" class="form-label">Postfächer auf demselben VPS hosten?</label>
    <select id="deploy-mail" class="form-input"><option value="no">Nein / externer Maildienst</option><option value="yes">Ja</option></select>
  </div>
  <div class="mb-6">
    <label for="deploy-sites" class="form-label">Anzahl aktiver Websites</label>
    <select id="deploy-sites" class="form-input"><option value="1">1</option><option value="few">2–5</option><option value="many">6+</option></select>
  </div>
  <button class="btn btn-primary" type="submit">Bereitstellungsweg wählen</button>
</form>
<p id="deployment-path-result" class="mt-6 rounded border border-border p-4 dark:border-darkmode-border" role="status" aria-live="polite">Wählen Sie Workload und bevorzugte Betriebsweise.</p>
</div>

<script>
document.addEventListener("DOMContentLoaded", function () {
  var form = document.getElementById("deployment-path-checker-form");
  if (!form) return;

  form.addEventListener("submit", function (event) {
    event.preventDefault();

    var type = document.getElementById("deploy-type").value;
    var panel = document.getElementById("deploy-panel").value === "yes";
    var db = document.getElementById("deploy-db").value === "yes";
    var mail = document.getElementById("deploy-mail").value === "yes";
    var sites = document.getElementById("deploy-sites").value;

    var result;

    if (panel) {
      result = "CONTROL-PANEL-WEG: Wählen Sie das Panel vor dem endgültigen Betriebssystem-Image. Prüfen Sie Betriebssystemkompatibilität, Panel-Ressourcenbedarf, Benutzer-/Website-Trennung, E-Mail-/DNS-Bedarf, Backups und Verwaltungsverantwortung.";
    } else if (type === "static" && !db && !mail) {
      result = "STATISCHER MANUELLER WEG: Sauberes Linux + SSH + Nginx oder Apache + Website-Dateien + DNS + HTTPS. Installieren Sie PHP oder eine Datenbank nur, wenn die Website diese tatsächlich benötigt.";
    } else if (type === "php") {
      result = "MANUELLER PHP-/WORDPRESS-WEG: Linux + SSH + Nginx/Apache + PHP-FPM + Datenbank bei Bedarf + DNS + HTTPS. Planen Sie RAM für PHP-Worker und Datenbank ein.";
    } else if (type === "app") {
      result = "ANWENDUNG MIT REVERSE PROXY: Betreiben Sie die Anwendung über einen eigenen Dienst/Prozessmanager ohne Root-Rechte, gewöhnlich auf localhost. Schalten Sie Nginx/Apache für den öffentlichen Hostnamen und HTTPS davor.";
    } else {
      result = "INDIVIDUELLER MANUELLER WEG: Gehen Sie von der dokumentierten Laufzeit der Anwendung aus und installieren Sie nur benötigte Dienste.";
    }

    if (sites === "many") {
      result += " Bei 6+ Websites müssen Benutzer und Berechtigungen pro Website ausdrücklich getrennt und die Gesamtlast geplant werden.";
    }
    if (mail) {
      result += " Lokale E-Mail-Dienste bringen zusätzliche Arbeit für SMTP/IMAP, DNS-Reputation, Speicher, Backup und Sicherheit mit sich. Prüfen Sie erneut, ob verwaltete externe Maildienste einfacher wären.";
    }

    document.getElementById("deployment-path-result").textContent = result;
  });
});
</script>

## Voraussetzungen {#prerequisites}

Bevor Sie am Server arbeiten, benötigen Sie:

- einen für den Workload dimensionierten VPS;
- die IP-Adresse des Servers;
- SSH-Zugangsdaten oder Schlüsselzugriff;
- einen funktionierenden Konsolen-/VNC-/Wiederherstellungszugang beim Anbieter;
- eine registrierte Domain und DNS-Zugriff;
- Website-Dateien oder das Anwendungs-Repository;
- die erforderlichen Laufzeitversionen;
- Datenbankanforderungen;
- einen Plan für Geheimnisse und Umgebungsvariablen;
- einen Backup-Speicherort;
- eine externe Möglichkeit, die Website-Erreichbarkeit zu testen.

Nutzen Sie vor der Bereitstellung [VPS-Dimensionierung für Websites]({{< relref "vps-sizing-for-website.md" >}}), falls der Ressourcenbedarf noch unklar ist.

Die aktuelle Standard-VPS-Seite von VDSina führt reine Betriebssystemvorlagen auf, darunter Ubuntu 26.04/24.04/22.04/20.04, Debian 13/12/11/10, AlmaLinux, Rocky, CentOS, Oracle Linux und ArchLinux. Diese Anleitung verwendet Beispiele nach Ubuntu-/Debian-Art, weil sich die aktuelle Webserver-Dokumentation und Paketverwaltung gut nachvollziehen lassen. Die Architektur gilt auch für andere unterstützte Linux-Distributionen mit abweichenden Paket- und Dienstbefehlen.

<p>
  <a class="btn btn-primary" href="https://www.vdsina.com/?partner=ni8gzrvz75" target="_blank" rel="sponsored nofollow noopener">VPS für die Website auswählen</a>
</p>
<p><small>Offenlegung: Der Herausgeber steht in einer beruflichen Beziehung zu VDSina. Diese Website kann eine Provision erhalten, wenn Sie über diesen Partnerlink bestellen. Wählen Sie Servergröße und Betriebsmodell anhand des Workloads, nicht anhand einer Provision.</small></p>

## Betriebssystem wählen {#choose-the-operating-system}

Wählen Sie für einen manuell verwalteten Website-Server ein Betriebssystem, das:

- von Anwendung und Laufzeit unterstützt wird;
- weiterhin gepflegt wird;
- Ihr Administrator kennt;
- aktuelle Pakete und Dokumentation für den Web-Stack bietet;
- die Anforderungen eines eventuell später eingesetzten Panels erfüllt.

Wählen Sie das Betriebssystem nicht allein deshalb, weil es das neueste ist. Anwendungskompatibilität und Erfahrung des Administrators sind wichtiger.

Für ein einfaches aktuelles Linux-Beispiel sind Ubuntu 24.04 LTS oder Debian 12 sinnvolle Dokumentationsgrundlagen. Schreibt der Anwendungshersteller eine andere unterstützte Distribution vor, folgen Sie dieser Anforderung.

## Ersten SSH-Zugriff absichern {#secure-first-ssh-access}

Ein neuer VPS gibt Ihnen administrativen Zugriff. Produktive Arbeit sollte aber nicht dauerhaft als Root erfolgen.

Ein sicherer Ablauf für den ersten Zugriff:

1. mit den vom VPS-Anbieter bereitgestellten Zugangsdaten oder Schlüsseln verbinden;
2. bestätigen, dass Server und IP dem gewünschten neuen Server entsprechen;
3. den Konsolen-/VNC-/Wiederherstellungsweg des Anbieters funktionsfähig halten;
4. einen namentlich zugeordneten Administratorbenutzer anlegen;
5. nur die erforderlichen sudo-/Administratorrechte vergeben;
6. nach Möglichkeit SSH-Schlüsselauthentifizierung hinzufügen;
7. die neue Anmeldung in einer zweiten Sitzung prüfen, **bevor** der ursprüngliche Zugang deaktiviert oder eingeschränkt wird.

Beispiel für Ubuntu/Debian:

```bash
ssh root@SERVER_IP
adduser deploy
usermod -aG sudo deploy
```

Sperren Sie beim „Härten“ des Servers nicht den einzigen funktionierenden Administrationszugang aus.

Die vertiefte SSH- und Firewall-Härtung behandelt die [VPS-Sicherheitscheckliste]({{< relref "vps-security-checklist.md" >}}). Diese Anleitung beschränkt sich auf das für die Bereitstellung erforderliche Minimum.

## Server vor der Stack-Installation aktualisieren {#update-the-server-before-installing-the-stack}

Unter Ubuntu/Debian:

```bash
sudo apt update
sudo apt upgrade -y
```

Starten Sie neu, wenn das Update es erfordert, und prüfen Sie anschließend die erneute Verbindung.

Verschieben Sie Sicherheitsupdates nicht auf die Zeit nach der Veröffentlichung der Website.

## Manueller Weg / ohne Control Panel {#manual--no-control-panel-path}

Ein manuell verwalteter VPS sollte nur die Dienste enthalten, die die Anwendung benötigt.

Die üblichen Varianten sind:

### Statische Website {#static-website}

Benötigt werden:

- Nginx oder Apache;
- Website-Dateien;
- DNS;
- HTTPS.

Nicht automatisch benötigt werden:

- PHP;
- MySQL/MariaDB/PostgreSQL;
- ein lokaler Mailserver.

### PHP-/WordPress-Website {#php--wordpress-website}

Gewöhnlich benötigt werden:

- Nginx oder Apache;
- PHP-FPM / PHP-Module;
- Datenbank;
- Website-Dateien/Uploads;
- DNS;
- HTTPS.

Das Ressourcenverhalten von WordPress behandelt [VPS für WordPress]({{< relref "vps-for-wordpress.md" >}}).

### Node.js / Python / individuelle Anwendung {#nodejs--python--custom-application}

Üblicherweise:

- Anwendungslaufzeit;
- eigener Anwendungsbenutzer ohne Root-Rechte;
- Prozessmanager/systemd-Dienst;
- Anwendung nach Möglichkeit an localhost oder einen privaten Socket gebunden;
- Nginx-/Apache-Reverse-Proxy;
- Datenbank nur bei Bedarf;
- DNS;
- HTTPS.

Veröffentlichen Sie einen Entwicklungsserver nicht direkt im Internet als produktive Architektur.

## Webserver installieren {#install-the-web-server}

Die aktuelle Ubuntu-Server-Dokumentation unterstützt sowohl Nginx als auch Apache. Keiner ist grundsätzlich „besser“.

Für das Nginx-Beispiel:

```bash
sudo apt update
sudo apt install nginx
sudo systemctl enable --now nginx
sudo systemctl status nginx
```

An diesem Punkt sollte die Server-IP die Nginx-Standardseite ausliefern, sofern Netzwerk und Firewall HTTP zulassen.

Verwenden Sie stattdessen Apache, wenn Anwendung, Team oder vorhandene Konfiguration besser dazu passen.

## Hostnamen der Website konfigurieren {#configure-the-website-hostname}

DNS und Webserver-Konfiguration sind zwei Teile derselben Aufgabe.

Der DNS-Anbieter muss den Hostnamen auf den VPS verweisen lassen, **und** der Webserver muss wissen, welche Website auf diesen Hostnamen antworten soll.

Legen Sie für Nginx einen Serverblock für die Domain an. Schematisch:

```nginx
server {
    listen 80;
    listen [::]:80;

    server_name example.com www.example.com;
    root /var/www/example.com/public;
    index index.html index.htm;

    location / {
        try_files $uri $uri/ =404;
    }
}
```

Unter Ubuntu/Debian liegen websitespezifische Konfigurationen üblicherweise unter:

- `/etc/nginx/sites-available/`
- `/etc/nginx/sites-enabled/`

Nach Änderungen:

```bash
sudo nginx -t
sudo systemctl reload nginx
```

Prüfen Sie vor dem Neuladen immer die Konfigurationssyntax.

Bei einer Anwendung hinter einem Reverse Proxy leitet der Serverblock die Anfragen stattdessen an den lokalen Anwendungsport oder Socket weiter.

## Dateien oder Anwendungscode bereitstellen {#deploy-files-or-application-code}

Wählen Sie eine wiederholbare Bereitstellungsmethode.

### SFTP/SCP {#sftpscp}

Geeignet für:

- kleine Websites;
- seltene manuelle Bereitstellungen;
- einfache Erstprojekte.

Risiko: Das Produktivverzeichnis kann leicht vom Quell-Repository abweichen.

### rsync über SSH {#rsync-over-ssh}

Nützlich für wiederholbare Dateisynchronisation und effiziente inkrementelle Updates.

### Git-basierte Bereitstellung {#git-based-deployment}

Nützlich, wenn produktive Releases konkreten Repository-Commits entsprechen sollen.

### CI/CD {#cicd}

Nützlich, wenn häufige Bereitstellungen automatisierte Build-, Test- und Release-Schritte rechtfertigen.

Unabhängig von der Methode:

- stellen Sie nicht als Root bereit, sofern die Aufgabe nicht tatsächlich Root-Rechte erfordert;
- lassen Sie Anwendungsdateien einem passenden Deployment-/Anwendungsbenutzer gehören;
- gewähren Sie dem Webserver nur den benötigten Zugriff;
- halten Sie Geheimnisse außerhalb öffentlich erreichbarer Dokumentverzeichnisse;
- verwenden Sie nicht als Abkürzung Schreibrechte für alle Nutzer.

## PHP-/WordPress-Weg {#php--wordpress-path}

Installieren Sie für eine PHP-Website unter Ubuntu/Debian die aktuellen unterstützten PHP-FPM-Pakete und die von der Anwendung benötigten Erweiterungen.

Typische Architektur:

**Browser -> Nginx/Apache -> PHP-FPM -> Datenbank**

Übernehmen Sie keine beliebige Erweiterungsliste eines anderen CMS. Installieren Sie, was die Anwendung tatsächlich benötigt.

Für WordPress:

- eine Datenbank und einen eigenen Datenbankbenutzer anlegen;
- PHP-Limits für Uploads, Speicher und Ausführungszeit am gemessenen Bedarf ausrichten;
- Geheimnisse in `wp-config.php` schützen;
- den Website-Hostnamen konfigurieren;
- HTTPS aktivieren;
- wp-cron und Hintergrundaufgaben prüfen;
- Caching passend zum Workload ergänzen.

Nutzen Sie für Dimensionierung und Performance [VPS für WordPress]({{< relref "vps-for-wordpress.md" >}}), statt diese Themen hier doppelt zu behandeln.

## Node.js-/Python-Weg und individuelle Anwendungen {#nodejs--python--custom-app-path}

Starten Sie nicht einfach den Entwicklungsbefehl manuell in einem Terminal und nennen Sie das Produktivbetrieb.

Nutzen Sie:

- einen eigenen Anwendungsbenutzer;
- eine Umgebungs-/Konfigurationsdatei mit eingeschränkten Berechtigungen;
- systemd oder einen geeigneten Prozessmanager für den Produktivbetrieb;
- automatischen Neustart bei Fehlern und Serverneustarts;
- einen lokalen/privaten Anwendungs-Listener;
- einen Nginx-/Apache-Reverse-Proxy;
- Anwendungsprotokolle;
- Zustandsprüfungen.

Typischer Ablauf:

**Browser -> HTTPS/Nginx -> Anwendung auf 127.0.0.1:PORT -> Datenbank/externe Dienste**

Prüfen Sie die Hinweise des Frameworks zur produktiven Bereitstellung.

## Datenbank nur bei Bedarf installieren {#database-install-only-when-required}

Eine statische Website benötigt keine Datenbank.

Für eine dynamische Anwendung mit Datenbankbedarf:

- die unterstützte Datenbank-Engine installieren;
- eine eigene Datenbank anlegen;
- einen anwendungsspezifischen Benutzer anlegen;
- nur benötigte Rechte vergeben;
- Zugangsdaten außerhalb des Webroots halten;
- den Datenbankport nicht öffentlich freigeben, sofern keine konkrete abgesicherte Architektur dies verlangt;
- die Datenbank in Backup- und Monitoring-Pläne aufnehmen.

Die Datenbankarbeit kann zum eigentlichen VPS-Engpass werden, obwohl der Webserver fast im Leerlauf ist.

## Dateieigentümer, Berechtigungen und Geheimnisse {#file-ownership-permissions-and-secrets}

Vermeiden Sie zwei häufige Fehler:

1. die Website als Root ausführen;
2. Anwendungsverzeichnisse für alle schreibbar machen, um Berechtigungsfehler zu „beheben“.

Stattdessen:

- einen Deployment-/Anwendungsbenutzer verwenden;
- verstehen, welcher Prozess Lese- und welcher Schreibzugriff benötigt;
- Upload-/Cache-Verzeichnissen nur die tatsächlich erforderlichen Schreibrechte geben;
- Umgebungsdateien und Zugangsdaten schützen;
- produktive Geheimnisse nicht in Git einchecken;
- private Schlüssel außerhalb öffentlich erreichbarer Dokumentverzeichnisse halten.

Die genaue Eigentümerzuordnung hängt von Anwendung und Webserver-Modell ab. Nutzen Sie die Anwendungsdokumentation, statt ein allgemeines `chmod 777`-Rezept zu kopieren.

## Vor der öffentlichen DNS-Umstellung testen {#test-before-public-dns}

Machen Sie die DNS-Umstellung nicht zum ersten echten Anwendungstest.

Prüfen Sie den neuen Server vor der öffentlichen Umstellung nach Möglichkeit mit einer dieser Methoden:

- Zugriff über die Server-IP für einen einfachen Standard-/Statiktest;
- lokaler hosts-Dateieintrag, sodass `example.com` nur auf Ihrem Computer auf den neuen VPS aufgelöst wird;
- privater/Test-Hostname, der nicht versehentlich als Duplikat indexiert werden darf;
- Anwendungstest über dieselbe Nginx-/Apache-Hostnamenkonfiguration wie im Produktivbetrieb.

Prüfen Sie mehr als die Startseite:

- wichtige Unterseiten;
- Anmeldung/Administration;
- Formulare;
- Uploads;
- statische Ressourcen;
- Datenbank-Lese- und Schreibvorgänge;
- Anwendungs-/API-Endpunkte;
- Weiterleitungen;
- Protokolle.

Ein Test über die hosts-Datei ist besonders hilfreich, weil sich viele Anwendungen unter dem echten Hostnamen anders verhalten als unter der reinen Server-IP.

Bei einer bereits produktiven Website verwenden Sie den strengeren Umstellungsablauf unter [Website auf VPS umziehen]({{< relref "website-migration-to-vps.md" >}}).

## Domain auf den VPS verweisen lassen {#point-the-domain-to-the-vps}

Konfigurieren Sie beim DNS-Anbieter die Einträge, die zu diesem Server führen sollen.

Typische IPv4-Konfiguration:

| Name | Typ | Wert |
|---|---|---|
| `@` | A | IPv4-Adresse des VPS |
| `www` | CNAME | Hauptdomain |

Für `www` ist auch ein A-Eintrag möglich.

Fügen Sie nur dann einen AAAA-Eintrag hinzu, wenn IPv6 auf dem VPS tatsächlich konfiguriert und erreichbar ist. Ein fehlerhafter AAAA-Eintrag kann Zugriffe mancher Besucher scheitern lassen, obwohl IPv4 funktioniert.

DNS allein macht die Website nicht funktionsfähig: Auch die Nginx-/Apache-Website-Konfiguration muss den passenden Hostnamen enthalten.

Beim Umzug einer bestehenden produktiven Website gehören DNS-Umstellung und Umgang mit letzten Schreibvorgängen zu [Website auf VPS umziehen]({{< relref "website-migration-to-vps.md" >}}).

## HTTPS nach erfolgreicher DNS-Auflösung ergänzen {#add-https-after-dns-resolves}

Fordern Sie ein vertrauenswürdiges Zertifikat erst an, wenn der öffentliche Hostname auf den Server aufgelöst wird, der die Validierungsanfrage beantworten soll. Stellen Sie sicher, dass Firewall und Netzwerkregeln des Anbieters den vorgesehenen HTTP-/HTTPS-Validierungsweg bereits zulassen.

Für Nginx/Apache kann ein ACME-Client wie Certbot Let's-Encrypt-Zertifikate anfordern und erneuern. Folgen Sie den aktuellen Certbot-/Betriebssystemanleitungen, statt einen alten Paketbefehl ungeprüft zu übernehmen.

Prüfen Sie:

- das Zertifikat deckt die verwendeten Hauptdomain- und `www`-Varianten ab;
- HTTP wird wie vorgesehen auf HTTPS weitergeleitet;
- Zertifikatserneuerung ist automatisiert;
- die Erneuerung funktioniert durch Firewall-/CDN-Konfiguration hindurch;
- die Anwendung erzeugt korrekte HTTPS-URLs.

Aktivieren Sie keine HTTPS-Weiterleitung, bevor Sie wissen, dass die Zertifikatsbereitstellung funktioniert.

## Firewall konfigurieren {#configure-the-firewall}

Halten Sie den administrativen Zugriff während der Änderung von Firewall-Regeln funktionsfähig.

Eine einfache öffentliche Website benötigt gewöhnlich:

- SSH von der benötigten Administrationsquelle beziehungsweise über den vorgesehenen Zugangsweg;
- TCP 80 für HTTP/ACME/Weiterleitungen;
- TCP 443 für HTTPS.

Geben Sie MySQL/PostgreSQL, Redis oder interne Anwendungsports nicht öffentlich frei, nur weil sie lokal standardmäßig auf Verbindungen warten.

Erlauben Sie auf einem Server mit UFW den benötigten SSH-Zugang, **bevor** Sie einschränkende Regeln aktivieren.

Ausführliche Firewall- und Härtungsdetails gehören zur [VPS-Sicherheitscheckliste]({{< relref "vps-security-checklist.md" >}}).

## Cronjobs, Warteschlangen und Worker {#cron-jobs-queues-and-workers}

Dynamische Websites scheitern nach der Bereitstellung oft daran, dass nur die Verarbeitung von Webanfragen eingerichtet wurde.

Erfassen Sie:

- Cronjobs;
- Warteschlangen-Worker;
- geplante Aktionen;
- Importe/Exporte;
- E-Mail-Aufgaben;
- Cache-Aufwärmung;
- Hintergrundverarbeitung.

Stellen Sie sicher, dass diese:

- unter dem richtigen Benutzer ohne Root-Rechte laufen;
- bei Bedarf automatisch starten;
- in bekannte Protokolle schreiben;
- sich nicht so überschneiden, dass CPU/RAM erschöpft werden;
- einen Serverneustart überstehen.

## Protokolle und grundlegende Beobachtbarkeit {#logs-and-basic-observability}

Vor produktivem Datenverkehr müssen Sie wissen, wo Sie bei einem Ausfall nachsehen.

Bestimmen Sie mindestens:

- Nginx-/Apache-Zugriffsprotokoll;
- Nginx-/Apache-Fehlerprotokoll;
- Anwendungsprotokoll;
- PHP-FPM-/Laufzeitprotokoll;
- Datenbankprotokoll/-status;
- Systemjournal;
- Speicherplatzbelegung;
- RAM-/CPU-Engpässe.

Ergänzen Sie eine externe HTTP(S)-Erreichbarkeitsprüfung, damit ein Serverausfall auch dann sichtbar wird, wenn niemand am VPS angemeldet ist.

Die vertiefte Auslegung von Schwellenwerten und Alarmen behandelt [VPS-Monitoring]({{< relref "vps-monitoring.md" >}}).

## Neustart prüfen {#reboot-validation}

Überraschend viele erste VPS-Bereitstellungen funktionieren nur bis zum ersten Neustart.

Bevor Sie den Server für einsatzbereit erklären:

```bash
sudo reboot
```

Prüfen Sie nach seiner Rückkehr:

- SSH-Zugriff;
- Nginx/Apache;
- PHP-FPM oder Anwendungsdienst;
- Datenbank;
- Cronjobs/Warteschlangen-Worker;
- HTTPS;
- Website-Seiten/Formulare;
- Monitoring;
- Backup-Zeitplan.

Wenn die Anwendung erst zurückkehrt, nachdem jemand manuell einen Befehl ausführt, ist die Bereitstellung noch nicht vollständig.

## Wann manuelles Hosting ohne Panel nicht passt {#when-manual--no-panel-hosting-is-the-wrong-fit}

Nutzen Sie stattdessen ein Control Panel oder verwaltete Administration, wenn:

- niemand sicher mit SSH und Wiederherstellung über die Kommandozeile umgehen kann;
- niemand Betriebssystem- und Sicherheitsupdates verantwortet;
- niemand Fehler von Webserver, Laufzeit oder Datenbank diagnostizieren kann;
- Backups erstellt werden, aber niemand sie wiederherstellen kann;
- für geschäftskritische Ausfallzeiten kein Verantwortlicher feststeht;
- das Team E-Mail, Nutzer und Domains über eine Hosting-Oberfläche statt über Serverkonfiguration verwalten möchte;
- der Anwendungs-Stack auf einer verwalteten Plattform besser aufgehoben ist.

Ein manueller VPS kann den zusätzlichen Ressourcenbedarf eines Panels vermeiden und maximale Kontrolle bieten. Er verringert aber nicht die Betriebsverantwortung.

Nutzen Sie [VPS mit Control Panel]({{< relref "vps-with-control-panel.md" >}}) für die Panel-Auswahl oder [Managed vs. Unmanaged VPS]({{< relref "managed-vs-unmanaged-vps.md" >}}), wenn eine verantwortliche Instanz für den Betrieb fehlt.

## Checkliste für die Produktionsabnahme {#production-acceptance-checklist}

| Prüfung | Erfolgskriterium |
|---|---|
| Serverzugriff | zugeordneter Administrator kann sich anmelden; Wiederherstellungskonsole bleibt erreichbar |
| Updates | aktuelle Sicherheits-/Systemupdates installiert |
| Webserver | startet automatisch; Konfigurationstest erfolgreich |
| Website-Hostname | Verhalten von Hauptdomain/`www` bewusst festgelegt |
| DNS | A/AAAA/CNAME werden zum vorgesehenen Server/Zugangsweg aufgelöst |
| HTTPS | vertrauenswürdiges Zertifikat, korrekte Namen, Erneuerungsweg verstanden |
| Anwendung | repräsentative Seiten, Anmeldung, Formulare und Uploads funktionieren |
| Datenbank | Anwendungsbenutzer funktioniert; Datenbankport nicht versehentlich öffentlich |
| Dateien | korrekte Eigentümer; kein `777`-Behelf |
| Aufgaben | Cronjobs/Worker starten und protokollieren korrekt |
| Neustart | benötigte Dienste kommen automatisch zurück |
| Protokolle | Betreiber weiß, wo Web-/Anwendungs-/Systemfehler erscheinen |
| Backup | erforderliche Dateien/Datenbank enthalten; Wiederherstellungsweg festgelegt |
| Monitoring | externe Website-Prüfung plus grundlegende Ressourcentransparenz |
| Kapazität | CPU/RAM/Datenträger unter realem Workload geprüft |

Eine Website ist nicht allein deshalb produktionsreif, weil die Startseite HTTP 200 liefert.

## Übergabe an Backup und Monitoring {#backups-and-monitoring-handoff}

Diese Seite legt nur die erforderlichen Mindestmaßnahmen für die Übergabe fest.

Bevor Sie sich auf die Website verlassen:

- Backups planen;
- eine unabhängige Kopie außerhalb des Servers vorhalten;
- Datenbank sowie für die Wiederherstellung nötige Konfigurationen und Geheimnisse einbeziehen;
- Wiederherstellbarkeit prüfen;
- Website-Erreichbarkeit überwachen;
- Speicherplatzwachstum überwachen;
- CPU-/RAM-/Datenbankengpässe beobachten;
- Zertifikatserneuerung überwachen.

Das ausführliche Wiederherstellungskonzept gehört zur [VPS-Backup-Strategie]({{< relref "vps-backup-strategy.md" >}}). Monitoring-Schwellenwerte und Alarmkonzepte gehören zu [VPS-Monitoring]({{< relref "vps-monitoring.md" >}}).

## Mehrere Websites {#multiple-websites}

Für mehrere Websites:

- einen eigenen Serverblock/virtuellen Host pro Hostname verwenden;
- Dokumentverzeichnisse trennen;
- eigene Anwendungs- und Datenbank-Zugangsdaten verwenden;
- getrennte Systemnutzer einsetzen, wenn das Vertrauensmodell es verlangt;
- verhindern, dass Cronjobs, Importe oder Backups einer Website den anderen Ressourcen entziehen;
- gemeinsame Lastspitzen berücksichtigen;
- verstehen, dass weiterhin alle Websites die gemeinsame Ausfallumgebung eines VPS teilen.

Nutzen Sie [VPS für mehrere Websites]({{< relref "vps-for-multiple-websites.md" >}}) für Kapazitäts- und Trennungsplanung.

## Technische Referenzen {#technical-references}

- Ubuntu Server: Nginx installieren
- Ubuntu Server: Nginx konfigurieren
- Ubuntu Server: Webdienste
- VDSina Standard VPS — aktuelle reine Betriebssystemvorlagen

<p>
  <a class="btn btn-primary" href="https://www.vdsina.com/?partner=ni8gzrvz75" target="_blank" rel="sponsored nofollow noopener">VPS für Ihre Website auswählen</a>
</p>
<p><small>Offenlegung: Der Herausgeber steht in einer beruflichen Beziehung zu VDSina. Partnerlinks sind als gesponsert gekennzeichnet. Prüfen Sie vor der Bestellung aktuelle VPS-Preise, verfügbare Betriebssysteme und Anbieterbedingungen.</small></p>

## FAQ {#faq}

### Kann ich eine Website auf einem VPS ohne Control Panel hosten? {#can-i-host-a-website-on-a-vps-without-a-control-panel}

Ja. Ein sauberer Linux-VPS kann eine Website mit SSH und den von der Anwendung benötigten Webserver-, Laufzeit- und Datenbankkomponenten hosten. Dieses Thema ist Teil der vorliegenden Anleitung und erhält keine separate konkurrierende Seite.

### Brauche ich Nginx, um eine Website auf einem VPS zu hosten? {#do-i-need-nginx-to-host-a-website-on-vps}

Nein. Nginx und Apache sind beide verbreitet. Nutzen Sie den Webserver, der zu Anwendung, Konfiguration und Erfahrung des Administrators passt.

### Braucht jede Website auf einem VPS eine Datenbank? {#does-every-vps-website-need-a-database}

Nein. Statische Websites benötigen keine. Installieren Sie MySQL/MariaDB/PostgreSQL nur, wenn die Anwendung eine Datenbank braucht.

### Sollte ich die Website als Root betreiben? {#should-i-use-root-to-host-the-website}

Nein. Root ist für Administration vorgesehen. Betreiben und veröffentlichen Sie die Website mit passenden Nutzern und Diensten ohne Root-Rechte, die nur die erforderlichen Berechtigungen erhalten.

### Wann sollte ich ein Control Panel verwenden? {#when-should-i-use-a-control-panel}

Wenn die browserbasierte Verwaltung von Websites, Domains, PHP, Datenbanken, Nutzern, E-Mail oder Backups genug wiederkehrende Administration abnimmt, um Ressourcenbedarf und Einschränkungen zu rechtfertigen.

### Kann ich WordPress auf einem VPS ohne cPanel hosten? {#can-i-host-wordpress-on-a-vps-without-cpanel}

Ja. WordPress braucht einen kompatiblen Webserver, PHP, eine Datenbank, die WordPress-Dateien, korrekte Berechtigungen, DNS und HTTPS. Ein Panel ist optional.

### Wann sollte DNS auf den VPS zeigen? {#when-should-i-point-dns-to-the-vps}

Bei einer neuen Website, sobald der Server den echten Hostnamen bedienen kann. Bei einer bestehenden produktiven Website zuerst testen und einen kontrollierten Migrations-/Umstellungsplan verwenden.

### Warum zeigt meine Domain auf den VPS, aber die falsche Website erscheint? {#why-does-my-domain-point-to-the-vps-but-show-the-wrong-site}

DNS führt den Hostnamen nur zur Server-IP. Nginx/Apache benötigt zusätzlich einen passenden Serverblock beziehungsweise virtuellen Host für diesen Hostnamen.

### Wann sollte ich HTTPS aktivieren? {#when-should-i-enable-https}

Nachdem der öffentliche Hostname zum Server aufgelöst wird und der Validierungsweg funktioniert. Stellen Sie dann das Zertifikat aus, prüfen Sie die Abdeckung von Hauptdomain/`www` und richten Sie die gewünschte HTTP-zu-HTTPS-Weiterleitung ein.

### Was sollte ich nach einem VPS-Neustart prüfen? {#what-should-i-check-after-rebooting-the-vps}

Prüfen Sie, dass Webserver, Anwendungsdienst/PHP-FPM, Datenbank, Worker, HTTPS, Monitoring und Website ohne manuelles Eingreifen wieder verfügbar sind.
