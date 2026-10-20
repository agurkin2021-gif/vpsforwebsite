#!/usr/bin/env python3
"""Check recovered French guide parity with the published English source.

This checks stable structure and interactive contracts, not linguistic quality.
Run after the Hugo build and recovery overlay:
    python3 scripts/audit-french-parity.py cloudflare-public
"""
from collections import Counter
from html import unescape
from pathlib import Path
import re
import sys

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else "cloudflare-public")
PAIRS = (
    ("fr/strategie-sauvegarde-vps/", "vps-backup-strategy/"),
    ("fr/vps-pour-plusieurs-sites/", "vps-for-multiple-websites/"),
)
TAGS = ("h1", "h2", "h3", "li", "table", "tr", "th", "td",
        "form", "select", "option", "script")
PARTNER_URL = "https://www.vdsina.com/?partner=ni8gzrvz75"
ATTRS = re.compile(r'([\w:-]+)\s*=\s*(?:"([^"]*)"|\'([^\']*)\'|([^\s>]+))', re.I)
MAIN = re.compile(r'<main\b[^>]*>([\s\S]*?)</main>', re.I)
HEADING = re.compile(r'<h[23]\b[^>]*>', re.I)
OPTION = re.compile(r'<option\b[^>]*>', re.I)
ANCHOR = re.compile(r'<a\b[^>]*>', re.I)


def attributes(tag):
    return {key.lower(): (v1 or v2 or v3) for key, v1, v2, v3 in ATTRS.findall(tag)}


def extract(html):
    result = MAIN.search(html)
    if not result:
        raise ValueError("Missing main content")
    main = result.group(1)
    counts = Counter({tag: len(re.findall(r"<" + tag + r"\b", main, re.I))
                      for tag in TAGS})
    headings = [attributes(tag).get("id", "") for tag in HEADING.findall(main)]
    options = [attributes(tag).get("value", "") for tag in OPTION.findall(main)]
    affiliates = [
        attributes(tag) for tag in ANCHOR.findall(main)
        if attributes(tag).get("href") == PARTNER_URL
    ]
    return main, counts, headings, options, affiliates


problems = []
for fr_slug, en_slug in PAIRS:
    fr_file = ROOT / fr_slug / "index.html"
    en_file = ROOT / en_slug / "index.html"
    if not fr_file.is_file() or not en_file.is_file():
        problems.append(f"{fr_slug}: source/target HTML missing")
        continue

    fr_html = fr_file.read_text(encoding="utf-8")
    en_html = en_file.read_text(encoding="utf-8")
    try:
        fr, fr_counts, fr_ids, fr_options, fr_affiliates = extract(fr_html)
        en, en_counts, en_ids, en_options, en_affiliates = extract(en_html)
    except ValueError as error:
        problems.append(f"{fr_slug}: {error}")
        continue

    for tag in TAGS:
        if fr_counts[tag] != en_counts[tag]:
            problems.append(
                f"{fr_slug}: <{tag}> count {fr_counts[tag]} vs EN {en_counts[tag]}"
            )
    if fr_ids != en_ids:
        problems.append(f"{fr_slug}: section heading IDs differ from English")
    if fr_options != en_options:
        problems.append(f"{fr_slug}: checker option values differ from English")
    if len(fr_affiliates) != len(en_affiliates):
        problems.append(f"{fr_slug}: affiliate-link count differs from English")
    for link in fr_affiliates:
        if not {"sponsored", "nofollow"}.issubset(link.get("rel", "").split()):
            problems.append(f"{fr_slug}: affiliate link lacks rel=sponsored nofollow")
    if not re.search(r'<html\b[^>]*\blang="fr"', fr_html, re.I):
        problems.append(f"{fr_slug}: wrong page language")

    if fr_slug.endswith("strategie-sauvegarde-vps/"):
        if "Exercice de restauration" not in fr or "RTO" not in fr:
            problems.append(f"{fr_slug}: untranslated backup hero or RTO")
    if fr_slug.endswith("vps-pour-plusieurs-sites/"):
        for value in ("1 To", "32 To", "0,07", "0,50", "0,67", "1,34"):
            if value not in fr:
                problems.append(f"{fr_slug}: missing reference tier fact {value}")

    print(
        f"FRENCH_PARITY {fr_slug} headings={fr_counts['h2'] + fr_counts['h3']}"
        f" lists={fr_counts['li']} rows={fr_counts['tr']}"
        f" select_options={fr_counts['option']} affiliate={len(fr_affiliates)}"
    )

if problems:
    for p in problems:
        print("FRENCH_PARITY_ERROR", p, file=sys.stderr)
    raise SystemExit(1)
print("French reference parity passed:", len(PAIRS), "pages")
