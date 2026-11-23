"""Rebuild the illustrative input fixture from authoritative publisher JATS.
No model results or expected outcomes are fetched or presented as chain state.
"""
from urllib.request import urlopen
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import subprocess, sys
papers=[('QAB','10.1371/journal.pone.0192773'),('RAT','10.1371/journal.pone.0258946'),('REVIEW','10.1371/journal.pone.0194143'),('qab-notice','10.1371/journal.pone.0199469')]
def fetch(item):
 sid,doi=item
 with urlopen('https://journals.plos.org/plosone/article/file?id='+doi+'&type=manuscript',timeout=60) as response:raw=response.read()
 Path('/tmp/'+sid+'.xml').write_bytes(raw)
 return sid
with ThreadPoolExecutor(max_workers=4) as pool:
 for sid in pool.map(fetch,papers):print('Retrieved',sid)
subprocess.run([sys.executable,'scripts/build-fixture.py'],check=True)
