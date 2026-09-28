# keycaps

Replacement keycaps for mechanical keyboards, modelled parametrically in
OpenSCAD, validated geometrically before anything gets sliced, and documented
with the provenance of every single dimension.

## Why it is built this way

Replacement keycaps fail for boring reasons: a stem 0.1 mm too tight, a
stabiliser hook 0.5 mm too high, a skirt that rubs the switch housing. So the
rule here is:

* **every dimension carries a provenance tag** — `[SRC]` from a source,
  `[DER]` derived from one, `[EST]` closest standard value, `[FIT]` fit-critical
  *and* unverifiable online, so it has to be measured off the original part;
* **nothing is asserted that was not found** — if a number could not be sourced
  it is marked as an estimate, never dressed up as confirmed;
* **checks are boolean probes, not eyeballing** — a solid shaped like a real MX
  cross is pushed into the socket and the interference volume is measured;
* **the drawing is generated from the rendered solid**, and the Python tooling
  reads its dimensions back out of the render, so neither can drift from the
  model.

## Layout

```
lib/keycap_common.scad      shared geometry: shell, dish, sculpt, MX cross
                            socket, Costar hook, ribs, relief legends
tools/build_and_validate.py render + write the print-ready STL + 20 checks
tools/make_drawing.py       dimensioned 4-view drawing from the solid
tools/scadparams.py         reads ##PARAM echoes back out of a render

<keyboard>/<key>.scad       parameters + provenance for one key
<keyboard>/<key>.stl        production STL, already in print orientation
<keyboard>/<key>-drawing.*  svg / pdf / png
<keyboard>/README.md        provenance, critical dimensions, print settings
<keyboard>/VALIDATION.txt   output of the last validation run
```

## Keyboards

| keyboard | key | status |
|---|---|---|
| [`ozone-strike-battle`](ozone-strike-battle/) | left Shift, ANSI 2.25u | **done** — all checks pass; one `[FIT]` dimension to measure before printing |
| [`asus-rog-falchion-ace`](asus-rog-falchion-ace/) | left Shift ISO 1.25u, G, ↑ — ITA layout | **done** — all checks pass; profile is estimated, nothing was measured |

## Usage

```bash
python3 tools/build_and_validate.py ozone-strike-battle/left-shift.scad
python3 tools/make_drawing.py       ozone-strike-battle/left-shift.scad
```

Or `make` (builds and validates everything, then the drawings).

### Requirements

* `openscad` with the manifold backend. On macOS the stable cask is disabled
  (Gatekeeper), so use the snapshot: `brew install --cask openscad@snapshot`
* Python: `trimesh manifold3d numpy rtree matplotlib`

```bash
python3 -m venv .venv && .venv/bin/pip install trimesh manifold3d numpy rtree matplotlib
```

## Adding a key

1. `cp ozone-strike-battle/left-shift.scad <keyboard>/<key>.scad` and strip it
   back to the parameters that actually differ. With more than one key on the
   same board, put the shared parameters in `<keyboard>/profile.inc.scad` —
   files matching `*.inc.scad` are not treated as keys by the tools.
2. Override only what you know. Anything left at the library default is an
   estimate by definition — tag it `[EST]` and say so in the README.
3. Run the validator. It refuses to pass on an unimplemented stabiliser style
   rather than silently skipping the check.
4. Write `<keyboard>/README.md` with the provenance table, and list what could
   **not** be verified. That section is the point of the repo.

## Two OpenSCAD traps this repo walked into

**An included file's *variable* cannot be referenced from an assignment in the
including file.** OpenSCAD reports `Ignoring unknown variable` and leaves
`undef`, which then propagates silently through the whole model. A *function*
from the same include resolves fine, which is why per-row values are exposed as
`fa_h(row)` / `fa_tilt(row)` rather than `FA_R4_H`. Module arguments
(`text(font = fa_font())`) are evaluated later and are also fine.

**A relief legend whose outline is tangent to the stem boss's cylindrical seam
produces sliver faces and a non-manifold mesh** — clean in OpenSCAD's own
report, broken on reload. That is why `stem_top_gap` stops the boss 0.90 mm
below the top surface: the boss stays fused to the roof and its seam never
reaches the surface where a legend sits.

## Licence

[MIT](LICENSE) — the OpenSCAD sources, the Python tooling and the generated
STLs alike. Print them, sell the prints, fork the lot; just keep the notice.

**No warranty, and that matters here more than usual**: several dimensions in
every model are estimates, and each keyboard's README says exactly which ones.
Test-fit a print on a spare switch before committing to a set.

## Stabiliser styles

`lib/keycap_common.scad` implements:

* `"none"` — 1u keys and anything unstabilised.
* `"costar"` — wire stabiliser with integrated hooks, so the original white
  Costar inserts are not needed. Used by the Strike Battle.

`"cherry"` (clip-in plastic stabiliser stems, what most modern boards use) is
deliberately **not implemented**: the housing and stem dimensions have to be
measured or sourced first. A wrong stabiliser stem binds the key, so it is
better to have nothing there than a plausible guess.
