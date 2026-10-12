#!/usr/bin/env python3
"""measure6.py — fine pass: math token glyphs, L3 comma spacing, gridline modals,
numeral sizes, bullet ring, note box border/text color, title+bullet font joint solve."""
from PIL import Image, ImageFont
import numpy as np

BASE = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction"
im = Image.open(f"{BASE}/unique_slides/slide_044.jpg").convert("RGB")
a = np.asarray(im).astype(int)
R, G, B = a[..., 0], a[..., 1], a[..., 2]

def runs(mask_1d, min_len=1):
    idx = np.where(mask_1d)[0]
    if len(idx) == 0:
        return []
    out, s, p = [], idx[0], idx[0]
    for v in idx[1:]:
        if v == p + 1:
            p = v
        else:
            if p - s + 1 >= min_len:
                out.append((s, p))
            s = p = v
    if p - s + 1 >= min_len:
        out.append((s, p))
    return out

def exact_modal(x0, x1, y0, y1, n=4):
    reg = a[y0:y1, x0:x1].reshape(-1, 3)
    vals, counts = np.unique(reg, axis=0, return_counts=True)
    order = np.argsort(-counts)[:n]
    return [(tuple(int(c) for c in vals[i]), int(counts[i])) for i in order]

# --- 1) math tokens: per-glyph clusters ---
def glyphs(x0, x1, y0, y1, label, thr=225):
    sub = a[y0:y1, x0:x1]
    ink = (sub[..., 0] < thr) | (sub[..., 1] < thr) | (sub[..., 2] < thr)
    colc = ink.sum(axis=0)
    segs = []
    s = None
    for i, v in enumerate(colc):
        if v > 0 and s is None: s = i
        elif v == 0 and s is not None: segs.append((s, i - 1)); s = None
    if s is not None: segs.append((s, len(colc) - 1))
    merged = []
    for w in segs:
        if merged and w[0] - merged[-1][1] <= 2: merged[-1] = (merged[-1][0], w[1])
        else: merged.append(list(w))
    print(f"{label}:")
    for (sx, ex) in merged:
        s2 = ink[:, sx:ex + 1]
        ys, _ = np.where(s2)
        print(f"  glyph x {sx+x0}..{ex+x0} (w {ex-sx+1}) y {ys.min()+y0}..{ys.max()+y0}")

glyphs(488, 556, 128, 162, "h-token (496..547)")
glyphs(600, 764, 128, 162, "w-token region (607..756?)")

# --- 2) L3 comma spacing ---
band = a[459:478, 300:480]
ink = (band[..., 0] < 200) | (band[..., 1] < 200) | (band[..., 2] < 200)
colc = ink.sum(axis=0)
segs = []
s = None
for i, v in enumerate(colc):
    if v > 0 and s is None: s = i
    elif v == 0 and s is not None: segs.append((s + 300, i - 1 + 300)); s = None
print("L3 x300..480 glyph runs:", segs)

# --- 3) gridline modals ---
print("g77 v-line modal (x179..182, y178..198):", exact_modal(179, 183, 178, 199, 5))
print("f33 v-line modal (x468..472, y252..308):", exact_modal(468, 473, 252, 309, 5))
print("o55 v-line modal (x660..664, y208..348):", exact_modal(660, 665, 208, 349, 5))
print("f33 h-line modal (y276..281 x445..525 minus glyphs):", exact_modal(444, 527, 278, 280, 5))

# --- 4) numeral sizes: digit ink heights ---
def digitbox(x0, x1, y0, y1, label):
    sub = a[y0:y1, x0:x1]
    ink = (sub[..., 0] < 120) & (sub[..., 1] < 120) & (sub[..., 2] < 120)
    ys, xs = np.where(ink)
    if len(xs):
        print(f"{label}: x {xs.min()+x0}..{xs.max()+x0} y {ys.min()+y0}..{ys.max()+y0} (h {ys.max()-ys.min()+1} w {xs.max()-xs.min()+1})")

digitbox(105, 136, 176, 200, "g77 r1c1 '0'")
digitbox(144, 176, 206, 230, "g77 r2c2 '1'")
digitbox(625, 660, 206, 230, "o55 r1c1 '1'")
digitbox(735, 775, 206, 230, "o55 r1c4 '0'")
digitbox(444, 470, 250, 270, "f33 r1c1 '0'")
digitbox(144, 176, 356, 380, "g77 r7c2 '0'")

# --- 5) bullet ring ---
sub = a[136:156, 106:130]
dark = sub.reshape(-1, 3)
dk = [tuple(p) for p in dark if sum(p) < 600]
print("bullet ring darkest:", sorted(dk, key=sum)[:6], "count", len(dk))
ink2 = (sub[..., 0] < 235) | (sub[..., 1] < 235) | (sub[..., 2] < 235)
ys, xs = np.where(ink2)
print(f"bullet ring bbox: x {xs.min()+106}..{xs.max()+106} y {ys.min()+136}..{ys.max()+136}")

# --- 6) note text color modal (dark px) ---
sub = a[400:505, 85:660]
darkm = sub[(sub[..., 0] + sub[..., 1] + sub[..., 2] < 260)]
print("note text dark px modal:", exact_modal(85, 660, 400, 505, 6) if len(darkm) == 0 else None)
vals, counts = np.unique(darkm // 8 * 8, axis=0, return_counts=True)
order = np.argsort(-counts)[:5]
print("note text dark modal:", [(tuple(int(c) for c in vals[i]), int(counts[i])) for i in order])

# --- 7) note box border strokes ---
print("notebox left border col profile x74..82 at y440:", [tuple(a[440, x]) for x in range(74, 83)])
print("notebox right border x668..678 at y440:", [tuple(a[440, x]) for x in range(668, 679)])
print("notebox top border rows y386..398 at x300:", [(y, tuple(a[y, 300])) for y in range(386, 399)])
print("notebox bottom border rows y505..517 at x300:", [(y, tuple(a[y, 300])) for y in range(505, 518)])

# --- 8) title font joint solve: advance 541 AND cap 24.5 (top 68, baseline 92.5) ---
TITLE = "Solution? Zero-padding! , Others !!"
fonts = {
    "Arial-Bold": "/usr/share/fonts/TTF/Arialbd.TTF",
    "Calibri-Bold": "/usr/share/fonts/TTF/calibrib.ttf",
    "Carlito-Bold": "/usr/share/fonts/carlito/Carlito-Bold.ttf",
    "LibSans-Bold": "/usr/share/fonts/liberation/LiberationSans-Bold.ttf",
    "LibSerif-Bold": "/usr/share/fonts/liberation/LiberationSerif-Bold.ttf",
    "DejaVuSans-Bold": "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
}
for name, path in fonts.items():
    try:
        best = None
        for size10 in range(280, 420):
            size = size10 / 10
            f = ImageFont.truetype(path, int(round(size * 4)))
            w = f.getlength(TITLE) / 4
            if best is None or abs(w - 541) < best[1]:
                asc, _ = f.getmetrics()
                # cap height proxy: measure 'S' bbox
                bb = f.getbbox("S")
                cap = (bb[3] - bb[1]) / 4
                best = (size, abs(w - 541), w, cap)
        print(f"TITLE {name}: size {best[0]} advance {best[2]:.0f} (off {best[1]:.0f}) capS {best[3]:.1f} (target ~24.5)")
    except OSError:
        print(name, "missing")

# --- 9) bullet sans joint solve using corrected word targets ---
words = [("For", 31), ("surround", 89), ("the", 32), ("image", 58), ("with", 43), ("and", 46), ("layers", 55), ("of", 20)]
for name, path in [("Arial", "/usr/share/fonts/TTF/Arial.TTF"),
                   ("Calibri", "/usr/share/fonts/TTF/calibri.ttf"),
                   ("Carlito", "/usr/share/fonts/carlito/Carlito-Regular.ttf"),
                   ("LibSans", "/usr/share/fonts/liberation/LiberationSans-Regular.ttf")]:
    offs = []
    for text, tgt in words:
        best = None
        for size10 in range(160, 280):
            size = size10 / 10
            f = ImageFont.truetype(path, int(round(size * 4)))
            w = f.getlength(text) / 4
            if best is None or abs(w - tgt) < best[1]:
                best = (size, abs(w - tgt))
        offs.append(best[0])
    print(f"BULLET {name}: per-word sizes {[round(o,1) for o in offs]} spread {max(offs)-min(offs):.1f}")
