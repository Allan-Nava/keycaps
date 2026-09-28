#!/usr/bin/env python3
"""
Prove that the validation suite can actually fail.

A check that never fails is decoration. This breaks a known-good model on
purpose, one defect at a time, and asserts that the specific check meant to
catch that defect reports FAIL - not merely that "something" went wrong.

Every case runs with --check, so nothing in the repo is overwritten.

Known gap, stated rather than papered over: there is no check on the DEPTH of
the cross socket, so a socket too shallow for the switch stem would pass. The
suite verifies that the cross fits in section and that the cap grips it, not
that it seats to the bottom.

Usage:  python3 tools/selftest.py
"""

import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
VALIDATE = os.path.join(HERE, "build_and_validate.py")

ISO = "ozone-strike-battle/left-shift-iso.scad"
ANSI = "ozone-strike-battle/left-shift-ansi.scad"

# (label, keycap, overrides, the check that MUST report FAIL)
CASES = [
    ("socket bored out so the stem cannot grip",
     ISO, {"cross_clr_w": "1.2", "cross_clr_t": "1.2"},
     "socket is not oversized"),

    ("cap made wider than its own key pitch",
     ISO, {"key_gap": "-2.0"},
     "fits inside the key pitch envelope"),

    ("walls thickened until the switch would not fit inside",
     ISO, {"wall": "3.0", "wall_skirt": "3.0"},
     "interior never tighter than a stock cap"),

    ("Costar bore shrunk below the wire diameter",
     ANSI, {"bore_clr": "-0.5"},
     "wire bore clear at"),

    ("socket undersized, so a real MX stem would not go in",
     ISO, {"cross_clr_w": "-0.6", "cross_clr_t": "-0.6"},
     "nominal MX cross"),
]


def run(keycap, overrides):
    cmd = [sys.executable, VALIDATE, "--check"]
    for k, v in overrides.items():
        cmd += ["-D", f"{k}={v}"]
    cmd.append(keycap)
    p = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    return p.returncode, p.stdout + p.stderr


def failed_checks(output):
    return [ln.strip() for ln in output.splitlines()
            if ln.lstrip().startswith("[FAIL]")]


def main():
    ok = True

    print("== control: an untouched model must pass ==")
    for keycap in (ISO, ANSI):
        code, out = run(keycap, {})
        good = code == 0 and "ALL CHECKS PASSED" in out
        print(f"  [{'PASS' if good else 'FAIL'}] {keycap}")
        if not good:
            ok = False
            print("\n".join(f"        {ln}" for ln in failed_checks(out)))

    print("== each defect must be caught by its own check ==")
    for label, keycap, overrides, want in CASES:
        code, out = run(keycap, overrides)
        fails = failed_checks(out)
        caught = any(want in ln for ln in fails)
        good = code != 0 and caught
        print(f"  [{'PASS' if good else 'FAIL'}] {label}")
        print(f"         expected a FAIL matching {want!r}")
        if good:
            hit = next(ln for ln in fails if want in ln)
            print(f"         got: {hit[:110]}")
        else:
            ok = False
            if code == 0:
                print("         but the validator passed the broken model")
            else:
                print("         the run failed, but not on that check. "
                      f"Failures seen: {len(fails)}")
                for ln in fails[:6]:
                    print(f"           {ln[:110]}")

    print()
    print("RESULT:", "SELF-TEST PASSED" if ok else "SELF-TEST FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
