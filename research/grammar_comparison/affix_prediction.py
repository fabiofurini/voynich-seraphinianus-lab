import pathlib,re,collections,random,math,json,unicodedata
P=pathlib.Path(__file__).parent
ns={'__file__':str(P/'run.py')};exec((P/'run.py').read_text().split('out={}')[0],ns)
rows={k:v for k,v in ns['rows'].items() if k in ['Voynich','Seraphinianus_OCR']}
rows['Voynich']=[(p,[tuple(re.findall('ckh|cth|cph|cfh|ch|sh|.',w)) for w in ws]) for p,ws in rows['Voynich']]
rows['Seraphinianus_OCR']=[(p,[tuple(w) for w in ws]) for p,ws in rows['Seraphinianus_OCR']]

base=P.parent/'Voynich_test_sostituzione/sources'
for lang in ['latin','italian']:
 try:t=(base/('crib_'+lang+'.txt')).read_text(encoding='utf-8-sig')
 except UnicodeDecodeError:t=(base/('crib_'+lang+'.txt')).read_text(encoding='latin-1')
 if '*** START' in t:t=t.split('*** START',1)[1].split('***',1)[1]
 if '*** END' in t:t=t.split('*** END',1)[0]
 t=re.sub('<[^>]*>','',t);t=unicodedata.normalize('NFKD',t.lower());t=''.join(c for c in t if not unicodedata.combining(c));ws=re.findall('[a-z]+',t)
 rows[lang]=[(str(i//150),[tuple(w) for w in ws[i:i+10]]) for i in range(0,len(ws),10)]
rng=random.Random(123);synthetic=[]
for p in range(100):
 ww=[]
 for j in range(60):
  c=rng.randrange(4);a=['ab','cd','ef','gh'][c];b=['ij','kl','mn','op'][c];middle=''.join(rng.choices('qrstuv',k=rng.randrange(3,8)));ww.append(tuple(a+middle+b))
 synthetic.append((str(p),ww))
rows['positive_control_prefix_suffix_agreement']=synthetic

def collect(rr):
 out=[]
 for p,ws in rr:
  for w in ws:
   if len(w)>=5:out.append((p,w))
 return out

def fit(data):
 marginal=collections.defaultdict(collections.Counter);ctx=[collections.defaultdict(collections.Counter) for _ in range(3)]
 for p,w in data:
  n=len(w);s=w[-2:];marginal[n][s]+=1
  ctx[0][(n,w[:2])][s]+=1
  ctx[1][(n,w[-4:-2])][s]+=1
  ctx[2][(n,w[:2],w[-4:-2])][s]+=1
 return marginal,ctx

def losses(data,model,K,taus):
 marg,ctx=model;out=[]
 for p,w in data:
  n=len(w);s=w[-2:];cc=marg[n];tot=sum(cc.values());base=(cc[s]+.1)/(tot+.1*K)
  pp=[base]
  for j,key in enumerate([w[:2],w[-4:-2]]):
   c=ctx[j][(n,key)];t=sum(c.values());pp.append((c[s]+taus[j]*base)/(t+taus[j]))
  c=ctx[2][(n,w[:2],w[-4:-2])];t=sum(c.values());pp.append((c[s]+taus[2]*pp[2])/(t+taus[2]))
  out.append((p,w,[-math.log2(x) for x in pp]))
 return out
out={}
for name,rr in rows.items():
 data=collect(rr);alphabet=set(x for p,w in data for x in w);K=len(alphabet)**2;splits=[]
 for seed in range(5):
  rng=random.Random(33125+seed);pages=sorted(set(p for p,w in data));rng.shuffle(pages);n=len(pages);testp=set(pages[:n//5]);valp=set(pages[n//5:2*(n//5)]);train=[d for d in data if d[0] not in testp|valp];val=[d for d in data if d[0] in valp];test=[d for d in data if d[0] in testp];model=fit(train);taus=[]
  for j in range(3):
   scores=[]
   for tau in [1,10,100,1000]:
    ll=losses(val,model,K,taus+[tau]*(3-len(taus)));scores.append((sum(x[2][j+1] for x in ll)/len(ll),tau))
   taus.append(min(scores)[1])
  ll=losses(test,model,K,taus);seen=set(w for p,w in train);new=[x for x in ll if x[1] not in seen]
  mean=lambda z:[sum(x[2][i] for x in z)/len(z) for i in range(4)] if z else []
  # Bootstrap by held-out page, paired prefix gain vs sequential.
  pg=collections.defaultdict(lambda:[0.,0])
  for p,w,l in ll:pg[p][0]+=l[2]-l[3];pg[p][1]+=1
  keys=list(pg);boots=[]
  for b in range(999):
   kk=rng.choices(keys,k=len(keys));boots.append(sum(pg[k][0] for k in kk)/sum(pg[k][1] for k in kk))
  boots.sort();splits.append({'seed':33125+seed,'train_tokens':len(train),'validation_tokens':len(val),'test_tokens':len(test),'test_unseen_form_tokens':len(new),'selected_taus_prefix_sequential':taus,'test_bits_per_suffix_baseline_prefix_sequential_combined':mean(ll),'unseen_form_bits_per_suffix_baseline_prefix_sequential_combined':mean(new),'combined_gain_vs_sequential_page_bootstrap95':[boots[24],boots[974]]})
 out[name]=splits
(P/'affix_prediction_results.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
