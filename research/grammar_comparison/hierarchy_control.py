import hierarchy_probe as h
import random,math,json,itertools,numpy as np
rng=random.Random(7712)
cat=lambda n:math.comb(2*n,n)//(n+1)
def sample(n,state):
 if n==1:return ['t'+str(state if rng.random()<.97 else 1-state)]
 ks=list(range(1,n));weights=[cat(k-1)*cat(n-k-1) for k in ks];k=rng.choices(ks,weights)[0]
 states=(state,1-state) if rng.random()<.95 else (1-state,state)
 return sample(k,states[0])+sample(n-k,states[1])
rows=[(str(p),sample(rng.randrange(4,15),0 if rng.random()<.9 else 1)) for p in range(100) for _ in range(20)]
out=h.experiment('Synthetic_same_PCFG_family',rows)
# Validate normalization by enumerating all binary strings n1..5 under a two-symbol PCFG
p=(np.array([.9,.1]),np.array([[[.01,.95],[.03,.01]],[[.01,.03],[.95,.01]]]),np.array([[.97,.03],[.03,.97]]))
checks={}
for n in range(1,6):
 probs=[]
 for x in itertools.product(range(2),repeat=n):
  ll,_,_=h.pcfg_eval([list(x)],p);probs.append(math.exp(ll))
 checks[n]=sum(probs)
(h.R/'grammar_comparison/hierarchy_control_results.json').write_text(json.dumps({'result':out,'PCFG_conditional_normalization_enumeration':checks,'generation':'2 states, uniform Catalan binary trees conditional length4..14, asymmetric rules0->01=.95 and1->10=.95; lexical .97 matchedstate; root0 .9;100pages20rowseach'},indent=2))
print('Normalization',checks)
