#!/usr/bin/env python3
"""Audit every recovered localization in the publishable build. No network requests."""
from collections import Counter, defaultdict
from html import unescape
from pathlib import Path
from urllib.parse import urlparse, unquote
import json
import re
import sys

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else "cloudflare-public")
LANGS = ("bn", "pt-br", "fr", "hi", "id", "ru", "es", "vi")
ISSUES = []
SUMMARY = defaultdict(Counter)
ATTR = re.compile(r"""([:\w-]+)\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s>]+))""", re.I)
HTML_TAG = re.compile(r"<[^>]*>", re.S)

def attrs(tag):
    return {k.lower(): (a or b or c or "") for k,a,b,c in ATTR.findall(tag)}

def local_file(link):
    u = urlparse(unescape(link))
    if u.hostname and u.hostname.lower() not in ("vpsforwebsite.com", "www.vpsforwebsite.com"):
        return None
    if u.scheme not in ("", "http", "https"):
        return None
    path = unquote(u.path or "/")
    if not path.startswith("/"):
        return None
    if path == "/":
        return ROOT / "index.html"
    if path.endswith("/"):
        return ROOT / path.lstrip("/") / "index.html"
    if Path(path).suffix:
        return ROOT / path.lstrip("/")
    return ROOT / path.lstrip("/") / "index.html"

def title(html, tag):
    m = re.search(r"<" + tag + r"\b[^>]*>([\s\S]*?)</" + tag + r">", html, re.I)
    return unescape(HTML_TAG.sub("", m.group(1))).strip() if m else ""

for lang in LANGS:
    pages = sorted((ROOT / lang).rglob("*.html"))
    SUMMARY[lang]["pages"] = len(pages)
    for page in pages:
        rel = page.relative_to(ROOT)
        html = page.read_text(encoding="utf-8", errors="replace")
        metas = [attrs(tag) for tag in re.findall(r"<meta\b[^>]*>", html, re.I)]
        robots = [m.get("content", "").lower() for m in metas if m.get("name", "").lower() == "robots"]
        is_noindex = any("noindex" in value for value in robots)
        refresh = next((m.get("content", "") for m in metas
                        if m.get("http-equiv", "").lower() == "refresh"), "")
        if refresh:
            target = re.split(r"url\s*=", refresh, maxsplit=1, flags=re.I)[-1].strip().strip("\'\"")
            target_file = local_file(target)
            SUMMARY[lang]["redirects"] += 1
            if target_file is None or not target_file.is_file():
                ISSUES.append((lang, "BROKEN_REDIRECT", str(rel), target))
                SUMMARY[lang]["broken_redirects"] += 1
            continue
        html_tag = re.search(r"<html\b[^>]*>", html, re.I)
        actual = attrs(html_tag.group(0)).get("lang", "") if html_tag else ""
        if actual.lower().split("-")[0] != lang.split("-")[0]:
            ISSUES.append((lang, "WRONG_HTML_LANG", str(rel), actual))
            SUMMARY[lang]["wrong_html_lang"] += 1
        t = title(html, "title")
        h1s = re.findall(r"<h1\b[^>]*>", html, re.I)
        h1 = title(html,"h1")
        if len(h1s) != 1:
            ISSUES.append((lang, "H1_COUNT", str(rel), len(h1s)))
            SUMMARY[lang]["h1_count"] += 1
        if t and h1 and t.strip().casefold() != h1.strip().casefold():
            ISSUES.append((lang, "TITLE_H1_DIFFER", str(rel), f"{t!r} != {h1!r}"))
            SUMMARY[lang]["title_h1_mismatch"] += 1
        canon = ""
        for tag in re.findall(r"<link\b[^>]*>", html, re.I):
            a=attrs(tag)
            if "canonical" in a.get("rel", "").split():
                canon = a.get("href","")
        expected = "https://vpsforwebsite.com/" + (str(rel.parent).replace("\\","/") + "/" if rel.name == "index.html" else str(rel))
        if canon:
            p=urlparse(unescape(canon))
            if p.path.rstrip("/") != urlparse(expected).path.rstrip("/"):
                ISSUES.append((lang,"WRONG_CANONICAL",str(rel),canon))
                SUMMARY[lang]["wrong_canonical"] += 1
        elif not is_noindex:
            ISSUES.append((lang, "NO_CANONICAL", str(rel), ""))
            SUMMARY[lang]["no_canonical"] += 1
        urls=set()
        for tag in re.findall(r"<link\b[^>]*>",html,re.I):
            a=attrs(tag)
            if "alternate" in a.get("rel","").split() and a.get("hreflang"):
                target=a.get("href","")
                if a["hreflang"] in urls:
                    SUMMARY[lang]["duplicate_hreflang"] += 1
                    ISSUES.append((lang,"DUPLICATE_HREFLANG",str(rel),a["hreflang"]))
                urls.add(a["hreflang"])
                if target:
                    f=local_file(target)
                    if f is not None and not f.is_file():
                        SUMMARY[lang]["broken_hreflang"] += 1
                        ISSUES.append((lang,"BROKEN_HREFLANG",str(rel),a["hreflang"]+" "+target))
        if len(urls) < 2 and not is_noindex:
            SUMMARY[lang]["too_few_hreflangs"] += 1
            ISSUES.append((lang,"TOO_FEW_HREFLANGS",str(rel),len(urls)))
        for a in re.findall(r"<a\b[^>]*>",html,re.I):
            url=attrs(a).get("href","")
            if not url or url.startswith("#") or url.startswith(("mailto:","tel:","javascript:")):
                continue
            f=local_file(url)
            if f is not None and not f.is_file():
                SUMMARY[lang]["broken_links"]+=1
                if SUMMARY[lang]["broken_links"]<=12:
                    ISSUES.append((lang,"BROKEN_LINK",str(rel),url))
        if is_noindex:
            SUMMARY[lang]["noindex"] += 1
        summary = html[html.find("<main"):html.find("</main>")+7]
        if actual.lower().startswith("en") and lang!="en":
            SUMMARY[lang]["english_fallback"]+=1
        if len(summary)<800 and not is_noindex:
            SUMMARY[lang]["short_main"]+=1
        if "https://www.vdsina.com/?partner=ni8gzrvz75" in html:
            SUMMARY[lang]["affiliate_present"] += 1

print("LOCALIZED_PAGE_AUDIT_V1")
for lang in LANGS:
    print(lang, json.dumps(dict(SUMMARY[lang]),ensure_ascii=False,sort_keys=True))
print("ISSUE_COUNT",len(ISSUES))
for entry in ISSUES[:160]:
    print("ISSUE",*entry,sep="\t")
if "--strict" in sys.argv and ISSUES:
    raise SystemExit(1)
