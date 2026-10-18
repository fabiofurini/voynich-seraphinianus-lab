import pathlib,collections,random,math,json
P=pathlib.Path(__file__).parent
ns={'__file__':str(P/'stability.py')};exec((P/'stability.py').read_text().split('\nout={}')[0],ns)
rows={k:v for k,v in ns['rows'].items() if k in ['Voynich','Seraphinianus_OCR','latin','italian']}
N=min(7500,min(sum(len(ws) for p,ws in rr) for rr in rows.values()))
def mi(words,B):
 c=collections.Counter(words);pairs=collections.Counter((w,i//B) for i,w in enumerate(words));blocks=collections.Counter(i//B for i in range(len(words)));n=len(words)
 return sum(z/n*math.log2(z*n/(c[w]*blocks[b])) for (w,b),z in pairs.items())
out={}
for name,rr in rows.items():
 words=[];pages=[]
 for p,ws in rr:
  for w in ws:
   if len(words)<N:words.append(w);pages.append(p)
 groups=collections.defaultdict(list)
 for i,p in enumerate(pages):groups[p].append(i)
 rng=random.Random(6337);rec={B:{'observed':mi(words,B),'global':[],'within_page':[]} for B in [100,300,1000,3000]}
 for rep in range(99):
  a=words[:];rng.shuffle(a);b=words[:]
  for inds in groups.values():
   vals=[words[i] for i in inds];rng.shuffle(vals)
   for i,w in zip(inds,vals):b[i]=w
  for B,r in rec.items():r['global'].append(mi(a,B));r['within_page'].append(mi(b,B))
 out[name]={'tokens':N,'pages_or_pseudopages':len(groups),'scales':{B:{'observed_MI':r['observed'],'global_shuffle_mean':sum(r['global'])/99,'within_page_shuffle_mean':sum(r['within_page'])/99,'excess_vs_global':r['observed']-sum(r['global'])/99,'excess_vs_within_page':r['observed']-sum(r['within_page'])/99,'p_upper_global':(1+sum(x>=r['observed'] for x in r['global']))/100,'p_upper_within_page':(1+sum(x>=r['observed'] for x in r['within_page']))/100} for B,r in rec.items()}}
(P/'multiscale_results.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
