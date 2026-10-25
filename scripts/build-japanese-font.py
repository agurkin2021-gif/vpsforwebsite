#!/usr/bin/env python3
"""Subset the pinned Noto Sans JP source and outline localized CTA text.

Requires fonttools[woff] and the upstream variable TTF passed as an argument.
See static/fonts/noto-sans-jp/README.md for provenance and reproduction.
"""
from pathlib import Path
import argparse
import hashlib
import json
import xml.etree.ElementTree as ET
from fontTools import subset
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

ROOT = Path(__file__).resolve().parents[1]
SOURCE_SHA256 = 'c2f3b4d463500a2ddcd3849cded1fceeb9fd6d1c32e6cbecd568453ba50fc68f'


def build(source):
    assert hashlib.sha256(source.read_bytes()).hexdigest() == SOURCE_SHA256, 'Unexpected upstream font'
    paths = list((ROOT / 'content/japanese').rglob('*.md')) + [ROOT / p for p in (
        'i18n/ja.yaml', 'config/_default/menus.ja.toml', 'layouts/404.ja.html')]
    labels = ['VPS構成を選ぶ', '実測データから選ぶ', '負荷を測定 → 余裕を確保 → 契約']
    text = ''.join(p.read_text(encoding='utf-8') for p in paths) + ''.join(labels)
    chars = {ord(c) for c in text if ord(c) >= 32} | set(range(32, 127))
    font = TTFont(source)
    missing = sorted(chars - set(font.getBestCmap()))
    assert not missing, ['Missing glyph', *map(hex, missing)]
    options = subset.Options()
    options.flavor = 'woff2'
    options.layout_features = ['*']
    options.name_IDs = ['*']
    options.name_legacy = True
    options.name_languages = ['*']
    job = subset.Subsetter(options=options)
    job.populate(unicodes=chars)
    job.subset(font)
    font.flavor = 'woff2'
    font.recalcTimestamp = False
    output = ROOT / 'static/fonts/noto-sans-jp/NotoSansJP-site.woff2'
    font.save(output)
    assert not chars - set(TTFont(output).getBestCmap()), 'Subset lost used glyphs'

    # External SVG images cannot inherit a document's @font-face. Outlined text
    # keeps the original CTA geometry portable on devices without Japanese fonts.
    svg = (ROOT / 'static/images/home/vps-cta.svg').read_text(encoding='utf-8')
    for old, new in zip(['Choose a VPS configuration', 'Choose from evidence', 'workload → headroom → buy'], labels):
        svg = svg.replace(old, new)
    ET.register_namespace('', 'http://www.w3.org/2000/svg')
    tree = ET.fromstring(svg)
    tag = '{http://www.w3.org/2000/svg}'
    faces = {}
    for element in list(tree):
        if element.tag != tag + 'text':
            continue
        weight = int(element.get('font-weight', '400'))
        if weight not in faces:
            faces[weight] = instantiateVariableFont(TTFont(output), {'wght': weight})
        face = faces[weight]
        glyphs = face.getGlyphSet()
        cmap = face.getBestCmap()
        label = element.text or ''
        scale = float(element.get('font-size')) / face['head'].unitsPerEm
        width = sum(glyphs[cmap[ord(c)]].width for c in label) * scale
        assert width < 440 if float(element.get('y')) == 145 else width < 374, (label, width)
        x = float(element.get('x')) - width / 2
        y = float(element.get('y'))
        pen = SVGPathPen(glyphs)
        for char in label:
            glyph = glyphs[cmap[ord(char)]]
            glyph.draw(TransformPen(pen, (scale, 0, 0, -scale, x, y)))
            x += glyph.width * scale
        element.tag = tag + 'path'
        element.attrib.clear()
        element.set('d', pen.getCommands())
        element.set('fill', '#000')
        element.set('aria-label', label)
        element.text = None
    (ROOT / 'static/images/home/vps-cta-ja.svg').write_text(ET.tostring(tree, encoding='unicode') + '\n', encoding='utf-8')
    print(json.dumps({'font_bytes': output.stat().st_size, 'glyphs': len(font.getBestCmap()),
                      'sha256': hashlib.sha256(output.read_bytes()).hexdigest(), 'missing_used_glyphs': 0}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source_ttf', type=Path)
    build(parser.parse_args().source_ttf)
