# Voynich e Seraphinianus: controlli statistici consolidati

18 ottobre 2026. Studio esplorativo riproducibile; nessuna traduzione e nessuna prova di intraducibilità.

> **Esiti finali:** (1) la debole utilità di contesti aggiuntivi nel Voynich sopravvive a pareggiamento e backoff, ma non è esattamente nulla con accorpamenti EVA; (2) auditOCR con388parole localizzabili: disaccordi e segmentazione impediscono un CER indipendente; (3) affissi3–4unità: dati Voynich troppo scarsi per inferenze affidabili disgiunte; (4) modello gerarchico rafforzato, calibrato su controllo sintetico, non migliora il Voynich rispetto a HMM nella rappresentazione esaminata; Seraph inconcludente. Nessuna prova di intraducibilità o di equivalenza fra codici.





## 1. Confronto pareggiato e contesti rari

Tre separazioni per pagine (seed19201–19203), 60% apprendimento,20% validazione,20% verifica. Entro ogni split stesso numero di parole per ogni lunghezza4–10 in tutti i cinque corpora. 1104–1139 parole di apprendimento e 270–301 di verifica a seconda dello split; 874–1070 caratteri interni verificati. Le pseudo-pagine dei controlli sono blocchi di150 parole.

Modelli interpolati di ordine0–5: ogni contesto ripiega su quello più corto; forza del backoff scelta in validazione fra0.1,1,10,100,1000. Valutazione sulle sole lettere reali dalla quarta posizione della parola, identiche per tutti gli ordini; esclusi inizi/fine parola. Alfabeto derivato dal solo train con classe ignota. Il pareggiamento usa disponibilità delle lunghezze nei corpora, non frequenze dei caratteri da predire.



|Corpus|Guadagno ordine2→3, min–max bit|Media ordine2|Media ordine3|

|---|---:|---:|---:|

|Voynich|0.0003–0.0014|1.9998|1.9988|

|Seraphinianus_OCR|0.0878–0.1052|2.0392|1.9420|

|Voynich_connected_EVA|0.0034–0.0146|2.0143|2.0071|

|latin|0.3189–0.3844|2.8926|2.5413|

|italian|0.2955–0.3425|2.8722|2.5530|



Il guadagno del Voynich grezzo è molto piccolo e tutti e tre gli intervalli bootstrap per pagina includono zero. Accorpando i sei gruppi EVA connessi il guadagno diventa piccolo ma positivo, con2/3 intervalli che escludono zero: dire che il testo non contiene nessuna informazione ulteriore sarebbe sbagliato. Seraphinianus e testi di controllo mostrano guadagni maggiori. Gli intervalli sono condizionati ai campioni; non danno probabilità che il libro sia asemico. Sono confronti multipli esplorativi e gli split riutilizzano pagine. Differenze di scrittura e traslitterazione restano.



## 2. Audit OCR Seraphinianus

Script e risultati ocr_audit*. Il campione documentato comprende442 etichette originali (senza augmentation);411 posizioni localizzabili;388 singole parole confrontabili su199 pagine. Accordo esatto alla posizione284/388=73.20%; entro±2 posizioni335/388=86.34%. Disaccordi includono spostamenti di segmentazione. Questi numeri NON sono un tasso CER o WER validato.

Sono etichette del dataset di addestramento, non una verifica indipendente. Sono state visualizzate12 immagini originali: ricorrenze grafiche visibili, ma convenzione segno→traslitterazione non certificata autonomamente. Esempi di differenza nella quantità di tratti ripetuti: label Xeeei contro OCR Xeei; label rrgiiiiiiiiLb contro OCR rrgiiiiiiiLb. Sono proprio discrepanze che possono alterare le statistiche dei contesti. Il limite OCR è documentato, non risolto.



## 3. Affissi lunghi e segmenti disgiunti

Script long_affix_prediction.py con parametro3 o4; prefisso, contesto locale presuffisso e suffisso non si sovrappongono: lunghezza minima3A. Prevede solo il suffisso, non una parola completa. Smoothing su un vocabolario di suffissi osservati nel corpus (informazione transduttiva sui tipi, non frequenze test). Nei test precedenti affix_prediction.py i segmenti erano di2 unità e la lunghezza minima5: il prefisso e il contesto locale possono quindi sovrapporsi in parte nelle parole più corte.

Nel Voynich restano33–53 occorrenze di verifica per split con segmenti3, e UNA per split con segmenti4. Il controllo sintetico è rilevato, ma nei dati reali non c’è potenza sufficiente per una conclusione sui segmenti lunghi. Nessun valore nullo va interpretato come assenza di grammatica. I file long_affix_3/4_results conservano la prima analisi meno restrittiva, quelli long_affix_disjoint_3/4_results la verifica disgiunta.



## 4. Organizzazione oltre la parola: confronto multiscala

Multiscale.py: primi7500 token di ciascun corpus, blocchi100/300/1000/3000, MI(parola,blocco),99 permutazioni globali e99 entro pagina. Tutti e quattro mostrano un eccesso rispetto al rimescolamento globale, incluso il Seraphinianus. A scala1000: Voynich0.1256bit di eccesso, Seraphinianus0.0820, latino0.1614, italiano0.0963. Questi valori non sono un test di equivalenza.

Rimescolare entro pagina lascia quasi invariato questo indicatore a scale ampie. Questo è in parte matematico: la statistica usa conteggi di parole nei blocchi, non ordine sintattico, e se una pagina resta nello stesso blocco i conteggi non cambiano. Lo stesso accade nei controlli linguistici. Non è una confutazione della semantica né una replica completa di Montemurro–Zanette. Dimostra che la misura da sola non identifica sintassi o significato.

Studio di riferimento: Montemurro e Zanette2013, https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0066344 . Il lavoro analizza sezioni riordinate e strutture di cooccorrenza non replicate integralmente qui.



## 5. Moro: cosa richiederebbe una verifica

Musso, Moro et al.2003, Broca’s area and the language instinct, https://www.nature.com/articles/nn1077 ; Moro, Impossible Languages, https://academic.oup.com/mit-press-scholarship-online/book/18683 . I risultati su apprendimento di regole e dipendenza dalla struttura non costituiscono una funzione nota che proietta vincoli grammaticali sulle sequenze di una scrittura ignota. Un confronto PCFG/sequenziale è una prova esplorativa su modelli statistici, non verifica dei vincoli di Moro. Anche una morfologia regolare può essere prodotta da un automa; l’esistenza di un albero di concatenazione non dimostra sintassi gerarchica linguistica.



## Conclusione provvisoria

Il risultato più robusto è la debole utilità del contesto aggiuntivo entro parola nel Voynich rispetto ai testi di confronto, anche pareggiando lunghezze e quantità e usando backoff. Sopravvive però un piccolo guadagno con segmentazione EVA connessa. Le somiglianze col Seraphinianus sono specifiche, non equivalenza generale. Non si può dedurre intraducibilità senza ipotesi restrittive sulla codifica.

## 6. Confronto gerarchico iniziale e controllo positivo
È stato eseguito un confronto oltre la singola parola usando righe di4–14 parole, trasformate in5 classi di suffissi frequenti nel solo train più OTHER. PCFG2 e HMM2 hanno due stati latenti; unigrammi e bigrammi sono controlli sequenziali. Split60/20/20 per pagine, cap1200righe train,2inizializzazioni,25EMepochs, scelta sul validation.
Test bit/token: Voynich bigramma2.29638,HMM2.29752,PCFG2.31111; Seraphinianus bigramma2.08774,HMM2.08965,PCFG2.11333.
Il controllo positivo è fallito: su2000righe generate da una grammatica della stessa famiglia, PCFG appresa0.991189, HMM0.899125, grammatica vera nota0.875845. Quindi un segnale gerarchico esiste, ma il primo fitting non lo recupera. L’assenza di vantaggio sui testi reali NON è evidenza di assenza di gerarchia. Probabilità condizionate alla lunghezza e normalizzazione PCFG verificate enumerando tutte le stringhe binarie di lunghezza1–5.
Righe non equivalgono a frasi; classi di suffissi possono eliminare dipendenze; due stati sono una semplificazione estrema. Non è una ricostruzione della grammatica umana né una verifica di Moro.

## Perché questi dati non possono provare intraducibilità assoluta
Senza limitare la famiglia di codifiche, qualsiasi stringa finita C può essere resa compatibile con qualsiasi testo P di uguale lunghezza definendo una chiave K=C−P modulo la dimensione dell’alfabeto. È un argomento di identificabilità, non l’ipotesi storica che sia stato usato un one-time pad. Bisogna quindi specificare quali codifiche, lingue e segmentazioni si stanno escludendo; un fallimento di apprendimento non esclude tutte le grammatiche.


### Correzione dopo calibrazione rafforzata
Il primo fallimento del controllo positivo non è definitivo: con inizializzazioni Dirichlet(0.3), più ripartenze e fino100iterazioni, il controllo sintetico è riuscito. Quattro ripartenze completate entro60s; PCFG migliore0.875506bit/token, rispetto a0.899125HMM e0.875845grammatica vera. Il fitting iniziale collassava in un ottimo locale; il modello probabilistico può recuperare il segnale nel controllo specifico. Questo dimostra l’importanza della calibrazione, non garantisce potenza per grammatiche umane o per la rappresentazione ignota dei codici.


## Riproduzione e provenienza

[Home](../README.md) · [Esperimenti](../EXPERIMENTS.md) · [Riproduzione](../REPRODUCIBILITY.md) · [Fonti](../DATA_SOURCES.json) · [Diritti](../RIGHTS.md)

Il repository pubblico contiene codice, aggregati e documenti originali in Markdown. Le trascrizioni di terzi, le etichette OCR complete e le immagini del libro moderno non sono redistribuite: il downloader le recupera localmente con hash verificato. I risultati pubblici dell’audit sono limitati agli aggregati. La versione privata precedente del pacchetto comprendeva materiali di analisi non inclusi nella pubblicazione.

### Esito finale del confronto gerarchico rafforzato
Quattro inizializzazioni[13,29,43,61],100iterazioni ciascuna, inizializzazione Dirichlet(0.3), smoothing0.1 e selezione del modello sulla validazione, sia PCFG2 sia HMM2. Corpus/rappresentazione e split invariati.
|Corpus|PCFG2 testbit/token|HMM2 testbit/token|Differenza PCFG−HMM|Bootstrap95% per pagina|
|---|---:|---:|---:|---|
|Voynich|2.312988|2.293697|+0.019291|[+0.006544,+0.034324]|
|SeraphinianusOCR|2.075637|2.079046|−0.003408|[−0.008042,+0.000793]|
2000bootstrap accoppiati su40pagine Voynich e57Seraph; intervalli esplorativi condizionati ai modelli selezionati e a questo split. Il modello gerarchico è peggiore nel Voynich; nel Seraph il vantaggio nominale è molto piccolo e l’intervallo comprende zero. Il controllo positivo rafforzato riesce. Questo risultato esclude solo l’utilità predittiva aggiuntiva di QUESTA PCFG a due stati su QUESTA rappresentazione in classi di suffissi. Non esclude grammatiche più ricche, rappresentazioni diverse, struttura interna alle parole o sintassi non conservata dai confini delle righe. Niente interpretazione semantica o test diretto di Moro.
