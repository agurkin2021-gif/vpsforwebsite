#!/usr/bin/env python3
from pathlib import Path
from urllib.parse import urlparse, unquote
import re
import sys

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else "cloudflare-public")
RECOVERED = Path(sys.argv[2] if len(sys.argv) > 2 else "recovered-public")
BASE = "https://vpsforwebsite.com"

LANGS = [
    ("en", "English", "/"),
    ("bn", "বাংলা", "/bn/"),
    ("pt-BR", "Português (Brasil)", "/pt-br/"),
    ("fr", "Français", "/fr/"),
    ("hi", "हिन्दी", "/hi/"),
    ("id", "Bahasa Indonesia", "/id/"),
    ("ru", "Русский", "/ru/"),
    ("es", "Español", "/es/"),
    ("vi", "Tiếng Việt", "/vi/"),
    ("ko", "한국어", "/ko/"),
    ("de", "Deutsch", "/de/"),
    ("it", "Italiano", "/it/"),
    ("fa", "فارسی", "/fa/"),
]
LANG_CODES = [x[0] for x in LANGS]
HOME = {code: url for code, _, url in LANGS}

ATTR_RE = re.compile(r"""([:\w-]+)\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s>]+))""", re.I)
TAG_RE = re.compile(r"<link\b[^>]*>", re.I)
ANCHOR_RE = re.compile(r"<a\b[^>]*>", re.I)
HTML_LANG_RE = re.compile(r"""<html\b[^>]*\blang\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s>]+))""", re.I)
LEGACY_LIST_RE = re.compile(r"""(<ul\b[^>]*\bid\s*=\s*(?:"language-options"|'language-options'|language-options)[^>]*>)(.*?)(</ul>)""", re.I | re.S)
GENERATED_LIST_RE = re.compile(r"""(<div\b[^>]*\bdata-language-options\b[^>]*>)(.*?)(</div>)""", re.I | re.S)


def attrs(tag):
    out = {}
    for m in ATTR_RE.finditer(tag):
        out[m.group(1).lower()] = m.group(2) or m.group(3) or m.group(4) or ""
    return out


def normalize_lang(value):
    low = (value or "").lower()
    if low.startswith("pt"):
        return "pt-BR"
    for code in LANG_CODES:
        if low == code.lower() or low.startswith(code.lower() + "-"):
            return code
    return value or "en"


def is_noindex(html):
    for tag in re.finditer(r"<meta\b[^>]*>", html, re.I):
        attributes = attrs(tag.group(0))
        if attributes.get("name", "").lower() == "robots" and "noindex" in attributes.get("content", "").lower():
            return True
    return False


def extract_alternates(html):
    result = {}
    for m in TAG_RE.finditer(html):
        a = attrs(m.group(0))
        if "alternate" not in a.get("rel", "").lower().split():
            continue
        lang = a.get("hreflang")
        href = a.get("href")
        if lang and href:
            result[normalize_lang(lang) if lang.lower() != "x-default" else "x-default"] = href
    return result


def html_language(html):
    m = HTML_LANG_RE.search(html)
    if not m:
        return "en"
    return normalize_lang(m.group(1) or m.group(2) or m.group(3) or "en")


def url_to_rel(url):
    path = unquote(urlparse(url).path or "/")
    if path == "/":
        return Path("index.html")
    if path.endswith("/"):
        return Path(path.lstrip("/")) / "index.html"
    return Path(path.lstrip("/"))


def ref_for(rel, html):
    same = RECOVERED / rel
    if same.is_file():
        return same
    current = extract_alternates(html)
    en = current.get("en") or current.get("x-default")
    if not en and html_language(html) in ENGLISH_BY_LOCALE:
        en = ENGLISH_BY_LOCALE[html_language(html)].get("/" + rel.parent.as_posix() + "/")
    if en:
        candidate = RECOVERED / url_to_rel(en)
        if candidate.is_file():
            return candidate
    return None


def ko_equivalent(en_url):
    if not en_url:
        return "/ko/"
    path = urlparse(en_url).path or "/"
    if path == "/":
        return "/ko/"
    candidate = "/ko" + (path if path.startswith("/") else "/" + path)
    if candidate.endswith("/"):
        file = ROOT / candidate.lstrip("/") / "index.html"
    else:
        file = ROOT / candidate.lstrip("/")
    return candidate if file.is_file() else "/ko/"


def route_exists(url):
    parsed = urlparse(url)
    if parsed.netloc and parsed.netloc != "vpsforwebsite.com":
        return False
    return (ROOT / url_to_rel(url)).is_file()


def source_equivalents(language):
    """Read Hugo's actual locale/EN pairs before rewriting recovered navigation.

    Source filenames connect translations even when their public slugs differ.
    Noindex service pages omit head alternates, so use their Hugo picker pairs.
    Never treat a fallback language homepage as an equivalent inner article.
    """
    pairs = {}
    for page in (ROOT / language).rglob("index.html"):
        html = page.read_text(encoding="utf-8", errors="strict")
        current = extract_alternates(html)
        en_url = current.get("en")
        if not en_url:
            picker = LEGACY_LIST_RE.search(html) or GENERATED_LIST_RE.search(html)
            if picker:
                for tag in ANCHOR_RE.finditer(picker.group(2)):
                    a = attrs(tag.group(0))
                    if normalize_lang(a.get("hreflang", "")) == "en":
                        en_url = a.get("href")
                        break
        localized_url = "/" + page.relative_to(ROOT).parent.as_posix() + "/"
        if en_url and route_exists(en_url):
            en_path = unquote(urlparse(en_url).path or "/")
            if en_path != "/" or localized_url == "/" + language + "/":
                pairs[en_path] = localized_url
    return pairs


def rebuild_generated_list(html, routes):
    m = GENERATED_LIST_RE.search(html)
    if not m:
        return html
    current = html_language(html)
    items = []
    for code, label, home in LANGS:
        href = routes.get(code, home)
        active = " font-bold" if normalize_lang(current) == code else ""
        aria = ' aria-current="page"' if normalize_lang(current) == code else ""
        items.append(
            f'<a href="{href}" hreflang="{code}" lang="{code}" '
            f'class="block px-4 py-2 text-sm text-white hover:text-primary hover:bg-white/10{active}"{aria}>'
            f'{label}</a>'
        )
    return html[:m.start()] + m.group(1) + "".join(items) + m.group(3) + html[m.end():]


def set_href(tag, href):
    if re.search(r"\bhref\s*=", tag, re.I):
        return re.sub(r"""\bhref\s*=\s*(?:"[^"]*"|'[^']*'|[^\s>]+)""", f'href="{href}"', tag, count=1, flags=re.I)
    return tag[:-1] + f' href="{href}">'


def patch_switcher_links(html, routes):
    def repl(m):
        tag = m.group(0)
        a = attrs(tag)
        lang = a.get("hreflang")
        if not lang:
            return tag
        code = normalize_lang(lang)
        href = routes.get(code)
        return set_href(tag, href) if href else tag
    return ANCHOR_RE.sub(repl, html)


def rebuild_legacy_list(html, routes):
    m = LEGACY_LIST_RE.search(html)
    if not m:
        return html
    current = html_language(html)
    items = []
    for code, label, home in LANGS:
        href = routes.get(code, home)
        active = ' aria-current="page"' if normalize_lang(current) == code else ""
        items.append(
            f'<li><a href="{href}" hreflang="{code}"{active}>'
            f'<bdi lang="{code}" dir="auto">{label}</bdi></a></li>'
        )
    return html[:m.start()] + m.group(1) + "".join(items) + m.group(3) + html[m.end():]


def replace_alternates(html, routes, include_ko):
    merged = {k: v for k, v in routes.items() if k in LANG_CODES}
    if not include_ko:
        merged.pop("ko", None)
    en = merged.get("en", "/")
    tags = []
    for code in LANG_CODES:
        href = merged.get(code)
        if href:
            abs_href = href if href.startswith("http") else BASE + href
            tags.append(f'<link rel="alternate" hreflang="{code}" href="{abs_href}">')
    abs_default = en if en.startswith("http") else BASE + en
    tags.append(f'<link rel="alternate" hreflang="x-default" href="{abs_default}">')

    def strip_tag(m):
        a = attrs(m.group(0))
        return "" if "alternate" in a.get("rel", "").lower().split() and a.get("hreflang") else m.group(0)

    html = TAG_RE.sub(strip_tag, html)
    block = "".join(tags)
    return html.replace("</head>", block + "</head>", 1)


changed = 0
patched_generated = 0
patched_legacy = 0
LOCALES_BY_EN = {language: source_equivalents(language) for language in ("de", "it", "fa")}
ENGLISH_BY_LOCALE = {language: {localized: en for en, localized in pairs.items()}
                     for language, pairs in LOCALES_BY_EN.items()}

for page in ROOT.rglob("*.html"):
    if page.name == "404.html":
        continue
    rel = page.relative_to(ROOT)
    html = page.read_text(encoding="utf-8", errors="ignore")
    original = html

    reference = ref_for(rel, html)
    legacy = {}
    if reference:
        legacy_html = reference.read_text(encoding="utf-8", errors="ignore")
        legacy = extract_alternates(legacy_html)

    current = extract_alternates(html)
    routes = {}
    routes.update(legacy)
    routes.update(current)
    if html_language(html) in ENGLISH_BY_LOCALE:
        own_url = "/" + rel.parent.as_posix() + "/"
        english_pairs = ENGLISH_BY_LOCALE[html_language(html)]
        if own_url in english_pairs:
            routes["en"] = english_pairs[own_url]

    # Always keep every language visible in the selector. When an equivalent
    # static translation is unavailable, fall back to that language homepage.
    for code, _, home in LANGS:
        routes.setdefault(code, home)

    en_url = routes.get("en", "/")
    en_reference = current.get("en") or legacy.get("en")
    if html_language(html) == "en":
        en_reference = "/" if rel.as_posix() == "index.html" else "/" + rel.parent.as_posix() + "/"
    elif html_language(html) in ENGLISH_BY_LOCALE:
        en_reference = ENGLISH_BY_LOCALE[html_language(html)].get("/" + rel.parent.as_posix() + "/") or en_reference
    native_urls = {}
    for language, pairs in LOCALES_BY_EN.items():
        localized_url = current.get(language)
        if not localized_url and en_reference:
            localized_url = pairs.get(unquote(urlparse(en_reference).path or "/"))
        if localized_url and route_exists(localized_url):
            routes[language] = localized_url
            native_urls[language] = localized_url
    ko_url = current.get("ko")
    if not ko_url:
        candidate = ko_equivalent(en_url)
        if candidate != "/ko/" or (urlparse(en_url).path or "/") == "/":
            ko_url = candidate
    if ko_url:
        routes["ko"] = ko_url

    # Never publish a switcher link to a missing page; use its recovered homepage.
    for code, _, home in LANGS:
        if not route_exists(routes.get(code, home)):
            routes[code] = home

    if "data-language-options" in html:
        html = rebuild_generated_list(html, routes)
        patched_generated += 1
    elif "language-options" in html and "language-picker" in html:
        html = rebuild_legacy_list(html, routes)
        patched_legacy += 1

    # Hreflang must describe equivalent pages only. Keep recovered equivalents,
    # keep Hugo translations, and add KO only where a real KO counterpart exists.
    seo_routes = {}
    seo_routes.update(legacy)
    seo_routes.update(current)
    actual_ko = current.get("ko")
    if not actual_ko:
        candidate = ko_equivalent(en_url)
        if candidate != "/ko/" or (urlparse(en_url).path or "/") == "/":
            actual_ko = candidate
    if actual_ko:
        seo_routes["ko"] = actual_ko
    # A language-home fallback is navigation, never an article hreflang target.
    # Contact/noindex pages retain the existing indexing policy; do not invent
    # an alternate for them merely because a localized picker target exists.
    noindex = is_noindex(html)
    for language in LOCALES_BY_EN:
        if language in native_urls and not noindex:
            seo_routes[language] = native_urls[language]
        else:
            seo_routes.pop(language, None)
    if not (noindex and html_language(html) in LOCALES_BY_EN):
        html = replace_alternates(html, seo_routes, bool(actual_ko))

    # Recovered pages need the same responsive fixes as Hugo pages. Preserve
    # their immutable fingerprinted CSS and add each shared stylesheet once.
    link_ids = {attrs(tag.group(0)).get("id") for tag in TAG_RE.finditer(html)}
    for style_id, href in (
        ("guide-navigation-css", "/css/guide-navigation.v1.css"),
        ("hero-layout-css", "/css/hero-layout.v1.css"),
    ):
        if style_id not in link_ids:
            html = html.replace(
                "</head>",
                f'<link id="{style_id}" rel="stylesheet" href="{href}"></head>',
                1,
            )

    if html != original:
        page.write_text(html, encoding="utf-8")
        changed += 1

print(f"Language navigation restored: changed_html={changed}, generated_switchers={patched_generated}, legacy_switchers={patched_legacy}")
