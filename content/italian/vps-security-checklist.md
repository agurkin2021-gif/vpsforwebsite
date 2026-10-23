---
title: "Checklist di sicurezza VPS"
description: "Checklist di sicurezza VPS: proteggi accessi amministrativi e servizi esposti, aggiorna il software, custodisci i segreti, verifica i backup e prepara la risposta agli incidenti senza perdere l’accesso."
image: "images/home/vps-for-website-hero.webp"
slug: "checklist-di-sicurezza-vps"
---

La checklist di sicurezza VPS è una verifica ordinata per priorità per un server autogestito esposto a Internet. Non mira a renderlo «sicuro al 100%», ma a eliminare esposizioni evitabili, proteggere gli accessi privilegiati, mantenere il software, consentire il recupero e verificare che qualcuno si occupi davvero della sicurezza.

L’ordine più sicuro conta: **prima preserva una via di recupero, verifica un secondo accesso amministrativo, inventaria i servizi esposti e poi restringi SSH e firewall**.

Se nessuno dalla tua parte gestisce aggiornamenti, firewall, verifica dei backup, monitoraggio e incidenti, definisci prima il modello operativo: vedi [VPS gestito o non gestito]({{< relref "managed-vs-unmanaged-vps.md" >}}).

Per la scelta complessiva del server, consulta [VPS per siti web]({{< relref "_index.md" >}}).

[Controlli di base](#security-baseline-in-order) · [Strumento di verifica](#vps-security-baseline-checker) · [SSH](#harden-administrative-access) · [Firewall](#firewall-only-the-services-you-need) · [Aggiornamenti](#patching-and-automatic-security-updates) · [Backup](#backups-are-a-security-control) · [Risposta agli incidenti](#after-a-suspected-compromise) · [Domande frequenti](#faq)

## Controlli di sicurezza di base, in ordine {#security-baseline-in-order}

Per un tipico VPS Linux pubblico:

1. **Mantieni disponibile console o recupero del provider.**
2. **Crea e testa un amministratore nominativo non root.**
3. **Aggiungi autenticazione SSH con chiave e verifica una seconda sessione.**
4. **Inventaria tutti i servizi in ascolto e le porte pubbliche.**
5. **Restringi SSH, root e password solo dopo aver verificato l’accesso con chiave.**
6. **Applica un firewall che neghi per impostazione predefinita e apri solo le porte necessarie.**
7. **Mantieni privati database, Redis e porte applicative interne per impostazione predefinita.**
8. **Applica gli aggiornamenti OS/pacchetti e assegna la responsabilità dei riavvii.**
9. **Aggiorna anche pannelli, CMS, plugin, runtime e dipendenze.**
10. **Proteggi i segreti e usa utenti e account DB con privilegi minimi.**
11. **Aggiungi protezioni contro forza bruta e limiti di frequenza come difesa aggiuntiva.**
12. **Usa HTTPS per i siti pubblici e proteggi le interfacce amministrative.**
13. **Mantieni backup indipendenti e prova il ripristino.**
14. **Attiva log e avvisi che rendano visibili errori di sicurezza e recupero.**
15. **Definisci la procedura per una sospetta compromissione.**
16. **Ripeti regolarmente la verifica.**

Non proteggere l’accesso remoto incollando comandi alla cieca. Una modifica che blocca l’amministratore legittimo causa un fermo.

## Verifica della sicurezza di base del VPS {#vps-security-baseline-checker}

Usa questo strumento per individuare lacune di base. Non certifica che il server sia sicuro.

<div class="rounded-2xl bg-light p-6 dark:bg-darkmode-light">
<form id="vps-security-checker">
  <div class="mb-6">
    <label for="sec-recovery" class="form-label">Console o percorso di recupero del provider testati?</label>
    <select id="sec-recovery" class="form-input"><option value="no">No / non so</option><option value="yes">Sì</option></select>
  </div>
  <div class="mb-6">
    <label for="sec-admin" class="form-label">Amministratore nominativo non root con accesso SSH tramite chiave testato?</label>
    <select id="sec-admin" class="form-input"><option value="no">No</option><option value="yes">Sì</option></select>
  </div>
  <div class="mb-6">
    <label for="sec-firewall" class="form-label">Firewall attivo con le sole porte pubbliche necessarie consentite?</label>
    <select id="sec-firewall" class="form-input"><option value="no">No / non so</option><option value="yes">Sì</option></select>
  </div>
  <div class="mb-6">
    <label for="sec-services" class="form-label">Servizi in ascolto e porte esposte inventariati?</label>
    <select id="sec-services" class="form-input"><option value="no">No</option><option value="yes">Sì</option></select>
  </div>
  <div class="mb-6">
    <label for="sec-updates" class="form-label">Responsabili degli aggiornamenti OS/app e procedura di riavvio definiti?</label>
    <select id="sec-updates" class="form-input"><option value="no">No</option><option value="yes">Sì</option></select>
  </div>
  <div class="mb-6">
    <label for="sec-backup" class="form-label">Esiste un backup indipendente con ripristino testato?</label>
    <select id="sec-backup" class="form-input"><option value="no">No</option><option value="yes">Sì</option></select>
  </div>
  <div class="mb-6">
    <label for="sec-logs" class="form-label">Gli errori di sicurezza e recupero producono log o avvisi letti da qualcuno?</label>
    <select id="sec-logs" class="form-input"><option value="no">No</option><option value="yes">Sì</option></select>
  </div>
  <div class="mb-6">
    <label for="sec-app" class="form-label">Gli aggiornamenti CMS/pannello/runtime/dipendenze hanno un responsabile?</label>
    <select id="sec-app" class="form-input"><option value="no">No</option><option value="yes">Sì</option></select>
  </div>
  <div class="mb-6">
    <label for="sec-owner" class="form-label">Una persona o un team specifici gestiscono gli incidenti di sicurezza?</label>
    <select id="sec-owner" class="form-input"><option value="no">No</option><option value="yes">Sì</option></select>
  </div>
  <button class="btn btn-primary" type="submit">Verifica la sicurezza di base</button>
</form>
<p id="vps-security-result" class="mt-6 rounded border border-border p-4 dark:border-darkmode-border" role="status" aria-live="polite">Segna solo controlli effettivamente implementati e testati.</p>
</div>

<script>
document.addEventListener("DOMContentLoaded", function () {
  var form = document.getElementById("vps-security-checker");
  if (!form) return;

  form.addEventListener("submit", function (event) {
    event.preventDefault();

    var ids = [
      "sec-recovery",
      "sec-admin",
      "sec-firewall",
      "sec-services",
      "sec-updates",
      "sec-backup",
      "sec-logs",
      "sec-app",
      "sec-owner"
    ];

    var missing = ids.filter(function (id) {
      return document.getElementById(id).value !== "yes";
    });

    var critical = ["sec-recovery", "sec-admin", "sec-firewall", "sec-updates", "sec-backup", "sec-owner"];
    var criticalMissing = critical.filter(function (id) {
      return document.getElementById(id).value !== "yes";
    });

    var result;

    if (criticalMissing.length >= 2) {
      result = "LACUNE CRITICHE: accessi privilegiati, firewall/aggiornamenti, recupero o responsabilità degli incidenti sono incompleti. Non considerare conclusa la sicurezza di base di questo VPS di produzione.";
    } else if (missing.length > 0) {
      result = "BASE INCOMPLETA: i controlli principali esistono, ma restano " + missing.length + " voci della checklist da risolvere. Completa e verifica i controlli, non solo i file di configurazione.";
    } else {
      result = "BASE DI PRODUZIONE PRONTA: i controlli elencati sono implementati e testati. Non è una garanzia di sicurezza: continua con aggiornamenti, monitoraggio, prove di backup e verifiche periodiche.";
    }

    document.getElementById("vps-security-result").textContent = result;
  });
});
</script>

## Mantieni una via di recupero prima di cambiare gli accessi {#keep-a-recovery-path-before-changing-access}

Prima di restringere SSH o attivare un firewall rigoroso, verifica di poter recuperare da una regola errata.

Mantieni disponibile almeno un accesso indipendente dalla normale connessione, come console browser, VNC o interfaccia di recupero del provider.

Poi:

1. crea l’utente amministratore nominativo;
2. aggiungi la chiave pubblica SSH;
3. apri una **seconda** sessione terminale;
4. verifica accesso e privilegi sudo/amministrativi;
5. tieni aperta la sessione funzionante mentre testi le nuove regole;
6. solo allora limita i vecchi metodi di accesso.

Il controllo importante non è «disabilitare root il prima possibile», ma **sostituire l’accesso rischioso con un percorso più sicuro e testato, senza restare bloccati fuori**.

Il primo avvio è descritto in [Come ospitare un sito web su VPS]({{< relref "how-to-host-a-website-on-vps.md" >}}).

## Inventaria i servizi esposti prima di bloccarli {#inventory-exposed-services-before-blocking}

Non indovinare quali porte siano aperte.

Su Linux, esamina i socket in ascolto con strumenti come:

```bash
sudo ss -lntup
```

Per ogni servizio in ascolto, decidi:

- deve esistere?
- deve ascoltare su tutte le interfacce?
- deve essere pubblico?
- può usare solo localhost o una rete privata?
- quali reti sorgenti devono raggiungerlo?
- chi gestisce aggiornamenti e log?

Le porte tipiche di un sito pubblico possono includere:

- accesso SSH/amministrativo;
- HTTP 80;
- HTTPS 443.

Questo **non** significa che ogni server debba esporle tutte e tre all’intera Internet.

Rimuovi i servizi inutilizzati anziché affidarti solo al firewall per nasconderli.

## Proteggi l’accesso amministrativo {#harden-administrative-access}

La documentazione OpenSSH di Ubuntu supporta l’autenticazione a chiave pubblica e consiglia algoritmi moderni come Ed25519.

Un modello amministrativo di base prevede:

- account amministratore nominativo;
- autenticazione SSH con chiave;
- chiave privata protetta da passphrase quando possibile;
- sudo solo agli utenti che ne hanno bisogno;
- nessuna applicazione eseguita come root;
- accesso SSH diretto root/password limitato dopo aver verificato l’alternativa più sicura.

Per ambienti con requisiti di garanzia maggiori, OpenSSH supporta anche modelli più forti, tra cui autenticazione a due fattori FIDO/U2F o TOTP.

### Accesso root e autenticazione con password {#root-login-and-password-authentication}

Non impostare queste opzioni alla cieca prima di verificare chiavi e console di recupero.

Quando l’alternativa più sicura funziona, controlla:

- `PermitRootLogin`;
- `PasswordAuthentication`;
- `AllowUsers` / `AllowGroups`;
- regole di inattività e sessione, se necessarie.

La configurazione esatta dipende dall’ambiente.

Spostare SSH dalla porta 22 può ridurre il rumore degli scanner, ma **non** sostituisce chiavi, privilegi minimi, firewall e software aggiornato.

## Firewall: solo i servizi necessari {#firewall-only-the-services-you-need}

Il frontend predefinito del firewall host di Ubuntu è UFW.

Una base sicura prevede concettualmente:

- negare per impostazione predefinita il traffico in ingresso non richiesto;
- consentire il percorso amministrativo effettivamente usato;
- consentire HTTP/HTTPS per un server web pubblico;
- mantenere privati database e servizi interni;
- verificare il comportamento IPv4 e IPv6.

Preserva l’accesso SSH prima di attivare regole restrittive.

Esempio di verifica:

```bash
sudo ufw status verbose
```

Non copiare un elenco generico «consenti 22/80/443» se l’architettura è diversa.

### Firewall del provider e dell’host {#provider-firewall-and-host-firewall}

Un firewall di rete o del provider può bloccare il traffico prima che raggiunga la VM.

Il firewall host controlla ciò che accetta il sistema operativo ospite.

Usarli entrambi può offrire difesa su più livelli, ma solo con regole documentate e coerenti tra loro.

## Mantieni privati database e servizi interni per impostazione predefinita {#keep-databases-and-internal-services-private-by-default}

Non esporre a Internet MySQL/MariaDB/PostgreSQL, Redis, porte interne Node/Python o socket di controllo solo perché il servizio è in ascolto.

Preferisci:

- localhost per servizi sullo stesso server;
- interfacce private per architetture con più server;
- restrizioni sull’IP sorgente quando serve amministrazione remota;
- SSH/VPN/bastion per le attività amministrative.

Apri pubblicamente una porta DB solo se l’architettura lo richiede espressamente e con accessi fortemente limitati.

## Aggiornamenti e aggiornamenti automatici di sicurezza {#patching-and-automatic-security-updates}

Anche un OS supportato diventa obsoleto se nessuno gestisce gli aggiornamenti.

Ubuntu Server usa `unattended-upgrades` per gli aggiornamenti automatici di sicurezza nelle installazioni supportate, per impostazione predefinita.

È utile, ma il processo deve anche chiarire:

- quali repository sono coperti?
- pacchetti e app di terzi vengono aggiornati?
- un servizio richiedeva un riavvio?
- serve riavviare il server?
- chi controlla gli aggiornamenti falliti?
- quando si possono riavviare in sicurezza i servizi di produzione?

La documentazione Ubuntu indica che possono servire riavvii dei servizi e talvolta del sistema perché il codice aggiornato entri effettivamente in uso.

«Aggiornamenti automatici attivi» non equivale a un processo completo di gestione delle patch.

## Fail2ban, CrowdSec e limiti di frequenza {#fail2ban-crowdsec-and-rate-limiting}

Gli strumenti contro la forza bruta possono ridurre tentativi abusivi ripetuti.

Sono **difesa aggiuntiva su più livelli**, non il modello principale di autenticazione.

Usali dopo aver verificato che:

- gli accessi privilegiati siano protetti;
- l’autenticazione sia robusta;
- i servizi esposti siano pubblici intenzionalmente;
- i log siano disponibili.

Uno strumento di blocco non rende sicuri una password debole, un pannello non aggiornato o un database esposto.

## Privilegi minimi per applicazioni e database {#least-privilege-for-applications-and-databases}

Il principio del minimo privilegio riguarda l’intero stack.

Preferisci:

- utenti di distribuzione e amministrazione separati;
- utenti applicativi separati;
- utenti DB separati per applicazione;
- soli privilegi DB necessari;
- utenti separati per siti di clienti indipendenti;
- scrittura limitata alle directory necessarie all’app.

Evita:

- app web eseguite come root;
- account DB root/amministratore condiviso con le applicazioni;
- `chmod 777` per correggere i permessi;
- un unico utente Unix per clienti indipendenti quando è possibile separarli meglio.

Per l’isolamento multisito, vedi [VPS per più siti web]({{< relref "vps-for-multiple-websites.md" >}}).

## Proteggi segreti e credenziali {#protect-secrets-and-credentials}

Tieni le credenziali di produzione fuori da:

- repository Git pubblici;
- document root accessibili dal web;
- pagine di debug;
- screenshot, ticket e chat;
- cronologia della shell, quando evitabile;
- file d’ambiente leggibili da troppi utenti.

Proteggi:

- password dei database;
- chiavi API;
- credenziali SMTP;
- segreti di pagamenti e webhook;
- credenziali dello storage dei backup;
- credenziali del pannello e degli amministratori;
- chiavi private SSH.

Ruota le credenziali quando personale o collaboratori lasciano il progetto o dopo una sospetta compromissione.

## Pannelli e interfacce amministrative {#control-panels-and-admin-interfaces}

Un pannello è un’applicazione di gestione privilegiata.

Verifica:

- versione attuale del pannello;
- account amministratori;
- 2FA dove supportata;
- porte e nomi host amministrativi esposti;
- restrizioni sull’IP sorgente quando praticabili;
- inventario di plugin ed estensioni;
- comportamento di backup e ripristino;
- log del pannello e accessi falliti.

Non presumere che installare un pannello renda il VPS sicuro o gestito.

Per la scelta del pannello, vedi [VPS con pannello di controllo]({{< relref "vps-with-control-panel.md" >}}). Per il prodotto specifico, vedi [Hosting VPS con FASTPANEL]({{< relref "fastpanel-vps-hosting.md" >}}).

## Aggiornamenti di applicazioni, CMS e runtime {#application-cms-and-runtime-updates}

Un OS completamente aggiornato può comunque ospitare un’app vulnerabile.

La responsabilità di sicurezza deve comprendere:

- PHP/Node/Python/runtime;
- framework;
- core WordPress;
- plugin e temi;
- WooCommerce ed estensioni;
- server web;
- pannello di controllo;
- librerie e dipendenze.

Rimuovi i componenti abbandonati che non ricevono più aggiornamenti di sicurezza.

Per WordPress, vedi [VPS per WordPress]({{< relref "vps-for-wordpress.md" >}}). Per negozi con transazioni, vedi [VPS per WooCommerce]({{< relref "vps-for-woocommerce.md" >}}).

## HTTPS protegge il trasporto, non l’intero server {#https-protects-transport-not-the-whole-server}

HTTPS è necessario per siti di produzione con accessi o dati sensibili ed è una base normale per i siti pubblici.

Protegge i dati in transito tra client e server.

Non corregge:

- plugin vulnerabili;
- SSH debole;
- database pubblici;
- chiavi API esposte;
- pacchetti obsoleti;
- permessi dei file non sicuri;
- backup mancanti.

Verifica il rinnovo dei certificati e controlla scadenze ed errori.

## La protezione DDoS non è sicurezza applicativa {#ddos-protection-is-not-application-security}

VDSina pubblicizza attualmente protezione DDoS gratuita sui VPS Standard.

Le sue domande e risposte pubbliche indicano che il servizio gratuito copre **attacchi L3-L4 al canale e alla rete** e **non è regolato da uno SLA**.

È una protezione utile a livello infrastrutturale e di rete, ma non sostituisce:

- protezione SSH;
- regole del firewall;
- sicurezza dell’applicazione web;
- limiti di frequenza a livello applicativo;
- WAF e controlli sui bot quando opportuni;
- aggiornamenti;
- risposta agli incidenti.

Non descrivere la mitigazione DDoS di rete come un servizio completo di sicurezza del sito.

<p>
  <a class="btn btn-primary" href="https://www.vdsina.com/?partner=ni8gzrvz75" target="_blank" rel="sponsored nofollow noopener">Verifica l’infrastruttura VPS attuale</a>
</p>
<p><small>Trasparenza: l’autore ha un rapporto professionale con VDSina e questo sito può ricevere una commissione se acquisti tramite questo link partner. Protezione DDoS e assistenza tecnica del provider non sostituiscono protezione e amministrazione di OS ospite e applicazioni.</small></p>

## I backup sono un controllo di sicurezza {#backups-are-a-security-control}

La sicurezza comprende il recupero dopo compromissioni, ransomware, aggiornamenti difettosi e cancellazioni accidentali.

Come minimo:

- mantieni una copia fuori dal VPS in esecuzione;
- non affidarti a un solo snapshot o immagine;
- proteggi le credenziali dei backup;
- rendi i backup inaccessibili all’applicazione quando possibile;
- monitora i processi di backup falliti;
- prova il ripristino;
- conosci la quantità di dati perdibile tra punti di ripristino.

CISA consiglia backup offline e cifrati dei dati critici e prove regolari di ripristino in uno scenario di recupero da disastro.

RPO/RTO, conservazione e architettura dei backup sono approfonditi in [Strategia di backup VPS]({{< relref "vps-backup-strategy.md" >}}).

## Log, avvisi e tracciabilità {#logs-alerts-and-audit-trail}

Una configurazione sicura che non osservi mai può smettere di funzionare senza segnali.

Come minimo, controlla:

- errori SSH/autenticazione ripetuti;
- nuovi utenti amministratori/sudo inattesi;
- accessi al pannello falliti;
- modifiche al firewall;
- nuove porte in ascolto;
- arresti e riavvii dei servizi;
- disco pieno;
- picchi di errori 5xx applicativi o del server web;
- errori dei backup;
- errori di rinnovo dei certificati;
- avvisi antimalware o degli strumenti di sicurezza, se usati.

Conserva i log abbastanza a lungo per indagare sugli incidenti.

Soglie e avvisi sono approfonditi in [Monitoraggio VPS]({{< relref "vps-monitoring.md" >}}).

## Dopo una sospetta compromissione {#after-a-suspected-compromise}

Se sospetti una compromissione privilegiata/root, non considerare una «pulizia» improvvisata una prova immediata di sicurezza.

Una risposta più sicura è:

1. **contenere** il VPS o il percorso di rete coinvolto;
2. preservare log e prove rilevanti quando possibile;
3. identificare credenziali e segreti potenzialmente esposti;
4. ruotarli da un sistema pulito e attendibile;
5. individuare un punto di ripristino noto come valido per app e dati;
6. ricostruire il server da OS e configurazioni affidabili quando opportuno;
7. ripristinare dati verificati anziché eseguibili e configurazioni compromessi alla cieca;
8. verificare la causa dell’accesso iniziale prima di ripristinare il traffico di produzione.

Le indicazioni CISA sulla risposta agli incidenti sottolineano isolamento, analisi di prove e log e recupero da backup verificati.

Per un sistema critico per l’attività, coinvolgi un professionista qualificato di sicurezza e risposta agli incidenti.

## Ripeti la checklist {#repeat-the-checklist}

La sicurezza non è un’attività svolta una sola volta all’installazione.

Ricontrolla con una frequenza definita:

- amministratori e chiavi SSH;
- privilegi sudo;
- porte aperte e in ascolto;
- regole del firewall;
- pacchetti e versioni OS non supportati;
- aggiornamenti di sicurezza in attesa;
- versioni di pannello, CMS e plugin;
- successo dei backup e prove di ripristino;
- scadenza e rinnovo dei certificati;
- log e avvisi;
- account e servizi inutilizzati;
- segreti esposti;
- contatti per gli incidenti.

Ripeti la checklist anche dopo migrazioni importanti, cambi di pannello, nuovi servizi o modifiche architetturali.

## Checklist di sicurezza per la produzione {#production-security-checklist}

| Controllo | Condizione di superamento |
|---|---|
| Recupero | console o percorso di recupero del provider funzionante |
| Accesso amministrativo | amministratore nominativo non root con chiave testata |
| Regole SSH | root/password configurati intenzionalmente dopo verifica dell’accesso alternativo |
| Servizi | porte in ascolto inventariate e giustificate |
| Firewall | negazione predefinita ed esposizione minima; accessi amministrativi/web testati |
| Servizi interni | porte DB/cache/app non pubbliche senza esigenza esplicita |
| Aggiornamenti | responsabili OS e app definiti; procedura di riavvio nota |
| Privilegi minimi | app, DB e utenti hanno solo gli accessi necessari |
| Segreti | non pubblici, accessibili dal web o leggibili indiscriminatamente |
| Pannello/interfaccia admin | aggiornati; accessi, 2FA e restrizioni verificati |
| TLS | HTTPS valido e procedura di rinnovo |
| Forza bruta | controlli usati come difesa aggiuntiva dove utili |
| Backup | copia indipendente e prova di ripristino |
| Log | errori di autenticazione, amministrazione, servizi e backup osservabili |
| DDoS | ambito della protezione di rete/provider compreso |
| Incidenti | responsabile, contenimento e recupero pulito definiti |
| Verifica periodica | data o procedura della prossima revisione definita |

## Riferimenti tecnici {#technical-references}

- Ubuntu Server — OpenSSH
- Ubuntu Server — firewall/UFW
- Ubuntu Server — aggiornamenti automatici
- CISA — guida StopRansomware
- VDSina Standard VPS
- Domande e risposte VDSina — ambito della protezione DDoS

## Domande frequenti {#faq}

### Che cosa proteggere per primo su un VPS nuovo? {#what-should-i-secure-first-on-a-new-vps}

Preserva console e recupero, crea e testa un amministratore nominativo non root con chiave SSH, inventaria i servizi in ascolto e poi restringi SSH e firewall. Evita più modifiche che rischiano di bloccare l’accesso prima di verificarlo.

### Dovrei disabilitare l’accesso SSH con password? {#should-i-disable-ssh-password-login}

L’autenticazione amministrativa con chiave è più robusta per il normale uso VPS, ma verifica prima accesso con chiave e console di recupero. Non disabilitare l’unico percorso funzionante.

### Dovrei cambiare la porta SSH? {#should-i-change-the-ssh-port}

Può ridurre il rumore di scanner e log, ma non è un controllo principale. Contano di più autenticazione robusta, privilegi minimi, firewall e aggiornamenti.

### Serve Fail2ban? {#do-i-need-fail2ban}

Non sempre, ma può essere una difesa aggiuntiva utile contro abusi ripetuti degli accessi. Non sostituisce chiavi SSH, aggiornamenti o corretta esposizione dei servizi.

### Quali porte devono essere aperte sul VPS? {#which-ports-should-be-open-on-a-vps}

Solo quelle richieste dall’architettura. Un server web pubblico richiede normalmente HTTP/HTTPS e un accesso amministrativo controllato. Database e servizi applicativi interni dovrebbero restare privati.

### Un firewall protegge un’app vulnerabile? {#does-a-firewall-protect-a-vulnerable-application}

No. Limita l’esposizione di rete. Un’app web pubblica richiede comunque codice sicuro, dipendenze supportate, aggiornamenti e controlli applicativi.

### Bastano gli aggiornamenti automatici di sicurezza? {#are-automatic-security-updates-enough}

No. Aiutano per i pacchetti OS supportati, ma app e dipendenze di terzi possono richiedere aggiornamenti separati; i riavvii di servizi o sistema possono ancora richiedere gestione operativa.

### Basta HTTPS per proteggere un VPS? {#is-https-enough-to-secure-a-vps}

No. Protegge il trasporto. Non risolve SSH debole, database esposti, plugin vulnerabili, pacchetti obsoleti, segreti divulgati o backup mancanti.

### Basta la protezione DDoS VDSina per proteggere il sito? {#is-vdsina-ddos-protection-enough-to-secure-the-website}

No. VDSina pubblicizza protezione DDoS gratuita e le sue risposte pubbliche la descrivono come L3-L4 senza SLA. Servono comunque sicurezza di OS ospite, accessi, applicazioni e recupero.

### Che cosa fare se sospetto che il VPS sia compromesso? {#what-should-i-do-if-i-suspect-the-vps-was-compromised}

Contieni l’incidente, conserva prove e log, ruota le credenziali esposte da un sistema pulito e, se sospetti compromissione privilegiata, preferisci ricostruire da fonti affidabili e backup verificati. Per sistemi critici, coinvolgi un professionista della risposta agli incidenti.
