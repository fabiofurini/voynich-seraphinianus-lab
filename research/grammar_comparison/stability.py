import pathlib,json,random,re,unicodedata
P=pathlib.Path(__file__).parent
ns={'__file__':str(P/'run.py')};exec((P/'run.py').read_text().split('out={}')[0],ns)
rows=ns['rows'];score=ns['score'];base=P.parent/'Voynich_test_sostituzione/sources'
for lang in ['latin','italian']:
 try:s=(base/('crib_'+lang+'.txt')).read_text(encoding='utf-8-sig')
 except UnicodeDecodeError:s=(base/('crib_'+lang+'.txt')).read_text(encoding='latin-1')
 if '*** START' in s:s=s.split('*** START',1)[1].split('***',1)[1]
 if '*** END' in s:s=s.split('*** END',1)[0]
 s=re.sub('<[^>]*>','',s);s=unicodedata.normalize('NFKD',s.lower());s=''.join(c for c in s if not unicodedata.combining(c));ws=re.findall('[a-z]+',s)
 # Artificial pages of 150 words, split into 10-word rows. Not manuscript pages.
 rows[lang]=[(str(i//150),ws[i:i+10]) for i in range(0,len(ws),10) if len(ws[i:i+10])>1]
out={}
for name,rr in rows.items():
 splits=[]
 for seed in range(5):
  rng=random.Random(seed+9821);pages=sorted(set(p for p,_ in rr));rng.shuffle(pages);held=set(pages[:max(1,len(pages)//5)]);train=[r for r in rr if r[0] not in held];test=[r for r in rr if r[0] in held]
  scores=[score(train,test,k)['bits_per_encoded_character_including_end'] for k in range(4)]
  splits.append({'seed':seed+9821,'H':scores,'relative_reduction_H0_H2':1-scores[2]/scores[0],'gain_order2_to3':scores[2]-scores[3]})
 out[name]=splits
(P/'stability_results.json').write_text(json.dumps(out,indent=2))
for name,ss in out.items():
 vals=[s['relative_reduction_H0_H2'] for s in ss];gain=[s['gain_order2_to3'] for s in ss]
 print(name,'relative reduction range',round(min(vals),4),round(max(vals),4),'order3 gain range',round(min(gain),4),round(max(gain),4))
