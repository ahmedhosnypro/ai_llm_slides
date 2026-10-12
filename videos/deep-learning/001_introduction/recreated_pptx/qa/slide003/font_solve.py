#!/usr/bin/env python3
"""Font solve for slide_003 title: candidate fonts x sizes, fit cap height 46px,
ink widths (L1 '[1] Revision of' = 433px @cols 269..701; L2 'Machine Learning' = 530px
@cols 218..747), then binary-mask correlation of a rendered candidate vs the original
crop. Also: title core color (3x3 all-red modal) and baseline refinement."""
import numpy as np
from PIL import Image, ImageDraw, ImageFont

IM = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_003.jpg"
im = np.asarray(Image.open(IM).convert("RGB")).astype(int)
r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]
red = (r > 120) & (g < 110) & (b < 110)

# --- title core color: pixels whose 3x3 neighborhood is fully red ---
core = np.zeros_like(red)
rr, cc = np.where(red)
for y, x in zip(rr, cc):
    if y < 2 or y > 537 or x < 2 or x > 957:
        continue
    if red[y-2:y+3, x-2:x+3].all():
        core[y, x] = True
core[40:60, :] = False  # exclude border strokes region
core[:, :70] = False
core[:, 890:] = False
core[510:, :] = False
ys, xs = np.where(core)
ink = im[ys, xs]
vals, counts = np.unique(ink.reshape(-1, 3), axis=0, return_counts=True)
top = vals[np.argsort(-counts)[:5]]
print("title core (5x5 all-red) modal:", [f"#{t[0]:02X}{t[1]:02X}{t[2]:02X}({c})" for t, c in zip(top, np.sort(counts)[::-1][:5])])
print(f"core mean: #{int(ink[:,0].mean()):02X}{int(ink[:,1].mean()):02X}{int(ink[:,2].mean()):02X}  n={len(ink)}")

# --- candidates ---
FONTS = {
    "LiberationSansBold": "/usr/share/fonts/liberation/LiberationSans-Bold.ttf",
    "LiberationSerifBold": "/usr/share/fonts/liberation/LiberationSerif-Bold.ttf",
    "DejaVuSansBold": "/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf",
}
import os
for k, v in list(FONTS.items()):
    if not os.path.exists(v):
        print("missing font:", k, v)
        del FONTS[k]

L1, L2 = "[1] Revision of", "Machine Learning"
MEAS = {"L1_w": 433, "L2_w": 530, "cap": 46}  # ink px

def render_mask(text, fontpath, size):
    f = ImageFont.truetype(fontpath, size)
    img = Image.new("L", (1400, 260), 0)
    d = ImageDraw.Draw(img)
    d.text((30, 30), text, font=f, fill=255)
    a = np.asarray(img) > 100
    ys, xs = np.where(a)
    if not len(ys):
        return None, None
    return a[ys.min():ys.max()+1, xs.min():xs.max()+1], (ys.max()-ys.min()+1, xs.max()-xs.min()+1)

print("\n--- metric solve ---")
results = []
for name, path in FONTS.items():
    # solve size from L2 ink width target
    best = None
    for size in range(55, 80):
        m, (h, w) = render_mask(L2, path, size)
        if m is None:
            continue
        err_w = abs(w - MEAS["L2_w"])
        # cap height check via 'H'
        mh, _ = render_mask("HML", path, size)
        cap = mh.shape[0] if mh is not None else 0
        err_cap = abs(cap - MEAS["cap"])
        m1, (h1, w1) = render_mask(L1, path, size)
        err_w1 = abs(w1 - MEAS["L1_w"]) if m1 is not None else 999
        score = err_w + err_w1 + 2 * err_cap
        if best is None or score < best[0]:
            best = (score, size, w, w1, cap, err_w, err_w1, err_cap)
    print(f"{name}: best size={best[1]} L2w={best[2]}(err{best[5]}) L1w={best[3]}(err{best[6]}) cap={best[4]}(err{best[7]})")
    results.append((best[0], name, best[1], path))

# --- mask correlation at each candidate's best size ---
def orig_mask(y0, y1, x0, x1):
    m = red[y0:y1+1, x0:x1+1]
    ys, xs = np.where(m)
    return m[ys.min():ys.max()+1, xs.min():xs.max()+1]

orig2 = orig_mask(266, 330, 210, 760)  # line 2 crop with margin
print(f"\norig L2 mask {orig2.shape}")

def iou(a, b):
    # resize b (candidate) to a's shape
    bi = np.asarray(Image.fromarray((b*255).astype(np.uint8)).resize((a.shape[1], a.shape[0]), Image.LANCZOS)) > 100
    inter = (a & bi).sum()
    union = (a | bi).sum()
    return inter / union

print("\n--- correlation (IoU) on line 2 ---")
for _, name, size, path in sorted(results):
    m, _ = render_mask(L2, path, size)
    print(f"{name}@{size}: IoU={iou(orig2, m):.3f}")

# baseline refinement from profiles
prof = red[:, :].sum(axis=1)
print("\nline1 rows 200-230:", {y: int(prof[y]) for y in range(200, 231) if prof[y] > 0 and 100 < y or (200 <= y <= 230 and prof[y] > 0)})
print("line2 rows 310-332:", {y: int(prof[y]) for y in range(310, 333) if prof[y] > 0})
