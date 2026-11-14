#!/usr/bin/env python3
"""rb6 bracket PNGs for slide 007 panels 2/3: mathtext-rendered \\left( \\right)
delimiters around a \\phantom substack, so the delimiter height matches the
row stack and the tight PNG cannot collide with entries or the 3*1/4*3/4*1
labels (the rb5 JS text-bracket overflow is gone). 600 dpi tight PNGs.
"""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
EQDIR = os.path.join(HERE, "eq_007")
RENDER = os.path.join(HERE, "render_math.py")
SIZE = 20.0

ASSETS = [
    ("rb6_br3", [r"#000000:\left(\phantom{\substack{x\\[4pt]x\\[4pt]x}}\right)"], 0.87, 0.78, 10),
    ("rb6_br4", [r"#000000:\left(\phantom{\substack{x\\[14pt]x\\[14pt]x\\[14pt]x}}\right)"], 0.95, 1.28, 10),
]


def main():
    os.makedirs(EQDIR, exist_ok=True)
    manifest = {}
    for name, rows, maxw, maxh, rowgap in ASSETS:
        out = os.path.join(EQDIR, name + ".png")
        js = os.path.join(EQDIR, name + ".rb6.json")
        cmd = [sys.executable, RENDER, "--out", out, "--size", str(SIZE),
               "--maxw", str(maxw), "--maxh", str(maxh), "--rowgap", str(rowgap),
               "--out-json", js]
        for r in rows:
            cmd += ["--row", r]
        subprocess.run(cmd, check=True, cwd=HERE)
        with open(js) as fh:
            info = json.load(fh)
        manifest[name] = {"image": name + ".png", "w_in": info["w_in"], "h_in": info["h_in"]}
        print(name, info["w_in"], "x", info["h_in"], "in")
    with open(os.path.join(EQDIR, "rb6_manifest.json"), "w") as fh:
        json.dump(manifest, fh, indent=2)


if __name__ == "__main__":
    main()
