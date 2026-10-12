#!/usr/bin/env python3
# m11_final.py — braces 1/2, brace3 profile, result band, canvas border, color cores
from PIL import Image
import numpy as np

im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_012.jpg').convert('RGB')
a = np.asarray(im).astype(int)
r, g, b = a[..., 0], a[..., 1], a[..., 2]
lum = (r + g + b) / 3

def med(x0, y0, x1, y1):
    return tuple(int(v) for v in np.median(a[y0:y1, x0:x1].reshape(-1, 3), axis=0))

def spans(mask1d, base=0, minlen=1):
    out, s = [], None
    for i, v in enumerate(mask1d):
        if v and s is None: s = i
        if not v and s is not None:
            if i - s >= minlen: out.append((base + s, base + i - 1))
            s = None
    if s is not None: out.append((base + s, base + len(mask1d) - 1))
    return out

print("=== A. BRACE1 / BRACE2 any-ink scans ===")
ink = lum < 228
for (x0, x1, nm) in [(392, 414, "brace1"), (556, 578, "brace2")]:
    m = ink[140:365, x0:x1]
    ys, xs = np.where(m)
    if len(ys):
        print(f"{nm}: fx {xs.min()+x0}..{xs.max()+x0} fy {ys.min()+140}..{ys.max()+140} n={len(ys)}")
        zc = a[140:365, x0:x1][m]
        redish = zc[(zc[:, 0] - zc[:, 1] > 25) & (zc[:, 0] > 120)]
        print(f"  red-ish core:", tuple(int(v) for v in np.median(redish, axis=0)) if len(redish) else None, "n=", len(redish))
        for yy in [150, 170, 190, 210, 230, 245, 250, 255, 260, 270, 290, 310, 330, 350, 358]:
            seg = np.where(ink[yy, x0:x1])[0]
            if len(seg):
                print(f"  fy {yy}: fx {seg.min()+x0}..{seg.max()+x0}")
print("\n=== B. BRACE3 profile ===")
ink3 = lum < 228
for yy in range(148, 366, 4):
    seg = np.where(ink3[yy, 712:745])[0]
    if len(seg):
        print(f"fy {yy}: fx {seg.min()+712}..{seg.max()+712}")
zc = a[150:360, 714:732]
m3 = (zc[..., 0] - zc[..., 1] > 25) & (zc[..., 0] > 120)
print("brace3 red core:", tuple(int(v) for v in np.median(zc[m3], axis=0)) if m3.sum() else None, "n=", int(m3.sum()))

print("\n=== C. RESULT BAND full ASCII (fx 255..705, fy 410..445, step2) ===")
def cls(px):
    rr, gg, bb = int(px[0]), int(px[1]), int(px[2])
    L = (rr + gg + bb) / 3
    if bb - rr > 18 and bb - gg > 12: return 'B' if bb > 150 else 'l'
    if rr - gg > 30 and bb - gg > 30: return 'M'
    if rr - gg > 35 and rr > 130 and bb < 120: return 'R'
    if L < 190: return 'k'
    return '.'
for yy in range(410, 446):
    row = "".join(cls(a[yy, x]) for x in range(255, 705, 2))
    print(f"fy {yy:3d} {row}")

print("\n=== D. color cores ===")
# subtitle deep blue cores
m = (b > 150) & (b - r > 60) & (g < 110)
z = a[80:98, 62:845][m[80:98, 62:845]]
print("subtitle deep-blue core:", tuple(int(v) for v in np.median(z, axis=0)) if len(z) else None, "n=", len(z))
# result-token deep cores (whole band)
m2 = (lum < 200)
z2 = a[420:445, 255:705][m2[420:445, 255:705]]
dk = z2[z2.sum(axis=1) < 400]
print("result band dark core:", tuple(int(v) for v in np.median(dk, axis=0)) if len(dk) else None, "n=", len(dk))
# X-circle glyph cores (fx 105..245, fy 160..186), dark pixels
z3 = a[160:186, 105:245].reshape(-1, 3)
dk3 = z3[z3.sum(axis=1) < 380]
print("X-circle glyph core:", tuple(int(v) for v in np.median(dk3, axis=0)) if len(dk3) else None, "n=", len(dk3))
pur = dk3[(dk3[:, 0] - dk3[:, 1] > 25) & (dk3[:, 2] - dk3[:, 1] > 25)]
print("  purple-ish:", tuple(int(v) for v in np.median(pur, axis=0)) if len(pur) else None, "n=", len(pur))
# circle fills (between glyphs): sample corners
print("circle fill samples:", med(120, 165, 124, 169), med(150, 165, 154, 169), med(184, 165, 188, 169), med(215, 165, 219, 169))
# embed label line colors
z4 = a[128:137, 91:215].reshape(-1, 3)
dk4 = z4[z4.sum(axis=1) < 420]
print("embed line1 core:", tuple(int(v) for v in np.median(dk4, axis=0)) if len(dk4) else None, "n=", len(dk4))
z5 = a[142:156, 91:230].reshape(-1, 3)
dk5 = z5[z5.sum(axis=1) < 420]
print("embed line2 core:", tuple(int(v) for v in np.median(dk5, axis=0)) if len(dk5) else None, "n=", len(dk5))
bl5 = z5[(z5[:, 2] - z5[:, 0] > 30)]
print("  line2 blue-ish:", tuple(int(v) for v in np.median(bl5, axis=0)) if len(bl5) else None, "n=", len(bl5))
# title core (strict red)
z6 = a[56:76, 62:850].reshape(-1, 3)
t6 = z6[(z6[:, 0] > 150) & (z6[:, 1] < 80) & (z6[:, 2] < 80)]
print("title red core:", tuple(int(v) for v in np.median(t6, axis=0)) if len(t6) else None, "n=", len(t6))
# caption red core
z7 = a[392:412, 240:740].reshape(-1, 3)
t7 = z7[(z7[:, 0] > 130) & (z7[:, 0] - z7[:, 1] > 35)]
print("caption red core:", tuple(int(v) for v in np.median(t7, axis=0)) if len(t7) else None, "n=", len(t7))
# y-strip label red core (strict)
z8 = a[362:380, 250:740].reshape(-1, 3)
t8 = z8[(z8[:, 0] > 130) & (z8[:, 0] - z8[:, 1] > 40) & (z8[:, 2] < 110)]
print("y-label red core:", tuple(int(v) for v in np.median(t8, axis=0)) if len(t8) else None, "n=", len(t8))
# cell W-label cores per row, strict saturated only
for (y0, y1, rn) in [(174, 196, "r1"), (211, 234, "r2"), (253, 275, "r3"), (291, 314, "r4")]:
    z9 = a[y0:y1, 250:740].reshape(-1, 3)
    for nm, pr in [("blue", lambda p: (p[2] - p[0] > 60) & (p[2] > 120)),
                   ("purple", lambda p: (p[0] - p[1] > 40) & (p[2] - p[1] > 40)),
                   ("orange", lambda p: (p[0] - p[2] > 60) & (p[0] - p[1] > 30) & (p[0] > 150)),
                   ("green", lambda p: (p[1] - p[0] > 30) & (p[1] - p[2] > 30) & (p[1] > 100))]:
        sel = pr(z9.T).T
        if sel.sum() > 3:
            print(f"cells {rn} {nm}:", tuple(int(v) for v in np.median(z9[sel], axis=0)), "n=", int(sel.sum()))

print("\n=== E. CANVAS BORDER SAMPLES ===")
for pt in [(300, 117), (300, 118), (300, 119), (300, 120), (300, 470), (300, 471), (92, 300), (93, 300), (769, 300), (770, 300), (768, 300)]:
    print(pt, med(pt[0], pt[1], pt[0] + 2, pt[1] + 2))

print("\n=== F. '=' and strips: fill colors (clean samples) ===")
print("strip1 band fill (fx 246..256):", med(246, 364, 256, 376))
print("y1 fill s1 (avoid text, top strip of cell):", med(259, 360, 265, 363))
print("y2 fill s2:", med(421, 360, 427, 363), " y2..y4 fills s1:", med(295, 360, 301, 363))
print("s1 last-cell fill:", med(367, 360, 373, 363), " s3 cells fill:", med(584, 360, 590, 363), med(693, 360, 699, 363))
