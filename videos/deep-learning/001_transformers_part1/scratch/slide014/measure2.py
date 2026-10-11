#!/usr/bin/env python3
"""Pass 2: figure placement match vs banked Figure 1; arc arrowhead; panel content checks."""
import numpy as np
from PIL import Image

VID = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1"
frame = np.asarray(Image.open(f"{VID}/unique_slides/slide_014.jpg").convert("RGB")).astype(int)
fig = Image.open(f"{VID}/../001_transformers_part1/slide_18_source/The Transformer - model architecture..png").convert("RGB")
print("fig size:", fig.size)

def pastel_mask(a):
    """Google-docs pastel fills: saturated light colors."""
    R, G, B = a[..., 0], a[..., 1], a[..., 2]
    mx = np.maximum(np.maximum(R, G), B)
    mn = np.minimum(np.minimum(R, G), B)
    return (mx - mn > 25) & (mx > 150)

def black_ink(a):
    R, G, B = a[..., 0], a[..., 1], a[..., 2]
    return (R < 90) & (G < 90) & (B < 90)

# ---- left panel of frame ----
LP = frame[108:522, 95:411]  # 414 x 316
lp_pastel = pastel_mask(LP)
lp_ink = black_ink(LP)
print("left panel pastel px:", lp_pastel.sum(), "ink px:", lp_ink.sum())

# ---- candidate: resize banked fig to exactly 316x414 (stretch) ----
for (w, h, tag) in [(316, 414, "stretch316x414"), (281, 414, "aspect_h414"), (316, 465, "aspect_w316")]:
    f = np.asarray(fig.resize((w, h), Image.LANCZOS)).astype(int)
    fp = pastel_mask(f)
    # IoU over overlapping region
    hh, ww = min(h, 414), min(w, 316)
    A = lp_pastel[:hh, :ww]
    Bm = fp[:hh, :ww]
    inter = (A & Bm).sum()
    union = (A | Bm).sum()
    # also with ink
    A2 = lp_ink[:hh, :ww]
    B2 = black_ink(f)[:hh, :ww]
    i2 = (A2 & B2).sum(); u2 = (A2 | B2).sum()
    print(f"{tag}: pastel IoU={inter/max(union,1):.3f} ink IoU={i2/max(u2,1):.3f}")

# ---- right panel: compare against ROTATED fig ----
RP = frame[154:470, 478:892]  # 316 x 414
fig_rot = fig.transpose(Image.ROTATE_270)  # 90 deg clockwise
print("fig_rot size:", fig_rot.size)
rp_pastel = pastel_mask(RP)
rp_ink = black_ink(RP)
for (w, h, tag) in [(414, 316, "stretch414x316"), (414, 316, "same")]:
    f = np.asarray(fig_rot.resize((w, h), Image.LANCZOS)).astype(int)
    fp = pastel_mask(f)
    A = rp_pastel[:h, :w]
    Bm = fp[:h, :w]
    print(f"right {tag}: pastel IoU={(A & Bm).sum()/max((A | Bm).sum(),1):.3f} "
          f"ink IoU={((rp_ink[:h,:w] & black_ink(f)).sum())/max((rp_ink[:h,:w] | black_ink(f)).sum(),1):.3f}")

# ---- arc: per-angle-bin radial extent (find arrowhead + stroke width) ----
R, G, B = frame[..., 0], frame[..., 1], frame[..., 2]
red = (R > 120) & (R - G > 60) & (R - B > 60)
ys, xs = np.where(red)
gut = (xs >= 400) & (xs <= 520) & (ys >= 230) & (ys <= 380)
xs, ys = xs[gut], ys[gut]
cx, cy = xs.mean(), ys.mean()
ang = np.degrees(np.arctan2(-(ys - cy), xs - cx))
rr = np.hypot(xs - cx, ys - cy)
print(f"\narc centroid ({cx:.1f},{cy:.1f})")
for lo in range(-180, 180, 10):
    m = (ang >= lo) & (ang < lo + 10)
    if m.sum() > 3:
        print(f"  bin [{lo:+4d},{lo+10:+4d}): n={m.sum():4d} r=[{rr[m].min():5.1f},{rr[m].max():5.1f}]")

# per-pixel radial histogram to find stroke width & arrowhead band
hist, edges = np.histogram(rr, bins=40, range=(0, 40))
print("radial hist:", [int(v) for v in hist])

# ---- check figure content bboxes within panels (content margins) ----
def content_bbox(a, name):
    p = pastel_mask(a)
    k = black_ink(a)
    m = p | k
    ys, xs = np.where(m)
    print(f"{name}: content bbox in-panel x[{xs.min()},{xs.max()}] y[{ys.min()},{ys.max()}] of {a.shape[1]}x{a.shape[0]}")

content_bbox(LP, "left panel")
content_bbox(RP, "right panel")
fc = pastel_mask(np.asarray(fig).astype(int)) | black_ink(np.asarray(fig).astype(int))
ys, xs = np.where(fc)
print(f"banked fig content bbox: x[{xs.min()},{xs.max()}] y[{ys.min()},{ys.max()}] of {fig.size[0]}x{fig.size[1]}")
