"""Exploratory same-hand, same-Currier visual-section prediction.
Requires numpy. Run: python voynich_sections.py ZL3b.txt > sections.json
"""
import sys,re,json,random,hashlib,collections
import numpy as np

pages={};meta={}
for line in open(sys.argv[1]):
    h=re.match(r'<(f[^.>]+)>\s+<! (.*)>',line)
    if h:meta=dict(re.findall(r'\$(\w)=([^\s>]+)',h[2]))
    m=re.match(r'<(f[^.>]+)\.([^,>]+),[^>]*P0>\s*(.*)',line)
    if not m or meta.get('H')!='2' or meta.get('L')!='B' or meta.get('I') not in ['H','B']:continue
    text=re.sub(r'<->','.',m[3]);text=re.sub(r'<[^>]*>','',text)
    text=re.sub(r'\{[^}]*\}','?',text).replace(',','.').replace('!','').replace('%','')
    words=[w for w in re.split(r'[.\s\-=]+',text) if w]
    if len(words)>2 and all(re.fullmatch('[a-z]+',w) for w in words):
        d=pages.setdefault(m[1],{'meta':dict(meta),'words':[]})
        d['words'].extend(words[1:-1])
pages={p:d for p,d in pages.items() if len(d['words'])>=30}
names=sorted(pages);groups=[pages[p]['meta']['Q']+'-'+pages[p]['meta']['B'] for p in names]
y=np.array([int(pages[p]['meta']['I']=='B') for p in names])
unique=sorted(set(groups));indices=[np.where(np.array(groups)==g)[0] for g in unique]
def prepare(seed,feature):
    docs=[]
    for p in names:
        rng=random.Random(f'{seed}:{p}')
        ws=rng.sample(pages[p]['words'],30)
        docs.append([w if feature=='word' else w[-1] if feature=='last_char' else w[-2:] for w in ws])
    vocab=sorted(set(x for d in docs for x in d));lookup={w:i for i,w in enumerate(vocab)}
    X=np.zeros((len(names),len(vocab)))
    for i,d in enumerate(docs):
        for w in d:X[i,lookup[w]]+=1
    return X,vocab
def predict(X,labels):
    out=np.zeros(len(names),dtype=int)
    for ix in indices:
        mask=np.ones(len(names),dtype=bool);mask[ix]=False
        active=X[mask].sum(axis=0)>0
        counts=np.stack([X[mask & (labels==c)][:,active].sum(axis=0)+1 for c in [0,1]])
        probs=np.log(counts/counts.sum(axis=1,keepdims=True))
        out[ix]=np.argmax(X[ix][:,active]@probs.T,axis=1)
    return out
def bal(pred,labels):
    return float(np.mean([np.mean(pred[labels==c]==c) for c in [0,1]]))
result={'design':'Hand 2, Currier B only. H vs B illustration categories. 30 randomly sampled interior tokens/page. Leave one quire+bifolio group out; uniform class prior; add-one multinomial NB.',
        'limits':['Section and quire/location are confounded: this is NOT proof of semantic content.',
                  'Hand/Currier assignments and illustration categories are supplied by ZL metadata.',
                  'Pseudotext or a changing encoding could yield section prediction.',
                  'Exploratory design selected after inspecting metadata; no external confirmation.'],
        'n_pages':len(names),'class_counts':{'H':int(sum(y==0)),'B':int(sum(y==1))},
        'n_bifolio_groups':len(unique),'features':{}}
for feature in ['word','last_char','last_two_chars']:
    X,v=prepare(20261017,feature);pred=predict(X,y)
    scores=[bal(predict(prepare(seed,feature)[0],y),y) for seed in range(30)]
    result['features'][feature]={'correct':int(sum(pred==y)),'balanced_accuracy':bal(pred,y),
        'sampling_30_seeds_range':[min(scores),max(scores)],'sampling_30_seeds_median':float(np.median(scores))}
    if feature=='word':
        result['page_predictions']=[{'page':p,'group':groups[i],'truth':'B' if y[i] else 'H',
            'pred':'B' if pred[i] else 'H'} for i,p in enumerate(names)]
        # Group-level label permutations preserve within-bifolio dependence.
        gl=[y[ix[0]] for ix in indices];rng=random.Random(20261017);null=[]
        for _ in range(1999):
            shuffled=gl[:];rng.shuffle(shuffled);yp=np.zeros(len(y),dtype=int)
            for ix,label in zip(indices,shuffled):yp[ix]=label
            null.append(bal(predict(X,yp),yp))
        result['permutation_reference']={'n':len(null),'mean':float(np.mean(null)),
           'fraction_at_least_observed_plus_one':(1+sum(s>=bal(pred,y) for s in null))/(len(null)+1),
           'caveat':'Bifolio permutation is a reference model, not a control for quire/location.'}
print(json.dumps(result,indent=2))
