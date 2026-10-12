#!/usr/bin/env python3
# m8_edges_alpha.py — row/col density profiles for exact highlight edges +
# refined global (alpha, color) fit with purity-screened patches.
import numpy as np
from PIL import Image

S = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide004"
B = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning"
frame = np.asarray(Image.open(f"{B}/002_transformers_part2/unique_slides/slide_004.jpg").convert("RGB"), dtype=np.float64)
render = np.asarray(Image.open(f"{S}/base-1.png").convert("RGB"), dtype=np.float64)
ax, sx, ay, sy = np.load(f"{S}/fit4.npy")

fr, fg, fb = frame[..., 0], frame[..., 1], frame[..., 2]
om = (fr > 200) & (fb < 175) & (fg > 130) & (fg < 225) & ((fr - fb) > 60) & ((fg - fb) > 25)

def profile(m, x0, x1, y0, y1, axis, tag):
    if axis == "row":
        d = m[y0:y1, x0:x1].sum(axis=1)
        for i, v in enumerate(d):
            if v > 0 or True:
                pass
        idx = np.where(d > 0)[0]
        print(f"{tag} rows y{y0}..{y1}: first {y0+idx.min()} last {y0+idx.max()}  (50% width crossings:)")
        half = (x1 - x0) * 0.5
        cross = [y0 + i for i in range(len(d)) if d[i] > half]
        print(f"   >50% rows: {cross[0]}..{cross[-1]}  -> slide y {-0.669+1.047547*cross[0]:.1f}..{-0.669+1.047547*(cross[-1]+1):.1f}")
    else:
        d = m[y0:y1, x0:x1].sum(axis=0)
        idx = np.where(d > 0)[0]
        half = (y1 - y0) * 0.5
        cross = [x0 + i for i in range(len(d)) if d[i] > half]
        print(f"{tag} cols x{x0}..{x1}: first {x0+idx.min()} last {x0+idx.max()}")
        print(f"   >50% cols: {cross[0]}..{cross[-1]}  -> slide x {-19.038+1.040408*cross[0]:.1f}..{-19.038+1.040408*(cross[-1]+1):.1f}")

print("== ENCODER highlight (frame) ==")
profile(om, 600, 700, 315, 405, "row", "enc rows (over x600..700)")
profile(om, 560, 745, 345, 385, "col", "enc cols (over y345..385)")
print("== DECODER highlight (frame) ==")
profile(om, 760, 850, 250, 325, "row", "dec rows (over x760..850)")
profile(om, 725, 895, 270, 305, "col", "dec cols (over y270..305)")

# --- refined overlay fit: purity-screened patches ---
def patch(a, x, y, rad=4):
    return a[int(y)-rad:int(y)+rad+1, int(x)-rad:int(x)+rad+1].reshape(-1, 3)

cands = [  # (frame x, y) interior spots; bg read from render at mapped spot
    (605, 352), (615, 380), (700, 382), (595, 370), (660, 350),
    (770, 275), (800, 305), (850, 295), (860, 275), (780, 300),
]
pairs = []
for x, y in cands:
    obs = patch(frame, x, y).mean(axis=0)
    rp = patch(render, ax + sx * x, ay + sy * y)
    bg = rp.mean(axis=0)
    spread = rp.std(axis=0).max()
    tag = "OK" if spread < 12 else f"impure(std {spread:.0f})"
    pairs.append((obs, bg, spread, (x, y), tag))
    print(f"patch ({x},{y}): obs {obs.round(0)} bg {bg.round(0)} {tag}")

good = [(o, bg) for o, bg, s, xy, t in pairs if t == "OK"]
print(f"\n{len(good)} pure patches")
best = None
for a in np.arange(0.35, 0.80, 0.01):
    Cs = np.array([(o - (1 - a) * bg) / a for o, bg in good])
    Cm = Cs.mean(axis=0)
    resid = sum(((o - (a * Cm + (1 - a) * bg)) ** 2).sum() for o, bg in good)
    if best is None or resid < best[1]:
        best = (a, resid, Cm, Cs.std(axis=0))
a, resid, Cm, sd = best
print(f"BEST: alpha={a:.2f} color=({Cm[0]:.0f},{Cm[1]:.0f},{Cm[2]:.0f}) hex=#{int(round(Cm[0])):02X}{int(round(Cm[1])):02X}{int(round(Cm[2])):02X}  per-patch std {sd.round(1)} rms {np.sqrt(resid/len(good)/3):.1f}")
# compare spec candidate
o_spec = []
for o, bg in good:
    pred = 0.5 * np.array([247, 169, 79]) + 0.5 * bg
    o_spec.append(((o - pred) ** 2).sum())
print(f"spec F7A94F@0.50 rms {np.sqrt(np.mean(o_spec)/3):.1f}")
# also C00000-mix check and E58722@0.6
for (C, al) in [((229,135,34), 0.6), ((231,117,1), 0.5)]:
    r_ = [((o - (al * np.array(C) + (1 - al) * bg)) ** 2).sum() for o, bg in good]
    print(f"candidate {C}@{al}: rms {np.sqrt(np.mean(r_)/3):.1f}")
