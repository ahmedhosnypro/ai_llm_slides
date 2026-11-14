#!/usr/bin/env python3
import json
import os
import gen_eq_036_rb4 as base
from PIL import Image

EQ = base.EQ36
manifest_path = os.path.join(EQ, "eq_s36rb5_manifest.json")
with open(manifest_path) as fh:
    manifest = json.load(fh)

for name, lower in [("s36rb4_b_top", False), ("s36rb4_b_bot", True)]:
    term = r"[W_i^T X_j]^2" if lower else r"W^T X_i"
    segs = [["all", base.BLACK, r"b=-\frac{1}{2}\left[\max_{i:y_i=-1}" + term + r"+\min_{i:y_i=+1}" + term + r"\right]"]]
    canvas, boxes, pt, w_in, h_in = base.fit(segs, 7.1, 0.60 if lower else 0.45)
    Image.fromarray(canvas).save(os.path.join(EQ, name + ".png"))
    m = manifest[name]
    m.update(w_in=w_in, h_in=h_in, fontsize_pt=pt, segments={"all": boxes["all"]}, highlights=[])
    print(name, w_in, h_in)

manifest["s36rb4_kern"]["image"] = "s36rb4_kern_fix.png"
segs = [["k", base.RED, r"K(a,b)=\left[a^T b\right]^2"]]
canvas, boxes, pt, w_in, h_in = base.fit(segs, 1.9, 0.42)
Image.fromarray(canvas).save(os.path.join(EQ, "s36rb4_kern_fix.png"))
manifest["s36rb4_kern"].update(w_in=w_in, h_in=h_in, fontsize_pt=pt)
with open(manifest_path, "w") as fh:
    json.dump(manifest, fh, indent=1)
