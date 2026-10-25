#!/usr/bin/env python3
"""Build Turkish subsets of the existing design families and outline CTA labels.

Requires fonttools[woff]; pass a directory containing the pinned upstream TTFs.
See assets/fonts/turkish-README.md for source URLs, hashes and licenses.
"""
from pathlib import Path
import argparse,hashlib,json,xml.etree.ElementTree as ET
from fontTools import subset
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

ROOT=Path(__file__).resolve().parents[1]
FONTS={
 'inter':('Inter[opsz,wght].ttf','29160a80ff49ddcab2c97711247e08b1fab27a484a329ce8b813d820dc559031',{'opsz':14,'wght':(400,400,700)}),
 'fraunces':('Fraunces[SOFT,WONK,opsz,wght].ttf','177ff6c0f14e5550a3c624247cd1189611d4eb65d000b14944c63d967958abbb',{'opsz':9,'SOFT':0,'WONK':1,'wght':(600,700,700)}),
}
TURKISH=set(map(ord,'ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZabcçdefgğhıijklmnoöprsştuüvyz'))

def build(source_dir):
 report={}
 for family,(name,sha,axes) in FONTS.items():
  source=source_dir/name
  assert hashlib.sha256(source.read_bytes()).hexdigest()==sha,'Unexpected upstream '+family
  original=TTFont(ROOT/f'assets/fonts/{family}-latin.woff2')
  chars=set(original.getBestCmap())|TURKISH|{0x2192}
  font=TTFont(source)
  # The arrow is needed only by the CTA's Inter labels.
  if family=='fraunces':chars.discard(0x2192)
  missing=chars-set(font.getBestCmap());assert not missing,(family,list(map(hex,missing)))
  options=subset.Options();options.flavor='woff2';options.layout_features=['*']
  options.name_IDs=['*'];options.name_legacy=True;options.name_languages=['*']
  job=subset.Subsetter(options=options);job.populate(unicodes=chars);job.subset(font)
  font=instantiateVariableFont(font,axes)
  font.flavor='woff2';font.recalcTimestamp=False
  output=ROOT/f'assets/fonts/{family}-turkish.woff2';font.save(output)
  assert not TURKISH-set(TTFont(output).getBestCmap()),'Missing Turkish letters'
  report[family]={'bytes':output.stat().st_size,'glyphs':len(font.getBestCmap()),'sha256':hashlib.sha256(output.read_bytes()).hexdigest()}
 labels=['VPS yapılandırması seçin','Ölçümlere göre seçin','İş yükü → kapasite payı → seçim']
 svg=(ROOT/'static/images/home/vps-cta.svg').read_text(encoding='utf-8')
 for old,new in zip(['Choose a VPS configuration','Choose from evidence','workload → headroom → buy'],labels):svg=svg.replace(old,new)
 ET.register_namespace('','http://www.w3.org/2000/svg');tree=ET.fromstring(svg);tag='{http://www.w3.org/2000/svg}'
 for element in list(tree):
  if element.tag!=tag+'text':continue
  face=instantiateVariableFont(TTFont(ROOT/'assets/fonts/inter-turkish.woff2'),{'wght':int(element.get('font-weight','400'))})
  glyphs=face.getGlyphSet();cmap=face.getBestCmap();label=element.text or ''
  scale=float(element.get('font-size'))/face['head'].unitsPerEm
  width=sum(glyphs[cmap[ord(c)]].width for c in label)*scale
  assert width<(440 if float(element.get('y'))==145 else 374),(label,width)
  x=float(element.get('x'))-width/2;y=float(element.get('y'));pen=SVGPathPen(glyphs)
  for char in label:
   glyph=glyphs[cmap[ord(char)]];glyph.draw(TransformPen(pen,(scale,0,0,-scale,x,y)));x+=glyph.width*scale
  element.tag=tag+'path';element.attrib.clear();element.set('d',pen.getCommands());element.set('fill','#000');element.set('aria-label',label);element.text=None
 (ROOT/'static/images/home/vps-cta-tr.svg').write_text(ET.tostring(tree,encoding='unicode')+'\n',encoding='utf-8')
 print(json.dumps(report,indent=2))

if __name__=='__main__':
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('source_dir',type=Path);build(parser.parse_args().source_dir)
