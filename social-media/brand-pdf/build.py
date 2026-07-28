#!/usr/bin/env python3
"""Render the Dominate Solutions brand PDF from index.html using headless Chromium.

Usage:  python3 build.py
Requires: playwright (pip install playwright) and a Chromium build.
Output:  Dominate-Solutions-Overview.pdf
"""
import os, glob, pathlib
from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).parent
html = (HERE / "index.html").resolve().as_uri()

def find_chromium():
    for pat in ["/opt/pw-browsers/chromium-*/chrome-linux/chrome",
                "/opt/pw-browsers/chromium/chrome-linux/chrome"]:
        hits = sorted(glob.glob(pat))
        if hits:
            return hits[-1]
    return None  # let Playwright use its default download

def main():
    exe = find_chromium()
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=exe, args=["--no-sandbox"])
        page = browser.new_page()
        page.goto(html, wait_until="networkidle")
        page.emulate_media(media="print")
        page.pdf(path=str(HERE / "Dominate-Solutions-Overview.pdf"),
                 width="8.5in", height="11in",
                 print_background=True, prefer_css_page_size=True)
        browser.close()
    print("Wrote Dominate-Solutions-Overview.pdf")

if __name__ == "__main__":
    main()
