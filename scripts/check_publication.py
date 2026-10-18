from pathlib import Path
import json,re,ast
R=Path(__file__).resolve().parent.parent
for p in R.rglob('*.py'):ast.parse(p.read_text(),filename=str(p))
for p in R.rglob('*.json'):json.loads(p.read_text())
html=(R/'docs/index.html').read_text();ids=re.findall(r'\bid="([^"]+)"',html)
assert len(ids)==len(set(ids)),'Duplicate HTML IDs'
for target in re.findall(r'(?:href|src)="([^"]+)"',html):
 if target.startswith('#'):
  assert target=='#' or target[1:] in ids,target
 elif not target.startswith(('https:','http:','data:','mailto:')):
  assert (R/'docs'/target).exists(),target
forbidden=['voynich_mail_attachments','@gmail.com','@lix.polytechnique.fr','ANGjdJ','base64_url_content','browserAuth']
for p in R.rglob('*'):
 if not p.is_file() or '.git' in p.parts:continue
 if p.name=='check_publication.py':continue
 if p.suffix in ['.py','.md','.json','.html','.js','.yml','.txt']:
  s=p.read_text(errors='ignore')
  for f in forbidden:assert f not in s,(p,f)
assert not (R/'research/seraph_ocr/CS_OCR_TRANSLITERATION.txt').exists(),'Raw copyrighted source accidentally included'
print('Public snapshot checks passed: syntax, JSON, internal links, IDs and private-data exclusions.')
