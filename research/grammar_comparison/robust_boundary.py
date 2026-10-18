import re,collections,random,math,json,pathlib
R=pathlib.Path(__file__).resolve().parent.parent
rows={};v=[]
for line in (R/'patterns/voynich_ZL3b.txt').read_text().splitlines():
 m=re.match(r'<(f[^.>]+)\.([^,>]+),([^>]*P0)>\s*(.*)',line)
 if not m:continue
 t=re.sub(r'<[^>]*>','',m[4].replace('<->','.'));ws=[w for w in re.split(r'[.,\s]+',t) if w]
 if len(ws)>1 and all(re.fullmatch('[a-z]+',w) for w in ws):v.append((m[1],ws))
rows['Voynich']=v;s=[];page=None
for line in (R/'seraph_ocr/CS_OCR_TRANSLITERATION.txt').read_text().splitlines():
 if line.startswith('###PAGE'):page=line.split()[-1];continue
 if line.startswith('#'):continue
 ws=line.split()
 if page and len(ws)>1 and all(re.fullmatch('[A-Za-z]+',w) for w in ws):s.append((page,ws))
rows['Seraphinianus_OCR']=s

def mi(pairs):
 c=collections.Counter(pairs);a=collections.Counter();b=collections.Counter();n=sum(c.values())
 for (x,y),z in c.items():a[x]+=z;b[y]+=z
 return sum(z/n*math.log2(z*n/(a[x]*b[y])) for (x,y),z in c.items())
out={}
for name,rr in rows.items():
 rng=random.Random(81273);obs=mi((a[-1],b[0]) for p,ws in rr for a,b in zip(ws,ws[1:]));null=[]
 # Independently permute whole words within same page, coarse line position, length bin.
 # Keeps positional distributions and approximate lengths; breaks neighboring word pairing.
 groups=collections.defaultdict(list);slots=[]
 for j,(p,ws) in enumerate(rr):
  for i,w in enumerate(ws):
   pos=0 if i==0 else 3 if i==len(ws)-1 else 1 if i/len(ws)<.5 else 2
   k=(p,pos,min(len(w)//3,4));groups[k].append(w);slots.append((j,i,k))
 for _ in range(199):
  pools={k:rng.sample(ws,len(ws)) for k,ws in groups.items()};indices=collections.Counter();new=[['']*len(ws) for _,ws in rr]
  for j,i,k in slots:new[j][i]=pools[k][indices[k]];indices[k]+=1
  null.append(mi((a[-1],b[0]) for ws in new for a,b in zip(ws,ws[1:])))
 out[name]={'observed_MI':obs,'position_length_page_preserving_null_mean':sum(null)/len(null),'null_min':min(null),'null_max':max(null),'p_upper':(1+sum(x>=obs for x in null))/200,'permutations':199,'singleton_slots':sum(len(v) for v in groups.values() if len(v)==1),'all_slots':len(slots)}
print(json.dumps(out,indent=2));(R/'grammar_comparison/robust_boundary_results.json').write_text(json.dumps(out,indent=2))
