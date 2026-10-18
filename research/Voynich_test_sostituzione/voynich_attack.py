import re,collections,math,unicodedata,json,random,subprocess,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parent
R=ROOT/'run';R.mkdir(exist_ok=True)
BIN=ROOT/'voynich_attack_bin'
if not BIN.exists():subprocess.run(['g++','-O3','-std=c++17',str(ROOT/'voynich_attack.cpp'),'-o',str(BIN)],check=True)
core=['a','d','e','f','g','i','k','l','m','n','o','p','q','r','s','t','y','ch','sh','ckh','cth','cph','cfh']
lookup={s:chr(97+i) for i,s in enumerate(core)}
voy={'train':[],'test':[]}
meta={}
for line in open(ROOT/'sources'/'voynich_ZL3b.txt'):
 h=re.match(r'<(f[^.>]+)>\s+<! (.*)>',line)
 if h:meta=dict(re.findall(r'\$(\w)=([^\s>]+)',h[2]))
 m=re.match(r'<(f[^.>]+)\.[^,>]+,[^>]*P0>\s*(.*)',line)
 if not m or meta.get('H')!='1' or meta.get('I')!='H' or meta.get('L')!='A':continue
 text=re.sub('<->','.',m[2]);text=re.sub('<[^>]*>','',text)
 side='test' if int(hashlib.sha256(m[1].encode()).hexdigest()[:8],16)%3==0 else 'train'
 for w in re.split(r'[.,\s]+',text):
  units=re.findall('ckh|cth|cph|cfh|ch|sh|.',w)
  if units and all(x in lookup for x in units):voy[side].append(''.join(lookup[x] for x in units))
trainvoy=' '.join(voy['train'])[:20000].rsplit(' ',1)[0]
testvoy=' '.join(voy['test'])
def norm(s):
 s=unicodedata.normalize('NFKD',s.lower());s=''.join(c for c in s if not unicodedata.combining(c))
 return ' '.join(re.findall('[a-z]+',s))
def make_input(name,s):
 grams=collections.Counter(tuple(26 if c==' ' else ord(c)-97 for c in s[i:i+4]) for i in range(len(s)-3))
 path=R/(name+'.cipher')
 path.write_text(s+'\n'+str(len(grams))+'\n'+'\n'.join(' '.join(map(str,g))+' '+str(n) for g,n in grams.items()))
 return path
def coverage(s,lex):
 w=[x for x in s.split() if len(x)>=3]
 return {'recognized_tokens':sum(x in lex for x in w),'tokens':len(w),'fraction':sum(x in lex for x in w)/len(w)}
results=json.loads((R/'results.json').read_text()) if (R/'results.json').exists() else {}
for lang in ['latin','italian']:
 if lang in results:continue
 try:raw=(ROOT/'sources'/('crib_'+lang+'.txt')).read_text(encoding='utf-8-sig')
 except UnicodeDecodeError:raw=(ROOT/'sources'/('crib_'+lang+'.txt')).read_text(encoding='latin-1')
 if lang=='italian':
  if '*** START' in raw:raw=raw.split('*** START',1)[1].split('***',1)[1]
  if '*** END' in raw:raw=raw.split('*** END',1)[0]
 else:raw=re.sub(r'<[^>]*>','',raw)
 plaintext=norm(raw);split=int(len(plaintext)*.8);split=plaintext.rfind(' ',0,split)
 lmtext=plaintext[:split];control=plaintext[split+1:][:20000].rsplit(' ',1)[0]
 N=27**4;counts=[0]*N
 for i in range(len(lmtext)-3):
  k=0
  for c in lmtext[i:i+4]:k=k*27+(26 if c==' ' else ord(c)-97)
  counts[k]+=1
 alpha=.01;den=sum(counts)+alpha*N
 lm=R/(lang+'.lm');lm.write_text('\n'.join(str(math.log((n+alpha)/den)) for n in counts))
 freq=R/(lang+'.freq');cf=collections.Counter(lmtext);freq.write_text(' '.join(str(cf[chr(97+i)]) for i in range(26)))
 lex=set(lmtext.split());rng=random.Random(20261017);perm=list('abcdefghijklmnopqrstuvwxyz');rng.shuffle(perm)
 cipher=''.join(' ' if c==' ' else perm[ord(c)-97] for c in control)
 lc={}
 for case,text in [('positive_control',cipher),('voynich',trainvoy)]:
  inp=make_input(lang+'_'+case,text)
  out=subprocess.check_output([str(BIN),str(lm),str(inp),str(freq),'8','50000'],text=True)
  (R/(lang+'_'+case+'.out')).write_text(out)
  score,key,decoded=out.splitlines()[:3]
  rec={'training_score_per_quadgram':float(score)/(len(text)-3),'key':key,'training_dictionary_coverage':coverage(decoded,lex)}
  if case=='positive_control':
   mask=[i for i,c in enumerate(control) if c!=' ']
   rec['character_recovery']=sum(control[i]==decoded[i] for i in mask)/len(mask)
   rec['true_plaintext_dictionary_coverage']=coverage(control,lex)
  else:
   held=''.join(' ' if c==' ' else key[ord(c)-97] for c in testvoy)
   rec['heldout_dictionary_coverage']=coverage(held,lex)
   rec['heldout_sample']=held[:300]
  lc[case]=rec
 results[lang]={'language_model_chars':len(lmtext),'control_chars':len(control),'cipher_train_chars':len(trainvoy),'cipher_test_chars':len(testvoy),'cases':lc}
 print(lang,json.dumps(results[lang]),flush=True)
 (R/'results.json').write_text(json.dumps(results,indent=2))
