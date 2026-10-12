#!/usr/bin/env python3
"""Targeted structure measurement of remapped 002:8 delta regions."""
from PIL import Image
import numpy as np

ROOT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning"
f8 = np.asarray(Image.open(f"{ROOT}/002_transformers_part2/scratch/slide008/frame8_remapped_960x540.png").convert("RGB")).astype(int)
f33 = np.asarray(Image.open(f"{ROOT}/001_transformers_part1/unique_slides/slide_033.jpg").convert("RGB")).astype(int)
r, g, b = f8[:,:,0], f8[:,:,1], f8[:,:,2]

def bbox(mask, tag):
    ys, xs = np.where(mask)
    n = mask.sum()
    if n < 20:
        print(f"{tag}: ({int(n)} px) NONE")
        return None
    print(f"{tag}: {int(n)} px  x {xs.min()}..{xs.max()}  y {ys.min()}..{ys.max()}  center ({(xs.min()+xs.max())//2},{(ys.min()+ys.max())//2})")
    return (xs.min(), ys.min(), xs.max(), ys.max())

def cc(img, x0, y0, x1, y1, tag=""):
    reg = img[y0:y1, x0:x1].reshape(-1, 3)
    # quantized color census
    q = (reg // 24) * 24
    vals, counts = np.unique(q, axis=0, return_counts=True)
    order = np.argsort(-counts)[:6]
    print(f"{tag} census [{x0},{y0}..{x1},{y1}]: " + ", ".join(f"{tuple(int(v) for v in vals[i])}:{int(counts[i])}" for i in order))

print("=== LEFT W_k region (parent has yellow band x150..200) ===")
cc(f8, 145, 230, 205, 390, "8 left W")
cc(f33, 145, 230, 205, 390, "33 left W")
yellow = (r > 215) & (g > 215) & (b < 160) & (b > 60)
bbox(yellow, "8 yellow(F7F96B-like) FULL")
yl = yellow.copy(); yl[:, 210:] = False
bbox(yl, "8 yellow LEFT half only")
yr = yellow.copy(); yr[:, :640] = False
bbox(yr, "8 yellow RIGHT half only")
yellow33 = (f33[:,:,0] > 215) & (f33[:,:,1] > 215) & (f33[:,:,2] < 160) & (f33[:,:,2] > 60)
print("33 yellow px:", int(yellow33.sum()))

print("\n=== mint ellipse detection (like 013) ===")
mint = (g > 220) & (g - r > 25) & (g - b > 25)
bbox(mint, "8 mint full")
m8l = mint.copy(); m8l[:, 250:] = False
bbox(m8l, "8 mint left")

print("\n=== dark-red K2 circle (parent 215..251 x 301..337) present in 8? ===")
darkred = (r > 110) & (r - g > 80) & (r - b > 80)
dr = darkred.copy(); dr[:260, :] = False; dr[370:, :] = False; dr[:, 180:] = False; dr[:, :200] = False
bbox(dr, "8 darkred @K2 region")

print("\n=== blue circle precision (alpha est) ===")
blue = (b - r > 25) & (b - g > 10) & (b > 120) & (r > 80)
bb = bbox(blue, "8 blue circle")
if bb:
    x0, y0, x1, y1 = bb
    # sample center color over known panel peach (247,226,205) and over DP fill (221,202,187)
    print("  8 center px:", tuple(f8[(y0+y1)//2, (x0+x1)//2]), " 33 same px:", tuple(f33[(y0+y1)//2, (x0+x1)//2]))
    # alpha estimate: obs = a*blue + (1-a)*bg. Use blue core 4169E1=(65,105,225)
    for px_, py_, bgname in [((x0+x1)//2, y0+12, "top over peach"), ((x0+x1)//2, (y0+y1)//2, "center"), (x0+15, (y0+y1)//2, "left")]:
        obs = f8[py_, px_]
        bg = f33[py_, px_]
        # solve a from R channel: obs_r = a*65 + (1-a)*bg_r  -> a = (bg_r - obs_r)/(bg_r - 65)
        den = bg[0] - 65
        a = (bg[0] - obs[0]) / den if abs(den) > 30 else float('nan')
        print(f"  alpha est @({px_},{py_}) [{bgname}]: obs={tuple(obs)} bg={tuple(bg)} a={a:.2f}")

print("\n=== chunky red block arrow in 8 (isolate) ===")
chunky = (r - g > 70) & (r - b > 70) & (r > 130)
ch = chunky.copy(); ch[:470, :] = False; ch[:, :250] = False; ch[:, 400:] = False
bbox(ch, "8 chunky arrow isolated x250..400 y470+")
ch33 = (f33[:,:,0] - f33[:,:,1] > 70) & (f33[:,:,0] - f33[:,:,2] > 70) & (f33[:,:,0] > 130)
ch33b = ch33.copy(); ch33b[:470, :] = False; ch33b[:, :180] = False; ch33b[:, 320:] = False
bbox(ch33b, "33 chunky arrow isolated")

print("\n=== DP box bbox in 8 (DCCBBB fill) ===")
dp = (abs(r - 220) < 14) & (abs(g - 202) < 16) & (abs(b - 187) < 16)
dp[:, 350:] = False; dp[:, :230] = False; dp[:150, :] = False
bbox(dp, "8 DP fill region")

print("\n=== multiply circles in 8 (white fill, red ring) near x510..660 ===")
white = (r > 235) & (g > 235) & (b > 235)
wc = white.copy(); wc[:220, :] = False; wc[:, :505] = False; wc[:, 665:] = False; wc[400:, :] = False
bbox(wc, "8 white circles region")

print("\n=== navy dots in DP box (staircase) ===")
navy = (b - r > 60) & (b - g > 60) & (b > 100) & (b < 220)
nv = navy.copy(); nv[:200, :] = False; nv[:, :250] = False; nv[:, 350:] = False; nv[420:, :] = False
bbox(nv, "8 navy dots region")
ys, xs = np.where(nv)
if len(ys) > 50:
    # cluster by y bands
    for band in [(230, 260), (265, 295), (305, 335), (345, 375)]:
        m = (ys >= band[0]) & (ys < band[1])
        if m.sum() > 10:
            print(f"  dot band y{band}: x {xs[m].min()}..{xs[m].max()} center ({(xs[m].min()+xs[m].max())//2}, {(band[0]+band[1])//2}) n={int(m.sum())}")

print("\n=== sentence row widgets in 8 (X labels red ink y455..500 x180..500) ===")
redink = (r - g > 60) & (r - b > 40) & (r > 140)
ri = redink.copy(); ri[:455, :] = False; ri[505:, :] = False; ri[:, :180] = False; ri[:, 520:] = False
bbox(ri, "8 sentence red ink")

print("\n=== W_q box in 8: yellow under blue circle? scan yellow in x260..340 y415..470 ===")
wy = yellow.copy(); wy[:415, :] = False; wy[470:, :] = False; wy[:, :255] = False; wy[:, 345:] = False
bbox(wy, "8 yellow @W_q region")
if wy.sum() > 30:
    ys, xs = np.where(wy)
    print("  sample color:", tuple(f8[ys[len(ys)//2], xs[len(xs)//2]]))

print("\n=== sigma box bbox 8 (EAFEFC fill) ===")
sig = (abs(r - 234) < 12) & (abs(g - 254) < 8) & (abs(b - 252) < 10)
sig[:, :480] = False; sig[:, 680:] = False; sig[:180, :] = False; sig[230:, :] = False
bbox(sig, "8 sigma fill")

print("\n=== Y2 output strip in 8 (green border sysDot box y115..150 x540..625) ===")
grn = (g - r > 30) & (g - b > 20) & (g > 120)
gy = grn.copy(); gy[:110, :] = False; gy[160:, :] = False; gy[:, :520] = False; gy[:, 650:] = False
bbox(gy, "8 Y2 green ink")

print("\n=== right input container bbox 8 (E7FFE9) ===")
paleg = (abs(r - 231) < 12) & (abs(g - 255) < 6) & (abs(b - 233) < 12)
pg = paleg.copy(); pg[:, :700] = False
bbox(pg, "8 pale green right")
pgl = paleg.copy(); pgl[:, 200:] = False
bbox(pgl, "8 pale green left")
