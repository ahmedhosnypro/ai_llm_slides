#!/usr/bin/env python3
import json, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "eq_008")
row = r"#1A1A1A:3x + 4y \leq 80"
out = os.path.join(OUT, "c5.png")
js = os.path.join(OUT, "c5.json")
subprocess.run([sys.executable, os.path.join(HERE, "render_math.py"), "--out", out,
                "--size", "26.0", "--maxw", "1.80", "--maxh", "0.30",
                "--row", row, "--out-json", js], check=True, cwd=HERE)
info = json.load(open(js))
man = json.load(open(os.path.join(OUT, "manifest.json")))
man["c5"] = {"image": "c5.png", "w_in": info["w_in"], "h_in": info["h_in"], "pt": info["fontsize_pt"][0]}
json.dump(man, open(os.path.join(OUT, "manifest.json"), "w"), indent=2)
print("c5", man["c5"])
