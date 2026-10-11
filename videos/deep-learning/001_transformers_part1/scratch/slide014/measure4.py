#!/usr/bin/env python3
"""Pass 4: correlation-fit pasted figure rects; panel border probe; arc color + faint sweep ends."""
import numpy as np
from PIL import Image

VID = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1"
frame = np.asarray(Image.open(f"{VID}/unique_slides/slide_014.jpg").convert("RGB")).astype(int)
fig_img = Image.open(f"{VID}/../001_transformers_part1/slide_18_source/The Transformer - model architecture..png").convert("RGB")

def masks(a):
    R, G, B = a[..., 0], a[..., 1], a[..., 2]
    mx = np.maximum(np.maximum(R, G), B); mn = np.minimum(np.minimum(R, G), B)
    pastel = (mx - mn > 22) & (mx > 140)
    ink = (R < 110) & (G < 110) & (B < 110)
    dark = (mx < 160) & (mx - mn < 40)  # grays/black lines
    return pastel, ink, dark

def fit_rect(panel_box, fig, tag, scales):
    x0, y0, x1, y1 = panel_box
    sub = frame[y0:y1, x0:x1]
    fp, fi, fd = masks(sub)
    fm = fp | fi | fd
    best = None
    for s in scales:
        w, h = max(1, int(round(fig.size[0] * s))), max(1, int(round(fig.size[1] * s)))
        if w > sub.shape[1] or h > sub.shape[0]:
            continue
        f = np.asarray(fig.resize((w, h), Image.LANCZOS)).astype(int)
        qp, qi, qd = masks(f)
        qm = qp | qi | qd
        # slide qm over fm, compute IoU
        for dy in range(0, sub.shape[0] - h + 1):
            for dx in range(0, sub.shape[1] - w + 1):
                A = fm[dy:dy + h, dx:dx + w]
                inter = (A & qm).sum(); union = (A | qm).sum()
                iou = inter / max(union, 1)
                if best is None or iou > best[0]:
                    best = (iou, s, w, h, dx, dy)
    iou, s, w, h, dx, dy = best
    print(f"{tag}: best IoU={iou:.3f} scale={s:.4f} img {w}x{h} at panel+offset ({dx},{dy}) -> frame rect x[{x0+dx},{x0+dx+w}] y[{y0+dy},{y0+dy+h}]")
    return best

# scale range: content suggests ~0.166-0.172 for left
import numpy as _np
scales = [0.160, 0.163, 0.166, 0.168, 0.169, 0.170, 0.171, 0.172, 0.174, 0.176]
fit_rect((95, 108, 411, 522), fig_img, "LEFT", scales)
fit_rect((478, 154, 892, 470), fig_img.transpose(Image.ROTATE_270), "RIGHT(rot)", [0.166, 0.168, 0.169, 0.170, 0.171, 0.172, 0.174, 0.176, 0.178, 0.180])

# ---- panel border probe (1px steps) ----
print("\nleft panel top edge x=300:", [f"{frame[y,300,0]:02X}" for y in range(104, 114)])
print("left panel left edge y=300:", [f"{frame[300,x,0]:02X}" for x in range(90, 100)])
print("left panel bottom edge x=300:", [f"{frame[y,300,0]:02X}" for y in range(516, 526)])
print("right panel top edge x=600:", [f"{frame[y,600,0]:02X}" for y in range(150, 160)])
print("right panel bottom edge x=600:", [f"{frame[y,600,0]:02X}" for y in range(464, 474)])
print("right panel right edge y=310:", [f"{frame[310,x,0]:02X}" for x in range(886, 898)])

# ---- arc core color + faint ends ----
R, G, B = frame[..., 0], frame[..., 1], frame[..., 2]
red_strict = (R > 120) & (R - G > 60) & (R - B > 60)
ys, xs = np.where(red_strict)
m = (xs >= 400) & (xs <= 520) & (ys >= 230) & (ys <= 380)
px = frame[ys[m], xs[m]]
q = (px // 8) * 8 + 4
keys, counts = np.unique(q.reshape(-1, 3), axis=0, return_counts=True)
top = np.argsort(counts)[::-1][:6]
print("\narc color modes:", [["#%02X%02X%02X" % tuple(keys[i]), int(counts[i])] for i in top])

# faint red in gap? lower threshold
red_faint = (R - G > 25) & (R - B > 25) & (R > 100)
ys2, xs2 = np.where(red_faint)
cx, cy = 450.38, 307.60
ang2 = np.degrees(np.arctan2(-(ys2 - cy), xs2 - cx))
rr2 = np.hypot(xs2 - cx, ys2 - cy)
mm = (rr2 > 12) & (rr2 < 36) & (xs2 >= 400) & (xs2 <= 520) & (ys2 >= 230) & (ys2 <= 380)
h2, _ = np.histogram(ang2[mm], bins=72, range=(-180, 180))
print("faint-red angular occupancy (5deg bins, -180..180):")
print([f"{i*5-180:+04d}:{int(v)}" for i, v in enumerate(h2) if v > 0][:40])

# ---- title/caption core colors ----
for tag, cond, box in [
    ("title", (R > 120) & (R - G > 60) & (R - B > 60), (150, 40, 830, 100)),
    ("red caption", (R > 120) & (R - G > 60) & (R - B > 60), (430, 100, 780, 150)),
    ("blue takeaway", (B > 120) & (B - R > 60) & (B - G > 60), (420, 460, 920, 540)),
]:
    x0, y0, x1, y1 = box
    sub = frame[y0:y1, x0:x1]
    msk = cond[sub[..., 0], sub[..., 1], sub[..., 2]] if False else None
    Rr, Gg, Bb = sub[..., 0], sub[..., 1], sub[..., 2]
    if tag.startswith("blue"):
        m2 = (Bb > 120) & (Bb - Rr > 60) & (Bb - Gg > 60)
    else:
        m2 = (Rr > 120) & (Rr - Gg > 60) & (Rr - Bb > 60)
    p = sub[m2]
    qq = (p // 8) * 8 + 4
    k2, c2 = np.unique(qq.reshape(-1, 3), axis=0, return_counts=True)
    t2 = np.argsort(c2)[::-1][:3]
    print(f"{tag} colors:", [["#%02X%02X%02X" % tuple(k2[i]), int(c2[i])] for i in t2])
