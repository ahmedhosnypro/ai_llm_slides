#!/usr/bin/env python3
# m5_fine.py — refine frame->render mapping by content-masked SSD around the chrome
# fit (slide_019 m6 method); report chrome-fit vs content-fit divergence.
import numpy as np
from PIL import Image

S = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide004"
frame_im = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_004.jpg").convert("RGB")
render = np.asarray(Image.open(S + "/base-1.png").convert("RGB"), dtype=np.float64)
ax0, sx0, ay0, sy0 = np.load(S + "/fit2.npy")

# content mask: ink areas + their surroundings (where alignment matters), inside panels
ink = render.mean(axis=2) < 160
from scipy import ndimage  # noqa
grow = ndimage.binary_dilation(ink, iterations=3)
mask = np.zeros_like(grow)
mask[250:1080, 200:1180] = True   # left panel + gutter
mask[250:1080, 1190:1900] = True  # right panel
mask &= grow
print("mask px:", mask.sum())

def ssd_for(ax, sx, ay, sy):
    W, H = render.shape[1], render.shape[0]
    w = np.asarray(frame_im.transform((W, H), Image.AFFINE,
        (1 / sx, 0, -ax / sx, 0, 1 / sy, -ay / sy), resample=Image.BILINEAR), dtype=np.float64)
    return np.abs(w - render).sum(axis=2)[mask].mean()

base = ssd_for(ax0, sx0, ay0, sy0)
print(f"chrome-fit SSD {base:.2f} (ax {ax0:.3f} sx {sx0:.6f} ay {ay0:.3f} sy {sy0:.6f})")

# coordinate descent, sub-pixel
ax, sx, ay, sy = ax0, sx0, ay0, sy0
for it in range(3):
    for step in (1.0, 0.5, 0.25):
        for _ in range(2):
            improved = False
            for name in ("ax", "sx", "ay", "sy"):
                for delta in (-step, step):
                    trial = dict(ax=ax, sx=sx, ay=ay, sy=sy)
                    trial[name] += delta * (0.01 if name in ("sx", "sy") else 1.0)
                    v = ssd_for(trial["ax"], trial["sx"], trial["ay"], trial["sy"])
                    if v < base - 1e-6:
                        base, ax, sx, ay, sy = v, trial["ax"], trial["sx"], trial["ay"], trial["sy"]
                        improved = True
            if not improved:
                break
print(f"content-fit SSD {base:.2f} (ax {ax:.3f} sx {sx:.6f} ay {ay:.3f} sy {sy:.6f})")
print(f"divergence from chrome fit: dax {ax - ax0:+.2f}px dsx {sx - sx0:+.6f} day {ay - ay0:+.2f}px dsy {sy - sy0:+.6f}")

# chrome-stroke residuals under the content fit
for fname, rval, fval, tag in [(None, 87.0, 59.0, "left"), (None, 1914.5, 901.0, "right"),
                               (None, 93.5, 43.0, "top"), (None, 1124.0, 516.0, "bottom")]:
    if tag in ("left", "right"):
        pred = ax + sx * fval
    else:
        pred = ay + sy * fval
    print(f"  {tag}: chrome landmark predicts render {pred:.1f} vs measured {rval} (residual {pred - rval:+.1f}px)")

np.save(S + "/fit_content.npy", np.array([ax, sx, ay, sy]))
