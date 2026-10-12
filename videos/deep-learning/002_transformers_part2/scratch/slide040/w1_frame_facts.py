from PIL import Image
import numpy as np
FR = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_040.jpg"
im = np.array(Image.open(FR).convert("RGB")).astype(int)
H, W = im.shape[:2]
print(f"frame {W}x{H}")

def core_color(x0, x1, y0, y1, sat_min=60):
    """sample saturated (colored) glyph pixels in box, return median + darkest median"""
    reg = im[y0:y1, x0:x1]
    r, g, b = reg[:,:,0], reg[:,:,1], reg[:,:,2]
    mx = reg.max(axis=2); mn = reg.min(axis=2)
    sat = mx - mn
    mask = sat > sat_min
    if mask.sum() == 0:
        return None, 0
    px = reg[mask]
    return np.median(px, axis=0), int(mask.sum())

print("\n== 1. intro gamma / beta glyph colors (frame) ==")
# intro line 2: "learn parameters γ and β that can ..." — γ/β after x~520 (frame)
# scan the colored glyph cores in x 500..640, rows 140..162
for label, x0, x1 in [("gamma-zone", 525, 555), ("and-zone", 555, 585), ("beta-zone", 583, 600)]:
    c, n = core_color(x0, x1, 140, 162)
    print(f"  {label} x{x0}..{x1}: median {c} n={n}")
# fine scan: per-column dominant hue in the glyph band
print("  per-column saturated medians x520..600:")
for x in range(520, 601, 4):
    c, n = core_color(x, x+4, 140, 162, sat_min=50)
    if n > 2:
        print(f"    x{x}: {c} (n={n})")

print("\n== 2. underline probes ==")
def row_ink(y, x0, x1, thr=200):
    row = im[y, x0:x1]
    dark = (row.mean(axis=1) < thr)
    idx = np.where(dark)[0]
    if len(idx) == 0: return 0, None, None
    return len(idx), x0+idx[0], x0+idx[-1]
print("  L2 red-run rows (y 155..172, x 500..880):")
for y in range(155, 173):
    n, a, b = row_ink(y, 500, 880)
    if n > 50:
        seg = im[y, a:b+1]
        print(f"    y={y}: n={n} x {a}..{b} median {np.median(seg.reshape(-1,3), axis=0)}")
print("  L3 rows (y 172..190, x 88..450):")
for y in range(172, 191):
    n, a, b = row_ink(y, 88, 450)
    if n > 80:
        seg = im[y, a:b+1]
        print(f"    y={y}: n={n} x {a}..{b} median {np.median(seg.reshape(-1,3), axis=0)}")

print("\n== 3. 'learn parameters' highlight vs underline (frame x 385..535, y 140..170) ==")
for y in range(140, 171, 2):
    n, a, b = row_ink(y, 380, 540, thr=235)
    if n > 20:
        seg = im[y, a:b+1]
        med = np.median(seg.reshape(-1,3), axis=0)
        print(f"    y={y}: n={n} x {a}..{b} median {med}")

print("\n== 4. eq3 region rectangle scan (frame x 150..320, rows 385..455) ==")
# long vertical runs per column
def col_runs(x, y0, y1, thr=215):
    col = im[y0:y1, x]
    nonbg = (col.mean(axis=1) < thr)
    # longest run
    best = 0; cur = 0; bs = None; s = None
    for i, v in enumerate(nonbg):
        if v:
            if cur == 0: s = i
            cur += 1
            if cur > best: best, bs = cur, s
        else:
            cur = 0
    return best, (y0+bs if bs is not None else None), (y0+bs+best if bs is not None else None)
print("  columns with vertical runs >= 20px:")
for x in range(150, 321):
    L, a, b = col_runs(x, 385, 455)
    if L >= 20:
        col_med = np.median(im[a:b, x], axis=0)
        print(f"    x={x}: run {L}px y {a}..{b} median {col_med}")
print("  rows with horizontal runs >= 80px:")
for y in range(385, 456):
    n, a, b = row_ink(y, 150, 320, thr=215)
    if n >= 80:
        print(f"    y={y}: n={n} x {a}..{b}")

print("\n== 5. eq4 region rectangle scan (frame x 150..600, rows 445..485) ==")
for x in range(150, 601):
    L, a, b = col_runs(x, 445, 486)
    if L >= 18:
        col_med = np.median(im[a:b, x], axis=0)
        print(f"    x={x}: run {L}px y {a}..{b} median {col_med}")
print("  rows with horizontal runs >= 150px:")
for y in range(445, 486):
    n, a, b = row_ink(y, 150, 600, thr=215)
    if n >= 150:
        seg = im[y, a:b+1]
        print(f"    y={y}: n={n} x {a}..{b} median {np.median(seg.reshape(-1,3), axis=0)}")

print("\n== 6. y_i ellipse fill (frame 170..191 x, 454..475 y) ==")
reg = im[456:474, 172:190]
dark = reg.mean(axis=2) < 150
nonbg = reg.mean(axis=2) < 240
interior = reg[~dark & nonbg]
print(f"  interior n={len(interior)} median {np.median(interior, axis=0)}")

print("\n== 7. blue words italic? full-word left-edge slant (L1) ==")
def word_slant(x0, x1, y0, y1, hue="blue"):
    tops, bots = [], []
    for x in range(x0, x1):
        col = im[y0:y1, x]
        r, g, b = col[:,0], col[:,1], col[:,2]
        if hue == "blue":
            m = (b > r + 40) & (b > 90) & (r < 150)
        else:
            m = (r > g + 40) & (r > 90) & (b < 100)
        idx = np.where(m)[0]
        if len(idx) > 0:
            tops.append(y0 + idx[0]); bots.append(y0 + idx[-1])
    if not tops: return None
    # left-edge drift: compare first-quarter vs last-quarter top edges
    q = max(1, len(tops)//4)
    lt = np.mean(tops[:q]); rt = np.mean(tops[-q:])
    return lt, rt, lt - rt
for label, x0, x1 in [("mean(L1 blue)", 634, 672), ("strictly(L1 blue)", 500, 560), ("variance,(L1 blue)", 790, 870)]:
    r = word_slant(x0, x1, 128, 152, "blue")
    print(f"  {label}: top-edge L vs R = {r}")

print("\n== 8. red runs italic? (L2 'convert' + L3 'Minimizes') ==")
for label, x0, x1 in [("convert(L2 red)", 676, 730), ("Minimizes(L3 red)", 320, 400), ("variance(L3 red)", 104, 170)]:
    r = word_slant(x0, x1, 155, 175, "red")
    print(f"  {label}: {r}")
