#!/usr/bin/env python3
from pathlib import Path
from PIL import Image
import numpy as np

V = Path("/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks")
B = V / "recreated_pptx/build"
Q = V / "recreated_pptx/qa/slide005/attempt_02"
Q.mkdir(parents=True, exist_ok=True)
orig = Image.open(V / "unique_slides/slide_005.jpg").convert("RGB")
render = Image.open(B / "slide_005_rendered-1.png").convert("RGB")
assert render.size == (2001, 1125), render.size
r = render.resize((960, 540), Image.Resampling.LANCZOS)
o = np.asarray(orig).astype(int)
a = np.asarray(r).astype(int)


def masks(x):
    R, G, B = x[:, :, 0], x[:, :, 1], x[:, :, 2]
    red = (R > 110) & (R - G > 25) & (R - B > 25)
    blue = (B > 90) & (B - R > 50) & (B - G > 50)
    return red, blue


def bbox(mask, win):
    x0, y0, x1, y1 = win
    ys, xs = np.nonzero(mask[y0:y1, x0:x1])
    if not len(xs):
        return None
    return (x0 + int(xs.min()), y0 + int(ys.min()), x0 + int(xs.max()), y0 + int(ys.max()))


def delta(ob, rb):
    if ob is None or rb is None:
        return None
    return tuple(abs(x - y) for x, y in zip(ob, rb))


o_red, o_blue = masks(o)
r_red, r_blue = masks(a)
checks = [
    ("augmented label", o_blue, r_blue, (290, 150, 419, 185)),
    ("weight bias red", o_red, r_red, (596, 100, 616, 126)),
    ("sum to step arrow", o_red, r_red, (439, 412, 471, 431)),
    ("step to output arrow", o_red, r_red, (504, 412, 579, 431)),
    ("top implication arrow", o_red, r_red, (172, 155, 201, 177)),
    ("banner implication arrow", o_red, r_red, (498, 282, 529, 304)),
]
failed = []
for name, om, rm, win in checks:
    ob, rb = bbox(om, win), bbox(rm, win)
    d = delta(ob, rb)
    ok = d is not None and max(d) <= 4
    print(f"{name}: original={ob} render={rb} delta={d} {'PASS' if ok else 'FAIL'}")
    if not ok:
        failed.append(name)

ys, xs = np.nonzero(r_blue[150:185, 290:419])
rows = np.where(r_blue[150:185, 290:419].any(axis=1))[0] + 150
bands = []
if len(rows):
    start = prev = int(rows[0])
    for y in rows[1:]:
        y = int(y)
        if y > prev + 1:
            bands.append((start, prev))
            start = y
        prev = y
    bands.append((start, prev))
print("augmented label blue row bands:", bands)
if len(bands) != 1:
    failed.append("augmented label wraps")

regions = {
    "v1": (110, 100, 145, 240),
    "aug": (242, 90, 279, 245),
    "w": (585, 90, 625, 245),
    "rules": (537, 255, 756, 338),
}
for name, box in regions.items():
    for tag, im in (("original", orig), ("render", r)):
        crop = im.crop(box)
        crop.resize((crop.width * 4, crop.height * 4), Image.Resampling.LANCZOS).save(Q / f"{name}_{tag}_x4.png")
print("delimiter crop pairs banked in", Q)
if failed:
    raise SystemExit("FAIL: " + ", ".join(failed))
print("FOCUSED GEOMETRY: PASS")
