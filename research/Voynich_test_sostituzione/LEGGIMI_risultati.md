# Voynich: prova di sostituzione con controlli positivi
17 ottobre 2026. Nessuna decifrazione ottenuta.

## Domanda verificata
Un campione botanico omogeneo potrebbe essere latino o italiano scritto mediante una sostituzione biunivoca fissa, mantenendo gli spazi della trascrizione?
La prova riguarda precisamente questa ipotesi, con la segmentazione grafica scelta. Non riguarda cifrari omofonici, codici sillabici, abbreviazioni, lingue differenti o segmentazioni alternative.

## Metodo
- Fonte Voynich: Zandbergen-Landini ZL3b, versione 13 maggio 2025.
- Solo paragrafi P0 delle pagine botaniche H, mano 1 e varietà Currier A, secondo i metadati ZL.
- Segmentazione grafica in 23 unità: ch/sh/ckh/cth/cph/cfh sono unità; i/n restano separati. Si accettano solo token integralmente leggibili.
- Pagine separate mediante hash SHA256 del nome pagina modulo 3; circa due terzi sviluppo, un terzo verifica. Niente ottimizzazione sulle pagine di verifica.
- 19.113 caratteri convenzionali (spazi compresi) per cercare la chiave e 18.820 per la verifica. La ricerca non utilizza tutto il manoscritto: la restrizione limita la miscela fra sezioni e mani.
- Modelli a quadrigrammi con smoothing 0,01: latino medico di Celso, De medicina libro I (40.052 caratteri per il modello), e italiano di Romolo Murri, Il partito radicale e il radicalismo italiano (95.555 caratteri per il modello). Il secondo è italiano moderno, non un corpus medievale.
- Normalizzazione minuscole e accenti; eliminazione della punteggiatura. Per il testo Gutenberg sono rimossi i delimitatori e il blocco finale della licenza prima del modello; il file originale incluso conserva la propria intestazione/licenza.
- Ricerca con simulated annealing: 8 avvii, 50.000 proposte di scambio per avvio; temperatura 60→0,06; seed 20261017.
- Il modello cerca una permutazione dell'alfabeto latino di 26 lettere. Le 23 unità Voynich occupano 23 posizioni; le restanti permettono scambi con lettere non assegnate.

## Calibrazione positiva
Per ciascuna lingua si prende un brano dalla porzione del testo esclusa dalla costruzione del modello e lo si cifra con una permutazione casuale nota, mantenendo gli spazi. Lo stesso algoritmo tenta di recuperarlo.

| Prova | Recupero delle lettere del controllo | Token riconosciuti nel lessico di confronto |
|---|---:|---:|
| Controllo latino | 100% | 933/1.360 = 68,60% |
| Controllo italiano | 100% | 1.770/2.387 = 74,15% |
| Voynich, chiave ottimizzata sul latino, pagine di verifica | Non misurabile: manca il testo vero | 35/3.153 = 1,11% |
| Voynich, chiave ottimizzata sull'italiano, pagine di verifica | Non misurabile: manca il testo vero | 221/3.153 = 7,01% |

Il lessico è l'insieme delle parole presenti nel testo usato per costruire il modello; non è un dizionario completo. Le percentuali sono calcolate su token di almeno tre lettere. Le corrispondenze occasionali non sono parole lette con significato dimostrato. L'output Voynich non fornisce una lettura coerente giustificabile; le stringhe nel JSON sono risultati meccanici, non traduzioni.

## Controllo indipendente dalla chiave: triplette
Nel campione di sviluppo Voynich, 39 token su 3.844 contengono tre unità identiche consecutive. Una sostituzione biunivoca conserva necessariamente questa proprietà. Nel testo latino di confronto non vi sono triplette (0/7.595 token); nell'italiano normalizzato ne compare una (www, 1/19.118). Questo segnala una differenza fra le unità grafiche scelte e le lettere dei testi confrontati. La segmentazione di iin o di altri tratti può contribuire: non è una dimostrazione che il manoscritto sia privo di lingua.

## Cosa conclude la prova
La ricerca funziona sui due controlli di sostituzione semplice, ma non produce una chiave convincente sul campione Voynich. Questo è un risultato negativo su una famiglia limitata di ipotesi, non una dimostrazione di impossibilità né una prova esaustiva su tutte le chiavi. La ricerca è euristica e i modelli sono limitati.
L'ipotesi di lettura non può quindi essere promossa a traduzione. Per proseguire servono unità di scrittura meglio identificate e/o un ancoraggio esterno che imponga vincoli indipendenti.

## Pista zodiacale precedente
okeodaly è confermata in trascrizioni storiche su f71v e f72r1, entrambi Toro, nell'anello esterno. La sequenza esatta compare due volte in ZL. I contesti immediati differiscono, non è una frase ripetuta. Le forme a distanza di una modifica da okeodaly (compresa la forma stessa) coprono 10 pagine con virgole separate e 9 con virgole unite: la somiglianza grafica non prova identità semantica. I due fogli appartengono allo stesso bifoglio, quindi non sono repliche indipendenti. Nessun valore fonetico è stato ricavato da questa pista.

## Fonte dati e documentazione
https://arxiv.org/src/2608.17096v1/anc/data/voynich-units/ZL3b.txt
https://arxiv.org/src/2608.17096v1/anc/data/voynich-units/latin/celsus.de_medicina.part.1.tess
https://arxiv.org/src/2608.17096v1/anc/data/voynich-units/italian/26166.txt
https://www.voynich.nu/q11/f071v_tr.txt
https://www.voynich.nu/q11/f072r1_tr.txt

## Riproduzione
Python 3 e g++ con C++17, nessuna libreria Python aggiuntiva.
Estrarre tutto il pacchetto e lanciare: python voynich_attack.py
Il programma compila il solver e salva i risultati in run/results.json. Riprende i risultati già completati: eliminare run/results.json per ripetere entrambe le lingue. I risultati originali sono nel results.json principale.
