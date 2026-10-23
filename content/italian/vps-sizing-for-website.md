---
title: "Dimensionamento VPS per siti web"
description: "Dimensionamento VPS per siti web: calcola CPU, RAM e spazio disco da carico reale, limiti dell'hosting condiviso, worker PHP, esigenze del database e picchi di traffico."
image: "images/home/vps-for-website-hero.webp"
slug: "dimensionamento-vps-per-siti-web"
---

Il dimensionamento di un VPS per un sito deve partire dal carico che raggiunge il server di origine, non dalle visite mensili. Possibilità di usare la cache, richieste dinamiche simultanee, worker PHP o applicativi, attività del database, processi in background, consumo del pannello e crescita dei dati determinano quanta CPU, RAM e spazio disco servono davvero.

Per la scelta d'acquisto complessiva, consulta [VPS per siti web]({{< relref "_index.md" >}}).

[Vai al dimensionamento RAM](#ram-budget) · [Diagnosi dell'hosting condiviso](#shared-hosting-to-vps-diagnostic) · [Scelta del piano](#match-the-result-to-a-vps) · [Domande frequenti](#faq)

## Indicazioni rapide sul dimensionamento {#quick-sizing-answer}

Queste configurazioni attuali dei piani Standard VDSina sono riferimenti utili, ma è il carico a determinare la fascia, non il contrario. I valori del provider riportati di seguito sono stati verificati il 13 ottobre 2026.

| Carico del sito | Esempio di VPS iniziale | Cosa verificare |
|---|---:|---|
| Sito molto leggero, ambiente di test, progetto servito in gran parte dalla cache | 1 vCPU / 1 GB RAM / 10 GB — $0.07/giorno, 1 TB/mese di traffico | Margine di memoria, dimensione del database, uso dello swap |
| Sito piccolo o CMS essenziale | 1 vCPU / 2 GB RAM / 40 GB — $0.50/giorno, 32 TB/mese di traffico | Worker PHP, consumo del pannello, memoria del database |
| Sito aziendale o carico dinamico WordPress tipico | 2 vCPU / 4 GB RAM / 80 GB — $0.67/giorno, 32 TB/mese di traffico | Richieste simultanee senza cache, attività cron, latenza del database |
| Sito dinamico più impegnativo, database più grande o più siti attivi | 4 vCPU / 8 GB RAM / 160 GB — $1.34/giorno, 32 TB/mese di traffico | Carico CPU persistente, memoria dei worker, sovrapposizione dei picchi |

Sono indicazioni di dimensionamento, non garanzie di traffico. Due siti con lo stesso numero di visitatori possono richiedere server molto diversi. Prezzi, traffico incluso e altre condizioni possono cambiare: verifica l'offerta attuale prima dell'ordine.

<p>
  <a class="btn btn-primary" href="https://www.vdsina.com/?partner=ni8gzrvz75" target="_blank" rel="sponsored nofollow noopener">Consulta le configurazioni VPS attuali</a>
</p>
<p><small>Trasparenza: il redattore ha un rapporto professionale con VDSina e il sito può ricevere una commissione se ordini tramite questo link di affiliazione. Il dimensionamento consigliato dipende dal carico, non dalla commissione.</small></p>

## Il modello di dimensionamento: riserva le risorse prima di contare le visite {#the-sizing-model-reserve-resources-before-counting-traffic}

Un calcolo utile delle risorse distingue i diversi consumatori presenti sul server.

### Fabbisogno di RAM {#ram-budget}

La RAM totale deve coprire:

1. sistema operativo e servizi di sistema;
2. server web o reverse proxy;
3. PHP-FPM, Node.js, Python o un altro runtime applicativo;
4. database;
5. servizi di cache come Redis, se utilizzati;
6. pannello di controllo e relativi servizi;
7. processi di monitoraggio, sicurezza e backup;
8. worker applicativi simultanei;
9. margine di sicurezza per picchi, rilasci e manutenzione.

Non confondere il limite di memoria di un CMS con la RAM richiesta dal server. Un limite PHP di 256 MB non significa che un VPS da 1 GB possa eseguire in sicurezza quattro processi PHP simultanei da 256 MB insieme a Linux, database e tutti gli altri servizi.

Un modello pratico è:

**RAM necessaria = servizi di base + memoria operativa del database + memoria dei worker simultanei + memoria delle attività in background + margine**

Misura i processi reali quando possibile. Le stime aiutano a scegliere una configurazione iniziale; le misurazioni stabiliscono se è davvero sufficiente.

### Calcolatore del fabbisogno di RAM {#ram-budget-estimator}

Usa questo calcolatore per rendere esplicite le ipotesi, anziché dedurre le risorse dalle visite. Stima solo la fascia di RAM: CPU, spazio disco e I/O richiedono verifiche separate. Inserisci le tue misurazioni; i valori di esempio nei campi riprendono il calcolo seguente e non sono valori predefiniti universali.

<div class="rounded-2xl bg-light p-6 dark:bg-darkmode-light">
<form id="ram-budget-estimator-form">
  <div class="mb-6">
    <label for="ram-baseline" class="form-label">Sistema operativo e servizi web di base, MB</label>
    <input id="ram-baseline" class="form-input" type="number" min="0" step="1" placeholder="450" required>
  </div>
  <div class="mb-6">
    <label for="ram-database" class="form-label">Memoria operativa del database, MB</label>
    <input id="ram-database" class="form-input" type="number" min="0" step="1" placeholder="500" required>
  </div>
  <div class="mb-6">
    <label for="ram-workers" class="form-label">Worker applicativi simultanei</label>
    <input id="ram-workers" class="form-input" type="number" min="0" step="1" placeholder="6" required>
  </div>
  <div class="mb-6">
    <label for="ram-worker-mb" class="form-label">Memoria media per worker, MB</label>
    <input id="ram-worker-mb" class="form-input" type="number" min="0" step="1" placeholder="120" required>
  </div>
  <div class="mb-6">
    <label for="ram-background" class="form-label">Pannello, cache e attività in background, MB</label>
    <input id="ram-background" class="form-input" type="number" min="0" step="1" placeholder="300" required>
  </div>
  <div class="mb-6">
    <label for="ram-headroom" class="form-label">Margine di sicurezza, %</label>
    <input id="ram-headroom" class="form-input" type="number" min="0" max="100" step="1" value="25" required>
  </div>
  <button class="btn btn-primary" type="submit">Stima la fascia di RAM</button>
</form>
<p id="ram-budget-result" class="mt-6 rounded border border-border p-4 dark:border-darkmode-border" role="status" aria-live="polite">Inserisci le misurazioni e calcola il fabbisogno.</p>
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
    else tier = "più di 8 GB RAM o un'architettura separata";
    document.getElementById("ram-budget-result").textContent =
      "Fabbisogno stimato dei servizi in esecuzione contemporanea: circa " + requiredGb + " GB, margine incluso. Configurazione iniziale basata sulla sola RAM: " + tier +
      ". Verifica memoria effettiva dei processi e CPU prima dell'ordine.";
  });
});
</script>

Esempio: 450 MB per i servizi di base + 500 MB per il database + 6 worker × 120 MB + 300 MB per pannello/cache/attività in background = 1,970 MB prima del margine. Con un margine del 25%, il fabbisogno è di circa 2.4 GB. Un VPS da 2 GB è quindi troppo limitato per queste ipotesi; 4 GB è una configurazione iniziale più sicura.

Quando misuri PHP-FPM o worker analoghi, ricorda che l'RSS grezzo può contare più volte pagine di memoria e librerie condivise tra processi. Considera le misurazioni come riscontri, non come valori perfettamente sommabili.

### Fabbisogno di CPU {#cpu-budget}

La CPU necessaria dipende dal lavoro da eseguire contemporaneamente. I file statici serviti dalla cache possono richiedere poco. Le richieste dinamiche che eseguono codice applicativo, interrogano il database, generano pagine, ridimensionano immagini, eseguono importazioni o chiamano API possono consumare molta più CPU.

Cerca questi segnali:

- saturazione persistente della CPU durante il traffico legittimo;
- tempi di risposta applicativi elevati mentre la CPU è occupata;
- più richieste dinamiche onerose che arrivano insieme;
- attività cron, backup o importazioni sovrapposti al traffico degli utenti;
- query che consumano CPU a causa di indici inefficienti o lavoro eccessivo.

Un breve picco di CPU non giustifica automaticamente un'espansione. Una saturazione persistente che rallenta il lavoro legittimo è un segnale più significativo.

Una stima pratica della simultaneità è:

**richieste dinamiche attive ≈ richieste dinamiche al secondo × durata della richiesta**

Esempio: 6 richieste dinamiche senza cache al secondo, con durata p95 di 0.8 secondi, implicano circa 4.8 richieste attive in quel momento. Se l'applicazione richiede un worker per richiesta attiva, prevedi circa cinque worker occupati più coda e margine. Se ogni richiesta consuma 0.12 secondi di CPU, 6 richieste al secondo corrispondono a circa 0.72 secondi di lavoro CPU al secondo, prima del margine. È una stima del carico, non una garanzia universale sulle vCPU: generazione della CPU, competizione per le risorse e pianificazione del provider possono variare.

## Esempi di carichi dei siti web {#website-workload-examples}

Lo stesso traffico può comportare requisiti VPS molto diversi, perché cambia il lavoro che raggiunge il server di origine.

| Carico | Pressione tipica | Conseguenze sul dimensionamento |
|---|---|---|
| Sito prevalentemente statico o servito in gran parte dalla cache | poco carico CPU applicativo, pochi worker simultanei, soprattutto distribuzione di file | parti da una configurazione piccola, includendo comunque sistema operativo, log, backup e richieste impreviste senza cache |
| Piccolo sito WordPress | worker PHP, letture del database, attività di plugin e cron | RAM e margine per i worker contano solitamente più delle sole visite mensili |
| WooCommerce o altro sito transazionale | carrello, checkout e sessioni account senza cache, azioni pianificate e più scritture nel database | dai priorità a richieste dinamiche simultanee, latenza del database e picchi sovrapposti; non assumere 1–2 GB come configurazione predefinita per la produzione |
| Più siti web | insieme di worker PHP/applicativi, database, attività cron e picchi sovrapposti | dimensiona sul picco complessivo e valuta l'isolamento se un sito può sottrarre risorse agli altri |
| Sito con molti worker in background o automazioni | code, importazioni, esportazioni, chiamate API, elaborazione di immagini, attività pianificate | riserva CPU/RAM oltre a quelle per le richieste degli utenti e separa i worker quando i carichi a raffica disturbano il sito |

Sono modelli di carico, non garanzie legate alla piattaforma. Usa misurazioni reali quando disponibili.

## Tradurre i limiti dell'hosting condiviso in requisiti VPS {#translate-shared-hosting-limits-into-vps-requirements}

Se il sito usa già un hosting condiviso, i dati più utili al dimensionamento potrebbero essere già nel pannello dell'hosting.

Raccogli:

- utilizzo della CPU ed eventi di raggiungimento del limite CPU;
- utilizzo della memoria fisica;
- entry process o limiti delle richieste simultanee;
- numero di processi;
- pressione su I/O del disco e IOPS;
- dimensione e crescita del database;
- spazio disco utilizzato;
- picchi di traffico per ora, oltre alle visite mensili;
- comportamento dei worker PHP o dei processi applicativi, quando visibile.

### Diagnosi per passare dall'hosting condiviso al VPS {#shared-hosting-to-vps-diagnostic}

Usa l'andamento dei superamenti dei limiti per capire cosa approfondire prima di scegliere una configurazione. Lo strumento non converte direttamente un limite CloudLinux in vCPU o RAM.

Su hosting cPanel con CloudLinux, parti dallo storico di Resource Usage, non da una singola lettura istantanea. Registra gli eventi ricorrenti e gli orari, quindi confrontali con traffico, cron, backup, importazioni e attività amministrative.

<div class="rounded-2xl bg-light p-6 dark:bg-darkmode-light">
<form id="shared-hosting-diagnostic">
  <div class="mb-6">
    <label for="diag-evidence" class="form-label">Qualità dei dati disponibili</label>
    <select id="diag-evidence" class="form-input">
      <option value="measured">Storico del pannello / metriche misurate</option>
      <option value="partial">Alcune metriche misurate</option>
      <option value="traffic">Solo numero di visitatori o impressioni</option>
    </select>
  </div>
  <div class="mb-6">
    <label for="diag-memory" class="form-label">Superamenti dei limiti di memoria / eventi PMEM</label>
    <select id="diag-memory" class="form-input"><option value="0">Nessuno</option><option value="1">Occasionali</option><option value="2">Ricorrenti</option></select>
  </div>
  <div class="mb-6">
    <label for="diag-cpu" class="form-label">Eventi di raggiungimento del limite CPU</label>
    <select id="diag-cpu" class="form-input"><option value="0">Nessuno</option><option value="1">Occasionali</option><option value="2">Ricorrenti</option></select>
  </div>
  <div class="mb-6">
    <label for="diag-ep" class="form-label">Saturazione di entry process / worker</label>
    <select id="diag-ep" class="form-input"><option value="0">Nessuna</option><option value="1">Occasionale</option><option value="2">Ricorrente</option></select>
  </div>
  <div class="mb-6">
    <label for="diag-nproc" class="form-label">Saturazione del numero di processi / NPROC</label>
    <select id="diag-nproc" class="form-input"><option value="0">Nessuna</option><option value="1">Occasionale</option><option value="2">Ricorrente</option></select>
  </div>
  <div class="mb-6">
    <label for="diag-io" class="form-label">Pressione su I/O / IOPS</label>
    <select id="diag-io" class="form-input"><option value="0">Nessuna</option><option value="1">Occasionale</option><option value="2">Ricorrente</option></select>
  </div>
  <button class="btn btn-primary" type="submit">Individua il collo di bottiglia</button>
</form>
<p id="shared-hosting-result" class="mt-6 rounded border border-border p-4 dark:border-darkmode-border" role="status" aria-live="polite">Seleziona i segnali che osservi realmente.</p>
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
    var confidence = evidence === "measured" ? "Alta" : (evidence === "partial" ? "Media" : "Bassa");
    var repeated = [memory, cpu, ep, nproc, io].filter(function (v) { return v === 2; }).length;
    var findings = [];
    if (memory >= 1) findings.push("pressione sulla memoria: controlla memoria dei worker, dati del database mantenuti in memoria, swap/OOM e attività in background");
    if (cpu >= 1) findings.push("pressione sulla CPU: analizza richieste dinamiche e lavoro del database prima di aggiungere vCPU");
    if (ep >= 1) findings.push("pressione su worker e simultaneità: riduci la durata delle richieste e misura quelle simultanee senza cache");
    if (nproc >= 1) findings.push("pressione sul numero di processi: individua processi PHP, cron o in background fuori controllo o eccessivi prima di acquistare capacità");
    if (io >= 1) findings.push("pressione sullo storage: controlla I/O del database, backup, log e importazioni; più RAM da sola potrebbe non risolvere il problema");
    var decision;
    if (findings.length === 0) decision = "Nessun forte segnale di capacità insufficiente. Resta sul piano attuale oppure ottimizza prima, finché le misurazioni non mostrano un limite reale.";
    else if (repeated >= 2) decision = "MIGRA / DIMENSIONA DAI DATI: più limiti ricorrenti giustificano il dimensionamento di un VPS dopo aver eliminato le inefficienze software evidenti.";
    else decision = "OTTIMIZZA PRIMA, POI RICONTROLLA: probabilmente esiste un collo di bottiglia, ma un singolo limite dell'hosting non si traduce direttamente in una specifica VPS.";
    document.getElementById("shared-hosting-result").textContent =
      decision + " Affidabilità: " + confidence + ". " + (findings.length ? findings.join("; ") + "." : "");
  });
});
</script>

Non copiare un limite dell'hosting condiviso in una specifica VPS. Una percentuale CPU CloudLinux, un limite di entry process o un tetto di memoria descrivono l'ambiente attuale: indicano un collo di bottiglia, ma non consentono una conversione diretta in risorse VPS.

Interpreta invece l'insieme dei segnali:

**Superamenti ricorrenti della memoria con CPU normale:** controlla memoria dei worker, del database e delle attività in background prima di aggiungere vCPU.

**Limite CPU raggiunto ripetutamente durante lavoro dinamico legittimo:** analizza applicazione e database, poi valuta più CPU se quel lavoro è effettivamente necessario.

**Saturazione di entry process o worker:** misura richieste dinamiche simultanee e durata delle richieste. Ridurre i tempi può eliminare la coda senza ingrandire il server.

**Pressione sull'I/O:** individua backup, log, attività del database, importazioni o plugin con uso intenso dello storage prima di presumere che più RAM risolva il problema.

Questo permette di distinguere una reale carenza di capacità da un limite del piano raggiunto per colpa di un solo componente inefficiente.

| Sintomo | Verifica | Ottimizza prima | Aumenta le risorse quando |
|---|---|---|---|
| Limiti di memoria, swap o OOM | memoria dei processi, dati del database in memoria, worker simultanei | perdite di memoria, worker sovradimensionati, impostazioni di cache/database | il carico ottimizzato esaurisce ancora la RAM |
| Limitazione della CPU | CPU sotto carico persistente e tempi di richieste/database | codice lento, lavoro senza cache, query onerose | il lavoro legittimo resta limitato dalla CPU |
| Coda EP/worker | richieste dinamiche simultanee e loro durata | cache, endpoint lenti, configurazione dei worker | la coda persiste dopo aver ridotto il costo delle richieste |
| Attesa I/O / superamenti IOPS | database, log, backup, importazioni | pianificazione, indici, gestione di log e backup | lo storage resta il collo di bottiglia durante il normale lavoro |



## VPS più grande o ottimizzazione del sito? {#vps-or-website-optimization}

Un VPS più grande è giustificato quando il carico legittimo esaurisce ripetutamente una risorsa anche dopo aver risolto i problemi applicativi evidenti.

Ottimizza prima se la pressione dipende da:

- un plugin o un'estensione lenta;
- una query senza indici adeguati o particolarmente inefficiente;
- cache di pagina o oggetti malfunzionante;
- bot abusivi;
- attività cron fuori controllo;
- elaborazioni di immagini eccessivamente grandi;
- backup o scansioni antimalware pianificati nelle ore di punta;
- perdite di memoria;
- registrazione eccessiva dei log.

Aumenta le risorse quando le misurazioni mostrano che il carico ottimizzato richiede ancora più capacità.

La distinzione ha un impatto economico. Trasferire codice inefficiente dall'hosting condiviso a un VPS più grande può nascondere temporaneamente il collo di bottiglia senza eliminarlo.

## Dimensiona i worker PHP e applicativi in base alla simultaneità {#size-php-and-application-workers-from-concurrency}

Le visite mensili sono un dato debole per dimensionare un server, che deve gestire richieste contemporanee.

Nei carichi PHP dinamici, ogni worker attivo consuma memoria e CPU mentre elabora una richiesta. La capacità dei worker dipende quindi sia dalla memoria media per worker sia dalla durata delle richieste.

Un controllo semplificato della RAM è:

**RAM per i worker = RAM utilizzabile dopo i servizi di base × quota assegnabile ai worker in sicurezza**

Confronta poi questo margine con la memoria misurata dei worker. Non configurare il massimo teorico di worker se così non rimane memoria per database, cache o sistema operativo.

La cache cambia il calcolo. Una pagina anonima in cache può evitare completamente PHP, mentre checkout, sessioni autenticate, wp-admin, API e pagine personalizzate continuano a raggiungere l'applicazione.

Per le caratteristiche specifiche di WordPress, consulta [VPS per WordPress]({{< relref "vps-for-wordpress.md" >}}). Per i carichi transazionali, consulta [VPS per WooCommerce]({{< relref "vps-for-woocommerce.md" >}}).

## Il database può determinare la dimensione del server {#database-demand-can-set-the-server-size}

Un sito può sembrare limitato dalla CPU quando il problema di fondo è il lavoro del database.

Controlla:

- ricorrenza delle query lente;
- dimensione dei dati del database mantenuti in memoria;
- query simultanee;
- indici mancanti;
- grandi quantità di dati caricati automaticamente o metadati applicativi equivalenti;
- ricerche, filtri o report onerosi;
- importazioni e attività di manutenzione;
- latenza dello storage.

Più RAM può aiutare quando il database ha realmente bisogno di mantenere più dati in memoria, ma non corregge query inefficienti. Più CPU può aumentare la capacità di elaborazione, ma anche consentire a più query onerose di competere contemporaneamente.

## Pianifica per i picchi, non per il traffico medio {#plan-for-peak-traffic-not-average-traffic}

Dimensionare sulla media nasconde i periodi in cui gli utenti subiscono effettivamente i problemi.

Individua la finestra di massimo carico plausibile: campagne, promozioni, invii di newsletter, lanci di prodotti, importazioni pianificate, backup o raffiche di cron. Stima quali richieste restano dinamiche e quali vengono assorbite dalla cache di pagina o da una CDN.

Mantieni margine per la combinazione di:

- traffico ordinario degli utenti;
- picchi di traffico dinamico;
- attività amministrative;
- attività pianificate;
- rilasci e popolamento della cache;
- processi di monitoraggio e backup.

Una CDN può ridurre la distribuzione di file statici e alcune richieste all'origine. Non elimina il lavoro dinamico dell'applicazione o del database che continua a raggiungere il VPS.

Esempio di picco: con 20 richieste/s e il 90% servito da cache/CDN, l'origine riceve circa 2 richieste dinamiche/s. Una campagna che raddoppia il traffico a 40 richieste/s, mantenendo la stessa quota in cache, invia circa 4 richieste dinamiche/s all'applicazione. Con durata p95 di 0.8 secondi, sono circa 3.2 richieste dinamiche attive contemporaneamente, prima di aggiungere attività amministrative o raffiche di checkout/API.

## Dimensionamento dello spazio disco {#storage-sizing}

La capacità del disco non riguarda solo la cartella attuale del sito.

Includi:

- file del sito;
- database;
- contenuti multimediali caricati;
- log;
- file temporanei;
- cache dei pacchetti e delle applicazioni;
- copie di staging, se conservate localmente;
- file di backup, se creati temporaneamente sul VPS;
- crescita prevista.

Non riempire il filesystem fino al limite. Database, aggiornamenti, log e operazioni di backup richiedono spazio di lavoro.

Un calcolo pratico della capacità è:

**disco necessario = file attuali + database + spazio per operazioni temporanee + preparazione locale dei backup + crescita prevista + margine libero di lavoro**

Esempio: 18 GB già utilizzati + 8 GB temporanei per migrazione/aggiornamenti + 18 GB temporanei per preparare backup locali + 6 GB di crescita prevista superano già un disco da 40 GB, prima del margine di sicurezza. In questo caso, una fascia da 80 GB è un punto di partenza più sicuro. La capacità è distinta da IOPS e latenza dello storage: un disco più grande non rende automaticamente più veloce un database lento.

## Dimensionamento della banda e del traffico mensile {#bandwidth-and-monthly-transfer-sizing}

Il traffico mensile è distinto da CPU, RAM e velocità della porta. Un server può avere ampio margine di calcolo e superare comunque il traffico incluso se distribuisce direttamente file grandi o contenuti multimediali senza cache.

Una stima approssimativa è:

**traffico mensile dall'origine ≈ byte medi inviati dal VPS per richiesta × richieste mensili all'origine + backup/esportazioni/altro traffico in uscita**

Per una stima più utile, separa traffico memorizzabile in cache e traffico dinamico:

**traffico dall'origine ≈ byte totali richiesti × (1 - quota gestita da CDN/cache) + risposte dinamiche senza cache + traffico in uscita non web**

Esempio: se gli utenti richiedono 2 TB di risorse/pagine al mese e una CDN serve l'80% di questi byte senza tornare all'origine, il VPS può distribuire circa 400 GB di quel traffico memorizzabile in cache, oltre a pagine dinamiche, risposte API, backup, esportazioni e richieste non soddisfatte dalla cache.

Non presumere che una CDN azzeri il traffico dall'origine. Pagine autenticate, checkout, API, richieste non presenti in cache, svuotamenti della cache, grandi download e trasferimenti dall'origine alla CDN possono ancora consumare traffico. Distingui anche il **traffico mensile incluso** dalla **velocità della porta di rete**: una porta veloce indica la capacità di trasferimento potenziale, mentre la quota indica quanti dati puoi inviare nel periodo di fatturazione.

## Più siti cambiano il calcolo {#multiple-websites-change-the-calculation}

Più siti sullo stesso VPS condividono CPU, RAM, storage e capacità dei processi. I picchi possono sovrapporsi anche se ogni sito, preso singolarmente, è piccolo.

Dimensiona sul carico complessivo e riserva margine affinché un'attività in background di un sito non sottragga risorse agli altri. Quando contano isolamento, impatto dei guasti o competizione per le risorse, separare i carichi può essere più utile che continuare a ingrandire un solo server.

Per la scelta multisito, consulta [VPS per più siti web]({{< relref "vps-for-multiple-websites.md" >}}).

## Includi pannello e posta nel calcolo delle risorse {#control-panel-and-mail-overhead-belong-in-the-budget}

Un pannello semplifica domini, SSL, database, versioni PHP e gestione degli account, ma esegue anche servizi propri. Riserva memoria e spazio disco al pannello, senza dimensionare solo per il sito.

La posta può aggiungere un altro consumo permanente di risorse: SMTP, IMAP/POP, filtri antispam, scansioni antivirus, code, log e spazio delle caselle. Se il VPS ospita sito ed email, includi questi consumi in RAM, CPU, storage e backup, senza considerarli gratuiti.

Per un piccolo sito, spostare la posta presso un provider email gestito può ridurre carico e rischi operativi. Se resta sul VPS, verifica separatamente i requisiti di recapito, come record DNS e vincoli del provider o dell'IP; un VPS più grande non risolve i problemi di reputazione del mittente.

Se preferisci amministrare tramite pannello, confronta vantaggi e limiti in [VPS con pannello di controllo]({{< relref "vps-with-control-panel.md" >}}).

## Un metodo ripetibile per dimensionare il VPS {#a-repeatable-vps-sizing-workflow}

1. **Misura il carico attuale.** Registra CPU, memoria, richieste dinamiche simultanee, comportamento del database, spazio disco e periodi di punta.
2. **Individua il collo di bottiglia.** Distingui problemi di CPU, RAM, worker, database, I/O e limiti software.
3. **Elimina le inefficienze evidenti.** Correggi cache, attività fuori controllo, query inefficienti e traffico abusivo prima di acquistare capacità.
4. **Calcola il fabbisogno.** Riserva RAM a servizi di base, database, worker applicativi, pannello e attività in background.
5. **Scegli una configurazione iniziale con margine.** Evita sia l'assenza di margine sia l'acquisto di risorse in eccesso senza riscontri.
6. **Riproduci un picco realistico.** Verifica la configurazione con un carico dinamico rappresentativo, non solo con la home inattiva.
7. **Monitora dopo la migrazione.** Adatta le risorse ai dati senza considerare definitiva la stima iniziale; usa [Monitoraggio VPS]({{< relref "vps-monitoring.md" >}}) come base per la produzione.

Dopo il dimensionamento, usa [Migrazione di un sito web su VPS]({{< relref "website-migration-to-vps.md" >}}) per pianificare inventario, test privati, sincronizzazione finale dei dati, cambio DNS e rollback.

## Raccomandazioni basate sui dati {#evidence-based-recommendation}

Una raccomandazione utile deve indicare sia la configurazione sia il motivo della scelta.

Per esempio:

**2 vCPU / 4 GB RAM / 80 GB** possono essere un punto di partenza ragionevole per un sito aziendale con CMS e database, attività PHP senza cache significativa, pannello di controllo e necessità di margine operativo. Non garantiscono un numero specifico di visitatori mensili.

L'affidabilità della stima è minore se l'unico dato è il numero di visitatori. Aumenta quando conosci storico CPU, pressione sulla memoria, richieste dinamiche simultanee, memoria dei worker, comportamento del database e crescita dei dati.

Usa una semplice indicazione di affidabilità:

- **Affidabilità bassa:** solo numero di visitatori, nome del CMS e stima dello spazio disco.
- **Affidabilità media:** alcuni dati reali sullo storico CPU/RAM, tipo di carico e andamento dei picchi.
- **Affidabilità alta:** serie temporali CPU/RAM/I/O, richieste simultanee senza cache, memoria dei worker, durata delle richieste, comportamento del database e crescita dei dati.

Un'affidabilità maggiore indica ipotesi meglio fondate, non una garanzia sul traffico futuro.

## Associare il risultato a un VPS {#match-the-result-to-a-vps}

Valuta insieme stima della RAM, dati CPU, fabbisogno di spazio disco e comportamento nei picchi. Queste configurazioni Standard VDSina sono esempi per associare il risultato a un piano; verifica le condizioni attuali prima dell'ordine.

| Configurazione | Impiego iniziale adatto | Evita / ricontrolla in presenza di | Verifica principale | Azione |
|---|---|---|---|---|
| 1 vCPU / 1 GB / 10 GB — $0.07/giorno, 1 TB/mese | sito di test, sito molto leggero con cache, servizi minimi | pannello + database + più worker dinamici, negozio in produzione | margine RAM e disco | <a href="https://www.vdsina.com/?partner=ni8gzrvz75" target="_blank" rel="sponsored nofollow noopener">Verifica il piano attuale</a> |
| 1 vCPU / 2 GB / 40 GB — $0.50/giorno, 32 TB/mese | piccolo sito o CMS essenziale con lavoro dinamico controllato | CPU costantemente sotto carico, più siti attivi, stack pannello/posta pesante | memoria dei worker e del database, crescita dei dati | <a href="https://www.vdsina.com/?partner=ni8gzrvz75" target="_blank" rel="sponsored nofollow noopener">Verifica il piano attuale</a> |
| 2 vCPU / 4 GB / 80 GB — $0.67/giorno, 32 TB/mese | CMS aziendale dinamico, PHP senza cache moderato, margine per il pannello | WooCommerce impegnativo, grandi importazioni, database sotto forte pressione, picchi multisito interferenti | saturazione CPU, latenza del database, picchi sovrapposti | <a href="https://www.vdsina.com/?partner=ni8gzrvz75" target="_blank" rel="sponsored nofollow noopener">Verifica il piano attuale</a> |
| 4 vCPU / 8 GB / 160 GB — $1.34/giorno, 32 TB/mese | carico dinamico più impegnativo, database più grande, più siti attivi | requisiti stringenti di alta disponibilità, scritture molto intense, carichi con scalabilità indipendente | verifica che un solo VPS sia ancora l'architettura adatta | <a href="https://www.vdsina.com/?partner=ni8gzrvz75" target="_blank" rel="sponsored nofollow noopener">Verifica il piano attuale</a> |

Una fascia da 1 GB o 2 GB non va consigliata automaticamente per la produzione solo perché il sito riesce ad avviarsi. Ecommerce, database grandi, più siti dinamici, posta e pannelli possono consumare rapidamente il margine.

<p>
  <a class="btn btn-primary" href="https://www.vdsina.com/?partner=ni8gzrvz75" target="_blank" rel="sponsored nofollow noopener">Scegli il tuo VPS</a>
</p>

## Prima di acquistare il VPS {#before-buying-the-vps}

Verifica le condizioni che il solo dimensionamento non chiarisce: traffico incluso, tipo e capacità dello storage, condizioni IP, politica di backup, possibilità di espansione, gestione inclusa, licenze del pannello e fatturazione attuale. Scegli separatamente la regione con [Come scegliere la posizione del VPS]({{< relref "how-to-choose-vps-location.md" >}}), perché CPU e RAM non determinano il percorso di rete migliore.

Se il sito usa ancora un hosting condiviso, valuta il cambiamento operativo in [VPS o hosting condiviso]({{< relref "vps-vs-shared-hosting.md" >}}) prima di migrare.

## Riferimenti tecnici {#technical-references}

- cPanel: requisiti hardware del server
- cPanel: come stabilire quanta RAM, CPU e spazio disco aggiungere
- Configurazioni VPS Standard VDSina

<p>
  <a class="btn btn-primary" href="https://www.vdsina.com/?partner=ni8gzrvz75" target="_blank" rel="sponsored nofollow noopener">Consulta l'offerta VPS attuale</a>
</p>
<p><small>Trasparenza: il redattore ha un rapporto professionale con VDSina. I link di affiliazione sono contrassegnati sponsored. Prezzi, traffico incluso e altre condizioni commerciali possono cambiare; verificali sul sito del provider prima dell'ordine.</small></p>

## Domande frequenti {#faq}

### Quanta RAM serve a un VPS per siti web? {#how-much-ram-does-a-website-vps-need}

Non esiste una quantità universale affidabile. Un sito essenziale con cache può usare poca memoria, mentre un CMS dinamico con database, pannello e worker simultanei può richiederne molta di più. Calcola la RAM dei processi che devono coesistere e lascia un margine.

### Bastano 2 GB di RAM per un VPS web? {#is-2-gb-ram-enough-for-a-website-vps}

Possono bastare per un carico piccolo ed essenziale. Diventano limitanti quando devono funzionare insieme pannello, database, più worker PHP, attività in background o più siti. Misura la pressione sulla memoria anziché basarti solo sulla RAM nominale.

### A cosa è adatto un VPS da 4 GB? {#what-does-a-4-gb-vps-tier-fit}

Un VPS da 4 GB è un punto di partenza pratico per molti CMS aziendali, perché lascia più spazio a Linux, database, worker applicativi/PHP e cache. L'idoneità dipende da richieste dinamiche simultanee, esigenze del database, attività in background e consumo del pannello. Per la scelta specifica di WordPress, consulta [VPS per WordPress]({{< relref "vps-for-wordpress.md" >}}).

### Quanti visitatori può gestire un VPS? {#how-many-visitors-can-a-vps-handle}

Il solo numero di visitatori non permette di rispondere. Percentuale di richieste servite dalla cache, simultaneità, tempo di esecuzione dell'applicazione, database e attività in background possono far variare la capacità di ordini di grandezza tra siti con traffico simile.

### Conviene aggiungere prima RAM o CPU? {#should-i-add-ram-or-cpu-first}

Aggiungi la risorsa che risulta limitante dalle misurazioni. Pressione sulla memoria, uso dello swap o eventi OOM indicano RAM insufficiente o necessità di ottimizzare la memoria. Saturazione CPU persistente durante lavoro legittimo già ottimizzato indica un limite CPU. Database e I/O richiedono una diagnosi separata.

### Una CDN riduce i requisiti del VPS? {#does-a-cdn-reduce-vps-requirements}

Può ridurre la distribuzione di file statici e le richieste all'origine memorizzabili in cache. Richieste dinamiche e lavoro del database che raggiungono l'origine continuano a consumare risorse VPS.

### Devo dimensionare per il traffico medio o di picco? {#should-i-size-for-average-or-peak-traffic}

Per un picco realistico, con margine operativo. La media può nascondere brevi periodi in cui si sovrappongono richieste simultanee, attività pianificate e lavoro dinamico.
