#!/usr/bin/env python3
"""m26: settle the crop-judge contested findings against the ORIGINAL frame (ground truth).
1. gamma/'and'/beta color classes (crop judge said green; m18 said dark red)
2. italic slant (centroid slope) for contested words vs roman/italic controls
3. underline probes: L2 red phrase, 'learn parameters'
4. eq4 red outline: ASCII + color class
5. eq3 blue outline: ASCII + color class
6. y_i ellipse interior fill mode
7. green highlight fills (intro vs panel params)
"""
import numpy as np
from PIL import Image

F = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_040.jpg").convert("RGB")
a = np.asarray(F).astype(int)
lum = (a[:, :, 0]*299 + a[:, :, 1]*587 + a[:, :, 2]*114)//1000

def modecol(x0, x1, y0, y1, lmin=140, lmax=256):
    """mode RGB of light pixels in box."""
    box = a[y0:y1, x0:x1].reshape(-1, 3)
    L = (box[:, 0]*299 + box[:, 1]*587 + box[:, 2]*114)//1000
    sel = box[(L >= lmin) & (L < lmax)]
    if len(sel) == 0:
        return None, 0
    q = (sel//8)*8
    keys, counts = np.unique(q, axis=0, return_counts=True)
    m = keys[counts.argmax()]
    return tuple(int(v) for v in m), int(counts.max())

print("== 1. gamma/and/beta color classes (rows 144..160) ==")
def classes(x0, x1, y0, y1, label):
    box = a[y0:y1, x0:x1].reshape(-1, 3)
    L = (box[:, 0]*299 + box[:, 1]*587 + box[:, 2]*114)//1000
    dark = box[L < 190]
    if len(dark) == 0:
        print(label, "no dark px"); return
    r, g, b = dark[:, 0], dark[:, 1], dark[:, 2]
    redish = (r > g + 40) & (r > b + 40)
    greenish = (g > r + 30) & (g > b + 30)
    bluish = (b > r + 30) & (b > g + 20)
    print(f"{label}: n_dark={len(dark)} red={int(redish.sum())} green={int(greenish.sum())} blue={int(bluish.sum())} mean_dark={dark.mean(axis=0).round(0)}")
classes(534, 549, 144, 160, "gamma  x534-548")
classes(551, 577, 144, 160, "and    x551-576")
classes(580, 597, 141, 160, "beta   x580-596")

print()
print("== 2. italic slant: per-row ink-centroid slope (px/row) ==")
def slant(x0, x1, y0, y1, label, thr=185):
    rows = []
    for y in range(y0, y1):
        xs = np.where(lum[y, x0:x1] < thr)[0]
        if len(xs) >= 2:
            rows.append((y, xs.mean() + x0, len(xs)))
    if len(rows) < 6:
        print(f"{label}: too few rows"); return
    ys = np.array([r[0] for r in rows], float)
    cs = np.array([r[1] for r in rows], float)
    span = ys.max() - ys.min()
    # use middle 60% rows to dodge serif flares
    lo, hi = np.percentile(ys, 20), np.percentile(ys, 80)
    m = (ys >= lo) & (ys <= hi)
    A = np.vstack([ys[m] - ys[m].mean(), np.ones(m.sum())]).T
    slope = (np.linalg.lstsq(A, cs[m], rcond=None)[0])[0]
    print(f"{label}: rows {int(ys.min())}..{int(ys.max())} slope={slope:+.3f} px/row -> drift over x-height {slope*(hi-lo):+.1f}px")
slant(105, 113, 115, 133, "ctrl I(Instead) roman?  x105-112")
slant(520, 596, 115, 135, "strictly (spec: italic) x520-595")
slant(593, 630, 115, 135, "Zero (bold)             x593-629")
slant(632, 680, 118, 133, "mean (blue)             x632-679")
slant(682, 710, 115, 133, "and  (blue)             x682-709")
slant(711, 752, 118, 133, "unit (bold blue)        x711-751")
slant(753, 823, 115, 135, "variance,(blue)         x753-822")
slant(598, 625, 140, 158, "ctrl that (black L2)    x598-624")
slant(663, 700, 143, 160, "convert (red L2)        x663-699")
slant(700, 906, 143, 160, "the-mean-and (red L2)   x700-905")
slant(105, 158, 164, 187, "variance (red L3)       x105-157")
slant(315, 391, 164, 187, "Minimizes (bold red)    x315-390")
slant(408, 435, 168, 187, "Loss. (bold red)        x408-434")

print()
print("== 3. underline probes (dark px per row, lum<190) ==")
def probe(x0, x1, y0, y1, label, thr=190):
    print(f"-- {label} x{x0}..{x1}")
    for y in range(y0, y1):
        xs = np.where(lum[y, x0:x1] < thr)[0]
        if len(xs):
            seg = xs + x0
            print(f"  y={y}: n={len(xs)} x {seg.min()}..{seg.max()}")
probe(640, 912, 155, 174, "L2 red phrase under-run")
probe(380, 540, 155, 174, "learn-parameters under-run")
probe(104, 440, 176, 190, "L3 underline (control, known present)")

print()
print("== 4. eq4 zone ASCII x160..255 y448..482 thr200 ==")
for y in range(448, 483):
    row = "".join("#" if lum[y, x] < 130 else ("+" if lum[y, x] < 200 else ".") for x in range(160, 256))
    print(f"{y:3d} {row}")
print("   " + "".join(str((160+i)//100 % 10) if (160+i) % 20 == 0 else " " for i in range(96)))
print("color samples of stroke pixels (lum<200) in zone:")
box = a[448:482, 160:256].reshape(-1, 3)
Lb = (box[:, 0]*299 + box[:, 1]*587 + box[:, 2]*114)//1000
sel = box[Lb < 200]
sel = sel[~((sel[:, 0] > 240) & (sel[:, 1] > 240) & (sel[:, 2] > 240))]
r, g, b = sel[:, 0], sel[:, 1], sel[:, 2]
orange = (r > 200) & (g > 120) & (g < 210) & (b < 120)
red = (r > 120) & (g < 110) & (b < 110) & ~orange
print(f"n={len(sel)} orange-class={int(orange.sum())} red-class={int(red.sum())} mean_all={sel.mean(axis=0).round(0)}")
if orange.sum():
    print("  mean orange:", sel[orange].mean(axis=0).round(0))
if red.sum():
    print("  mean red:   ", sel[red].mean(axis=0).round(0))
ys, xs = np.where((Lb < 200).reshape(448-448, 0)) if False else (None, None)

print()
print("== 5. eq3 zone ASCII x222..300 y393..452 thr200 ==")
for y in range(393, 453):
    row = "".join("#" if lum[y, x] < 130 else ("+" if lum[y, x] < 200 else ".") for x in range(222, 301))
    print(f"{y:3d} {row}")
print("stroke color classes in x222..300 y393..452:")
box = a[393:453, 222:301].reshape(-1, 3)
Lb = (box[:, 0]*299 + box[:, 1]*587 + box[:, 2]*114)//1000
sel = box[(Lb < 200) & ~((box[:, 0] > 240) & (box[:, 1] > 240) & (box[:, 2] > 240))]
r, g, b = sel[:, 0], sel[:, 1], sel[:, 2]
lav = (b > r + 15) & (r > 90) & (r < 200)
blue = (b > r + 60) & (r < 120)
dark = (Lb.reshape(-1)[ (Lb<200) & ~((box[:,0]>240)&(box[:,1]>240)&(box[:,2]>240)) ] < 120)
print(f"n={len(sel)} lavender-class={int(lav.sum())} strongblue={int(blue.sum())} verydark={int(dark.sum())} mean_all={sel.mean(axis=0).round(0)}")
if lav.sum():
    print("  mean lav:", sel[lav].mean(axis=0).round(0))
if blue.sum():
    print("  mean blue:", sel[blue].mean(axis=0).round(0))

print()
print("== 6. y_i ellipse interior fill ==")
m, n = modecol(173, 190, 457, 473, 150, 256)
print(f"ellipse interior mode: {m} (n={n})")
m2, n2 = modecol(174, 189, 458, 472, 180, 256)
print(f"ellipse interior mode(180+): {m2} (n={n2})")

print()
print("== 7. green highlight fills ==")
m, n = modecol(392, 530, 146, 158, 150, 256)
print(f"intro 'learn parameters' fill mode: {m} (n={n})")
m, n = modecol(206, 424, 228, 248, 150, 256)
print(f"panel params-line fill mode: {m} (n={n})")
