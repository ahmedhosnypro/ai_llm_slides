#!/usr/bin/env python3
"""Per-line run analysis of the rules box text: word-level blue/red runs + underline rows."""
import numpy as np
from PIL import Image

V = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2"
img = np.asarray(Image.open(f"{V}/unique_slides/slide_024.jpg").convert("RGB")).astype(int)

sx = (899 - 58) / (919.0 - 42.0); a = 58 - sx * 42.0
sy = (516 - 43) / (540.0 - 45.0); b = 43 - sy * 45.0
def S(fx, fy): return ((fx - a) / sx, (fy - b) / sy)

bands = [(363, 384, "L1"), (386, 406, "L2"), (408, 429, "L3"),
         (430, 450, "L4"), (452, 472, "L5"), (474, 494, "L6")]

def runs_of(mask_row, off):
    d = np.diff(np.concatenate(([0], mask_row.astype(int), [0])))
    starts = np.where(d == 1)[0]; ends = np.where(d == -1)[0]
    return [(s_ + off, e_ + off - 1) for s_, e_ in zip(starts, ends) if e_ - s_ >= 1]

def merge_runs(rs, gap=4):
    if not rs: return []
    out = [list(rs[0])]
    for s, e in rs[1:]:
        if s - out[-1][1] <= gap: out[-1][1] = e
        else: out.append([s, e])
    return [tuple(r) for r in out]

for y0, y1, tag in bands:
    reg = img[y0:y1, 78:882]
    r, g, bl = reg[..., 0], reg[..., 1], reg[..., 2]
    blue = (bl > 100) & (bl > r + 30)
    red = (r > 110) & (r > bl + 40) & (g < r - 30)
    # word-level: merge column ink (any color) with gap<=4
    any_ = blue | red
    colprof = any_.any(axis=0)
    words = merge_runs(runs_of(colprof, 78), gap=4)
    out = []
    for ws, we in words:
        sub = slice(ws - 78, we - 78 + 1)
        nb = int(blue[:, sub].sum()); nr = int(red[:, sub].sum())
        col = "RED" if nr > nb else "BLU"
        s0, _ = S(ws, 0); s1, _ = S(we, 0)
        out.append(f"[{col} {s0:.0f}..{s1:.0f}]")
    # underlines: rows in lower part of band with long runs
    urls = []
    for yy in range(reg.shape[0]):
        for (s_, e_) in runs_of(blue[yy], 78):
            if e_ - s_ >= 20:
                urls.append((y0 + yy, s_, e_))
    print(f"{tag} y{y0}..{y1}:")
    print("   words:", " ".join(out))
    if urls:
        su = merge_runs([(u[1], u[2]) for u in urls], gap=6)
        print("   underline runs (frame x):", [(f"{s}", f"{e}", f"S {S(s,0)[0]:.0f}..{S(e,0)[0]:.0f}") for s, e in su],
              "rows", sorted(set(u[0] for u in urls)))
