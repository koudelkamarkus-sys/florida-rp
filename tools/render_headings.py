"""Render complete fixed Pricedown heading compositions, never a webfont.
Usage: python tools/render_headings.py /path/to/Pricedown.otf
Requires fonttools. Font remains on the local workstation, not in this repository.
"""
import sys,re,html
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.transformPen import TransformPen
root=Path(__file__).resolve().parent.parent
font=TTFont(sys.argv[1]);glyphs=font.getGlyphSet();cmap=font.getBestCmap();metrics=font['hmtx'].metrics
page=root/'dist/index.html';source=page.read_text(encoding='utf-8')
# Only initial conversion edits HTML. Rerun from stored heading manifest afterward.
import json
manifest=root/'tools/heading-text.json'
if manifest.exists() and 'class="heading-art"' in source:items=json.loads(manifest.read_text())
else:
 items=[]
 def replace(m):
  tag,attrs,body=m.groups();plain=html.unescape(re.sub('<[^>]+>',' ',body)).strip()
  lines=[html.unescape(re.sub('<[^>]+>','',s)).strip() for s in re.split(r'<br\s*/?>',body)]
  if tag=='1':lines=['Florida.','Your way.']
  key=f'heading-{len(items)+1}';items.append({'file':key,'lines':lines,'hero':tag=='1','text':plain})
  return f'<h{tag}{attrs} class="pricedown-heading"><span class="heading-accessible">{html.escape(plain)}</span><img class="heading-art" src="headings/{key}.svg" alt="" aria-hidden="true" decoding="async"></h{tag}>'
 source=re.sub(r'<h([12])([^>]*)>(.*?)</h\1>',replace,source,flags=re.S)
 manifest.write_text(json.dumps(items,indent=2),encoding='utf-8');page.write_text(source,encoding='utf-8')
for item in items:
 item['text']=' '.join(item['lines'])
 paths=[];allbounds=[];baseline=0
 for index,text in enumerate(item['lines']):
  x=0;pen=SVGPathPen(glyphs);bounds=[]
  for ch in text.upper():
   name=cmap.get(ord(ch));
   if not name:continue
   glyph=glyphs[name];tp=TransformPen(pen,(1,0,0,-1,x,baseline));glyph.draw(tp)
   bp=BoundsPen(glyphs);glyph.draw(TransformPen(bp,(1,0,0,-1,x,baseline)))
   if bp.bounds:bounds.append(bp.bounds)
   x+=metrics[name][0]
  if not bounds:continue
  bb=(min(b[0] for b in bounds),min(b[1] for b in bounds),max(b[2] for b in bounds),max(b[3] for b in bounds));allbounds.append(bb)
  color='#93c5f2' if item['hero'] and index==1 else '#edf4ff'
  paths.append(f'<path fill="{color}" d="{pen.getCommands()}"/>')
  baseline+=max(1,bb[3]-bb[1])*1.24
 left=min(b[0] for b in allbounds)-8;top=min(b[1] for b in allbounds)-8;right=max(b[2] for b in allbounds)+8;bottom=max(b[3] for b in allbounds)+8
 svg=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{left} {top} {right-left} {bottom-top}" role="presentation">'+''.join(paths)+'</svg>'
 (root/'dist/headings'/f"{item['file']}.svg").write_text(svg,encoding='utf-8')
# Update one heading at a time. A replacement must never span section boundaries.
lookup={item['file']:item for item in items}
def synchronize(m):
 tag,attrs,body=m.groups()
 asset=re.search(r'src="headings/(heading-\d+)\.svg"',body)
 if not asset:return m.group(0)
 item=lookup[asset.group(1)]
 body=re.sub(r'<span class="heading-accessible">[^<]*</span>',lambda _: '<span class="heading-accessible">'+html.escape(item['text'])+'</span>',body,count=1)
 return '<h'+tag+attrs+'>'+body+'</h'+tag+'>'
source=re.sub(r'<h([12])([^>]*)>(.*?)</h\1>',synchronize,source,flags=re.S)
page.write_text(source,encoding='utf-8')
manifest.write_text(json.dumps(items,indent=2),encoding='utf-8')
print(f"Rendered {len(items)} complete heading graphics. No font embedded.")
