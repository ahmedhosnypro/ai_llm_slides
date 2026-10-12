#!/usr/bin/env python3
"""Pass 4: exact edges + cursor hunt + badge dot check."""
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

def edge_scan(mask, axis, fixed, lo, hi, lbl):
    """first/last True along axis"""
    if axis == "y":
        v = mask[lo:hi, fixed]
        idx = np.where(v)[0]
        print(f"{lbl} (col x={fixed}, y {lo}..{hi}):", f"first={lo+idx.min()} last={lo+idx.max()}" if len(idx) else "none")
    else:
        v = mask[fixed, lo:hi]
        idx = np.where(v)[0]
        print(f"{lbl} (row y={fixed}, x {lo}..{hi}):", f"first={lo+idx.min()} last={lo+idx.max()}" if len(idx) else "none")

print("=== LEFT PANEL exact edges ===")
edge_scan(red, "x", 300, 225, 245, "left panel top border @x300")
edge_scan(red, "x", 300, 468, 485, "left panel bottom border @x300")
edge_scan(red, "y", 350, 78, 95, "left panel left border @y350")
edge_scan(red, "y", 350, 470, 488, "left panel right border @y350")
# thickness: count red px in border cross-sections
print("  top border thickness @x300:", [int(y) for y in range(228, 245) if red[y, 300]])
print("  bottom border thickness @x300:", [int(y) for y in range(470, 484) if red[y, 300]])
print("  left border thickness @y350:", [int(x) for x in range(80, 94) if red[350, x]])
print("  right border thickness @y350:", [int(x) for x in range(472, 486) if red[350, x]])

print("\n=== RIGHT PANEL exact edges ===")
edge_scan(red, "x", 700, 262, 280, "right panel top border @x700")
edge_scan(red, "x", 700, 438, 452, "right panel bottom border @x700")
edge_scan(red, "y", 350, 532, 548, "right panel left border @y350")
edge_scan(red, "y", 350, 878, 892, "right panel right border @y350")
print("  top border thickness @x700:", [int(y) for y in range(262, 280) if red[y, 700]])
print("  bottom border thickness @x700:", [int(y) for y in range(438, 452) if red[y, 700]])
print("  left border thickness @y350:", [int(x) for x in range(532, 550) if red[350, x]])
print("  right border thickness @y350:", [int(x) for x in range(878, 892) if red[350, x]])
# horizontal extent of top/bottom borders
for y in [269, 270, 271, 272]:
    idx = np.where(red[y, 500:900])[0]
    if len(idx): print(f"  top border y={y}: x {500+idx.min()}..{500+idx.max()}")
for y in [443, 444, 445]:
    idx = np.where(red[y, 500:900])[0]
    if len(idx): print(f"  bottom border y={y}: x {500+idx.min()}..{500+idx.max()}")

print("\n=== RIGHT IMAGE exact bbox (lum<140 within panel) ===")
d = (lum < 140)
d[:276, :] = False; d[437:, :] = False; d[:, :545] = False; d[:, 880:] = False
ys, xs = np.where(d)
print(f"  bbox x[{xs.min()}..{xs.max()}] y[{ys.min()}..{ys.max()}] px={len(xs)}")
# per-edge first/last with threshold on density
rows = d.sum(axis=1); cols = d.sum(axis=0)
rr = np.where(rows > 30)[0]; cc = np.where(cols > 30)[0]
print(f"  dense bbox: x[{cc.min()}..{cc.max()}] y[{rr.min()}..{rr.max()}]")

print("\n=== LEFT PHOTO exact bbox (non-white non-red in panel interior) ===")
nw = (R < 232) | (G < 232) | (B < 232)
ph = nw & ~red
ph[:282, :] = False; ph[472:, :] = False; ph[:, :88] = False; ph[:, 476:] = False
rows = ph.sum(axis=1); cols = ph.sum(axis=0)
rr = np.where(rows > 8)[0]; cc = np.where(cols > 8)[0]
print(f"  dense bbox: x[{cc.min()}..{cc.max()}] y[{rr.min()}..{rr.max()}]")

print("\n=== CAPTION (strict black, y230..285, x85..475) ===")
cap = black & (np.arange(H)[:, None] >= 230) & (np.arange(H)[:, None] <= 285)
cap[:, :85] = False; cap[:, 476:] = False
ys, xs = np.where(cap)
print(f"  caption ink bbox x[{xs.min()}..{xs.max()}] y[{ys.min()}..{ys.max()}] px={len(xs)}")
rows = cap.sum(axis=1)
print("  row profile:", [(int(y), int(rows[y])) for y in range(ys.min(), ys.max()+1, 3)])

print("\n=== ARROW fine map (x478..545, y330..380) ===")
for y in range(330, 380, 2):
    row = ""
    for x in range(478, 546):
        if red[y, x]: row += "R"
        elif black[y, x]: row += "K"
        elif whitep[y, x]: row += "w"
        else: row += "."
    print(f"{y:4d} {row}")

print("\n=== TITLE cap-height ('A' col x117..140) + full bbox ===")
t = red.copy(); t[130:, :] = False
ys, xs = np.where(t)
print(f"  title bbox x[{xs.min()}..{xs.max()}] y[{ys.min()}..{ys.max()}]")
sub = t[:, 117:141]
rr = np.where(sub.sum(axis=1) > 0)[0]
print(f"  'A' glyph rows y[{rr.min()}..{rr.max()}] -> cap height {rr.max()-rr.min()+1}px")

print("\n=== BADGE AREA colors (x875..915, y50..92) ===")
for y in range(50, 94, 6):
    out = []
    for x in range(872, 918, 6):
        out.append(f"({x},{y})#{R[y,x]:02X}{G[y,x]:02X}{B[y,x]:02X}")
    print("  " + " ".join(out))

print("\n=== mystery dot (x905..925, y35..55) ===")
for y in range(35, 56, 3):
    out = []
    for x in range(900, 930, 4):
        out.append(f"#{R[y,x]:02X}{G[y,x]:02X}{B[y,x]:02X}")
    print(f"  y={y}: " + " ".join(out))

print("\n=== CURSOR hunt fine map (x340..430, y392..458): R=red K=black w=white .=other ===")
for y in range(392, 458, 2):
    row = ""
    for x in range(340, 430):
        if red[y, x]: row += "R"
        elif black[y, x]: row += "K"
        elif whitep[y, x]: row += "w"
        else: row += "."
    print(f"{y:4d} {row}")
