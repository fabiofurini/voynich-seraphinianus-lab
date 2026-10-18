import re,json,collections,pathlib,zipfile
root=pathlib.Path(__file__).resolve().parent.parent
blocks={};key=None
for l in (root/'seraph_ocr/CS_OCR_TRANSLITERATION.txt').read_text().splitlines():
 m=re.match(r'#\s+cs-(\d+)-(\d+\.\d+)',l)
 if m:key=(m[1],m[2]);blocks[key]=[]
 elif l.strip() and not l.startswith('#') and key:blocks[key].append(l.split())
def lev(a,b):
 d=list(range(len(b)+1))
 for i,x in enumerate(a,1):
  n=[i]
  for j,y in enumerate(b,1):n.append(min(n[-1]+1,d[j]+1,d[j-1]+(x!=y)))
  d=n
 return d[-1]
records=[]
for l in (root/'seraph_ocr/CS_DB/gt/words.txt').read_text().splitlines():
 if '.AAA_' not in l:continue
 m=re.match(r'(\S*cs(\d+)-(\d+\.\d+)-L(\d+)\.(\d+)\.AAA_\S+) .*? NN (.*)',l)
 if not m:continue
 ident,page,block,line,word,truth=m.groups();lines=blocks.get((page,block),[]);i=int(line)-1;j=int(word)-1
 if i>=len(lines) or j>=len(lines[i]):records.append(dict(id=ident,status='out_of_range',truth=truth));continue
 pred=lines[i][j];distance=lev(truth,pred)
 records.append(dict(id=ident,status='aligned_position',page=page,block=block,line=i+1,word=j+1,truth=truth,pred=pred,edit=distance,exact=truth==pred,multiword=len(truth.split())>1,nearby_exact=truth in lines[i][max(0,j-2):j+3]))
aligned=[r for r in records if r['status']=='aligned_position'];single=[r for r in aligned if not r['multiword']]
summary={'AAA_labels':len(records),'position_available':len(aligned),'single_word_labels':len(single),'exact_single':sum(r['exact'] for r in single),'exact_single_fraction':sum(r['exact'] for r in single)/len(single),'CER_single_position':sum(r['edit'] for r in single)/sum(len(r['truth']) for r in single),'nearby_exact_single':sum(r['nearby_exact'] for r in single),'caveat':'Training labels, not independent ground truth. Fixed positional comparison is contaminated by OCR segmentation shifts; CER is positional disagreement, not validated OCR error rate.'}
(root/'grammar_comparison/ocr_audit_results.json').write_text(json.dumps({'summary':summary,'records':records},indent=2));print(json.dumps(summary,indent=2));print('examples',json.dumps(single[:10],indent=2))
# Extract original labelled crops for visual inspection, no augments
examples=[]
for r in single:
 if len(examples)>=12:break
 zpath=root/'seraph_ocr/CS_DB/img'/(r['id'].split('-')[0]+'.zip')
 if not zpath.exists():continue
 with zipfile.ZipFile(zpath) as z:
  names=[n for n in z.namelist() if n.endswith('/'+r['id']+'.png')]
  if names:
   from PIL import Image,ImageDraw
   import io
   im=Image.open(io.BytesIO(z.read(names[0]))).convert('RGB');examples.append((r,im))
from PIL import Image,ImageDraw
canvas=Image.new('RGB',(1000,max(1,len(examples))*115),'white');draw=ImageDraw.Draw(canvas)
for k,(r,im) in enumerate(examples):
 im.thumbnail((400,75));canvas.paste(im,(10,k*115+25));draw.text((430,k*115+30),'label: '+r['truth']+' | OCR: '+r['pred'],fill='black');draw.text((10,k*115+5),r['id'],fill='black')
canvas.save(root/'grammar_comparison/ocr_audit_samples.png')
