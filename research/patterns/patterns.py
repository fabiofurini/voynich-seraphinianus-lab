import re,collections,json,math,random,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
src=ROOT/'voynich_ZL3b.txt'
merge='--merge-commas' in sys.argv
rows=[]
for line in src.read_text().splitlines():
 m=re.match(r'<(f[^.>]+)\.([^,>]+),([^>]*P0)>\s*(.*)',line)
 if not m:continue
 raw=m[4];para='<%>' in raw
 text=raw.replace('<->','.')
 text=re.sub(r'<[^>]*>','',text)
 if merge:text=text.replace(',','')
 # Strict sample: no alternatives, special groups or unknown signs in a row.
 words=[w for w in re.split(r'[.,\s]+',text) if w]
 if len(words)>1 and all(re.fullmatch('[a-z]+',w) for w in words):rows.append((m[1],words,para))
C=collections.Counter(w for _,ws,_ in rows for w in ws)
bi=collections.Counter();tri=collections.Counter();pages=collections.defaultdict(set)
repeat=0;exp_repeat=0;start=collections.Counter();otherstart=collections.Counter()
for p,ws,para in rows:
 cc=collections.Counter(ws);n=len(ws)
 repeat+=sum(a==b for a,b in zip(ws,ws[1:]))
 exp_repeat+=sum(c*(c-1)/n for c in cc.values())
 bi.update(zip(ws,ws[1:]));tri.update(zip(ws,ws[1:],ws[2:]))
 for ng in zip(ws,ws[1:]):pages[ng].add(p)
 (start if para else otherstart).update([ws[0][0]])
for_ng=[]
for ng,count in bi.most_common(25):
 expected=0
 for _,ws,_ in rows:
  cc=collections.Counter(ws);a,b=ng
  expected+=cc[a]*(cc[b]-(a==b))/len(ws)
 for_ng.append({'words':ng,'count':count,'pages':len(pages[ng]),'expected_line_shuffle':round(expected,3),'ratio':round(count/expected,3) if expected else None})
patterns={}
for n in [3,4,5,6]:
 ngs=collections.Counter();pp=collections.defaultdict(set)
 for p,ws,_ in rows:
  for i in range(len(ws)-n+1):ng=tuple(ws[i:i+n]);ngs[ng]+=1;pp[ng].add(p)
 patterns[n]=[{'words':ng,'count':c,'pages':len(pp[ng])} for ng,c in ngs.most_common(12) if c>=2]
stems=['ok','qok','ot','qot','ch','sh'];endings=['aiin','ain','edy','eedy','ol','ar']
families={p:{e:C[p+e] for e in endings} for p in stems}
def mi(pairs):
 c=collections.Counter(pairs);a=collections.Counter();b=collections.Counter();N=sum(c.values())
 for (x,y),n in c.items():a[x]+=n;b[y]+=n
 return sum(n/N*math.log2(n*N/(a[x]*b[y])) for (x,y),n in c.items())
actual_mi=mi((a[-1],b[0]) for _,ws,_ in rows for a,b in zip(ws,ws[1:]))
rng=random.Random(20261017);repnull=[];minull=[]
for _ in range(499):
 shuffled=[];rep=0
 for _,ws,_ in rows:
  v=ws[:];rng.shuffle(v);rep+=sum(a==b for a,b in zip(v,v[1:]));shuffled.append(v)
 repnull.append(rep);minull.append(mi((a[-1],b[0]) for ws in shuffled for a,b in zip(ws,ws[1:])))
paired=collections.defaultdict(lambda:[0,0,0,0])
for p,ws,para in rows:
 i=0 if para else 2;paired[p][i]+=ws[0][0] in 'fkpt';paired[p][i+1]+=1
both=[v for v in paired.values() if v[1] and v[3]]
out={'scope':'ZL3b; P0 paragraphs only; whole rows with ambiguous tokens excluded; no cross-line ngrams.',
 'comma_policy':'merge' if merge else 'split',
 'lines':len(rows),'pages':len(set(p for p,_,_ in rows)),'tokens':sum(C.values()),
 'adjacent_identical_words':{'observed':repeat,'exact_shuffle_expectation':exp_repeat,'null_min_max':[min(repnull),max(repnull)],'permutations':len(repnull)},
 'boundary_last_first_eva_char_mi_bits':{'observed':actual_mi,'shuffle_mean':sum(minull)/len(minull),'shuffle_min_max':[min(minull),max(minull)]},
 'paragraph_first_letters':dict(start),'other_line_first_letters':dict(otherstart),
 'paired_page_initials':{'pages':len(both),'higher_paragraph_gallows_rate':sum(v[0]/v[1]>v[2]/v[3] for v in both),'ties':sum(v[0]/v[1]==v[2]/v[3] for v in both)},
 'word_family_counts':families,'common_bigrams':for_ng,'repeated_sequences':patterns}
(ROOT/('results_merge.json' if merge else 'results.json')).write_text(json.dumps(out,ensure_ascii=False,indent=2))
print(json.dumps(out,ensure_ascii=False,indent=2))
