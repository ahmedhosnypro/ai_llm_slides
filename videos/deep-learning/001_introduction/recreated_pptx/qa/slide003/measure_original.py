#!/usr/bin/env python3
"""PIL measurement of the ground-truth frame slide_003.jpg (960x540, 1px=1pt).
Slide 003 = section title "[1] Revision of / Machine Learning".
Measures: canvas/panel/background colors, red border, black bottom bar,
title ink bands (per line bbox, cap height, left/right extents), title color,
mouse cursor presence. Prints numbers used by the build."""
import numpy as np
from PIL import Image

IM = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_003.jpg"
im = np.asarray(Image.open(IM).convert("RGB")).astype(int)
H, W = im.shape[:2]
print(f"frame {W}x{H}")
r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]


def modal(patch, label):
    px = np.asarray(patch).reshape(-1, 3)
    if len(px) == 0:
        print(f"{label}: EMPTY")
        return None
    vals, counts = np.unique(px, axis=0, return_counts=True)
    top = vals[np.argsort(-counts)[:3]]
    cnt = np.sort(counts)[::-1][:3]
    print(f"{label}: modal {['#%02X%02X%02X (%d)' % (t[0], t[1], t[2], c) for t, c in zip(top, cnt)]}")
    return top[0]


# --- overall background samples ---
modal(im[5:40, 5:40], "outer corner TL (canvas)")
modal(im[200:260, 60:100], "inside panel left band")
modal(im[300:400, 400:560], "inside panel center (below title)")

# --- panel extent: gray E9E9E7 ---
gray = (abs(r - 233) < 16) & (abs(g - 233) < 16) & (abs(b - 231) < 18)
cols = np.where(gray[100:500].sum(axis=0) > 200)[0]
rows = np.where(gray[:, 60:160].sum(axis=1) > 50)[0]
print(f"panel gray cols {cols.min()}..{cols.max()}" if len(cols) else "no gray cols")
print(f"panel gray rows {rows.min()}..{rows.max()}" if len(rows) else "no gray rows")

# --- red border strokes (C00000-ish) ---
red = (r > 120) & (g < 110) & (b < 110)
print("red px total:", int(red.sum()))
for name, sl in [("top", np.s_[0:80, 400:560]), ("left", np.s_[200:400, 0:80]),
                 ("right", np.s_[200:400, 880:960]), ("bottom", np.s_[480:540, 400:560])]:
    ys, xs = np.where(red[sl])
    if len(ys):
        print(f"red {name}: rows {ys.min()+sl[0].start}..{ys.max()+sl[0].start} cols {xs.min()+sl[1].start}..{xs.max()+sl[1].start} n={len(ys)}")
    else:
        print(f"red {name}: none in {sl}")

# full-frame red col/row profile (frame strokes)
red_cols = np.where(red.sum(axis=0) > 100)[0]
red_rows = np.where(red.sum(axis=1) > 100)[0]
print("red heavy cols:", red_cols.tolist())
print("red heavy rows:", red_rows.tolist())

# --- black bottom bar ---
black = (r < 60) & (g < 60) & (b < 60)
black_rows = np.where(black.sum(axis=1) > 300)[0]
print("black heavy rows (bar):", black_rows.tolist())
if len(black_rows):
    bar = black_rows.min()
    bx = np.where(black[bar])[0]
    print(f"bar row {bar}: cols {bx.min()}..{bx.max()}")

# --- title ink: red text inside panel ---
# red text mask = red-ish but located inside panel (x 60..900, y 60..500)
text_red = red.copy()
text_red[:60, :] = False
text_red[:, :60] = False
text_red[:, 900:] = False
text_red[500:, :] = False
# exclude the border strokes: border cols/rows are thin vertical/horizontal lines
if len(red_cols):
    for c in red_cols:
        text_red[:, max(0, c - 3): c + 4] = False
if len(red_rows):
    for rr in red_rows:
        text_red[max(0, rr - 3): rr + 4, :] = False
trows = np.where(text_red.sum(axis=1) > 3)[0]
print("title ink rows:", (trows.min(), trows.max()) if len(trows) else "none")
# split into line bands (gap > 8 px)
bands = []
if len(trows):
    s = p = trows[0]
    for i in trows[1:]:
        if i <= p + 8:
            p = i
        else:
            bands.append((s, p))
            s = p = i
    bands.append((s, p))
print(f"title line bands: {bands}")
for bi, (y0, y1) in enumerate(bands):
    bx = np.where(text_red[y0:y1 + 1].sum(axis=0) > 0)[0]
    modal(im[y0:y1 + 1][text_red[y0:y1 + 1]], f"line{bi+1} ink color")
    # cap height via column extent at the band's core rows
    print(f"line{bi+1}: rows {y0}..{y1} (h={y1-y0+1}) cols {bx.min()}..{bx.max()} (w={bx.max()-bx.min()+1}) center_x={(bx.min()+bx.max())/2:.1f}")

# --- row profile of title ink (per-row pixel counts, to find cap-top vs x-height vs baseline) ---
if len(trows):
    prof = text_red.sum(axis=1)
    for y in range(trows.min(), trows.max() + 1):
        if prof[y] > 0:
            pass
    # print coarse profile every row for band 1 and 2
    for bi, (y0, y1) in enumerate(bands):
        seg = [f"{y}:{int(prof[y])}" for y in range(y0, y1 + 1)]
        print(f"line{bi+1} rowprofile: {' '.join(seg)}")

# --- mouse cursor: black+white small shape in lower-center ---
cur = black.copy()
cur[:350, :] = False
cur[520:, :] = False  # exclude bar
crows = np.where(cur.sum(axis=1) > 2)[0]
if len(crows):
    cy0, cy1 = crows.min(), crows.max()
    cx = np.where(cur[cy0:cy1 + 1].sum(axis=0) > 0)[0]
    print(f"cursor-like dark ink rows {cy0}..{cy1} cols {cx.min()}..{cx.max()} n={int(cur.sum())}")
else:
    print("no cursor-like dark ink found below y=350")
