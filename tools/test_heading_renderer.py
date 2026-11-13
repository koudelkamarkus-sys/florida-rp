"""Regression check for fixed heading rendering; requires a local licensed font.
Usage: python tools/test_heading_renderer.py /path/to/Pricedown.otf
"""
from pathlib import Path
import tempfile,shutil,subprocess,sys,re,json
from html.parser import HTMLParser
root=Path(__file__).resolve().parent.parent
class Page(HTMLParser):
 def __init__(self,s):super().__init__();self.ids=set();self.counts={};self.feed(s)
 def handle_starttag(self,tag,attrs):
  self.counts[tag]=self.counts.get(tag,0)+1
  for k,v in attrs:
   if k=='id':self.ids.add(v)
with tempfile.TemporaryDirectory() as td:
 stage=Path(td);(stage/'tools').mkdir();(stage/'dist/headings').mkdir(parents=True)
 for name in ['render_headings.py','heading-text.json']:shutil.copy2(root/'tools'/name,stage/'tools'/name)
 shutil.copy2(root/'dist/index.html',stage/'dist/index.html')
 original=(stage/'dist/index.html').read_text(encoding='utf-8');before=Page(original)
 required={'home','community','scenarios','membership','faq'};assert required<=before.ids
 for _ in range(2):
  subprocess.run([sys.executable,str(stage/'tools/render_headings.py'),str(Path(sys.argv[1]).resolve())],check=True,capture_output=True)
  actual=(stage/'dist/index.html').read_text(encoding='utf-8');after=Page(actual)
  assert before.ids==after.ids,'Section or control IDs were removed'
  assert before.counts==after.counts,'Page elements were lost'
  assert actual==original,'Unchanged heading rerun changed page content'
 # Edit a middle heading; its new text must not consume earlier/later sections.
 manifest=stage/'tools/heading-text.json';items=json.loads(manifest.read_text());items[2]['lines']=['Same streets.','Another story.'];manifest.write_text(json.dumps(items))
 subprocess.run([sys.executable,str(stage/'tools/render_headings.py'),str(Path(sys.argv[1]).resolve())],check=True,capture_output=True)
 actual=(stage/'dist/index.html').read_text(encoding='utf-8');after=Page(actual)
 expected=original.replace('Same streets. A different story.</span>','Same streets. Another story.</span>')
 assert actual==expected,'A heading edit changed unrelated page content'
 assert before.ids==after.ids and before.counts==after.counts
 assert before.counts['h1']==1 and before.counts['h2']==6
 print('PASS: repeated render is identical; middle-heading edit preserves every section and control.')
