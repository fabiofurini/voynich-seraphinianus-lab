"""Run python voynich_controls.py SOURCE_H SOURCE_ZL > controls.json.
Exploratory robustness tests; all strings are EVA, never translations.
"""
import re,sys,json,hashlib,collections,random

def load(path,kind,comma='split'):
    rows=[];meta={}
    for line in open(path):
        if kind=='ZL':
            header=re.match(r'<(f[^.>]+)>\s+<! (.*)>',line)
            if header:meta=dict(re.findall(r'\$(\w)=([^\s>]+)',header[2]))
            m=re.match(r'<(f[^.>]+)\.([^,>]+),[^>]*P0>\s*(.*)',line)
            if not m:continue
            page,text=m[1],m[3]
            text=re.sub(r'<->','.',text)
            text=re.sub(r'<[^>]*>','',text)
            # Curly groups denote nonbasic/compound glyphs here: reject, do not erase.
            text=re.sub(r'\{[^}]*\}','?',text)
        else:
            m=re.match(r'<([^>]+);H>\s*(.*)',line)
            if not m or not re.search(r'\.P\d*\.',m[1]):continue
            page=m[1].split('.')[0];text=re.sub(r'\{[^}]*\}','',m[2])
        if comma=='reject' and ',' in text:continue
        text=text.replace(',', '.' if comma=='split' else '')
        text=text.replace('!','').replace('%','')
        words=[x for x in re.split(r'[.\s\-=]+',text) if x]
        if len(words)>1 and all(re.fullmatch('[a-z]+',x) for x in words):
            rows.append((page,words,dict(meta)))
    return rows

def test(rows):
    held=lambda p:int(hashlib.sha256(p.encode()).hexdigest()[:8],16)%3==0
    train=[x for x in rows if not held(x[0])];test=[x for x in rows if held(x[0])]
    vocab=set(w for _,ws,_ in train for w in ws[:-1])
    seen=set(w for _,ws,_ in train for w in ws)
    targets=[(p,ws[-1]) for p,ws,_ in test if ws[-1].endswith('m')]
    types=sorted(set(w for _,w in targets));novel=[w for w in types if w not in seen]
    candidates=['m','r','l','in','iin','ain','n','y','ry','rl','']
    score=lambda w,r:w[:-1]+r in vocab
    def rates(words):
        return {r:{'hits':sum(score(w,r) for w in words),'n':len(words)} for r in candidates}
    pages=collections.defaultdict(list)
    for p,w in targets:pages[p].append(w)
    rng=random.Random(20261017);keys=sorted(pages);boot=[]
    for _ in range(4000):
        sample=[w for p in rng.choices(keys,k=len(keys)) for w in pages[p]]
        boot.append(sum(int(score(w,'r'))-int(score(w,'l')) for w in sample)/len(sample))
    boot.sort()
    controls={}
    for ending in ['m','l','s','n','y']:
        ww=[ws[-1] for _,ws,_ in test if ws[-1].endswith(ending)]
        controls[ending]={'n':len(ww),'to_r':sum(w[:-1]+'r' in vocab for w in ww),
                          'identity':sum(w in vocab for w in ww)}
    bigrams=set((ws[i-1],w) for _,ws,_ in train for i,w in enumerate(ws)
                if i>0 and i<len(ws)-1)
    contexts=[(ws[-2],ws[-1]) for _,ws,_ in test if ws[-1].endswith('m')]
    context_scores={r:{'matches':sum((a,b[:-1]+r) in bigrams for a,b in contexts),
                       'n':len(contexts)} for r in ['m','r','l','in','iin']}
    position={}
    for label,field in [('hand','H'),('currier','L')]:
        grouped=collections.defaultdict(lambda:[0,0,0,0])
        for _,ws,meta in rows:
            g=grouped[meta.get(field,'unknown')];g[0]+=1
            g[1]+=sum(w.endswith('m') for w in ws)
            g[2]+=ws[-1].endswith('m');g[3]+=len(ws)
        position[label]=dict(grouped)
    return {'lines':len(rows),'pages':len(set(p for p,_,_ in rows)),
            'train_pages':len(set(p for p,_,_ in train)),
            'test_pages':len(set(p for p,_,_ in test)),
            'token_scores':rates([w for _,w in targets]),'type_scores':rates(types),
            'unseen_type_scores':rates(novel),'unseen_types':novel,
            'r_minus_l_page_bootstrap_95pct':[boot[100],boot[3899]],
            'last_letter_controls':controls,'position_groups':position,
            'exact_previous_word_context':context_scores,
            'test_page_scores':{p:{'n':len(ww),'r':sum(score(w,'r') for w in ww),
                                  'l':sum(score(w,'l') for w in ww)} for p,ww in pages.items()}}

results={}
for kind,path in [('H',sys.argv[1]),('ZL',sys.argv[2])]:
    for comma in ['split','merge','reject']:
        results[kind+'_'+comma]=test(load(path,kind,comma))
print(json.dumps(results,indent=2))
