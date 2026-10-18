import re,json,random,math,collections,pathlib,time
import numpy as np
R=pathlib.Path(__file__).resolve().parent.parent

def rows():
 out={};v=[]
 for l in (R/'patterns/voynich_ZL3b.txt').read_text().splitlines():
  m=re.match(r'<(f[^.>]+)\.([^,>]+),([^>]*P0)>\s*(.*)',l)
  if not m:continue
  ws=[x for x in re.split(r'[.,\s]+',re.sub(r'<[^>]*>','',m[4].replace('<->','.'))) if x]
  if len(ws)>1 and all(re.fullmatch('[a-z]+',x) for x in ws):v.append((m[1],ws))
 out['Voynich']=v;s=[];page=None
 for l in (R/'seraph_ocr/CS_OCR_TRANSLITERATION.txt').read_text().splitlines():
  if l.startswith('###PAGE'):page=l.split()[-1]
  elif l.strip() and not l.startswith('#') and page:
   ws=l.split()
   if len(ws)>1 and all(re.fullmatch('[A-Za-z]+',x) for x in ws):s.append((page,ws))
 out['Seraphinianus_OCR']=s;return out

def groups(rows):
 d=collections.defaultdict(list)
 for x in rows:d[len(x)].append(x)
 return [np.array(z,dtype=int) for n,z in sorted(d.items())]

def pcfg_eval(data,p,em=False):
 root,rules,lex=p;cr=np.zeros(2);ct=np.zeros((2,2,2));ce=np.zeros_like(lex);ll=0;tokens=0
 for x in groups(data):
  b,n=x.shape;I=np.zeros((b,n,n+1,2));O=np.zeros_like(I)
  for i in range(n):I[:,i,i+1,:]=lex[:,x[:,i]].T
  for width in range(2,n+1):
   for i in range(n-width+1):
    j=i+width
    for k in range(i+1,j):I[:,i,j,:]+=np.einsum('auv,bu,bv->ba',rules,I[:,i,k,:],I[:,k,j,:])
  z=I[:,0,n,:]@root;ll+=np.log(z).sum()-b*(math.lgamma(2*n-1)-math.lgamma(n)-math.lgamma(n+1));tokens+=b*n
  if not em:continue
  O[:,0,n,:]=root[None,:]/z[:,None];cr+=(I[:,0,n,:]*O[:,0,n,:]).sum(0)
  for width in range(n,1,-1):
   for i in range(n-width+1):
    j=i+width
    for k in range(i+1,j):
     left=I[:,i,k,:];right=I[:,k,j,:];parent=O[:,i,j,:]
     ct+=np.einsum('ba,auv,bu,bv->auv',parent,rules,left,right)
     O[:,i,k,:]+=np.einsum('ba,auv,bv->bu',parent,rules,right)
     O[:,k,j,:]+=np.einsum('ba,auv,bu->bv',parent,rules,left)
  for i in range(n):
   post=I[:,i,i+1,:]*O[:,i,i+1,:]
   for a in range(2):np.add.at(ce[a],x[:,i],post[:,a])
 return ll,tokens,(cr,ct,ce)

def hmm_eval(data,p,em=False):
 root,trans,lex=p;cr=np.zeros(2);ct=np.zeros((2,2));ce=np.zeros_like(lex);ll=0;tokens=0
 for x in groups(data):
  b,n=x.shape;A=np.zeros((b,n,2));B=np.ones_like(A);E=lex[:,x].transpose(1,2,0);A[:,0,:]=root*E[:,0,:]
  for i in range(1,n):A[:,i,:]=(A[:,i-1,:]@trans)*E[:,i,:]
  z=A[:,-1,:].sum(1);ll+=np.log(z).sum();tokens+=b*n
  if not em:continue
  B[:,-1,:]/=z[:,None]
  for i in range(n-2,-1,-1):B[:,i,:]=(B[:,i+1,:]*E[:,i+1,:])@trans.T
  post=A*B;cr+=post[:,0,:].sum(0)
  for i in range(n-1):ct+=np.einsum('ba,ac,bc->ac',A[:,i,:],trans,E[:,i+1,:]*B[:,i+1,:])
  for i in range(n):
   for a in range(2):np.add.at(ce[a],x[:,i],post[:,i,a])
 return ll,tokens,(cr,ct,ce)

def norm(a,axes):return a/a.sum(axis=axes,keepdims=True)
def fit(kind,tr,va,te,V):
 fn=pcfg_eval if kind=='PCFG2' else hmm_eval;best=None;history=[]
 for seed in [13,29]:
  rng=np.random.default_rng(seed);p=(norm(rng.random(2),0),norm(rng.random((2,2,2) if kind=='PCFG2' else (2,2)),(1,2) if kind=='PCFG2' else 1),norm(rng.random((2,V)),1))
  for epoch in range(25):
   _,_,counts=fn(tr,p,True);p=(norm(counts[0]+.1,0),norm(counts[1]+.1,(1,2) if kind=='PCFG2' else 1),norm(counts[2]+.1,1));vl,nt,_=fn(va,p);loss=-vl/nt/math.log(2)
   if best is None or loss<best[0]:best=(loss,p,seed,epoch+1)
  history.append({'seed':seed,'last_validation_bits':loss})
 vl,p,seed,ep=best;ll,nt,_=fn(te,p);return {'validation_bits_per_token':vl,'test_bits_per_token':-ll/nt/math.log(2),'seed':seed,'epoch':ep,'params':[x.tolist() for x in p]}

def experiment(name,rr):
 rng=random.Random(1309);pages=sorted({p for p,_ in rr});rng.shuffle(pages);n=len(pages);train=set(pages[:int(.6*n)]);valid=set(pages[int(.6*n):int(.8*n)]);test=set(pages[int(.8*n):]);sets=[[ws for p,ws in rr if p in ss and 4<=len(ws)<=14] for ss in [train,valid,test]]
 freq=collections.Counter(w[-2:] for ws in sets[0] for w in ws);vocab=[s for s,c in freq.most_common(5)];encode={s:i for i,s in enumerate(vocab)};sets=[[[encode.get(w[-2:],5) for w in ws] for ws in subset] for subset in sets]
 # Fixed train subsampling is after page split, no test data used for vocabulary or fit
 rng.shuffle(sets[0]);sets[0]=sets[0][:1200]
 out={'name':name,'encoding':'train-only five common 2-character suffixes + OTHER; OCR coding units, not phonemes','suffixes':vocab,'split_pages':[len(s) for s in [train,valid,test]],'rows':[len(s) for s in sets],'tokens':[sum(map(len,s)) for s in sets]}
 for kind in ['HMM2','PCFG2']:out[kind]=fit(kind,*sets,6)
 # unigram / first order Markov with add0.1, learn train only
 for order in [0,1]:
  counts=collections.defaultdict(lambda:np.ones(6)*.1)
  for ws in sets[0]:
   for i,x in enumerate(ws):counts[ws[i-1] if order and i else -1][x]+=1
  ll=0;nt=0
  for ws in sets[2]:
   for i,x in enumerate(ws):
    c=counts[ws[i-1] if order and i else -1];ll+=math.log2(c[x]/c.sum());nt+=1
  out['ngram'+str(order)]={'test_bits_per_token':-ll/nt}
 print(json.dumps(out),flush=True);return out
if __name__=='__main__':
 start=time.time();out=[experiment(n,r) for n,r in rows().items()];(R/'grammar_comparison/hierarchy_probe_results.json').write_text(json.dumps({'results':out,'seconds':time.time()-start,'limitations':['Rows are not known sentences.','Tokenization into suffix classes is arbitrary and loses information.','Two-state uniform-tree PCFG and HMM are very restricted hypotheses, not tests of Moro or all hierarchical grammars.','No independently annotated syntax or meaning.','No positive synthetic control yet; absence of PCFG advantage is not evidence against hierarchy.']},indent=2))
