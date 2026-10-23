---
title: "Come ospitare un sito web su VPS"
description: "Come ospitare un sito web su VPS: scegli il percorso, proteggi il primo accesso, installa lo stack corretto, collega il dominio, attiva HTTPS e verifica riavvio e idoneità alla produzione."
image: "images/home/vps-for-website-hero.webp"
slug: "come-ospitare-un-sito-web-su-vps"
---

Come ospitare un sito web su VPS dipende dall’applicazione. Un sito statico richiede server web e DNS. WordPress o un altro CMS PHP richiedono anche PHP e database. Un’app Node.js o Python funziona in genere dietro un reverse proxy. Puoi configurare questi componenti manualmente su un VPS pulito oppure gestirli dal browser con un pannello.

Questa guida copre il percorso **dal VPS nuovo al sito online**. Se trasferisci un sito di produzione con dati attivi, usa [Migrazione di un sito web su VPS]({{< relref "website-migration-to-vps.md" >}}) per passaggio e rollback.

Per la scelta di acquisto complessiva, consulta [VPS per siti web]({{< relref "_index.md" >}}).

[Sequenza rapida](#quick-deployment-sequence) · [Scelta del percorso](#choose-manual-panel-or-managed) · [Verifica del percorso](#deployment-path-checker) · [Percorso manuale](#manual--no-control-panel-path) · [DNS](#point-the-domain-to-the-vps) · [Checklist di produzione](#production-acceptance-checklist) · [Domande frequenti](#faq)

## Sequenza rapida di installazione {#quick-deployment-sequence}

Una prima installazione affidabile segue questo ordine:

1. **Scegli e dimensiona il VPS.**
2. **Scegli amministrazione manuale, tramite pannello o gestita.**
3. **Installa un OS pulito o l’immagine attuale del provider con pannello.**
4. **Proteggi il primo accesso e crea un accesso amministrativo non root.**
5. **Aggiorna il sistema operativo.**
6. **Installa solo lo stack web necessario all’applicazione.**
7. **Configura sito e applicazione prima del cambio DNS pubblico, quando possibile.**
8. **Distribuisci file e codice, configura proprietà, segreti e accesso DB.**
9. **Limita il firewall mantenendo funzionanti SSH e gli accessi HTTP/HTTPS necessari.**
10. **Testa la destinazione prima del cambio DNS pubblico.**
11. **Punta il dominio al VPS.**
12. **Attiva HTTPS quando il nome host raggiunge il server.**
13. **Verifica cron, worker, log, backup e monitoraggio esterno.**
14. **Riavvia una volta e conferma il ritorno automatico di tutti i servizi necessari.**
15. **Solo allora considera l’installazione pronta per la produzione.**

Non installare PHP, MySQL, posta o un pannello solo perché compaiono in una guida generica. Installa i componenti che servono davvero al sito.

## Scegli gestione manuale, pannello o servizio gestito {#choose-manual-panel-or-managed}

Esistono tre percorsi operativi distinti.

### Manuale / senza pannello {#manual--no-control-panel}

Scegli un VPS Linux pulito e amministra lo stack tramite SSH.

Adatto quando:

- conosci lo stack applicativo;
- vuoi ridurre al minimo i servizi;
- serve una configurazione personalizzata di Nginx/Apache/runtime;
- usi script, Git o infrastruttura come codice;
- non serve un’interfaccia tradizionale per account di hosting.

Questa guida include il precedente tema **VPS senza pannello di controllo**. Non creiamo un altro URL concorrente per lo stesso intento.

### Pannello di controllo {#control-panel}

Usa un pannello quando gestire dal browser siti, domini, PHP, database, posta o utenti elimina una quantità significativa di lavoro ripetitivo.

Vedi [VPS con pannello di controllo]({{< relref "vps-with-control-panel.md" >}}). Se hai già scelto FASTPANEL, consulta [Hosting VPS con FASTPANEL]({{< relref "fastpanel-vps-hosting.md" >}}).

### Amministrazione gestita {#managed-administration}

Pannello e gestione sono distinti. Se nessuno dalla tua parte si occupa di aggiornamenti, sicurezza, backup, monitoraggio e incidenti, risolvi il problema prima del lancio.

Vedi [VPS gestito o non gestito]({{< relref "managed-vs-unmanaged-vps.md" >}}).

## Verifica del percorso di installazione {#deployment-path-checker}

Questo strumento individua lo stack da approfondire. Non sostituisce la documentazione dell’applicazione.

<div class="rounded-2xl bg-light p-6 dark:bg-darkmode-light">
<form id="deployment-path-checker-form">
  <div class="mb-6">
    <label for="deploy-type" class="form-label">Tipo di sito / applicazione</label>
    <select id="deploy-type" class="form-input">
      <option value="static">HTML statico / sito statico generato</option>
      <option value="php">WordPress / CMS PHP</option>
      <option value="app">Node.js / Python / applicazione personalizzata</option>
    </select>
  </div>
  <div class="mb-6">
    <label for="deploy-panel" class="form-label">Preferisci un pannello di hosting?</label>
    <select id="deploy-panel" class="form-input"><option value="no">No / gestione manuale</option><option value="yes">Sì</option></select>
  </div>
  <div class="mb-6">
    <label for="deploy-db" class="form-label">L’applicazione richiede un database locale?</label>
    <select id="deploy-db" class="form-input"><option value="no">No</option><option value="yes">Sì</option></select>
  </div>
  <div class="mb-6">
    <label for="deploy-mail" class="form-label">Vuoi ospitare la posta sullo stesso VPS?</label>
    <select id="deploy-mail" class="form-input"><option value="no">No / posta esterna</option><option value="yes">Sì</option></select>
  </div>
  <div class="mb-6">
    <label for="deploy-sites" class="form-label">Numero di siti attivi</label>
    <select id="deploy-sites" class="form-input"><option value="1">1</option><option value="few">2–5</option><option value="many">6+</option></select>
  </div>
  <button class="btn btn-primary" type="submit">Scegli il percorso</button>
</form>
<p id="deployment-path-result" class="mt-6 rounded border border-border p-4 dark:border-darkmode-border" role="status" aria-live="polite">Seleziona il carico e la modalità di gestione preferita.</p>
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
      result = "PERCORSO CON PANNELLO: scegli il pannello prima dell’immagine OS definitiva. Verifica compatibilità, consumo di risorse, isolamento di utenti e siti, posta/DNS, backup e responsabilità di gestione.";
    } else if (type === "static" && !db && !mail) {
      result = "PERCORSO STATICO MANUALE: Linux pulito + SSH + Nginx o Apache + file del sito + DNS + HTTPS. Installa PHP o un database solo se il sito ne ha davvero bisogno.";
    } else if (type === "php") {
      result = "PERCORSO MANUALE PHP / WORDPRESS: Linux + SSH + Nginx/Apache + PHP-FPM + database se necessario + DNS + HTTPS. Prevedi RAM per worker PHP e database.";
    } else if (type === "app") {
      result = "PERCORSO APP + REVERSE PROXY: esegui l’applicazione con un proprio servizio o gestore di processi non root, di solito su localhost, e metti Nginx/Apache davanti per nome host pubblico e HTTPS.";
    } else {
      result = "PERCORSO MANUALE PERSONALIZZATO: parti dal runtime documentato dell’applicazione e installa solo i servizi necessari.";
    }

    if (sites === "many") {
      result += " Con 6+ siti, aggiungi utenti e permessi espliciti per sito e pianifica il carico complessivo.";
    }
    if (mail) {
      result += " La posta locale aggiunge SMTP/IMAP, reputazione DNS, spazio, backup e sicurezza: valuta se la posta esterna gestita sia più semplice.";
    }

    document.getElementById("deployment-path-result").textContent = result;
  });
});
</script>

## Prerequisiti {#prerequisites}

Prima di intervenire sul server, procurati:

- un VPS dimensionato per il carico;
- l’indirizzo IP del server;
- credenziali SSH o accesso con chiave;
- console, VNC o procedura di recupero del provider funzionanti;
- un dominio registrato e accesso ai DNS;
- file del sito o repository dell’applicazione;
- versioni dei runtime necessarie;
- requisiti del database;
- un piano per segreti e variabili d’ambiente;
- una destinazione dei backup;
- un modo esterno per verificare la disponibilità del sito.

Consulta [Dimensionamento VPS per siti web]({{< relref "vps-sizing-for-website.md" >}}) prima dell’installazione se le risorse necessarie sono ancora incerte.

La pagina attuale VDSina Standard VPS elenca immagini OS tra cui Ubuntu 26.04/24.04/22.04/20.04, Debian 13/12/11/10, AlmaLinux, Rocky, CentOS, Oracle Linux e ArchLinux. Questa guida usa esempi in stile Ubuntu/Debian per la chiarezza della documentazione web e della gestione dei pacchetti; l’architettura si applica ad altre distribuzioni Linux supportate con comandi diversi per pacchetti e servizi.

<p>
  <a class="btn btn-primary" href="https://www.vdsina.com/?partner=ni8gzrvz75" target="_blank" rel="sponsored nofollow noopener">Scegli un VPS per il sito</a>
</p>
<p><small>Trasparenza: l’autore ha un rapporto professionale con VDSina e questo sito può ricevere una commissione se acquisti tramite questo link partner. Scegli dimensione del server e modello operativo in base al carico, non alla commissione.</small></p>

## Scegli il sistema operativo {#choose-the-operating-system}

Per un server web manuale, scegli un OS che:

- sia supportato da applicazione e runtime;
- riceva ancora manutenzione;
- sia conosciuto dall’amministratore;
- abbia pacchetti e documentazione aggiornati per lo stack web;
- rispetti i requisiti di un eventuale pannello futuro.

Non scegliere l’OS solo perché è il più nuovo. Compatibilità applicativa e familiarità dell’amministratore contano di più.

Per un semplice esempio Linux attuale, Ubuntu 24.04 LTS o Debian 12 sono riferimenti ragionevoli. Se il produttore dell’applicazione richiede un’altra distribuzione supportata, segui quel requisito.

## Proteggi il primo accesso SSH {#secure-first-ssh-access}

Un VPS nuovo offre accesso amministrativo, ma il lavoro in produzione non dovrebbe svolgersi stabilmente come root.

Una sequenza sicura di primo accesso è:

1. connettiti con credenziali o chiave fornite dal provider;
2. conferma che server e IP siano quelli previsti;
3. mantieni funzionante console, VNC o recupero del provider;
4. crea un utente amministrativo nominativo;
5. assegna solo i privilegi sudo/amministrativi necessari;
6. aggiungi autenticazione SSH con chiave quando possibile;
7. verifica il nuovo accesso in una seconda sessione **prima** di disabilitare o limitare quello originale.

Esempio su Ubuntu/Debian:

```bash
ssh root@SERVER_IP
adduser deploy
usermod -aG sudo deploy
```

Non bloccare l’unico accesso amministrativo funzionante mentre metti in sicurezza il server.

La protezione approfondita di SSH e firewall è trattata in [Checklist di sicurezza VPS]({{< relref "vps-security-checklist.md" >}}); qui manteniamo il minimo necessario all’installazione.

## Aggiorna il server prima di installare lo stack {#update-the-server-before-installing-the-stack}

Su Ubuntu/Debian:

```bash
sudo apt update
sudo apt upgrade -y
```

Riavvia se l’aggiornamento lo richiede e verifica di poterti riconnettere.

Non rimandare gli aggiornamenti di sicurezza a dopo la pubblicazione del sito.

## Percorso manuale / senza pannello {#manual--no-control-panel-path}

Un VPS manuale dovrebbe contenere solo i servizi necessari all’applicazione.

Le scelte comuni sono:

### Sito statico {#static-website}

Necessari:

- Nginx o Apache;
- file del sito;
- DNS;
- HTTPS.

Non automaticamente necessari:

- PHP;
- MySQL/MariaDB/PostgreSQL;
- server di posta locale.

### Sito PHP / WordPress {#php--wordpress-website}

Di solito necessari:

- Nginx o Apache;
- PHP-FPM / moduli PHP;
- database;
- file del sito e caricamenti;
- DNS;
- HTTPS.

Per il consumo di risorse WordPress, consulta [VPS per WordPress]({{< relref "vps-for-wordpress.md" >}}).

### Node.js / Python / applicazione personalizzata {#nodejs--python--custom-application}

Di solito:

- runtime applicativo;
- utente applicativo dedicato non root;
- gestore di processi / servizio systemd;
- app in ascolto su localhost o socket privato quando possibile;
- reverse proxy Nginx/Apache;
- database solo se necessario;
- DNS;
- HTTPS.

Non esporre direttamente a Internet un server di sviluppo come architettura di produzione.

## Installa il server web {#install-the-web-server}

La documentazione server attuale di Ubuntu supporta Nginx e Apache. Nessuno è universalmente «migliore».

Per l’esempio Nginx:

```bash
sudo apt update
sudo apt install nginx
sudo systemctl enable --now nginx
sudo systemctl status nginx
```

A questo punto l’IP del server dovrebbe mostrare la pagina predefinita Nginx, se rete e firewall consentono HTTP.

Usa Apache se si adatta meglio all’applicazione, al team o alla configurazione esistente.

## Configura il nome host del sito {#configure-the-website-hostname}

DNS e configurazione del server web sono due parti dello stesso lavoro.

Il provider DNS deve puntare il nome host al VPS **e** il server web deve sapere quale sito deve rispondere a quel nome.

Per Nginx, crea un blocco server per il dominio. In termini generali:

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

Su Ubuntu/Debian, le configurazioni dei singoli siti si trovano comunemente in:

- `/etc/nginx/sites-available/`
- `/etc/nginx/sites-enabled/`

Dopo le modifiche:

```bash
sudo nginx -t
sudo systemctl reload nginx
```

Verifica sempre la sintassi prima di ricaricare la configurazione.

Per un’app dietro reverse proxy, il blocco server inoltra invece le richieste alla porta o al socket locale dell’applicazione.

## Distribuisci file o codice applicativo {#deploy-files-or-application-code}

Scegli un metodo ripetibile.

### SFTP/SCP {#sftpscp}

Adatto a:

- piccoli siti;
- distribuzioni manuali poco frequenti;
- primi progetti semplici.

Rischio: la directory di produzione può facilmente divergere dal repository sorgente.

### rsync tramite SSH {#rsync-over-ssh}

Utile per sincronizzazioni ripetibili dei file e aggiornamenti incrementali efficienti.

### Distribuzione basata su Git {#git-based-deployment}

Utile quando le versioni in produzione devono corrispondere a commit del repository.

### CI/CD {#cicd}

Utile quando la frequenza delle distribuzioni giustifica fasi automatiche di build, test e rilascio.

Qualunque metodo usi:

- non distribuire come root, salvo effettiva necessità;
- assegna i file a un utente di distribuzione o applicazione appropriato;
- concedi al server web solo l’accesso necessario;
- tieni i segreti fuori dalle document root pubbliche;
- non usare permessi di scrittura per tutti come scorciatoia.

## Percorso PHP / WordPress {#php--wordpress-path}

Per un sito PHP su Ubuntu/Debian, installa i pacchetti PHP-FPM supportati attuali e le estensioni richieste dall’applicazione.

Architettura tipica:

**browser -> Nginx/Apache -> PHP-FPM -> database**

Non copiare un elenco casuale di estensioni da un altro CMS. Installa ciò che l’applicazione richiede davvero.

Per WordPress:

- crea un database e un utente DB dedicato;
- configura limiti PHP di caricamento, memoria ed esecuzione in base alle esigenze misurate;
- proteggi i segreti di `wp-config.php`;
- configura il nome host del sito;
- attiva HTTPS;
- verifica wp-cron e attività in background;
- aggiungi la cache in base al carico.

Usa [VPS per WordPress]({{< relref "vps-for-wordpress.md" >}}) per dimensionamento e prestazioni, senza duplicarli qui.

## Percorso Node.js / Python / app personalizzata {#nodejs--python--custom-app-path}

Non lanciare il comando di sviluppo in un terminale considerandolo una configurazione di produzione.

Usa:

- un utente applicativo dedicato;
- file di ambiente e configurazione con permessi limitati;
- systemd o un gestore di processi adatto alla produzione;
- riavvio automatico dopo errori o riavvio del server;
- app in ascolto su interfaccia locale/privata;
- reverse proxy Nginx/Apache;
- log applicativi;
- controlli di stato.

Flusso tipico:

**browser -> HTTPS/Nginx -> applicazione su 127.0.0.1:PORT -> database/servizi esterni**

Verifica le indicazioni di produzione del framework.

## Database: installalo solo se necessario {#database-install-only-when-required}

Un sito statico non ha bisogno di database.

Per un’app dinamica che lo richiede:

- installa il motore DB supportato;
- crea un database dedicato;
- crea un utente specifico dell’applicazione;
- assegna solo i privilegi necessari;
- tieni le credenziali fuori dalla web root;
- non esporre pubblicamente la porta DB, salvo un’architettura specifica e protetta che lo richieda;
- includi il database nei piani di backup e monitoraggio.

Il database può diventare il vero collo di bottiglia del VPS anche quando il server web è quasi inattivo.

## Proprietà dei file, permessi e segreti {#file-ownership-permissions-and-secrets}

Evita due errori comuni:

1. eseguire il sito come root;
2. rendere le directory scrivibili da tutti per «risolvere» errori di permessi.

Invece:

- usa un utente di distribuzione/applicazione;
- identifica quali processi richiedono lettura e quali scrittura;
- concedi alle directory di caricamento e cache solo la scrittura necessaria;
- proteggi file d’ambiente e credenziali;
- non inserire segreti di produzione in Git;
- tieni le chiavi private fuori dalle document root pubbliche.

La proprietà corretta dipende da applicazione e modello del server web: segui la documentazione anziché copiare una ricetta universale con `chmod 777`.

## Testa prima del cambio DNS pubblico {#test-before-public-dns}

Non fare del cambio DNS il primo vero test dell’applicazione.

Prima del passaggio pubblico, verifica il nuovo server con uno di questi metodi, quando possibile:

- accedi all’IP per un controllo semplice della pagina predefinita o statica;
- modifica il file hosts locale affinché `example.com` punti al nuovo VPS solo sul tuo computer;
- usa un nome host privato o di test che non possa diventare per errore un duplicato indicizzato;
- testa l’app tramite la stessa configurazione Nginx/Apache del nome host usata in produzione.

Controlla più della homepage:

- pagine interne importanti;
- accesso e amministrazione;
- moduli;
- caricamenti;
- risorse statiche;
- letture e scritture DB;
- endpoint applicativi/API;
- reindirizzamenti;
- log.

Il test tramite file hosts è utile perché molte app si comportano diversamente con il nome host reale rispetto al solo IP.

Per un sito già online, usa la procedura più rigorosa di [Migrazione di un sito web su VPS]({{< relref "website-migration-to-vps.md" >}}).

## Punta il dominio al VPS {#point-the-domain-to-the-vps}

Presso il provider DNS, configura i record che devono raggiungere il server.

Configurazione IPv4 tipica:

| Nome | Tipo | Valore |
|---|---|---|
| `@` | A | Indirizzo IPv4 del VPS |
| `www` | CNAME | Dominio principale |

Per `www` è possibile anche un record A.

Aggiungi un record AAAA solo se IPv6 è effettivamente configurato e raggiungibile sul VPS. Un AAAA errato può impedire l’accesso ad alcuni visitatori anche se IPv4 funziona.

I DNS da soli non fanno funzionare il sito: Nginx/Apache deve avere il nome host corrispondente nella configurazione.

Per un sito già in produzione, cambio DNS e gestione delle ultime scritture sono trattati in [Migrazione di un sito web su VPS]({{< relref "website-migration-to-vps.md" >}}).

## Aggiungi HTTPS dopo la risoluzione DNS {#add-https-after-dns-resolves}

Ottieni un certificato attendibile solo quando il nome host pubblico punta al server che risponderà alla validazione. Verifica che firewall e regole di rete del provider consentano già il percorso HTTP/HTTPS previsto per la verifica.

Per Nginx/Apache, un client ACME come Certbot può richiedere e rinnovare certificati Let’s Encrypt. Segui le istruzioni attuali di Certbot e dell’OS anziché copiare alla cieca vecchi comandi di installazione.

Verifica che:

- il certificato copra dominio principale e varianti `www` utilizzate;
- HTTP reindirizzi a HTTPS come previsto;
- il rinnovo sia automatico;
- il rinnovo funzioni attraverso firewall e CDN;
- l’app generi URL HTTPS corretti.

Non attivare il reindirizzamento HTTPS prima di sapere che certificato e relativa configurazione funzionano.

## Configura il firewall {#configure-the-firewall}

Mantieni funzionante l’accesso amministrativo mentre cambi le regole.

Un sito pubblico di base richiede comunemente:

- SSH dalla sorgente o dal percorso amministrativo previsto;
- TCP 80 per HTTP, ACME e reindirizzamenti;
- TCP 443 per HTTPS.

Non esporre pubblicamente MySQL/PostgreSQL, Redis o porte applicative interne solo perché ascoltano localmente per impostazione predefinita.

Su un server con UFW, consenti il percorso SSH necessario **prima** di attivare regole restrittive.

I dettagli di firewall e protezione approfondita sono in [Checklist di sicurezza VPS]({{< relref "vps-security-checklist.md" >}}).

## Cron, code e worker {#cron-jobs-queues-and-workers}

I siti dinamici spesso falliscono dopo l’installazione perché è stato configurato solo il percorso delle richieste web.

Fai un inventario di:

- processi cron;
- worker delle code;
- azioni pianificate;
- importazioni/esportazioni;
- processi di invio email;
- preriscaldamento della cache;
- elaborazioni in background.

Assicurati che:

- usino l’utente non root corretto;
- si avviino automaticamente quando necessario;
- scrivano in log conosciuti;
- non si sovrappongano fino a esaurire CPU/RAM;
- continuino a funzionare dopo un riavvio.

## Log e osservabilità di base {#logs-and-basic-observability}

Prima del traffico di produzione, identifica dove cercare in caso di guasto.

Come minimo, individua:

- log di accesso Nginx/Apache;
- log degli errori Nginx/Apache;
- log applicativo;
- log PHP-FPM/runtime;
- log e stato del database;
- journal di sistema;
- uso del disco;
- pressione su memoria e CPU.

Aggiungi un controllo HTTP(S) esterno, così il guasto è visibile anche quando nessuno è collegato al VPS.

Soglie e avvisi approfonditi sono trattati in [Monitoraggio VPS]({{< relref "vps-monitoring.md" >}}).

## Verifica del riavvio {#reboot-validation}

Molte prime installazioni VPS funzionano solo fino al primo riavvio.

Prima di considerare pronto il server:

```bash
sudo reboot
```

Quando torna online, conferma:

- accesso SSH;
- Nginx/Apache;
- PHP-FPM o servizio applicativo;
- database;
- cron e worker delle code;
- HTTPS;
- pagine e moduli del sito;
- monitoraggio;
- pianificazione dei backup.

Se l’applicazione torna solo dopo un comando lanciato manualmente, l’installazione non è completa.

## Quando l’hosting manuale senza pannello non è adatto {#when-manual--no-panel-hosting-is-the-wrong-fit}

Usa un pannello o amministrazione gestita quando:

- nessuno sa usare SSH e recuperare il server da riga di comando;
- nessuno si occupa degli aggiornamenti OS e di sicurezza;
- nessuno sa diagnosticare guasti di server web, runtime o database;
- si creano backup ma nessuno sa ripristinarli;
- i fermi critici non hanno un responsabile degli incidenti;
- il team vuole gestire posta, utenti e domini da un’interfaccia di hosting;
- lo stack applicativo è servito meglio da una piattaforma gestita.

Un VPS manuale può ridurre il consumo del pannello e massimizzare il controllo, ma non riduce le responsabilità operative.

Usa [VPS con pannello di controllo]({{< relref "vps-with-control-panel.md" >}}) per scegliere il pannello o [VPS gestito o non gestito]({{< relref "managed-vs-unmanaged-vps.md" >}}) quando manca un responsabile della gestione.

## Checklist di accettazione per la produzione {#production-acceptance-checklist}

| Controllo | Condizione di superamento |
|---|---|
| Accesso al server | amministratore nominativo può accedere; console di recupero disponibile |
| Aggiornamenti | aggiornamenti attuali di sistema e sicurezza applicati |
| Server web | avvio automatico e test di configurazione superato |
| Nome host | comportamento di dominio principale/`www` intenzionale |
| DNS | A/AAAA/CNAME puntano al server o percorso previsto |
| HTTPS | certificato attendibile, nomi corretti, procedura di rinnovo nota |
| Applicazione | pagine rappresentative, accesso, moduli e caricamenti funzionano |
| Database | utente applicativo funziona; porta DB non pubblica per errore |
| File | proprietà corretta; nessuna scorciatoia `777` |
| Processi | cron e worker si avviano e scrivono correttamente nei log |
| Riavvio | i servizi necessari ripartono automaticamente |
| Log | il responsabile sa dove compaiono errori web, applicativi e di sistema |
| Backup | file e database necessari inclusi; procedura di ripristino definita |
| Monitoraggio | controllo esterno del sito e visibilità di base delle risorse |
| Capacità | CPU, RAM e disco verificati con carico reale |

Una homepage che risponde HTTP 200 non basta a rendere il sito pronto per la produzione.

## Passaggio a backup e monitoraggio {#backups-and-monitoring-handoff}

Questa pagina stabilisce solo i requisiti minimi di passaggio alla gestione ordinaria.

Prima di affidarti al sito:

- pianifica i backup;
- mantieni una copia indipendente fuori dal server;
- includi database, configurazione e segreti necessari al recupero;
- verifica la possibilità di ripristino;
- monitora la disponibilità del sito;
- monitora la crescita del disco;
- osserva pressione su CPU, RAM e database;
- controlla il rinnovo dei certificati.

Il progetto di recupero approfondito è in [Strategia di backup VPS]({{< relref "vps-backup-strategy.md" >}}). Soglie e avvisi sono in [Monitoraggio VPS]({{< relref "vps-monitoring.md" >}}).

## Più siti web {#multiple-websites}

Per più siti:

- usa un blocco server o virtual host separato per nome host;
- separa le document root;
- usa credenziali applicative e DB separate;
- usa utenti di sistema separati quando richiesto dal modello di fiducia;
- evita che cron, importazioni o backup di un sito sottraggano risorse agli altri;
- considera il carico di picco complessivo;
- ricorda che tutti i siti condividono un solo dominio di guasto VPS.

Usa [VPS per più siti web]({{< relref "vps-for-multiple-websites.md" >}}) per pianificare capacità e isolamento.

## Riferimenti tecnici {#technical-references}

- Ubuntu Server: installazione di Nginx
- Ubuntu Server: configurazione di Nginx
- Ubuntu Server: servizi web
- VDSina Standard VPS — immagini OS attuali

<p>
  <a class="btn btn-primary" href="https://www.vdsina.com/?partner=ni8gzrvz75" target="_blank" rel="sponsored nofollow noopener">Scegli un VPS per il tuo sito</a>
</p>
<p><small>Trasparenza: l’autore ha un rapporto professionale con VDSina. I link partner sono contrassegnati come sponsorizzati. Verifica prezzi VPS, sistemi operativi disponibili e condizioni del provider prima di ordinare.</small></p>

## Domande frequenti {#faq}

### Posso ospitare un sito su VPS senza pannello? {#can-i-host-a-website-on-a-vps-without-a-control-panel}

Sì. Un VPS Linux pulito può ospitare un sito con SSH e i componenti web, runtime e database necessari. Questo intento senza pannello fa parte della guida, senza una pagina concorrente separata.

### Serve Nginx per ospitare un sito su VPS? {#do-i-need-nginx-to-host-a-website-on-vps}

No. Nginx e Apache sono entrambi comuni. Scegli quello adatto ad applicazione, configurazione ed esperienza dell’amministratore.

### Ogni sito su VPS richiede un database? {#does-every-vps-website-need-a-database}

No. I siti statici non ne hanno bisogno. Installa MySQL/MariaDB/PostgreSQL solo quando l’applicazione lo richiede.

### Dovrei usare root per ospitare il sito? {#should-i-use-root-to-host-the-website}

No. Root serve all’amministrazione. Esegui e distribuisci il sito tramite utenti e servizi non root con i soli permessi necessari.

### Quando conviene usare un pannello? {#when-should-i-use-a-control-panel}

Quando gestire dal browser siti, domini, PHP, database, utenti, posta o backup elimina abbastanza lavoro ripetitivo da giustificare consumo di risorse e vincoli.

### Posso ospitare WordPress su VPS senza cPanel? {#can-i-host-wordpress-on-a-vps-without-cpanel}

Sì. WordPress richiede server web compatibile, PHP, database, file WordPress, permessi corretti, DNS e HTTPS. Il pannello è facoltativo.

### Quando devo puntare i DNS al VPS? {#when-should-i-point-dns-to-the-vps}

Per un sito nuovo, quando il server può rispondere al nome host reale. Per un sito già in produzione, testa prima e usa un piano controllato di migrazione e passaggio.

### Perché il dominio punta al VPS ma mostra il sito sbagliato? {#why-does-my-domain-point-to-the-vps-but-show-the-wrong-site}

I DNS inviano il nome host all’IP del server. Anche Nginx/Apache deve avere un blocco server o virtual host corrispondente a quel nome.

### Quando devo attivare HTTPS? {#when-should-i-enable-https}

Dopo che il nome host pubblico punta al server e il percorso di validazione funziona. Emetti il certificato, verifica dominio principale/`www` e configura il reindirizzamento HTTP-HTTPS previsto.

### Che cosa devo verificare dopo il riavvio del VPS? {#what-should-i-check-after-rebooting-the-vps}

Conferma che server web, servizio applicativo/PHP-FPM, database, worker, HTTPS, monitoraggio e sito ripartano senza interventi manuali.
