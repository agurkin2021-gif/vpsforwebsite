#!/usr/bin/env python3
"""Fail a Cloudflare build if cached locale pages or their switchers disappear."""
from html import unescape
from pathlib import Path
from urllib.parse import unquote, urlparse
import re
import sys

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else "cloudflare-public")
RECOVERED = Path(sys.argv[2] if len(sys.argv) > 2 else "recovered-public")
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
]
LEGACY = re.compile(r"""<ul\b[^>]*\bid\s*=\s*(?:"language-options"|'language-options'|language-options)[^>]*>(.*?)</ul>""", re.I | re.S)
GENERATED = re.compile(r"""<div\b[^>]*\bdata-language-options\b[^>]*>(.*?)</div>""", re.I | re.S)
ANCHORS = re.compile(r"(<a\b[^>]*>)(.*?)</a>", re.I | re.S)
TAGS = re.compile(r"<[^>]*>")
errors = []

def attr(tag, name):
    match = re.search(r"""(?:^|\s)""" + re.escape(name) + r"""\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s>]+))""", tag, re.I)
    return (match.group(1) or match.group(2) or match.group(3)) if match else None

def local_file(href):
    parsed = urlparse(href)
    if parsed.hostname and parsed.hostname not in ("vpsforwebsite.com", "www.vpsforwebsite.com"):
        return None
    path = unquote(parsed.path or "/")
    if not path.startswith("/"):
        return None
    if path == "/":
        return ROOT / "index.html"
    if path.endswith("/"):
        return ROOT / path.lstrip("/") / "index.html"
    return ROOT / path.lstrip("/")

if not ROOT.is_dir() or not RECOVERED.is_dir():
    raise SystemExit("Missing Cloudflare build or recovered cache snapshot")

cached_html = list(RECOVERED.rglob("*.html"))
for page in cached_html:
    target = ROOT / page.relative_to(RECOVERED)
    if not target.is_file():
        errors.append(f"CACHE LOST: {page.relative_to(RECOVERED)}")

for code, label, url in LANGS:
    target = local_file(url)
    if target is None or not target.is_file():
        errors.append(f"LOCALE HOME MISSING: {code} {url}")

checked = 0
for page in ROOT.rglob("*.html"):
    if page.name == "404.html":
        continue  # Error documents have intentionally missing localized 404 routes.
    html = page.read_text(encoding="utf-8", errors="replace")
    match = GENERATED.search(html) or LEGACY.search(html)
    if not match:
        if page.name != "404.html" and re.search(r"<header\b", html, re.I) and not re.search(r"http-equiv=['\"]?refresh", html, re.I):
            errors.append(f"SWITCHER MISSING: {page.relative_to(ROOT)}")
        continue
    checked += 1
    options = []
    for anchor, text in ANCHORS.findall(match.group(1)):
        code, href = attr(anchor, "hreflang"), attr(anchor, "href")
        label = unescape(TAGS.sub("", text)).strip()
        options.append((code, label, href))
    actual = [code for code, _, _ in options]
    if actual != [code for code, _, _ in LANGS]:
        errors.append(f"LANGUAGE ORDER: {page.relative_to(ROOT)} -> {actual}")
        continue
    for (expected_code, expected_label, _), (code, label, href) in zip(LANGS, options):
        if label != expected_label:
            errors.append(f"LANGUAGE LABEL: {page.relative_to(ROOT)} {code}: {label!r}")
        path = local_file(href or "") if href else None
        if path is None or not path.is_file():
            errors.append(f"LANGUAGE LINK BROKEN: {page.relative_to(ROOT)} {code}: {href}")

if checked < len(cached_html):
    errors.append(f"TOO FEW SWITCHERS: checked {checked}, recovered HTML pages {len(cached_html)}")

print(f"Recovery audit: {len(cached_html)} cached HTML pages preserved, {len(LANGS)} locale homes, {checked} language switchers checked, {len(errors)} errors")
for error in errors[:60]:
    print(error, file=sys.stderr)
if errors:
    raise SystemExit(1)
