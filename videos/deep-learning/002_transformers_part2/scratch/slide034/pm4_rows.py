#!/usr/bin/env python3
"""pm4_rows.py — slide 034 row detail: lane extents, per-box edges, digit/label ink,
slant, dots, gap fill + emptiness proof, N-2/N-1 token form.

Output: pm4_rows_output.txt
"""
import numpy as np
from PIL import Image
import os

HERE = os.path.dirname(os.path.abspath(__file__))
FR = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_034.jpg"
OUT = os.path.join(HERE, "pm4_rows_output.txt")

AX, SX, SY = 17.891, 0.962062, 0.955556
def FX(fx): return (fx - AX) / SX
def FY(fy): return fy / SY

img = np.asarray(Image.open(FR).convert("RGB")).astype(int)
r, g, b = img[..., 0], img[..., 1], img[..., 2]
s = r + g + b
lines = []
def say(sx_=""):
    lines.append(sx_)
    print(sx_)

def edges_from_columns(colcount, thresh, min_gap=4):
    """Cluster columns with count>=thresh into edge positions (weighted centroids)."""
    cols = np.where(colcount >= thresh)[0]
    if len(cols) == 0:
        return []
    groups = [[cols[0]]]
    for c in cols[1:]:
        if c - groups[-1][-1] <= min_gap:
            groups[-1].append(c)
        else:
            groups.append([c])
    out = []
    for gr in groups:
        w = colcount[gr].astype(float)
        out.append(float((np.array(gr) * w).sum() / w.sum()))
    return out

say("== TOKEN ROW (row 1) ==")
# border class: dark navy-violet. Box borders span ~24 rows continuously; digit ink
# spans <=16. Require count>=20 over the y143..168 band to isolate BORDER columns.
bb_band = (s < 640) & (b - r > -10) & (b > 80)
band = bb_band[143:168, 160:895]
colcount = band.sum(axis=0)
edges = [e + 160 for e in edges_from_columns(colcount, 20)]
edges = [e for e in edges if e >= 176]  # drop the lane's left vertical dash column
say(f"  box-edge columns (y142..170, count>=12): {[round(e,1) for e in edges]}")
if len(edges) >= 2:
    pairs = [(edges[i], edges[i + 1]) for i in range(0, len(edges) - 1, 2)]
    say(f"  -> {len(pairs)} box x-pairs: {[(round(a,1), round(bb_,1)) for a, bb_ in pairs]}")
    centers = [(a + b_) / 2 for a, b_ in pairs]
    say(f"  centers: {[round(c,1) for c in centers]}")
    if len(centers) >= 6:
        xs = np.array(centers[:6])
        k = np.polyfit(np.arange(6), xs, 1)
        say(f"  linear fit over boxes 1-6: center0={k[1]:.1f} pitch={k[0]:.2f}")
    rows = bb_band[135:180, 178:890].sum(axis=1)
    say("  y-profile (x178..890): " + "  ".join(f"{135+i}:{v}" for i, v in enumerate(rows) if v > 25))

# digit ink per box (first 6 boxes + last 2)
say("\n  digit ink per box (dark sum<430, inside each box, y142..170):")
digit_data = []
for i, (a, b_) in enumerate(pairs):
    win = s[142:170, int(a) + 3:int(b_) - 3]
    m = win < 430
    ys, xs = np.where(m)
    if len(xs) == 0:
        say(f"    box{i+1}: no ink")
        continue
    x0, x1 = xs.min() + a + 3, xs.max() + a + 3
    y0, y1 = ys.min() + 142, ys.max() + 142
    cx = (x0 + x1) / 2
    box_cx = (a + b_) / 2
    digit_data.append((i + 1, x0, x1, y0, y1, cx, box_cx))
    say(f"    box{i+1}: ink x[{x0},{x1}] y[{y0},{y1}] h={y1-y0+1} inkC={cx:.1f} boxC={box_cx:.1f} dx={cx-box_cx:+.1f}")

# slant estimate on each digit: top-half vs bottom-half ink centroid dx
say("\n  italic slant (inkC top-half minus bottom-half, frame px):")
for (i, x0, x1, y0, y1, cx, box_cx) in digit_data:
    x0, x1, y0, y1 = int(x0), int(x1), int(y0), int(y1)
    if y1 - y0 < 8:
        continue
    win = s[y0:y1 + 1, x0:x1 + 1] < 430
    h = y1 - y0 + 1
    mid = h // 2
    top = win[:mid, :]
    bot = win[mid:, :]
    if top.sum() and bot.sum():
        xs_ = np.arange(x0, x1 + 1, dtype=float)
        tx = (top * xs_[None, :])[top].sum() / top.sum()
        bx = (bot * xs_[None, :])[bot].sum() / bot.sum()
        say(f"    box{i}: topC-x {tx:.1f} bottomC-x {bx:.1f} shift {tx-bx:+.1f}px over h={h}")

# dots
say("\n  dots in gap (x612..730, y144..172): dot-class = sum<610 & b>r")
dotm = (s < 610) & (b > r)
win = dotm[144:172, 612:730]
colc = win.sum(axis=0)
cols = np.where(colc > 0)[0]
groups = []
if len(cols):
    groups = [[cols[0]]]
    for c in cols[1:]:
        if c - groups[-1][-1] <= 2:
            groups[-1].append(c)
        else:
            groups.append([c])
dcenters = []
for gr in groups:
    w = colc[gr].astype(float)
    cx = (np.array(gr) * w).sum() / w.sum() + 612
    sub = win[:, gr]
    ys = np.where(sub.any(axis=1))[0]
    dcenters.append(cx)
    say(f"    dot at x~{cx:.1f} y[{ys.min()+144},{ys.max()+144}] w={len(gr)} h={ys.max()-ys.min()+1}")
say(f"  dot centers: {[round(c,1) for c in dcenters]}  pitch: {[round(dcenters[i+1]-dcenters[i],1) for i in range(len(dcenters)-1)] if len(dcenters)>1 else 'n/a'}")
# gap fill tint vs lane fill (dot-free strips)
gap_px = img[150:160, 615:624].reshape(-1, 3)   # left of dot 1
lane_px = img[150:160, 340:358].reshape(-1, 3)
say(f"  gap fill mean (x615..624, dot-free): #%02X%02X%02X   mid-lane fill mean (x340..358): #%02X%02X%02X" %
    (*gap_px.mean(axis=0).astype(int), *lane_px.mean(axis=0).astype(int)))

say("\n== VECTOR ROW (row 3) ==")
vb_band = (s < 640) & (r - b > 5) & (r > 120)
band = vb_band[297:324, 160:895]
colcount = band.sum(axis=0)
edges = [e + 160 for e in edges_from_columns(colcount, 18)]
say(f"  box-edge columns (y296..326, count>=12): {[round(e,1) for e in edges]}")
if len(edges) >= 2:
    pairs = [(edges[i], edges[i + 1]) for i in range(0, len(edges) - 1, 2)]
    say(f"  -> {len(pairs)} box x-pairs: {[(round(a,1), round(bb_,1)) for a, bb_ in pairs]}")
    centers = [(a + b_) / 2 for a, b_ in pairs]
    say(f"  centers: {[round(c,1) for c in centers]}")
rows = vb_band[288:334, 178:890].sum(axis=1)
say("  y-profile (x178..890): " + "  ".join(f"{288+i}:{v}" for i, v in enumerate(rows) if v > 25))

say("\n  vector label ink per box (dark sum<430, y296..326):")
for i, (a, b_) in enumerate(pairs):
    win = s[296:326, int(a) + 3:int(b_) - 3]
    m = win < 430
    ys, xs = np.where(m)
    if len(xs) == 0:
        say(f"    box{i+1}: no ink")
        continue
    x0, x1 = xs.min() + a + 3, xs.max() + a + 3
    y0, y1 = ys.min() + 296, ys.max() + 296
    say(f"    box{i+1}: ink x[{x0},{x1}] y[{y0},{y1}] w={x1-x0+1} h={y1-y0+1} inkC={(x0+x1)/2:.1f} boxC={(a+b_)/2:.1f} dx={(x0+x1)/2-(a+b_)/2:+.1f}")

# N-2/N-1 token form (token row boxes 7/8): ink rows of the whole label vs a
# subscripted form (which would show a step down). Compare ink y-extent by x.
say("\n  N-2/N-1 form check (token boxes 7+8): per-column ink y-center")
for (a, b_), lab in [(pairs[6], "N-2"), (pairs[7], "N-1")]:
    win = s[142:172, int(a) + 3:int(b_) - 3] < 430
    cols = np.where(win.any(axis=0))[0]
    if len(cols):
        seg = cols.reshape(-1, 1)
        yc = np.array([np.where(win[:, c])[0].mean() for c in cols])
        say(f"    {lab}: ink cols {cols.min()+a+3}..{cols.max()+a+3}; y-center first-quarter {yc[:max(1,len(yc)//4)].mean()+142:.1f}, last-quarter {yc[-max(1,len(yc)//4):].mean()+142:.1f} (subscript would drop the tail)")

# vector-row gap emptiness (excluding dash rows)
say("\n  vector-gap emptiness: dark px (sum<620) in x612..728, y296..324:")
win = s[296:324, 612:728] < 620
say(f"    count={int(win.sum())}")
if win.sum():
    ys, xs = np.where(win)
    say(f"    bbox x[{xs.min()+612},{xs.max()+612}] y[{ys.min()+296},{ys.max()+296}]")

# vector box interior vs lane fill (is there a distinct box fill?) — light px only
say("\n  fills (light px sum>500 only): lane3 gap vs inside-box P1 vs token box1 vs token lane:")
lane_px = img[298:320, 630:706].reshape(-1, 3)
lane_px = lane_px[lane_px.sum(axis=1) > 500]
box_px = img[304:318, 253:262].reshape(-1, 3)   # P1 left strip, label-free
box_px = box_px[box_px.sum(axis=1) > 500]
tok_px = img[147:162, 185:210].reshape(-1, 3)   # token box1 left strip, digit-free
tok_px = tok_px[tok_px.sum(axis=1) > 500]
tl_px = img[147:162, 340:358].reshape(-1, 3)    # token lane mid strip
tl_px = tl_px[tl_px.sum(axis=1) > 500]
say(f"    lane3 fill      #%02X%02X%02X" % tuple(lane_px.mean(axis=0).astype(int)))
say(f"    vec box P1 fill #%02X%02X%02X" % tuple(box_px.mean(axis=0).astype(int)))
say(f"    tok box1 fill   #%02X%02X%02X" % tuple(tok_px.mean(axis=0).astype(int)))
say(f"    token lane fill #%02X%02X%02X" % tuple(tl_px.mean(axis=0).astype(int)))

# lane dash x extents
say("\n== LANE DASH EXTENTS ==")
navy = (s < 620) & (b - r > 20)
for label, y0, y1, m in [("lane1 top dash", 134, 139, navy), ("lane1 bottom dash", 172, 177, navy)]:
    win = m[y0:y1, 150:905]
    xs = np.where(win.any(axis=0))[0]
    if len(xs):
        say(f"  {label}: x[{xs.min()+150},{xs.max()+150}] npx={int(win.sum())}")
teal = (s < 640) & (np.abs(r - 95) < 50) & (np.abs(g - 115) < 50) & (np.abs(b - 130) < 50) & (b >= r)
for label, y0, y1 in [("lane3 top dash", 288, 293), ("lane3 bottom dash", 326, 331)]:
    win = teal[y0:y1, 150:905]
    xs = np.where(win.any(axis=0))[0]
    if len(xs):
        say(f"  {label}: x[{xs.min()+150},{xs.max()+150}] npx={int(win.sum())}")
# vertical dash columns at lane left/right edges
say("  lane1 vertical dashes (left/right cols, y138..172):")
for x0, x1 in [(160, 175), (880, 895)]:
    win = navy[138:172, x0:x1]
    cols = np.where(win.sum(axis=0) > 4)[0]
    say(f"    x{x0}..{x1}: cols {[int(c)+x0 for c in cols]}")
say("  lane3 vertical dashes (left/right cols, y292..326):")
for x0, x1 in [(160, 175), (880, 895)]:
    win = teal[292:326, x0:x1]
    cols = np.where(win.sum(axis=0) > 4)[0]
    say(f"    x{x0}..{x1}: cols {[int(c)+x0 for c in cols]}")

with open(OUT, "w") as f:
    f.write("\n".join(lines) + "\n")
print(f"\nwrote {OUT}")
