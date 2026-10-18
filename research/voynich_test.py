"""Exploratory test, not a decipherment. Python 3 standard library only.
Run: python voynich_test.py /tmp/voynich.evt > results.json
Source: Stolfi/Landini interlinear 1.6e6, Takeshi Takahashi (H).
"""
import sys,re,collections,json,hashlib

raw=open(sys.argv[1],'rb').read()
rows=[]
for line in raw.decode('utf-8').splitlines():
    m=re.match(r'<([^>]+);H>\s*(.*)',line)
    if not m or not re.search(r'\.P\d*\.',m[1]): continue
    text=re.sub(r'\{[^}]*\}','',m[2]).replace('!','').replace('%','')
    ws=[w for w in re.split(r'[.\s,\-=]+',text) if w]
    if len(ws)>1 and all(re.fullmatch('[a-z]+',w) for w in ws):
        page=m[1].split('.')[0]
        rows.append((page,ws))
# All lines from a page stay together. Deterministic split, no optimization.
is_test=lambda p:int(hashlib.sha256(p.encode()).hexdigest()[:8],16)%3==0
train=[(p,w) for p,w in rows if not is_test(p)]
test=[(p,w) for p,w in rows if is_test(p)]
vocab=collections.Counter(x for _,w in train for x in w[:-1])
candidates=['']+sorted(set(''.join(vocab)))+['ch','sh','aiin','in','dy']
def evaluate(rr,replacement,ending='m'):
    words=[w[-1] for _,w in rr if w[-1].endswith(ending)]
    pairs=[(w,w[:-len(ending)]+replacement) for w in words]
    hits=[(a,b) for a,b in pairs if b in vocab]
    return dict(n=len(words),hits=len(hits),rate=round(len(hits)/len(words),4) if words else None,
                examples=collections.Counter(hits).most_common(12))
rank=sorted(candidates,key=lambda r:evaluate(train,r)['hits'],reverse=True)
out={'source_sha256':hashlib.sha256(raw).hexdigest(),
 'clean_lines':len(rows),'train_pages':len(set(p for p,_ in train)),
 'test_pages':len(set(p for p,_ in test)),
 'method':'Map terminal EVA m to a fixed string; score membership in TRAIN internal-word vocabulary. Rank on train; evaluate on held-out pages. No phonetic interpretation.',
 'candidate_ranking_train':[(r,evaluate(train,r)['hits']) for r in rank],
 'winner':rank[0], 'winner_train':evaluate(train,rank[0]),
 'winner_test':evaluate(test,rank[0]),
 'identity_test':evaluate(test,'m'),
 'all_candidates_test':{r:evaluate(test,r)['rate'] for r in candidates},
 'limits':['Vocabulary overlap is not semantic evidence.','Common target endings and short forms can inflate matches.','A global substitution may conceal multiple glyph functions.','Single transcription; no image validation.','Exploratory hypothesis; not evidence of novel discovery.']}
print(json.dumps(out,indent=2,ensure_ascii=False))
