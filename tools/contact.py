#!/usr/bin/env python3
"""Regenerate contact.vcf and img/qr.svg from the data below.

Run after changing contact details:  pip install segno && python3 tools/contact.py
"""
import base64
import pathlib
import textwrap

import segno

ROOT = pathlib.Path(__file__).resolve().parent.parent

FIRST, LAST = "Ivan", "Kuleshov"
TITLE = "Head of Hardware, Serial Founder, Hacker"
EMAIL = "merocle@gmail.com"
SITE = "https://merocle.com/"
SOCIAL = [  # (label, type for X-SOCIALPROFILE, url)
    ("LinkedIn", "linkedin", "https://www.linkedin.com/in/merocle/"),
    ("Telegram", "telegram", "https://t.me/ASCII"),
    ("GitHub", "github", "https://github.com/merocle"),
    ("X", "twitter", "https://x.com/Merocle"),
    ("Instagram", "instagram", "https://www.instagram.com/uptime.lab/"),
]


def fold(line: str) -> str:
    """RFC 6350 line folding at 75 octets."""
    if len(line) <= 75:
        return line
    head, rest = line[:75], line[75:]
    return head + "".join("\r\n " + c for c in textwrap.wrap(rest, 74, break_on_hyphens=False, break_long_words=True))


def vcard(full: bool) -> str:
    lines = [
        "BEGIN:VCARD",
        "VERSION:3.0",
        f"N:{LAST};{FIRST};;;",
        f"FN:{FIRST} {LAST}",
        f"TITLE:{TITLE.replace(',', chr(92) + ',')}",
        f"EMAIL;TYPE=INTERNET:{EMAIL}",
        f"URL:{SITE}",
    ]
    if full:
        for i, (label, kind, url) in enumerate(SOCIAL, 1):
            lines += [f"item{i}.URL:{url}", f"item{i}.X-ABLabel:{label}"]
            lines.append(f"X-SOCIALPROFILE;TYPE={kind}:{url}")
        photo = base64.b64encode((ROOT / "img/avatar.jpg").read_bytes()).decode()
        lines.append(f"PHOTO;ENCODING=b;TYPE=JPEG:{photo}")
    lines.append("END:VCARD")
    return "\r\n".join(fold(l) for l in lines) + "\r\n"


# Full card (photo + all links) — downloaded by the "Save contact" button.
(ROOT / "contact.vcf").write_text(vcard(full=True), newline="")

# Compact card in the QR itself, so scanning works offline and stays easy to read.
qr = segno.make(vcard(full=False), error="l")
qr.save(ROOT / "img/qr.svg", kind="svg", scale=1, border=0, dark="#000", xmldecl=False, svgns=True,
        svgclass=None, lineclass=None, nl=False)
n = qr.symbol_size(scale=1, border=0)[0]
svg = (ROOT / "img/qr.svg").read_text()
svg = svg.replace(f'width="{n}" height="{n}"', f'viewBox="0 0 {n} {n}" shape-rendering="crispEdges"', 1)
(ROOT / "img/qr.svg").write_text(svg)
print(f"contact.vcf + img/qr.svg written (QR version {qr.version}, {qr.symbol_size(scale=1, border=0)[0]} modules)")
