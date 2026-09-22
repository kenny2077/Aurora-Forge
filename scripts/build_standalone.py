#!/usr/bin/env python3
"""Rebuild the root standalone copies from the live site in docs/.

docs/ is the source of truth (served by GitHub Pages). The root copies are
self-contained, content-only pages (no <!doctype>/<head> wrapper) used for
claude.ai artifacts: forge.css and forge.js are inlined and relative links are
rewritten to absolute Pages URLs so they work outside the repo.

Run after every change to docs/:  python3 scripts/build_standalone.py
"""
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, "docs")
BASE = "https://kenny2077.github.io/Aurora-Forge/"
PAGES = {
    "index.html": "fundamentals_exam.html",
    "swe.html": "swe_problems.html",
    "days.html": "agentic_interview_site.html",
}
LINKS = {'"./#warmup"': f'"{BASE}#warmup"', '"./"': f'"{BASE}"',
         '"swe.html"': f'"{BASE}swe.html"', '"days.html"': f'"{BASE}days.html"'}


def read(name):
    with open(os.path.join(DOCS, name), encoding="utf-8") as f:
        return f.read()


def build(src):
    html = read(src)
    css, js = read("forge.css"), read("forge.js")
    head = re.search(r"<head>(.*?)</head>", html, re.S).group(1)
    body = re.search(r"<body>(.*?)</body>", html, re.S).group(1)
    # keep the title, font links and page styles; the artifact host supplies charset/viewport
    keep = re.findall(r"<title>.*?</title>|<link rel=\"(?:preconnect|stylesheet)\"[^>]*>|<style>.*?</style>", head, re.S)
    keep = [k for k in keep if 'href="forge.css"' not in k]
    tags = [k for k in keep if not k.startswith("<style>")]
    page_styles = [k for k in keep if k.startswith("<style>")]
    # shared CSS first so each page's own <style> still overrides it, as in docs/
    out = "\n".join([*tags, f"<style>\n{css}</style>", *page_styles, body.strip()]) + "\n"
    out = out.replace('<script src="forge.js"></script>', f"<script>\n{js}</script>")
    for a, b in LINKS.items():
        out = out.replace(a, b)
    return out


if __name__ == "__main__":
    for src, dst in PAGES.items():
        text = build(src)
        assert "forge.css" not in text and 'src="forge.js"' not in text, dst
        with open(os.path.join(ROOT, dst), "w", encoding="utf-8") as f:
            f.write(text)
        print(f"docs/{src} -> {dst} ({len(text) // 1024} KB)")
