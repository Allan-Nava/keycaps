# Ozone Strike Battle — replacement LEFT SHIFT keycap

Cherry MX cross stem, OEM-like sculpt, designed for FDM in PLA / PETG.
**Two variants, and they are not interchangeable — pick by your layout:**

| variant | file | size | stabiliser | fits |
|---|---|---|---|---|
| **ISO** | `left-shift-iso.stl` | **1.25u**, 22.85 × 18.10 × 11.39 | **none** | ITA / UK / DE — a `<>` or `\|` key sits next to the left Shift, and the Enter is the tall L |
| ANSI | `left-shift-ansi.stl` | 2.25u, 41.90 × 18.10 × 11.39 | Costar wire, integrated hooks | US — Z is directly next to the left Shift, and the Enter is a flat 2.25u bar |

The board this was built for is an **ISO Italian** Strike Battle. ITA, UK and DE
share the same 1.25u left Shift — only the glyph on the key next to it differs
(`<>` on ITA, `\|` on UK) — so the ISO cap covers all three.

Look at your own board before printing. On an ISO keyboard the left Shift is
split into a 1.25u Shift plus the extra `<>` key, so it is short and carries no
stabiliser at all; on ANSI it is one 2.25u key on a 2u Costar wire.

The **ISO cap is the simpler of the two**: no stabiliser means the one
fit-critical, unverifiable dimension of the ANSI cap (§1) does not exist for it.
If you are on ISO, you can print straight away.

| file | what it is |
|---|---|
| `left-shift-iso.*` / `left-shift-ansi.*` | STL, parametric source, dimensioned drawing, renders |
| `VALIDATION-left-shift-iso.txt` / `-ansi.txt` | validation output — **ALL CHECKS PASSED** for both |

Rebuild:

```bash
python3 ../tools/build_and_validate.py left-shift-iso.scad
python3 ../tools/make_drawing.py       left-shift-iso.scad
```

Everything below — provenance, profile, print settings — applies to both caps.
The parts that are specific to the Costar stabiliser are marked as such and are
simply absent from the ISO variant.

---

## 1. ANSI variant only — the one dimension I could not verify

*(The ISO 1.25u cap has no stabiliser, so none of this section applies to it.)*

**`wire_z = 4.20 mm`** — the height of the Costar wire stub above the bottom rim
of the keycap. This is the single fit-critical dimension that is **not documented
anywhere online**, not for the Strike Battle and not for Costar stabilisers in
general. I did not find a drawing, a datasheet or a measured teardown.

If it is wrong, the Shift key will bind or the wire will not seat.

**Measure it on your original cap** (or on the keyboard, with the stabiliser
installed and the cap off): the distance from the plane of the keycap's bottom
rim to the centre of the horizontal wire stub. Then edit one line:

```openscad
wire_z       = 4.20;    // <- your measurement
```

and re-render. Everything else in the stabiliser interface (bore, throat,
lead-in, block) follows from it automatically.

Two related things I also could not confirm, and how the design sidesteps them:

* **Whether the original Ozone cap uses separate white Costar inserts or moulded-in
  hooks.** The Deskthority Costar page shows Filco inserts but gives no
  dimensions, and no Strike Battle underside teardown photo with measurements
  exists that I could find. → This design uses **integrated hooks**, so you do
  not need the original inserts at all. If you would rather reuse them, the hook
  block is a single module in the `.scad` and can be replaced with a pocket.
* **Which way the wire stub points** (inwards, towards the key centre, or
  outwards). → The bore is a **through-hole along X across the whole hook block**,
  so it works either way.

---

## 2. Critical dimensions

All in mm. Origin = key centre, z = 0 at the bottom rim of the skirt, +Y towards
the back of the keyboard.

### Outside

| dimension | value | tag |
|---|---|---|
| 1u pitch | 19.05 | SRC |
| key size | 2.25u → 42.8625 pitch | SRC |
| body width (plastic) | **41.90** | DER |
| body depth (plastic) | **18.10** | DER |
| gap to Caps Lock / Z | 0.48 per side | DER |
| height at the key centre (top of the dish) | 9.60 | EST |
| overall height (highest point, at the back edge) | 11.39 *(measured on the solid)* | DER |
| row tilt (back edge higher) | 6° | EST |
| top plate | 37.70 × 13.90 | EST |
| side draft | 2.10 per side over 10.05 → ~11.8° | EST |
| corner radius, skirt / top | R1.20 / R2.60 | EST |
| top edge chamfer | 0.60 | EST |
| dish | cylindrical, R28, 1.05 deep, axis along X | EST |
| legend | embossed up-arrow, 0.45 high, at x = −13.5 | EST |

### Shell

| dimension | value | tag |
|---|---|---|
| side wall | 1.55 | EST |
| skirt wall (below z = 4.20, blending back over 0.80) | 1.15 | EST |
| roof under the dish | 1.70 | EST |
| diagonal ribs | 4 × 1.20 thick, starting at z = 5.00 | EST |

The skirt is deliberately thinner than the rest: it keeps the interior at least
as roomy as a stock OEM cap all the way around the switch housing (validated —
see §4).

### Cherry MX stem

| dimension | value | tag |
|---|---|---|
| cross, switch side | 4.10 × 1.17 | SRC |
| socket, as modelled | **4.22 × 1.39** | DER (SRC + tolerance) |
| FDM clearance added | +0.12 across, +0.22 through | EST |
| socket depth | 4.30 (MX stem is ~3.7 tall) | EST / SRC |
| chamfered lead-in at the mouth | 0.45 | EST |
| stem boss OD | 5.60 (stock ≈ 5.5) | EST |
| boss bottom face | z = 0.50 | EST |

### Costar stabiliser

| dimension | value | tag |
|---|---|---|
| mount spacing | 1.25u = **23.8125** (±11.90625) | SRC → DER |
| wire diameter assumed | 1.30 (quoted 1.2 + margin) | SRC / EST |
| bore | Ø1.65 (0.35 diametral clearance), through the block along X | EST |
| wire height above the rim | **4.20** | **FIT — unverified** |
| snap throat | 1.20 wide, straight for 0.60 below the bore, then flared +1.6 | EST |
| hook block | 6.00 (X) × 5.50 (Y), bottom face at z = 2.60 | EST |

---

## 3. Where each number came from

### Taken from a source

* **19.05 mm per unit; left Shift = 2.25u; left Shift stabiliser = 2u** —
  [Omnitype keycap sizes](https://intercom.help/omnitype/en/articles/5121683-keycap-sizes).
  That page gives no millimetres, only units.
* **2u stabiliser mounts are 1.25u apart** → 1.25 × 19.05 = **23.8125 mm**, i.e.
  ±11.90625 from the stem. Stated as "stabilizers are the same for 2u, 2.25u and
  2.75u keys with 1.25u between mounts" in the Cherry MX plate-measurement
  discussion on [Deskthority](https://deskthority.net/viewtopic.php?t=20144).
* **Cherry MX cross: 4.1 mm wide, 1.17 mm thick** — the Cherry MX drawing, as
  cited by the [MX keycap tolerance test](https://www.thingiverse.com/thing:4397634)
  and the [Cherry MX mount thread](https://deskthority.net/viewtopic.php?t=11183).
  The same sources list the common keycap-side variants 4.0 × 1.0 (Signature
  Plastics) and 4.1 × 1.35.
* **MX stem ~3.7 mm tall, 4.0 mm travel** — [Telcontar KBK, Cherry MX](https://telcontar.net/KBK/Cherry/MX).
* **This keyboard specifically** — the [Test-Gear review](https://www.test-gear.pl/testy-i-recenzje/klawiatury/ozone-strike-battle/):
  Cherry MX switches, **Costar-type stabilisers under the long keys**, ABS
  keycaps, "cylindrical shape with rounded edges", keycap **heights 9–11 mm**,
  **right Shift measured at 51 mm**, **spacebar at 118 mm**. Plus the
  [Ozone specification page](https://ozonegaming.com/en/pages/especificaciones-strike-battle):
  87 keys, ABS 94HB keycaps, backlight with brightness steps (so there *is* an
  LED in the switch's north window to clear).
* **Costar 2u wire quoted at 1.2 mm diameter** — from a stabiliser listing found
  via search. Single, weak source; treated as 1.30 with margin.
* **FDM tolerance guidance: cut-outs need ~0.1 mm added** — the MX tolerance
  test above (0.05 for SLA, >0.1 for FDM).

### Derived from those

* **41.90 body width.** The review's 51 mm right Shift (2.75u pitch = 52.3875)
  and 118 mm spacebar (6.25u pitch = 119.0625) both fit an inter-cap gap of
  ≈1.0 mm: 52.3875 − 1.0 = 51.39 → "51", and 119.0625 − 1.0 = 118.06 → "118".
  A gap of 0.85 (the usual 18.2 mm 1u body) would give 51.5 and 118.2, which
  rounds to 52 and 118 — a worse fit to the measurements. I used 0.96, giving
  41.90 for 2.25u. The review's figures are ruler measurements, so treat this as
  ±0.3 mm; it only affects the gap to Caps Lock and Z, not the fit.
* **18.10 body depth** — same reasoning on the 1u axis (gap 0.95).
* **±11.90625 stabiliser positions** — 1.25u/2.
* **4.22 × 1.39 socket** — the 4.10 × 1.17 cross plus FDM clearance.

### Estimated (closest standard value, not verified for this board)

Everything tagged `[EST]` in §2: the sculpt (heights, tilt, taper, radii, dish),
all wall and roof thicknesses, the rib and hook-block geometry, socket depth,
stem boss diameter, and the print tolerances. The only anchor for the sculpt is
the review's "9–11 mm" height range and "cylindrical" top, which the model
matches (9.60 at the dish centre, 11.60 at the back edge, cylindrical R28 dish).

OEM row heights are quoted inconsistently across vendor pages (10.3–13.3 mm
depending on who is measuring what), so I did not use them.

### Cannot be verified from online documentation

1. **`wire_z` = 4.20** — see §1. The one that matters.
2. Whether the original cap uses **separate Costar inserts** and, if so, their
   socket dimensions. No dimensioned source exists.
3. The **direction of the wire stub**. Worked around with a through-bore.
4. The exact **Cherry MX top-housing envelope above the plate** and the LED
   height. Because of this, the switch-clearance check is *relative* (see §4)
   rather than against an invented envelope.

---

## 4. Validation (all automated, see `VALIDATION.txt`)

Every check is a boolean probe against the rendered solid, not a visual check.

```
mesh        watertight, single closed solid, euler = 2, volume 2731.7 mm^3
size        41.903 x 18.100 x 11.39 ; fits the 2.25u x 1u pitch with
            0.48 mm per side to Caps Lock / Z and 0.47 mm front / back
stem        a nominal 4.10 x 1.17 MX cross enters with zero interference;
            a 4.40 x 1.47 probe does clash -> the socket is not oversized;
            socket centroid X = 0.000, Y = 0.000 -> centred
Costar      bores clear at x = +-11.90625 ; throat (1.20) open to the underside ;
            seated wire free to move +-0.15 mm inside the bore ;
            wire arm clears the whole cavity from |x| = 3.2 to 18.5 (misses the
            stem boss, the ribs and the walls) ; 0.02 mm^3 of intentional
            throat interference = a light snap
switch/LED  interior never tighter than a stock OEM cap (18.20 outer, 1.20 wall,
            same draft) anywhere from z = 0.2 to 5.0 -> worst margin -0.00 mm ;
            the north LED column (4 x 2.2 mm at y = 2.9..5.1, 7 mm tall) is clear
printing    sits flat on z = 0 ; first layer is the top-plate rim, not a point ;
            4.6 mm^2 of true overhang (the two bore roofs, 6 mm wide bridges) ;
            532 mm^2 of dish bridged over the bed, anchored all round ;
            1373 mm^2 of drafted wall at <= 12.6 deg from vertical
```

The switch-clearance check is deliberately **relative**: since the MX housing
envelope above the plate is not reliably documented, the model is required to be
no tighter anywhere than a stock OEM 1u cap's interior. It passes at every height
from 0.2 to 5.0 mm.

---

## 5. Printing

The STL is already oriented: **top plate flat on the bed, open side up**. Nothing
needs support — the dish is a 1.05 mm deep pocket sitting directly on the bed and
is bridged from its own rim, and the two wire bores are 6 mm bridges.

### PLA

| setting | value | why |
|---|---|---|
| **layer height** | **0.12 mm** (0.16 acceptable) | the cross socket is 1.39 mm through — thin layers keep it dimensionally honest |
| first layer | 0.20 mm | rim-only contact |
| **wall count** | **3** (0.4 nozzle, 0.42 width ≈ 1.26 mm) | matches the 1.15 mm skirt and the 1.55 mm wall without leaving gaps; 4 walls would over-stuff the skirt |
| **infill** | **100 %** | the part is nearly all perimeters; 100 % only fills the stem boss and hook blocks, where the strength is needed, and costs ≈2.7 cm³ total |
| top / bottom layers | 5 / 5 | |
| nozzle / bed | 205–215 °C / 60 °C | |
| cooling | 100 % from layer 3 | |
| supports | **none** | |
| brim | 5 mm, or a raft if your first layer is fussy | the bed contact is only the top-plate rim |
| seam | aligned, placed at a rear corner | keeps the visible top clean |
| horizontal expansion / XY compensation | 0 | the clearances are already in the model |

**PETG:** same, but 230–245 °C, 50 % cooling, and add 0.05 mm to
`cross_clr_w` / `cross_clr_t` — PETG swells more on the way out of the nozzle.

### Test fit first

Print the model once and try the stem on a spare switch before committing to the
stabiliser geometry.

* **too tight** → raise `cross_clr_w` / `cross_clr_t` by 0.05
* **too loose / wobbles** → lower them by 0.05
* **wire will not snap in** → raise `throat_w` toward `stab_wire_d`
* **wire rattles** → lower `bore_clr` to 0.25

### Fitting

1. Press the cap onto the switch far enough to locate the stem.
2. Line the two wire stubs up with the throats and push straight down — each
   stub snaps up into its bore.
3. Press home on the stem last.

To remove, pull evenly from both ends, not from one corner.

---

## 6. Deliberate departures from the original

* **Integrated Costar hooks instead of separate inserts** — you do not need the
  original white clips, and it removes an unverifiable set of socket dimensions.
* **Stem boss Ø5.60 instead of the stock ≈5.5** — a little more meat around the
  cross for FDM, while still clearing the in-switch LED at the north face.
* **Thinner skirt (1.15) than the upper wall (1.55)** — keeps the interior at
  least as roomy as a stock cap around the switch housing while leaving a wall
  thick enough to print at 3 perimeters higher up.
* **Embossed arrow instead of the original's laser-cut legend** — a single-colour
  FDM print cannot reproduce a dye-sub two-layer legend. Set
  `legend_arrow = false` for a blank cap.
* Functional compatibility was prioritised over cosmetic similarity throughout,
  as requested.
