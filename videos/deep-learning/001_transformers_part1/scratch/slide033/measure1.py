#!/usr/bin/env python3
"""PIL forensics on slide_033.jpg (960x540, 1px = 1pt).

Color-cluster scans for the major diagram shapes + text-ink band maps.
Everything prints px coords in the 960x540 frame.
"""
import sys
import numpy as np
from PIL import Image

IM = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_033.jpg').convert('RGB')
A = np.asarray(IM).astype(int)
H, W = A.shape[:2]
print(f"frame {W}x{H}")

def bbox_of(mask, label):
    ys, xs = np.nonzero(mask)
    if len(xs) == 0:
        print(f"{label}: EMPTY")
        return None
    print(f"{label}: x {xs.min()}..{xs.max()}  y {ys.min()}..{ys.max()}  n={len(xs)}")
    return (xs.min(), xs.max(), ys.min(), ys.max())

def colmask(target, tol):
    t = np.array(target)
    d = np.abs(A - t).sum(axis=2)
    return d <= tol

def runs_in_col(x, mask, minlen=3):
    col = mask[:, x]
    out = []
    y = 0
    while y < H:
        if col[y]:
            y0 = y
            while y < H and col[y]:
                y += 1
            if y - y0 >= minlen:
                out.append((y0, y - 1))
        else:
            y += 1
    return out

def runs_in_row(y, mask, minlen=3):
    row = mask[y]
    out = []
    x = 0
    while x < W:
        if row[x]:
            x0 = x
            while x < W and row[x]:
                x += 1
            if x - x0 >= minlen:
                out.append((x0, x - 1))
        else:
            x += 1
    return out

def region_profile(x0, x1, y0, y1, label, step=4):
    """Count colors inside a region to identify dominant fills."""
    sub = A[y0:y1 + 1, x0:x1 + 1].reshape(-1, 3)
    from collections import Counter
    cnt = Counter(map(tuple, (sub // 16 * 16)))
    top = cnt.most_common(6)
    tops = ", ".join(f"{c}x{v}" for c, v in top)
    print(f"{label} [{x0}..{x1} x {y0}..{y1}] top-16 buckets: {tops}")

if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "all"

    if which in ("all", "panel"):
        print("== PANEL (peach FCE4C6 fill, maroon 7A0000 border) ==")
        peach = colmask((252, 228, 198), 45)
        bbox_of(peach, "peach fill")
        maroon = colmask((122, 0, 0), 60)
        bbox_of(maroon, "maroon border ink")
        # panel border edges: strong horizontal maroon runs
        for y in range(80, 130):
            r = runs_in_row(y, maroon, 30)
            if r:
                print(f"maroon row y={y}: {r}")
                break
        for y in range(539, 490, -1):
            r = runs_in_row(y, maroon, 30)
            if r:
                print(f"maroon row y={y}: {r}")
                break
        for x in range(20, 80):
            c = runs_in_col(x, maroon, 20)
            if c:
                print(f"maroon col x={x}: {c[0]}..{c[-1]} (nruns={len(c)})")
                break
        for x in range(959, 900, -1):
            c = runs_in_col(x, maroon, 20)
            if c:
                print(f"maroon col x={x}: {c[0]}..{c[-1]} (nruns={len(c)})")
                break

    if which in ("all", "green"):
        print("== GREEN dashed containers (00A651) ==")
        green = colmask((0, 166, 81), 90)
        bbox_of(green, "green ink all")
        # left container: scan vertical green runs in x 40..160
        for x in (50, 55, 60, 100, 140, 150, 155, 160):
            print(f"  green col x={x}: {runs_in_col(x, green, 2)[:8]}")
        for y in (200, 220, 250, 300, 350, 390, 400):
            print(f"  green row y={y}: {runs_in_row(y, green, 2)[:10]}")

    if which in ("all", "yellow"):
        print("== YELLOW boxes (FFFF00 fill, CC7A00 border) ==")
        yel = colmask((255, 255, 0), 60)
        bbox_of(yel, "yellow all")
        for y in (220, 250, 280, 310, 340, 370, 400, 430, 460):
            print(f"  yellow row y={y}: {runs_in_row(y, yel, 4)[:12]}")

    if which in ("all", "taupe"):
        print("== TAUPE Dot Product box (B3AAA4) ==")
        tp = colmask((179, 170, 164), 40)
        bbox_of(tp, "taupe fill")

    if which in ("all", "orchid"):
        print("== ORCHID Soft max bar (E7C1E7) ==")
        orh = colmask((231, 193, 231), 45)
        bbox_of(orh, "orchid fill")

    if which in ("all", "blue"):
        print("== BLUE Sigma box (CCE4F7 fill / 003366 border+glyph) ==")
        lb = colmask((204, 228, 247), 40)
        bbox_of(lb, "light blue fill")
        db = colmask((0, 51, 102), 60)
        bbox_of(db, "dark blue ink")

    if which in ("all", "red"):
        print("== RED ink (CC0000 / 8B0000) ==")
        r1 = colmask((204, 0, 0), 70)
        r2 = colmask((139, 0, 0), 60)
        bbox_of(r1, "bright red CC0000")
        bbox_of(r2, "dark red 8B0000")

    if which in ("all", "magenta"):
        print("== MAGENTA X2 highlight (FF00FF) ==")
        mg = colmask((255, 0, 255), 80)
        bbox_of(mg, "magenta")

    if which in ("all", "pills"):
        print("== YELLOW pills (FFFFCC) ==")
        pl = colmask((255, 255, 204), 25)
        bbox_of(pl, "pill fill")

    if which in ("all", "rows"):
        print("== per-color row bands (count per row) for layout sanity ==")
        for name, tgt, tol in [("peach", (252, 228, 198), 45),
                               ("green", (0, 166, 81), 90),
                               ("yellow", (255, 255, 0), 60),
                               ("taupe", (179, 170, 164), 40),
                               ("orchid", (231, 193, 231), 45)]:
            m = colmask(tgt, tol)
            counts = m.sum(axis=1)
            bands = []
            inb = False
            for y in range(H):
                if counts[y] > 3 and not inb:
                    y0 = y; inb = True
                elif counts[y] <= 3 and inb:
                    if y - y0 > 2:
                        bands.append((y0, y - 1))
                    inb = False
            if inb:
                bands.append((y0, H - 1))
            print(f"  {name} row bands: {bands}")
