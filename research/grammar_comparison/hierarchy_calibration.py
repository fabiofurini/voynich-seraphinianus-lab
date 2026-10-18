import hierarchy_probe as h
import random,math,json,numpy as np,time,collections
rng=random.Random(7712);cat=lambda n:math.comb(2*n,n)//(n+1)
def sample(n,state):
 if n==1:return ['t'+str(state if rng.random()<.97 else 1-state)]
 ks=list(range(1,n));k=rng.choices(ks,[cat(k-1)*cat(n-k-1) for k in ks])[0];a,b=(state,1-state) if rng.random()<.95 else (1-state,state);return sample(k,a)+sample(n-k,b)
rr=[(str(p),sample(rng.randrange(4,15),0 if rng.random()<.9 else 1)) for p in range(100) for _ in range(20)]
rng=random.Random(1309);pages=sorted({p for p,_ in rr});rng.shuffle(pages);ss=[set(pages[:60]),set(pages[60:80]),set(pages[80:])];sets=[[ws for p,ws in rr if p in s] for s in ss];v=[s for s,c in collections.Counter(w[-2:] for ws in sets[0] for w in ws).most_common(5)];enc={s:i for i,s in enumerate(v)};sets=[[[enc.get(w[-2:],5) for w in ws] for ws in z] for z in sets];rng.shuffle(sets[0]);sets[0]=sets[0][:1200]
start=time.time();best=None;completed=[]
for seed in [13,29,43,61,79,97,113,131]:
 rg=np.random.default_rng(seed);p=(rg.dirichlet([.3]*2),rg.dirichlet([.3]*4,size=2).reshape(2,2,2),rg.dirichlet([.3]*6,size=2))
 for epoch in range(100):
  _,_,counts=h.pcfg_eval(sets[0],p,True);p=(h.norm(counts[0]+.1,0),h.norm(counts[1]+.1,(1,2)),h.norm(counts[2]+.1,1));ll,nt,_=h.pcfg_eval(sets[1],p);loss=-ll/nt/math.log(2)
  if best is None or loss<best[0]:best=(loss,p,seed,epoch+1)
  if time.time()-start>60:break
 completed.append({'seed':seed,'epochs':epoch+1,'last_validation_bits':loss});print(completed[-1],flush=True)
 if time.time()-start>60:break
vl,p,seed,epoch=best;ll,nt,_=h.pcfg_eval(sets[2],p);obj={'initialization':'8 seeds requested, Dirichlet(.3) random priors/rules/emissions; smoothing .1; 100 epochs per seed; timecap60s','completed':completed,'best_validation':vl,'test_bits_per_token':-ll/nt/math.log(2),'best_seed':seed,'best_epoch':epoch,'seconds':time.time()-start,'params':[a.tolist() for a in p]};(h.R/'grammar_comparison/hierarchy_calibration_results.json').write_text(json.dumps(obj,indent=2));print(json.dumps(obj),flush=True)
