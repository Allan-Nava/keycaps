#!/usr/bin/env python3
"""
Build + validate a keycap.

  1. renders the .scad twice (design orientation for checking, print
     orientation for the slicer) with OpenSCAD's manifold backend,
  2. drops the print-orientation mesh onto z = 0 and centres it in XY,
     writing <name>.stl next to the source,
  3. runs the geometric validation suite with boolean probes.

Every dimension used by the checks is read back out of the render, so this
file never has to mirror the .scad by hand.

Usage:  python3 tools/build_and_validate.py <keyboard>/<key>.scad
        python3 tools/build_and_validate.py --check <keyboard>/<key>.scad

--check does not overwrite the committed STL. It renders, runs the same
checks, and then verifies that the STL already in the repo still matches what
the .scad produces - which is what catches "edited the model, forgot to
regenerate". The comparison is on the bounding box and the volume rather than
on bytes, because OpenSCAD tessellation and font substitution differ between
machines and versions; see the tolerances below.
"""

import argparse
import os
import sys

import numpy as np
import trimesh

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from scadparams import render                                   # noqa: E402

# --- reference cap for the relative interior-clearance check ---------------
# A stock 1u cap: 18.20 body, 1.20 wall, and THE SAME sculpt as the cap under
# test. Using the cap's own shoulder height is what makes the check fair for a
# short Cherry-profile cap, which is legitimately narrower at a given z than a
# tall OEM one and still clears the same switch.
REF_BODY = 18.20
REF_WALL = 1.20

# --- tolerances for --check -------------------------------------------------
# The bounding box is set by the sculpt parameters alone, so it can be tight.
# The volume cannot: a text legend is rendered with whatever font fontconfig
# substitutes, and that differs between a Mac and a CI runner.
CHECK_BBOX_TOL = 0.02      # mm
CHECK_VOLUME_TOL = 0.02    # fraction


def box(sx, sy, sz, cx=0.0, cy=0.0, z0=0.0):
    b = trimesh.creation.box(extents=(sx, sy, sz))
    b.apply_translation((cx, cy, z0 + sz / 2))
    return b


def cross_probe(P, clearance=0.0):
    """Solid shaped like the real MX stem cross."""
    d, z0 = P["cross_depth"], P["stem_z0"]
    a = box(P["cross_w"] + clearance, P["cross_t"] + clearance, d, z0=z0)
    b = box(P["cross_t"] + clearance, P["cross_w"] + clearance, d, z0=z0)
    return trimesh.boolean.union([a, b])


def x_cylinder(diameter, length, cx, cy, cz):
    c = trimesh.creation.cylinder(radius=diameter / 2, height=length)
    c.apply_transform(trimesh.transformations.rotation_matrix(np.pi / 2, [0, 1, 0]))
    c.apply_translation((cx, cy, cz))
    return c


def clash(mesh, probe):
    """Volume of solid material inside the probe (mm^3)."""
    try:
        inter = trimesh.boolean.intersection([mesh, probe])
    except Exception:
        return float("nan")
    return 0.0 if inter is None or inter.is_empty else float(inter.volume)


def clear_width(mesh, z, x=0.0):
    """Interior free width along Y at height z, measured on the centre line."""
    ys = np.arange(-9.5, 9.5001, 0.01)
    pts = np.column_stack([np.full_like(ys, x), ys, np.full_like(ys, z)])
    free = ys[~mesh.contains(pts)]
    free = free[(free > -9.0) & (free < 9.0)]
    return float(free.max() - free.min()) if free.size else 0.0


class Report:
    def __init__(self):
        self.ok = True

    def __call__(self, name, ok, detail):
        print(f"  [{'PASS' if ok else 'FAIL'}] {name:<52} {detail}")
        self.ok &= bool(ok)
        return ok

    def info(self, name, detail):
        print(f"  [info] {name:<52} {detail}")


def main(scad, check=False, defines=None):
    scad = os.path.abspath(scad)
    base = os.path.splitext(scad)[0]
    name = os.path.basename(base)
    print(f"== rendering {os.path.relpath(scad)} ==")
    m, P = render(scad, base + "._design.off", False, extra=defines)
    printed, _ = render(scad, base + "._print.off", True, extra=defines)

    printed.apply_translation((0, 0, -printed.bounds[0][2]))
    c = printed.bounds.mean(axis=0)
    printed.apply_translation((-c[0], -c[1], 0))
    out = base + ".stl"
    if check:
        print(f"   --check: not writing {os.path.relpath(out)}")
    else:
        printed.export(out)
        print(f"   wrote {os.path.relpath(out)}")

    lo, hi = m.bounds
    r = Report()

    print("== mesh integrity ==")
    r("watertight, single closed solid", m.is_watertight and m.body_count == 1,
      f"watertight={m.is_watertight} bodies={m.body_count} "
      f"euler={m.euler_number}")
    r("consistent winding / positive volume",
      m.is_winding_consistent and m.volume > 0,
      f"volume={m.volume:.1f} mm^3 (~{m.volume * 1.24 / 1000:.2f} g PLA solid)")

    print("== outside dimensions ==")
    pitch_x, pitch_y = P["units"] * P["U"], P["U"]
    r(f'{P["units"]:g}u body width (X)', abs((hi[0] - lo[0]) - P["body_x"]) < 0.02,
      f'{hi[0] - lo[0]:.3f} mm  ({P["units"]:g}u pitch = {pitch_x:.4f})')
    r("body depth (Y)", abs((hi[1] - lo[1]) - P["body_y"]) < 0.02,
      f'{hi[1] - lo[1]:.3f} mm  (1u pitch = {pitch_y:.2f})')
    r("fits inside the key pitch envelope",
      (hi[0] - lo[0]) < pitch_x and (hi[1] - lo[1]) < pitch_y,
      f"gap to the neighbours = {(pitch_x - (hi[0] - lo[0])) / 2:.2f} mm per "
      f"side, {(pitch_y - (hi[1] - lo[1])) / 2:.2f} mm front/back")
    r("total height", 7.0 < (hi[2] - lo[2]) < 15.0, f"{hi[2] - lo[2]:.2f} mm")

    print("== MX cross stem ==")
    r(f'nominal MX cross ({P["cross_w"]:.2f} x {P["cross_t"]:.2f}) enters',
      clash(m, cross_probe(P, 0.0)) < 1e-6,
      f"interference = {clash(m, cross_probe(P, 0.0)):.4f} mm^3")
    tight = clash(m, cross_probe(P, 0.30))
    r("socket is not oversized (+0.30 probe does clash)", tight > 0.05,
      f"interference = {tight:.3f} mm^3 -> grip present")
    void = trimesh.boolean.difference([cross_probe(P, 0.30), m])
    ctr = void.centroid
    r("stem is centred on the key", abs(ctr[0]) < 0.02 and abs(ctr[1]) < 0.02,
      f"socket centroid X={ctr[0]:+.3f} Y={ctr[1]:+.3f}")

    if P.get("stab_style") == "costar":
        print("== Costar stabiliser ==")
        sx_pair = (+P["stab_x"], -P["stab_x"])
        span = P["hook_len"] + 4
        for sx in sx_pair:
            v = clash(m, x_cylinder(P["stab_wire_d"], span, sx, 0.0, P["wire_z"]))
            r(f'wire bore clear at x={sx:+.3f} '
              f'({2 * P["stab_x"] / P["U"]:.2f}u apart)', v < 1e-6,
              f"interference = {v:.4f} mm^3")
        tw = max(clash(m, box(span, P["throat_w"],
                              P["wire_z"] - P["hook_z0"] + 2.0, sx, 0,
                              P["hook_z0"] - 2.0)) for sx in sx_pair)
        r(f'throat ({P["throat_w"]:.2f} mm) open to the underside', tw < 1e-6,
          f"interference = {tw:.4f} mm^3")
        worst = 0.0
        for dy, dz in ((0.15, 0), (-0.15, 0), (0, 0.15), (0, -0.15), (0, 0)):
            for sx in sx_pair:
                worst = max(worst, clash(m, x_cylinder(
                    P["stab_wire_d"], span, sx, dy, P["wire_z"] + dz)))
        r("seated wire is free to move inside the bore (+-0.15 mm)",
          worst < 1e-6, f"worst interference = {worst:.4f} mm^3")
        arm = 0.0
        x0, x1 = P["stem_od"] / 2 + 0.4, P["body_x"] / 2 - 2.5
        for sign in (+1, -1):
            c = trimesh.creation.cylinder(radius=P["stab_wire_d"] / 2,
                                          height=x1 - x0)
            c.apply_transform(
                trimesh.transformations.rotation_matrix(np.pi / 2, [0, 1, 0]))
            c.apply_translation((sign * (x0 + (x1 - x0) / 2), 0.0, P["wire_z"]))
            arm = max(arm, clash(m, c))
        r(f"wire arm clears the cavity from x=+-{x0:.1f} to +-{x1:.1f}",
          arm < 1e-6, f"worst interference = {arm:.4f} mm^3 "
                      f"(stem boss, ribs and walls all missed)")
        ret = clash(m, x_cylinder(P["stab_wire_d"], span, P["stab_x"], 0.0,
                                  P["wire_z"] - 0.40))
        r("throat retains the wire (interference is intentional)", ret > 0.005,
          f"{ret:.2f} mm^3 of PLA must flex to snap the wire in")
    elif P.get("stab_style") != "none":
        r(f'stabiliser style "{P.get("stab_style")}" is implemented', False,
          "unknown style - nothing was validated")

    print("== switch / LED clearance ==")
    # The exact switch top-housing envelope above the plate is not documented,
    # so the check is relative: this cap's interior must never be tighter than
    # a stock OEM 1u cap's interior at the same height.
    shoulder = P["h_center"] - P["bevel"]
    z_max = min(5.0, P["h_center"] - P["roof"] - 0.3)
    worst_d, worst_z = 1e9, None
    for z in np.arange(0.2, z_max + 1e-9, 0.2):
        ref = REF_BODY - 2 * REF_WALL - 2 * (P["taper"] * z / shoulder)
        d = clear_width(m, z) - ref
        if d < worst_d:
            worst_d, worst_z = d, z
    r("interior never tighter than a stock cap of the same sculpt",
      worst_d > -0.05,
      f"worst margin {worst_d:+.2f} mm at z = {worst_z:.1f} mm "
      f"(checked to z = {z_max:.1f})")
    led_h = P.get("led_clear_h", 7.0)
    if led_h > 0:
        led = box(4.0, 2.2, led_h, 0.0, 4.0, 0.0)
        r(f"north in-switch LED column (4 x 2.2, {led_h:.1f} mm tall) is clear",
          clash(m, led) < 1e-6, f"interference = {clash(m, led):.4f} mm^3")
    else:
        r.info("north LED column",
               "not checked: led_clear_h = 0, the board lights each key with an "
               "SMD LED under the switch, nothing enters the cap")

    print("== printability ==")
    r("print orientation sits flat on z = 0", abs(printed.bounds[0][2]) < 1e-6,
      f"min z = {printed.bounds[0][2]:.6f}")
    zs = printed.vertices[:, 2]
    r("first layer is the top-plate rim, not a point", (zs < 0.25).sum() > 20,
      f"{(zs < 0.25).sum()} vertices within 0.25 mm of the bed")
    n, a = printed.face_normals, printed.area_faces
    ztop = printed.vertices[printed.faces][:, :, 2].max(axis=1)
    # |nz| = sin(angle from vertical): -0.707 is the classic 45 deg limit
    down = n[:, 2] < -0.707
    dish_lip = P["dish_depth"] + 0.45
    dish, real = down & (ztop <= dish_lip), down & (ztop > dish_lip)
    r("no overhang past 45 deg above the bed", a[real].sum() < 12.0,
      f"{a[real].sum():.1f} mm^2 above the dish + {a[dish].sum():.1f} mm^2 of "
      f"dish bridged over the bed")
    r.info("drafted walls",
           f'{a[(n[:, 2] < -0.001) & (n[:, 2] >= -0.707)].sum():.1f} mm^2 at '
           f'<={np.degrees(np.arctan(P["taper"] / (P["h_center"] - P["bevel"]))):.1f} '
           f"deg from vertical")

    if check:
        print("== committed STL is current ==")
        if not os.path.exists(out):
            r(f"{name}.stl exists", False, "missing - run without --check")
        else:
            have = trimesh.load(out, process=True)
            dbox = float(np.abs(have.bounds - printed.bounds).max())
            dvol = abs(have.volume - printed.volume) / printed.volume
            r("committed STL matches the .scad (bounding box)",
              dbox <= CHECK_BBOX_TOL,
              f"largest corner difference {dbox:.4f} mm "
              f"(tolerance {CHECK_BBOX_TOL})")
            r("committed STL matches the .scad (volume)",
              dvol <= CHECK_VOLUME_TOL,
              f"{have.volume:.1f} vs {printed.volume:.1f} mm^3, "
              f"{dvol * 100:.2f}% apart (tolerance "
              f"{CHECK_VOLUME_TOL * 100:.0f}%)")

    print()
    print("RESULT:", "ALL CHECKS PASSED" if r.ok else "SOME CHECKS FAILED")
    return 0 if r.ok else 1


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__.strip().splitlines()[0])
    ap.add_argument("scad", help="path to a <keyboard>/<key>.scad")
    ap.add_argument("--check", action="store_true",
                    help="do not write the STL; verify the committed one "
                         "still matches the model")
    ap.add_argument("-D", "--define", action="append", default=[],
                    metavar="NAME=VALUE",
                    help="override a .scad parameter, as openscad -D. Used by "
                         "tools/selftest.py to break a model on purpose and "
                         "prove the checks catch it.")
    a = ap.parse_args()
    defs = {}
    for d in a.define:
        if "=" not in d:
            ap.error(f"-D expects NAME=VALUE, got {d!r}")
        k, v = d.split("=", 1)
        defs[k.strip()] = v.strip()
    if defs:
        print(f"== overrides: {defs} ==")
    sys.exit(main(a.scad, check=a.check, defines=defs or None))
