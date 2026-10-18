import hierarchy_probe as h,json,random,collections,math,numpy as np
obj=json.loads((h.R/'grammar_comparison/hierarchy_stronger_results.json').read_text());out=[]
for fit in obj['results']:
 rr=h.rows()[fit['name']];rng=random.Random(1309);pages=sorted({p for p,_ in rr});rng.shuffle(pages);n=len(pages);train=set(pages[:int(.6*n)]);test=set(pages[int(.8*n):]);freq=collections.Counter(w[-2:] for p,ws in rr if p in train and 4<=len(ws)<=14 for w in ws);enc={s:i for i,(s,c) in enumerate(freq.most_common(5))};groups=collections.defaultdict(list)
 for p,ws in rr:
  if p in test and 4<=len(ws)<=14:groups[p].append([enc.get(w[-2:],5) for w in ws])
 ps=[np.array(a) for a in fit['PCFG2']['params']];hs=[np.array(a) for a in fit['HMM2']['params']];scores=[]
 for page,seq in groups.items():
  lp,nt,_=h.pcfg_eval(seq,ps);lh,_,_=h.hmm_eval(seq,hs);scores.append(((lh-lp)/math.log(2),nt))
 scores=np.array(scores);rg=np.random.default_rng(601);boot=[]
 for _ in range(2000):
  z=scores[rg.integers(0,len(scores),len(scores))];boot.append(z[:,0].sum()/z[:,1].sum())
 out.append({'name':fit['name'],'PCFG_minus_HMM_bits_per_token':scores[:,0].sum()/scores[:,1].sum(),'test_page_cluster_bootstrap95_percentile':np.quantile(boot,[.025,.975]).tolist(),'test_pages_with_eligible_rows':len(scores),'note':'Conditional on fitted models, single split; no adjustment for model search.'})
(h.R/'grammar_comparison/hierarchy_bootstrap_results.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
