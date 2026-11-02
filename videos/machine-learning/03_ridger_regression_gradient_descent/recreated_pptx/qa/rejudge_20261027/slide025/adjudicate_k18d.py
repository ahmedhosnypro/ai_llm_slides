#!/usr/bin/env python3
"""Round 4: NCC matching of render BL label crops vs orig label crops (which label is where)."""
import numpy as np
from PIL import Image

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
Q = NS + "/recreated_pptx/qa/rejudge_20261027/slide025"
ORIG = NS + "/unique_slides/slide_025.jpg"
S = 2001 / 960.0

orig = np.asarray(Image.open(ORIG).convert("RGB")).astype(int)
ren = np.asarray(Image.open(Q + "/render_18.png").convert("RGB")).astype(int)

def crop(a, x0, y0, x1, y1, scale):
    return a[int(y0*scale):int(np.ceil(y1*scale))+1, int(x0*scale):int(np.ceil(x1*scale))+1]

def dark(a, t=170):
    return (a.max(2) < t).astype(float)

def ncc(a, b):
    a = np.asarray(Image.fromarray((a*255).astype(np.uint8)).resize((64, 24), Image.LANCZOS)).astype(float)/255.0
    b = np.asarray(Image.fromarray((b*255).astype(np.uint8)).resize((64, 24), Image.LANCZOS)).astype(float)/255.0
    a = a - a.mean(); b = b - b.mean()
    return float((a*b).sum() / (np.sqrt((a*a).sum()*(b*b).sum()) + 1e-9))

# anchor boxes: (name, x0,y0,x1,y1)
BOX = {
    "GM_max(orig top)": (242, 304, 268, 319),
    "LM_max": (286, 337, 315, 352),
    "LM_min": (286, 390, 311, 399),
    "GM_min(orig bl)": (145, 439, 201, 465),
}
pad = 10
print("NCC matrix: rows = render crop at anchor, cols = orig crop at anchor")
orig_crops = {}
for name, (x0, y0, x1, y1) in BOX.items():
    orig_crops[name] = dark(crop(orig, x0-pad, y0-pad, x1+pad, y1+pad, 1.0))
ren_crops = {}
for name, (x0, y0, x1, y1) in BOX.items():
    c = crop(ren, x0-pad, y0-pad, x1+pad, y1+pad, S)
    # resize render crop to orig crop size
    oc = orig_crops[name]
    rs = np.asarray(Image.fromarray(c.astype(np.uint8)).convert("L").resize((oc.shape[1], oc.shape[0]), Image.LANCZOS)).astype(float)
    rs = (rs < 170).astype(float)
    ren_crops[name] = rs
names = list(BOX)
print("render-anchor \\ orig-anchor      " + "  ".join(f"{n[:12]:>12}" for n in names))
for rn in names:
    row = [f"{ncc(ren_crops[rn], orig_crops[on]):+.3f}" for on in names]
    print(f"{rn[:24]:<26}" + "  ".join(f"{v:>12}" for v in row))

# also: ink counts per render anchor box at thresholds
print()
print("render ink counts per anchor box (thresholds 120/170/220):")
for name, (x0, y0, x1, y1) in BOX.items():
    c = crop(ren, x0, y0, x1, y1, S)
    oc = crop(orig, x0, y0, x1, y1, 1.0)
    vals = []
    for t in (120, 170, 220):
        vals.append(int((c.max(2) < t).sum()))
    ov = int((oc.max(2) < 170).sum())
    print(f"  {name:<20} render ink@120/170/220 = {vals}   orig ink@170 = {ov}")
