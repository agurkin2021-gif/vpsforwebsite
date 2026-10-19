#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import re
import sys
import time
from collections import deque
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from urllib.parse import urljoin, urlparse, urlunparse
import xml.etree.ElementTree as ET

import requests
from bs4 import BeautifulSoup

BASE = "https://vpsforwebsite.com/"
HOSTS = {"vpsforwebsite.com", "www.vpsforwebsite.com"}
OUT = Path("recovered-public")
MANIFEST = Path("recovery-manifest.json")
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/154.0.0.0 Safari/537.36"
TIMEOUT = 20
MAX_WORKERS = 12
MAX_URLS = 20000

session = requests.Session()
session.headers.update({
    "User-Agent": UA,
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br",
})

def normalize(raw: str, base: str) -> str | None:
    if not raw:
        return None
    raw = raw.strip()
    if raw.startswith(("mailto:", "tel:", "javascript:", "data:", "blob:", "#")):
        return None
    try:
        u = urlparse(urljoin(base, raw))
    except Exception:
        return None
    host = (u.hostname or "").lower()
    if u.scheme not in ("http", "https") or host not in HOSTS:
        return None
    # Keep exact production host/path. Strip query/fragment to avoid cache-key misses.
    u = u._replace(scheme="https", netloc="vpsforwebsite.com", query="", fragment="")
    return urlunparse(u)

def output_path(url: str, content_type: str) -> Path:
    p = urlparse(url).path or "/"
    ctype = content_type.lower()
    is_html = "text/html" in ctype
    if is_html:
        if p.endswith("/"):
            rel = p.lstrip("/") + "index.html"
        elif Path(p).suffix.lower() in {".html", ".htm"}:
            rel = p.lstrip("/")
        else:
            rel = p.lstrip("/") + "/index.html"
    else:
        rel = p.lstrip("/") or "index"
    return OUT / rel

def parse_sitemap_bytes(data: bytes, base: str) -> tuple[set[str], set[str]]:
    pages, sitemaps = set(), set()
    try:
        root = ET.fromstring(data)
    except Exception:
        return pages, sitemaps
    locs = [e.text.strip() for e in root.iter() if e.tag.endswith("loc") and e.text]
    if root.tag.endswith("sitemapindex"):
        for loc in locs:
            n = normalize(loc, base)
            if n:
                sitemaps.add(n)
    else:
        for loc in locs:
            n = normalize(loc, base)
            if n:
                pages.add(n)
    return pages, sitemaps

def discover_html(text: str, base: str) -> set[str]:
    found = set()
    soup = BeautifulSoup(text, "html.parser")
    attrs = ("href", "src", "poster", "action", "data-src", "data-href")
    for tag in soup.find_all(True):
        for attr in attrs:
            val = tag.get(attr)
            if val:
                n = normalize(val, base)
                if n:
                    found.add(n)
        for attr in ("srcset", "data-srcset"):
            val = tag.get(attr)
            if val:
                for part in val.split(","):
                    raw = part.strip().split(" ")[0]
                    n = normalize(raw, base)
                    if n:
                        found.add(n)
    # CSS url() occasionally embedded in inline style.
    for raw in re.findall(r"url\((?:['\"])?([^)'\"]+)", text, re.I):
        n = normalize(raw, base)
        if n:
            found.add(n)
    return found

def discover_css(text: str, base: str) -> set[str]:
    found = set()
    for raw in re.findall(r"url\((?:['\"])?([^)'\"]+)", text, re.I):
        n = normalize(raw.strip(), base)
        if n:
            found.add(n)
    for raw in re.findall(r"@import\s+(?:url\()?['\"]?([^'\"\s)]+)", text, re.I):
        n = normalize(raw.strip(), base)
        if n:
            found.add(n)
    return found

def discover_js(text: str, base: str) -> set[str]:
    found = set()
    for pat in (
        r'''(?:import|from)\s*\(?\s*["']([^"']+)["']''',
        r'''["']([^"']+\.(?:js|mjs|css|json|wasm|svg|png|webp|jpg|jpeg|gif|woff2?|ttf|ico))["']''',
    ):
        for raw in re.findall(pat, text, re.I):
            n = normalize(raw, base)
            if n:
                found.add(n)
    return found

def fetch_one(url: str):
    started = time.time()
    try:
        r = session.get(url, timeout=TIMEOUT, allow_redirects=True)
        ctype = r.headers.get("content-type", "").split(";")[0].strip().lower()
        status = r.status_code
        cache = r.headers.get("cf-cache-status", "")
        ray = r.headers.get("cf-ray", "")
        result = {
            "url": url,
            "final_url": r.url,
            "status": status,
            "content_type": ctype,
            "cf_cache_status": cache,
            "cf_ray": ray,
            "elapsed_ms": int((time.time() - started) * 1000),
            "size": len(r.content),
        }
        discovered = set()

        if 200 <= status < 300:
            path = output_path(url, ctype)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(r.content)
            result["path"] = str(path)
            result["sha256"] = hashlib.sha256(r.content).hexdigest()

            if "text/html" in ctype:
                discovered |= discover_html(r.text, url)
            elif "text/css" in ctype or path.suffix.lower() == ".css":
                discovered |= discover_css(r.text, url)
            elif "javascript" in ctype or path.suffix.lower() in {".js", ".mjs"}:
                discovered |= discover_js(r.text, url)

            if "xml" in ctype or url.endswith(".xml"):
                pages, maps = parse_sitemap_bytes(r.content, url)
                discovered |= pages | maps

        return result, discovered
    except Exception as e:
        return {
            "url": url,
            "status": 0,
            "error": repr(e),
            "elapsed_ms": int((time.time() - started) * 1000),
        }, set()

def main():
    OUT.mkdir(parents=True, exist_ok=True)

    # Exact production URLs only; no cache-busting query strings.
    seeds = {
        BASE,
        BASE + "robots.txt",
        BASE + "sitemap.xml",
        BASE + "404.html",
        BASE + "about/",
        BASE + "contact/",
        BASE + "vps-for-wordpress/",
        BASE + "vps-for-woocommerce/",
        BASE + "vps-for-multiple-websites/",
        BASE + "vps-security-checklist/",
        BASE + "vps-backup-strategy/",
        BASE + "vps-monitoring/",
        BASE + "vps-vs-shared-hosting/",
        BASE + "website-migration-to-vps/",
        BASE + "how-to-host-a-website-on-vps/",
        BASE + "managed-vs-unmanaged-vps/",
        BASE + "fastpanel-vps-hosting/",
        BASE + "vps-with-control-panel/",
        BASE + "how-to-choose-vps-location/",
        BASE + "vps-sizing-for-website/",
        BASE + "privacy-policy/",
    }

    # Known language roots used by the live site. Missing cache entries are harmless.
    langs = """
    es de fr pt pl ru it tr ja nl id vi cs uk ko fa ar ro hu sv el he bg da fi no sk hr sr bs
    hi ur bn th ms fil et lv lt sl sq az ka hy be mk kk uz mn ne si sw af ca eu gl is ga cy mt
    lb eo la jv su ha yo ig zu xh st sn rw so am km lo my
    """.split()
    for lang in langs:
        seeds.add(f"{BASE}{lang}/")

    queue = deque(sorted(seeds))
    scheduled = set()
    results = []

    while queue:
        batch = []
        while queue and len(batch) < 200:
            u = queue.popleft()
            if u not in scheduled:
                scheduled.add(u)
                batch.append(u)
        if not batch:
            continue
        if len(scheduled) > MAX_URLS:
            raise SystemExit(f"Safety limit exceeded: {len(scheduled)} URLs")

        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as ex:
            futs = [ex.submit(fetch_one, u) for u in batch]
            for fut in as_completed(futs):
                rec, found = fut.result()
                results.append(rec)
                if 200 <= rec.get("status", 0) < 300:
                    for n in found:
                        if n not in scheduled:
                            queue.append(n)

        ok = sum(1 for x in results if 200 <= x.get("status", 0) < 300)
        hits = sum(1 for x in results if x.get("cf_cache_status") in {"HIT", "STALE", "UPDATING", "REVALIDATED"})
        print(f"visited={len(scheduled)} queued={len(queue)} ok={ok} cache_like={hits}", flush=True)

    results.sort(key=lambda x: x.get("url", ""))
    MANIFEST.write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")

    html_count = sum(1 for p in OUT.rglob("*.html"))
    file_count = sum(1 for p in OUT.rglob("*") if p.is_file())
    ok = sum(1 for x in results if 200 <= x.get("status", 0) < 300)
    cache_like = sum(1 for x in results if x.get("cf_cache_status") in {"HIT", "STALE", "UPDATING", "REVALIDATED"})

    print(f"RECOVERY SUMMARY files={file_count} html={html_count} ok={ok} cache_like={cache_like}")
    if not (OUT / "index.html").is_file():
        raise SystemExit("Homepage was not recovered")
    if html_count < 10:
        raise SystemExit(f"Too few cached HTML pages recovered: {html_count}")

if __name__ == "__main__":
    main()
