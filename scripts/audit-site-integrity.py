#!/usr/bin/env python3
"""Fail publication on missing local links/assets or invalid resource integrity."""
import argparse
import base64
import hashlib
from html.parser import HTMLParser
from pathlib import Path
import re
from urllib.parse import unquote, urljoin, urlsplit

ORIGIN = "https://vpsforwebsite.com"
HOSTS = {"vpsforwebsite.com", "www.vpsforwebsite.com"}
CSS_URL = re.compile(r"""url\(\s*['"]?([^'")\s]+)['"]?\s*\)""", re.I)


class References(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.base = ""
        self.refs = []
        self.in_style = False

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        if tag == "base" and not self.base:
            self.base = attrs.get("href", "")
        if tag in ("a", "link", "area") and attrs.get("href"):
            self.refs.append((attrs["href"], attrs.get("integrity", "")))
        for attr in ("src", "poster"):
            if attrs.get(attr):
                self.refs.append((attrs[attr], attrs.get("integrity", "")))
        if attrs.get("srcset") and not attrs["srcset"].startswith("data:"):
            for candidate in attrs["srcset"].split(","):
                if candidate.strip():
                    self.refs.append((candidate.strip().split()[0], ""))
        if tag == "meta" and attrs.get("http-equiv", "").lower() == "refresh":
            target = re.search(r"url\s*=\s*(.+)$", attrs.get("content", ""), re.I)
            if target:
                self.refs.append((target[1].strip().strip("'\""), ""))
        self.refs.extend((url, "") for url in CSS_URL.findall(attrs.get("style", "")))
        if tag == "style":
            self.in_style = True

    def handle_endtag(self, tag):
        if tag == "style":
            self.in_style = False

    def handle_data(self, data):
        if self.in_style:
            self.refs.extend((url, "") for url in CSS_URL.findall(data))


def audit(root):
    root = Path(root).resolve()
    errors = []
    checked = set()
    css_queue = []
    pages = sorted(root.rglob("*.html"))
    if not pages:
        errors.append("No HTML pages found in publish root")

    def inspect(raw, base, source, integrity=""):
        if not raw or raw.startswith("#"):
            return
        parsed = urlsplit(urljoin(base, raw))
        if parsed.scheme not in ("http", "https") or parsed.hostname not in HOSTS:
            return
        # Cloudflare's injected analytics endpoint is not a static site asset.
        if parsed.path.startswith("/cdn-cgi/"):
            return
        file = (root / unquote(parsed.path).lstrip("/")).resolve()
        if not file.is_relative_to(root):
            errors.append(f"{source}: URL escapes publish root: {raw}")
            return
        if file.is_dir() or (not file.is_file() and not file.suffix):
            file /= "index.html"
        if not file.is_file():
            errors.append(f"{source}: missing local target {raw}")
            return
        key = (file, integrity)
        if key in checked:
            return
        checked.add(key)
        if integrity:
            tokens = [token.split("-", 1) for token in integrity.split() if "-" in token]
            supported = [(algorithm, digest) for algorithm, digest in tokens
                         if algorithm in ("sha256", "sha384", "sha512")]
            if not supported:
                errors.append(f"{source}: unsupported integrity for {raw}")
            else:
                # Browsers use the strongest hash algorithm supplied in SRI.
                algorithm = max((alg for alg, _ in supported), key=lambda alg: int(alg[3:]))
                actual = base64.b64encode(hashlib.new(algorithm, file.read_bytes()).digest()).decode()
                if not any(alg == algorithm and digest == actual for alg, digest in supported):
                    errors.append(f"{source}: invalid integrity for {raw}")
        if file.suffix == ".css":
            css_queue.append(file)

    for page in pages:
        rel = page.relative_to(root).as_posix()
        url = ORIGIN + "/" + (rel[:-10] if rel.endswith("index.html") else rel)
        parser = References()
        parser.feed(page.read_text(encoding="utf-8"))
        base = urljoin(url, parser.base) if parser.base else url
        for raw, integrity in parser.refs:
            inspect(raw, base, rel, integrity)

    seen_css = set()
    while css_queue:
        file = css_queue.pop()
        if file in seen_css:
            continue
        seen_css.add(file)
        rel = file.relative_to(root).as_posix()
        for raw in CSS_URL.findall(file.read_text(encoding="utf-8")):
            inspect(raw, ORIGIN + "/" + rel, rel)

    return {"pages": len(pages), "targets": len({file for file, _ in checked}),
            "stylesheets": len(seen_css), "errors": errors}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", default="cloudflare-public")
    args = parser.parse_args()
    result = audit(args.root)
    for error in result["errors"]:
        print("SITE_INTEGRITY_ERROR", error)
    print(f"Site integrity: {result['pages']} HTML pages, "
          f"{result['targets']} local targets, {result['stylesheets']} stylesheets, "
          f"{len(result['errors'])} errors")
    raise SystemExit(bool(result["errors"]))
