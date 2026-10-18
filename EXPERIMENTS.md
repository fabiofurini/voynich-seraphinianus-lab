# Registro degli esperimenti

[Home](README.md) · [Stato](STATUS.md) · [Ipotesi](HYPOTHESES.md) · [Metodo](REPRODUCIBILITY.md) · [Roadmap](ROADMAP.md)

|ID|Esperimento|Codice|Output|
|---|---|---|---|
|E01|Contesti locali, primo confronto|[run.py](research/grammar_comparison/run.py)|[risultati](research/grammar_comparison/results.json)|
|E02|Campioni pareggiati e backoff|[matched_backoff.py](research/grammar_comparison/matched_backoff.py)|[risultati](research/grammar_comparison/matched_backoff_results.json)|
|E03|Dipendenze ai confini|[robust_boundary.py](research/grammar_comparison/robust_boundary.py)|[risultati](research/grammar_comparison/robust_boundary_results.json)|
|E04|Prefissi e suffissi|[affix_prediction.py](research/grammar_comparison/affix_prediction.py)|[risultati](research/grammar_comparison/affix_prediction_results.json)|
|E05|Affissi lunghi disgiunti|[long_affix_prediction.py](research/grammar_comparison/long_affix_prediction.py)|[tre unita](research/grammar_comparison/long_affix_disjoint_3_results.json) · [quattro](research/grammar_comparison/long_affix_disjoint_4_results.json)|
|E06|Audit OCR|[ocr_audit.py](research/grammar_comparison/ocr_audit.py)|[sintesi](research/grammar_comparison/ocr_audit_results.json)|
|E07|Gerarchia, primo fitting|[hierarchy_probe.py](research/grammar_comparison/hierarchy_probe.py)|[risultati](research/grammar_comparison/hierarchy_probe_results.json)|
|E08|Controllo sintetico e calibrazione|[hierarchy_calibration.py](research/grammar_comparison/hierarchy_calibration.py)|[risultati](research/grammar_comparison/hierarchy_calibration_results.json)|
|E09|Gerarchia, fitting rafforzato|[hierarchy_stronger.py](research/grammar_comparison/hierarchy_stronger.py)|[risultati](research/grammar_comparison/hierarchy_stronger_results.json)|
|E10|Bootstrap per pagina|[hierarchy_bootstrap.py](research/grammar_comparison/hierarchy_bootstrap.py)|[risultati](research/grammar_comparison/hierarchy_bootstrap_results.json)|
|E11|Organizzazione multiscala|[multiscale.py](research/grammar_comparison/multiscale.py)|[risultati](research/grammar_comparison/multiscale_results.json)|
|E12|Sostituzione semplice|[metodo](research/Voynich_test_sostituzione/LEGGIMI_risultati.md)|[risultati](research/Voynich_test_sostituzione/results.json)|

Il risultato E07 non va usato come prova negativa: la prima calibrazione falliva. E08 risolve il problema con piu inizializzazioni; la valutazione finale e E09. E05 resta inconcludente per scarsita di dati.
