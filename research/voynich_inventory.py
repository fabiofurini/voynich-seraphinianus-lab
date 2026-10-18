"""Candidate graphic inventory, not phonetic decipherment.
python voynich_inventory.py voynich_ZL3b.txt voynich_source.evt > inventory.json
Counts only readable tokens in paragraph text; does not discard whole lines.
"""
import sys,re,json,collections
CORE=['a','d','e','f','g','i','k','l','m','n','o','p','q','r','s','t','y','ch','sh','ckh','cth','cph','cfh']
def words(path,kind):
    out=[]
    for line in open(path):
        if kind=='ZL':
            m=re.match(r'<f[^.>]+\.[^,>]+,[^>]*P0>\s*(.*)',line)
            if not m:continue
            t=re.sub('<->','.',m[1]);t=re.sub('<[^>]*>','',t)
            t=re.sub(r'\{[^}]*\}','?',t)
        else:
            m=re.match(r'<([^>]+);H>\s*(.*)',line)
            if not m or not re.search(r'\.P\d*\.',m[1]):continue
            t=re.sub(r'\{[^}]*\}','',m[2]).replace('!','').replace('%','')
        out.extend(w for w in re.split(r'[.,\s\-=]+',t) if re.fullmatch('[a-z]+',w))
    return out
def stats(ws):
    counts=collections.Counter(t for w in ws for t in re.findall('ckh|cth|cph|cfh|ch|sh|.',w))
    chars=collections.Counter(''.join(ws))
    def relation(ch):
        before=collections.Counter();after=collections.Counter()
        for w in ws:
            for j,c in enumerate(w):
                if c==ch:
                    before[w[j-1] if j else '^']+=1
                    after[w[j+1] if j+1<len(w) else '$']+=1
        return {'n':chars[ch],'previous':dict(before),'next':dict(after)}
    runs=collections.Counter()
    for w in ws:
        for m in re.finditer(r'i+n',w):runs[m[0]]+=1
    return {'readable_paragraph_tokens':len(ws),'eva_characters':sum(chars.values()),
        'graphic_tokens':sum(counts.values()),'core_23_counts':{x:counts[x] for x in CORE},
        'other_counts':{x:n for x,n in counts.items() if x not in CORE},
        'core_coverage':sum(counts[x] for x in CORE)/sum(counts.values()),
        'relations':{x:relation(x) for x in ['c','h','q','n']},'i_run_n_clusters':dict(runs)}
out={kind:stats(words(path,kind)) for kind,path in [('ZL',sys.argv[1]),('H',sys.argv[2])]}
out['hypothesis']={'core':CORE,'status':'Provisional inventory of graphical units; not 23 established letters.',
 'ambiguities':['in/iin/iiin may require single units or a compositional model.',
 'ch/sh may be distinct or base-plus-diacritic; compound gallows may be ligatures.',
 'qo may be a unit, a prefix, or a constrained pair.',
 'm and r are retained as distinct; no global merger justified.',
 'Rare forms and excluded ambiguous tokens prevent completeness claims.']}
print(json.dumps(out,indent=2))
