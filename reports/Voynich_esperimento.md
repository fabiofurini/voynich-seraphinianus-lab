# Voynich: esperimento riproducibile sulla m finale
17 ottobre 2026 — analisi esplorativa, nessuna traduzione e nessuna rivendicazione di novità.

## Domanda
Il segno rappresentato da m in EVA potrebbe essere una variante posizionale di un altro segno?

## Fonte e metodo
Archivio Stolfi/Landini 1.6e6, trascrittore Takeshi Takahashi (H):
https://www.ic.unicamp.br/~stolfi/EXPORT/00-EXPORT/98-12-28-interln16e6/
Il file incluso è una copia locale UTF-8 del testo decompresso originariamente Latin-1. Ringraziamenti a trascrittori e curatore; condizioni nella pagina fonte.
Solo righe P con almeno due parole e senza token incerti; rimozione commenti e filler di allineamento. Le virgole sono trattate come separatori: scelta da verificare con altre segmentazioni. 3840 righe pulite, 202 pagine.
Divisione deterministica per hash del codice pagina: 119 pagine di sviluppo, 83 di verifica. Le pagine di verifica non entrano nel vocabolario.
Il vocabolario di riferimento comprende tutte le parole NON finali nelle righe di sviluppo (incluse le iniziali).
Sostituiamo solo m finale delle parole che chiudono riga. Candidati: caratteri osservati, cancellazione, ch/sh/aiin/in/dy. Scegliamo sullo sviluppo la sostituzione che produce più occorrenze presenti nel vocabolario di riferimento. L'obiettivo è copertura lessicale, non probabilità linguistica né significato.

## Risultato
Il candidato migliore sullo sviluppo è r: 280/363 (77,1%).
Sulle 83 pagine tenute da parte: r produce 207/277 corrispondenze (74,7%); mantenere m ne produce 118/277 (42,6%).
Alternative sulla verifica: l 69,3%; in 54,5%; cancellazione 31,8%.
Esempi di trasformazioni con forma corrispondente nel vocabolario: dam→dar; am→ar; qokam→qokar; otam→otar; okam→okar; chom→chor.
Questi sono segni EVA, non parole lette in una lingua e non valori fonetici.

## Interpretazione e limiti
Il risultato motiva un test dell'ipotesi di variante posizionale, ma NON dimostra m=r. r e l sono entrambe terminazioni produttive: la loro frequenza e la presenza di forme brevi possono spiegare parte del risultato. Il confronto con identità è descrittivo, non un test calibrato di significatività. Le forme viste in verifica possono essere già comparse nello sviluppo: il test separa pagine, non tipi di parola. La divisione non separa necessariamente scribi o bifogli. Nessuna verifica sulle immagini e nessuna replica su altra trascrizione. I numeri precedenti di 203 pagine includevano righe con parole incerte: qui il campione è più restrittivo.

## Prossimo test discriminante
Confrontare i contesti precedenti delle coppie Xam/Xar/Xal controllando sezione, mano, lunghezza della riga e frequenza; ripetere su tipi di parola mai visti nello sviluppo; verificare i glifi nelle immagini. Se il vantaggio scompare dopo i controlli, abbandonare la sostituzione globale.

## Riproduzione
Estrarre questo archivio e usare Python 3:
python voynich_test.py voynich_source.evt > risultati.json
L'hash della fonte è nei risultati. Nessuna dipendenza esterna.
