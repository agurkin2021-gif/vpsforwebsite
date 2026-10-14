#!/usr/bin/env python3
"""Audit one Hugo localization without changing source files.

Usage:
  python3 scripts/translation_audit.py content/english/_index.md content/spanish/_index.md
  python3 scripts/translation_audit.py content/english/_index.md content/spanish/_index.md --json
Exit 0: structural checks passed; exit 1: differences requiring review.
Requires Python 3.10+, standard library only.
"""
import argparse
from collections import Counter
import json
from pathlib import Path
import re
import sys

AFFILIATE = re.compile(r'https?://[^\s\\"\'<>)]*(?:partner=|affiliate=|ref=)[^\s\\"\'<>)]*', re.I)
HTML_HREF = re.compile(r'\bhref\s*=\s*([\\"\'])(.*?)\1', re.I)
MARKDOWN_LINK = re.compile(r'(?<!!)\[[^\]]+\]\(([^)]+)\)')
IMAGE = re.compile(r'!\[[^\]]*\]\(([^)]+)\)|\b(?:src|image):?\s*[= ]\s*[\\"\']([^\\"\']+)', re.I)
RELREF = re.compile(r'\{\{<\s*relref\s+\\"([^\\"]+)\\"\s*>\}\}')
ID = re.compile(r'\bid\s*=\s*([\\"\'])(.*?)\1')
SCRIPT = re.compile(r'<script\b[^>]*>(.*?)</script>', re.I | re.S)
HTML_TAG = re.compile(r'</?([a-z][\w-]*)\b', re.I)
PRICE = re.compile(r'\$\d+(?:\.\d+)?(?:/(?:day|month|year))?', re.I)
NUMBER_UNIT = re.compile(r'\b\d+(?:\.\d+)?\s*(?:vCPU|GB|TB|Gbit/s|MHz)\b', re.I)
MD_HEADING = re.compile(r'^(#{1,6})\s+', re.M)
TABLE_ROW = re.compile(r'^\|.*\|\s*$', re.M)
YAML_KEY = re.compile(r'^(\s*)(?:-\s*)?([a-zA-Z_][\w-]*):(?:\s|$)')
TEXT_KEYS = {'title','description','content','label','intro','button','initial','checked','fit','warning','note','question','answer','affiliate_label'}

def counter(pattern, value, group=0):
    return Counter(m.group(group) for m in pattern.finditer(value))

def yaml_shape(text):
    shape = []
    for line in text.splitlines():
        m = YAML_KEY.match(line)
        if m:
            shape.append((len(m.group(1)), m.group(2)))
    return shape

def report(source, target):
    errors, warnings = [], []
    def equal(name, left, right):
        if left != right:
            errors.append({'check':name,'source':left,'translation':right})
    def counts(name, pattern, group=0):
        a,b=counter(pattern,source,group),counter(pattern,target,group)
        equal(name,dict(a),dict(b))
    counts('affiliate_urls',AFFILIATE)
    counts('html_href',HTML_HREF,2)
    counts('hugo_relref_targets',RELREF,1)
    counts('html_ids',ID,2)
    counts('image_paths',IMAGE)
    counts('prices',PRICE)
    counts('numbered_specs',NUMBER_UNIT)
    counts('html_tags',HTML_TAG,1)
    equal('markdown_heading_levels',dict(counter(MD_HEADING,source,1)),dict(counter(MD_HEADING,target,1)))
    equal('markdown_table_rows',len(TABLE_ROW.findall(source)),len(TABLE_ROW.findall(target)))
    equal('markdown_link_count',len(MARKDOWN_LINK.findall(source)),len(MARKDOWN_LINK.findall(target)))
    equal('script_block_count',len(SCRIPT.findall(source)),len(SCRIPT.findall(target)))
    # Script logic must remain intact except for user-facing strings; compare skeleton.
    def js_skeleton(block):
        block=re.sub(r'([\\"\'])(?:\\\\.|(?!\1).)*?\1','STRING',block)
        return re.sub(r'\s+','',block)
    if len(SCRIPT.findall(source))==len(SCRIPT.findall(target)):
        for i,(a,b) in enumerate(zip(SCRIPT.findall(source),SCRIPT.findall(target)),1):
            if js_skeleton(a)!=js_skeleton(b):
                warnings.append(f'Script {i}: inspect logic manually; text-only changes expected')
    if source.startswith('---\n') and target.startswith('---\n'):
        sa=source.split('---',2)[1]
        ta=target.split('---',2)[1]
        equal('frontmatter_yaml_key_shape',yaml_shape(sa),yaml_shape(ta))
        # Count list items, not literal wording.
        equal('frontmatter_list_items',len(re.findall(r'^\s+- ',sa,re.M)),len(re.findall(r'^\s+- ',ta,re.M)))
    else:
        errors.append({'check':'frontmatter','source':'expected YAML delimiters','translation':'missing'})
    if source.count('partner=ni8gzrvz75')!=target.count('partner=ni8gzrvz75'):
        errors.append({'check':'VDSina affiliate occurrence count','source':source.count('partner=ni8gzrvz75'),'translation':target.count('partner=ni8gzrvz75')})
    if source==target:
        warnings.append('Translation is byte-identical to English; check language')
    warnings.append('Automated checks do not prove natural Spanish, correct SEO intent, browser rendering or working deployment')
    return {'passed':not errors,'errors':errors,'warnings':warnings,'source_lines':len(source.splitlines()),'translation_lines':len(target.splitlines())}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('source',type=Path)
    p.add_argument('translation',type=Path)
    p.add_argument('--json',action='store_true')
    a=p.parse_args()
    result=report(a.source.read_text(encoding='utf-8'),a.translation.read_text(encoding='utf-8'))
    if a.json: print(json.dumps(result,ensure_ascii=False,indent=2))
    else:
        print('PASS' if result['passed'] else 'FAIL')
        for e in result['errors']: print('ERROR',json.dumps(e,ensure_ascii=False))
        for w in result['warnings']: print('WARN',w)
    return 0 if result['passed'] else 1

if __name__=='__main__': sys.exit(main())
