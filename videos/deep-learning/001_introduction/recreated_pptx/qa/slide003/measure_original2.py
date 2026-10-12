#!/usr/bin/env python3
"""Measurement pass 2 for slide_003.jpg: clean title bands (no bad exclusions),
border strokes located properly, cursor region scan, ASCII map of red ink."""
import numpy as np
from PIL import Image

IM = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_003.jpg"
im = np.asarray(Image.open(IM).convert("RGB")).astype(int)
H, W = im.shape[:2]
r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]

red = (r > 120) & (g < 110) & (b < 110)
black = (r < 60) & (g < 60) & (b < 60)

# --- border strokes: scan thin vertical lines away from title ---
# left: cols where red count in rows 350..500 (below title, above bar) is high
strip = red[350:500, :]
lcols = np.where(strip.sum(axis=0) > 100)[0]
print("left border cols (rows350-500):", lcols.tolist())
rcols = np.where(red[:, 880:960].sum(axis=0) > 50)[0] + 880
print("right border cols (full-height x880-960):", rcols.tolist())
trows_ = np.where(red[:, 300:700].sum(axis=1) > 200)[0]
print("horizontal red rows (x300-700):", trows_.tolist())
# top border: rows 30..70 red-ish (maybe lighter) at x 300..700
for y in range(35, 70):
    seg = im[y, 300:700]
    redish = ((seg[:, 0] > 120) & (seg[:, 1] < 110) & (seg[:, 2] < 110)).sum()
    if redish > 100:
        print(f"top border candidate row {y}: {redish} red px")

# --- title ink: red inside panel interior, excluding border cols/rows found above ---
text_red = red.copy()
for c in lcols:
    text_red[:, max(0, c - 2): c + 3] = False
text_red[:, 880:] = False
# exclude any long horizontal border rows (>400 px wide runs)
hrows = np.where(red[:, 100:860].sum(axis=1) > 500)[0]
for y in hrows:
    text_red[max(0, y - 2): y + 3, :] = False
trows = np.where(text_red.sum(axis=1) > 2)[0]
bands = []
if len(trows):
    s = p = trows[0]
    for i in trows[1:]:
        if i <= p + 6:
            p = i
        else:
            bands.append((s, p))
            s = p = i
    bands.append((s, p))
print(f"\ntitle bands: {bands}")
prof = text_red.sum(axis=1)
for bi, (y0, y1) in enumerate(bands):
    bxs = np.where(text_red[y0:y1 + 1].sum(axis=0) > 0)[0]
    ink = im[y0:y1 + 1][text_red[y0:y1 + 1]]
    vals, counts = np.unique(ink.reshape(-1, 3), axis=0, return_counts=True)
    top3 = vals[np.argsort(-counts)[:3]]
    print(f"band{bi+1}: rows {y0}..{y1} (h={y1-y0+1}) cols {bxs.min()}..{bxs.max()} (w={bxs.max()-bxs.min()+1}) cx={(bxs.min()+bxs.max())/2:.1f} modal={['#%02X%02X%02X(%d)' % (t[0],t[1],t[2],c) for t,c in zip(top3, np.sort(counts)[::-1][:3])]}")
    print(f"   profile: {' '.join(f'{y}:{int(prof[y])}' for y in range(y0, y1+1))}")

# --- ASCII map of red ink (4px cell) rows 140..360 ---
print("\nASCII map (rows 140-360, cols 150-820, cell 6x6, '#'=red>2):")
for y in range(140, 362, 6):
    line = ""
    for x in range(150, 820, 6):
        cell = red[y:y+6, x:x+6].sum()
        line += "#" if cell > 2 else "."
    print(f"{y:3d} {line}")

# --- cursor region scan: non-background in lower area ---
bg = np.array([233, 233, 231])
region = im[340:517, 60:900]
diff = np.abs(region - bg).sum(axis=2)
nb = diff > 90
ys, xs = np.where(nb)
if len(ys):
    print(f"\nnon-bg ink rows 340-517: {ys.min()+340}..{ys.max()+340}, cols {xs.min()+60}..{xs.max()+60}, n={len(ys)}")
    # cluster coarse
    rowsum = nb.sum(axis=1)
    rr = np.where(rowsum > 2)[0]
    if len(rr):
        print("ink rows:", rr.min()+340, "..", rr.max()+340)
        cs = np.where(nb[rr.min():rr.max()+1].sum(axis=0) > 0)[0]
        print("ink cols:", cs.min()+60, "..", cs.max()+60)
else:
    print("\nno non-bg ink in lower region besides bar")

# --- top edge: exact panel top border color sample rows 40..50 ---
for y in range(40, 52):
    print(f"row {y}: modal x300-700:", end=" ")
    seg = im[y, 300:700].reshape(-1, 3)
    vals, counts = np.unique(seg, axis=0, return_counts=True)
    t = vals[np.argmax(counts)]
    print(f"#{t[0]:02X}{t[1]:02X}{t[2]:02X} ({counts.max()})")
