# Voynich — controlli e risultati, seconda analisi
17 ottobre 2026. Tutte le forme citate sono traslitterazioni EVA, non letture fonetiche. Nessuna traduzione ottenuta, nessuna rivendicazione di novità.

## Risultato principale
I controlli NON identificano univocamente m con r. Il testo distingue alcune sezioni illustrate anche tenendo fisse mano e varietà Currier, ma il solo segno finale delle parole fornisce quasi la stessa capacità discriminante. Questa analisi documenta struttura e variazione; non dimostra contenuto semantico.

## Fonti
1. Stolfi/Landini 1.6e6, strato H di Takeshi Takahashi:
https://www.ic.unicamp.br/~stolfi/EXPORT/00-EXPORT/98-12-28-interln16e6/
2. Zandbergen–Landini ZL3b, versione dichiarata nel file 13 maggio 2025, copia pubblicata come materiale di ricerca:
https://arxiv.org/src/2608.17096v1/anc/data/voynich-units/ZL3b.txt
Le due trascrizioni hanno una storia di fonti condivise: non sono campioni statisticamente indipendenti.
3. Emma May Smith, “What is [m]?”, 27 dicembre 2016:
https://agnosticvoynich.wordpress.com/2016/12/27/what-is-m/
Questa fonte primaria di ricerca esplorativa discute già m→r e i suoi limiti. Il commento di René Zandbergen segnala otalar/otalam in due etichette vicine; qui ne abbiamo verificato la presenza nella trascrizione ZL, non nelle immagini.
4. Bowern e Lindemann, The Linguistics of the Voynich Manuscript (2021):
https://doi.org/10.1146/annurev-linguistics-011619-030613

## A. Controlli sulla sostituzione della m finale
119 pagine di sviluppo e 83 di verifica per H; divisione deterministica SHA256 del codice pagina modulo 3. La stessa regola si applica a ZL. In ogni test il vocabolario contiene solo parole non finali delle righe di sviluppo. Per i dettagli e i conteggi di ciascun campione vedere controls.json.
Candidati aggiuntivi iin/ain/ry/rl sono stati introdotti DOPO aver consultato la letteratura: sono confronti esplorativi, non una nuova verifica cieca del candidato selezionato in precedenza.

| Corpus e trattamento spazi incerti | n | m invariata | m→r | m→l | m→iin |
|---|---:|---:|---:|---:|---:|
| H, campione originale pulito | 277 | 118 | 207 | 192 | 189 |
| ZL, virgole separate | 198 | 89 | 133 | 123 | 132 |
| ZL, virgole unite | 198 | 69 | 110 | 103 | 117 |

La sostituzione migliore cambia con il trattamento degli spazi incerti: r non è identificata univocamente. I campioni H e ZL sono diversi anche per le esclusioni di righe ambigue: il confronto tra percentuali non misura una pura differenza tra trascrittori.
In ZL con virgole separate, m→r dà 67,2%, mentre l→r produce una forma nota in 124/160 casi (77,5%). Questo non dimostra che l→r sia una sostituzione valida: mostra che la copertura di vocabolario da sola favorisce trasformazioni non necessariamente corrette.

### Forme mai viste
Delle 150 forme distinte con m finale nel test H, 91 non erano presenti in alcuna posizione nello sviluppo: m→r trova un corrispondente per 32/91, m→l per 27/91, m→iin per 22/91.
In ZL separato: 64 forme nuove, corrispondenti per r 20/64, l 12/64, iin 15/64. Le percentuali per occorrenza erano favorite dalle parole frequenti; sulle forme nuove la copertura è molto più bassa.
Il bootstrap per pagina, 4000 campioni e seed fisso, dà per il vantaggio r-l circa +1,2/+9,5 punti in H e -0,6/+11,0 in ZL separato. È un intervallo descrittivo: pagine dello stesso fascicolo non sono necessariamente indipendenti.

### Contesto precedente
Cercando anche la medesima parola precedente all'interno delle righe di sviluppo, sulle 198 occorrenze ZL di verifica si ottengono 20 corrispondenze per r, 22 per l, 24 per iin, 17 per in, 5 con m invariata. Le coppie sono sparse e influenzate dalla frequenza; questo test non sostiene una preferenza univoca per r.

### Controesempio alla fusione indiscriminata
ZL contiene:
<f70v2.24,&Lz> <!00:00>otalar
<f70v2.25,&Lz> <!01:30>otalam
Si tratta di etichette, non di parole al margine di righe in prosa. La compresenza richiede una spiegazione prima di normalizzare sempre m in r. Non è una confutazione logica di ogni possibile allografia, perché potrebbero esserci altre condizioni, ma vieta di trattare l'equivalenza come acquisita.

## B. Il testo distingue sezioni illustrate a mano fissa?
Selezione ZL: mano 2, varietà Currier B; sole categorie di illustrazione H (botanica) e B (bagni/figure umane). I nomi delle categorie descrivono le immagini, non una traduzione del testo. Rimangono 39 pagine: 20 H e 19 B.
Per ogni pagina: 30 token campionati senza rimpiazzo da posizioni interne alle righe; escluse prima e ultima parola e intere righe con letture incerte. Questo limita effetti di lunghezza e di margine.
Classificatore multinomiale Naive Bayes, smoothing +1 e prior delle classi uniforme. Validazione lasciando fuori un gruppo Q+B (fascicolo + numero del bifoglio) alla volta; 10 gruppi totali. Il vocabolario di ogni fold è costruito esclusivamente sui gruppi di sviluppo. I gruppi di verifica non entrano nella stima né del vocabolario né dei parametri.

| Informazione usata | Pagine corrette | Accuratezza bilanciata |
|---|---:|---:|
| Parole intere | 34/39 | 87,4% |
| Solo ultimo carattere EVA di ogni parola | 34/39 | 87,5% |
| Solo ultimi due caratteri EVA | 33/39 | 85,0% |

Seed principale 20261017. Su 30 campionamenti diversi, le mediane di accuratezza bilanciata sono 92,5% per parole e 84,8% per ultimo carattere; intervalli min-max 82,2–97,5% e 74,5–95,0%. Questi intervalli descrivono sensibilità al campionamento delle parole, NON incertezza sulla generalizzazione ad altri manoscritti.
Nel test principale le parole intere non migliorano il numero di pagine riconosciute rispetto al solo carattere finale. Nei ricampionamenti c'è una differenza mediana, ma non abbiamo testato formalmente un vantaggio semantico.
Riferimento esplorativo: 1999 permutazioni delle etichette per gruppo di bifogli; p empirico +1 pari a 0,012. Questo riferimento NON controlla la posizione o il fascicolo e non è prova di semantica.
Limite determinante: le pagine B selezionate appartengono al fascicolo M, le H ad altri fascicoli. Tema illustrato e posizione fisica restano confusi. Variazioni cronologiche, ortografiche o di codifica potrebbero spiegare il risultato. Il controllo per mano e Currier è utile ma insufficiente.

## C. Cosa abbiamo stabilito e cosa no
Stabilito nel campione: struttura posizionale; assenza di una sostituzione m→r univocamente sostenuta da questi test; variazione testuale che predice categorie illustrate anche a mano e Currier fisse.
Non stabilito: che gli spazi separino parole linguistiche; il valore di un glifo; una lingua; una traduzione; il contenuto semantico; una scoperta nuova rispetto alla letteratura.
È metodologicamente corretto abbandonare per ora la normalizzazione globale m=r. Il prossimo esperimento utile deve separare tema da fascicolo e ortografia e verificare direttamente le immagini; non basta migliorare una copertura di dizionario.

## Riproduzione
Python 3; per il test sezioni serve numpy. I primi due test usano solo la libreria standard.
python voynich_test.py voynich_source.evt > risultati_base.json
python voynich_controls.py voynich_source.evt voynich_ZL3b.txt > controlli.json
python voynich_sections.py voynich_ZL3b.txt > sezioni.json
I file JSON inclusi contengono conteggi, predizioni pagina per pagina e parametri. Questa versione finale usa un vocabolario strettamente di sviluppo: una prima esecuzione esplorativa aveva prodotto 35/39, prima di escludere dal vocabolario anche i tipi presenti esclusivamente nella verifica. Il risultato da citare è 34/39.
