#!/usr/bin/env python3
"""dotfix_045.py — replace the tofu-rect \\cdot tokens (eq_045_dot_a/b.png) with real
round dots rendered via mathtext.fontset=dejavuserif (the CWD matplotlibrc selects it;
certified scripts/render_eq.py is used UNCHANGED). Re-solves the size from the same
target ink box as render_tokens_045.py (6x7 pt, solve='h') and updates
eq_045_manifest.json in place (placement fields preserved)."""
import json, subprocess, sys, os

SCRIPT = "/home/ahmed/Projects/ai_llm_slides/scripts/render_eq.py"
CWD = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/scratch_045/dotfix"
ASSETS = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/build/assets"
MANIFEST = f"{ASSETS}/eq_045_manifest.json"
LATEX = r"\cdot"
TARGET_W, TARGET_H, SOLVE = 6, 7, "w"  # round glyph is 1:1 — match width 6pt (closest to the original 6x7 ink box)
PAD_PT = 8 * 72.0 / 600.0

def render(png, size):
    out = subprocess.run([sys.executable, SCRIPT, LATEX, png, str(size), "#000000"],
                         capture_output=True, text=True, check=True, cwd=CWD)
    return json.loads(out.stdout)

man = json.load(open(MANIFEST))
# trial at 16pt to measure the glyph, then solve size exactly like render_tokens_045.py
t = render(f"{CWD}/dot_trial.png", 16)
ink_w = (t["w_px"] - 16) * 72.0 / 600.0
ink_h = (t["h_px"] - 16) * 72.0 / 600.0
size_h = 16.0 * TARGET_H / ink_h
size_w = 16.0 * TARGET_W / ink_w
size = round(size_h if SOLVE == "h" else size_w, 1)
print(f"trial 16pt ink {ink_w:.2f}x{ink_h:.2f}pt  -> solved size {size}pt (alt {round(size_w if SOLVE=='h' else size_h,1)})")

for name in ("dot_a", "dot_b"):
    final_png = f"{ASSETS}/eq_045_{name}.png"
    f = render(final_png, size)
    f["ink_w_pt"] = round((f["w_px"] - 16) * 72.0 / 600.0, 2)
    f["ink_h_pt"] = round((f["h_px"] - 16) * 72.0 / 600.0, 2)
    f["target_w"], f["target_h"] = TARGET_W, TARGET_H
    f["place_left"] = man[name]["place_left"]
    f["place_top"] = man[name]["place_top"]
    f["solve"] = SOLVE
    f["size_by_alt"] = round(size_w if SOLVE == "h" else size_h, 1)
    man[name] = f
    print(f"{name}: ink {f['ink_w_pt']}x{f['ink_h_pt']}pt (target {TARGET_W}x{TARGET_H})  "
          f"place {f['place_left']},{f['place_top']}")

with open(MANIFEST, "w") as fp:
    json.dump(man, fp, indent=1)
print("manifest updated")

# verify: no tofu rectangles remain among the final token PNGs
from PIL import Image
import numpy as np
bad = []
for name, tok in man.items():
    a = np.asarray(Image.open(tok["path"]).convert("RGBA"))
    ink = a[:, :, 3] > 40
    ys, xs = np.where(ink)
    sub = ink[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    rows = sub.sum(axis=1)
    if sub.mean() > 0.95 and float(np.std(rows)) < 0.5 and sub.shape[0] > 3:
        bad.append(name)
print("tofu scan:", "CLEAN" if not bad else f"STILL BAD: {bad}")
