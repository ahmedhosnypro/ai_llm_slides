#!/usr/bin/env python3
"""slide033 selfcheck_final: render_5 key bands + frame containment assertions."""
import numpy as np
from PIL import Image
import scipy.ndimage as ndi

REN = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/qa/slide033/render_5.png"
ra = np.asarray(Image.open(REN).convert("RGB")).astype(int)
H, W, _ = ra.shape
RPT = 72 / 150.0
ok = lambda d: "OK " if d <= 5 else ("~  " if d <= 9 else "DIFF")

def band(x0, x1, y0, y1, mask_fn, label, target, gap=5):
    sub = ra[int(y0/RPT):int(y1/RPT), int(x0/RPT):int(x1/RPT)]
    m = mask_fn(sub[..., 0], sub[..., 1], sub[..., 2])
    lab, n = ndi.label(m, structure=np.ones((3, 3)))
    boxes = []
    for i in range(1, n + 1):
        ys, xs = np.where(lab == i)
        if len(ys) < 4: continue
        boxes.append([xs.min(), ys.min(), xs.max(), ys.max()])
    if not boxes:
        print(f"[NO INK] {label}")
        return
    x0m = min(b[0] for b in boxes) * RPT + x0
    x1m = max(b[2] for b in boxes) * RPT + x0
    y0m = min(b[1] for b in boxes) * RPT + y0
    y1m = max(b[3] for b in boxes) * RPT + y0
    d = max(abs(x0m - target[0]), abs(x1m - target[1]), abs(y0m - target[2]), abs(y1m - target[3]))
    print(f"[{ok(d)}] {label:26s} ren ({x0m:.0f},{x1m:.0f} x {y0m:.0f},{y1m:.0f}) tgt {target} d={d:.1f}")

navy = lambda r, g, b: (b > 100) & (r < 100) & (b - r > 40)
red = lambda r, g, b: (r > 130) & (g < 100) & (b < 100)
dark = lambda r, g, b: (r < 120) & (g < 120) & (b < 120)
anyd = lambda r, g, b: (r < 150) & (g < 150) & (b < 150)

print("== key text bands (target = original measured) ==")
band(100, 850, 70, 100, navy, "subtitle", (129.4, 812.9, 74.3, 94.2))
band(432, 768, 112, 140, anyd, "defs L1", (434.2, 762.9, 122.4, 135.0))
band(792, 898, 112, 140, anyd, "example E1", (797.3, 862.8, 122.4, 136.0))
band(478, 888, 313, 334, navy, "omega A1", (482.1, 778.6, 320.2, 329.6))
band(478, 888, 334, 354, navy, "omega A2", (481.0, 775.4, 339.1, 348.5))
band(478, 888, 415, 444, navy, "omega B1 row", (488.3, 863.9, 424.9, 437.4))
band(478, 888, 444, 462, navy, "omega B2 row", (488.3, 848.3, 443.7, 454.2))
band(478, 888, 464, 490, navy, "omega Note", (487.3, 519.5, 475.1, 484.5))
band(478, 888, 490, 510, navy, "omega C2", (491.4, 873.2, 494.0, 506.5))
band(478, 888, 508, 530, navy, "omega C3", (491.4, 835.8, 512.8, 525.3))
band(52, 200, 240, 262, dark, "info L1", (78.4, 171.0, 245.9, 257.4))
band(715, 885, 358, 418, red, "eq box ring", (715.1, 882.6, 359.0, 415.5))
band(720, 762, 374, 398, red, "eq omega", (731.7, 747.3, 379.9, 391.4))
band(810, 832, 362, 382, dark, "eq '1'", (818.1, 821.2, 367.3, 378.8))
band(780, 845, 392, 416, dark, "eq '10,000'", (786.9, 837.9, 397.7, 409.2))
band(320, 400, 138, 162, anyd, "pair1 L1", (318.7, 385, 141.3, 155.9))
band(404, 445, 514, 537, red, "dx1 label", (407.2, 439.4, 513.8, 534.8))

print("== FRAME CONTAINMENT (self-check #2): content ink inside panel x42..918, y45..540 ==")
ink = ra.mean(axis=2) < 200
ink[:93, :] = False; ink[1116:, :] = False   # exclude chrome border rows
ys, xs = np.where(ink)
print(f"  content ink bbox: x {xs.min()*RPT:.1f}..{xs.max()*RPT:.1f} y {ys.min()*RPT:.1f}..{ys.max()*RPT:.1f}")
viol = 0
if xs.min() * RPT < 41.0 or xs.max() * RPT > 919.5: print("  [X] horizontal overflow"); viol += 1
if ys.min() * RPT < 44.0 or ys.max() * RPT > 539.6: print("  [X] vertical overflow"); viol += 1
print("  containment:", "PASS" if viol == 0 else "FAIL")

# panel containment: defs/example/omega boxes' text inside their boxes
def inside(label, bx0, bx1, by0, by1, x0, x1, y0, y1):
    sub = ra[int(y0/RPT):int(y1/RPT), int(x0/RPT):int(x1/RPT)]
    m = sub.mean(axis=2) < 185
    ys, xs = np.where(m)
    if len(ys) == 0:
        print(f"  [NO INK] {label}"); return
    X0, X1 = xs.min() * RPT + x0, xs.max() * RPT + x0
    Y0, Y1 = ys.min() * RPT + y0, ys.max() * RPT + y0
    pad_l, pad_r, pad_t, pad_b = X0 - bx0, bx1 - X1, Y0 - by0, by1 - Y1
    good = pad_l > 0 and pad_r > 0 and pad_t > 0 and pad_b > 0
    print(f"  [{'OK ' if good else 'X'}] {label:12s} pads L{pad_l:.1f} R{pad_r:.1f} T{pad_t:.1f} B{pad_b:.1f}")

print("== per-box containment ==")
inside("defs box", 427.5, 770.8, 106.3, 300.9, 428, 770, 107, 300)
inside("example box", 789.5, 902.9, 106.3, 299.8, 790, 902, 107, 299)
inside("omega box", 474.5, 892, 312, 533, 475, 891, 313, 532)
inside("info box", 48.7, 201.7, 238.1, 336.5, 49, 201, 239, 336)
inside("eq subbox", 718.7, 880, 362.6, 412.9, 719, 879, 363, 412)

print("== EQUATION REGIONS HAVE INK (self-check #3) ==")
for label, x0, x1, y0, y1, mf in [("eq omega", 720, 762, 374, 398, red), ("eq K", 744, 766, 388, 402, navy),
                                   ("eq bars+bar", 760, 870, 380, 392, navy), ("eq 1", 810, 832, 362, 382, dark),
                                   ("eq 10000", 780, 845, 392, 416, dark), ("eq 2k/d", 835, 868, 386, 406, red)]:
    sub = ra[int(y0/RPT):int(y1/RPT), int(x0/RPT):int(x1/RPT)]
    n = int(mf(sub[..., 0], sub[..., 1], sub[..., 2]).sum())
    print(f"  [{'OK ' if n > 20 else 'X'}] {label}: {n} ink px")
print("== pair formula PNGs have ink ==")
for i, y0, y1 in [(1, 136, 162), (2, 204, 228), (3, 272, 298), (4, 372, 398), (5, 471, 499)]:
    sub = ra[int(y0/RPT):int(y1/RPT), int(320/RPT):int(400/RPT)]
    n = int((np.abs(sub - sub.mean(axis=2, keepdims=True)).sum(axis=2) > 60).sum())
    print(f"  [{'OK ' if n > 60 else 'X'}] pair box {i} lines: {n} chroma px")
