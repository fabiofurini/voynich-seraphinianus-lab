import re,json,random,math,collections,hashlib,pathlib
root=pathlib.Path(__file__).resolve().parent.parent
rows={};v=[]
for line in (root/'patterns/voynich_ZL3b.txt').read_text().splitlines():
 m=re.match(r'<(f[^.>]+)\.([^,>]+),([^>]*P0)>\s*(.*)',line)
 if not m:continue
 t=re.sub(r'<[^>]*>','',m[4].replace('<->','.'));w=[x for x in re.split(r'[.,\s]+',t) if x]
 if len(w)>1 and all(re.fullmatch('[a-z]+',x) for x in w):v.append((m[1],w))
rows['Voynich']=v;s=[];page=None
for line in (root/'seraph_ocr/CS_OCR_TRANSLITERATION.txt').read_text().splitlines():
 if line.startswith('###PAGE'):page=line.split()[-1];continue
 if line.startswith('#') or not line.strip():continue
 w=line.split()
 if page and len(w)>1 and all(re.fullmatch('[A-Za-z]+',x) for x in w):s.append((page,w))
rows['Seraphinianus_OCR']=s
rows['Voynich_connected_EVA']=[(p,[re.sub(r'ckh|cth|cph|cfh|ch|sh',lambda m:dict(zip(['ckh','cth','cph','cfh','ch','sh'],'αβγδεζ'))[m[0]],w) for w in ws]) for p,ws in v]
rows['Seraphinianus_lowercase_sensitivity']=[(p,[w.lower() for w in ws]) for p,ws in s]

def mi(pairs):
 c=collections.Counter(pairs);a=collections.Counter();b=collections.Counter();n=sum(c.values())
 for (x,y),z in c.items():a[x]+=z;b[y]+=z
 return sum(z/n*math.log2(z*n/a[x]/b[y]) for (x,y),z in c.items())
def score(train,test,k):
 alphabet=set(''.join(w for _,ws in train+test for w in ws))|{'$'};K=len(alphabet);cs=collections.defaultdict(collections.Counter)
 for _,ws in train:
  for w in ws:
   t='^'*k+w+'$'
   for i in range(k,len(t)):cs[t[i-k:i] if k else ''][t[i]]+=1
 totals={x:sum(c.values()) for x,c in cs.items()};loss=0;n=0
 for _,ws in test:
  for w in ws:
   t='^'*k+w+'$'
   for i in range(k,len(t)):
    context=t[i-k:i] if k else '';loss-=math.log2((cs[context][t[i]]+.1)/(totals.get(context,0)+.1*K));n+=1
 return {'bits_per_encoded_character_including_end':loss/n,'contexts':len(totals)}
out={}
for name,rr in rows.items():
 rng=random.Random(20261018);pages=sorted(set(p for p,_ in rr));rng.shuffle(pages);held=set(pages[:max(1,len(pages)//5)]);train=[r for r in rr if r[0] not in held];test=[r for r in rr if r[0] in held]
 obs=mi((a[-1],b[0]) for _,ws in rr for a,b in zip(ws,ws[1:]));null=[]
 for _ in range(199):
  shuffled=[]
  for p,ws in rr:
   x=ws[:];rng.shuffle(x);shuffled.append((p,x))
  null.append(mi((a[-1],b[0]) for _,ws in shuffled for a,b in zip(ws,ws[1:])))
 scrambled=[]
 for p,ws in rr:
  ww=[]
  for w in ws:
   x=list(w);rng.shuffle(x);ww.append(''.join(x))
  scrambled.append((p,ww))
 out[name]={'pages':len(pages),'lines':len(rr),'tokens':sum(len(ws) for _,ws in rr),'train_pages':len(pages)-len(held),'test_pages':len(held),'word_internal_models':{k:score(train,test,k) for k in range(4)},'within_word_character_shuffle_models':{k:score([r for r in scrambled if r[0] not in held],[r for r in scrambled if r[0] in held],k) for k in range(4)},'word_boundary_last_first_MI':{'observed':obs,'line_word_shuffle_mean':sum(null)/len(null),'null_min':min(null),'null_max':max(null),'p_upper':(1+sum(x>=obs for x in null))/200}}
(root/'grammar_comparison/results.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
