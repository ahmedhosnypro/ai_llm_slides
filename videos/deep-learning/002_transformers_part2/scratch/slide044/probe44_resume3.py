#!/usr/bin/env python3
# probe44_resume3.py — comprehensive cube geometry with tuned masks (frame = ground truth).
import numpy as np
from PIL import Image

F = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_044.jpg").convert("RGB")
a = np.asarray(F).astype(int)
R, G, B = a[:,:,0], a[:,:,1], a[:,:,2]

def near(c, tol):
    return (abs(R-c[0])<tol) & (abs(G-c[1])<tol) & (abs(B-c[2])<tol)

def bbox(m, x0, x1, y0, y1, name):
    ys, xs = np.where(m[y0:y1, x0:x1]); xs = xs + x0; ys = ys + y0
    if len(xs) == 0: print(f"{name}: EMPTY"); return None
    print(f"{name}: x {xs.min()}..{xs.max()}  y {ys.min()}..{ys.max()}  n={len(xs)}")
    return (xs.min(), xs.max(), ys.min(), ys.max())

SALMON = (216,78,52); MAG = (157,0,166)
m_sal = near(SALMON, 40); m_mag = near(MAG, 45)

print("== FRONT FACES ==")
bbox(m_sal, 40, 210, 200, 445, "LEFT front (salmon)")
bbox(m_mag, 260, 345, 165, 340, "GN front magenta part")
bbox(m_sal, 345, 420, 165, 340, "GN front salmon part")
bbox(m_mag, 445, 555, 185, 360, "IN front magenta part")
bbox(m_sal, 552, 590, 185, 360, "IN salmon column")
bbox(m_mag, 670, 830, 150, 340, "RT front magenta")

print("== GN front internal seams (bright rows/cols inside magenta) ==")
bright = (R>200) & (G>150) & (B>200)  # bright magenta/pink seams
for yy in range(180, 335):
    n = int(bright[yy, 280:332].sum())
    if n > 25: print(f"  bright row y{yy}: {n}")
for xx in range(277, 340):
    n = int(bright[200:330, xx].sum())
    if n > 25: print(f"  bright col x{xx}: {n}")

print("== IN front internal seams ==")
for yy in range(200, 355):
    n = int(bright[yy, 460:545].sum())
    if n > 25: print(f"  IN bright row y{yy}: {n}")
for xx in range(456, 550):
    n = int(bright[210:350, xx].sum())
    if n > 25: print(f"  IN bright col x{xx}: {n}")

print("== RT front internal seams ==")
for yy in range(168, 332):
    n = int(bright[yy, 692:816].sum())
    if n > 30: print(f"  RT bright row y{yy}: {n}")
for xx in range(689, 820):
    n = int(bright[175:330, xx].sum())
    if n > 30: print(f"  RT bright col x{xx}: {n}")

print("== LEFT front internal seams (dark rows/cols inside salmon) ==")
lum = (0.299*R + 0.587*G + 0.114*B)
for yy in range(240, 432):
    n = int((lum[yy, 80:190] < 150).sum())
    if n > 80: print(f"  LEFT dark row y{yy}: {n}")
for xx in range(70, 200):
    n = int((lum[250:420, xx] < 150).sum())
    if n > 100: print(f"  LEFT dark col x{xx}: {n}")

print("== TOP BANDS (dark) per cube — bbox per color ==")
BLUEGRAY_D = (37,55,68); YELLOW_D = (84,92,0); ORANGE_D = (81,40,1); GREEN_D = (43,94,0); MAG_D = (78,0,78)
m_bg = near(BLUEGRAY_D, 22); m_yd = near(YELLOW_D, 22); m_od = near(ORANGE_D, 20); m_gd = near(GREEN_D, 22); m_md = near(MAG_D, 22)
print("-- LEFT cube --")
bbox(m_bg, 60, 290, 150, 205, "L bluegray band"); bbox(m_yd, 60, 290, 195, 222, "L yellow band")
bbox(m_od, 60, 290, 215, 245, "L orange band"); bbox(m_gd, 60, 290, 230, 260, "L green band"); bbox(m_md, 60, 290, 240, 270, "L mag band")
print("-- GN cube --")
bbox(m_bg, 270, 480, 85, 120, "GN bluegray band"); bbox(m_yd, 270, 480, 110, 140, "GN yellow band")
bbox(m_od, 270, 480, 128, 158, "GN orange band"); bbox(m_gd, 270, 480, 145, 175, "GN green band"); bbox(m_md, 270, 480, 160, 190, "GN mag band")
print("-- IN cube --")
bbox(m_bg, 430, 630, 85, 120, "IN bluegray band"); bbox(m_yd, 430, 630, 110, 145, "IN yellow band")
bbox(m_od, 430, 630, 130, 160, "IN orange band"); bbox(m_gd, 430, 630, 145, 180, "IN green band"); bbox(m_md, 430, 630, 175, 210, "IN mag band")
print("-- RT cube --")
bbox(m_bg, 660, 900, 80, 115, "RT bluegray band"); bbox(m_yd, 660, 900, 105, 140, "RT yellow band")
bbox(m_od, 660, 900, 125, 155, "RT orange band"); bbox(m_gd, 660, 900, 140, 172, "RT green band"); bbox(m_md, 660, 900, 155, 200, "RT mag band")

print("== SIDE STRIPS (bright staircase) per cube ==")
GREEN_B = (133,255,9); ORANGE_B = (238,121,6); YELLOW_B = (250,255,11); BLUEGRAY_B = (117,160,202)
m_gb = near(GREEN_B, 45); m_ob = near(ORANGE_B, 40); m_yb = near(YELLOW_B, 45); m_bb = near(BLUEGRAY_B, 35)
print("-- LEFT --"); bbox(m_gb, 190, 290, 230, 445, "L green strip"); bbox(m_ob, 190, 290, 230, 445, "L orange strip")
bbox(m_yb, 190, 290, 230, 445, "L yellow strip"); bbox(m_bb, 190, 290, 230, 445, "L bluegray strip")
print("-- GN --"); bbox(m_gb, 400, 480, 170, 345, "GN green strip"); bbox(m_ob, 400, 480, 170, 345, "GN orange strip")
bbox(m_yb, 400, 480, 170, 345, "GN yellow strip"); bbox(m_bb, 400, 480, 170, 345, "GN bluegray strip")
print("-- IN --"); bbox(m_gb, 580, 670, 190, 365, "IN green strip"); bbox(m_ob, 580, 670, 190, 365, "IN orange strip")
bbox(m_yb, 580, 670, 190, 365, "IN yellow strip"); bbox(m_bb, 580, 670, 190, 365, "IN bluegray strip")
print("-- RT --"); bbox(m_gb, 815, 900, 160, 340, "RT green strip"); bbox(m_ob, 815, 900, 160, 340, "RT orange strip")
bbox(m_yb, 815, 900, 160, 340, "RT yellow strip"); bbox(m_bb, 815, 900, 160, 340, "RT bluegray strip")

print("== per-strip column profiles (which x ranges are filled) ==")
def colprof(m, x0, x1, y0, y1, name):
    cols = []
    for xx in range(x0, x1):
        n = int(m[y0:y1, xx].sum())
        if n > (y1-y0)*0.3: cols.append(xx)
    # group into runs
    runs = []
    for c in cols:
        if runs and c - runs[-1][1] <= 2: runs[-1][1] = c
        else: runs.append([c, c])
    print(f"  {name}: {runs}")
colprof(m_gb, 190, 290, 260, 400, "L green"); colprof(m_ob, 190, 290, 260, 400, "L orange")
colprof(m_yb, 190, 290, 260, 400, "L yellow"); colprof(m_bb, 190, 290, 260, 400, "L bluegray")
colprof(m_gb, 400, 480, 200, 320, "GN green"); colprof(m_ob, 400, 480, 200, 320, "GN orange")
colprof(m_yb, 400, 480, 200, 320, "GN yellow"); colprof(m_bb, 400, 480, 200, 320, "GN bluegray")
colprof(m_gb, 580, 670, 220, 340, "IN green"); colprof(m_ob, 580, 670, 220, 340, "IN orange")
colprof(m_yb, 580, 670, 220, 340, "IN yellow"); colprof(m_bb, 580, 670, 220, 340, "IN bluegray")
colprof(m_gb, 815, 900, 190, 320, "RT green"); colprof(m_ob, 815, 900, 190, 320, "RT orange")
colprof(m_yb, 815, 900, 190, 320, "RT yellow"); colprof(m_bb, 815, 900, 190, 320, "RT bluegray")
