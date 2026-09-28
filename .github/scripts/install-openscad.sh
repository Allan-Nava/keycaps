#!/usr/bin/env bash
# Install OpenSCAD with the manifold backend on a Linux CI runner.
#
# Why not apt: Ubuntu ships OpenSCAD 2021.01, which predates --backend=manifold
# and would fail on every render in this repo.
#
# Why a pin with a fallback: files.openscad.org keeps only a rolling window of
# dated snapshots (about nine months). A hard pin is reproducible until the day
# it 404s; floating on "newest" is never reproducible. So: try the pin, and if
# it has rotated out, take the newest one on the server and say so loudly.
#
# Env:
#   OPENSCAD_SNAPSHOT  date of the snapshot to prefer, e.g. 2026.09.27
#   OPENSCAD_PREFIX    where to install (default /opt/openscad)
set -euo pipefail

BASE="https://files.openscad.org/snapshots"
PREFIX="${OPENSCAD_PREFIX:-/opt/openscad}"
WANT="${OPENSCAD_SNAPSHOT:-}"

resolve_newest() {
    curl -fsSL --max-time 60 "$BASE/" \
        | grep -oE 'OpenSCAD-[0-9]{4}\.[0-9]{2}\.[0-9]{2}-x86_64\.AppImage' \
        | sort -u | tail -1
}

file=""
if [ -n "$WANT" ]; then
    candidate="OpenSCAD-${WANT}-x86_64.AppImage"
    if curl -fsIL --max-time 30 -o /dev/null "$BASE/$candidate"; then
        file="$candidate"
    else
        echo "::warning::pinned OpenSCAD snapshot $WANT is gone from $BASE;" \
             "falling back to the newest available. Update OPENSCAD_SNAPSHOT" \
             "in the workflow to make CI reproducible again."
    fi
fi
[ -n "$file" ] || file="$(resolve_newest)"
[ -n "$file" ] || { echo "could not resolve any OpenSCAD snapshot" >&2; exit 1; }

echo "OpenSCAD snapshot: $file"

work="$(mktemp -d)"
trap 'rm -rf "$work"' EXIT
cd "$work"

curl -fsSL --retry 3 --retry-connrefused -o openscad.AppImage "$BASE/$file"

# The server publishes a checksum next to every snapshot. Verify it: this
# script runs a downloaded binary, so an unchecked download is a supply chain
# hole, not a convenience.
if curl -fsSL --max-time 30 -o openscad.sha256 "$BASE/${file}.sha256"; then
    expected="$(awk '{print $1}' openscad.sha256)"
    actual="$(sha256sum openscad.AppImage | awk '{print $1}')"
    if [ "$expected" != "$actual" ]; then
        echo "checksum mismatch for $file" >&2
        echo "  expected $expected" >&2
        echo "  actual   $actual" >&2
        exit 1
    fi
    echo "sha256 verified"
else
    echo "no published sha256 for $file" >&2
    exit 1
fi

# GitHub runners have no FUSE, so extract rather than mount.
chmod +x openscad.AppImage
./openscad.AppImage --appimage-extract >/dev/null

sudo rm -rf "$PREFIX"
sudo mkdir -p "$(dirname "$PREFIX")"
sudo mv squashfs-root "$PREFIX"
sudo ln -sf "$PREFIX/AppRun" /usr/local/bin/openscad

# If a system library is missing, report EVERY missing one at once. Finding
# them one CI run at a time is a waste of everyone's afternoon.
if ! openscad --version >/dev/null 2>&1; then
    echo "::error::openscad will not start. Missing shared libraries:"
    for bin in "$PREFIX/usr/bin/openscad" "$PREFIX/AppRun"; do
        [ -f "$bin" ] || continue
        LD_LIBRARY_PATH="$PREFIX/usr/lib:${LD_LIBRARY_PATH:-}" \
            ldd "$bin" 2>/dev/null | grep "not found" | sort -u || true
    done
    for lib in "$PREFIX"/usr/lib/*.so*; do
        LD_LIBRARY_PATH="$PREFIX/usr/lib:${LD_LIBRARY_PATH:-}" \
            ldd "$lib" 2>/dev/null | grep "not found" || true
    done | sort -u
    openscad --version || true
    exit 1
fi

openscad --version 2>&1 | head -1
openscad --info 2>&1 | grep -iE '^(manifold|cgal) version' || true
