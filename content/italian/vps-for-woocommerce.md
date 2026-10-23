---
title: "VPS per WooCommerce"
description: "VPS per WooCommerce: dimensiona CPU e RAM da checkout simultanei, worker PHP, scritture nel database, Action Scheduler, integrazioni e picchi di vendita, poi scegli la gestione."
image: "images/home/vps-for-website-hero.webp"
slug: "vps-per-woocommerce"
---

Un VPS per WooCommerce va dimensionato per le parti del negozio che non si comportano come un blog in cache: **carrello, checkout, account, ordini, scorte, callback di pagamento, azioni pianificate e scritture nel database**. Visite mensili o numero di prodotti, da soli, non indicano le risorse necessarie.

Per il carico WordPress generale, consulta [VPS per WordPress]({{< relref "vps-for-wordpress.md" >}}). Per il percorso principale d'acquisto del server, consulta [VPS per siti web]({{< relref "_index.md" >}}).

[Risposta rapida](#quick-answer) · [Verifica di idoneità](#woocommerce-vps-fit-checker) · [Carico del checkout](#checkout-and-account-traffic-stay-dynamic) · [Database](#database-demand-and-hpos) · [Azioni pianificate](#action-scheduler-and-background-work) · [Picchi di vendita](#size-for-sale-and-campaign-peaks) · [Domande frequenti](#faq)

## Risposta rapida {#quick-answer}

Questi sono punti di partenza pratici per le fasce Standard VDSina attuali, non garanzie sul numero di ordini o visitatori.

| Carico WooCommerce | Punto di partenza pratico | Limite principale da verificare |
|---|---:|---|
| Negozio di laboratorio/test o installazione estremamente essenziale con pochi ordini | **1 vCPU / 2 GB / 40 GB** | margine di produzione molto ridotto quando si sovrappongono PHP, database e attività in background |
| Piccolo negozio aziendale | **2 vCPU / 4 GB / 80 GB** | checkout simultanei, worker PHP, latenza del database, azioni pianificate |
| Negozio più impegnativo, catalogo/database più grande, più integrazioni o picchi di vendita | **4 vCPU / 8 GB / 160 GB** | CPU sotto carico persistente, coda PHP, dati del database in memoria, Action Scheduler, crescita dello storage |
| Carico transazionale oltre la capacità di un solo VPS da 8 GB | **Rivedi l'architettura** | separa database/worker/servizi o adotta un'architettura più potente, cloud o gestita, invece di ingrandire solo una macchina |

Le indicazioni di scalabilità di WooCommerce hanno proposto **1 vCPU + almeno 2 GB di RAM** come base per un'installazione autogestita con supporto a OPcache, CDN e cache persistente. È una soglia iniziale, non la promessa che un negozio di produzione continui a funzionare comodamente con quelle risorse.

Prezzi attuali dei piani Standard VDSina ricontrollati il 13 ottobre 2026:

- 1 vCPU / 1 GB / 10 GB / 1 TB di traffico mensile — **$0.07/giorno**;
- 1 vCPU / 2 GB / 40 GB / 32 TB — **$0.50/giorno**;
- 2 vCPU / 4 GB / 80 GB / 32 TB — **$0.67/giorno**;
- 4 vCPU / 8 GB / 160 GB / 32 TB — **$1.34/giorno**.

Per molti negozi aziendali reali, **4 GB è la fascia iniziale più pratica**, perché il VPS deve sostenere contemporaneamente sistema operativo, database, worker PHP, cache, attività in background e margine operativo.

Per un dimensionamento più approfondito dell'intero stack, usa [Dimensionamento VPS per siti web]({{< relref "vps-sizing-for-website.md" >}}).

## I requisiti di WooCommerce non dimensionano il VPS di produzione {#woocommerce-requirements-are-not-production-vps-sizing}

Le raccomandazioni attuali per WooCommerce 10.8+ richiedono:

- **WordPress 6.9+**;
- **PHP 8.3+**;
- **MySQL 8.0+ o MariaDB 10.6+**;
- **HTTPS**;
- **limite di memoria WordPress di 256 MB+**;
- Apache o Nginx come server web consigliati.

Questi valori rispondono alla domanda **«l'ambiente soddisfa i requisiti software di base di WooCommerce?»**.

Non indicano:

- quanti worker PHP servono;
- quanta RAM totale deve avere il VPS;
- se i dati operativi del database rientrano in memoria;
- se il checkout si accoda sotto carico;
- se le azioni pianificate sono in ritardo;
- se backup e importazioni interferiscono con i clienti;
- se le integrazioni di pagamento o i webhook rallentano le richieste.

Un **limite WordPress/PHP di 256 MB non equivale a 256 MB di RAM VPS**. La RAM totale deve coprire anche Linux, server web, database, worker PHP, cache, attività, pannello/posta e margine.

## Verifica del VPS per WooCommerce {#woocommerce-vps-fit-checker}

Usala come orientamento iniziale, non come garanzia di prestazioni.

<div class="rounded-2xl bg-light p-6 dark:bg-darkmode-light">
<form id="woocommerce-vps-fit-checker-form">
  <div class="mb-6">
    <label for="wc-stage" class="form-label">Fase del negozio / importanza per l'attività</label>
    <select id="wc-stage" class="form-input">
      <option value="test">Test / prima del lancio / impatto aziendale basso</option>
      <option value="small">Piccolo negozio online</option>
      <option value="business">Negozio critico per l'attività</option>
    </select>
  </div>
  <div class="mb-6">
    <label for="wc-limits" class="form-label">L'hosting attuale mostra limiti ricorrenti delle risorse o funzionalità mancanti?</label>
    <select id="wc-limits" class="form-input">
      <option value="no">No / non misurato</option>
      <option value="yes">Sì</option>
    </select>
  </div>
  <div class="mb-6">
    <label for="wc-external" class="form-label">Il guasto o la latenza principale dipende già da pagamenti, spedizioni, imposte, SMTP o altri servizi esterni?</label>
    <select id="wc-external" class="form-input">
      <option value="no">No / non noto</option>
      <option value="yes">Sì</option>
    </select>
  </div>
  <div class="mb-6">
    <label for="wc-checkout" class="form-label">Attività simultanea di checkout e account</label>
    <select id="wc-checkout" class="form-input">
      <option value="low">Bassa</option>
      <option value="medium">Livello medio</option>
      <option value="high">Alta / legata a campagne</option>
    </select>
  </div>
  <div class="mb-6">
    <label for="wc-catalog" class="form-label">Carico di catalogo, ricerca e filtri</label>
    <select id="wc-catalog" class="form-input">
      <option value="light">Leggero</option>
      <option value="medium">Livello medio</option>
      <option value="heavy">Elevato / molte query</option>
    </select>
  </div>
  <div class="mb-6">
    <label for="wc-jobs" class="form-label">Plugin, importazioni, webhook, abbonamenti o attività pianificate impegnativi?</label>
    <select id="wc-jobs" class="form-input"><option value="no">No</option><option value="yes">Sì</option></select>
  </div>
  <div class="mb-6">
    <label for="wc-db" class="form-label">Attività del database / ordini</label>
    <select id="wc-db" class="form-input">
      <option value="small">Ridotta / modesta</option>
      <option value="medium">Livello medio</option>
      <option value="heavy">Scritture/query intense</option>
    </select>
  </div>
  <div class="mb-6">
    <label for="wc-panel" class="form-label">Pannello di controllo o posta locale sullo stesso VPS?</label>
    <select id="wc-panel" class="form-input"><option value="no">No</option><option value="yes">Sì</option></select>
  </div>
  <div class="mb-6">
    <label for="wc-spikes" class="form-label">Picchi regolari dovuti a saldi, newsletter o promozioni?</label>
    <select id="wc-spikes" class="form-input"><option value="no">No</option><option value="yes">Sì</option></select>
  </div>
  <div class="mb-6">
    <label for="wc-operator" class="form-label">Qualcuno può amministrare il VPS?</label>
    <select id="wc-operator" class="form-input">
      <option value="no">No</option>
      <option value="help">Solo con servizio gestito o amministratore a pagamento</option>
      <option value="yes">Sì</option>
    </select>
  </div>
  <button class="btn btn-primary" type="submit">Valuta il VPS per WooCommerce</button>
</form>
<p id="woocommerce-vps-fit-result" class="mt-6 rounded border border-border p-4 dark:border-darkmode-border" role="status" aria-live="polite">Scegli il carico più simile a quello del negozio.</p>
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
      result = "ANALIZZA PRIMA SERVIZI ESTERNI / APPLICAZIONE: il guasto principale è già stato ricondotto a cause esterne alle risorse del VPS. Correggi o misura gateway, API, SMTP e integrazioni prima di acquistare più CPU o RAM.";
    } else if (!limits && stage !== "business" && score <= 2) {
      result = "HOSTING GESTITO / CONDIVISO ANCORA POSSIBILE: non è stato misurato un limite che richieda un VPS. Mantieni il modello più semplice oppure ottimizza prima, finché non emerge una reale esigenza di risorse o funzionalità.";
    } else if (stage === "business" && operator !== "yes") {
      result = "SERVIZIO GESTITO / AMMINISTRATORE: il negozio è critico per l'attività e la gestione del server non ha un responsabile interno completo. Organizza un servizio gestito o amministrativo prima di scegliere un VPS non gestito con la sola infrastruttura.";
    } else if (score <= 2) {
      result = "CONFIGURAZIONE ESSENZIALE DA 2 GB / PICCOLO NEGOZIO: 1 vCPU / 2 GB / 40 GB possono essere una base iniziale per un negozio molto leggero. Verifica checkout, memoria dei worker PHP, latenza del database e azioni pianificate prima di considerarlo pronto per la produzione.";
    } else if (score <= 7) {
      result = "CONFIGURAZIONE PRATICA DA 4 GB: 2 vCPU / 4 GB / 80 GB offrono più margine a un piccolo negozio WooCommerce aziendale con checkout dinamico, scritture nel database e normali attività in background.";
    } else {
      result = "8 GB O REVISIONE DELL'ARCHITETTURA: 4 vCPU / 8 GB / 160 GB sono una base più solida per negozi impegnativi o picchi di vendita. Se dominano database, attività o integrazioni, valuta carichi separati o un'architettura gestita/cloud più potente.";
    }

    document.getElementById("woocommerce-vps-fit-result").textContent = result;
  });
});
</script>

## Quando WooCommerce ha davvero bisogno di un VPS {#when-woocommerce-actually-needs-vps}

Un negozio WooCommerce può giustificare un VPS quando:

- l'hosting condiviso raggiunge ripetutamente limiti di CPU, memoria, processi o I/O sotto carico legittimo;
- richieste di checkout e account si accodano sotto carico reale;
- i dati del database da mantenere in memoria o il carico di scrittura richiedono più controllo;
- le estensioni richiedono servizi vietati dall'hosting attuale;
- servono Redis/Memcached o configurazioni personalizzate del server;
- Action Scheduler o le attività in background richiedono esecuzione più affidabile;
- importazioni di prodotti, feed o sincronizzazione delle scorte interferiscono con i clienti;
- servono impostazioni personalizzate di PHP, runtime o server web;
- servono staging o controllo operativo specifico del negozio.

Se il negozio è piccolo, stabile e ben supportato da un hosting WooCommerce/WordPress gestito, il VPS non è automaticamente la scelta migliore.

## Quando può essere migliore un hosting WooCommerce gestito {#when-managed-woocommerce-hosting-may-be-better}

Un VPS autogestito è poco adatto quando:

- nessuno cura gli aggiornamenti di sistema e sicurezza;
- nessuno monitora la disponibilità del checkout o gli avvisi del server;
- i backup esistono ma il ripristino non è stato provato;
- interruzioni di pagamenti e ordini hanno un impatto critico sull'attività;
- il gruppo vuole assistenza WordPress/WooCommerce anziché occuparsi di Linux;
- la piattaforma gestita attuale risolve già adeguatamente prestazioni e scalabilità.

Un VPS dà più controllo, ma anche più possibili guasti di cui assumersi la responsabilità.

Consulta [VPS gestito o non gestito]({{< relref "managed-vs-unmanaged-vps.md" >}}) prima di affidare un negozio essenziale ai ricavi a un server autogestito.

## Checkout e account restano dinamici {#checkout-and-account-traffic-stay-dynamic}

Le indicazioni ufficiali di WooCommerce sulla cache escludono **Carrello, Il mio account e Checkout** dalla cache dell'intera pagina, perché contengono lo stato specifico del cliente.

È importante perché le richieste commercialmente più rilevanti possono ancora eseguire:

- PHP;
- logica di sessione e carrello;
- calcoli di spedizione e imposte;
- codice d'integrazione dei pagamenti;
- letture e scritture nel database;
- creazione degli ordini;
- aggiornamento delle scorte;
- hook ed estensioni.

Il negozio può quindi servire velocemente una pagina prodotto in cache mentre il checkout continua ad accodarsi.

Non dimensionare WooCommerce dalla sola percentuale di richieste del catalogo servite dalla cache.

## Worker PHP e richieste dinamiche simultanee {#php-workers-and-dynamic-concurrency}

Per le richieste dinamiche WooCommerce, i worker PHP determinano quante richieste possono essere eseguite contemporaneamente.

Un'approssimazione utile è:

**richieste dinamiche attive ≈ richieste senza cache al secondo × durata della richiesta**

Se nei picchi le richieste di checkout/account/API durano in media 0.8 secondi e arrivano a PHP 5 richieste dinamiche al secondo, circa quattro worker possono essere occupati insieme, prima di aggiungere amministrazione, webhook e attività in background.

Ogni worker consuma memoria. Aumentarne il numero senza un calcolo della RAM può sottrarre risorse al database o portare il server a swap/OOM.

Usa questa formula:

**RAM WooCommerce = sistema operativo + server web + database + cache + worker PHP + attività + pannello/posta + margine**

Verifica poi memoria media e di picco dei worker, anziché copiare un numero generico di processi.

## Configura correttamente la cache per WooCommerce {#cache-woocommerce-correctly}

WooCommerce richiede una strategia di cache a più livelli.

### Cache dell'intera pagina {#full-page-cache}

Utile per pagine del catalogo e contenuti memorizzabili in cache.

**Non** mettere indiscriminatamente in cache:

- Carrello;
- Checkout;
- Il mio account;
- risposte specifiche del cliente o della sessione.

Le indicazioni ufficiali di WooCommerce escludono esplicitamente queste pagine.

### OPcache {#opcache}

Conserva il bytecode PHP compilato e riduce le compilazioni ripetute.

### Cache persistente degli oggetti {#persistent-object-cache}

Redis o Memcached possono ridurre il lavoro ripetuto su database e oggetti quando il carico ne beneficia.

Non sostituiscono la cache dell'intera pagina e non correggono automaticamente query inefficienti.

### Browser / CDN {#browser--cdn}

Utili per risorse statiche e contenuti distribuibili dai nodi periferici.

Una CDN può ridurre le richieste statiche all'origine, ma non elimina il lavoro dinamico di checkout e database.

## Esigenze del database e HPOS {#database-demand-and-hpos}

WooCommerce genera letture e scritture più intense rispetto a un normale sito WordPress con cache.

Le attività rilevanti del database possono includere:

- creazione e aggiornamento degli ordini;
- dati di clienti e account;
- variazioni delle scorte;
- consultazione di prodotti e catalogo;
- sessioni;
- metadati delle estensioni;
- report e analisi;
- ricerca e filtri;
- attività pianificate.

**High-Performance Order Storage (HPOS)** di WooCommerce conserva i dati degli ordini in tabelle dedicate ed è attivo per impostazione predefinita nelle nuove installazioni da WooCommerce 8.2.

HPOS è un miglioramento architetturale importante, ma non sostituisce:

- compatibilità di estensioni e codice personalizzato;
- revisione di query e indici;
- memoria adeguata per il database;
- bassa latenza dello storage;
- monitoraggio;
- staging e test prima delle modifiche principali.

Per grandi negozi esistenti, WooCommerce raccomanda di provare la migrazione HPOS e i flussi critici prima del passaggio in produzione.

## Action Scheduler e lavoro in background {#action-scheduler-and-background-work}

WooCommerce usa **Action Scheduler** per attività in background come:

- notifiche degli ordini;
- elaborazioni legate ai pagamenti;
- webhook;
- abbonamenti e rinnovi;
- attività delle estensioni;
- importazioni e sincronizzazioni.

WooCommerce mostra queste attività in **WooCommerce > Stato > Azioni programmate**.

Controlla:

- azioni fallite;
- azioni scadute non eseguite;
- arretrato persistente di azioni in attesa;
- attività di lunga durata;
- code che crescono durante i picchi dei clienti.

Per impostazione predefinita, Action Scheduler dipende dalla pianificazione di WordPress; cron lato server può essere utile quando serve rispettare gli orari in modo affidabile.

Un negozio con pagine in cache veloci può comunque avere problemi operativi se la coda delle attività pianificate non funziona.

## Pagamenti, webhook, email e integrazioni {#payments-webhooks-email-and-integrations}

Un VPS più grande non risolve ogni errore del checkout.

Le dipendenze esterne possono includere:

- gateway di pagamento;
- API per le imposte;
- API per le spedizioni;
- sincronizzazione di inventario ed ERP;
- CRM;
- email transazionali;
- controlli antifrode;
- webhook;
- ricerca o servizi esterni.

Misura se la latenza nasce nel VPS o nel servizio esterno.

Monitora:

- errori delle callback di pagamento;
- consegna dei webhook;
- code email;
- timeout delle API;
- tentativi successivi e attese progressive;
- errori di Action Scheduler.

Non acquistare CPU per risolvere il collo di bottiglia di un'API di terzi.

## Catalogo, ricerca e filtri {#catalog-search-and-filtering}

Un grande catalogo non genera carico soltanto perché contiene molti prodotti.

La pressione reale deriva da:

- query complesse di ricerca e filtro;
- query su attributi e tassonomie;
- tabelle di ricerca dei prodotti;
- numero di varianti;
- regole di prezzo e scorte;
- estensioni che aggiungono SQL o chiamate esterne;
- risultati personalizzati senza cache.

Misura gli endpoint di ricerca e filtro separatamente dalla normale consultazione delle pagine prodotto.

La cache persistente può aiutare alcune query ripetute, ma la progettazione del database e delle query resta importante.

## Dimensiona per picchi di vendite e campagne {#size-for-sale-and-campaign-peaks}

Il picco WooCommerce combina spesso più attività contemporanee:

- traffico da newsletter e pubblicità;
- consultazione del catalogo;
- aggiunta al carrello;
- checkout;
- callback di pagamento;
- email degli ordini;
- aggiornamento delle scorte;
- amministrazione ed elaborazione degli ordini;
- webhook;
- azioni pianificate;
- analisi e registrazione dei log.

Dimensiona per una **finestra di picco rappresentativa**, non per la giornata media.

Prima di una promozione importante:

1. prova un traffico di checkout rappresentativo;
2. verifica il margine dei worker PHP;
3. verifica latenza e connessioni del database;
4. controlla l'arretrato di Action Scheduler;
5. sospendi o ripianifica importazioni, backup e scansioni;
6. conferma il funzionamento delle API esterne di pagamento, spedizione e imposte;
7. osserva log e metriche delle risorse durante l'evento.

## Spazio disco, backup e staging {#storage-backups-and-staging}

Un backup WooCommerce deve proteggere sia i file sia i dati transazionali.

Includi:

- file WordPress/WooCommerce;
- upload e contenuti multimediali dei prodotti;
- database e dati degli ordini;
- configurazione e segreti necessari al ripristino;
- plugin, temi e codice personalizzato;
- impostazioni delle integrazioni.

### Ripristino che tenga conto delle transazioni {#transaction-aware-recovery}

Se il negozio riceve ordini continuamente, la frequenza dei backup determina la possibile perdita di dati degli ordini.

Con un backup giornaliero del database, fino a un giorno di transazioni recenti può restare fuori da quel punto di ripristino.

Scegli la frequenza in base all'**obiettivo del punto di ripristino (RPO)** accettabile, non alla comodità.

L'architettura di backup approfondita è trattata in [Strategia di backup VPS]({{< relref "vps-backup-strategy.md" >}}).

### Staging {#staging}

Quando possibile, prova in staging le modifiche a PHP, WooCommerce, plugin, temi, HPOS e pagamenti prima della produzione.

Le copie di staging consumano però spazio disco e talvolta risorse di database, RAM e backup: includile nella pianificazione della capacità.

## Pannello di controllo, FASTPANEL o stack manuale {#control-panel-fastpanel-or-manual-stack}

WooCommerce può funzionare su un VPS Linux amministrato manualmente oppure tramite un pannello hosting.

Per scegliere un pannello in generale, consulta [VPS con pannello di controllo]({{< relref "vps-with-control-panel.md" >}}).

Per la soluzione FASTPANEL su VDSina, consulta [Hosting VPS con FASTPANEL]({{< relref "fastpanel-vps-hosting.md" >}}).

Per un'installazione Linux manuale, consulta [Come ospitare un sito web su VPS]({{< relref "how-to-host-a-website-on-vps.md" >}}).

Un pannello semplifica le attività ordinarie, ma non si assume la responsabilità di affidabilità del checkout, aggiornamenti WooCommerce/plugin, ottimizzazione del database, backup o incidenti.

## La migrazione di un negozio attivo ha un limite legato ai dati {#live-store-migration-has-a-data-boundary}

Migrare WooCommerce non significa soltanto «copiare file e database».

Ordini, scorte, carrelli, clienti e azioni pianificate possono cambiare mentre il negozio è online.

Per la migrazione:

- prepara e prova prima la destinazione;
- controlla le ultime scritture;
- sincronizza database e upload un'ultima volta;
- evita che due negozi di produzione scrivibili divergano;
- verifica gli endpoint di pagamento e webhook;
- preserva posta e DNS;
- mantieni un piano di rollback.

Per l'intero passaggio, usa [Migrazione di un sito web su VPS]({{< relref "website-migration-to-vps.md" >}}).

## Quando espandere il VPS WooCommerce {#woocommerce-vps-upgrade-triggers}

Aumenta le risorse o rivedi l'architettura quando le misurazioni mostrano:

- code ricorrenti dei worker PHP;
- saturazione CPU persistente dopo ottimizzazione di cache, query e plugin;
- pressione sulla RAM, swap o OOM;
- latenza del database o memoria insufficiente per i suoi dati operativi;
- arretrati o errori di Action Scheduler causati dalla capacità;
- errori di checkout o pagamento sotto picchi legittimi;
- crescita dei dati che riduce il margine sicuro;
- backup, importazioni o scansioni che interferiscono con i clienti;
- più negozi o servizi in competizione per un VPS.

Se il checkout è lento ma le risorse del server sono regolari, cerca cause in pagamenti, API, plugin e database prima di acquistare un VPS più grande.

## Checklist di avvio del VPS WooCommerce {#woocommerce-vps-launch-checklist}

| Controllo | Condizione di superamento |
|---|---|
| Runtime WooCommerce | WordPress/PHP/database attuali e compatibili, con HTTPS |
| Memoria PHP | limite WooCommerce/WordPress configurato; RAM totale del VPS verificata separatamente |
| Worker PHP | sufficienti per checkout e account dinamici simultanei rappresentativi |
| Cache di pagina | esclusi carrello, checkout, account e flussi specifici della sessione |
| Cache oggetti/OPcache | livelli scelti consapevolmente; Redis/Memcached solo dove utili |
| Database | carico di ordini, catalogo e query monitorato; compatibilità HPOS compresa |
| Azioni pianificate | nessun arretrato inspiegato di azioni fallite o scadute |
| Pagamenti | test di ordini, pagamenti, rimborsi e webhook superati |
| Scorte | variazioni coerenti delle giacenze |
| Email | messaggi transazionali recapitati tramite un percorso affidabile |
| Backup | definiti file, database, RPO degli ordini recenti e procedura di ripristino |
| Staging | aggiornamenti critici verificabili fuori dalla produzione |
| Monitoraggio | controlli esterni di sito e checkout, più visibilità su CPU/RAM/disco/database |
| Riavvio | web, PHP, database e attività tornano attivi automaticamente |
| Picco | carico rappresentativo di vendite e campagne verificato |

## Esempi attuali di VPS per WooCommerce {#current-woocommerce-vps-examples}

Questi piani Standard VDSina attuali sono esempi di corrispondenza tra carico e risorse, non garanzie sulla capacità del negozio.

| VPS | Impiego iniziale adatto | Ricontrolla in presenza di |
|---|---|---|
| 1 vCPU / 2 GB / 40 GB — $0.50/giorno | laboratorio, piccolo negozio molto leggero o installazione controllata con pochi ordini | checkout realmente critico per l'attività, plugin pesanti, molte attività |
| 2 vCPU / 4 GB / 80 GB — $0.67/giorno | base pratica per un piccolo negozio WooCommerce aziendale | forti picchi di vendita, database/catalogo grande, molte integrazioni |
| 4 vCPU / 8 GB / 160 GB — $1.34/giorno | negozio più impegnativo / più margine per database, PHP e attività in background | architettura su una sola macchina che diventa collo di bottiglia o dominio di guasto |

La fascia Standard da 1 GB non viene proposta come normale soluzione WooCommerce di produzione.

L'attuale pagina Standard di VDSina **non** elenca un'applicazione WooCommerce preinstallata dedicata nei gruppi visibili di template/applicazioni. Usa un percorso WordPress, manuale o con pannello compatibile, senza presumere un'installazione WooCommerce in un clic.

<p>
  <a class="btn btn-primary" href="https://www.vdsina.com/?partner=ni8gzrvz75" target="_blank" rel="sponsored nofollow noopener">Consulta le opzioni VPS attuali per WooCommerce</a>
</p>
<p><small>Trasparenza: il redattore ha un rapporto professionale con VDSina e il sito può ricevere una commissione se ordini tramite questo link di affiliazione. Verifica prezzi VPS, template e pannelli attualmente disponibili prima dell'ordine.</small></p>

## Riferimenti tecnici {#technical-references}

- WooCommerce — raccomandazioni per il server
- Documentazione per sviluppatori WooCommerce — scalabilità con WooCommerce
- Documentazione per sviluppatori WooCommerce — configurazione dei plugin di cache
- WooCommerce — azioni programmate
- Documentazione per sviluppatori WooCommerce — High Performance Order Storage
- VPS Standard VDSina

## Domande frequenti {#faq}

### Quanta RAM serve a WooCommerce su VPS? {#how-much-ram-does-woocommerce-need-on-a-vps}

Non esiste un numero universale. Le indicazioni di scalabilità di WooCommerce hanno usato 2 GB come base autogestita, mentre 4 GB sono un punto di partenza più solido per molti negozi aziendali, perché worker PHP, database, cache e attività devono coesistere.

### Bastano 2 GB di RAM per WooCommerce? {#is-2-gb-ram-enough-for-woocommerce}

Possono bastare per un negozio molto piccolo ed essenziale o un'installazione controllata con pochi ordini. Verifica checkout simultanei, latenza del database, azioni pianificate e pressione sulla memoria prima di considerarla pronta per la produzione.

### Bastano 4 GB di RAM per WooCommerce? {#is-4-gb-ram-enough-for-woocommerce}

Per molti piccoli negozi aziendali, 4 GB sono un punto di partenza pratico. Traffico intenso, cataloghi/database più grandi, molte integrazioni, abbonamenti, importazioni o picchi di vendita possono richiedere di più.

### Perché WooCommerce è più impegnativo del normale WordPress? {#why-is-woocommerce-heavier-than-normal-wordpress}

Carrello, checkout, account, ordini, scorte e molte integrazioni sono dinamici. Queste richieste eseguono ancora PHP e operazioni sul database anche se le pagine pubbliche di catalogo e contenuti sono in cache.

### Posso mettere in cache il checkout WooCommerce? {#can-i-cache-woocommerce-checkout}

La cache dell'intera pagina deve escludere Carrello, Checkout e Il mio account perché contengono lo stato specifico del cliente. Usa gli altri livelli di cache per dati e contenuti appropriati.

### WooCommerce richiede Redis? {#does-woocommerce-need-redis}

No. Redis o Memcached possono fornire cache persistente degli oggetti quando il carico ne beneficia. Non sostituiscono corrette esclusioni dalla cache di pagina o query efficienti.

### Cos'è HPOS? {#what-is-hpos}

High-Performance Order Storage conserva gli ordini WooCommerce in tabelle dedicate. È attivo per impostazione predefinita nelle nuove installazioni da WooCommerce 8.2. Quando modifichi un negozio esistente, verifica compatibilità di estensioni e codice personalizzato e flussi critici del negozio.

### Cosa sono le azioni programmate di WooCommerce? {#what-are-woocommerce-scheduled-actions}

Sono attività in background accodate e gestite da Action Scheduler, come notifiche degli ordini, elaborazioni dei pagamenti, webhook e attività delle estensioni. Code di azioni fallite o scadute sono un segnale operativo.

### VDSina include WooCommerce preinstallato? {#does-vdsina-include-woocommerce-preinstalled}

La pagina attuale Standard di VDSina non elenca WooCommerce come applicazione preinstallata dedicata nei gruppi visibili di template/applicazioni. Verifica l'interfaccia d'ordine attuale prima di presumere la disponibilità di un template.

### Un VPS è sempre migliore dell'hosting gestito per WooCommerce? {#is-a-vps-always-better-for-woocommerce-than-managed-hosting}

No. Un VPS autogestito è utile se servono controllo e risorse e sai amministrare il server. Hosting WooCommerce/WordPress gestito può essere più sicuro quando il negozio è critico per l'attività e manca un responsabile interno dell'amministrazione.
