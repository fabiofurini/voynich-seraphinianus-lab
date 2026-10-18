import hierarchy_probe as h
import numpy as np,time,math,json

def fit(kind,tr,va,te,V):
 fn=h.pcfg_eval if kind=='PCFG2' else h.hmm_eval;best=None;completed=[];start=time.time()
 # Same four starts that bounded calibration reached, now fixed100 epochs for all.
 for seed in [13,29,43,61]:
  rg=np.random.default_rng(seed);p=(rg.dirichlet([.3]*2),rg.dirichlet([.3]*(4 if kind=='PCFG2' else 2),size=2).reshape((2,2,2) if kind=='PCFG2' else (2,2)),rg.dirichlet([.3]*V,size=2))
  for epoch in range(100):
   _,_,counts=fn(tr,p,True);p=(h.norm(counts[0]+.1,0),h.norm(counts[1]+.1,(1,2) if kind=='PCFG2' else 1),h.norm(counts[2]+.1,1));ll,nt,_=fn(va,p);loss=-ll/nt/math.log(2)
   if best is None or loss<best[0]:best=(loss,p,seed,epoch+1)
  completed.append({'seed':seed,'epochs':100,'last_validation_bits':loss});print(kind,completed[-1],flush=True)
 vl,p,seed,epoch=best;ll,nt,_=fn(te,p)
 return {'validation_bits_per_token':vl,'test_bits_per_token':-ll/nt/math.log(2),'seed':seed,'epoch':epoch,'completed':completed,'seconds':time.time()-start,'params':[x.tolist() for x in p]}
h.fit=fit
out=[]
for n,r in h.rows().items():
 out.append(h.experiment(n,r));(h.R/'grammar_comparison/hierarchy_stronger_results.json').write_text(json.dumps({'protocol':'4 Dirichlet(.3)random starts x100 EM, validation-selected, matching synthetic calibration seeds; no test fitting','results':out},indent=2))
