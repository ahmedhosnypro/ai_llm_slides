#!/usr/bin/env python3
import numpy as np, os
from PIL import Image, ImageFont, ImageDraw

IM = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_015.jpg"
im = np.asarray(Image.open(IM).convert("RGB")).astype(int)
r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]
red = (r > 120) & (g < 110) & (b < 110)

def crop_mask(y0, y1, x0, x1):
    m = red[y0:y1+1, x0:x1+1]
    ys, xs = np.where(m)
    return m[ys.min():ys.max()+1, xs.min():xs.max()+1]

L1m = crop_mask(180, 250, 200, 780)   # "[2] Machine Learning"
L3m = crop_mask(310, 380, 290, 690)   # "Deep Learning"
VSm = crop_mask(260, 300, 460, 520)   # "vs"

# cap heights
mcap = L1m[:, 80:132]  # 'M' of Machine
dys = np.where(mcap.sum(axis=1) > 0)[0]
print("L1 'M' rows:", dys.min(), dys.max(), "cap h =", dys.max()-dys.min()+1, "(abs rows", 189+dys.min(), 189+dys.max(), ")")
d3 = L3m[:, :int(L3m.shape[1]*0.12)]
dys3 = np.where(d3.sum(axis=1) > 0)[0]
print("L3 'D' rows:", dys3.min(), dys3.max(), "cap h =", dys3.max()-dys3.min()+1, "(abs rows", 320+dys3.min(), 320+dys3.max(), ")")

# core color (5x5 all-red) within the three bands, excluding border cols
core_red = red.copy()
core_red[:185, :] = False; core_red[380:, :] = False; core_red[:, :70] = False; core_red[:, 890:] = False
core = np.zeros_like(core_red)
rr, cc = np.where(core_red)
for y, x in zip(rr, cc):
    if core_red[y-2:y+3, x-2:x+3].all(): core[y, x] = True
ys, xs = np.where(core)
ink = im[ys, xs]
vals, counts = np.unique(ink.reshape(-1, 3), axis=0, return_counts=True)
topi = np.argsort(-counts)[:5]
print("text core (5x5 all-red) modal:", [f"#{vals[i][0]:02X}{vals[i][1]:02X}{vals[i][2]:02X}({counts[i]})" for i in topi])
print(f"core mean: #{int(ink[:,0].mean()):02X}{int(ink[:,1].mean()):02X}{int(ink[:,2].mean()):02X}  n={len(ink)}")

FONTS = {
    "LiberationSansBold": "/usr/share/fonts/liberation/LiberationSans-Bold.ttf",
    "LiberationSerifBold": "/usr/share/fonts/liberation/LiberationSerif-Bold.ttf",
    "DejaVuSansBold": "/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf",
}
for k, v in list(FONTS.items()):
    if not os.path.exists(v):
        print("missing:", k); del FONTS[k]

def render_mask(text, fontpath, size):
    f = ImageFont.truetype(fontpath, size)
    img = Image.new("L", (1600, 300), 0)
    ImageDraw.Draw(img).text((30, 30), text, font=f, fill=255)
    a = np.asarray(img) > 100
    ys, xs = np.where(a)
    if not len(ys): return None
    return a[ys.min():ys.max()+1, xs.min():xs.max()+1]

def iou(a, bmask):
    bi = np.asarray(Image.fromarray((bmask*255).astype(np.uint8)).resize((a.shape[1], a.shape[0]), Image.LANCZOS)) > 100
    return (a & bi).sum() / (a | bi).sum()

MEAS = {"L1": ("[2] Machine Learning", L1m, 543, 39), "L3": ("Deep Learning", L3m, 371, 39)}
print("\n--- metric solve (titles) ---")
results = []
for name, path in FONTS.items():
    best = None
    for size in range(45, 80):
        mL1 = render_mask(MEAS["L1"][0], path, size)
        if mL1 is None: continue
        e_w1 = abs(mL1.shape[1] - MEAS["L1"][2])
        mH = render_mask("HMD", path, size)
        cap = mH.shape[0]
        e_cap = abs(cap - MEAS["L1"][3])
        mL3 = render_mask(MEAS["L3"][0], path, size)
        e_w3 = abs(mL3.shape[1] - MEAS["L3"][2])
        score = e_w1 + e_w3 + 2*e_cap
        if best is None or score < best[0]: best = (score, size, e_w1, e_w3, cap, e_cap)
    print(f"{name}: size={best[1]} L1w_err={best[2]} L3w_err={best[3]} cap={best[4]}(err{best[5]})")
    results.append((name, best[1], path))

print("\n--- IoU on L1 and L3 ---")
for name, size, path in results:
    print(f"{name}@{size}: L1 IoU={iou(L1m, render_mask(MEAS['L1'][0], path, size)):.3f}  L3 IoU={iou(L3m, render_mask(MEAS['L3'][0], path, size)):.3f}")

print("\n--- vs solve: 'vs' vs 'VS' ---")
for name, path in FONTS.items():
    for text in ("vs", "VS"):
        best = None
        for size in range(20, 60):
            m = render_mask(text, path, size)
            if m is None: continue
            e = abs(m.shape[1]-37) + abs(m.shape[0]-20)
            if best is None or e < best[0]: best = (e, size, m.shape[1], m.shape[0])
        print(f"{name} '{text}': size={best[1]} w={best[2]} h={best[3]} err={best[0]}")
best_overall = []
for name, path in FONTS.items():
    for text in ("vs", "VS"):
        for size in range(24, 56):
            m = render_mask(text, path, size)
            if m is None: continue
            best_overall.append((iou(VSm, m), f"{name} '{text}'@{size}"))
best_overall.sort(reverse=True)
for s, lab in best_overall[:6]: print(f"IoU {s:.3f}  {lab}")
