#!/usr/bin/env python3
"""Audit complete Italian source coverage and rendered SEO/interactive parity.

Run after a production Hugo build: python scripts/audit-italian.py public
Uses only Python's standard library; does not rewrite translations or outputs.
"""
import argparse
from collections import Counter
from html.parser import HTMLParser
import importlib.util
import json
from pathlib import Path
import re
from urllib.parse import unquote, urljoin, urlsplit

PROJECT = Path(__file__).resolve().parents[1]
ORIGIN = 'https://vpsforwebsite.com'
PARTNER = 'https://www.vdsina.com/?partner=ni8gzrvz75'


def route(path, text, language):
    front = text.split('---', 2)[1]
    explicit = re.search(r'^url:\s*"([^"]+)"', front, re.M)
    if explicit:
        return explicit[1]
    slug = re.search(r'^slug:\s*"([^"]+)"', front, re.M)
    tail = slug[1] if slug else str(path.with_suffix('')).replace('\\', '/')
    tail = tail.removesuffix('/_index')
    if tail == '_index':
        tail = ''
    return ('/it/' if language == 'it' else '/') + (tail + '/' if tail else '')


class Document(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.tags = Counter()
        self.headings = []
        self.forms = []
        self.options = []
        self.inputs = []
        self.anchors = []
        self.ids = []
        self.title = ''
        self.h1 = ''
        self.h1_count = 0
        self.lang = ''
        self.canonical = []
        self.hreflang = []
        self.robots = ''
        self.description = ''
        self.feed(text)

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        if tag not in ('area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr'):
            self.stack.append(tag)
        if tag == 'html':
            self.lang = attrs.get('lang', '')
        if tag == 'link' and attrs.get('rel') == 'canonical':
            self.canonical.append(attrs.get('href', ''))
        if tag == 'link' and attrs.get('hreflang'):
            self.hreflang.append((attrs['hreflang'], attrs.get('href', '')))
        if tag == 'meta':
            if attrs.get('name') == 'robots':
                self.robots = attrs.get('content', '')
            if attrs.get('name') == 'description':
                self.description = attrs.get('content', '')
        if attrs.get('id'):
            self.ids.append(attrs['id'])
        if tag == 'a':
            self.anchors.append(attrs)
        if 'main' in self.stack:
            self.tags[tag] += 1
            if tag in ('h2', 'h3') and attrs.get('id'):
                self.headings.append(attrs['id'])
            if tag == 'h1':
                self.h1_count += 1
            if tag == 'form':
                self.forms.append(attrs.get('id'))
            if tag == 'option':
                self.options.append(attrs.get('value'))
            if tag in ('select', 'input'):
                self.inputs.append({k: attrs.get(k) for k in ('id', 'name', 'type', 'value', 'min', 'max', 'step', 'required')})

    def handle_endtag(self, tag):
        if tag in self.stack:
            self.stack = self.stack[:len(self.stack) - 1 - self.stack[::-1].index(tag)]

    def handle_data(self, data):
        if 'title' in self.stack and 'head' in self.stack:
            self.title += data
        if 'h1' in self.stack:
            self.h1 += data


def audit(build):
    spec = importlib.util.spec_from_file_location('translation_audit', PROJECT / 'scripts/translation_audit.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    english = PROJECT / 'content/english'
    italian = PROJECT / 'content/italian'
    sources = sorted(p.relative_to(english) for p in english.rglob('*.md'))
    targets = sorted(p.relative_to(italian) for p in italian.rglob('*.md'))
    errors, records, exceptions = [], [], []
    if sources != targets:
        errors.append({'source_coverage': {'missing': [str(p) for p in set(sources) - set(targets)], 'extra': [str(p) for p in set(targets) - set(sources)]}})
    forms = 0
    routes = []
    for rel in sources:
        if not (italian / rel).is_file():
            continue
        en = (english / rel).read_text(encoding='utf-8')
        it = (italian / rel).read_text(encoding='utf-8')
        # Only explicit, meaning-preserving localization exceptions are normalized.
        de_normalized = re.sub(r'^(?:slug|url):.*\n', '', it, flags=re.M)
        de_normalized = de_normalized.replace('/giorno', '/day').replace('/mese', '/month').replace('/anno', '/year')
        de_normalized = de_normalized.replace('images/home/vps-cta-it.svg', 'images/home/vps-cta.svg')
        if rel.as_posix() == 'vps-sizing-for-website.md':
            # One IT-only accessibility hint accompanies the mobile scroll wrapper.
            de_normalized = re.sub(r'<p class="vps-table-scroll-hint">[^<]+</p>\n?', '', de_normalized)
        result = module.report(en, de_normalized)
        for error in result['errors']:
            errors.append({'page': str(rel), **error})
        # These source structures must not be shortened or padded.
        en_body, de_body = en.split('---', 2)[2], it.split('---', 2)[2]
        for name, pattern in [('bullets', r'^\s*[-*] '), ('numbered_items', r'^\s*\d+\. '), ('code_fences', r'^```')]:
            if len(re.findall(pattern, en_body, re.M)) != len(re.findall(pattern, de_body, re.M)):
                errors.append({'page': str(rel), 'check': name})
        if en == it:
            errors.append({'page': str(rel), 'check': 'untranslated_source'})
        if rel.parts[0] == 'sections':
            continue
        en_route, de_route = route(rel, en, 'en'), route(rel, it, 'it')
        routes.append({'source': str(rel).replace('\\', '/'), 'en': en_route, 'it': de_route})
        en_file = build / en_route.strip('/') / 'index.html'
        de_file = build / de_route.strip('/') / 'index.html'
        if not en_file.is_file() or not de_file.is_file():
            errors.append({'page': str(rel), 'check': 'missing_rendered_page', 'it': de_route})
            continue
        ed, dd = Document(en_file.read_text(encoding='utf-8')), Document(de_file.read_text(encoding='utf-8'))
        expected_title = re.search(r'^title:\s*"([^"]+)"', it, re.M)[1]
        if dd.lang.split('-')[0] != 'it' or dd.title.strip() != expected_title or dd.h1.strip() != expected_title or dd.h1_count != 1:
            errors.append({'page': de_route, 'check': 'lang_title_h1', 'title': dd.title, 'h1': dd.h1, 'lang': dd.lang})
        expected_noindex = rel.parts[0] == 'contact'
        if dd.canonical != [ORIGIN + de_route] and not (expected_noindex and not dd.canonical):
            errors.append({'page': de_route, 'check': 'canonical', 'actual': dd.canonical})
        if not dd.description or dd.description == ed.description:
            errors.append({'page': de_route, 'check': 'description'})
        if ('noindex' in dd.robots) != expected_noindex:
            errors.append({'page': de_route, 'check': 'robots', 'actual': dd.robots})
        if not expected_noindex:
            hfl = dict(dd.hreflang)
            if len(hfl) != len(dd.hreflang) or hfl.get('it') != ORIGIN + de_route or hfl.get('en') != ORIGIN + en_route or hfl.get('x-default') != ORIGIN + en_route:
                errors.append({'page': de_route, 'check': 'hreflang', 'actual': dd.hreflang})
        if len(dd.ids) != len(set(dd.ids)):
            errors.append({'page': de_route, 'check': 'duplicate_ids'})
        for key in ('forms', 'options', 'inputs'):
            if getattr(ed, key) != getattr(dd, key):
                errors.append({'page': de_route, 'check': key})
        forms += len(dd.forms)
        # About/Contact source bodies were historically hidden in EN, deliberately rendered in DE.
        if rel.parts[0] not in ('about', 'contact'):
            for tag in ('h2', 'h3', 'li', 'table', 'tr', 'th', 'td', 'form', 'select', 'option'):
                if ed.tags[tag] != dd.tags[tag]:
                    errors.append({'page': de_route, 'check': 'rendered_' + tag, 'en': ed.tags[tag], 'it': dd.tags[tag]})
            if ed.headings != dd.headings:
                errors.append({'page': de_route, 'check': 'heading_anchors', 'en': ed.headings, 'it': dd.headings})
        en_aff = [a for a in ed.anchors if a.get('href') == PARTNER]
        de_aff = [a for a in dd.anchors if a.get('href') == PARTNER]
        if len(en_aff) != len(de_aff):
            errors.append({'page': de_route, 'check': 'rendered_affiliate_count', 'en': len(en_aff), 'it': len(de_aff)})
        for a in de_aff:
            if not {'sponsored', 'nofollow', 'noopener'}.issubset(a.get('rel', '').split()):
                errors.append({'page': de_route, 'check': 'affiliate_attributes'})
        for a in dd.anchors:
            raw = a.get('href') or ''
            if raw.startswith('//'):
                errors.append({'page': de_route, 'check': 'protocol_relative_link', 'href': raw})
                continue
            u = urlsplit(urljoin(ORIGIN + de_route, raw))
            if u.netloc != 'vpsforwebsite.com' or u.scheme not in ('http', 'https'):
                continue
            local = build / unquote(u.path).lstrip('/')
            if not local.suffix:
                local = local / 'index.html'
            if not local.is_file():
                errors.append({'page': de_route, 'check': 'missing_internal_link', 'href': raw})
            elif u.fragment:
                dest = Document(local.read_text(encoding='utf-8'))
                if unquote(u.fragment) not in dest.ids:
                    errors.append({'page': de_route, 'check': 'missing_anchor', 'href': raw})
        records.append({'path': de_route, 'title': expected_title, 'headings': len(dd.headings), 'forms': len(dd.forms), 'affiliates': len(de_aff)})
    sitemap = build / 'sitemap.xml'
    if sitemap.is_file():
        sitemap_text = sitemap.read_text(encoding='utf-8')
        if '<sitemapindex' not in sitemap_text:
            for record in records:
                present = '<loc>' + ORIGIN + record['path'] + '</loc>' in sitemap_text
                if present == (record['path'] == '/it/contatti/'):
                    errors.append({'page': record['path'], 'check': 'sitemap_indexability'})
    if len(records) != 18 or forms != 16:
        errors.append({'check': 'complete_rendered_scope', 'pages': len(records), 'forms': forms})
    return {'passed': not errors, 'source_files': len(sources), 'pages': len(records), 'forms': forms, 'errors': errors, 'routes': routes, 'records': records,
            'reviewed_exceptions': ['Localized slugs/section URLs', 'day/month/year units translated; USD amounts unchanged', 'Italian text in matching CTA SVG', 'IT About/Contact render full English source bodies historically hidden in EN']}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('build', type=Path)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    result = audit(args.build)
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(result, ensure_ascii=True, indent=2))
    raise SystemExit(0 if result['passed'] else 1)
