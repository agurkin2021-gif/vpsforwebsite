#!/usr/bin/env python3
"""Validate a localized Hugo page against its English source.

Usage:
 python scripts/check_translation.py content/english/vps-for-wordpress.md content/spanish/vps-for-wordpress.md
"""
import collections
import pathlib
import re
import sys

AFFILIATE = re.compile(r'https?://[^\s"<>)]*(?:partner=|ref=|affiliate=)[^\s"<>)]*', re.I)
HREF = re.compile(r'\bhref\s*=\s*["\']([^"\']+)["\']', re.I)
SHORTCODE = re.compile(r'\{\{<\s*relref\s+"([^"]+)"\s*>\}\}')
ID = re.compile(r'\bid\s*=\s*["\']([^"\']+)["\']')
PRICE = re.compile(r'\$\d+(?:\.\d+)?(?:/\w+)?')
SPEC = re.compile(r'\b\d+\s*(?:vCPU|GB|TB|Gbit/s|MHz)\b', re.I)
SCRIPT = re.compile(r'<script\b[^>]*>(.*?)</script>', re.I | re.S)
HTML_TAG = re.compile(r'</?([a-z][a-z0-9-]*)\b', re.I)
HEADING = re.compile(r'^(#{1,6})\s+', re.M)
TABLE = re.compile(r'^\|.*\|\s*$', re.M)
LINK = re.compile(r'\]\(([^)]+)\)')
FAQ = re.compile(r'^###\s+', re.M)

def check(source, target):
    errors = []
    def same(label, regex, *, exact=True):
        a, b = regex.findall(source), regex.findall(target)
        if exact and collections.Counter(a) != collections.Counter(b):
            errors.append(f'{label}: source={dict(collections.Counter(a))}; target={dict(collections.Counter(b))}')
        elif not exact and len(a) != len(b):
            errors.append(f'{label} count: {len(a)} vs {len(b)}')
    same('Affiliate URLs', AFFILIATE)
    same('HTML link destinations', HREF)
    same('Hugo relref targets', SHORTCODE)
    same('HTML IDs', ID)
    same('Prices', PRICE)
    same('Technical specs', SPEC)
    same('HTML tag structure', HTML_TAG)
    same('Heading levels', HEADING)
    same('Table rows', TABLE, exact=False)
    same('Markdown links', LINK, exact=False)
    same('FAQ subsections', FAQ, exact=False)
    if len(SCRIPT.findall(source)) != len(SCRIPT.findall(target)):
        errors.append('JavaScript block count differs')
    if 'partner=ni8gzrvz75' in source and 'partner=ni8gzrvz75' not in target:
        errors.append('VDSina affiliate identifier lost')
    if source.count('---') >= 2 and target.count('---') < 2:
        errors.append('Front matter missing')
    return errors

def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    source = pathlib.Path(sys.argv[1]).read_text(encoding='utf-8')
    target = pathlib.Path(sys.argv[2]).read_text(encoding='utf-8')
    errors = check(source, target)
    if errors:
        print('TRANSLATION CHECK FAILED')
        for error in errors:
            print(' -', error)
        return 1
    print('Structural checks passed. Human linguistic and rendered-site review still required.')
    return 0

if __name__ == '__main__':
    sys.exit(main())
