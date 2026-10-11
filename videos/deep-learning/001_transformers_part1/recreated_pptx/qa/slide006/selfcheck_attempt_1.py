#!/usr/bin/env python3
"""selfcheck_attempt_1.py — closed-loop structural check: render vs original measurements.
Render 150dpi (2000x1125); 72-dpi frame px * 2.08333 = render px.
"""
from PIL import Image
import numpy as np

R = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/scratch/slide006/render/slide-1.png"
im = Image.open(R).convert("RGB")
a = np.asarray(im).astype(int)
H, W = a.shape[:2]
S = 150 / 72.0
print(f"render {W}x{H} (scale {S:.4f})")

fails = []
def check(name, ok, detail):
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}: {detail}")
    if not ok: fails.append(name)

def pxy(x72, y72):
    return int(round(x72 * S)), int(round(y72 * S))

def sample(x72, y72, r=2):
    x, y = pxy(x72, y72)
    reg = a[max(0,y-r):y+r+1, max(0,x-r):x+r+1].reshape(-1,3)
    med = np.median(reg, axis=0).astype(int)
    return tuple(med)

def near(c1, c2, tol=40):
    return sum(abs(a-b) for a, b in zip(c1, c2)) <= tol

def ink_bbox(x072, y072, x172, y172, thresh=500):
    """ink pixels (dark-ish) in region, bbox in 72-space."""
    x0, y0 = pxy(x072, y072); x1, y1 = pxy(x172, y172)
    reg = a[y0:y1+1, x0:x1+1]
    m = reg.sum(axis=2) < thresh
    if not m.any(): return None
    ys, xs = np.where(m)
    return ((x0+xs.min())/S, (y0+ys.min())/S, (x0+xs.max())/S, (y0+ys.max())/S, int(m.sum()))

def nonbg_bbox(x072, y072, x172, y172, ref, tol=90):
    x0, y0 = pxy(x072, y072); x1, y1 = pxy(x172, y172)
    reg = a[y0:y1+1, x0:x1+1]
    d = np.abs(reg - np.array(ref)).sum(axis=2)
    m = d > tol
    if not m.any(): return None
    ys, xs = np.where(m)
    return ((x0+xs.min())/S, (y0+ys.min())/S, (x0+xs.max())/S, (y0+ys.max())/S, int(m.sum()))

print("\n== FILL SAMPLES (expect measured original colors) ==")
fills = [
    ("decoder container", 700, 135, (253,255,133)),
    ("green bar cell", 545, 208, (232,255,110)),
    ("hidden bar cell", 545, 264, (250,236,105)),
    ("encoder container", 300, 470, (248,213,173)),
    ("pink bar cell", 150, 330, (242,199,167)),
    ("tan bar cell", 150, 414, (249,213,163)),
    ("callout fill", 620, 422, (246,220,221)),
]
for name, x, y, want in fills:
    got = sample(x, y)
    check(f"fill {name}", near(got, want, 60), f"got #{got[0]:02x}{got[1]:02x}{got[2]:02x} want #{want[0]:02x}{want[1]:02x}{want[2]:02x}")

print("\n== RED DOTS ==")
for name, x, y in [("decoder dot", 513.5, 262.5), ("encoder dot", 469, 326.5)]:
    got = sample(x, y, 1)
    ok = got[0] > 110 and got[1] < 90 and got[2] < 90
    check(f"{name} reddish", ok, f"#{got[0]:02x}{got[1]:02x}{got[2]:02x}")

print("\n== TEXT/INK PRESENCE + POSITION (72-space bbox vs original) ==")
txt = [
    ("title", 250, 50, 660, 90, (265, 59, 640, 80)),
    ("dec caption", 660, 85, 845, 112, (677, 91, 827, 107)),
    ("o1", 540, 125, 566, 145, (547, 131, 558, 139)),
    ("o2", 672, 125, 698, 145, (678, 131, 690, 139)),
    ("o3", 803, 125, 829, 145, (809, 131, 821, 139)),
    ("softmax1", 485, 168, 552, 190, (488, 175, 546, 181)),
    ("s1 label", 608, 270, 632, 286, (613, 274, 626, 281)),
    ("h1 label", 205, 308, 230, 330, (212, 313, 223, 326)),
    ("emb1 label", 55, 358, 158, 384, (62, 364, 152, 377)),
    ("x1 label", 146, 468, 172, 490, (153, 474, 166, 483)),
    ("callout text", 565, 410, 830, 435, (579, 417, 818, 430)),
    ("enc caption", 210, 500, 380, 535, (223, 509, 368, 526)),
]
for name, x0, y0, x1, y1, orig in txt:
    bb = ink_bbox(x0, y0, x1, y1)
    if bb is None:
        check(f"ink {name}", False, "NO INK FOUND")
        continue
    bx0, by0, bx1, by1, n = bb
    dx = (bx0 + bx1) / 2 - (orig[0] + orig[2]) / 2
    dy = (by0 + by1) / 2 - (orig[1] + orig[3]) / 2
    ok = abs(dx) <= 4 and abs(dy) <= 4
    check(f"ink {name}", ok, f"bbox=({bx0:.0f},{by0:.0f})-({bx1:.0f},{by1:.0f}) vs orig {orig} dcenter=({dx:+.1f},{dy:+.1f}) n={n}")

print("\n== ARROW/STRUCTURE INK (local ink presence) ==")
def has_ink(x072, y072, r=4, thresh=620):
    x, y = pxy(x072, y072)
    reg = a[max(0,y-r):y+r+1, max(0,x-r):x+r+1]
    return bool((reg.sum(axis=2) < thresh).any())
arr = [
    ("dec up-arrow col1", 554, 172), ("dec down-arrow col1", 554, 236),
    ("dec s1 arrow", 620, 264.5), ("dec s3 arrow", 880, 264.5),
    ("enc in-arrow", 90, 329.5), ("enc h1 arrow", 225, 329.5), ("enc h2 arrow", 358, 329.5),
    ("enc emb-arrow col1", 161, 372), ("enc x-arrow col1", 161, 448),
    ("curve A mid", 600, 205), ("curve B mid", 731, 205),
    ("leader line mid", 514, 366),
    ("divider g1", 535.25, 208), ("divider g2", 554.5, 208), ("divider g3", 573.75, 208),
]
for name, x, y in arr:
    check(f"ink {name}", has_ink(x, y), f"ink present at ({x},{y})")

print("\n== CONTAINMENT (content within panel x42..918 y45..539) ==")
# outer strip outside panel must be pure white canvas (no content bleed)
strip_l = a[:, :int(40*S)]
strip_r = a[:, int(921*S):]
strip_t = a[:int(43*S), :]
ok_l = bool((np.abs(strip_l - 255).sum(axis=2) < 30).mean() > 0.99)
ok_r = bool((np.abs(strip_r - 255).sum(axis=2) < 30).mean() > 0.99)
ok_t = bool((np.abs(strip_t - 255).sum(axis=2) < 30).mean() > 0.99)
check("no bleed left", ok_l, f"white frac {np.abs(strip_l - 255).sum(axis=2).mean():.1f}")
check("no bleed right", ok_r, f"white frac {np.abs(strip_r - 255).sum(axis=2).mean():.1f}")
check("no bleed top", ok_t, f"white frac {np.abs(strip_t - 255).sum(axis=2).mean():.1f}")

print("\n" + ("ALL SELF-CHECKS PASS" if not fails else f"FAILURES: {fails}"))

# WIDTH CHECKS appended (attempt 1 iteration 2): text ink width vs original
print("\n== TEXT WIDTH CHECKS (render vs original, tol 8px) ==")
wchecks = [
    ("title", 250, 50, 660, 90, 375),
    ("dec caption", 660, 85, 845, 112, 150),
    ("softmax1", 485, 168, 552, 190, 58),
    ("emb1 label", 50, 358, 158, 384, 90),
    ("callout text", 565, 410, 830, 435, 239),
    ("enc caption", 210, 500, 380, 535, 145),
    ("o1", 540, 125, 566, 145, 11),
    ("s1 label", 605, 270, 635, 286, 13),
    ("h1 label", 205, 306, 232, 326, 11),
    ("x1 label", 146, 468, 172, 490, 13),
]
for name, x0, y0, x1, y1, worig in wchecks:
    bb = ink_bbox(x0, y0, x1, y1)
    if bb is None:
        check(f"width {name}", False, "NO INK")
        continue
    w = bb[2] - bb[0]
    check(f"width {name}", abs(w - worig) <= 8, f"w={w:.1f} vs orig {worig}")
print("FINAL:", "ALL PASS" if not fails else f"FAILURES: {fails}")
