#!/usr/bin/env python3
"""slide007 pre-judge self-check (attempt 1) — 150dpi render (2001x1125).
Scale: frame(960x540, 1px=1pt) -> render x2.0844. Checks:
  A inheritance diff vs certified parent render (only delta zones may differ)
  B subtitle presence/geometry   C callout box fill/border
  D 4 text lines + pitch + underline rows   E containment/wrap
  F connector ink along traced path   G font-size calibration (ink widths)
"""
from PIL import Image
import numpy as np
import sys

ROOT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1"
REN = f"{ROOT}/recreated_pptx/qa/slide007/render_1.png"
PAR = f"{ROOT}/recreated_pptx/qa/slide006/render_1.png"
K = 2001 / 960.0

img = np.asarray(Image.open(REN).convert("RGB")).astype(int)
par = np.asarray(Image.open(PAR).convert("RGB")).astype(int)
H, W = img.shape[:2]
print(f"render {W}x{H}, k={K:.4f}")
fails = []

def check(name, ok, detail=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {name} {detail}")
    if not ok:
        fails.append(name)

# ---- A: inheritance diff ----
print("A) inheritance diff vs certified parent render:")
d = np.abs(img - par).sum(axis=2)
mask = d > 45
ys, xs = np.nonzero(mask)
if len(ys) == 0:
    check("A0 diff exists (badge/subtitle/callout/connector)", False, "renders identical - delta missing?")
else:
    # cluster into bands
    rows = np.nonzero(mask.sum(axis=1) > 2)[0]
    bands = []
    start = prev = rows[0]
    for r in rows[1:]:
        if r - prev > 6:
            bands.append((start, prev)); start = r
        prev = r
    bands.append((start, prev))
    # allowed zones (render px, generous)
    zones = [
        ("badge",      1790, 1935,  95, 205),
        ("subtitle",    740, 1180, 160, 250),
        ("callout+connector", 80, 1040, 340, 600),
    ]
    ok = True; detail = []
    for (y0, y1) in bands:
        sub = mask[y0:y1 + 1]
        cols = np.nonzero(sub.sum(axis=0) > 0)[0]
        x0, x1 = cols.min(), cols.max()
        hit = [n for (n, zx0, zx1, zy0, zy1) in zones if x0 >= zx0 and x1 <= zx1 and y0 >= zy0 and y1 <= zy1]
        detail.append(f"band y{y0}-{y1} x{x0}-{x1}:{hit[0] if hit else 'OUTSIDE'}")
        if not hit: ok = False
    check("A1 all diff bands inside delta zones", ok, "; ".join(detail))
    n_out = sum(1 for (y0, y1) in bands)
    print(f"   ({len(bands)} diff bands, {int(mask.sum())} px)")

# ---- B: subtitle ----
print("B) subtitle '(Challenges)':")
# window excludes title baseline rows (title ink ends ~y169 render; subtitle starts 181)
win = img[176:250, 760:1160]
ink = win.sum(axis=2) < 430
ys2, xs2 = np.nonzero(ink)
if len(ys2) < 40:
    check("B1 subtitle ink present", False, f"n={len(ys2)}")
else:
    bx = (760 + xs2.min(), 176 + ys2.min(), 760 + xs2.max(), 176 + ys2.max())
    tw = 329
    check("B1 subtitle ink present", True, f"bbox x{bx[0]}..{bx[2]} y{bx[1]}..{bx[3]} n={len(ys2)}")
    check("B2 width ~329±40", abs((bx[2] - bx[0]) - tw) <= 40, f"w={bx[2]-bx[0]}")
    c = (bx[0] + bx[2]) / 2
    check("B3 center ~947±12", abs(c - 947) <= 12, f"cx={c:.0f}")
    check("B4 v-center ~206±12", abs((bx[1] + bx[3]) / 2 - 206) <= 12, f"cy={(bx[1]+bx[3])/2:.0f}")

# ---- C: callout box ----
print("C) callout box (x92..949 y354..557):")
fill = img[400, 500]  # inside box, between text lines? choose y=368 x=500 (above L1 caps 386)
print("   fill sample @ (500,368):", img[368, 500].tolist())
f = img[368, 500]
check("C1 fill ~DFFFFC(223,255,252)", all(abs(int(f[i]) - v) <= 28 for i, v in enumerate((223, 255, 252))), str(f.tolist()))
# border presence: scan box mid-rows/cols for border-colored strokes
rowy = 455
row = img[rowy, 80:1000]
edge = np.nonzero(np.abs(row - np.array([171, 184, 203])).sum(axis=1) < 150)[0]
check("C2 left+right border strokes on mid row", len(edge) >= 2 and edge.min() < 100 and edge.max() > 860, f"x {(80+edge.min()) if len(edge) else -1}..{(80+edge.max()) if len(edge) else -1}")
colx = 500
col = img[340:580, colx]
edgev = np.nonzero(np.abs(col - np.array([171, 184, 203])).sum(axis=1) < 150)[0]
check("C3 top+bottom border strokes on mid col", len(edgev) >= 2 and edgev.min() < 25 and edgev.max() > 200, f"y {(340+edgev.min()) if len(edgev) else -1}..{(340+edgev.max()) if len(edgev) else -1}")

# ---- D: text lines ----
print("D) 4 text lines (target centers y399/438/475/514, pitch 37.5):")
sub = img[350:570, 110:940]
inkd = sub.sum(axis=2) < 400
rows = inkd.sum(axis=1)
bands = []
cur = None
for i, v in enumerate(rows):
    if v > 2:
        if cur and (350 + i) - cur[1] <= 4:
            cur[1] = 350 + i; cur[2] += int(v)
        else:
            if cur: bands.append(cur)
            cur = [350 + i, 350 + i, int(v)]
if cur: bands.append(cur)
print(f"   bands: {[(b[0], b[1]) for b in bands]}")
tcent = [399, 438, 475, 514]
if len(bands) != 4:
    check("D1 exactly 4 line bands", False, f"got {len(bands)}")
else:
    check("D1 exactly 4 line bands", True)
    cents = [(b[0] + b[1]) / 2 for b in bands]
    ok = all(abs(c - t) <= 9 for c, t in zip(cents, tcent))
    check("D2 line centers within ±9", ok, str([f"{c:.0f}" for c in cents]))
    pitch = (cents[-1] - cents[0]) / 3
    check("D3 pitch ~37.5±3", abs(pitch - 37.5) <= 3, f"{pitch:.1f}")
    # widths
    tw = [242, 680, 790, 396]
    ws = []
    for (b0, b1, _) in bands:
        m = inkd[b0 - 350:b1 - 350 + 1]
        xs3 = np.nonzero(m.sum(axis=0) > 0)[0]
        ws.append(xs3.max() - xs3.min())
    print(f"   widths: {ws} targets {tw}")
    check("D4 ink widths within ±12%", all(abs(w - t) <= 0.12 * t for w, t in zip(ws, tw)), str(ws))
    # underlines: longest consecutive dark run in the bottom 6 rows of bands 1,3,4
    def uline(y0, y1, x0t, x1t):
        best = None
        for yy in range(int(y0), int(y1) + 1):
            seg = img[yy, 92:950]
            dk = (seg.sum(axis=1) < 480).astype(int)
            bestlen, cur, bs = 0, 0, None
            for i, v in enumerate(dk):
                if v:
                    if cur == 0: s0 = i
                    cur += 1
                    if cur > bestlen: bestlen, bs, be = cur, s0, i
                else:
                    cur = 0
            if bestlen > 60 and (best is None or bestlen > best[0]):
                best = (bestlen, yy, 92 + bs, 92 + be)
        return best
    u1 = uline(bands[0][1] - 5, bands[0][1] + 2, 398, 642)
    check("D5 L1 underline row below band1", u1 is not None and abs((u1[2]+u1[3])/2 - (398+642)/2) < 45, str(u1))
    u3 = uline(bands[2][1] - 5, bands[2][1] + 2, 563, 921)
    check("D6 L3 underline (right-shifted, center ~742)", u3 is not None and abs((u3[2]+u3[3])/2 - 742) < 60, str(u3))
    u4 = uline(bands[3][1] - 5, bands[3][1] + 2, 396, 717)
    check("D7 L4 underline (center ~556)", u4 is not None and abs((u4[2]+u4[3])/2 - 556) < 50, str(u4))
    # L2 must have NO underline: no long run in bottom rows of band2
    u2 = uline(bands[1][1] - 3, bands[1][1] + 2, 173, 857)
    check("D8 L2 no underline", u2 is None, str(u2))

# ---- E: containment / wrap ----
print("E) containment:")
# LEFT margin x82..90: only the house panel border (RED r>140,g<80) may be dark there
# (frame: box left edge x44 sits 1px right of the house border x42..43 — adjacent by design)
bad_left = 0
for yy in range(348, 566):
    for xx in range(82, 91):
        p = img[yy, xx]
        if p.sum() < 420 and not (p[0] > 140 and p[1] < 80):
            bad_left += 1
# RIGHT margin x954..962 (connector zone x>=963 excluded; border AA ends ~x952)
out_r = 0
for yy in range(348, 566):
    for xx in range(954, 963):
        if img[yy, xx].sum() < 420:
            out_r += 1
# and above/below the box (y<347 or y>564) within box x-range, excluding subtitle/title rows
out_v = 0
for yy in list(range(340, 348)) + list(range(565, 600)):
    for xx in range(92, 950):
        if img[yy, xx].sum() < 420:
            out_v += 1
check("E1 no non-chrome ink left of box / none right of box", bad_left < 10 and out_r < 10, f"left={bad_left} right={out_r}")
check("E1b no ink above/below box (border rows +4px)", out_v < 25, f"n={out_v}")
# box inside house panel content area
check("E2 box inside house frame", 92 > 42 * K - 2 and 949 < 918 * K + 2 and 354 > 45 * K and 557 < 539 * K, "")

# ---- F: connector ----
print("F) connector (965,392)->(994,582):")
hits = 0; miss = []
for t in np.linspace(0.08, 0.92, 12):
    x = 965 + t * (994 - 965); y = 392 + t * (582 - 392)
    x0, x1 = int(x) - 5, int(x) + 6
    seg = img[int(y) - 5:int(y) + 6, x0:x1]
    if (seg.sum(axis=2) < 600).any():
        hits += 1
    else:
        miss.append((int(x), int(y)))
check("F1 ink along connector path (12 samples)", hits >= 10, f"hits={hits} miss={miss}")

# ---- G: colors of text ink ----
print("G) ink color:")
tzone = img[int(390):int(410), 400:640].reshape(-1, 3)
td = tzone[tzone.sum(axis=1) < 250]
if len(td):
    med = np.median(td, axis=0)
    check("G1 text ink dark blue ~ (0,0,102)±60", med[0] < 70 and med[1] < 70 and 60 < med[2] < 190, str(med.round(0).tolist()))
else:
    check("G1 text ink present", False)

print()
if fails:
    print("FAILED:", fails)
    sys.exit(1)
print("ALL SELF-CHECKS PASS")
