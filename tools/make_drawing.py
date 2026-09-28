#!/usr/bin/env python3
"""
Dimensioned technical drawing for a keycap.

Every outline is a real cross-section of the rendered solid, so the drawing
cannot drift away from the model. Dimension values are read back out of the
render (see tools/scadparams.py), never typed in.

Usage:  python3 tools/make_drawing.py <keyboard>/<key>.scad
        -> <keyboard>/<key>-drawing.svg / .pdf / .png
"""

import os
import sys

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt                                 # noqa: E402
from matplotlib.lines import Line2D                             # noqa: E402
import trimesh                                                  # noqa: E402

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from scadparams import render                                   # noqa: E402

DIMC = "#b00020"
NOTEC = "#204080"
LW = 1.1


def section(mesh, origin, normal):
    """Return the section as a list of 3-D polylines."""
    s = mesh.section(plane_origin=origin, plane_normal=normal)
    if s is None:
        return []
    planar, to_3D = s.to_planar()      # to_3D maps the 2-D path back to space
    out = []
    for ent in planar.entities:
        pts = planar.vertices[ent.points]
        out.append(trimesh.transform_points(
            np.column_stack([pts, np.zeros(len(pts))]), to_3D))
    return out


def style(ax, title, sub=""):
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title(f"{title}\n{sub}" if sub else title, fontsize=10.5,
                 fontweight="bold", loc="left", pad=6)


def hdim(ax, x0, x1, y, text, tick=0.7):
    ax.annotate("", (x0, y), (x1, y),
                arrowprops=dict(arrowstyle="<->", color=DIMC, lw=0.8))
    for x in (x0, x1):
        ax.add_line(Line2D([x, x], [y - tick, y + tick], color=DIMC, lw=0.6))
    ax.text((x0 + x1) / 2, y + 0.35, text, ha="center", va="bottom",
            fontsize=7.5, color=DIMC)


def vdim(ax, y0, y1, x, text, tick=0.7):
    ax.annotate("", (x, y0), (x, y1),
                arrowprops=dict(arrowstyle="<->", color=DIMC, lw=0.8))
    for y in (y0, y1):
        ax.add_line(Line2D([x - tick, x + tick], [y, y], color=DIMC, lw=0.6))
    ax.text(x + 0.4, (y0 + y1) / 2, text, ha="left", va="center",
            fontsize=7.5, color=DIMC, rotation=90)


def note(ax, x, y, tx, ty, text, fs=7.0):
    ax.annotate(text, xy=(x, y), xytext=(tx, ty), fontsize=fs, color=NOTEC,
                arrowprops=dict(arrowstyle="-", color=NOTEC, lw=0.6))


def main(scad):
    scad = os.path.abspath(scad)
    base = os.path.splitext(scad)[0]
    mesh, P = render(scad, base + "._design.off", False)
    costar = P.get("stab_style") == "costar"
    hx = P["body_x"] / 2
    hy = P["body_y"] / 2
    pitch_x = P["units"] * P["U"]

    fig = plt.figure(figsize=(16.5, 11.7))
    fig.patch.set_facecolor("white")

    # ==================================================== A - plan (top) ====
    ax = fig.add_subplot(2, 2, 1)
    style(ax, "A   PLAN  (top)", "outline at the skirt and at the top plate")
    for pl in section(mesh, [0, 0, 0.05], [0, 0, 1]):
        ax.plot(pl[:, 0], pl[:, 1], color="k", lw=LW)
    for pl in section(mesh, [0, 0, P["h_center"] - P["bevel"] - 0.15], [0, 0, 1]):
        ax.plot(pl[:, 0], pl[:, 1], color="#888", lw=0.8, ls="--")
    ax.add_patch(plt.Rectangle((-pitch_x / 2, -P["U"] / 2), pitch_x, P["U"],
                               fill=False, ec="#2a7", lw=0.7, ls=":"))
    ax.plot([0], [0], marker="+", color=DIMC, ms=9, mew=1.2)
    hdim(ax, -hx, hx, -hy - 2.2, f'{P["body_x"]:.2f}  body')
    hdim(ax, -pitch_x / 2, pitch_x / 2, -hy - 4.6,
         f'{pitch_x:.4f}   {P["units"]:g}u pitch (19.05 x {P["units"]:g})')
    vdim(ax, -hy, hy, hx + 5.0, f'{P["body_y"]:.2f}')
    hdim(ax, -(hx - P["taper"]), hx - P["taper"], hy + 0.6,
         f'{P["body_x"] - 2 * P["taper"]:.2f}  top plate')
    note(ax, -hx + 1.5, hy - 1.0, -hx - 8, hy + 4.5, f'R{P["r_bot"]:.1f} skirt corner')
    note(ax, -hx + 3.3, hy - 2.6, -hx - 8, hy + 2.0, f'R{P["r_top"]:.1f} top corner')
    ax.set_xlim(-hx - 11, hx + 11)
    ax.set_ylim(-hy - 6.5, hy + 7)

    # ============================================ B - section on Y = 0 ======
    ax = fig.add_subplot(2, 2, 2)
    style(ax, "B   SECTION  Y = 0   (front, through the stem"
              + (" and both hooks)" if costar else ")"),
          "the Costar wire runs left-right through the two bores" if costar
          else "")
    for pl in section(mesh, [0, 0, 0], [0, 1, 0]):
        ax.plot(pl[:, 0], pl[:, 2], color="k", lw=LW)
    ax.axhline(0, color="#bbb", lw=0.5)
    if costar:
        for s in (-1, 1):
            ax.plot([s * P["stab_x"]], [P["wire_z"]], marker="o", ms=4,
                    mfc="none", color=DIMC)
        hdim(ax, -P["stab_x"], P["stab_x"], -3.4,
             f'{2 * P["stab_x"]:.4f}   Costar stabiliser centres '
             f'({2 * P["stab_x"] / P["U"]:.2f}u)')
        vdim(ax, 0, P["wire_z"], hx + 3.5, f'{P["wire_z"]:.2f} wire')
        note(ax, P["stab_x"], P["wire_z"], hx * 0.34, P["h_center"] + 4.8,
             f'bore d{P["stab_wire_d"] + P["bore_clr"]:.2f} for a '
             f'd{P["stab_wire_d"]:.2f} wire\nthroat {P["throat_w"]:.2f} (snap)')
    hdim(ax, -hx, hx, -5.8, f'{P["body_x"]:.2f}')
    vdim(ax, 0, P["h_center"], hx + 7.5, f'{P["h_center"]:.2f} @ centre')
    note(ax, 0, P["stem_z0"] + P["cross_depth"] / 2, -hx * 0.80,
         P["h_center"] + 4.8,
         f'MX cross socket {P["cross_w"] + P["cross_clr_w"]:.2f} x '
         f'{P["cross_t"] + P["cross_clr_t"]:.2f}, {P["cross_depth"]:.1f} deep')
    ax.set_xlim(-hx - 5, hx + 9)
    ax.set_ylim(-7, P["h_center"] + 6.5)

    # ============================================ C - section on X = 0 ======
    ax = fig.add_subplot(2, 2, 3)
    style(ax, "C   SECTION  X = 0   (side, front of the keyboard to the left)",
          "OEM-style sculpt: top plate tilted back, cylindrical dish")
    for pl in section(mesh, [0, 0, 0], [1, 0, 0]):
        ax.plot(pl[:, 1], pl[:, 2], color="k", lw=LW)
    ax.axhline(0, color="#bbb", lw=0.5)
    hdim(ax, -hy, hy, -3.2, f'{P["body_y"]:.2f}')
    vdim(ax, 0, P["h_center"] - P["dish_depth"], hy + 3.0,
         f'{P["h_center"] - P["dish_depth"]:.2f} at the dish')
    vdim(ax, 0, mesh.bounds[1][2], hy + 7.0,
         f'{mesh.bounds[1][2]:.2f} overall height')
    note(ax, 0, P["h_center"] - P["dish_depth"], -hy - 5, P["h_center"] + 4.8,
         f'dish R{P["dish_r"]:.0f}, {P["dish_depth"]:.2f} deep,\n'
         f'axis along X;  roof {P["roof"]:.2f}')
    note(ax, -hy + 1.0, 8.5, -hy - 7, P["h_center"] + 1.0, f'wall {P["wall"]:.2f}')
    note(ax, -hy + 0.5, 1.5, -hy - 7, 4.0,
         f'skirt wall {P["wall_skirt"]:.2f}\nup to z={P["skirt_z"]:.1f}')
    note(ax, 3.0, P["h_center"] - 0.3, 4.0, P["h_center"] + 3.8,
         f'{P["row_tilt"]:.0f} deg row tilt')
    ax.set_xlim(-hy - 9, hy + 11)
    ax.set_ylim(-5, P["h_center"] + 6.5)

    # ======================================== D - underside at z = 3.0 ======
    ax = fig.add_subplot(2, 2, 4)
    style(ax, "D   UNDERSIDE  (section at z = 3.00, looking up)",
          "stem boss, four diagonal ribs"
          + (", two Costar hook blocks" if costar else ""))
    for pl in section(mesh, [0, 0, 3.0], [0, 0, 1]):
        ax.plot(pl[:, 0], pl[:, 1], color="k", lw=LW)
    for pl in section(mesh, [0, 0, 6.0], [0, 0, 1]):
        ax.plot(pl[:, 0], pl[:, 1], color="#888", lw=0.8, ls="--")
    ax.plot([0], [0], marker="+", color=DIMC, ms=9, mew=1.2)
    note(ax, 0, 2.6, 2.0, hy + 3.0, f'stem boss d{P["stem_od"]:.2f}')
    note(ax, 4.2, 4.2, -hx * 0.55, hy + 3.0,
         f'ribs {P["rib_t"]:.1f} thick,\nstart z={P["rib_z0"]:.1f}')
    if costar:
        for s in (-1, 1):
            ax.plot([s * P["stab_x"]], [0], marker="+", color=DIMC, ms=8, mew=1.0)
        hdim(ax, 0, P["stab_x"], -hy - 2.0, f'{P["stab_x"]:.4f}')
        hdim(ax, -P["stab_x"], P["stab_x"], -hy - 4.4, f'{2 * P["stab_x"]:.4f}')
        note(ax, P["stab_x"], 2.4, hx * 0.72, hy + 2.0,
             f'hook {P["hook_len"]:.1f} x {P["hook_w"]:.1f},\n'
             f'bottom z={P["hook_z0"]:.2f}')
    ax.set_xlim(-hx - 6, hx + 8)
    ax.set_ylim(-hy - 6.5, hy + 5)

    fig.suptitle(
        f'{os.path.basename(os.path.dirname(scad))} / '
        f'{os.path.basename(base)}  -  {P["units"]:g}u, MX cross stem'
        + (", Costar stabiliser" if costar else "")
        + "   |   all dimensions in mm   |   dashed = hidden outline   |   "
          "dotted green = key pitch envelope", fontsize=10, y=0.985)
    fig.tight_layout(rect=[0, 0.01, 1, 0.965])
    for ext in ("svg", "pdf", "png"):
        fig.savefig(f"{base}-drawing.{ext}", dpi=170)
    print(f"wrote {os.path.relpath(base)}-drawing.svg / .pdf / .png")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
