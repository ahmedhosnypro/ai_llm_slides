#!/usr/bin/env python3
"""slide_028 measurement pass 2 — precise blob detection with calibrated masks.
Verifies inherited blocks (k=0..4 chips, k=0..3 heads/labels) against slide_027's
certified values and measures the delta blocks (chips 5..8, heads 4..7, labels 4..7)
against the component's polar rules. Frame->slide mapping (parent-certified):
  slide_x = (frame_x-18.63)/0.96123 ; slide_y = frame_y/0.95556
"""
import numpy as np
from PIL import Image
from scipy import ndimage as ndi
import json

A = np.asarray(Image.open(
    "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_028.jpg"
).convert("RGB")).astype(int)
H, W = A.shape[:2]
r, g, b = A[:, :, 0], A[:, :, 1], A[:, :, 2]

def sx(fx): return (fx - 18.63) / 0.96123
def sy(fy): return fy / 0.95556

out = {}

# ---------- circle: FBFCC9-ish fill, largest blob right of x=350 ----------
cf = (r > 235) & (g > 235) & (b > 170) & (b < 230)
cf[:, :350] = False
lab, n = ndi.label(cf)
sizes = ndi.sum(cf, lab, range(1, n + 1))
big = int(np.argmax(sizes)) + 1
ys, xs = np.where(lab == big)
CXf, CYf = (xs.min() + xs.max()) / 2.0, (ys.min() + ys.max()) / 2.0
radf = ((xs.max() - xs.min()) + (ys.max() - ys.min())) / 4.0
print(f"circle: frame center ({CXf:.1f},{CYf:.1f}) fill r {radf:.1f} | slide center ({sx(CXf):.1f},{sy(CYf):.1f})")
out["circle"] = {"frame_c": [round(CXf, 1), round(CYf, 1)], "frame_r": round(float(radf), 1),
                 "slide_c": [round(sx(CXf), 1), round(sy(CYf), 1)]}

# 027 certified reference (slide pt)
REF = {
    "chips": [[762.6, 297.2], [738.4, 204.6], [672.3, 138.6], [581.1, 113.3], [490.4, 139.9]],
    "heads": [[776.4, 188.4], [692.6, 100.5], [585.6, 71.2], [473.3, 101.5]],
    "labels": [[840.2, 236.5], [788.8, 104.1], [642.8, 75.4], [520.6, 75.4]],
}
CXs, CYs = 581.0, 297.2
def polar_s(deg, rad):
    return (CXs + rad * np.cos(np.radians(deg)), CYs - rad * np.sin(np.radians(deg)))

def report(name, blobs, ref_list, polar_pred, k_of_ang):
    print(f"\n== {name} ==")
    rows = []
    for bl in blobs:
        k = k_of_ang(bl["ang"])
        pred = polar_pred(k)
        rows.append((k, bl, pred))
    rows.sort(key=lambda t: t[0])
    for k, bl, pred in rows:
        inherited = k < len(ref_list)
        ref = ref_list[k] if inherited else None
        ds = f" d_vs_027cert=({bl['slide'][0]-ref[0]:+.1f},{bl['slide'][1]-ref[1]:+.1f})" if inherited else ""
        dp = f" d_vs_polar=({bl['slide'][0]-pred[0]:+.1f},{bl['slide'][1]-pred[1]:+.1f})"
        print(f" k={k} ang {bl['ang']:6.1f} r_f {bl['radf']:6.1f} slide ({bl['slide'][0]:6.1f},{bl['slide'][1]:6.1f})"
              f" wh {bl['wh']}{ds}{dp}")
    out[name] = [{"k": k, "ang": bl["ang"], "radf": bl["radf"], "slide": bl["slide"], "wh": bl["wh"]} for k, bl, _ in rows]

# ---------- chips: green ----------
ch = ((g - r) > 25) & ((g - b) > 25)
lab, n = ndi.label(ch)
chips = []
for i in range(1, n + 1):
    ys, xs = np.where(lab == i)
    area = len(ys)
    if area < 250: continue
    h = ys.max() - ys.min(); w = xs.max() - xs.min()
    if w > 110 or h > 110: continue
    cx, cy = (xs.min() + xs.max()) / 2.0, (ys.min() + ys.max()) / 2.0
    ang = float(np.degrees(np.arctan2(-(cy - CYf), cx - CXf)) % 360)
    chips.append({"ang": round(ang, 1), "radf": round(float(np.hypot(cx - CXf, cy - CYf)), 1),
                  "slide": [round(sx(cx), 1), round(sy(cy), 1)], "wh": [int(w), int(h)], "area": int(area)})
kch = lambda a: int(round(a / 30)) % 12
report("chips", chips, REF["chips"], lambda k: polar_s(k * 30, 182.5), kch)

# ---------- heads: orange E06010 ----------
ah = (r > 160) & ((r - g) > 80) & ((g - b) > 40)
lab, n = ndi.label(ah)
heads = []
for i in range(1, n + 1):
    ys, xs = np.where(lab == i)
    area = len(ys)
    if area < 25 or area > 500: continue
    h = ys.max() - ys.min(); w = xs.max() - xs.min()
    if w > 28 or h > 28: continue
    cx, cy = (xs.min() + xs.max()) / 2.0, (ys.min() + ys.max()) / 2.0
    ang = float(np.degrees(np.arctan2(-(cy - CYf), cx - CXf)) % 360)
    heads.append({"ang": round(ang, 1), "radf": round(float(np.hypot(cx - CXf, cy - CYf)), 1),
                  "slide": [round(sx(cx), 1), round(sy(cy), 1)], "wh": [int(w), int(h)], "area": int(area)})
kh = lambda a: (int(round(a / 30)) % 12) - 1
report("heads", heads, REF["heads"], lambda k: polar_s((k + 1) * 30, 224.5), kh)

# ---------- labels: red CC0000-ish (incl JPEG-faded), annulus ----------
rl = (r > 150) & ((r - g) > 55) & (g < 175) & (b < 195)
Yg, Xg = np.mgrid[0:H, 0:W]
rr = np.hypot(Xg - CXf, Yg - CYf)
ann = rl & (rr > 190) & (rr < 330)
lab, n = ndi.label(ann)
labels = []
for i in range(1, n + 1):
    ys, xs = np.where(lab == i)
    area = len(ys)
    if area < 12: continue
    h = ys.max() - ys.min(); w = xs.max() - xs.min()
    if w > 50 or h > 26: continue
    cx, cy = (xs.min() + xs.max()) / 2.0, (ys.min() + ys.max()) / 2.0
    ang = float(np.degrees(np.arctan2(-(cy - CYf), cx - CXf)) % 360)
    labels.append({"ang": round(ang, 1), "radf": round(float(np.hypot(cx - CXf, cy - CYf)), 1),
                   "slide": [round(sx(cx), 1), round(sy(cy), 1)], "wh": [int(w), int(h)], "area": int(area)})
kl = lambda a: (int(round(a / 30)) % 12) - 1
report("labels", labels, REF["labels"], lambda k: polar_s((2 * k + 1) * 15, 255), kl)

# ---------- spokes at 270 / 330 (faint-ink ray scan, parent method) ----------
print("\n== faint-ink ray scan (270/330 deg, r 135..245 frame) ==")
for deg in (240, 270, 300, 330):
    hits = 0; tot = 0
    for rr_ in np.arange(135, 246, 1.0):
        x = CXf + rr_ * np.cos(np.radians(deg)); y = CYf - rr_ * np.sin(np.radians(deg))
        xi, yi = int(round(x)), int(round(y))
        if not (0 <= xi < W and 0 <= yi < H): continue
        c = A[yi, xi]
        d = (233 - c[0]) + (233 - c[1]) + (231 - c[2])
        tot += 1
        if d > 45: hits += 1
    print(f" {deg}deg: faint hits {hits}/{tot}")
    out[f"spoke_{deg}"] = [hits, tot]

json.dump(out, open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide028/measure2.json", "w"), indent=1)
print("\nsaved measure2.json")
