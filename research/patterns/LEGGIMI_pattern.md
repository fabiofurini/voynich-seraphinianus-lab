# Pattern osservati nel Voynich
17 ottobre 2026. Risultati esplorativi; nessuna attribuzione di suono o significato.

## Campione e convenzioni
Zandbergen-Landini ZL3b del 13 maggio 2025. Solo righe di paragrafi P0 con almeno due token, interamente leggibili: sono escluse intere righe con alternative, glifi speciali e letture incerte. Campione principale: 2.952 righe, 202 facciate/pannelli, 25.373 token. Si dividono gli spazi incerti indicati da virgola; un secondo test li unisce (2.951 righe, 23.560 token). Questi numeri non sono i conteggi dell'intero manoscritto dei precedenti rapporti.
I token sono convenzioni di trascrizione, non parole linguistiche già identificate. Tutti i pattern sotto sono interni alla stessa riga; nessun n-gramma attraversa un a capo. Le interruzioni dovute alle figure sono trattate come separatori. Le etichette EVA sono soltanto nomi dei segni.

## 1. Famiglie combinatorie
Le sei terminazioni aiin, ain, edy, eedy, ol, ar sono presenti dopo ciascuno degli inizi ok, qok, ot, qot, ch, sh: tutte le 36 combinazioni selezionate sono attestate.
Esempi qok: qokaiin 220; qokain 230; qokedy 209; qokeedy 244; qokol 75; qokar 117.
Esempi ch: chaiin 37; chain 14; chedy 383; cheedy 41; chol 287; char 54.
La matrice completa è nell'immagine e nel JSON. Non è una grammatica identificata: prefissi e finali potrebbero riflettere morfologia, codifica o produzione meccanica. Le famiglie sono state selezionate a fini descrittivi, non scoperte da una ricerca cieca.

## 2. Posizione nel paragrafo
438/490 token iniziali di paragrafo (89,39%) iniziano con uno dei segni EVA f/k/p/t. Negli altri inizi riga: 208/2.462 (8,45%). Queste etichette corrispondono ai cosiddetti gallows.
Controllo per pagina: fra le 178 pagine con entrambe le categorie nel campione, 169 mostrano una percentuale superiore a inizio paragrafo, 6 sono pari, 3 mostrano l'opposto. Questo limita la spiegazione basata soltanto sulla miscela fra pagine.
Le decorazioni delle iniziali e la selezione di righe leggibili possono influenzare la misura. Non possiamo stabilire se i segni siano marcatori strutturali separati oppure facciano parte delle parole.

## 3. Associazioni fra token
Confronto con l'attesa da permutazioni uniformi delle parole all'interno di ciascuna riga, preservando contenuto, lunghezza e appartenenza della riga:

| Coppia | Osservata | Attesa | Pagine con la coppia |
|---|---:|---:|---:|
| s aiin | 38 | 5,45 | 32 |
| or aiin | 37 | 6,49 | 29 |
| chol daiin | 25 | 11,25 | 24 |
| ol shedy | 21 | 7,15 | 16 |
| shedy qokedy | 20 | 8,04 | 14 |

Queste coppie sono state selezionate dopo aver contato le frequenze: i rapporti sono descrittivi, non test corretti per selezione multipla. I pattern s aiin/or aiin possono risentire della segmentazione. Unendo le virgole, s aiin resta a 18 contro 2,18 attese, or aiin a 17 contro 2,96, chol daiin a 22 contro 10,66.

## 4. Sequenze più lunghe
ol shedy qokedy ricorre 5 volte su 5 pagine nel campione principale e 3 volte su 3 pagine unendo le virgole.
ol shedy qokedy qokeedy ricorre due volte su due pagine, con entrambe le convenzioni.
Nel campione non si trovano sequenze identiche di 5 o 6 token ripetute entro una riga. Questo non esclude parafrasi, varianti o ripetizioni a cavallo di righe.

## 5. Dipendenza fra fine e inizio dei token
Informazione mutua fra ultimo carattere EVA di un token e primo del successivo: 0,2071 bit. Nelle 499 permutazioni entro riga: media 0,01626, intervallo osservato 0,01280–0,02078.
Unendo gli spazi incerti: 0,17276 bit contro media 0,01622; intervallo nullo 0,01290–0,01927. Nessuno dei due risultati si avvicina al riferimento di rimescolamento.
Il calcolo riguarda caratteri EVA ai bordi, non fonemi o glifi indipendenti già accertati. La dipendenza potrebbe derivare anche da segmentazione, legature o vincoli di codifica. Il controllo dimostra dipendenza nell'ordine trascritto rispetto al modello nullo scelto; non dimostra lingua o semantica.

## 6. Un pattern che NON supera il controllo globale
Ripetizioni immediate della stessa parola: 218, contro attesa esatta 210,86. Nelle 499 permutazioni: 174–254. Non c'è un eccesso globale netto in questo campione. Con virgole unite: 192 contro 171,34, riferimento 140–205. Questo risultato vieta di descrivere ogni ripetizione come eccezionale.

## Conclusione
Il testo trascritto presenta almeno tre famiglie di vincoli: costruzione dei token, posizione nel paragrafo e collegamento fra token successivi. Le cifre permettono di testare modelli della scrittura. Non abbiamo ancora una corrispondenza verificata con significati.
Questi fenomeni sono già oggetto di studi sul Voynich: non vengono presentati come scoperte nuove. Si tratta di conteggi riproducibili svolti qui.

## Riproduzione e fonti
python patterns.py
python patterns.py --merge-commas
Solo Python standard per i calcoli. I risultati sono results.json e results_merge.json. L'immagine usa forme tipografiche EVA autentiche del font di riferimento di G. Landini, non ritagli del manoscritto. Per rigenerarla: scaricare il PDF di riferimento in /tmp/eva_reference.pdf e usare chart.py con PyMuPDF, fontTools, Pillow e i font DejaVu di sistema.
Fonte trascrizione: https://arxiv.org/src/2608.17096v1/anc/data/voynich-units/ZL3b.txt
Fonte forme: https://www.voynich.nu/hist/gabriel/eva2_reference.pdf
