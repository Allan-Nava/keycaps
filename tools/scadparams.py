"""Render a keycap .scad and read its parameters straight out of the render.

`lib/keycap_common.scad` echoes every parameter as `ECHO: "##PARAM", "name", v`,
so the Python tools never mirror a dimension by hand and can never drift from
the model.
"""

import os
import re
import shutil
import subprocess

OPENSCAD = (shutil.which("openscad")
            or "/Applications/OpenSCAD.app/Contents/MacOS/OpenSCAD")
_ECHO = re.compile(r'ECHO: "##PARAM", "(\w+)", (.+)$')


def render(scad, out, print_orientation=False, extra=None):
    """Render `scad` to `out` (.off keeps full precision; .stl is float32).

    Returns (trimesh.Trimesh, params_dict).
    """
    import trimesh

    cmd = [OPENSCAD, "--backend=manifold", "-o", out,
           "-D", f"print_orientation={'true' if print_orientation else 'false'}"]
    for k, v in (extra or {}).items():
        cmd += ["-D", f"{k}={v}"]
    cmd.append(scad)
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0 or not os.path.exists(out):
        raise RuntimeError(f"openscad failed:\n{proc.stderr}")

    params = {}
    for line in proc.stderr.splitlines():
        m = _ECHO.match(line.strip())
        if m:
            raw = m.group(2).strip()
            if raw.startswith('"'):
                params[m.group(1)] = raw.strip('"')
            else:
                try:
                    params[m.group(1)] = float(raw)
                except ValueError:
                    params[m.group(1)] = raw
    if not params:
        raise RuntimeError(
            "no ##PARAM echoes: does the .scad include lib/keycap_common.scad?")
    return trimesh.load(out, process=True), params
