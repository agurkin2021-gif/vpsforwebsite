#!/usr/bin/env python3
"""Audit complete Persian source coverage and rendered SEO/interactive parity.

Run after a production Hugo build: python scripts/audit-persian.py public
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
    return ('/fa/' if language == 'fa' else '/') + (tail + '/' if tail else '')


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
        self.direction = ''
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
            self.direction = attrs.get('dir', '')
        if tag == 'link' and attrs.get('rel') == 'canonical':
            self.canonical.append(unquote(attrs.get('href', '')))
        if tag == 'link' and attrs.get('hreflang'):
            self.hreflang.append((attrs['hreflang'], unquote(attrs.get('href', ''))))
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
    persian = PROJECT / 'content/persian'
    sources = sorted(p.relative_to(english) for p in english.rglob('*.md'))
    targets = sorted(p.relative_to(persian) for p in persian.rglob('*.md'))
    errors, records, exceptions = [], [], []
    if sources != targets:
        errors.append({'source_coverage': {'missing': [str(p) for p in set(sources) - set(targets)], 'extra': [str(p) for p in set(targets) - set(sources)]}})
    forms = 0
    routes = []
    for rel in sources:
        if not (persian / rel).is_file():
            continue
        en = (english / rel).read_text(encoding='utf-8')
        fa = (persian / rel).read_text(encoding='utf-8')
        # Only explicit, meaning-preserving localization exceptions are normalized.
        fa_normalized = re.sub(r'^(?:slug|url):.*\n', '', fa, flags=re.M)
        fa_normalized = fa_normalized.replace('/روز', '/day').replace('/ماه', '/month').replace('/سال', '/year')
        fa_normalized = fa_normalized.replace('images/home/vps-cta-fa.svg', 'images/home/vps-cta.svg')
        # RTL-only semantic wrappers keep Latin resource/price runs together;
        # every enclosed number and unit remains subject to English parity.
        fa_normalized = re.sub(r'<bdi dir="ltr">(.*?)</bdi>', r'\1', fa_normalized)
        # Native Persian unit names (including adjectival forms) preserve the
        # exact numeric specifications checked against the English source.
        for native, latin in [('گیگابایتی', 'GB'), ('گیگابایت', 'GB'), ('ترابایتی', 'TB'), ('ترابایت', 'TB'), ('مگاهرتز', 'MHz')]:
            fa_normalized = fa_normalized.replace(native, latin)
        if rel.as_posix() == 'vps-sizing-for-website.md':
            # A localized accessibility hint may accompany the mobile scroll wrapper.
            fa_normalized = re.sub(r'<p class="vps-table-scroll-hint">[^<]+</p>\n?', '', fa_normalized)
        result = module.report(en, fa_normalized)
        for error in result['errors']:
            errors.append({'page': str(rel), **error})
        # These source structures must not be shortened or padded.
        en_body, fa_body = en.split('---', 2)[2], fa.split('---', 2)[2]
        for name, pattern in [('bullets', r'^\s*[-*] '), ('numbered_items', r'^\s*\d+\. '), ('code_fences', r'^```')]:
            if len(re.findall(pattern, en_body, re.M)) != len(re.findall(pattern, fa_body, re.M)):
                errors.append({'page': str(rel), 'check': name})
        if en == fa:
            errors.append({'page': str(rel), 'check': 'untranslated_source'})
        if rel.parts[0] == 'sections':
            continue
        en_route, fa_route = route(rel, en, 'en'), route(rel, fa, 'fa')
        routes.append({'source': str(rel).replace('\\', '/'), 'en': en_route, 'fa': fa_route})
        en_file = build / en_route.strip('/') / 'index.html'
        fa_file = build / fa_route.strip('/') / 'index.html'
        if not en_file.is_file() or not fa_file.is_file():
            errors.append({'page': str(rel), 'check': 'missing_rendered_page', 'fa': fa_route})
            continue
        ed, fd = Document(en_file.read_text(encoding='utf-8')), Document(fa_file.read_text(encoding='utf-8'))
        expected_title = re.search(r'^title:\s*"([^"]+)"', fa, re.M)[1]
        if fd.direction != 'rtl' or fd.lang.split('-')[0] != 'fa' or fd.title.strip() != expected_title or fd.h1.strip() != expected_title or fd.h1_count != 1:
            errors.append({'page': fa_route, 'check': 'lang_title_h1', 'title': fd.title, 'h1': fd.h1, 'lang': fd.lang})
        expected_noindex = rel.parts[0] == 'contact'
        if fd.canonical != [ORIGIN + fa_route] and not (expected_noindex and not fd.canonical):
            errors.append({'page': fa_route, 'check': 'canonical', 'actual': fd.canonical})
        if not fd.description or fd.description == ed.description:
            errors.append({'page': fa_route, 'check': 'description'})
        if ('noindex' in fd.robots) != expected_noindex:
            errors.append({'page': fa_route, 'check': 'robots', 'actual': fd.robots})
        if not expected_noindex:
            hfl = dict(fd.hreflang)
            if len(hfl) != len(fd.hreflang) or hfl.get('fa') != ORIGIN + fa_route or hfl.get('en') != ORIGIN + en_route or hfl.get('x-default') != ORIGIN + en_route:
                errors.append({'page': fa_route, 'check': 'hreflang', 'actual': fd.hreflang})
        if len(fd.ids) != len(set(fd.ids)):
            errors.append({'page': fa_route, 'check': 'duplicate_ids'})
        for key in ('forms', 'options', 'inputs'):
            if getattr(ed, key) != getattr(fd, key):
                errors.append({'page': fa_route, 'check': key})
        forms += len(fd.forms)
        # About/Contact source bodies were historically hidden in EN, deliberately rendered in FA.
        if rel.parts[0] not in ('about', 'contact'):
            for tag in ('h2', 'h3', 'li', 'table', 'tr', 'th', 'td', 'form', 'select', 'option'):
                if ed.tags[tag] != fd.tags[tag]:
                    errors.append({'page': fa_route, 'check': 'rendered_' + tag, 'en': ed.tags[tag], 'fa': fd.tags[tag]})
            if ed.headings != fd.headings:
                errors.append({'page': fa_route, 'check': 'heading_anchors', 'en': ed.headings, 'fa': fd.headings})
        en_aff = [a for a in ed.anchors if a.get('href') == PARTNER]
        fa_aff = [a for a in fd.anchors if a.get('href') == PARTNER]
        if len(en_aff) != len(fa_aff):
            errors.append({'page': fa_route, 'check': 'rendered_affiliate_count', 'en': len(en_aff), 'fa': len(fa_aff)})
        for a in fa_aff:
            if not {'sponsored', 'nofollow', 'noopener'}.issubset(a.get('rel', '').split()):
                errors.append({'page': fa_route, 'check': 'affiliate_attributes'})
        for a in fd.anchors:
            raw = a.get('href') or ''
            if raw.startswith('//'):
                errors.append({'page': fa_route, 'check': 'protocol_relative_link', 'href': raw})
                continue
            u = urlsplit(urljoin(ORIGIN + fa_route, raw))
            if u.netloc != 'vpsforwebsite.com' or u.scheme not in ('http', 'https'):
                continue
            local = build / unquote(u.path).lstrip('/')
            if not local.suffix:
                local = local / 'index.html'
            if not local.is_file():
                errors.append({'page': fa_route, 'check': 'missing_internal_link', 'href': raw})
            elif u.fragment:
                dest = Document(local.read_text(encoding='utf-8'))
                if unquote(u.fragment) not in dest.ids:
                    errors.append({'page': fa_route, 'check': 'missing_anchor', 'href': raw})
        records.append({'path': fa_route, 'title': expected_title, 'headings': len(fd.headings), 'forms': len(fd.forms), 'affiliates': len(fa_aff)})
    sitemap = build / 'sitemap.xml'
    if sitemap.is_file():
        sitemap_text = unquote(sitemap.read_text(encoding='utf-8'))
        if '<sitemapindex' not in sitemap_text:
            for record in records:
                present = '<loc>' + ORIGIN + record['path'] + '</loc>' in sitemap_text
                if present == (record['path'] == '/fa/تماس-با-ما/'):
                    errors.append({'page': record['path'], 'check': 'sitemap_indexability'})
    if len(records) != 18 or forms != 16:
        errors.append({'check': 'complete_rendered_scope', 'pages': len(records), 'forms': forms})
    return {'passed': not errors, 'source_files': len(sources), 'pages': len(records), 'forms': forms, 'errors': errors, 'routes': routes, 'records': records,
            'reviewed_exceptions': ['Localized slugs/section URLs', 'day/month/year units translated; USD amounts unchanged', 'LTR bdi wrappers isolate unchanged Latin specifications and prices inside RTL tables', 'Persian text in matching CTA SVG', 'FA About/Contact render full English source bodies historically hidden in EN']}


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
