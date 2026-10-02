#!/usr/bin/env python3
"""
Build the GitHub Pages site into site/.

Everything on the page comes from files the validator wrote or from the .scad
sources themselves: dimensions, weights, check results and the provenance
counts are read, never retyped. A page that restates numbers by hand goes
stale the first time a model changes, and a stale spec sheet is worse than no
spec sheet.

Usage:  python3 tools/make_site.py [outdir]
"""

import html
import json
import os
import re
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from list_keys import keys                                      # noqa: E402

REPO = "https://github.com/Allan-Nava/keycaps"
TAGS = ("SRC", "DER", "EST", "FIT")
TAG_WORDS = {
    "SRC": "sourced",
    "DER": "derived",
    "EST": "estimated",
    "FIT": "unverifiable — measure it",
}


# --------------------------------------------------------------- gathering --
def scad_blurb(path):
    """Title and first paragraph out of the .scad header comment."""
    title, para, seen = None, [], False
    for raw in open(path, encoding="utf-8"):
        line = raw.rstrip("\n")
        if not line.startswith("//"):
            break
        body = line[2:].strip()
        if set(body) <= {"=", "-", ""} and body:
            continue
        if not body:
            if seen:
                break
            continue
        if title is None:
            title = body
            seen = True
        else:
            para.append(body)
    return title or os.path.basename(path), " ".join(para)


ASSIGN = re.compile(r"^\s*\w+\s*=")


def provenance(path):
    """Count provenance tags on PARAMETER lines only.

    A file's header comment explains what the tags mean, so counting every
    occurrence in the text adds one phantom dimension per tag per file. Only a
    line that actually assigns something is a dimension.
    """
    counts = {t: 0 for t in TAGS}
    for line in open(path, encoding="utf-8"):
        if not ASSIGN.match(line):
            continue
        for t in TAGS:
            if f"[{t}]" in line:
                counts[t] += 1
    return counts


def collect():
    boards = {}
    for rel in keys():
        board, fname = os.path.split(rel)
        stem = os.path.splitext(fname)[0]
        jpath = os.path.join(ROOT, board, stem + ".json")
        if not os.path.exists(jpath):
            print(f"  ! {rel}: no {stem}.json - run build_and_validate first",
                  file=sys.stderr)
            continue
        facts = json.load(open(jpath, encoding="utf-8"))
        src = os.path.join(ROOT, rel)
        facts["title"], facts["blurb"] = scad_blurb(src)
        facts["provenance"] = provenance(src)
        facts["rel"] = rel
        facts["stem"] = stem
        facts["assets"] = {}
        for label, suffix in (("stl", ".stl"),
                              ("svg", "-drawing.svg"),
                              ("pdf", "-drawing.pdf"),
                              ("top", "-preview-top.png"),
                              ("under", "-preview-underside.png")):
            p = os.path.join(ROOT, board, stem + suffix)
            if os.path.exists(p):
                facts["assets"][label] = p
        boards.setdefault(board, []).append(facts)
    return boards


def photos():
    """Images in photos/, newest name last. Data-driven: drop a file in and it
    appears, so the page cannot claim a print that is not there."""
    d = os.path.join(ROOT, "photos")
    if not os.path.isdir(d):
        return []
    return [os.path.join(d, f) for f in sorted(os.listdir(d))
            if f.lower().endswith((".webp", ".jpg", ".jpeg", ".png"))]


def board_title(board):
    path = os.path.join(ROOT, board, "README.md")
    if os.path.exists(path):
        for line in open(path, encoding="utf-8"):
            if line.startswith("# "):
                return line[2:].strip()
    return board


# ------------------------------------------------------------------ markup --
CSS = """
:root{
  --bg:#fbfbfa; --panel:#fff; --ink:#1b1b19; --muted:#6b6b66;
  --line:#e4e3df; --accent:#8a4b2a; --ok:#2f6f3e; --warn:#8a6d1f;
  --mono:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;
}
@media (prefers-color-scheme:dark){
  :root{ --bg:#141413; --panel:#1c1c1a; --ink:#ecebe6; --muted:#9b9a93;
         --line:#2e2e2b; --accent:#d29468; --ok:#6fbd80; --warn:#d9bb63; }
}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);
  font:16px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;
  -webkit-font-smoothing:antialiased}
.wrap{max-width:1040px;margin:0 auto;padding:0 20px}
header{border-bottom:1px solid var(--line);padding:56px 0 40px;margin-bottom:8px}
h1{font-size:2.1rem;margin:0 0 .3em;letter-spacing:-.02em}
h2{font-size:1.35rem;margin:2.4em 0 .2em;letter-spacing:-.01em}
h3{font-size:1.02rem;margin:0 0 .15em}
.sub{color:var(--muted);max-width:60ch;margin:0}
.lede{max-width:66ch}
a{color:var(--accent)}
.bar{display:flex;gap:10px;flex-wrap:wrap;margin-top:22px}
.btn{display:inline-block;padding:7px 13px;border:1px solid var(--line);
  border-radius:7px;background:var(--panel);color:var(--ink);
  text-decoration:none;font-size:.86rem}
.btn:hover{border-color:var(--accent);color:var(--accent)}
.btn.primary{background:var(--accent);border-color:var(--accent);color:#fff}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));
  gap:18px;margin-top:18px}
.card{background:var(--panel);border:1px solid var(--line);border-radius:11px;
  overflow:hidden;display:flex;flex-direction:column}
.shot{background:var(--bg);border-bottom:1px solid var(--line);
  display:flex;align-items:center;justify-content:center;padding:6px}
.shot img{width:100%;height:auto;display:block;max-height:220px;
  object-fit:contain}
.card .body{padding:15px 16px 16px}
.blurb{color:var(--muted);font-size:.84rem;margin:.4em 0 0}
dl{display:grid;grid-template-columns:auto 1fr;gap:2px 14px;
  margin:13px 0 0;font-size:.85rem}
dt{color:var(--muted)}
dd{margin:0;font-family:var(--mono);font-size:.82rem}
.pill{display:inline-block;font-size:.74rem;padding:2px 8px;border-radius:20px;
  border:1px solid var(--line);color:var(--muted)}
.pill.ok{color:var(--ok);border-color:currentColor}
.pill.warn{color:var(--warn);border-color:currentColor}
.tags{display:flex;gap:6px;flex-wrap:wrap;margin-top:11px}
details{margin-top:12px;font-size:.84rem}
summary{cursor:pointer;color:var(--muted)}
details table{width:100%;border-collapse:collapse;margin-top:9px;
  font-size:.78rem}
details td{padding:3px 6px 3px 0;border-bottom:1px solid var(--line);
  vertical-align:top}
details td:first-child{width:1.4em}
.mono{font-family:var(--mono)}
table.spec{width:100%;border-collapse:collapse;margin-top:14px;font-size:.88rem}
table.spec th,table.spec td{text-align:left;padding:7px 10px 7px 0;
  border-bottom:1px solid var(--line)}
table.spec th{color:var(--muted);font-weight:500;font-size:.82rem}
.note{border-left:3px solid var(--warn);padding:2px 0 2px 15px;
  margin:18px 0;color:var(--muted);max-width:66ch}
footer{border-top:1px solid var(--line);margin-top:64px;padding:26px 0 56px;
  color:var(--muted);font-size:.84rem}
"""


def e(x):
    return html.escape(str(x))


def card(k):
    a = k["assets"]
    shot = ""
    if "top" in a:
        shot = (f'<div class="shot"><img loading="lazy" '
                f'src="assets/{e(k["stem"])}-preview-top.png" '
                f'alt="{e(k["title"])}"></div>')

    n_ok = sum(1 for c in k["checks"] if c["kind"] == "check" and c["ok"])
    n_all = sum(1 for c in k["checks"] if c["kind"] == "check")
    status = (f'<span class="pill ok">{n_ok}/{n_all} checks passed</span>'
              if k["passed"] else
              f'<span class="pill warn">{n_all - n_ok} check(s) failing</span>')

    prov = k["provenance"]
    tags = "".join(
        f'<span class="pill">{v} {e(TAG_WORDS[t])}</span>'
        for t, v in prov.items() if v)

    s = k["size_mm"]
    rows = [
        ("size", f'{s["x"]:.2f} × {s["y"]:.2f} × {s["z"]:.2f} mm'),
        ("material", f'{k["volume_mm3"]:.0f} mm³ ≈ {k["pla_grams"]:.2f} g PLA'),
        ("stem", "Cherry MX cross"),
        ("stabiliser", k["parameters"].get("stab_style", "none")),
    ]
    dl = "".join(f"<dt>{e(a_)}</dt><dd>{e(b_)}</dd>" for a_, b_ in rows)

    under = ""
    if "under" in a:
        under = (f'<details><summary>Underside — stem, ribs and mounts'
                 f'</summary><div class="shot"><img loading="lazy" '
                 f'src="assets/{e(k["stem"])}-preview-underside.png" '
                 f'alt="underside of {e(k["title"])}"></div></details>')

    checks = "".join(
        f'<tr><td>{"✓" if c["ok"] else ("·" if c["ok"] is None else "✗")}</td>'
        f'<td>{e(c["name"])}</td><td class="mono">{e(c["detail"])}</td></tr>'
        for c in k["checks"])

    links = [f'<a class="btn primary" href="assets/{e(k["stem"])}.stl" '
             f'download>Download STL</a>']
    if "svg" in a:
        links.append(f'<a class="btn" href="assets/{e(k["stem"])}-drawing.svg" '
                     f'target="_blank" rel="noopener">Drawing</a>')
    if "pdf" in a:
        links.append(f'<a class="btn" href="assets/{e(k["stem"])}-drawing.pdf" '
                     f'target="_blank" rel="noopener">PDF</a>')
    links.append(f'<a class="btn" href="{REPO}/blob/main/{e(k["rel"])}">'
                 f'Source</a>')

    return f"""<article class="card">{shot}<div class="body">
<h3>{e(k["title"])}</h3>
<p class="blurb">{e(k["blurb"][:230])}</p>
<dl>{dl}</dl>
<div class="tags">{status}{tags}</div>
{under}
<details><summary>All {n_all} checks</summary>
<table>{checks}</table></details>
<div class="bar">{"".join(links)}</div>
</div></article>"""


def build(outdir):
    boards = collect()
    if not boards:
        print("nothing to publish", file=sys.stderr)
        return 1

    assets = os.path.join(outdir, "assets")
    shutil.rmtree(outdir, ignore_errors=True)
    os.makedirs(assets, exist_ok=True)

    total_keys = 0
    for board, items in boards.items():
        for k in items:
            total_keys += 1
            for path in k["assets"].values():
                shutil.copy2(path, os.path.join(assets,
                                                os.path.basename(path)))

    shots = photos()
    for path in shots:
        shutil.copy2(path, os.path.join(assets, os.path.basename(path)))

    sections = []
    for board in sorted(boards):
        items = sorted(boards[board], key=lambda k: k["stem"])
        sections.append(
            f'<h2 id="{e(board)}">{e(board_title(board))}</h2>'
            f'<p class="sub"><a href="{REPO}/blob/main/{e(board)}/README.md">'
            f'Provenance of every dimension, and what could not be verified '
            f'→</a></p>'
            f'<div class="grid">{"".join(card(k) for k in items)}</div>')

    all_prov = {t: 0 for t in TAGS}
    for items in boards.values():
        for k in items:
            for t in TAGS:
                all_prov[t] += k["provenance"][t]

    if shots:
        imgs = "".join(
            f'<div class="card"><div class="shot"><img loading="lazy" '
            f'src="assets/{e(os.path.basename(p))}" '
            f'alt="a printed keycap on the build plate"></div></div>'
            for p in shots)
        printed_block = f"""
<h2>Printed</h2>
<p class="lede">Everything above is geometry: a solid is rendered, boolean
probes are pushed into it, and the numbers are recorded. That catches a great
deal and it cannot catch anything that only exists once plastic cools.</p>
<div class="grid">{imgs}</div>
<p class="note">A photo is not a check — it is the thing a check cannot be.
These prove the geometry is sliceable, that the committed orientation works
and that no support was needed, which is what the checks predicted. They do
<strong>not</strong> prove the cap seats on a real switch, and that is the row
that matters: until one has, the stem clearances are still the estimates the
provenance tables say they are.</p>"""
    else:
        printed_block = ""

    page = f"""<!DOCTYPE html>
<html lang="en"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>keycaps — 3D-printable replacement keycaps</title>
<meta name="description" content="Replacement mechanical-keyboard keycaps,
parametric in OpenSCAD. Every dimension carries its provenance and the
geometry is validated with boolean probes before it is sliced.">
<style>{CSS}</style>
</head><body>
<header><div class="wrap">
<h1>keycaps</h1>
<p class="sub">Replacement mechanical-keyboard keycaps, parametric in
OpenSCAD. {total_keys} models, each one rendered and geometrically validated
in CI before it gets here.</p>
<div class="bar">
<a class="btn primary" href="{REPO}">Repository</a>
<a class="btn" href="{REPO}/actions/workflows/validate.yml">CI status</a>
<a class="btn" href="{REPO}/blob/main/LICENSE">MIT</a>
</div></div></header>

<div class="wrap">

<h2>Why this exists</h2>
<p class="lede">Replacement keycaps fail for boring reasons: a stem 0.1 mm too
tight, a stabiliser hook half a millimetre too high, a skirt that rubs the
switch housing. So nothing here is asserted that was not found. Every
dimension in every model carries a tag — <strong>sourced</strong> from a
document, <strong>derived</strong> from one, a standard-value
<strong>estimate</strong>, or fit-critical <em>and</em> impossible to verify
online, in which case it says so and tells you to reach for a caliper.</p>
<p class="lede">Across the models published here that comes to
<strong>{all_prov["SRC"]} sourced</strong>,
<strong>{all_prov["DER"]} derived</strong>,
<strong>{all_prov["EST"]} estimated</strong> and
<strong>{all_prov["FIT"]} unverifiable</strong> dimensions. The counts are
read out of the sources, not claimed.</p>
<p class="lede">Checks are boolean probes, not eyeballing: a solid shaped like
a real Cherry MX cross is pushed into the socket and the interference volume
is measured. A second CI workflow breaks each model on purpose to prove those
checks can actually fail — a check that never fails is decoration.</p>

{"".join(sections)}

{printed_block}

<h2>Printing</h2>
<p class="lede">Every STL is already oriented: top plate flat on the bed, open
side up, <strong>no supports</strong>. The dish is a shallow pocket sitting on
the bed and bridges from its own rim.</p>
<table class="spec">
<tr><th>layer height</th><td>0.12 mm (0.16 acceptable), first layer 0.20</td></tr>
<tr><th>walls</th><td>3 perimeters — matches the 1.15 mm skirt and the
1.55 mm wall without leaving gaps</td></tr>
<tr><th>infill</th><td>100 % — the part is nearly all perimeters, so this only
fills the stem boss where the strength is needed</td></tr>
<tr><th>supports</th><td>none</td></tr>
<tr><th>brim</th><td>5 mm; the bed contact is only the top-plate rim</td></tr>
<tr><th>PLA</th><td>205–215 °C, bed 60 °C, 100 % cooling from layer 3</td></tr>
<tr><th>PETG</th><td>230–245 °C, 50 % cooling, and add 0.05 mm to the stem
clearances — PETG swells more on the way out of the nozzle</td></tr>
</table>
<p class="note">Test-fit one print on a spare switch before committing to a
set. Too tight or too loose is two parameters at the top of the source, not a
redesign.</p>

<h2>What is not guaranteed</h2>
<p class="lede">Several dimensions in every model are estimates, and each
keyboard's README says exactly which ones and why. Where a fit-critical
dimension could not be established from any public document, it is marked and
left for you to measure rather than invented. Shine-through legends cannot be
reproduced in single-material FDM at all, so a printed cap stays dark on a
backlit board.</p>

</div>
<footer><div class="wrap">
Generated from the validator's own output by
<a href="{REPO}/blob/main/tools/make_site.py">tools/make_site.py</a> — the
numbers on this page are the numbers the checks measured.
· <a href="{REPO}">source</a> · MIT
</div></footer>
</body></html>
"""

    with open(os.path.join(outdir, "index.html"), "w", encoding="utf-8") as fh:
        fh.write(page)
    open(os.path.join(outdir, ".nojekyll"), "w").close()

    size = sum(os.path.getsize(os.path.join(dp, f))
               for dp, _, fs in os.walk(outdir) for f in fs)
    print(f"wrote {outdir}/ - {total_keys} keycaps, "
          f"{len(os.listdir(assets))} assets, {size / 1e6:.1f} MB")
    return 0


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "site")
    sys.exit(build(out))
