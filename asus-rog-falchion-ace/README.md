# ASUS ROG Falchion Ace — replacement keycap (ITA layout)

**Status: scaffold only. No research done, no model, nothing here is verified.**

This file exists so the next session starts from the open questions instead of
from a blank page. Nothing below is a measurement — it is a list of what has to
be established before a single dimension is written.

## What was stated

* Keyboard: ASUS ROG Falchion Ace
* Switches: ROG NX
* Layout: **ITA** (Italian, ISO)
* Described as "TKL 60%"

## Open questions — answer these first

### 1. Form factor ⚠️

The Falchion Ace is normally described as a **65 %** board (68 keys, with a
dedicated arrow cluster and a right-hand column), **not** a 60 % and not a TKL.
This matters because it changes which keys exist and which ones are stabilised.
**Confirm against the actual keyboard before modelling anything.**

### 2. Which key?

Not yet specified. The answer decides almost everything:

* a 1u alpha → `stab_style = "none"`, easy;
* **ISO Enter** → 1.5u wide × 2u tall, L-shaped, stabilised, and the hardest
  cap on the board to print;
* **ISO left Shift** (1.25u) → unstabilised, unlike the ANSI 2.25u one;
* right Shift / Backspace / Space → stabilised.

Note the ITA/ISO specifics: ISO left Shift is **1.25u**, ISO Enter is the tall
L shape, and there is an extra key next to left Shift that ANSI does not have.
Do not reuse the ANSI Shift reasoning from `ozone-strike-battle/`.

### 3. Stabiliser style ⚠️ blocking

Modern ASUS boards almost certainly use **Cherry-style clip-in plastic
stabiliser stems**, not Costar wire. `lib/keycap_common.scad` implements
`"costar"` only — `"cherry"` is deliberately missing because the housing and
stem dimensions have to be measured or sourced first.

So either the chosen key is unstabilised, or the Cherry stabiliser stem has to
be added to the library, with its own provenance.

### 4. ROG NX stem

ROG NX switches are MX-compatible in principle, so the `cross_w` / `cross_t`
4.10 × 1.17 from the Cherry drawing should carry over — **but confirm**, and
confirm the stem height, since it sets `cross_depth`.

### 5. Profile

ASUS does not publish a keycap profile for this board. Needs: cap heights,
row sculpt, whether the top is cylindrical or spherical, and the plastic body
size versus the 19.05 pitch. Same method as the Strike Battle: find a review
that *measured* something, and reconcile the gap from it.

### 6. Backlight

The Falchion Ace is RGB — check whether the LED is SMD (under the switch, no
clearance problem) or a north-facing in-switch LED (needs the clearance the
Strike Battle cap has). Shine-through legends are not reproducible in
single-material FDM; say so rather than pretending.

## When starting

```bash
cp ../ozone-strike-battle/left-shift.scad ./<key>.scad
```

then strip it to the parameters that genuinely differ, and keep the provenance
tags honest. See the root [README](../README.md), "Adding a key".
