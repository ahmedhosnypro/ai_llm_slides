#!/usr/bin/env python3
"""selfcheck_attempt_1.py — pre-judge self-checks for slide 002 attempt 1.

Compares the 150dpi render against PIL measurements of the original frame
(960x540, 1px=1pt; render scale = *150/72 = *2.0833). Adapted containment law:
content must sit inside the PLAYLIST panel (x 42..918, y 45..540 frame-px);
the black footer bar is measured content allowed to span x 38..921.
"""
from PIL import Image
from collections import Counter
import sys

RENDER = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/qa/slide002/render_1.png"
ORIG   = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_002.jpg"

r_im = Image.open(RENDER).convert("RGB"); rp = r_im.load(); RW, RH = r_im.size
o_im = Image.open(ORIG).convert("RGB");   op = o_im.load(); OW, OH = o_im.size
S = RH / 540.0  # render px per frame px
fails = []; notes = []

def isred(c): r,g,b=c; return r>120 and r>g+40 and r>b+40
def isblue(c): r,g,b=c; return b>110 and b>r+25 and b>g+25
def isblack(c): return sum(c[:3])<200
def to_f(v): return v / S  # render px -> frame px

# --- 1. FRAME CONTAINMENT (playlist panel x 42..918, y 45..540; bar exempt) ---
PANEL = (42, 918, 45, 540)
# collect non-white, non-chrome ink inside panel area of the render
ink_pts = []
for y in range(int(45*S), RH):
    for x in range(int(30*S), RW, 1):
        c = rp[x, y]
        if sum(c[:3]) < 720:  # non-white-ish
            fx, fy = to_f(x), to_f(y)
            ink_pts.append((fx, fy))
# containment: everything except the bar zone (fy>510) must be within panel+2px
out = [(x,y) for (x,y) in ink_pts if (x < PANEL[0]-2 or x > PANEL[1]+2) and y < 510]
if out:
    fails.append(f"containment: {len(out)} ink px outside panel (e.g. {out[:3]})")
else:
    notes.append("containment: all non-bar ink within panel x42..918 y45..540 (+2px tol)")
# bar zone: ink only within x 38..921
bar_out = [(x,y) for (x,y) in ink_pts if y >= 512 and (x < 36 or x > 923)]
if bar_out:
    fails.append(f"bar containment: {len(bar_out)} ink px outside x36..923")
else:
    notes.append("bar containment: bottom ink within x38..921 (measured extent)")

# --- 2. BLUE BOX geometry vs original ---
def box_bounds(pxl, W, H):
    blues = [(x,y) for y in range(int(120*S) if W>1000 else 120, int(500*S) if W>1000 else 500)
                     for x in range(W) if isblue(pxl[x,y])]
    ys = sorted(set(b[1] for b in blues)); xs_all = [b[0] for b in blues]
    from collections import Counter as C
    rows = C(b[1] for b in blues); cols = C(b[0] for b in blues)
    wr = sorted([y for y,n in rows.items() if n > (300*S if W>1000 else 300)])
    wc = sorted([x for x,n in cols.items() if n > (100*S if W>1000 else 100)])
    return (min(wc), max(wc), min(wr), max(wr))
rb = box_bounds(rp, RW, RH); ob = box_bounds(op, OW, OH)
for name, rv, ov in [("box x0", rb[0], ob[0]), ("box x1", rb[1], ob[1]),
                     ("box y0", rb[2], ob[2]), ("box y1", rb[3], ob[3])]:
    d = abs(to_f(rv) - ov)
    (notes if d <= 4 else fails).append(f"{name}: render {to_f(rv):.1f} vs orig {ov} (d={d:.1f}px)" + ("" if d<=4 else " > tol 4"))

# --- 3. BULLET BANDS (positions + pitch) ---
def bands(pxl, W, H, S_):
    bx0, bx1, by0, by1 = box_bounds(pxl, W, H)
    out = []
    cur = None
    for y in range(by0+int(4*S_), by1-int(3*S_)):
        n = sum(1 for x in range(bx0+int(8*S_), bx1-int(8*S_)) if isblue(pxl[x,y]))
        if n > 3*S_:
            if cur is None: cur = [y, y]
            else: cur[1] = y
        else:
            if cur: out.append(tuple(cur)); cur = None
    if cur: out.append(tuple(cur))
    res = []
    for b in out:
        xs = [x for y in range(b[0], b[1]+1) for x in range(bx0+int(8*S_), bx1-int(8*S_)) if isblue(pxl[x,y])]
        res.append((b[0], b[1], min(xs), max(xs)))
    return res
rbands = bands(rp, RW, RH, S); obands = bands(op, OW, OH, 1.0)
if len(rbands) != 4: fails.append(f"bands: render has {len(rbands)} bands, expected 4")
else:
    for i, ((ry0, ry1, rx0, rx1), (oy0, oy1, ox0, ox1)) in enumerate(zip(rbands, obands)):
        dt, db, dl, dr = abs(to_f(ry0)-oy0), abs(to_f(ry1)-oy1), abs(to_f(rx0)-ox0), abs(to_f(rx1)-ox1)
        msg = f"band{i+1}: top {to_f(ry0):.1f}/{oy0} bottom {to_f(ry1):.1f}/{oy1} left {to_f(rx0):.1f}/{ox0} right {to_f(rx1):.1f}/{ox1} (max d {max(dt,db,dl,dr):.1f}px)"
        (notes if max(dt, db, dl, dr) <= 4 else fails).append(msg)
    pitch_r = (to_f(rbands[3][0]) - to_f(rbands[0][0])) / 3
    pitch_o = (obands[3][0] - obands[0][0]) / 3
    (notes if abs(pitch_r - pitch_o) <= 2 else fails).append(
        f"line pitch: render {pitch_r:.1f} vs orig {pitch_o:.1f} frame-px (pinned 68)")

# --- 4. DOTS (black, near x 122) ---
def dots(pxl, W, H, S_):
    out = []
    for (y0, y1, *_ ) in (rbands if S_>1 else obands):
        yy0, yy1 = int(y0 - 6*S_), int(y1 + 6*S_)
        pts = [(x, y) for y in range(yy0, yy1+1) for x in range(int(110*S_), int(137*S_)) if sum(pxl[x,y][:3]) < 260]
        if pts:
            xs=[p[0] for p in pts]; ys=[p[1] for p in pts]
            out.append((sum(xs)/len(xs)/S_, sum(ys)/len(ys)/S_))
    return out
rdots = dots(rp, RW, RH, S); odots = dots(op, OW, OH, 1.0)
if len(rdots) != 4: fails.append(f"dots: {len(rdots)} found, expected 4")
else:
    for i, ((rx, ry), (ox, oy)) in enumerate(zip(rdots, odots)):
        d = max(abs(rx-ox), abs(ry-oy))
        (notes if d <= 4 else fails).append(f"dot{i+1}: render ({rx:.1f},{ry:.1f}) vs orig ({ox:.1f},{oy:.1f}) (d={d:.1f})")

# --- 5. TITLE (red ink band between panel top and box top) ---
def title_bbox(pxl, W, H, S_):
    y_lo, y_hi = int(50*S_), int(135*S_)
    pts = [(x,y) for y in range(y_lo, y_hi) for x in range(int(100*S_), int(880*S_)) if isred(pxl[x,y])]
    xs=[p[0] for p in pts]; ys=[p[1] for p in pts]
    return (min(xs)/S_, max(xs)/S_, min(ys)/S_, max(ys)/S_)
rt = title_bbox(rp, RW, RH, S); ot = title_bbox(op, OW, OH, 1.0)
td = max(abs(rt[i]-ot[i]) for i in range(4))
msg = (f"title: render x {rt[0]:.1f}..{rt[1]:.1f} y {rt[2]:.1f}..{rt[3]:.1f} vs orig x {ot[0]:.0f}..{ot[1]:.0f} y {ot[2]:.0f}..{ot[3]:.0f} (max d {td:.1f}px)")
(notes if td <= 4.5 else fails).append(msg)

# --- 6. BLACK BAR (top edge + extent) ---
def bar(pxl, W, H, S_):
    y = int(530*S_)
    xs = [x for x in range(W) if sum(pxl[x,y][:3]) < 200]
    top = None
    for yy in range(int(510*S_), int(530*S_)):
        if sum(pxl[int(480*S_), yy][:3]) < 200: top = yy; break
    return min(xs)/S_, max(xs)/S_, (top/S_ if top else None)
rbar = bar(rp, RW, RH, S); obar = bar(op, OW, OH, 1.0)
msg = f"bar: render x {rbar[0]:.1f}..{rbar[1]:.1f} top {rbar[2]} vs orig x {obar[0]}..{obar[1]} top {obar[2]} (bottom stroke kept visible by design, bottom edge 537.5 vs 539)"
if abs(rbar[0]-obar[0])<=4 and abs(rbar[1]-obar[1])<=4 and rbar[2] and abs(rbar[2]-obar[2])<=3: notes.append(msg)
else: fails.append(msg)

# --- 7. COLORS (modal) ---
def modal(pxl, pts): return Counter(pxl[p] for p in pts).most_common(1)[0][0]
r_title_c = modal(rp, [(x,y) for y in range(int(rt[2]*S), int(rt[3]*S)) for x in range(int(rt[0]*S), int(rt[1]*S)) if isred(rp[x,y]) and rp[x,y][0]>150])
r_band_c  = modal(rp, [(x,y) for y in range(int(rbands[0][0]), int(rbands[0][1])+1) for x in range(int(rbands[0][2]), int(rbands[0][3])) if isblue(rp[x,y])])
notes.append(f"render title modal {r_title_c} (orig ~192,0,0 -> C00000); render band modal {r_band_c} (orig ~(0,0,170) -> 0000AA)")

print("=== SELF-CHECK attempt 1 ===")
for n in notes: print("  ok:", n)
for f in fails: print("  FAIL:", f)
print("RESULT:", "PASS" if not fails else f"FAIL ({len(fails)})")
sys.exit(1 if fails else 0)
