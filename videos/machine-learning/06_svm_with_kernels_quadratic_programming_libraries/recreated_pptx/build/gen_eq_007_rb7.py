#!/usr/bin/env python3
"""rb7: dimension annotations as true subscripts (_{3*1} etc.), small red,
placed at the bottom-right of the closing bracket by slide_007.js."""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
EQDIR = os.path.join(HERE, "eq_007")
RENDER = os.path.join(HERE, "render_math.py")
SIZE = 20.0

ASSETS = [
    ("rb5_ann31", r"#FF0000:_{3*1}", 0.50, 0.26),
    ("rb5_ann43", r"#FF0000:_{4*3}", 0.50, 0.26),
    ("rb5_ann41", r"#FF0000:_{4*1}", 0.50, 0.26),
]


def main():
    man_path = os.path.join(EQDIR, "rb5_manifest.json")
    manifest = json.load(open(man_path))
    for name, row, maxw, maxh in ASSETS:
        out = os.path.join(EQDIR, name + ".png")
        js = os.path.join(EQDIR, name + ".rb7.json")
        cmd = [sys.executable, RENDER, "--out", out, "--size", str(SIZE),
               "--maxw", str(maxw), "--maxh", str(maxh), "--rowgap", "10",
               "--out-json", js, "--row", row]
        subprocess.run(cmd, check=True, cwd=HERE)
        with open(js) as fh:
            info = json.load(fh)
        manifest[name] = {"image": name + ".png", "w_in": info["w_in"], "h_in": info["h_in"]}
        print(name, info["w_in"], "x", info["h_in"], "in")
    with open(man_path, "w") as fh:
        json.dump(manifest, fh, indent=2)


if __name__ == "__main__":
    main()
