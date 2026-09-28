#!/usr/bin/env python3
"""
Print the repo's keycap sources as a JSON array, for a CI build matrix.

A key is any <keyboard>/<key>.scad, excluding the shared library and any
*.inc.scad, which are includes rather than keys.

Usage:  python3 tools/list_keys.py
"""

import glob
import json
import os
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def keys():
    out = []
    for p in sorted(glob.glob(os.path.join(HERE, "*", "*.scad"))):
        rel = os.path.relpath(p, HERE)
        if rel.startswith("lib" + os.sep) or rel.endswith(".inc.scad"):
            continue
        out.append(rel)
    return out


if __name__ == "__main__":
    found = keys()
    if not found:
        print("no keycap sources found", file=sys.stderr)
        sys.exit(1)
    print(json.dumps(found))
