---
title: "Strategia di backup VPS"
description: "Strategia di backup VPS: definisci RPO e RTO, combina immagini del provider e copie esterne indipendenti, proteggi database e segreti, imposta la conservazione e prova il ripristino."
image: "images/home/vps-for-website-hero.webp"
slug: "strategia-di-backup-vps"
---

Una strategia di backup VPS non significa «attivare snapshot una volta al giorno». Un piano utilizzabile definisce **quanti dati puoi perdere (RPO), quanto può durare il recupero (RTO), quali dati devono sopravvivere, dove sono le copie indipendenti, quanto conservare le versioni e se qualcuno le ha davvero ripristinate**.

Un piano solido combina di solito recupero rapido presso il provider, copia indipendente fuori dal server e backup DB consapevoli dell’applicazione. La combinazione dipende dalla velocità di cambiamento dei dati e dal costo dei fermi.

Serve anche un responsabile. Se nessuno gestisce processi falliti, prove di ripristino e decisioni di recupero, definisci prima il modello operativo: vedi [VPS gestito o non gestito]({{< relref "managed-vs-unmanaged-vps.md" >}}).

Per la scelta complessiva del server, consulta [VPS per siti web]({{< relref "_index.md" >}}).

[Risposta rapida](#quick-answer) · [Verifica](#vps-backup-strategy-checker) · [RPO / RTO](#start-with-rpo-and-rto) · [Livelli di backup](#snapshot-image-file-backup-and-replication-are-different) · [3-2-1](#a-practical-3-2-1-model-for-vps) · [Prove di ripristino](#test-restores-and-measure-real-rto) · [VDSina](#how-vdsina-backups-fit-the-strategy) · [Domande frequenti](#faq)

## Risposta rapida {#quick-answer}

Un progetto pratico di recupero VPS ha più livelli:

| Livello | Compito principale | Che cosa non dimostra |
|---|---|---|
| **Immagine di backup / snapshot del provider** | rollback o ricostruzione rapida dell’intero server | recupero indipendente se account o storage del provider non sono disponibili |
| **Backup coerente del database** | recupero dello stato applicativo e delle scritture recenti | configurazione completa del server da solo |
| **Backup di file/configurazioni** | ripristino di caricamenti, configurazioni, dati applicativi e file selezionati | recupero rapido dell’intero server |
| **Copia esterna indipendente** | sopravvivenza al guasto di provider, account o server principale | RTO breve senza prove di ripristino |
| **Esercitazione di ripristino** | verifica che copie, chiavi e procedura funzionino davvero | correttezza dei backup futuri senza monitoraggio |

Per molti VPS web ordinari, una buona base comprende:

- immagine o snapshot del provider per rollback rapido;
- backup cifrato indipendente di file, configurazione e DB in un altro dominio di guasto;
- più punti di ripristino;
- frequenza DB scelta in base alla perdita di dati accettabile;
- prove regolari di ripristino.

È più utile che fidarsi di un solo stato «backup riuscito».

## Verifica della strategia di backup VPS {#vps-backup-strategy-checker}

Questo strumento identifica l’architettura di recupero necessaria. Non garantisce il recupero.

<div class="rounded-2xl bg-light p-6 dark:bg-darkmode-light">
<form id="vps-backup-strategy-checker-form">
  <div class="mb-6">
    <label for="bk-workload" class="form-label">Tipo di carico</label>
    <select id="bk-workload" class="form-input">
      <option value="static">Sito statico / vetrina / con modifiche rare</option>
      <option value="cms">WordPress / CMS / sito aziendale</option>
      <option value="transactional">WooCommerce / ordini / area membri / scritture frequenti</option>
    </select>
  </div>
  <div class="mb-6">
    <label for="bk-rpo" class="form-label">Perdita massima di dati accettabile (RPO)</label>
    <select id="bk-rpo" class="form-input">
      <option value="24">Fino a 24 ore</option>
      <option value="4">Fino a 4 ore</option>
      <option value="1">Fino a 1 ora</option>
      <option value="lt1">Meno di 1 ora</option>
    </select>
  </div>
  <div class="mb-6">
    <label for="bk-rto" class="form-label">Fermo massimo accettabile (RTO)</label>
    <select id="bk-rto" class="form-input">
      <option value="24">Fino a 24 ore</option>
      <option value="4">Fino a 4 ore</option>
      <option value="1">Circa 1 ora</option>
      <option value="lt1">Meno di 1 ora</option>
    </select>
  </div>
  <div class="mb-6">
    <label for="bk-offsite" class="form-label">Esiste una copia indipendente fuori dal server o dalla sede principale?</label>
    <select id="bk-offsite" class="form-input"><option value="no">No</option><option value="yes">Sì</option></select>
  </div>
  <div class="mb-6">
    <label for="bk-db" class="form-label">Metodo di backup coerente del database verificato?</label>
    <select id="bk-db" class="form-input">
      <option value="na">Non applicabile / nessun database</option>
      <option value="no">No / non so</option>
      <option value="yes">Sì</option>
    </select>
  </div>
  <div class="mb-6">
    <label for="bk-restore" class="form-label">Una prova di ripristino recente è riuscita?</label>
    <select id="bk-restore" class="form-input"><option value="no">No</option><option value="yes">Sì</option></select>
  </div>
  <div class="mb-6">
    <label for="bk-creds" class="form-label">Credenziali dei backup e chiave di recupero della cifratura sono separate dal VPS?</label>
    <select id="bk-creds" class="form-input"><option value="no">No / non so</option><option value="yes">Sì</option></select>
  </div>
  <div class="mb-6">
    <label for="bk-versions" class="form-label">Sono disponibili più punti di ripristino o uno storico?</label>
    <select id="bk-versions" class="form-input"><option value="no">Solo l’ultimo / non so</option><option value="yes">Sì</option></select>
  </div>
  <button class="btn btn-primary" type="submit">Verifica la strategia di backup</button>
</form>
<p id="vps-backup-strategy-result" class="mt-6 rounded border border-border p-4 dark:border-darkmode-border" role="status" aria-live="polite">Seleziona i requisiti di recupero effettivi.</p>
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
      result = "LACUNE CRITICHE NEI BACKUP: la strategia dipende ancora da un recupero non verificato o non indipendente. Aggiungi copie esterne indipendenti, più punti di ripristino, credenziali e chiavi separate, backup coerenti del database quando necessari e una vera prova di ripristino.";
    } else if (rto === "lt1" || rto === "1") {
      result = "RTO RIDOTTO / RIVALUTA IL RECUPERO DA DISASTRO: i backup possono essere corretti, ma la ricostruzione manuale può superare l’obiettivo di un’ora. Cronometra un recupero completo e valuta automazione, immagini pronte, standby predisposto o separazione dei carichi se l’RTO misurato è troppo lungo.";
    } else if (workload === "transactional" || rpo === "lt1" || rpo === "1") {
      result = "PERCORSO TRANSAZIONALE / BACKUP DB FREQUENTI: mantieni livelli di recupero indipendenti, ma scegli la frequenza del database in base all’RPO richiesto. Un backup notturno non soddisfa una perdita massima di dati di un’ora.";
    } else {
      result = "STRATEGIA DI RECUPERO DI BASE: i livelli principali sono presenti. Mantieni punti di recupero del provider e backup esterni indipendenti, monitora gli errori, conserva più versioni e ripeti prove di ripristino cronometrate.";
    }

    document.getElementById("vps-backup-strategy-result").textContent = result;
  });
});
</script>

## Parti da RPO e RTO {#start-with-rpo-and-rto}

Due valori devono guidare la strategia.

### Obiettivo del punto di ripristino — RPO {#recovery-point-objective--rpo}

L’RPO risponde a questa domanda:

**Quanti dati recenti può permettersi di perdere l’attività?**

Se l’RPO è:

- **24 ore** — un punto di recupero giornaliero riuscito può essere accettabile;
- **4 ore** — i backup giornalieri non bastano;
- **1 ora** — lo stato mutevole di app e database va protetto almeno con tale frequenza;
- **minuti** — i soli backup pianificati ordinari potrebbero non bastare.

L’RPO riguarda la **perdita di dati**, non il fermo.

### Obiettivo del tempo di ripristino — RTO {#recovery-time-objective--rto}

L’RTO risponde a questa domanda:

**Quanto può restare indisponibile il sito o servizio?**

Un backup può rispettare l’RPO e non rispettare l’RTO.

Esempio:

- database copiato ogni ora;
- perdita dei dati più recenti inferiore a un’ora;
- ma ricreare il VPS, scaricare i dati, ripristinare il DB e verificare il sito richiede sei ore.

La strategia può soddisfare un RPO di un’ora, ma ha un RTO effettivo vicino a sei ore.

Le indicazioni NIST sulla pianificazione di emergenza definiscono RPO come punto temporale di recupero e RTO come finestra massima accettabile di indisponibilità. Stabilisci questi obiettivi prima di scegliere gli strumenti.

## Che cosa salvare nei backup? {#what-should-be-backed-up}

Classifica il server in parti **ricostruibili** e **con stato/insostituibili**.

### Ricostruibili {#rebuildable}

Spesso riproducibili da codice o automazione:

- sistema operativo di base;
- pacchetti;
- codice applicativo già conservato in sicurezza in Git;
- immagini container ricostruibili o scaricabili;
- pacchetti standard del server web.

### Con stato / difficili da ricreare {#stateful--difficult-to-recreate}

Di solito con priorità maggiore:

- database;
- caricamenti e media degli utenti;
- caselle email, se locali;
- configurazione;
- ambiente e segreti necessari al recupero;
- chiavi TLS/private quando non facilmente sostituibili;
- dati generati dall’applicazione;
- configurazione del pannello e dei siti;
- configurazione cron/worker;
- zone DNS se ospitate sul VPS;
- script personalizzati non conservati altrove.

Non sprecare capacità copiando alla cieca cache, file temporanei e artefatti ricostruibili, dimenticando database o segreti necessari ad avviare il sito.

## Snapshot, immagini, backup di file e replica sono diversi {#snapshot-image-file-backup-and-replication-are-different}

Non considerarli intercambiabili.

### Snapshot del provider / immagine del server {#provider-snapshot--server-image}

Utile per:

- rollback rapido dopo un aggiornamento rischioso;
- recupero completo del server;
- clonazione o ricreazione della VM.

Limiti:

- può restare nello stesso dominio di guasto di provider o account;
- può non offrire ripristino granulare di file o siti;
- va comunque compresa la coerenza di app e database;
- un’unica immagine recente offre poco storico.

### Backup a livello di file {#file-level-backup}

Utile per:

- caricamenti;
- configurazione;
- dati applicativi selezionati;
- ripristino granulare.

Strumenti come restic o Borg possono conservare backup cifrati e versionati in repository remoti.

### Backup del database {#database-backup}

Usa un metodo consapevole del motore:

- dump logico;
- strumento di backup nativo;
- snapshot o procedura coerenti con l’applicazione.

Non presumere che copiare file di un database attivo produca un backup utilizzabile.

### Replica / standby {#replication--standby}

La replica può ridurre tempo di recupero o perdita di dati, ma da sola non è un backup storico.

Si possono replicare anche cancellazioni errate, corruzione ed errori applicativi.

Usa replica o standby per disponibilità e RTO quando necessari, mantenendo backup versionati per il recupero storico.

## Un modello 3-2-1 pratico per VPS {#a-practical-3-2-1-model-for-vps}

Il comune modello 3-2-1 significa:

- **3 copie** dei dati importanti;
- **2 modalità di archiviazione o guasto diverse**;
- **1 copia esterna, fuori dal dominio di guasto principale**.

Per un VPS, un’interpretazione pratica può essere:

1. dati di produzione sul VPS;
2. immagine del provider per recupero rapido;
3. backup esterno cifrato di file e database su una destinazione indipendente.

Lo scopo non è rispettare letteralmente uno slogan, ma evitare che un evento distrugga produzione e tutte le copie di recupero.

Esempi di domini di guasto:

- filesystem del VPS;
- storage dei backup del provider;
- account del provider;
- account o provider di storage a oggetti separato;
- copia offline o immutabile.

Se chi controlla il VPS può cancellare tutti i backup con le stesse credenziali, le copie non sono realmente indipendenti.

## Backup coerenti del database {#database-consistent-backups}

Lo stato del database cambia mentre il sito è attivo.

Una strategia valida deve sapere come viene protetto il motore DB.

Per WordPress/MySQL/MariaDB, si può usare:

- dump logici;
- strumenti DB nativi;
- snapshot coordinati;
- software che gestisca esplicitamente la coerenza del database.

Per PostgreSQL, usa metodi di backup o PITR specifici quando richiesti dall’RPO.

Il punto non è lo strumento preciso, ma che il DB ripristinato sia internamente coerente e utilizzabile.

Per stato applicativo e gestione WordPress, vedi [VPS per WordPress]({{< relref "vps-for-wordpress.md" >}}).

Verifica che:

- dump o backup termini;
- il file non sia vuoto;
- ripristino o importazione riesca;
- esistano tabelle e record rappresentativi;
- l’app possa connettersi ed eseguire letture e scritture critiche.

## I siti con transazioni richiedono un RPO diverso {#transactional-sites-need-a-different-rpo}

Un sito vetrina può tollerare una copia del giorno prima.

Un negozio con transazioni potrebbe non tollerarla.

Per WooCommerce, aree membri, fatturazione o ordini, definisci quanto stato recente puoi perdere:

- ordini;
- pagamenti;
- disponibilità di magazzino;
- clienti;
- iscrizioni;
- invii di moduli;
- caricamenti.

Se un negozio riceve ordini ogni ora, un backup DB notturno può perdere molte transazioni.

Usa [VPS per WooCommerce]({{< relref "vps-for-woocommerce.md" >}}) per il carico del negozio. Scegli qui la pianificazione in base alla finestra accettabile di perdita delle transazioni.

## Frequenza e conservazione dei backup {#backup-frequency-and-retention}

L’intervallo tra backup non dovrebbe superare l’RPO della classe di dati protetta.

Dati diversi possono avere pianificazioni diverse:

- DB: frequente;
- caricamenti: frequenti o attivati da eventi;
- OS/configurazione: dopo modifiche importanti e a intervalli pianificati;
- immagine completa del provider: meno frequente, ma utile attorno a modifiche rischiose.

La conservazione protegge dai problemi scoperti in ritardo.

Uno schema illustrativo può mantenere:

- punti di ripristino orari recenti;
- diverse copie giornaliere;
- diverse copie settimanali;
- copie mensili selezionate.

La conservazione esatta dipende da:

- esigenze aziendali di recupero;
- costo dello storage;
- frequenza di cambiamento dei dati;
- requisiti legali e di conformità;
- tempo per cui corruzione o compromissione possono restare inosservate.

Non conservare solo «l’ultimo».

## Mantieni una destinazione indipendente fuori dal server {#keep-an-independent-off-server-destination}

Un backup sul disco dello stesso VPS non protegge da:

- perdita di disco o filesystem;
- cancellazione del server;
- compromissione root;
- ransomware;
- errore nell’account;
- perdita della VM presso il provider.

Trasferisci o invia direttamente i dati di recupero fuori dal VPS.

Destinazioni possibili:

- storage a oggetti;
- altro servizio o provider di backup;
- un altro VPS usato solo per backup;
- storage offline o controllato.

Separa credenziali di provider e account quando possibile.

## Cifra i backup e proteggi la chiave di recupero {#encrypt-backups--and-protect-the-recovery-key}

Cifra i dati sensibili in transito e a riposo quando opportuno.

La cifratura crea però un’altra dipendenza del recupero.

Non conservare **l’unica** password o chiave del backup:

- solo sul VPS;
- solo nello stesso vault o account che potrebbe diventare indisponibile;
- solo dentro il backup cifrato stesso.

Mantieni credenziali e chiavi in un luogo sicuro e indipendente e verificane la disponibilità nelle prove di ripristino.

## Separa credenziali dei backup e diritti di cancellazione {#separate-backup-credentials-and-deletion-rights}

La compromissione della produzione non dovrebbe consentire automaticamente di eliminare ogni copia di recupero.

Preferisci:

- credenziali di backup con ambito limitato;
- scrittura senza ampi privilegi di cancellazione, se supportata;
- credenziali amministrative separate;
- blocco di conservazione o immutabilità quando opportuni;
- copia offline o isolata dalla rete per dati di alto valore.

Il progetto esatto dipende dal servizio di storage.

Per questo i backup sono anche un controllo di sicurezza: vedi [Checklist di sicurezza VPS]({{< relref "vps-security-checklist.md" >}}).

## Monitora i processi di backup {#monitor-backup-jobs}

L’automazione riduce le dimenticanze, ma può fallire senza segnali.

Monitora:

- ora dell’ultimo backup riuscito;
- processi falliti o parziali;
- disponibilità di repository e storage;
- scadenza delle credenziali;
- spazio libero prima della preparazione locale;
- quota dello storage esterno;
- errori dei dump DB;
- variazioni della durata;
- dimensioni insolitamente piccole;
- errori di conservazione o eliminazione delle vecchie copie.

Uno stato verde di cron o servizio dimostra che il comando è stato eseguito, non che il ripristino funzioni.

Gli avvisi generali su server e servizi sono in [Monitoraggio VPS]({{< relref "vps-monitoring.md" >}}); lo stato dei processi di backup resta parte della strategia di recupero.

## Prova i ripristini e misura l’RTO reale {#test-restores-and-measure-real-rto}

Un backup diventa credibile quando viene ripristinato.

Esegui esercitazioni in una destinazione pulita e isolata.

Verifica una parte sufficiente della sequenza completa:

1. crea un VPS o ambiente di test nuovo;
2. recupera il punto di backup corretto;
3. recupera credenziali di cifratura e repository;
4. ripristina file e configurazione;
5. ripristina o importa il database;
6. ripristina segreti e certificati necessari;
7. configura servizi e rete;
8. avvia l’applicazione;
9. testa pagine e transazioni importanti;
10. verifica attività in background e integrazioni;
11. misura il tempo di recupero trascorso.

Registra il risultato misurato.

Se l’RTO aziendale è quattro ore e il test ne richiede otto, la strategia non soddisfa il requisito anche se ogni file è stato ripristinato.

Le indicazioni NIST sottolineano creazione regolare dei backup, prove di ripristino ed esercitazioni di recupero.

## La granularità del ripristino conta {#restore-granularity-matters}

Una buona strategia risponde al guasto effettivo.

### Recupero di un singolo file o sito {#single-filesite-recovery}

Necessario per:

- caricamento cancellato;
- configurazione danneggiata;
- un sito compromesso;
- recupero di un database o tabella danneggiati.

### Recupero dell’intero server {#full-server-recovery}

Necessario per:

- VPS guasto o cancellato;
- guasto del filesystem;
- compromissione grave;
- sostituzione di provider o server.

Se l’unico backup è un’immagine completa del disco, recuperare un file può essere scomodo.

Se il backup contiene solo file selezionati, ricostruire tutto il VPS può richiedere troppo tempo.

Combina più metodi.

## Più siti richiedono ripristino per singolo sito {#multiple-websites-need-site-level-restore}

Su un VPS multisito, evita che riparare il sito A riporti automaticamente B/C/D allo stato di ieri.

Preferisci backup che permettano di ripristinare:

- una document root;
- un database;
- un pannello o utente;
- un insieme di caricamenti;
- l’intero VPS solo quando necessario.

Per architettura e domini di guasto, consulta [VPS per più siti web]({{< relref "vps-for-multiple-websites.md" >}}).

## Anche i backup possono causare fermi {#backups-can-cause-outages-too}

Le operazioni di backup consumano risorse.

Possibili effetti:

- CPU per dump DB;
- CPU per compressione;
- I/O di lettura;
- occupazione temporanea del disco;
- banda di invio allo storage a oggetti;
- espulsione di dati dalla cache;
- sovrapposizione con importazioni, scansioni o picchi di traffico.

Evita di creare un archivio locale da 30 GB con soli 10 GB liberi sul VPS.

Quando possibile:

- invia i backup direttamente fuori dal server;
- monitora lo spazio temporaneo;
- pianifica le operazioni pesanti fuori dai picchi;
- limita la velocità se lo strumento lo consente;
- misura la durata del backup.

## Come inserire i backup VDSina nella strategia {#how-vdsina-backups-fit-the-strategy}

La documentazione pubblica VDSina descrive attualmente diverse funzioni utili:

- copie manuali del server;
- backup pianificati;
- ripristino sul server di origine;
- creazione di un nuovo server da backup;
- clonazione del server;
- download dell’immagine di backup.

La documentazione del download mostra un nome file nella forma:

`vXXX.backup.hosted-by-vdsina.com.img.gz`

L’immagine scaricabile offre portabilità: una copia di recupero non deve restare solo nel pannello del provider.

Tuttavia:

- considera l’immagine del provider **un livello**, non l’intera strategia;
- testa come l’ambiente di recupero scelto usa l’immagine scaricata;
- non presumere che ogni hypervisor la utilizzi direttamente senza conversione;
- mantieni backup applicativi, di file e DB per recupero granulare;
- conserva una copia in un dominio di guasto indipendente quando il rischio lo giustifica.

Le condizioni VDSina attribuiscono esplicitamente al cliente la responsabilità dei backup e consigliano una procedura regolare con prove periodiche di ripristino.

Per creare un nuovo server da backup, le risposte VDSina indicano vincoli come collocazione nel data center e quota disco sufficiente; dopo il ripristino possono servire modifiche alla rete.

Non confondere backup e migrazione. Un backup può essere una protezione durante il trasferimento, ma passaggio live, ultime scritture, DNS e rollback sono aspetti distinti: vedi [Migrazione di un sito web su VPS]({{< relref "website-migration-to-vps.md" >}}).

<p>
  <a class="btn btn-primary" href="https://www.vdsina.com/?partner=ni8gzrvz75" target="_blank" rel="sponsored nofollow noopener">Verifica le opzioni attuali di backup VPS</a>
</p>
<p><small>Trasparenza: l’autore ha un rapporto professionale con VDSina e questo sito può ricevere una commissione se acquisti tramite questo link partner. Le funzioni del provider non sostituiscono una strategia indipendente o le prove di ripristino.</small></p>

## Procedura operativa di recupero {#recovery-runbook}

Scrivi la procedura prima del fermo.

Registra almeno:

- destinazioni dei backup;
- nomi e conservazione dei punti di ripristino;
- credenziali del repository;
- posizione di recupero delle chiavi di cifratura;
- distinzione tra DB, file e configurazione;
- passaggi per creare un server nuovo;
- versioni software e runtime;
- ordine di ripristino;
- passaggi DNS e rete;
- integrazioni esterne e webhook;
- test di accettazione;
- chi decide recupero e rollback.

Conserva la procedura in un luogo accessibile anche quando il VPS non lo è.

## Checklist dei backup VPS {#vps-backup-checklist}

| Controllo | Condizione di superamento |
|---|---|
| RPO | finestra massima accettabile di perdita dati definita |
| RTO | fermo massimo accettabile definito |
| Inventario dati | DB, caricamenti, configurazione, segreti e altro stato classificati |
| Recupero del provider | pianificazione di immagini/snapshot compresa |
| Database | metodo specifico del motore e ripristinabile |
| Copia esterna | copia indipendente fuori dal dominio di guasto VPS |
| Credenziali | account backup limitato e separato dalla produzione |
| Cifratura | backup sensibili cifrati quando opportuno |
| Recupero chiavi | chiave o password conservata fuori dal VPS guasto |
| Conservazione | più punti di ripristino storici |
| Monitoraggio | rilevamento di processi falliti, parziali o backup obsoleti |
| Disco/I/O | il backup non riempie o sovraccarica la produzione senza segnali |
| Granularità | ripristino di file, sito o DB dove necessario |
| Recupero completo | esiste un percorso per ricostruire VPS e servizi |
| Prova di ripristino | ripristino isolato riuscito |
| RTO misurato | durata reale registrata ed entro l’obiettivo |
| Procedura operativa | ordine, credenziali, DNS e test documentati |
| Responsabile | persona o team specifici per backup e ripristino |

## Riferimenti tecnici {#technical-references}

- NIST SP 800-34 Rev.1 — RPO/RTO e pianificazione di emergenza
- NIST SP 1339 — creazione, test ed esercitazioni di recupero dei backup
- Ubuntu — strumento restic per backup e ripristino
- Ubuntu — BorgBackup
- Condizioni VDSina — responsabilità del cliente sui backup
- VDSina — backup, ripristino e creazione di server da backup
- VDSina — backup pianificati
- VDSina — download e uso del backup di un server

## Domande frequenti {#faq}

### Qual è una buona strategia di backup VPS? {#what-is-a-good-vps-backup-strategy}

Definisci RPO/RTO, mantieni copie indipendenti, proteggi i DB con un metodo coerente con l’applicazione, conserva più versioni, monitora gli errori e ripristina regolarmente in un ambiente di test pulito.

### Basta uno snapshot VPS? {#is-a-vps-snapshot-enough}

Non come unico livello. Snapshot e immagini del provider aiutano nel rollback rapido e nel recupero completo, ma possono condividere il dominio di guasto di account/provider e risultare meno comodi per ripristini granulari.

### Che cosa significa 3-2-1 per un VPS? {#what-does-3-2-1-mean-for-a-vps}

Mantieni dati live e più copie di recupero su storage o domini di guasto indipendenti, con almeno una copia fuori dal percorso di guasto del VPS o provider principale.

### Con quale frequenza fare il backup del VPS? {#how-often-should-i-back-up-a-vps}

Scegli in base all’RPO di ogni tipo di dato. Un sito statico può tollerare copie giornaliere; un DB con transazioni può richiedere protezione oraria o più frequente.

### Qual è la differenza tra RPO e RTO? {#what-is-the-difference-between-rpo-and-rto}

RPO è la perdita massima accettabile di dati recenti. RTO è il fermo massimo accettabile prima del ripristino del servizio.

### Salvare tutto il VPS o solo i file del sito? {#should-i-back-up-the-whole-vps-or-only-website-files}

Di solito sono utili entrambi i livelli. L’immagine del server accelera il recupero completo; backup di file e DB semplificano ripristini granulari e coerenti con l’applicazione.

### Come salvare MySQL o PostgreSQL in sicurezza? {#how-do-i-back-up-mysql-or-postgresql-safely}

Usa un backup logico o nativo specifico del motore, oppure un metodo coordinato e coerente con l’app, poi provalo ripristinandolo in un ambiente isolato.

### I backup devono essere cifrati? {#should-backups-be-encrypted}

I dati di recupero sensibili vanno cifrati quando opportuno, ma conserva password o chiave in sicurezza fuori dal VPS guasto.

### La replica è un backup? {#is-replication-a-backup}

Non da sola. Può copiare cancellazioni accidentali, corruzione o modifiche malevole. Mantieni backup storici e versionati oltre a replica o standby.

### VDSina offre backup VPS? {#does-vdsina-provide-vps-backups}

VDSina documenta copie manuali e pianificate, ripristino e creazione di server da backup, oltre a immagini scaricabili. Le condizioni attribuiscono comunque al cliente la responsabilità e consigliano prove periodiche di ripristino.

### Quanto spesso provare i ripristini? {#how-often-should-i-test-restores}

Con una pianificazione definita e dopo modifiche rilevanti a backup o architettura. I sistemi di alto valore o in rapido cambiamento vanno testati abbastanza spesso da mantenere affidabile la procedura misurata.

### Se l’RTO è inferiore a un’ora? {#what-if-my-rto-is-under-one-hour}

Un progetto basato solo sui backup può essere troppo lento. Cronometra un recupero completo e valuta automazione, immagini pronte, standby predisposto o modifiche architetturali se l’RTO misurato supera l’obiettivo.
