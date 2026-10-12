#!/usr/bin/env python3
"""Pass 4b: exact edges (fixed axes) + cursor map."""
import numpy as np
from PIL import Image

im = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_030.jpg").convert("RGB")
a = np.asarray(im).astype(int)
H, W = a.shape[:2]
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]
lum = 0.299 * R + 0.587 * G + 0.114 * B
red = (R > 130) & (G < 90) & (B < 90)
black = (R < 90) & (G < 90) & (B < 90)
whitep = (R > 240) & (G > 240) & (B > 240)

def colspan(y, lo, hi, lbl):
    idx = np.where(red[y, lo:hi])[0]
    print(f"  {lbl} (row y={y}):", f"x {lo+idx.min()}..{lo+idx.max()} n={len(idx)}" if len(idx) else "none")

def rowspan(x, lo, hi, lbl):
    idx = np.where(red[lo:hi, x])[0]
    print(f"  {lbl} (col x={x}):", f"y {lo+idx.min()}..{lo+idx.max()} n={len(idx)}" if len(idx) else "none")

print("=== LEFT PANEL exact edges ===")
rowspan(300, 225, 245, "top border @x300")
rowspan(300, 468, 485, "bottom border @x300")
colspan(350, 78, 95, "left border @y350")
colspan(350, 470, 488, "right border @y350")
print("  top thickness @x300:", [int(y) for y in range(228, 245) if red[y, 300]])
print("  bottom thickness @x300:", [int(y) for y in range(470, 484) if red[y, 300]])
print("  left thickness @y350:", [int(x) for x in range(80, 94) if red[350, x]])
print("  right thickness @y350:", [int(x) for x in range(472, 486) if red[350, x]])
# full horizontal extent of top and bottom borders
for y in [234, 235, 236, 475, 476, 477]:
    idx = np.where(red[y, 70:490])[0]
    if len(idx): print(f"  border row y={y}: x {70+idx.min()}..{70+idx.max()} n={len(idx)}")
# full vertical extent of left and right borders
for x in [84, 85, 86, 477, 478, 479, 480]:
    idx = np.where(red[220:490, x])[0]
    if len(idx): print(f"  border col x={x}: y {220+idx.min()}..{220+idx.max()} n={len(idx)}")

print("\n=== RIGHT PANEL exact edges ===")
rowspan(700, 262, 282, "top border @x700")
rowspan(700, 436, 452, "bottom border @x700")
colspan(350, 535, 550, "left border @y350")
colspan(350, 878, 894, "right border @y350")
print("  top thickness @x700:", [int(y) for y in range(262, 282) if red[y, 700]])
print("  bottom thickness @x700:", [int(y) for y in range(436, 452) if red[y, 700]])
print("  left thickness @y350:", [int(x) for x in range(535, 550) if red[350, x]])
print("  right thickness @y350:", [int(x) for x in range(878, 894) if red[350, x]])
for y in [268, 269, 270, 271, 272, 443, 444, 445]:
    idx = np.where(red[y, 500:900])[0]
    if len(idx): print(f"  border row y={y}: x {500+idx.min()}..{500+idx.max()} n={len(idx)}")
for x in [477, 478, 479, 480, 883, 884, 885, 886]:
    idx = np.where(red[255:490, x])[0]
    if len(idx): print(f"  border col x={x}: y {255+idx.min()}..{255+idx.max()} n={len(idx)}")

print("\n=== RIGHT IMAGE bbox (lum<140 in panel interior) ===")
d = (lum < 140)
d[:278, :] = False; d[435:, :] = False; d[:, :540] = False; d[:, 882:] = False
rows = d.sum(axis=1); cols = d.sum(axis=0)
rr = np.where(rows > 30)[0]; cc = np.where(cols > 30)[0]
print(f"  dense bbox: x[{cc.min()}..{cc.max()}] y[{rr.min()}..{rr.max()}]")

print("\n=== LEFT PHOTO bbox (non-white non-red in panel interior) ===")
nw = (R < 232) | (G < 232) | (B < 232)
ph = nw & ~red
ph[:282, :] = False; ph[473:, :] = False; ph[:, :88] = False; ph[:, 476:] = False
rows = ph.sum(axis=1); cols = ph.sum(axis=0)
rr = np.where(rows > 8)[0]; cc = np.where(cols > 8)[0]
print(f"  dense bbox: x[{cc.min()}..{cc.max()}] y[{rr.min()}..{rr.max()}]")

print("\n=== CAPTION strict black bbox (y230..285) ===")
cap = black & (np.arange(H)[:, None] >= 230) & (np.arange(H)[:, None] <= 285)
cap[:, :85] = False; cap[:, 476:] = False
ys, xs = np.where(cap)
print(f"  bbox x[{xs.min()}..{xs.max()}] y[{ys.min()}..{ys.max()}] px={len(xs)}")

print("\n=== TITLE bbox + cap height ===")
t = red.copy(); t[130:, :] = False
ys, xs = np.where(t)
print(f"  title bbox x[{xs.min()}..{xs.max()}] y[{ys.min()}..{ys.max()}]")
sub = t[:, 117:141]
rr = np.where(sub.sum(axis=1) > 0)[0]
print(f"  'A' rows y[{rr.min()}..{rr.max()}] cap height {rr.max()-rr.min()+1}px")

print("\n=== BADGE AREA (x872..918, y50..92) every 6px ===")
for y in range(50, 94, 6):
    out = [f"#{R[y,x]:02X}{G[y,x]:02X}{B[y,x]:02X}" for x in range(872, 918, 6)]
    print(f"  y={y}: " + " ".join(out))

print("\n=== DOT near (910,45) ===")
for y in range(35, 56, 3):
    out = [f"#{R[y,x]:02X}{G[y,x]:02X}{B[y,x]:02X}" for x in range(900, 930, 4)]
    print(f"  y={y}: " + " ".join(out))

print("\n=== CURSOR fine map (x340..430, y392..458) ===")
for y in range(392, 458, 2):
    row = ""
    for x in range(340, 430):
        if red[y, x]: row += "R"
        elif black[y, x]: row += "K"
        elif whitep[y, x]: row += "w"
        else: row += "."
    print(f"{y:4d} {row}")
