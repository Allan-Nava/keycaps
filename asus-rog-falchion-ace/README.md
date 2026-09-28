# ASUS ROG Falchion Ace — replacement keycaps (ISO/ITA)

Three keys, none of them stabilised: **left Shift (ISO 1.25u)**, **G (1u)** and
**↑ (1u)**. MX-compatible cross stem, Cherry-like sculpt, for FDM in PLA/PETG.

| key | file | size | row | overall height | STL |
|---|---|---|---|---|---|
| left Shift | `left-shift.scad` | 1.25u | ZXCV | 9.97 mm | `left-shift.stl` |
| ↑ | `arrow-up.scad` | 1u | ZXCV | 9.86 mm | `arrow-up.stl` |
| G | `g.scad` | 1u | home (ASDF) | 8.50 mm | `g.stl` |

All three pass every check — `VALIDATION-<key>.txt`. Shared parameters live in
`profile.inc.scad`; the geometry itself is in [`../lib/keycap_common.scad`](../lib/keycap_common.scad).

```bash
python3 ../tools/build_and_validate.py left-shift.scad
python3 ../tools/make_drawing.py       left-shift.scad
```

---

## 1. What is confirmed, and by what

### From the product photo supplied by the user

The user's board is the **Italian** one. The photo they supplied happens to show
the DE/QWERTZ variant, which they confirmed matches their layout physically —
and it does: ITA and DE differ only in which glyphs are printed on *other* keys
(QWERTZ vs QWERTY, Ü Ö Ä vs Ì Ò À), never in key sizes or positions. For the
three keys modelled here — ⇧, G and ↑ — the two layouts are identical.

The photo settles three things a spec sheet does not:

* **left Shift is 1.25u**, with the extra ISO `<>|` key next to it — so, unlike
  the ANSI 2.25u left Shift in `../ozone-strike-battle/`, **it is not
  stabilised**;
* **↑ sits in the ZXCV row**, to the right of the right Shift, so it takes that
  row's sculpt, not the bottom row's;
* legends on the alphas are centred, and the board is ISO (tall L-shaped Enter).

### From sources

* **ROG NX stem is MX-compatible**: ASUS states the "standard cross-shaped stem
  design ensures compatibility with most keycaps", so the Cherry MX cross
  (4.10 × 1.17) applies. [ROG NX switch page](https://rog.asus.com/content/rog-keyboard-switch/)
* **No LED enters the keycap.** Per-key RGB comes from "centrally placed RGB
  LEDs" on the PCB, shining through the switch's **hollow stem** and its
  transparent polycarbonate upper housing. So there is nothing to clear inside
  the cap — `led_clear_h = 0`, and the validator says so explicitly instead of
  silently skipping. [ROG NX switch page](https://rog.asus.com/content/rog-keyboard-switch/)
* **Cherry profile, PBT doubleshot**, "mid-height keycaps". [ASUS product page](https://rog.asus.com/keyboards/keyboards/compact/rog-falchion-ace-model/),
  [review](https://basic-tutorials.com/reviews/peripherals/asus-rog-falchion-ace/)
* **65 %, 68 keys, 306 mm long.** ASUS product page.
* Cherry MX cross 4.10 × 1.17: the Cherry drawing, via the
  [MX tolerance test](https://www.thingiverse.com/thing:4397634) and
  [Deskthority](https://deskthority.net/viewtopic.php?t=11183).

---

## 2. The profile — how the heights were arrived at

**This is the weak part of the model, and it is cosmetic, not fit-critical.**

ASUS publishes no keycap drawing. The public Cherry-profile guides contradict
each other badly: one gives R1 9.81 / R2 7.85 / R3 7.22 / R4 8.59 mm with the
home row lowest and calls the sculpt spherical (it is cylindrical); another
gives 9.4 / 9.0 / 8.75 / 8.1 mm monotonically decreasing, with the home row
*not* lowest. They cannot both be right and I could not resolve which is.

So the numbers here are built from the one claim both sources agree on —
**Cherry is 1–2 mm lower than OEM across all rows** — plus this repo's own
validated OEM cap:

* `../ozone-strike-battle/left-shift` is a validated OEM ZXCV-row cap at
  **11.39 mm** overall → Cherry ZXCV ≈ 11.39 − 1.5 = **~9.9 mm**. Modelled:
  9.97 (1.25u) / 9.86 (1u).
* The **row-to-row delta** (1.37 mm between ZXCV and home) and the **tilts**
  (12° / 5°) come from the internally coherent source — the one where the home
  row is lowest and the tilt grows away from it, which is how a sculpted
  profile actually behaves. Home row → **8.50 mm** overall.

Every profile number is therefore `[EST]`. If you ever get a caliper on an
original cap, `profile.inc.scad` has `fa_h(row)` and `fa_tilt(row)` at the top —
two lines.

Same for the body size: no measurement exists for this board, so 1u is
**18.10 × 18.10 mm** (the common value for Cherry-profile sets), leaving 0.47 mm
of gap per side inside the 19.05 pitch.

---

## 3. Critical dimensions

mm, origin at the key centre, z = 0 at the bottom rim, +Y towards the back.

| | value | tag |
|---|---|---|
| 1u pitch | 19.05 | SRC |
| body, 1u | 18.10 × 18.10 | EST |
| body, 1.25u (left Shift) | 22.86 × 18.10 | DER |
| gap to the neighbouring caps | 0.47 per side | DER |
| top plate | body − 2 × 2.10 per side | EST |
| row tilt, ZXCV / home | 12° / 5° | EST |
| top plate height at centre, ZXCV / home | 8.52 / 7.99 | EST |
| dish | cylindrical, **axis along Y** (concave left-right), R25, 0.90 deep | EST |
| corner radius, skirt / top | R1.20 / R2.60 | EST |
| top edge chamfer | 0.60 | EST |
| side wall | 1.55 | EST |
| skirt wall (below z = 4.20) | 1.15 | EST |
| roof | 1.70 | EST |
| MX cross, switch side | 4.10 × 1.17 | SRC |
| socket as modelled | 4.22 × 1.39, 4.30 deep | DER |
| stem boss | Ø5.60, from z = 0.50, stopping 0.90 below the top surface | EST |
| stabiliser | none on all three keys | SRC (photo) |
| ribs | none — a 1u/1.25u roof is carried by four close walls | EST |
| legend relief | ⇧ and ↑ raised 0.40; **G engraved 0.40** | EST |

The dish axis differs from the Strike Battle cap on purpose: a 2u+ key is
concave front-to-back, a 1u/1.25u key is concave left-right.

The G is **engraved** rather than raised — it is a key you type on constantly
and a raised glyph is felt under the fingertip. The two arrows are raised, where
the relief doubles as a tactile marker. Either way a single-material FDM print
cannot reproduce the original's doubleshot legend, and **shine-through is not
reproducible at all**: these three caps will be dark while the rest of the board
lights up.

---

## 4. Validation

```
left-shift  22.863 x 18.100 x 9.97   1158.2 mm^3   all checks pass
arrow-up    18.100 x 18.100 x 9.86    957.9 mm^3   all checks pass
g           18.100 x 18.100 x 8.50    878.9 mm^3   all checks pass
```

For all three: watertight single solid (euler 2), a nominal 4.10 × 1.17 MX
cross enters with zero interference while a +0.30 probe does clash, socket
centred to 0.000, interior never tighter than a stock cap of the same sculpt,
**0.0 mm² of overhang past 45°**, and the dish bridged over the bed from its
own rim.

---

## 5. Printing

The STLs are already oriented: top plate flat on the bed, open side up, no
supports. Settings are the same as
[`../ozone-strike-battle/README.md` §5](../ozone-strike-battle/README.md):
**0.12 mm layers, 3 walls, 100 % infill**, 5 mm brim. These caps are small
(~1 cm³ each), so print all three at once.

Test the stem on a spare switch before printing the set. Too tight → raise
`cross_clr_w` / `cross_clr_t` by 0.05 in `profile.inc.scad`; too loose → lower
them. ROG NX is advertised with a "shorter stem", which the 4.30 mm socket
depth accommodates (a deeper socket is harmless); if the caps feel wobbly on
the switch rather than loose on the cross, that is the switch, not this model.

---

## 6. Still open

* **No original cap was measured** — the user asked for a model built from
  online sources only. The profile (§2) and the body size are the part that
  would change if one ever is measured.
* **The other Cherry-profile rows** are not defined: `fa_h()` / `fa_tilt()`
  only cover rows 3 and 4. Adding the number row or the bottom row means
  extending those two functions.
* **Stabilised keys on this board** (space, Backspace, right Shift, ISO Enter)
  still need the Cherry-style stabiliser stem, which `lib/keycap_common.scad`
  deliberately does not implement. See the root README.
