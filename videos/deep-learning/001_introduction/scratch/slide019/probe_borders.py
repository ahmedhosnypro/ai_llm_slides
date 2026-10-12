#!/usr/bin/env python3
"""Decisive probes: (1) original box top-border rows (continuous vs dashed per row);
(2) input/samples top border row; (3) container asset dash check; (4) verr text clean cap band."""
import numpy as np
from PIL import Image
from collections import Counter

IM = np.asarray(Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_019.jpg").convert("RGB")).astype(int)
r, g, b = IM[..., 0], IM[..., 1], IM[..., 2]
lum = (r * 299 + g * 587 + b * 114) // 1000

def runs(m, base):
    out, s = [], None
    for i, v in enumerate(m):
        if v and s is None: s = i
        elif not v and s is not None: out.append((base + s, base + i - 1)); s = None
    if s is not None: out.append((base + s, base + len(m) - 1))
    return out

print("== ORIGINAL: per-row dark count in box interiors (continuous=border) ==")
for label, x0, x1 in [("pre int 210..275", 210, 275), ("extr int 325..400", 325, 400),
                      ("sel int 432..508", 432, 508), ("input int 85..155", 85, 155),
                      ("samples int 812..880", 812, 880)]:
    print(f" {label}:")
    for y in range(194, 212):
        n = int((lum[y, x0:x1] < 205).sum())
        rr = runs(lum[y, x0:x1] < 205, x0)
        print(f"   y{y}: n={n:3d} runs={len(rr)} {rr[:4] if len(rr) <= 4 else str(rr[:3])+'...'}")
print(" bottom rows:")
for label, x0, x1 in [("pre int", 210, 275), ("extr int", 325, 400), ("input int", 85, 155)]:
    row = " ".join(f"y{y}:{int((lum[y, x0:x1] < 205).sum())}" for y in range(268, 278))
    print(f" {label}: {row}")

print("== container asset dash check ==")
A = np.asarray(Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/build/assets/container_v2_019.png"))
print(" asset shape:", A.shape)
al = A[..., 3] if A.shape[2] == 4 else None
# top border band: asset rows for frame y195..198 = (y-193)*8.333
band = al[int((195 - 193) * 8.333):int((198.5 - 193) * 8.333), :]
colred = (band > 128).any(axis=0)
rr = runs(colred, 0)
print(f" top-band alpha runs: n={len(rr)} first8 {rr[:8]}")
onpx = int(colred.sum()); span = rr[-1][1] - rr[0][0] + 1 if rr else 0
print(f" on={onpx} span={span} duty={onpx/span if span else 0:.2f}")
# left border band: asset cols for frame x193..196
lb = al[:, int((193 - 191) * 8.333):int((196 - 191) * 8.333)]
rowred = (lb > 128).any(axis=1)
rr2 = runs(rowred, 0)
print(f" left-band alpha runs: n={len(rr2)} first8 {rr2[:8]} on={int(rowred.sum())}")

print("== verr text clean cap band (render) ==")
R = np.asarray(Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/qa/slide019/render_3.png").convert("RGB")).astype(int)
Wr = R.shape[1]; S = Wr / 960.0
rr_, gg_, bb_ = R[..., 0], R[..., 1], R[..., 2]
lumr = (rr_ * 299 + gg_ * 587 + bb_ * 114) // 1000
m = (rr_ > 140) & (gg_ < 95) & (bb_ < 95) & (lumr < 150)
sub = m[int(175 * S):int(225 * S), int(760 * S):int(800 * S)]  # above arrow band y228
ys, xs = np.nonzero(sub)
if len(xs):
    print(f" verr text (y175..225 only): x {760 + xs.min()/S:.1f}..{760 + xs.max()/S:.1f} y {175 + ys.min()/S:.1f}..{175 + ys.max()/S:.1f}")
sub2 = m[int(245 * S):int(300 * S), int(760 * S):int(800 * S)]  # below arrow band
ys2, xs2 = np.nonzero(sub2)
if len(xs2):
    print(f" verr text (y245..300 only): x {760 + xs2.min()/S:.1f}..{760 + xs2.max()/S:.1f} y {245 + ys2.min()/S:.1f}..{245 + ys2.max()/S:.1f}")
print(" (orig text x774..786 y183..286; arrows at y228..242 excluded)")
