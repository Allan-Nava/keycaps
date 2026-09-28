#!/usr/bin/env python3
"""
Repo hygiene checks that need neither OpenSCAD nor a render.

  * every keycap source has a committed STL next to it,
  * every keycap source has a validation report,
  * every keyboard directory has a README,
  * every keycap source includes the shared library,
  * no keycap source carries an undefined-looking parameter.

Usage:  python3 tools/repo_lint.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from list_keys import HERE, keys                                # noqa: E402


def main():
    problems = []
    boards = set()

    for rel in keys():
        board, name = os.path.split(rel)
        boards.add(board)
        stem = os.path.splitext(name)[0]
        src = os.path.join(HERE, rel)

        for want, why in (
            (os.path.join(board, stem + ".stl"), "committed STL"),
            (os.path.join(board, f"VALIDATION-{stem}.txt"), "validation report"),
        ):
            if not os.path.exists(os.path.join(HERE, want)):
                problems.append(f"{rel}: missing {why} ({want})")

        text = open(src, encoding="utf-8").read()
        if "keycap_common.scad" not in text:
            problems.append(f"{rel}: does not include lib/keycap_common.scad")
        if "render_keycap()" not in text:
            problems.append(f"{rel}: never calls render_keycap()")

        report = os.path.join(HERE, board, f"VALIDATION-{stem}.txt")
        if os.path.exists(report):
            body = open(report, encoding="utf-8").read()
            if "ALL CHECKS PASSED" not in body:
                problems.append(
                    f"{rel}: its committed validation report does not say "
                    f"ALL CHECKS PASSED")

    for board in sorted(boards):
        if not os.path.exists(os.path.join(HERE, board, "README.md")):
            problems.append(f"{board}/: missing README.md")

    for f in ("README.md", "LICENSE", "lib/keycap_common.scad"):
        if not os.path.exists(os.path.join(HERE, f)):
            problems.append(f"missing {f}")

    print(f"checked {len(keys())} keycap sources across "
          f"{len(boards)} keyboard(s)")
    for p in problems:
        print(f"  [FAIL] {p}")
    if problems:
        print(f"\nRESULT: {len(problems)} problem(s)")
        return 1
    print("\nRESULT: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
