#!/usr/bin/env python3
"""Pass 5: extended scale search; clean panel border probes; text color percentiles."""
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
    return pastel | ink

def fit_rect(panel_box, fig, tag, scales):
    x0, y0, x1, y1 = panel_box
    sub = frame[y0:y1, x0:x1]
    fm = masks(sub)
    best = None
    for s in scales:
        w, h = int(round(fig.size[0] * s)), int(round(fig.size[1] * s))
        if w > sub.shape[1] - 2 or h > sub.shape[0] - 2:
            continue
        f = np.asarray(fig.resize((w, h), Image.LANCZOS)).astype(int)
        qm = masks(f)
        for dy in range(0, sub.shape[0] - h + 1):
            for dx in range(0, sub.shape[1] - w + 1):
                A = fm[dy:dy + h, dx:dx + w]
                iou = (A & qm).sum() / max((A | qm).sum(), 1)
                if best is None or iou > best[0]:
                    best = (iou, s, w, h, dx, dy)
    iou, s, w, h, dx, dy = best
    print(f"{tag}: IoU={iou:.3f} scale={s:.4f} {w}x{h} frame rect x[{x0+dx},{x0+dx+w}] y[{y0+dy},{y0+dy+h}] margins L{dx} T{dy} R{sub.shape[1]-dx-w} B{sub.shape[0]-dy-h}")

scales = [round(0.170 + 0.002 * i, 4) for i in range(13)]  # 0.170..0.194
fit_rect((95, 108, 411, 522), fig_img, "LEFT", scales)
fit_rect((478, 154, 892, 470), fig_img.transpose(Image.ROTATE_270), "RIGHT(rot)", scales)

# ---- clean border probes (white margin zones) ----
print("\nleft panel TOP edge at x=120 (white zone):", [f"{frame[y,120,0]:02X}" for y in range(103, 112)])
print("left panel BOTTOM edge at x=115:", [f"{frame[y,115,0]:02X}" for y in range(516, 526)])
print("left panel LEFT edge at y=130:", [f"{frame[130,x,0]:02X}" for x in range(90, 99)])
print("left panel RIGHT edge at y=130:", [f"{frame[130,x,0]:02X}" for x in range(406, 416)])
print("right panel TOP edge at x=520:", [f"{frame[y,520,0]:02X}" for y in range(150, 159)])
print("right panel BOTTOM edge at x=520:", [f"{frame[y,520,0]:02X}" for y in range(465, 474)])
print("right panel LEFT edge at y=180:", [f"{frame[180,x,0]:02X}" for x in range(473, 482)])
print("right panel RIGHT edge at y=180:", [f"{frame[180,x,0]:02X}" for x in range(887, 896)])

# ---- text color percentiles ----
def text_stats(tag, box, chan):
    x0, y0, x1, y1 = box
    sub = frame[y0:y1, x0:x1]
    c = sub[..., chan]
    others = [i for i in range(3) if i != chan]
    strong = c >= np.percentile(c, 99.5)
    print(f"{tag}: chan{chan} p99.5={np.percentile(c, 99.5):.0f} max={c.max()} "
          f"mean@strong={c[strong].mean():.0f} | other-ch means at strong: "
          f"{sub[...,others[0]][strong].mean():.0f},{sub[...,others[1]][strong].mean():.0f}")

text_stats("title (R)", (150, 40, 830, 100), 0)
text_stats("red caption (R)", (430, 100, 780, 150), 0)
text_stats("blue takeaway (B)", (420, 460, 920, 540), 2)
text_stats("badge numeral (dark)", (874, 54, 912, 89), 0)
