#!/usr/bin/env python3
"""Decisive font tests: (1) title glyph-run fingerprint, (2) stmt2 text rows,
(3) bullet descender/cursor rows, (4) title N cap extent."""
from PIL import Image, ImageFont, ImageDraw
import json

SRC = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_039.jpg"
img = Image.open(SRC).convert("RGB")
px = img.load()
def ink(p): return sum(p) < 640

out = {}
# (2) stmt2 rows: x 160..715, rows 328..358
out["stmt2_rows"] = {y: sum(1 for x in range(160, 716) if ink(px[x, y])) for y in range(328, 359)}
# (3) bullet rows x-locations: rows 456..468 -> which x have ink
for y in [459, 460, 461, 462, 463]:
    xs = [x for x in range(95, 760) if ink(px[x, y])]
    out[f"row{y}_xs"] = (min(xs), max(xs), len(xs)) if xs else None
# (4) title N column extent (x 344..365)
out["title_N_rows"] = [y for y in range(50, 95) if any(ink(px[x, y]) for x in range(344, 366))]
# title full ink rows again incl x 340..570
out["title_rows_full"] = [y for y in range(50, 95) if any(ink(px[x, y]) for x in range(340, 570))]

# (1) glyph-run fingerprints at fitted sizes
FONTS = {
    "VerdanaB": "/usr/share/fonts/TTF/Verdanab.TTF",
    "ArialB": "/usr/share/fonts/TTF/Arialbd.TTF",
    "ArialBlack": "/usr/share/fonts/TTF/AriBlk.TTF",
    "TimesB": "/usr/share/fonts/TTF/Timesbd.TTF",
    "NotoSansB": "/usr/share/fonts/TTF/NotoSans-Bold.ttf",
    "LiberationSansB": "/usr/share/fonts/liberation/LiberationSans-Bold.ttf",
    "DejaVuSansB": "/usr/share/fonts/TTF/DejaVuSans-Bold.ttf",
}
d = ImageDraw.Draw(Image.new("L", (10, 10)))
def runs_at(fontpath, size, text):
    f = ImageFont.truetype(fontpath, int(round(size * 4)))  # 4x supersample
    bb = d.textbbox((0, 0), text, font=f)
    im = Image.new("L", (bb[2] - bb[0] + 8, bb[3] - bb[1] + 8), 255)
    dd = ImageDraw.Draw(im)
    dd.text((4 - bb[0], 4 - bb[1]), text, font=f, fill=0)
    w = im.size[0]
    prof = [sum(1 for y in range(im.size[1]) if im.getpixel((x, y)) < 160) for x in range(w)]
    runs = []
    x0 = None
    for x, n in enumerate(prof):
        if n > 0 and x0 is None: x0 = x
        if n == 0 and x0 is not None: runs.append((x0, x - 1)); x0 = None
    if x0 is not None: runs.append((x0, w - 1))
    # merge gaps of 1 supersample px, then downscale
    merged = []
    for r in runs:
        if merged and r[0] - merged[-1][1] <= 4: merged[-1] = (merged[-1][0], r[1])
        else: merged.append(list(r))
    return {"w_px": round(w / 4, 1), "h_px": round(im.size[1] / 4, 1),
            "runs_scaled": [[round(r[0] / 4, 1), round(r[1] / 4, 1)] for r in merged]}

ORIG_RUNS = [[344, 365], [368, 386], [390, 400], [403, 429], [432, 457], [462, 467], [470, 516], [518, 523], [527, 545], [548, 565]]
orig_w = 565 - 344 + 1
orig_rel = [[round((a - 344) / orig_w, 3), round((b - 344) / orig_w, 3)] for a, b in ORIG_RUNS]
out["orig_rel_runs"] = orig_rel
for name, path in FONTS.items():
    # size that matches ink width 222 frame px -> slide 231.2? use frame px directly: PIL size in px = pt at 1:1
    # find size where ink width == 222
    lo, hi = 10, 80
    for _ in range(20):
        mid = (lo + hi) / 2
        f = ImageFont.truetype(path, int(round(mid * 4)))
        bb = d.textbbox((0, 0), "Normalization", font=f)
        w = (bb[2] - bb[0]) / 4
        if w < 222: lo = mid
        else: hi = mid
    size = round((lo + hi) / 2, 1)
    r = runs_at(path, size, "Normalization")
    rel = [[round((a) / r["w_px"], 3), round((b) / r["w_px"], 3)] for a, b in r["runs_scaled"]]
    # compare run boundaries
    err = 0
    if len(rel) == len(orig_rel):
        err = sum(abs(a[0] - b[0]) + abs(a[1] - b[1]) for a, b in zip(rel, orig_rel)) / len(rel)
    out[f"fit_{name}"] = {"size": size, "n_runs": len(rel), "mean_run_err": round(err, 4), "rel_runs": rel, "ink_h": r["h_px"]}

print(json.dumps(out, indent=1))
