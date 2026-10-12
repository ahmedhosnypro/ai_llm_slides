#!/usr/bin/env python3
"""Pass 5: settle matrix glyph columns, arrow shape, black bar, panel borders/fills."""
import numpy as np
from PIL import Image

im = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_030.jpg").convert("RGB")
a = np.asarray(im).astype(int)
H, W = a.shape[:2]
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]
lum = 0.299 * R + 0.587 * G + 0.114 * B
red = (R > 130) & (G < 90) & (B < 90)
black = (R < 90) & (G < 90) & (B < 90)

print("=== MATRIX 1px map (x135..405, y305..440), R=red ===")
for y in range(305, 441, 3):
    row = ""
    for x in range(135, 406):
        row += "R" if red[y, x] else "."
    print(f"{y:4d} {row}")

print("\n=== MATRIX column profile (red cols in x135..405, y310..435) ===")
sub = red[310:436, 135:406]
cols = sub.sum(axis=0)
runs = []
inr = False
for i, v in enumerate(cols):
    if v > 0 and not inr:
        s = i; inr = True
    elif v == 0 and inr:
        runs.append((135 + s, 135 + i - 1)); inr = False
if inr: runs.append((135 + s, 135 + len(cols) - 1))
print("  col runs:", runs)

print("\n=== ARROW 1px map (x470..545, y325..378), R=red ===")
for y in range(325, 379, 2):
    row = ""
    for x in range(470, 546):
        row += "R" if red[y, x] else "."
    print(f"{y:4d} {row}")

print("\n=== ARROW row extents (red runs x472..540, excluding border col x478/x534) ===")
for y in range(328, 376, 2):
    idx = np.where(red[y, 472:540])[0]
    if len(idx):
        print(f"  y={y}: x {472+idx.min()}..{472+idx.max()} n={len(idx)}")

print("\n=== BLACK BAR ===")
bb = black.copy(); bb[:500, :] = False
ys, xs = np.where(bb)
print(f"  bbox x[{xs.min()}..{xs.max()}] y[{ys.min()}..{ys.max()}] px={len(xs)}")
for y in [505, 508, 510, 512, 515, 525, 535, 539]:
    idx = np.where(black[y, :])[0]
    print(f"  y={y}: x {idx.min()}..{idx.max()} n={len(idx)}" if len(idx) else f"  y={y}: none")
print("  sample colors:", [f"#{R[525,x]:02X}{G[525,x]:02X}{B[525,x]:02X}" for x in [5, 100, 300, 500, 700, 900, 950]])
# top edge exact at x=480
col = np.where(black[:540, 480])[0]
print("  top edge @x480:", col.min() if len(col) else None)

print("\n=== RIGHT PANEL left border? (red in x528..542, y272..442) ===")
for y in range(272, 443, 20):
    idx = np.where(red[y, 528:543])[0]
    print(f"  y={y}:", f"x {528+idx.min()}..{528+idx.max()} n={len(idx)}" if len(idx) else "none")
# scan the exact left border column
colred = red[272:443, 528:543].sum(axis=0)
print("  red count per col x528..542:", {528 + i: int(v) for i, v in enumerate(colred) if v > 0})

print("\n=== RIGHT IMAGE precise bbox (lum<150 in x536..883, y272..443) ===")
d = (lum < 150)
d[:272, :] = False; d[443:, :] = False; d[:, :536] = False; d[:, 884:] = False
ys, xs = np.where(d)
print(f"  bbox x[{xs.min()}..{xs.max()}] y[{ys.min()}..{ys.max()}] px={len(xs)}")
print("  corner colors:", [f"#{R[y,x]:02X}{G[y,x]:02X}{B[y,x]:02X}" for (x, y) in [(550, 280), (870, 280), (550, 435), (870, 435), (712, 356)]])

print("\n=== LEFT PANEL fill + photo edges ===")
print("  panel interior (x460, y460):", f"#{R[460,460]:02X}{G[460,460]:02X}{B[460,460]:02X}")
print("  panel interior (x95, y250):", f"#{R[250,95]:02X}{G[250,95]:02X}{B[250,95]:02X}")
# photo top edge: scan column x=200 y270..300
for y in range(272, 292):
    print(f"  x200 y{y}: #{R[y,200]:02X}{G[y,200]:02X}{B[y,200]:02X}", end="  ")
    if y % 4 == 3: print()
print()
# photo bottom edge x=200 y448..470
for y in range(448, 470, 2):
    print(f"  x200 y{y}: #{R[y,200]:02X}{G[y,200]:02X}{B[y,200]:02X}")
# photo left/right edges at y=350
for x in list(range(86, 112, 2)) + list(range(436, 462, 2)):
    print(f"  y350 x{x}: #{R[350,x]:02X}{G[350,x]:02X}{B[350,x]:02X}", end="  ")
print()

print("\n=== GRAY PANEL edges ===")
grayish = (np.abs(R - 0xE7) < 16) & (np.abs(G - 0xE9) < 16) & (np.abs(B - 0xE6) < 16)
row45 = np.where(grayish[45, :])[0]
row50 = np.where(grayish[50, :])[0]
print(f"  y=45 gray x[{row45.min()}..{row45.max()}] n={len(row45)}" if len(row45) else "  y=45 none")
print(f"  y=50 gray x[{row50.min()}..{row50.max()}] n={len(row50)}" if len(row50) else "  y=50 none")
col100 = np.where(grayish[:, 100])[0]
col900 = np.where(grayish[:, 900])[0]
print(f"  x=100 gray y[{col100.min()}..{col100.max()}]" if len(col100) else "  x=100 none")
print(f"  x=900 gray y[{col900.min()}..{col900.max()}]" if len(col900) else "  x=900 none")
# white canvas margins
print("  x=20,y=300:", f"#{R[300,20]:02X}{G[300,20]:02X}{B[300,20]:02X}", " x=940,y=300:", f"#{R[300,940]:02X}{G[300,940]:02X}{B[300,940]:02X}")
print("  x=41,y=300:", f"#{R[300,41]:02X}{G[300,41]:02X}{B[300,41]:02X}", " x=919,y=300:", f"#{R[300,919]:02X}{G[300,919]:02X}{B[300,919]:02X}")

print("\n=== TITLE color core sample ===")
tt = red.copy(); tt[130:, :] = False
ys, xs = np.where(tt)
print(f"  title bbox x[{xs.min()}..{xs.max()}] y[{ys.min()}..{ys.max()}]")
samples = [(x, y) for y in range(85, 115, 6) for x in range(120, 860, 40) if red[y, x]]
print("  red glyph samples:", [f"({x},{y})#{R[y,x]:02X}{G[y,x]:02X}{B[y,x]:02X}" for (x, y) in samples[:12]])

print("\n=== CAPTION bbox + color ===")
cap = black.copy(); cap[:236, :] = False; cap[283:, :] = False; cap[:, :87] = False; cap[:, 477:] = False
ys, xs = np.where(cap)
print(f"  caption bbox x[{xs.min()}..{xs.max()}] y[{ys.min()}..{ys.max()}] px={len(xs)}")
rr = cap.sum(axis=1)
prof = [(y, int(rr[y])) for y in range(ys.min(), ys.max() + 1) if rr[y] > 0]
print("  row profile:", prof[:6], "...", prof[-6:])

print("\n=== CURSOR mask (for inpaint): black px x330..380, y388..434 ===")
cur = black.copy(); cur[:388, :] = False; cur[435:, :] = False; cur[:, :330] = False; cur[:, 381:] = False
ys, xs = np.where(cur)
print(f"  cursor bbox x[{xs.min()}..{xs.max()}] y[{ys.min()}..{ys.max()}] px={len(xs)}")
# row-1 '1' glyph patch source (for copy): red in x355..385, y310..345
g1 = red.copy(); g1[:308, :] = False; g1[346:, :] = False; g1[:, :355] = False; g1[:, 386:] = False
ys, xs = np.where(g1)
print(f"  row1-col3 '1' glyph bbox x[{xs.min()}..{xs.max()}] y[{ys.min()}..{ys.max()}] px={len(xs)}")
# row-3 '1' glyph remnants (red) in cursor zone
g3 = red.copy(); g3[:400, :] = False; g3[436:, :] = False; g3[:, :355] = False; g3[:, 386:] = False
ys, xs = np.where(g3)
print(f"  row3-col3 '1' glyph bbox x[{xs.min()}..{xs.max()}] y[{ys.min()}..{ys.max()}] px={len(xs)}")
