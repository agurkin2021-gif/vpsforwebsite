---
title: "Monitoraggio VPS"
description: "Monitora il VPS con controlli esterni di disponibilità, metriche CPU/RAM/disco/rete, stato dei servizi, log e avvisi utili. Include strumenti, soglie e una checklist pratica."
image: "images/home/vps-for-website-hero.webp"
slug: "monitoraggio-vps"
---

Il monitoraggio VPS deve rispondere a più della domanda «il server è attivo?». Una base di produzione richiede **controlli esterni di disponibilità, metriche host storiche, stato di servizi e applicazioni, log, avvisi utilizzabili e un responsabile della risposta**.

Un VPS può rispondere al ping mentre Nginx è guasto, il database è bloccato, il disco è pieno o il certificato TLS sta per scadere. Il monitoraggio deve quindi coprire server e sito visto dagli utenti.

Per la scelta complessiva del server, consulta [VPS per siti web]({{< relref "_index.md" >}}).

[Risposta rapida](#quick-answer) · [Verifica](#vps-monitoring-baseline-checker) · [Metriche host](#monitor-cpu-memory-disk-and-network) · [Stato applicativo](#monitor-services-and-application-health) · [Avvisi](#build-actionable-alerts) · [Capacità](#use-trends-for-capacity-planning) · [Domande frequenti](#faq)

## Risposta rapida {#quick-answer}

Uno stack pratico di monitoraggio VPS ha cinque livelli:

| Livello | Che cosa indica | Guasto tipico rilevato |
|---|---|---|
| **Disponibilità esterna** | se gli utenti raggiungono il sito dall’esterno del VPS | VPS, rete o sito irraggiungibili |
| **Metriche host** | andamento di CPU, RAM, swap, disco, inode, I/O e rete | perdita di memoria, disco pieno, pressione CPU persistente |
| **Stato di servizi/applicazioni** | se web server, runtime, DB ed endpoint critici funzionano davvero | guasto Nginx/PHP/DB/app con server ancora online |
| **Log/eventi** | che cosa è cambiato o fallito | picco 5xx, OOM, worker fallito, errore DB |
| **Avvisi e responsabilità** | se la persona giusta viene avvisata e può intervenire | fermo silenzioso o dashboard ignorata |

Non eseguire l’unico controllo di disponibilità sul VPS che deve sorvegliare. Se il VPS o il suo percorso di rete si guasta del tutto, il controllo può sparire insieme al sito.

## Verifica del monitoraggio di base VPS {#vps-monitoring-baseline-checker}

Usa questo strumento per trovare punti ciechi. Non garantisce la disponibilità.

<div class="rounded-2xl bg-light p-6 dark:bg-darkmode-light">
<form id="vps-monitoring-checker">
  <div class="mb-6">
    <label for="mon-workload" class="form-label">Carico principale</label>
    <select id="mon-workload" class="form-input">
      <option value="static">Sito statico / semplice</option>
      <option value="cms">WordPress / CMS</option>
      <option value="transactional">WooCommerce / sito con transazioni</option>
      <option value="multi">Più siti / insieme eterogeneo</option>
    </select>
  </div>
  <div class="mb-6">
    <label for="mon-external" class="form-label">Controllo HTTP(S) esterno a questo VPS?</label>
    <select id="mon-external" class="form-input"><option value="no">No</option><option value="yes">Sì</option></select>
  </div>
  <div class="mb-6">
    <label for="mon-metrics" class="form-label">Storico delle metriche CPU/RAM/disco/rete conservato?</label>
    <select id="mon-metrics" class="form-input"><option value="no">No / solo top o htop occasionali</option><option value="yes">Sì</option></select>
  </div>
  <div class="mb-6">
    <label for="mon-disk" class="form-label">Capacità disco, inode e pressione sullo storage monitorati?</label>
    <select id="mon-disk" class="form-input"><option value="no">No / solo GB liberi</option><option value="yes">Sì</option></select>
  </div>
  <div class="mb-6">
    <label for="mon-app" class="form-label">Controlli sui servizi e sulle applicazioni critiche configurati?</label>
    <select id="mon-app" class="form-input"><option value="no">No / solo ping</option><option value="yes">Sì</option></select>
  </div>
  <div class="mb-6">
    <label for="mon-jobs" class="form-label">DB, code, cron e aggiornamento dei backup monitorati dove necessario?</label>
    <select id="mon-jobs" class="form-input"><option value="no">No / non so</option><option value="yes">Sì</option><option value="na">Non applicabile</option></select>
  </div>
  <div class="mb-6">
    <label for="mon-alerts" class="form-label">Avvisi automatici con regole utili di gravità e durata?</label>
    <select id="mon-alerts" class="form-input"><option value="no">No / solo dashboard</option><option value="yes">Sì</option></select>
  </div>
  <div class="mb-6">
    <label for="mon-notify" class="form-label">Il canale di notifica sopravvive al guasto del VPS?</label>
    <select id="mon-notify" class="form-input"><option value="no">No / solo sullo stesso VPS</option><option value="yes">Sì</option></select>
  </div>
  <div class="mb-6">
    <label for="mon-owner" class="form-label">Esistono un responsabile e una procedura di prima risposta?</label>
    <select id="mon-owner" class="form-input"><option value="no">No</option><option value="yes">Sì</option></select>
  </div>
  <button class="btn btn-primary" type="submit">Verifica il monitoraggio di base</button>
</form>
<p id="vps-monitoring-result" class="mt-6 rounded border border-border p-4 dark:border-darkmode-border" role="status" aria-live="polite">Segna solo controlli che raccolgono davvero dati e inviano avvisi.</p>
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
      result = "PUNTI CIECHI: il sistema non vede ancora uno o più guasti fondamentali. Aggiungi controlli indipendenti di disponibilità, storico delle metriche host, visibilità su disco e inode e verifiche reali di servizi e applicazioni.";
    } else if (!alerts || !notify || !owner) {
      result = "AVVISI / RESPONSABILITÀ INCOMPLETI: i dati possono esistere, ma un incidente può restare inosservato o senza responsabile. Aggiungi avvisi utilizzabili, un canale indipendente e una procedura con un responsabile definito.";
    } else if (!jobs && (workload === "transactional" || workload === "cms" || workload === "multi")) {
      result = "MONITORAGGIO DI BASE: l’infrastruttura è monitorata, ma processi applicativi, database o aggiornamento dei backup restano punti ciechi per questo carico.";
    } else {
      result = "BASE DI MONITORAGGIO DI PRODUZIONE: disponibilità esterna, storico delle metriche, stato dei servizi, avvisi e responsabilità sono presenti. Continua ad adattare le soglie al comportamento reale: non è una garanzia di disponibilità.";
    }

    document.getElementById("vps-monitoring-result").textContent = result;
  });
});
</script>

## Monitora il sito dall’esterno del VPS {#monitor-the-website-from-outside-the-vps}

Un comando interno può indicare che Nginx è in esecuzione. Non prova che un utente reale su Internet raggiunga il sito.

Usa un controllo esterno per i nomi host importanti.

Controlli utili includono:

- disponibilità HTTP/HTTPS;
- codice di stato atteso;
- tempo di risposta;
- verifica di parole chiave o contenuto;
- risoluzione DNS;
- stato e scadenza del certificato TLS;
- porte TCP quando pertinenti.

Se i falsi positivi sono rilevanti, richiedi errori ripetuti o conferma da più località prima di allertare qualcuno.

Strumenti autogestiti come Uptime Kuma eseguono controlli HTTP(S), parole chiave, TCP, ping e DNS, ma vanno collocati fuori dal dominio di guasto del VPS di produzione.

Un server di monitoraggio soggetto allo stesso guasto di VPS, rete del provider o DNS può essere utile per le dashboard, ma non è un controllo indipendente di disponibilità.

## La diagnosi in tempo reale non è monitoraggio storico {#real-time-diagnostics-are-not-historical-monitoring}

Comandi come:

```bash
top
htop
free -h
df -h
ss -s
```

sono utili quando stai già indagando su un problema.

Non dicono:

- che cosa è successo alle 03:12;
- se la RAM è cresciuta costantemente per sei ore;
- se la latenza del disco è salita durante un backup;
- se il sito è rimasto fermo dieci minuti;
- se un problema peggiora settimana dopo settimana.

Conserva serie temporali dei segnali che influenzano disponibilità e capacità.

Per un VPS può bastare un agente leggero. Per più server, conservazione lunga o dashboard personalizzate, Prometheus + Node Exporter + Grafana è un’architettura comune.

Prometheus Node Exporter espone metriche host e kernel raccoglibili da Prometheus, tra cui CPU, filesystem e rete.

## Monitora CPU, memoria, disco e rete {#monitor-cpu-memory-disk-and-network}

### CPU {#cpu}

Non generare avvisi per ogni breve picco.

Osserva:

- utilizzo CPU persistente;
- carico medio rispetto al numero di vCPU;
- CPU per processo;
- tempo CPU sottratto dall’hypervisor, se esposto dallo stack di virtualizzazione;
- latenza applicativa e delle richieste nello stesso momento.

Un breve picco al 100% durante il preriscaldamento della cache o un cron può essere innocuo. Saturazione persistente con latenza e code in crescita è un segnale più forte di collo di bottiglia.

### Memoria, swap e OOM {#memory-swap-and-oom}

Linux usa spesso RAM libera per la cache del filesystem: «90% di RAM usata» non indica automaticamente un guasto.

Osserva:

- memoria disponibile;
- attività di swap;
- crescita dello swap;
- eventi OOM-killer;
- crescita della memoria dei processi;
- memoria dei worker PHP/app;
- memoria del database.

Una perdita di memoria può sembrare normale a mezzogiorno e terminare il processo di notte. Lo storico rende visibile la tendenza.

### Capacità del disco {#disk-capacity}

Osserva l’uso del filesystem prima che impedisca il funzionamento di DB, log o aggiornamenti.

Una coppia iniziale illustrativa di soglie avviso/critica può essere **80% / 90% di spazio usato**, ma non è uno SLA universale. Un database in rapida crescita può richiedere interventi molto prima.

Monitora anche lo spazio operativo libero necessario a:

- backup;
- manutenzione DB;
- aggiornamenti dei pacchetti;
- caricamenti;
- log;
- staging e importazioni.

### Inode {#inodes}

Un filesystem può esaurire gli inode pur avendo molti GB liberi.

Può accadere con:

- directory di cache;
- sessioni;
- code di posta;
- enormi quantità di file minuscoli;
- file temporanei fuori controllo.

Monitora gli inode separatamente dai GB del disco.

### I/O e latenza del disco {#disk-io-and-latency}

Il disco può diventare un collo di bottiglia prima di riempirsi.

Osserva:

- attesa I/O;
- latenza di lettura e scrittura;
- profondità delle code, se disponibile;
- tempo di risposta DB;
- finestre di backup e importazione.

Aumentare la capacità del disco non risolve automaticamente un I/O lento.

### Rete {#network}

Controlla più della sola banda totale:

- traffico in ingresso e uscita;
- variazioni improvvise del traffico;
- errori di connessione;
- perdita di pacchetti e latenza, quando misurabili;
- traffico in uscita insolito;
- errori delle interfacce.

Le metriche di rete aiutano a distinguere lentezza applicativa e problemi di provider o percorso.

## Monitora servizi e stato applicativo {#monitor-services-and-application-health}

Un VPS può essere raggiungibile mentre il sito è guasto.

Monitora servizi importanti come:

- Nginx/Apache;
- PHP-FPM;
- servizio applicativo Node/Python;
- MySQL/MariaDB/PostgreSQL;
- Redis, se usato;
- worker delle code;
- servizio delle attività pianificate;
- pannello, se critico per l’attività.

Su Linux con systemd, `systemctl --failed` aiuta nella diagnosi, ma il monitoraggio continuo dovrebbe avvisare di servizi necessari falliti o in riavvio ripetuto.

Non fermarti a «il processo esiste». Può essere attivo senza riuscire a servire richieste valide.

## HTTP 200 non significa sempre corretto funzionamento {#http-200-is-not-always-healthy}

Un’app può rispondere HTTP 200 mostrando:

- pagina di manutenzione;
- errore DB dentro un template;
- contenuto vuoto o errato;
- procedura di accesso non funzionante;
- cache obsoleta.

Per siti critici, usa il controllo mirato più utile:

- parola chiave o testo atteso;
- endpoint di stato;
- risposta API;
- URL pubblico critico;
- accesso o transazione sintetica solo se il valore aziendale giustifica la complessità.

Non far modificare dati di produzione ai controlli sintetici, salvo siano progettati specificamente per farlo in sicurezza.

## Monitora TLS e DNS {#monitor-tls-and-dns}

Il VPS può funzionare mentre il sito è indisponibile per errori di certificato o DNS.

Controlla:

- scadenza dei certificati;
- mancata corrispondenza del nome host nel certificato;
- rinnovi falliti;
- risoluzione DNS;
- modifiche accidentali dei record, se supportate dagli strumenti.

Un esempio utile è avvisare con anticipo, per esempio **14 giorni** prima della scadenza, aumentando la gravità più vicino al termine, per esempio a **7 giorni**. La finestra esatta deve riflettere la rapidità di intervento sul rinnovo.

## Monitora il database come dipendenza applicativa {#monitor-the-database-as-an-application-dependency}

Per siti basati su DB, raccogli abbastanza informazioni per capire se il database è un collo di bottiglia o una dipendenza guasta.

Secondo motore e carico, segnali utili includono:

- disponibilità del servizio;
- numero di connessioni;
- errori di connessione;
- latenza delle query;
- sintomi di blocchi e contesa;
- attività delle query lente;
- pressione sulla memoria;
- crescita dello spazio;
- stato di replica e backup, se usati.

Non avvisare per ogni metrica DB. Scegli condizioni legate a effetti sugli utenti o a guasti noti.

Per il carico WordPress, vedi [VPS per WordPress]({{< relref "vps-for-wordpress.md" >}}). Per negozi con transazioni, vedi [VPS per WooCommerce]({{< relref "vps-for-woocommerce.md" >}}).

## Monitora cron, code e attività in background {#monitor-cron-queues-and-background-jobs}

Una homepage funzionante non dimostra che il lavoro in background sia sano.

Controlla le attività importanti per l’app:

- cron;
- worker delle code;
- importazioni pianificate;
- webhook;
- invii email;
- WP-Cron WordPress / cron di sistema;
- WooCommerce Action Scheduler;
- abbonamenti e rinnovi;
- sincronizzazione del magazzino.

Segnali utili:

- ultima esecuzione riuscita;
- dimensione della coda e arretrati;
- processi falliti;
- attività in attesa più vecchia;
- tentativi ripetuti;
- worker fermo o in riavvio.

In WooCommerce, una coda Action Scheduler di attività fallite o scadute in crescita può essere un problema operativo anche con catalogo accessibile.

## Monitora quanto sono recenti i backup {#monitor-backup-freshness}

Il processo di backup appartiene alla strategia di recupero, ma **l’età del backup è un segnale di monitoraggio**.

Genera avvisi quando:

- un backup pianificato fallisce;
- l’ultimo backup riuscito è più vecchio dell’RPO definito;
- il dump DB fallisce;
- l’invio esterno fallisce;
- scadono le credenziali del repository;
- la dimensione cambia in modo sospetto;
- il processo di eliminazione o conservazione fallisce.

«Cron eseguito» non prova l’esistenza di un backup utilizzabile.

Per RPO/RTO, conservazione, copie indipendenti e prove di ripristino, usa [Strategia di backup VPS]({{< relref "vps-backup-strategy.md" >}}).

## Correla log e metriche {#correlate-logs-with-metrics}

Le metriche indicano **che cosa è cambiato**. I log spesso spiegano **perché**.

Confronta la stessa finestra temporale tra:

- log di accesso ed errore Nginx/Apache;
- log PHP-FPM/runtime;
- log applicativi;
- log DB;
- journal di sistema;
- log di autenticazione;
- log di backup e processi.

Esempio:

- picco CPU alle 14:03;
- aumento dei 5xx alle 14:03;
- il log applicativo mostra timeout DB;
- il log DB mostra contesa sui blocchi.

È più utile per intervenire di un generico avviso «CPU alta».

Conserva abbastanza log per indagare, ma non lasciare che riempiano il filesystem di produzione.

## Crea avvisi che permettano di intervenire {#build-actionable-alerts}

Un avviso deve indicare che cosa è fallito e che cosa controllare per primo.

Preferisci:

- **avviso** — indagare prima dell’impatto sugli utenti;
- **critico** — impatto sugli utenti o guasto imminente;
- durata e filtraggio dei transitori — evitare allarmi per picchi di un secondo;
- raggruppamento e deduplicazione — evitare 40 notifiche per un fermo;
- host o servizio coinvolto chiaramente identificato;
- link a dashboard, log e procedura;
- prima azione ed escalation note.

Prometheus Alertmanager è un esempio di sistema progettato per raggruppare, deduplicare e instradare gli avvisi.

### Evita soglie universali {#avoid-universal-thresholds}

Le soglie devono corrispondere al carico.

Esempi di logica iniziale ragionevole:

- CPU: utilizzo elevato persistente con latenza o code, anziché picco isolato;
- RAM: poca memoria disponibile con swap/OOM, anziché solo «RAM usata > 80%»;
- disco: avviso anticipato mentre resta margine operativo;
- TLS: avviso giorni prima della scadenza;
- HTTP: errori ripetuti o conferma da più località quando contano i falsi positivi;
- backup: ultimo successo più vecchio dell’RPO;
- 5xx/latenza: deviazione persistente dal comportamento normale dell’applicazione.

Regola le soglie dopo aver osservato la produzione normale.

## Mantieni indipendente il canale di notifica {#keep-the-notification-path-independent}

Un avviso è inutile se il suo sistema di consegna muore nello stesso incidente.

Quando possibile, invia gli avvisi importanti fuori dal VPS tramite:

- provider email esterno;
- servizio esterno di chat o notifiche;
- strumento ospitato di gestione incidenti;
- monitoraggio in un altro dominio di guasto.

Non affidarti solo a SMTP o dashboard sullo stesso VPS guasto.

## Ogni avviso richiede un responsabile e una procedura {#every-alert-needs-an-owner-and-runbook}

Prima di creare un avviso, rispondi:

- chi lo riceve?
- chi può intervenire?
- qual è il primo passo diagnostico?
- quale dashboard o log aprire?
- quando va inoltrato a un livello superiore?
- quando si può silenziare in sicurezza?
- che cosa succede fuori orario?

Se nessuno risponde, il monitoraggio ha soltanto trasformato un fermo in una notifica.

Per le responsabilità operative complessive, vedi [VPS gestito o non gestito]({{< relref "managed-vs-unmanaged-vps.md" >}}).

## Scegli lo stack in base alla complessità {#choose-the-monitoring-stack-by-complexity}

Non installare una grande piattaforma di osservabilità solo perché è popolare.

### Dashboard del provider come livello iniziale {#provider-dashboard-as-a-starting-layer}

Se il provider offre storico di CPU, RAM, disco o rete, usalo come comodo punto di partenza a livello host.

Non confondere i grafici infrastrutturali del provider con un monitoraggio completo del sito. Possono non verificare HTTP(S) dall’esterno del provider, contenuto applicativo, DB, attività in background, rinnovo TLS o responsabilità degli avvisi.

Considera il monitoraggio del provider una fonte di dati e aggiungi i controlli esterni e applicativi richiesti dal carico.

### Percorso leggero per un VPS {#lightweight-single-vps-path}

Una piccola configurazione pratica può unire:

- controllo esterno di disponibilità;
- Netdata o un altro agente/dashboard di metriche host;
- log di sistema e applicazione;
- notifiche.

Adatto quando una persona gestisce uno o pochi VPS.

### Percorso Prometheus / Grafana {#prometheus--grafana-path}

Utile se servono:

- metriche di più server;
- storico più lungo;
- query personalizzate;
- metriche di servizi ed exporter;
- dashboard condivise;
- regole di avviso strutturate.

Node Exporter fornisce metriche Linux; Prometheus le conserva e interroga; Grafana le visualizza; Alertmanager può instradare, raggruppare e deduplicare avvisi.

### Percorso con monitoraggio ospitato {#hosted-monitoring-path}

Utile quando:

- il monitor deve essere indipendente da VPS o provider;
- vuoi meno infrastruttura di monitoraggio da gestire;
- notifiche gestite e integrazioni di reperibilità sono utili.

Anche il monitoraggio è infrastruttura di produzione. Mantieni la complessità proporzionata al rischio ridotto.

## Proteggi lo stack di monitoraggio {#secure-the-monitoring-stack}

Agenti e dashboard possono esporre dati operativi sensibili.

Proteggi:

- dashboard;
- exporter;
- endpoint delle metriche;
- token API;
- webhook di notifica;
- backend dei log.

Non esporre Prometheus, Node Exporter, Grafana o dashboard amministrative a Internet senza un modello esplicito di accesso protetto.

Usa firewall, rete privata o autenticazione sul reverse proxy secondo necessità.

Il monitoraggio non sostituisce la protezione: usa [Checklist di sicurezza VPS]({{< relref "vps-security-checklist.md" >}}) per la base del server.

## Conta anche il consumo del monitoraggio {#monitoring-overhead-matters}

Il monitoraggio consuma:

- RAM;
- CPU;
- disco per conservare metriche e log;
- rete;
- capacità di backup.

Un piccolo agente costa di solito poco, ma metriche e log conservati a lungo possono diventare un carico significativo sullo storage.

Controlla anche lo stack stesso:

- stato di agenti e servizi;
- errori di raccolta delle metriche;
- crescita dello spazio;
- conservazione;
- consegna delle notifiche.

Non lasciare che l’osservabilità riempia il disco che dovrebbe proteggere.

## Usa le tendenze per pianificare la capacità {#use-trends-for-capacity-planning}

Lo storico del monitoraggio è la migliore base per il prossimo dimensionamento.

Usa le tendenze per capire:

- la saturazione CPU è persistente o occasionale?
- la RAM disponibile diminuisce nel corso delle settimane?
- swap o OOM compaiono con carico legittimo?
- quanto rapidamente cresce il disco?
- la latenza DB aumenta durante i picchi?
- si formano code PHP o applicative?
- backup e importazioni creano contesa prevedibile?

Non fare un upgrade solo perché una dashboard è diventata rossa per poco.

Aumenta le risorse quando il **carico legittimo ottimizzato** le esaurisce ripetutamente o quando l’architettura richiede scalabilità indipendente.

Usa [Dimensionamento VPS per siti web]({{< relref "vps-sizing-for-website.md" >}}) per tradurre i dati in una scelta di risorse.

<p>
  <a class="btn btn-primary" href="https://www.vdsina.com/?partner=ni8gzrvz75" target="_blank" rel="sponsored nofollow noopener">Verifica le configurazioni VPS attuali</a>
</p>
<p><small>Trasparenza: l’autore ha un rapporto professionale con VDSina e questo sito può ricevere una commissione se acquisti tramite questo link partner. Il dimensionamento deve seguire i dati di monitoraggio; questa pagina non afferma che VDSina offra gli strumenti descritti come servizio gestito.</small></p>

## Monitora più siti su due livelli {#monitor-multiple-websites-at-two-levels}

Su un VPS multisito, monitora:

### Livello server {#server-level}

- CPU/RAM/swap;
- disco/inode/I/O;
- database;
- rete;
- servizi principali.

### Livello sito {#site-level}

- ogni nome host importante;
- TLS;
- tempo di risposta;
- 5xx;
- errori di applicazioni e processi;
- log per sito o pressione sui worker, se disponibili.

Il server può funzionare mentre un virtual host, certificato o sito è guasto.

Usa [VPS per più siti web]({{< relref "vps-for-multiple-websites.md" >}}) per la scelta di consolidamento e dominio di guasto.

## Checklist di monitoraggio VPS {#vps-monitoring-checklist}

| Segnale | Condizione di superamento |
|---|---|
| Disponibilità esterna | nome host importante controllato dall’esterno del VPS |
| Stato HTTP | stato, contenuto o endpoint attesi verificati |
| CPU | storico di utilizzo persistente, carico e processi conservato |
| RAM | memoria disponibile, swap e OOM visibili |
| Disco | capacità e crescita monitorate |
| Inode | esaurimento monitorato separatamente |
| I/O | latenza e attesa visibili quando lo storage conta |
| Rete | traffico, errori e sintomi del percorso osservabili |
| Servizi | stato di web, runtime, DB e worker monitorato |
| Database | disponibilità, latenza e connessioni rilevanti visibili |
| Processi | errori o arretrati di cron, code e background osservabili |
| TLS/DNS | scadenze ed errori di risoluzione rilevabili |
| Backup | età dell’ultimo successo ed errori monitorati |
| Log | log web, app, DB e sistema disponibili per correlare incidenti |
| Avvisi | gravità avviso/critica e regole di durata o filtro configurate |
| Notifiche | avvisi importanti fuori dal dominio di guasto VPS |
| Responsabilità | persona definita e procedura di primo intervento |
| Conservazione | storico sufficiente per tendenze e analisi delle cause |
| Sicurezza | endpoint e dashboard non pubblici involontariamente |
| Capacità | tendenze usate per decidere ottimizzazione o crescita |

## Riferimenti tecnici {#technical-references}

- Prometheus — metriche host Linux con Node Exporter
- Prometheus — Alertmanager
- Uptime Kuma — progetto ufficiale
- [Strategia di backup VPS]({{< relref "vps-backup-strategy.md" >}})
- [Checklist di sicurezza VPS]({{< relref "vps-security-checklist.md" >}})

## Domande frequenti {#faq}

### Che cosa monitorare su un VPS? {#what-should-i-monitor-on-a-vps}

Almeno disponibilità esterna del sito, CPU, RAM disponibile/swap/OOM, capacità disco, inode, servizi principali, stato applicativo, scadenza TLS, età dei backup e consegna degli avvisi.

### CPU oltre l’80% è sempre un problema? {#is-cpu-over-80-always-bad}

No. Brevi picchi possono essere normali. Indaga sull’utilizzo persistente insieme a carico, latenza, code e processo responsabile.

### Perché la RAM Linux è quasi piena? {#why-is-linux-ram-almost-full}

Linux usa memoria libera per la cache. Monitora memoria disponibile, swap, OOM e crescita dei processi anziché allarmarti per la sola percentuale usata.

### Che cosa monitorare per i problemi del disco? {#what-should-i-monitor-for-disk-problems}

Capacità del filesystem, inode, crescita e latenza/attesa I/O. I soli GB liberi non coprono ogni possibile guasto.

### Basta il ping per monitorare la disponibilità? {#is-ping-enough-for-uptime-monitoring}

No. Può riuscire mentre sito, DB o TLS sono guasti. Usa HTTP(S) e controlli di app e servizi per il funzionamento visto dagli utenti.

### Il controllo di disponibilità deve stare sullo stesso VPS? {#should-the-uptime-monitor-run-on-the-same-vps}

Non come unico controllo. Un guasto completo di VPS o rete può fermarlo insieme al sito. Tieni almeno disponibilità critica e notifiche fuori da quel dominio di guasto.

### Qual è il miglior strumento di monitoraggio VPS? {#which-vps-monitoring-tool-is-best}

Non esiste una scelta universale. Un VPS può richiedere solo controllo esterno e un agente leggero; più server possono giustificare Prometheus, Grafana e Alertmanager. Scegli in base a visibilità, conservazione e complessità necessarie.

### Servono Prometheus e Grafana per un VPS? {#do-i-need-prometheus-and-grafana-for-one-vps}

Non necessariamente. Sono potenti per storico lungo, query personalizzate e più server, ma un agente leggero con monitoraggio esterno può bastare per una piccola installazione.

### Come monitorare i backup? {#how-should-i-monitor-backups}

Genera avvisi per processi falliti e per l’età dell’ultimo backup riuscito rispetto all’RPO. Verifica separatamente la recuperabilità con prove di ripristino.

### Quando il monitoraggio deve portare a un upgrade del VPS? {#when-should-monitoring-trigger-a-vps-upgrade}

Quando lo storico mostra che un carico legittimo ottimizzato esaurisce ripetutamente CPU, RAM, storage/I/O o altre risorse. Un picco isolato non basta.
