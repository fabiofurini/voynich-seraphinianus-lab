# Voynich: inventario grafico candidato, non alfabeto fonetico
17 ottobre 2026

## Esito
Inventario operativo di 23 unità grafiche, costruito utilizzando le convenzioni EVA e le distinzioni documentate dai trascrittori. La scelta dei sei composti NON è una scoperta automatica: deriva dalla documentazione del sistema di scrittura. La novità di questo esercizio è soltanto il conteggio riproducibile e il confronto fra i due corpora, non una rivendicazione scientifica di novità.

17 forme indicate con una sola etichetta EVA:
a d e f g i k l m n o p q r s t y

6 forme con etichette EVA composte:
ch sh ckh cth cph cfh

Non si tratta di un ordinamento alfabetico recuperato, e nessuna etichetta assegna un suono al segno.

## Campione
Solo testo di paragrafi: loci P0 in ZL, loci P in H. Si contano token interamente leggibili, anche se altri token della stessa riga sono incerti. Non è quindi il campione di righe completamente pulite dei precedenti esperimenti. Le sequenze ambigue, gruppi speciali ZL e annotazioni non interpretate sono escluse. Esclusi etichette, sequenze marginali e testi circolari.
Tokenizzazione grafica massimale: ckh/cth/cph/cfh/ch/sh prima dei caratteri singoli. Le virgole sono separatori; si tratta di una convenzione, non di un risultato.

| Corpus | Token di testo leggibili | Unità grafiche contate | Copertura delle 23 unità |
|---|---:|---:|---:|
| ZL3b (2025) | 32.888 | 146.382 | 99,963% |
| Takahashi H, archivio Stolfi | 33.017 | 149.575 | 99,795% |

La copertura vale soltanto sul testo già trascritto e sui token accettati. Non include tutti i segni del manoscritto: non è una verifica paleografica esaustiva e non autorizza a ignorare le forme rare.

## Evidenze per non leggere ingenuamente le lettere EVA
In ZL P0, h compare 15.517 volte: soltanto 3 restano fuori dai sei composti. In H restano 165 casi su 15.958: le trascrizioni non segmentano tutti i casi nello stesso modo. Il fatto che un composto sia connesso non prova che sia una lettera semplice: può essere una legatura.
q è all'inizio del token 5.061/5.087 volte (99,49%) ed è seguito da o 4.987/5.087 volte (98,03%). Questo rende qo un candidato a unità o elemento prefissato; non permette di scegliere fra le due interpretazioni.
n segue i 5.439/5.550 volte (98,00%) e chiude il token 5.493/5.550 volte (98,97%). I gruppi in/iin/iiin potrebbero dover essere trattati come unità distinte o come un sistema composizionale di tratti.
Le sequenze massimali terminanti in n contate in ZL sono in 1.601, iin 3.688, iiin 149, iiiin 1. La variabilità del numero di tratti non viene eliminata dalla proposta.
m resta separata da r: gli esperimenti precedenti non giustificano la fusione globale.

## Conclusione operativa
Possiamo usare 23 unità come rappresentazione di lavoro con una copertura molto alta. Non abbiamo stabilito che siano 23 lettere linguistiche, e non abbiamo trovato una tabella di corrispondenza con latino, italiano o altre lingue. La segmentazione di in/iin e qo e il rapporto tra legatura e lettera restano irrisolti.
La ricostruzione di un inventario grafico e la decifrazione fonetica sono risultati distinti: solo il primo è stato affrontato qui. Attribuire valori A/B/C alle forme sarebbe arbitrario.

## Fonti e tavola dei glifi
Gabriel Landini, documentazione EVA (1998):
https://www.ic.unicamp.br/~stolfi/EXPORT/projects/voynich/work/programs/c/projects/voynich/alphabet-gabriel/eva.htm
La documentazione distingue convenzioni di connessione grafica da interpretazione fonetica.
Tavola di riferimento originale EVA:
https://www.voynich.nu/hist/gabriel/eva2_reference.pdf
René Zandbergen, analisi del sistema di scrittura:
https://www.voynich.nu/writing.html
Le fonti e gli hash dei due corpora sono nel pacchetto. Per la fonte ZL: versione 3b del 13 maggio 2025, come dichiarato nell'intestazione del file.

## Riproduzione
python voynich_inventory.py voynich_ZL3b.txt voynich_source.evt > inventory.json
Solo libreria standard Python 3. Il JSON contiene frequenze per ciascuna unità, segni residui e distribuzioni dei contesti di c/h/q/n.
