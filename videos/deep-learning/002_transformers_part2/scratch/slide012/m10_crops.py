#!/usr/bin/env python3
# m10_crops.py — settle: strip structure, result symbols, headers, embedding circles,
# cell boxes per panel, canvas border, subtitle W_q color
from PIL import Image
import numpy as np

im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_012.jpg').convert('RGB')
a = np.asarray(im).astype(int)
H, W = a.shape[:2]
r, g, b = a[..., 0], a[..., 1], a[..., 2]
lum = (r + g + b) / 3

def med(x0, y0, x1, y1):
    return tuple(int(v) for v in np.median(a[y0:y1, x0:x1].reshape(-1, 3), axis=0))

def spans(mask1d, base=0, minlen=2):
    out, s = [], None
    for i, v in enumerate(mask1d):
        if v and s is None: s = i
        if not v and s is not None:
            if i - s >= minlen: out.append((base + s, base + i - 1))
            s = None
    if s is not None: out.append((base + s, base + len(mask1d) - 1))
    return out

def classify(px):
    rr, gg, bb = int(px[0]), int(px[1]), int(px[2])
    if rr > 235 and gg > 225 and 150 < bb < 240 and rr - bb > 10: return 'y'   # cream cell
    if gg - rr > 18 and gg - bb > 10: return 'G'                                # green
    if rr - gg > 22 and gg - bb > 8 and rr > 225: return 'O'                    # orange
    if bb - gg > 18 and bb - rr > 18: return 'L'                                # lavender
    if rr > 140 and gg < 110 and bb < 110: return 'R'                           # red ink
    if bb - rr > 30 and bb > 110: return 'B'                                    # blue ink
    if rr - gg > 30 and bb - gg > 30: return 'M'                                # magenta
    if lum_at(rr, gg, bb) < 200: return 'k'                                     # dark ink
    return '.'

def lum_at(rr, gg, bb):
    return (rr + gg + bb) / 3

print("=== A. STRIP-1 structure: ASCII fy 352..390, fx 245..400 ===")
for yy in range(352, 392, 1):
    row = "".join(classify(a[yy, x]) for x in range(245, 400, 1))
    print(f"fy {yy:3d} {row}")
print("strip1 modal colors: y1cell", med(258, 362, 285, 378), " y2cell", med(294, 362, 315, 378),
      " gapbetween", med(287, 366, 292, 372))

print("\n=== B. RESULT SYMBOL ZONE: ASCII fy 415..450, fx 305..345 + colors ===")
for yy in range(415, 452, 1):
    row = "".join(classify(a[yy, x]) for x in range(305, 348, 1))
    print(f"fy {yy:3d} {row}")
# any-ink bbox + modal
ink = lum < 215
m = ink[412:455, 240:740]
ys, xs = np.where(m)
print("res zone any-ink: fx", xs.min() + 240, "..", xs.max() + 240, " fy", ys.min() + 412, "..", ys.max() + 412)
zpix = a[412:455, 240:740][m]
dark = zpix[zpix.sum(axis=1) < 380]
print("res glyph core:", tuple(int(v) for v in np.median(dark, axis=0)) if len(dark) else None, "n=", len(dark))

print("\n=== C. HEADERS ASCII (fy 134..162) ===")
for (x0, x1, nm) in [(240, 360, "H1"), (444, 524, "H2"), (606, 730, "H3")]:
    print(f"--- {nm} header ---")
    for yy in range(134, 163, 1):
        row = "".join("#" if lum[yy, x] < 190 else "." for x in range(x0, x1, 1))
        if "#" in row:
            print(f"fy {yy:3d} {row}")

print("\n=== D. CELL BOXES: rim scan per panel ===")
# cell rims olive (138,120,83)-ish
rim = (np.abs(r - 138) < 45) & (np.abs(g - 120) < 45) & (np.abs(b - 83) < 45) & (r - b > 25)
for nm, (x0, x1) in [("H1", (243, 400)), ("H2", (403, 568)), ("H3", (565, 730))]:
    m = rim[165:330, x0:x1]
    colc = m.sum(axis=0); rowc = m.sum(axis=1)
    print(f"{nm} rim col bands:", spans(colc > 12, x0, 3))
    print(f"{nm} rim row bands:", spans(rowc > 12, 165, 3))
# per-cell rim bbox for H1 (row1): columns where rim pixels exist in fy 174..196
m = rim[174:196, 243:400]
colc = m.sum(axis=0)
print("H1 r1 rim col bands:", spans(colc > 2, 243, 2))

print("\n=== E. EMBEDDING BOX ASCII (fy 148..200, fx 95..255) ===")
for yy in range(148, 202, 1):
    row = "".join(classify(a[yy, x]) for x in range(95, 255, 1))
    print(f"fy {yy:3d} {row}")

print("\n=== F. SUBTITLE W_q red? (fy 78..98, exclude badge fx>845) ===")
subred = (r - b > 45) & (r > 130) & (r < 220)
m = subred[78:100, 62:845]
ys, xs = np.where(m)
if len(ys) > 2:
    print("subtitle red: fx", xs.min() + 62, "..", xs.max() + 62, " fy", ys.min() + 78, "..", ys.max() + 78, " n=", len(ys))
    for yy in range(78, 100):
        seg = np.where(m[yy - 78, :])[0]
        if len(seg) > 1:
            print(f"  fy {yy}: fx {seg.min()+62}..{seg.max()+62} n={len(seg)}")
    zc = a[78:100, 62:845][m]
    print("subtitle red core:", tuple(int(v) for v in np.median(zc, axis=0)))
# subtitle blue core excluding badge
subblue = (b - r > 30) & (b > 110)
m = subblue[80:98, 62:845]
zpix = a[80:98, 62:845][m]
core = zpix[zpix.sum(axis=1) < 420]
print("subtitle blue core:", tuple(int(v) for v in np.median(core, axis=0)) if len(core) else None, "n=", len(core))

print("\n=== G. CANVAS BORDER ===")
# light border of white rounded canvas
for yy in [117, 118, 119, 120, 121]:
    seg = np.where(lum[yy, 60:900] < 235)[0] + 60
    if len(seg) > 3:
        print(f"canvas top fy {yy}: fx {seg.min()}..{seg.max()} n={len(seg)}")
for yy in [468, 469, 470, 471, 472, 473]:
    seg = np.where(lum[yy, 60:900] < 235)[0] + 60
    if len(seg) > 3:
        print(f"canvas bottom fy {yy}: fx {seg.min()}..{seg.max()} n={len(seg)}")
for xx in [89, 90, 91, 92, 769, 770, 771, 772]:
    seg = np.where(lum[115:475, xx] < 235)[0] + 115
    if len(seg) > 3:
        print(f"canvas side fx {xx}: fy {seg.min()}..{seg.max()} n={len(seg)}")

print("\n=== H. X_2 label (blue) in 'Current Word X_2' line ===")
subblue2 = (b - r > 30) & (b > 110)
m = subblue2[138:158, 62:300]
ys, xs = np.where(m)
if len(ys) > 2:
    print("X_2 blue: fx", xs.min() + 62, "..", xs.max() + 62, " fy", ys.min() + 138, "..", ys.max() + 138, " n=", len(ys))

print("\n=== I. mapped slide coords of key targets (certified mapping) ===")
f2s = lambda fx: (fx - 17.628) / 0.961232
f2sy = lambda fy: fy / 0.955556
pts = [("canvasTL", 91, 119), ("canvasBR", 770, 472), ("H1tl", 246, 157), ("H1br", 391, 359),
       ("H2tl", 413, 157), ("H2br", 557, 359), ("H3tl", 572, 157), ("H3br", 717, 359),
       ("s1l", 247, 358), ("s1r", 391, 383), ("s2l", 408, 358), ("s2r", 563, 383),
       ("s3l", 570, 358), ("s3r", 725, 383), ("brace1t", 396, 152), ("brace1b", 400, 340),
       ("res1", 305, 415), ("res3r", 345, 450), ("eq", 204, 368), ("badge", 875.5, 71)]
for nm, fx, fy in pts:
    print(f"{nm}: frame ({fx},{fy}) -> slide ({f2s(fx):.1f},{f2sy(fy):.1f})")
