#!/usr/bin/env python3
"""slide_024 spot-verification of contested measurements (5th round, builder resume).
Banks measure_spot_out.txt. All coords in 960x540 frame px (1px = 1pt)."""
import numpy as np
from PIL import Image

IM = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_024.jpg").convert("RGB")
A = np.asarray(IM).astype(int)
H, W = A.shape[:2]
BEIGE = np.array([218, 208, 196])
GRAYP = np.array([231, 233, 230])

def P(*a):
    print(*a)

def near(px, ref, tol):
    return all(abs(int(px[i]) - ref[i]) <= tol for i in range(3))

# 1. beige panel edges (strict beige, tol 18)
P("== 1. beige panel edges ==")
xs = [x for x in range(40, 930) if near(A[300, x], BEIGE, 18) or near(A[212, x], BEIGE, 18)]
P(" panel x extent (rows 212/300):", min(xs), max(xs))
ys_top = [y for y in range(140, 200) if near(A[y, 350], BEIGE, 18) or near(A[y, 500], BEIGE, 18)]
P(" panel top candidates x350/500:", min(ys_top), max(ys_top))
ys_bot = [y for y in range(395, 445) if near(A[y, 350], BEIGE, 18) or near(A[y, 500], BEIGE, 18)]
P(" panel bottom candidates x350/500:", min(ys_bot), max(ys_bot))
for y in range(155, 175):
    if near(A[y, 500], BEIGE, 18):
        P(" first beige row at x500:", y); break
for y in range(440, 400, -1):
    if near(A[y, 500], BEIGE, 18):
        P(" last beige row at x500:", y); break

# 2. error bar
P("== 2. error bar ==")
red = ((A[:, :, 0] > 120) & (A[:, :, 1] < 60) & (A[:, :, 2] < 60))
sub = red[150:430, 780:830]
yy, xx = np.nonzero(sub)
P(" bar bbox x", 780 + xx.min(), 780 + xx.max(), " y", 150 + yy.min(), 150 + yy.max())
P(" fill modal:", {tuple(v): int(c) for v, c in zip(*np.unique(A[200:380, 800:815].reshape(-1, 3), axis=0, return_counts=True))} if False else np.unique(A[200:380, 800:815].reshape(-1, 3), axis=0, return_counts=True)[0][np.argsort(np.unique(A[200:380, 800:815].reshape(-1, 3), axis=0, return_counts=True)[1])[-3:]])

# 3. output boxes: dark+white ink per row band (x720..792, exclude error bar)
P("== 3. output boxes (x720..792) ==")
dark = (A[:, :, 0] < 110) & (A[:, :, 1] < 110) & (A[:, :, 2] < 110)
white = (A[:, :, 0] > 235) & (A[:, :, 1] > 235) & (A[:, :, 2] > 225)
for tag, y0, y1 in [("r1", 195, 240), ("r2", 270, 315), ("r3", 350, 395)]:
    d = dark[y0:y1, 720:792]; w = white[y0:y1, 720:792]
    dy, dx = np.nonzero(d); wy, wx = np.nonzero(w)
    if len(dy):
        P(f" {tag} dark y {y0+dy.min()}..{y0+dy.max()} x {720+dx.min()}..{720+dx.max()} n={len(dy)} | white n={len(wy)}", 
          f"white y {y0+wy.min()}..{y0+wy.max()} x {720+wx.min()}..{720+wx.max()}" if len(wy) else "")

# 4. col5 neuron + col1 outline/fill
P("== 4. col5/col1 neurons ==")
sub = A[266:306, 655:700]
m = (np.abs(sub - BEIGE).sum(axis=2) > 60) & (np.abs(sub - GRAYP).sum(axis=2) > 60)
yy, xx = np.nonzero(m)
P(" col5 r2 ink bbox x", 655+xx.min(), 655+xx.max(), "y", 266+yy.min(), 266+yy.max())
P(" col5 fill samples (677,285):", tuple(A[285, 677]), "(670,280):", tuple(A[280, 670]), "(684,290):", tuple(A[290, 684]))
P(" col5 edge samples (661,285):", tuple(A[285, 661]), "(693,285):", tuple(A[285, 693]), "(677,266):", tuple(A[266, 677]))
P(" col1 fill samples (170,200):", tuple(A[200, 170]), "(150,212):", tuple(A[212, 150]), "(178,212):", tuple(A[212, 178]))
P(" col1 edge (140,212):", tuple(A[212, 140]), "(160,192):", tuple(A[192, 160]), "(180,212):", tuple(A[212, 180]))
P(" col2 fill (261,205):", tuple(A[205, 261]), "(255,218):", tuple(A[218, 255]))

# 5. rings before col5 + after col1 (stroke clusters, scan bands clear of O labels)
P("== 5. rings ==")
for tag, cy, y0, y1 in [("pre5 r1", 212, 213, 221), ("pre5 r2", 285, 281, 290), ("pre5 r3", 366, 362, 371),
                        ("post1 r1", 212, 213, 221), ("post1 r3", 366, 362, 371)]:
    x0, x1 = (595, 660) if "pre5" in tag else (185, 245)
    band = A[y0:y1, x0:x1]
    m = (np.abs(band - BEIGE).sum(axis=2) > 55)
    cols = np.nonzero(m.any(axis=0))[0]
    if len(cols):
        groups, start = [], cols[0]
        for i in range(1, len(cols)):
            if cols[i] != cols[i-1] + 1:
                groups.append((x0+start, x0+cols[i-1])); start = cols[i]
        groups.append((x0+start, x0+cols[-1]))
        P(f" {tag} y{y0}..{y1} stroke col-groups:", groups)

# 6. links: gray ink presence
P("== 6. links ==")
def ink_runs(y, x0, x1, tol=22):
    row = A[y, x0:x1]
    m = (np.abs(row - BEIGE).sum(axis=1) > tol) & (np.abs(row - GRAYP).sum(axis=1) > tol)
    runs, s = [], None
    for i, v in enumerate(m):
        if v and s is None: s = i
        if not v and s is not None: runs.append((x0+s, x0+i-1)); s = None
    if s is not None: runs.append((x0+s, x0+len(m)-1))
    return runs
P(" col4-col5 gap y212:", ink_runs(212, 610, 660), " y213:", ink_runs(213, 610, 660))
P(" col4-col5 gap y285:", ink_runs(285, 610, 660), " y366:", ink_runs(366, 610, 660))
P(" col1-col2 gap y212 x181..242:", ink_runs(212, 181, 243))
for xx in (95, 115, 135):
    colm = (np.abs(A[240:340, xx] - BEIGE).sum(axis=1) > 25) & (np.abs(A[240:340, xx] - GRAYP).sum(axis=1) > 25)
    rows = np.nonzero(colm)[0] + 240
    P(f" fan col x{xx} ink rows:", list(rows))

# 7. block arrow i profile
P("== 7. block arrow i (x235..300, y383..436) ==")
for y in range(383, 437, 4):
    P(f"  y{y}:", ink_runs(y, 235, 302, tol=15))

# 8. magenta boxes text bands + arrowhead
P("== 8. magenta boxes ==")
for tag, x0, x1, y0, y1 in [("IS", 60, 145, 120, 165), ("SL", 815, 895, 118, 160)]:
    band = A[y0:y1, x0:x1]
    dk = (band.sum(axis=2) < 330)
    rows = [y0+i for i in range(y1-y0) if dk[i].sum() >= 2]
    P(f" {tag} dark-text rows:", rows)
P(" arrowhead zone ink (x120..140, y130..152):", ink_runs(141, 118, 142, tol=30), "| y135:", ink_runs(135, 118, 142, tol=30), "| y148:", ink_runs(148, 118, 142, tol=30))

# 9. callout nxt rows + borders
P("== 9. callouts ==")
for tag, x0, x1 in [("prev", 215, 315), ("cur", 378, 478), ("nxt", 552, 635)]:
    band = A[415:470, x0:x1]
    dk = (np.abs(band - GRAYP).sum(axis=2) > 40)
    rows = [415+i for i in range(55) if dk[i].sum() >= 3]
    P(f" {tag} ink rows:", rows[:3], "...", rows[-3:] if len(rows) > 3 else "")

# 10. class boxes fill + text
P("== 10. class boxes ==")
P(" fill modal r1:", [tuple(v) for v in np.unique(A[206:218, 830:885].reshape(-1, 3), axis=0, return_counts=True)[0][np.argsort(np.unique(A[206:218, 830:885].reshape(-1, 3), axis=0, return_counts=True)[1])[-2:]]])
P(" r1 dark text rows:", [y for y in range(200, 225) if (A[y, 828:888].sum(axis=1) < 330).sum() >= 2])

# 11. title red bbox
P("== 11. title ==")
redm = (A[:, :, 0] > 120) & (A[:, :, 1] < 90) & (A[:, :, 2] < 90) & (np.arange(W)[None, :] < 700) & (np.arange(H)[:, None] < 110)
yy, xx = np.nonzero(redm[50:110, 250:720])
P(" title ink x", 250+xx.min(), 250+xx.max(), " y", 50+yy.min(), 50+yy.max())

# 12. O labels: red text rows per window
P("== 12. O labels ==")
redm2 = (A[:, :, 0] > 130) & (A[:, :, 1] < 100) & (A[:, :, 2] < 100)
for tag, x0, x1, y0, y1 in [("Oi r1", 278, 302, 188, 220), ("Oi r2", 275, 300, 258, 292), ("Oi r3", 272, 297, 336, 370),
                            ("Oj r1", 443, 470, 188, 220), ("Oj r2", 441, 468, 258, 292), ("Oj r3", 441, 468, 340, 370),
                            ("Ok r1", 606, 634, 188, 216), ("Ok r2", 604, 631, 258, 285), ("Ok r3", 604, 631, 338, 365)]:
    band = redm2[y0:y1, x0:x1]
    rows = [y0+i for i in range(y1-y0) if band[i].sum() >= 2]
    cols = np.nonzero(band.any(axis=0))[0]
    P(f" {tag}: rows {rows[0]}..{rows[-1]}" if rows else f" {tag}: none", f"x {x0+cols.min()}..{x0+cols.max()}" if len(cols) else "")

# 13. Net label arrows
P("== 13. Net arrows ==")
for tag, x0, x1, y0, y1 in [("Net_i", 200, 260, 168, 196), ("Net_j", 365, 425, 168, 196), ("Net_k", 528, 592, 168, 196)]:
    band = redm2[y0:y1, x0:x1]
    yy2, xx2 = np.nonzero(band)
    if len(yy2):
        P(f" {tag} red ink x {x0+xx2.min()}..{x0+xx2.max()} y {y0+yy2.min()}..{y0+yy2.max()}")

# 14. weight labels: blue ink bboxes (refined)
P("== 14. weight labels ==")
blum = (A[:, :, 2] > 90) & (A[:, :, 2] - A[:, :, 0] > 40) & (A[:, :, 1] < A[:, :, 2])
for tag, x0, x1, y0, y1 in [("A1", 310, 370, 186, 218), ("A2", 306, 356, 218, 252), ("A3", 314, 358, 252, 294),
                            ("B1", 474, 526, 188, 218), ("B2", 476, 524, 218, 256), ("B3", 478, 520, 252, 294)]:
    band = blum[y0:y1, x0:x1]
    yy2, xx2 = np.nonzero(band)
    if len(yy2):
        P(f" {tag}: x {x0+xx2.min()}..{x0+xx2.max()} y {y0+yy2.min()}..{y0+yy2.max()} n={len(yy2)}")
    else:
        P(f" {tag}: none")

# 15. magenta dots
P("== 15. dots ==")
mag = (A[:, :, 0] > 140) & (A[:, :, 2] > 140) & (A[:, :, 1] < 110)
sub = mag[240:340, 65:95]
yy2, xx2 = np.nonzero(sub)
rows = sorted(set(240 + v for v in yy2))
groups, s, prev = [], None, None
for r in rows:
    if s is None: s = r
    elif r != prev + 1: groups.append((s, prev)); s = r
    prev = r
if s is not None: groups.append((s, prev))
P(" dot row-groups:", groups, " x extent:", 65+xx2.min(), 65+xx2.max())

# 16. extra probes: output box fill/border, col1 border, arrow fills, glyphs, dash
P("== 16. extra ==")
P(" outbox r1 interior (724,212):", tuple(A[212, 724]), "(780,212):", tuple(A[212, 780]),
  "(724,285):", tuple(A[285, 724]), "(780,285):", tuple(A[285, 780]), "(750,209):", tuple(A[209, 750]))
P(" outbox top edge y205..207 x740..760:", [tuple(A[y, 750]) for y in (205, 206, 207)])
P(" col1 border ring (r=20 around 160,285.5):",
  [tuple(A[286, 180]), tuple(A[300, 174]), tuple(A[286, 140]), tuple(A[271, 174]), tuple(A[305, 160])])
P(" col2 border (241,285):", tuple(A[285, 241]), "(283,267):", tuple(A[267, 283]))
P(" arrow shafts: i(264,420):", tuple(A[420, 264]), "j(429,420):", tuple(A[420, 429]), "k(589,420):", tuple(A[420, 589]))
P(" arrow heads: i(264,392):", tuple(A[392, 264]), "j(429,392):", tuple(A[392, 429]), "k(589,392):", tuple(A[392, 589]))
P(" divider col3 r2 (426,290):", tuple(A[290, 426]), "(427,290):", tuple(A[290, 427]),
  "| col5 r2 (677,295):", tuple(A[295, 677]), "(676,295):", tuple(A[295, 676]))
P(" glyph darkest col2 r2:", A[272:298, 248:276].reshape(-1, 3)[np.argmin(A[272:298, 248:276].reshape(-1, 3).sum(axis=1))])
P(" glyph darkest col5 r2:", A[272:298, 664:692].reshape(-1, 3)[np.argmin(A[272:298, 664:692].reshape(-1, 3).sum(axis=1))])
P(" class top edge (855,201..203):", [tuple(A[y, 855]) for y in (201, 202, 203)])
P(" callout tops: prev(260,427..429):", [tuple(A[y, 260]) for y in (427, 428, 429)],
  "cur(427,427..429):", [tuple(A[y, 427]) for y in (427, 428, 429)], "nxt(590,431..433):", [tuple(A[y, 590]) for y in (431, 432, 433)])
dashrow = A[139:144, 200:800]
ink = (np.abs(dashrow - BEIGE).sum(axis=2) > 60).any(axis=0)
P(" dash band y139..143 ink count x200..800:", int(ink.sum()))
P(" IS/SL text samples: IS(80,135):", tuple(A[135, 80]), "SL(840,133):", tuple(A[133, 840]))
P("done")
