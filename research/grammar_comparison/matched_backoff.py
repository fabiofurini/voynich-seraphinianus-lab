import pathlib,collections,random,math,json,re
P=pathlib.Path(__file__).parent
ns={'__file__':str(P/'stability.py')};exec((P/'stability.py').read_text().split('\nout={}')[0],ns)
rows=ns['rows'];rows={k:v for k,v in rows.items() if k in ['Voynich','Voynich_connected_EVA','Seraphinianus_OCR','latin','italian']}
# Each unicode character is one selected unit in merged EVA variant.
def buckets(rr,seed):
 rng=random.Random(seed);pages=sorted(set(p for p,ws in rr));rng.shuffle(pages);n=len(pages);te=set(pages[:n//5]);va=set(pages[n//5:2*(n//5)]);d={s:collections.defaultdict(list) for s in ['train','val','test']}
 for p,ws in rr:
  side='test' if p in te else 'val' if p in va else 'train'
  for w in ws:
   if 4<=len(w)<=10:d[side][len(w)].append((p,w))
 for side in d:
  for a in d[side].values():rng.shuffle(a)
 return d

def fit(data):
 alphabet=set(''.join(w for p,w in data))|{'$','?'};c=[collections.defaultdict(collections.Counter) for _ in range(6)]
 for p,w in data:
  for i,ch in enumerate(w+'$'):
   prev='^'*5+w[:i]
   for k in range(6):c[k][prev[-k:] if k else ''][ch]+=1
 totals=[{h:sum(cc.values()) for h,cc in ck.items()} for ck in c]
 return alphabet,c,totals

def losses(data,model,taus,maxorder):
 alphabet,c,tot=model;out=[];K=len(alphabet)
 for p,w in data:
  ww=''.join(ch if ch in alphabet else '?' for ch in w);vals=[0.]*(maxorder+1);N=0
  # Only real interior characters at position >=3; same events for every order.
  for i in range(3,len(ww)):
   ch=ww[i];hist='^'*5+ww[:i];cc=c[0][''];pr=(cc[ch]+.1)/(tot[0].get('',0)+.1*K)
   vals[0]-=math.log2(pr)
   for k in range(1,maxorder+1):
    h=hist[-k:];n=tot[k].get(h,0);pr=(c[k][h][ch]+taus[k-1]*pr)/(n+taus[k-1]);vals[k]-=math.log2(pr)
   N+=1
  out.append((p,vals,N))
 return out

def average(ll,k):return sum(x[1][k] for x in ll)/sum(x[2] for x in ll)
out=[]
for seed in [19201,19202,19203]:
 bs={name:buckets(rr,seed) for name,rr in rows.items()};counts={side:{n:min(cap,min(len(b[side][n]) for b in bs.values())) for n in range(4,11)} for side,cap in [('train',200),('val',50),('test',50)]};rec={'seed':seed,'matched_counts_by_length':counts,'datasets':{}}
 for name,b in bs.items():
  d={side:[x for n,nn in counts[side].items() for x in b[side][n][:nn]] for side in counts};model=fit(d['train']);taus=[]
  for k in range(1,6):
   best=min((average(losses(d['val'],model,taus+[t],k),k),t) for t in [.1,1,10,100,1000]);taus.append(best[1])
  ll=losses(d['test'],model,taus,5);h=[average(ll,k) for k in range(6)];pages=collections.defaultdict(lambda:[0.,0])
  for p,vals,n in ll:pages[p][0]+=vals[2]-vals[3];pages[p][1]+=n
  rng=random.Random(seed);kk=list(pages);bb=[]
  for _ in range(999):
   picked=rng.choices(kk,k=len(kk));bb.append(sum(pages[p][0] for p in picked)/sum(pages[p][1] for p in picked))
  bb.sort();rec['datasets'][name]={'train_words':len(d['train']),'val_words':len(d['val']),'test_words':len(d['test']),'train_units':sum(len(w) for p,w in d['train']),'test_events':sum(x[2] for x in ll),'taus':taus,'test_bits_orders0to5':h,'gain_order2to3':h[2]-h[3],'gain_order2to3_page_bootstrap95':[bb[24],bb[974]]}
 out.append(rec)
(P/'matched_backoff_results.json').write_text(json.dumps(out,indent=2))
for name in rows:
 rr=[x['datasets'][name] for x in out];print(name,'gains', [round(x['gain_order2to3'],4) for x in rr], 'H means',[round(sum(x['test_bits_orders0to5'][k] for x in rr)/len(rr),4) for k in range(6)],'CI',[x['gain_order2to3_page_bootstrap95'] for x in rr])
