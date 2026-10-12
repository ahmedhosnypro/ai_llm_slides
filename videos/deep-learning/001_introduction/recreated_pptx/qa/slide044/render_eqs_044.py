#!/usr/bin/env python3
"""render_eqs_044.py — render slide 044's math tokens via the certified render_eq.py,
size-solved against the frame's measured ink boxes. Targets (frame px = pt):
  s=1,        ink w~62 band y137..152  (ink left 173, baseline 150)
  (h_f-1)/2   ink w~97 band y136..157  (ink left 496, baseline 150)
  (w_f-1)/2   ink w~106 band y136..156 (ink left 651, baseline 150)
  \\ast        ink 7x7 at (407..413, 278..284)
  =           ink 14x6 at (546..559, 276..281)
"""
import json, subprocess, sys
from PIL import Image
import numpy as np

BASE = "/home/ahmed/Projects/ai_llm_slides"
ASSETS = f"{BASE}/videos/deep-learning/001_introduction/recreated_pptx/build/assets"

SPECS = [
    ("eq_044_s1",    r"s\;\;=\;\;1,",      62, 173, 150),
    ("eq_044_htok",  r"(h_f-1)/2",         97, 496, 150),
    ("eq_044_wtok",  r"(w_f-1)/2",        106, 651, 150),
    ("eq_044_ast",   r"\ast",               7, 410, None),   # center-placed at (410,281)
    ("eq_044_eq",    r"=",                 14, 552, None),   # center-placed at (552.5,278.5)
]

def render(latex, out, size):
    r = subprocess.run([sys.executable, f"{BASE}/scripts/render_eq.py", latex, out, str(size), "000000"],
                       capture_output=True, text=True)
    if r.returncode != 0:
        print("FAIL", latex, r.stdout, r.stderr)
        return None
    return json.loads(r.stdout)

results = {}
for name, latex, tgt_w, left, baseline in SPECS:
    size = 20.0
    best = None
    for _ in range(6):
        out = f"{ASSETS}/{name}.png"
        info = render(latex, out, size)
        if info is None:
            break
        # actual ink (tight PNG minus the 8px pad each side)
        im = Image.open(out)
        alpha = np.asarray(im)[..., 3]
        ys, xs = np.where(alpha > 8)
        ink_w = (xs.max() - xs.min() + 1) / 600 * 72  # pt
        ink_h = (ys.max() - ys.min() + 1) / 600 * 72
        err = abs(ink_w - tgt_w)
        if best is None or err < best["err"]:
            best = {"err": err, "size": size, "ink_w": ink_w, "ink_h": ink_h, "info": info, "png": out}
        if err <= 1.5:
            break
        size = round(size * tgt_w / ink_w, 1)
    if best:
        results[name] = best
        print(f"{name}: size {best['size']} ink {best['ink_w']:.1f}x{best['ink_h']:.1f}pt (target w {tgt_w}) "
              f"baseline_frac {best['info']['baseline_frac']:.4f} err {best['err']:.1f}")
json.dump({k: {"size": v["size"], "ink_w": v["ink_w"], "ink_h": v["ink_h"],
               "sidecar": v["info"]} for k, v in results.items()},
          open(f"{ASSETS}/eq_044_manifest.json", "w"), indent=1)
print("manifest written")
