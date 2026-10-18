"""Download locally, verify exact bytes, never silently substitute source versions."""
from pathlib import Path
import urllib.request,json,hashlib,sys
R=Path(__file__).resolve().parent.parent
for e in json.loads((R/'DATA_SOURCES.json').read_text()):
 if e.get('optional') and e['optional'] not in sys.argv:continue
 p=R/e['path'];p.parent.mkdir(parents=True,exist_ok=True)
 bb=p.read_bytes() if p.exists() else urllib.request.urlopen(e['url'],timeout=60).read()
 if hashlib.sha256(bb).hexdigest()!=e['sha256']:raise SystemExit('SOURCE HASH MISMATCH: '+e['path'])
 p.write_bytes(bb);print('Verified:',e['path'])
 if e['path'].endswith('patterns/voynich_ZL3b.txt'):
  q=R/'research/substitution_attack/sources/voynich_ZL3b.txt';q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(bb)
