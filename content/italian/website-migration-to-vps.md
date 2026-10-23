---
title: "Migrazione di un sito web su VPS"
description: "Migrazione di un sito web su VPS: inventaria lo stack, prova il nuovo server, controlla le ultime scritture, cambia DNS in sicurezza, conserva email e SEO e prepara il rollback."
image: "images/home/vps-for-website-hero.webp"
slug: "migrazione-di-un-sito-web-su-vps"
---

Migrare un sito su VPS è più sicuro quando il nuovo server viene preparato e verificato mentre il vecchio hosting continua a ricevere traffico. Inventaria lo stack, dimensiona la destinazione, copia e controlla il sito, gestisci le ultime modifiche ai dati, cambia il DNS per ultimo e monitora entrambi gli ambienti finché puoi dismettere quello precedente.

Questa pagina presuppone che dominio e struttura degli URL pubblici restino invariati. Se cambiano anche dominio o percorsi, la mappatura degli URL e i redirect permanenti diventano un'attività di migrazione separata.

Per la scelta complessiva dell'hosting, consulta [VPS per siti web]({{< relref "_index.md" >}}).

[Piano rapido](#quick-migration-plan) · [Verifica preliminare](#migration-cutover-preflight) · [Sincronizzazione finale](#control-new-writes-and-the-final-sync) · [Cambio DNS](#switch-dns-deliberately) · [Controlli SEO](#preserve-seo-when-urls-stay-the-same) · [Domande frequenti](#faq)

## Piano rapido di migrazione {#quick-migration-plan}

Una migrazione controllata segue quest'ordine:

1. **Inventaria l'origine.** Registra applicazione, runtime, database, file, DNS, posta, attività cron, worker, webhook e dipendenze esterne.
2. **Dimensiona la destinazione.** Scegli CPU, RAM e disco in base al carico reale e al margine necessario alla migrazione.
3. **Crea un backup ripristinabile.** Conserva una copia fuori dal server di origine e verifica che contenga davvero database e file necessari.
4. **Prepara il VPS in parallelo.** Installa stack web o pannello e soddisfa i requisiti applicativi prima di spostare il traffico.
5. **Copia tutti i dati una prima volta.** Trasferisci i file e importa il database mentre il vecchio sito resta online.
6. **Esegui test privati.** Usa una modifica locale del file hosts, un hostname di anteprima controllato o un metodo equivalente per provare il nuovo server prima del cambio DNS.
7. **Controlla le ultime scritture.** Per negozi, aree riservate, moduli e altri siti con dati variabili, pianifica un breve blocco delle scritture o una sincronizzazione finale delle differenze adatta all'applicazione.
8. **Cambia il DNS per ultimo.** Modifica solo i record necessari al trasferimento e conserva quelli della posta e di verifica.
9. **Monitora entrambi i server.** Controlla traffico, errori, moduli, ordini, cron, webhook, email, HTTPS e scansione dei motori di ricerca.
10. **Dismetti il vecchio hosting solo dopo l'accettazione.** Mantienilo disponibile durante la finestra di rollback.

Non è corretto promettere universalmente zero interruzioni. L'obiettivo è un passaggio controllato, con la minima interruzione praticabile e senza perdite di dati impreviste.

## Definisci cosa viene effettivamente trasferito {#define-what-is-actually-moving}

«Spostare il sito» può coinvolgere sistemi diversi. Definisci l'ambito prima di copiare qualsiasi cosa.

| Componente | Domande da chiarire prima della migrazione |
|---|---|
| Sito / applicazione | CMS o framework, document root, upload, file nascosti, cache, cartelle scrivibili |
| Runtime | versione PHP/Node/Python, estensioni/moduli, server web, gestore dei processi |
| Database | motore/versione, dimensione, utenti/permessi, set di caratteri, manutenzione pianificata |
| DNS | provider, record A/AAAA/CNAME, comportamento www/dominio principale, TTL, record di verifica |
| Email | sede della posta, MX, SPF, DKIM, DMARC, caselle, inoltri, SMTP |
| Attività pianificate | cron, code, worker, importazioni, esportazioni, backup, azioni pianificate |
| Sistemi esterni | webhook di pagamento, API, IP autorizzati, CDN/WAF, analisi delle visite, Search Console |
| Sicurezza / segreti | variabili d'ambiente, chiavi API, chiavi SSH, TLS, regole firewall |

Evita di unire modifiche indipendenti senza una ragione. È più semplice diagnosticare una migrazione quando dominio, struttura URL, versione applicativa e aggiornamenti software principali non cambiano tutti contemporaneamente.

## Verifiche preliminari al passaggio {#migration-cutover-preflight}

Usa questa verifica prima di cambiare il DNS. Non garantisce il successo della migrazione, ma evidenzia i prerequisiti mancanti da risolvere prima.

<div class="rounded-2xl bg-light p-6 dark:bg-darkmode-light">
<form id="migration-preflight">
  <div class="mb-6">
    <label for="mig-backup" class="form-label">Esiste un backup indipendente e il ripristino/importazione è stato provato</label>
    <select id="mig-backup" class="form-input"><option value="no">Non pronto</option><option value="yes">Pronto</option></select>
  </div>
  <div class="mb-6">
    <label for="mig-sizing" class="form-label">CPU, RAM e disco della destinazione sono dimensionati con margine</label>
    <select id="mig-sizing" class="form-input"><option value="no">Non pronto</option><option value="yes">Pronto</option></select>
  </div>
  <div class="mb-6">
    <label for="mig-runtime" class="form-label">Runtime, database ed estensioni richieste sono compatibili</label>
    <select id="mig-runtime" class="form-input"><option value="no">Non pronto</option><option value="yes">Pronto</option></select>
  </div>
  <div class="mb-6">
    <label for="mig-test" class="form-label">Il nuovo sito è stato provato privatamente prima del cambio DNS</label>
    <select id="mig-test" class="form-input"><option value="no">Non pronto</option><option value="yes">Pronto</option></select>
  </div>
  <div class="mb-6">
    <label for="mig-dns" class="form-label">I record DNS sono documentati e TTL e passaggio sono pianificati</label>
    <select id="mig-dns" class="form-input"><option value="no">Non pronto</option><option value="yes">Pronto</option></select>
  </div>
  <div class="mb-6">
    <label for="mig-mail" class="form-label">Sono decise la sede della posta e la gestione di MX/SPF/DKIM/DMARC</label>
    <select id="mig-mail" class="form-input"><option value="no">Non pronto</option><option value="yes">Pronto</option><option value="na">Non applicabile / posta separata e invariata</option></select>
  </div>
  <div class="mb-6">
    <label for="mig-writes" class="form-label">Esiste un piano per le ultime scritture e la sincronizzazione di ordini, moduli, iscritti o upload</label>
    <select id="mig-writes" class="form-input"><option value="no">Non pronto</option><option value="yes">Pronto / sito sostanzialmente in sola lettura</option></select>
  </div>
  <div class="mb-6">
    <label for="mig-tls" class="form-label">HTTPS/TLS può funzionare sulla destinazione con l'hostname reale</label>
    <select id="mig-tls" class="form-input"><option value="no">Non pronto</option><option value="yes">Pronto</option></select>
  </div>
  <div class="mb-6">
    <label for="mig-jobs" class="form-label">Cron, worker, webhook e IP autorizzati sono documentati e controllati</label>
    <select id="mig-jobs" class="form-input"><option value="no">Non pronto</option><option value="yes">Pronto</option><option value="na">Non applicabile</option></select>
  </div>
  <div class="mb-6">
    <label for="mig-rollback" class="form-label">Sono definite le condizioni di rollback e il vecchio hosting resterà disponibile</label>
    <select id="mig-rollback" class="form-input"><option value="no">Non pronto</option><option value="yes">Pronto</option></select>
  </div>
  <button class="btn btn-primary" type="submit">Verifica se il passaggio è pronto</button>
</form>
<p id="migration-preflight-result" class="mt-6 rounded border border-border p-4 dark:border-darkmode-border" role="status" aria-live="polite">Indica i requisiti che sono effettivamente pronti.</p>
</div>

<script>
document.addEventListener("DOMContentLoaded", function () {
  var form = document.getElementById("migration-preflight");
  if (!form) return;

  form.addEventListener("submit", function (event) {
    event.preventDefault();

    var items = [
      ["mig-backup", "backup indipendente"],
      ["mig-sizing", "dimensionamento della destinazione"],
      ["mig-runtime", "compatibilità di runtime e database"],
      ["mig-test", "test privati della destinazione"],
      ["mig-dns", "piano DNS/TTL"],
      ["mig-mail", "piano per email e record DNS della posta"],
      ["mig-writes", "piano delle ultime scritture e della sincronizzazione finale"],
      ["mig-tls", "predisposizione HTTPS/TLS"],
      ["mig-jobs", "cron/worker/webhook/IP autorizzati"],
      ["mig-rollback", "piano di rollback"]
    ];

    function isComplete(id) {
      var value = document.getElementById(id).value;
      return value === "yes" || value === "na";
    }

    var missing = items.filter(function (item) {
      return !isComplete(item[0]);
    }).map(function (item) {
      return item[1];
    });

    var result;
    if (missing.length === 0) {
      result = "PRONTO PER UN PASSAGGIO CONTROLLATO: tutti i requisiti sono indicati come pronti o esplicitamente non applicabili. Ricontrolla sincronizzazione finale e condizioni di rollback subito prima di modificare il DNS.";
    } else {
      result = "PASSAGGIO NON ANCORA PRONTO: risolvi prima queste lacune: " + missing.join(", ") + ".";
    }

    document.getElementById("migration-preflight-result").textContent = result;
  });
});
</script>

## Inventaria il sito attuale {#inventory-the-current-website}

Prepara un registro di migrazione prima di intervenire sulla destinazione.

Registra:

- dominio e tutti i sottodomini attivi;
- versione di applicazione/CMS/framework;
- versione di PHP, Node.js, Python o altro runtime;
- motore/versione del database, dimensione e modello delle credenziali;
- document root e cartelle esterne;
- upload/contenuti multimediali e cartelle scrivibili;
- redirect e regole di riscrittura;
- cron, code, worker e attività pianificate;
- servizi di cache come Redis, se utilizzati;
- configurazione SSL/TLS;
- record DNS;
- caselle email, inoltri e percorso SMTP in uscita;
- gateway di pagamento, webhook e callback API;
- elenchi di IP autorizzati presso servizi terzi;
- vincoli CDN/WAF e accesso all'origine;
- verifiche Search Console e strumenti di analisi;
- spazio disco attualmente utilizzato e crescita.

L'inventario serve anche da checklist di accettazione dopo la migrazione: ogni elemento deve funzionare sul VPS oppure essere lasciato intenzionalmente su un servizio esterno.

## Dimensiona e prepara il VPS di destinazione {#size-and-prepare-the-destination-vps}

Non migrare per poi chiederti se il VPS è abbastanza grande.

Scegli la destinazione considerando carico attuale, comportamento del database, crescita dei dati, consumo di pannello/posta e spazio di lavoro per la migrazione. Il trasferimento stesso può richiedere spazio temporaneo per archivi, dump del database, log e preparazione locale dei backup.

Per il calcolo delle risorse usa [Dimensionamento VPS per siti web]({{< relref "vps-sizing-for-website.md" >}}), senza duplicarlo qui.

La migrazione comporta anche una scelta di gestione. Se il vecchio hosting si occupava di gran parte dell'amministrazione, decidi prima chi gestirà la destinazione dopo il passaggio: confronta [VPS gestito o non gestito]({{< relref "managed-vs-unmanaged-vps.md" >}}). Scegli poi tra pannello di controllo e stack Linux amministrato manualmente; consulta [VPS con pannello di controllo]({{< relref "vps-with-control-panel.md" >}}).

<p>
  <a class="btn btn-primary" href="https://www.vdsina.com/?partner=ni8gzrvz75" target="_blank" rel="sponsored nofollow noopener">Scegli il VPS di destinazione</a>
</p>
<p><small>Trasparenza: il redattore ha un rapporto professionale con VDSina e il sito può ricevere una commissione se ordini tramite questo link di affiliazione. Le indicazioni sulla migrazione e i criteri di dimensionamento non dipendono dalla commissione.</small></p>

## Crea un backup che consenta il rollback {#create-a-rollback-capable-backup}

Un backup è utile solo se contiene i dati necessari ed è ripristinabile.

Prima della migrazione:

1. crea una copia aggiornata dei file del sito;
2. esporta tutti i database necessari;
3. conserva una copia fuori dall'account di hosting di origine;
4. salva in modo sicuro file di configurazione e variabili d'ambiente;
5. registra separatamente record DNS e della posta;
6. se possibile, ripristina il backup in un ambiente temporaneo o di test; almeno importa realmente il database e verifica file rappresentativi, senza limitarti ad aprire l'archivio;
7. conferma che la copia ripristinata contenga i dati attesi e si avvii quanto basta per consentire il rollback;
8. scrivi la sequenza di rollback prima di modificare il DNS.

Per un sito dinamico, il primo backup non contiene i dati finali di produzione. Ordini, invii dei moduli, commenti, iscrizioni e upload possono cambiare dopo la prima copia. Pianifica separatamente la sincronizzazione delle ultime differenze.

## Prepara la destinazione prima di cambiare il DNS {#build-the-destination-before-dns-changes}

La destinazione deve poter eseguire il sito prima dell'arrivo del traffico pubblico.

Riproduci o verifica esplicitamente:

- comportamento del server web;
- versione PHP/Node/Python;
- estensioni/moduli richiesti;
- motore/versione del database;
- proprietari e permessi dei file;
- limiti degli upload e del corpo delle richieste;
- ambiente delle attività pianificate;
- servizi di cache;
- regole di riscrittura e redirect;
- variabili d'ambiente e segreti;
- esigenze SMTP e di rete in uscita;
- regole firewall;
- percorsi specifici dell'applicazione.

Non approfittare della migrazione per aggiornare ogni runtime o riscrivere lo stack, salvo necessità. Meno modifiche simultanee rendono più semplici diagnosi e rollback.

## Copia file e database {#copy-files-and-database}

Il metodo di trasferimento dipende dall'accesso disponibile all'origine.

Le opzioni tipiche includono:

- cPanel/File Manager ed esportazioni phpMyAdmin;
- SFTP/FTP se non è disponibile l'accesso shell;
- SSH/rsync quando consentiti da entrambe le parti;
- strumenti di migrazione consapevoli dell'applicazione per trasferimenti specifici del CMS;
- strumenti di esportazione o backup del provider.

Conserva i file di configurazione nascosti, come le regole di riscrittura, quando servono all'applicazione. Dopo l'importazione, verifica utente e privilegi del database, presupposti su set di caratteri/collation e impostazioni di connessione dell'applicazione.

Per grandi quantità di dati, confronta dimensioni, numero di righe o checksum quando possibile, senza presumere che «trasferimento completato» significhi «dati identici».

## Esegui test privati prima del passaggio {#test-privately-before-cutover}

Non indirizzare il DNS verso un server non verificato.

Prova la destinazione con una modifica locale del file hosts, un hostname di anteprima controllato o un altro metodo privato che eserciti lo stack applicativo reale.

Controlla:

- home e pagine interne rappresentative;
- accesso amministratore;
- accesso utenti;
- immagini, CSS, JavaScript e download;
- ricerca;
- moduli e recapito dei messaggi;
- upload;
- redirect;
- endpoint API;
- checkout e callback di pagamento;
- cron e azioni pianificate;
- code e worker;
- posta in uscita;
- log di applicazione, server web e database;
- impaginazione e navigazione su dispositivi mobili.

Un hostname pubblico temporaneo non deve diventare un duplicato involontario nei motori di ricerca. Se è accessibile durante i test, impediscine l'indicizzazione e rimuovi i blocchi temporanei dall'hostname reale di produzione prima del passaggio.

## Controlla le nuove scritture e la sincronizzazione finale {#control-new-writes-and-the-final-sync}

Questa è la differenza principale tra un sito vetrina e un sito transazionale.

Se vecchio e nuovo database accettano scritture durante il cambio DNS, possono divergere. Un ordine salvato sul vecchio server non compare automaticamente su quello nuovo.

Per i siti con dati in evoluzione:

1. scegli una finestra di passaggio a basso rischio;
2. sospendi o controlla le nuove scritture all'origine, quando praticabile;
3. ferma o controlla cron e worker delle code che potrebbero scrivere gli stessi dati due volte;
4. esegui la sincronizzazione finale del database e copia upload e file modificati;
5. annota l'istante finale a cui corrispondono i dati autorevoli;
6. sposta il traffico;
7. verifica che le nuove scritture arrivino solo alla destinazione.

Per [VPS per WooCommerce]({{< relref "vps-for-woocommerce.md" >}}), includi nel test di accettazione checkout, ordini, webhook di pagamento, scorte, azioni pianificate ed email transazionali. Per un sito statico o con cache può bastare un confronto finale dei file.

Non definire una migrazione «senza interruzioni» se applicazione e metodo di sincronizzazione non lo consentono realmente.

## Cambia il DNS in modo controllato {#switch-dns-deliberately}

Il DNS è il punto di commutazione del traffico, non il primo passo della migrazione.

Prima del passaggio:

- esporta o registra la zona attuale;
- identifica esattamente quali record A/AAAA/CNAME o impostazioni dell'origine devono cambiare;
- se possibile, abbassa il TTL pertinente almeno un intero intervallo del vecchio TTL prima del passaggio; per esempio, se è di 86,400 secondi, riducilo più di 24 ore prima;
- ricorda che abbassare ora il TTL non elimina le cache che hanno già memorizzato quello precedente, più lungo;
- conserva MX, SPF, DKIM, DMARC, TXT di verifica, SRV, CAA e gli altri record che non vengono trasferiti;
- verifica il comportamento sia del dominio principale sia di www.

Se il provider DNS non cambia, modificare un record A/AAAA comporta in genere meno rischi che sostituire i nameserver. Se cambi nameserver, ricrea prima l'intera zona necessaria.

Dopo il passaggio, verifica il DNS pubblico tramite più resolver o reti e osserva lo spostamento del traffico dal vecchio server al nuovo.

## Evita interruzioni della posta {#keep-email-from-breaking}

Migrazione del sito e migrazione della posta sono attività separate, anche se il vecchio account di hosting condiviso le includeva entrambe.

Scegli una soluzione prima del passaggio:

- mantieni la posta presso il provider attuale o gestito e conserva i record MX/TXT esistenti;
- trasferisci la posta a un altro provider gestito;
- trasferisci la posta sul VPS e ricrea caselle, instradamento, autenticazione e controlli di recapito.

Se trasferisci la posta, considera:

- priorità MX;
- SPF;
- DKIM;
- DMARC;
- DNS inverso/PTR, dove applicabile;
- dati delle caselle;
- alias e inoltri;
- credenziali SMTP;
- filtri antispam;
- backup e reputazione del mittente.

Non sostituire un'intera zona DNS solo per spostare il sito, a meno di riprodurre i record della posta e tutte le altre dipendenze.

## Verifica HTTPS, CDN e servizi esterni {#verify-https-cdn-and-external-services}

Se non hai ancora scelto la regione di destinazione, fallo prima del passaggio usando [Come scegliere la posizione del VPS]({{< relref "how-to-choose-vps-location.md" >}}). Cambiarla in seguito può richiedere un'altra migrazione di IP e DNS.

Una destinazione funzionante tramite IP può comunque non funzionare con l'hostname reale.

Verifica che:

- il certificato TLS copra gli hostname necessari;
- il redirect HTTP → HTTPS sia corretto;
- il comportamento canonico tra dominio principale e www resti invariato;
- i presupposti relativi a HSTS siano chiari;
- CDN/WAF puntino alla nuova origine o ne consentano l'accesso;
- la gestione dell'IP reale del client funzioni ancora in presenza di proxy;
- i webhook di pagamento raggiungano la nuova origine;
- siano aggiornati i provider API che autorizzano il vecchio IP del server;
- le credenziali SMTP/API siano valide dal nuovo server.

Limita le eccezioni temporanee di firewall/WAF allo stretto necessario e rimuovile dopo l'accettazione.

## Conserva la SEO quando gli URL non cambiano {#preserve-seo-when-urls-stay-the-same}

Un semplice cambio di hosting mantiene normalmente gli stessi URL pubblici. In questo caso il lavoro SEO consiste soprattutto nel **preservare l'equivalenza**, non nel mappare redirect.

Prima e dopo il passaggio confronta:

- codici di stato HTTP;
- URL canonici;
- robots.txt;
- meta robots ed eventuali noindex accidentali;
- URL della sitemap;
- link interni;
- dati strutturati, dove rilevanti;
- contenuto delle pagine e risorse visualizzate;
- verifica Search Console;
- risposte del server a Googlebot e agli utenti normali.

Google Search Central raccomanda di preparare e provare il nuovo hosting, cambiare DNS solo quando è pronto, monitorare vecchio e nuovo ambiente e dismettere quello precedente dopo lo spostamento del traffico. Raccomanda inoltre di abbassare in anticipo il TTL DNS e mantenere funzionante la verifica Search Console.

Se cambia solo l'infrastruttura di hosting e dominio e URL restano invariati, **non usare lo strumento Cambio di indirizzo di Google Search Console**. Serve ai trasferimenti di dominio, non a migrazioni di hosting con gli stessi URL.

Se cambiano anche dominio o percorsi, usa una mappa dai vecchi ai nuovi URL e redirect permanenti lato server. È un tipo di trasferimento diverso dalla migrazione su VPS a URL invariati.

## Checklist del passaggio {#cutover-checklist}

Subito prima del cambio DNS:

| Controllo | Condizione di superamento |
|---|---|
| Backup | esiste una copia indipendente; ripristino/importazione provati e dati rappresentativi verificati |
| Destinazione | runtime, database, permessi e segreti corretti |
| Test privati | pagine, moduli, accesso e checkout/API, dove applicabili, superano i test |
| Dati finali | sincronizzate le ultime differenze di database/upload; annotato l'istante dei dati autorevoli |
| Attività | vecchi cron/worker controllati; nuove attività avviate al momento previsto |
| DNS | identificati i record esatti da cambiare; conservati quelli di posta e verifica |
| HTTPS | la destinazione serve in sicurezza l'hostname reale |
| Servizi esterni | gestiti webhook, IP autorizzati, CDN/WAF e SMTP |
| Equivalenza SEO | canonical, robots, sitemap e codici di stato corrispondono a quanto previsto |
| Rollback | definite condizioni di attivazione, azione responsabile e disponibilità del vecchio hosting |

Non effettuare il passaggio solo perché «i file sono stati copiati». Fallo quando la destinazione supera i criteri di accettazione.

## Accettazione dopo la migrazione e rollback {#post-migration-acceptance-and-rollback}

Dopo il cambio DNS:

- monitora log di accesso ed errori su vecchio e nuovo server;
- conferma che le nuove attività degli utenti raggiungano il database di destinazione;
- riprova moduli, checkout, accessi e upload;
- verifica cron, code e azioni pianificate;
- verifica posta in uscita e instradamento di quella in ingresso, se pertinenti;
- osserva CPU, RAM, disco e comportamento del database;
- conferma il funzionamento di HTTPS e CDN/WAF;
- controlla l'equivalenza di risposte 200 e redirect sugli URL importanti;
- monitora in Search Console i segnali di scansione e indicizzazione;
- mantieni disponibile il vecchio ambiente per la finestra di stabilità concordata.

### Il rollback ha un limite legato ai dati {#rollback-has-a-data-boundary}

Nelle prime fasi può bastare riportare il DNS al vecchio server, **solo finché questo contiene ancora i dati autorevoli**.

Dopo che ordini, registrazioni, commenti o upload vengono scritti sul nuovo server, un rollback del solo DNS può perdere quelle modifiche. A quel punto servono una riconciliazione dei dati o un'altra sincronizzazione pianificata.

Definisci prima della migrazione le condizioni di rollback, per esempio:

- errori 5xx diffusi;
- malfunzionamento di checkout o pagamenti;
- corruzione del database o scritture mancanti;
- grave incompatibilità del runtime;
- autenticazione non funzionante;
- guasto critico di posta o webhook non risolvibile nella finestra concordata.

## Note su WordPress, WooCommerce e applicazioni personalizzate {#wordpress-woocommerce-and-custom-application-notes}

### WordPress {#wordpress}

Verifica versione ed estensioni PHP, compatibilità del database, upload, riscritture, comportamento di wp-cron, cache, SMTP/moduli di contatto e accesso amministratore. Evita sostituzioni indiscriminate che possono danneggiare dati serializzati; usa strumenti consapevoli dell'applicazione quando necessario.

Per il comportamento delle risorse, consulta [VPS per WordPress]({{< relref "vps-for-wordpress.md" >}}).

### WooCommerce e altri siti transazionali {#woocommerce-and-other-transactional-sites}

Considera ordini, scorte, callback di pagamento, sessioni, azioni pianificate ed email transazionali come dati in continua evoluzione. Pianifica un passaggio finale di database e scritture, senza affidarti alla prima copia.

Consulta [VPS per WooCommerce]({{< relref "vps-for-woocommerce.md" >}}).

### Applicazioni personalizzate {#custom-applications}

Documenta variabili d'ambiente, segreti, worker in background, code, versioni di compilazione/runtime, object storage, percorsi dei file, webhook, IP autorizzati dalle API e procedure di rilascio e avvio. Prova il comportamento dell'hostname reale, non solo la risposta dell'IP.

## Riferimenti tecnici {#technical-references}

- Google Search Central: cambio di hosting e SEO
- Google Search Central: trasferimenti di siti con modifica degli URL

<p>
  <a class="btn btn-primary" href="https://www.vdsina.com/?partner=ni8gzrvz75" target="_blank" rel="sponsored nofollow noopener">Scegli un VPS per la migrazione</a>
</p>
<p><small>Trasparenza: il redattore ha un rapporto professionale con VDSina. I link di affiliazione sono contrassegnati sponsored. Prezzi VPS, traffico incluso e altre condizioni del provider possono cambiare: verifica l'offerta attuale prima dell'ordine.</small></p>

## Domande frequenti {#faq}

### Posso migrare un sito su VPS senza cambiare dominio? {#can-i-migrate-a-website-to-a-vps-without-changing-the-domain}

Sì. La migrazione di hosting può mantenere dominio e URL pubblici. Prepara e verifica prima la destinazione, poi modifica i record DNS per inviare il traffico al nuovo server.

### Servono redirect 301 per spostare un sito su VPS? {#do-i-need-301-redirects-when-moving-a-website-to-a-vps}

Non se gli URL pubblici restano invariati. I redirect servono quando cambiano realmente gli URL, per esempio con un nuovo dominio, un cambio di protocollo o percorso, oppure una riorganizzazione dei contenuti.

### Come riduco le interruzioni durante la migrazione su VPS? {#how-do-i-reduce-downtime-during-a-vps-migration}

Prepara la destinazione in parallelo, abbassa in anticipo il TTL DNS pertinente, esegui test privati, controlla le ultime scritture, sincronizza i dati finali, cambia DNS solo dopo l'accettazione e mantieni disponibile il vecchio hosting durante la propagazione.

### Devo trasferire anche la posta sul VPS? {#should-i-move-email-to-the-vps-too}

Non automaticamente. Lasciarla su un servizio email gestito può ridurre i rischi di migrazione e recapito. Se la trasferisci, pianifica separatamente MX, SPF, DKIM, DMARC, dati delle caselle, DNS inverso dove pertinente e backup.

### Cosa devo provare prima di cambiare il DNS? {#what-should-i-test-before-changing-dns}

Prova pagine rappresentative, accesso, moduli, upload, ricerca, checkout e callback di pagamento dove pertinenti, attività pianificate, API/webhook, posta in uscita, HTTPS, redirect e log di applicazione e server.

### Per quanto tempo devo conservare il vecchio hosting? {#how-long-should-i-keep-the-old-hosting-after-migration}

Finché il traffico DNS è passato alla destinazione, il nuovo server è stabile, le nuove scritture sono verificate e la finestra di rollback concordata è terminata. Usa i log, non un numero universale di ore o giorni.

### Posso migrare WooCommerce senza perdere ordini? {#can-i-migrate-woocommerce-without-losing-orders}

Sì, ma non affidandoti a una sola vecchia copia del database. Controlla le scritture durante il passaggio ed esegui una sincronizzazione finale adatta all'applicazione, affinché ordini e variazioni delle scorte non si dividano tra due database scrivibili.

### Cambiare hosting danneggia la SEO? {#does-moving-hosting-hurt-seo}

Un cambio di hosting a URL invariati dovrebbe preservare i segnali di ricerca se la destinazione restituisce gli stessi contenuti, codici di stato, canonical e possibilità di scansione. Monitora Search Console e log dopo la migrazione: possono verificarsi variazioni temporanee della frequenza di scansione durante un cambio d'infrastruttura.
