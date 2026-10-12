#!/usr/bin/env python3
"""Slide 055 selfcheck attempt 1 — closed-loop PIL verification of render_1.png vs frame targets.
Render 2001x1125 @150dpi: render_px = slide_pt * 2000/960 (factor 2.08333).
frame->render: rx = (fx-18.63)/0.96123*2.08333 ; ry = fy/0.95556*2.08333.
Tolerances: equation edges ±4px @150dpi; general elements ±8px (JPEG halo)."""
from PIL import Image
import json, sys

REN = sys.argv[1] if len(sys.argv) > 1 else "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/qa/slide055/render_1.png"
img = Image.open(REN).convert("RGB")
W, H = img.size
px = img.load()
F = 2000.0 / 960.0
X0, SX, SY = 18.63, 0.96123, 0.95556
def rx(fx): return (fx - X0) / SX * F
def ry(fy): return fy / SY * F

results = {}
fails = []

def redness(p):
    r, g, b = p
    return r - max(g, b)
def is_reddish(p, t=40):
    return redness(p) > t
def is_navy(p):
    r, g, b = p
    return b > 90 and r < 110 and g < 110 and (b - r) > 40
def is_dark(p):
    return sum(p) < 330

def ink_bbox(x0, y0, x1, y1, pred):
    xs, ys = [], []
    for y in range(max(0, int(y0)), min(H, int(y1))):
        for x in range(max(0, int(x0)), min(W, int(x1))):
            if pred(px[x, y]):
                xs.append(x); ys.append(y)
    if not xs:
        return None
    return (min(xs), min(ys), max(xs), max(ys), len(xs))

def check(name, target_frame, got, tol=8, tag=""):
    """target_frame = (fx0,fy0,fx1,fy1) frame ink bbox; got = render bbox or None."""
    if got is None:
        results[name] = "MISSING"
        fails.append(name)
        return
    t = (int(round(rx(target_frame[0]))), int(round(ry(target_frame[1]))),
         int(round(rx(target_frame[2]))), int(round(ry(target_frame[3]))))
    d = (got[0] - t[0], got[1] - t[1], got[2] - t[2], got[3] - t[3])
    ok = all(abs(v) <= tol for v in d)
    results[name] = {"target": t, "got": got[:4], "delta": d, "ok": ok, "px": got[4]}
    if not ok:
        fails.append(name + tag)

# 1. title lines (dark+red ink)
def ink_title(p):
    return is_dark(p) or is_reddish(p, 50)
check("title_L1", (264, 58, 740, 71), ink_bbox(rx(200), ry(52), rx(810), ry(75), ink_title), 10)
check("title_L2", (201, 79, 803, 94), ink_bbox(rx(150), ry(76), rx(860), ry(100), ink_title), 10)

# 2. peach panel edges (fill ~F7E2CD)
def is_peach(p):
    r, g, b = p
    return r > 238 and 214 < g < 240 and 182 < b < 220
pc = [x for x in range(0, W) if is_peach(px[x, int(ry(300))])]
pr = [y for y in range(int(ry(90)), min(int(ry(520)), H - 1)) if sum(1 for x in range(int(rx(100)), int(rx(860)), 3) if is_peach(px[x, y])) > 200]
results["panel_cols"] = [min(pc), max(pc), "target", int(rx(84)), int(rx(879))]
results["panel_rows"] = [min(pr), max(pr), "target", int(ry(104)), int(ry(502))]
if abs(min(pc) - rx(84)) > 10 or abs(max(pc) - rx(879)) > 10 or abs(min(pr) - ry(104)) > 10 or abs(max(pr) - ry(502)) > 10:
    fails.append("panel_edges")

# 3. fraction: red ink bbox in region (frame [446,185,471,218]) — tol 4
check("fraction_ink", (446, 185, 471, 218),
      ink_bbox(rx(438), ry(180), rx(482), ry(224), lambda p: is_reddish(p, 45)), 4, "_EQ")

# 4. rotated strips
# Scaling text: red ink inside column x 415..442, y 200..380
sc = ink_bbox(rx(414), ry(200), rx(444), ry(380), lambda p: is_reddish(p, 45))
if sc is None:
    fails.append("rot_scaling"); results["rot_scaling"] = "MISSING"
else:
    cx = (sc[0] + sc[2]) / 2
    tcx = rx((411 + 446) / 2)
    results["rot_scaling"] = {"cx": cx, "target_cx": tcx, "dcx": cx - tcx, "yband": [sc[1], sc[2]]}
    if abs(cx - tcx) > 6:
        fails.append("rot_scaling_cx")
# Soft max text: purple ink lines 1-2 in column x 489..513 (frame text band 255..284)
def is_purp(p):
    r, g, b = p
    return 90 < r < 180 and g < 110 and b > 130 and (b - g) > 40
sm = ink_bbox(rx(489), ry(250), rx(513), ry(290), is_purp)
if sm is None:
    fails.append("rot_softmax"); results["rot_softmax"] = "MISSING"
else:
    cy_ = (sm[1] + sm[3]) / 2
    tcy = ry(270)
    results["rot_softmax"] = {"cy": cy_, "target_cy": tcy, "dcy": cy_ - tcy}
    if abs(cy_ - tcy) > 10:
        fails.append("rot_softmax_cy")
# final-sigma glyph: frame band 292..320
sg = ink_bbox(rx(489), ry(290), rx(513), ry(326), is_purp)
if sg is None:
    fails.append("sigma_glyph"); results["sigma_glyph"] = "MISSING"
else:
    gcy = (sg[1] + sg[3]) / 2
    results["sigma_glyph"] = {"band": [sg[1], sg[3]], "target": [ry(292), ry(320)], "cy": gcy, "target_cy": ry(306)}
    if abs(gcy - ry(306)) > 10 or (sg[3] - sg[1]) < ry(318) - ry(294):
        fails.append("sigma_glyph")

# 5. dots: navy clusters at the 4 measured centers (tol 6 render px)
for i, (dx, dy) in enumerate([(363, 237.5), (348, 276.5), (330, 316), (311.5, 359)]):
    bb = ink_bbox(rx(dx) - 12, ry(dy) - 12, rx(dx) + 12, ry(dy) + 12, is_navy)
    if bb is None:
        fails.append(f"dot{i+1}"); results[f"dot{i+1}"] = "MISSING"
    else:
        c = ((bb[0] + bb[2]) / 2, (bb[1] + bb[3]) / 2)
        dd = (c[0] - rx(dx), c[1] - ry(dy))
        results[f"dot{i+1}"] = {"d": [round(v, 1) for v in dd]}
        if abs(dd[0]) > 7 or abs(dd[1]) > 7:
            fails.append(f"dot{i+1}")

# 6. nodes: red ring presence at the 4 centers
for i, (nx, ny) in enumerate([(557.5, 237), (587, 277), (616.5, 316.5), (645.5, 359)]):
    bb = ink_bbox(rx(nx) - 14, ry(ny) - 14, rx(nx) + 14, ry(ny) + 14, lambda p: is_reddish(p, 60))
    if bb is None or bb[4] < 20:
        fails.append(f"node{i+1}"); results[f"node{i+1}"] = "MISSING/WEAK"
    else:
        results[f"node{i+1}"] = "present px=%d" % bb[4]

# 7. sigma box fill presence
def is_sigblue(p):
    r, g, b = p
    return 220 < r < 245 and g > 245 and b > 240
sb = ink_bbox(rx(543), ry(186), rx(671), ry(212), is_sigblue)
results["sigma_box"] = sb
if sb is None or sb[4] < 500:
    fails.append("sigma_box")

# 8. shaft continuity: sample midline redness along each K->dot line + node->Sigma shafts + query
def shaft_ok(x_a, y_a, x_b, y_b, frac=0.75, t=25):
    n = 12
    hits = 0
    for k in range(1, n):
        x = x_a + (x_b - x_a) * k / n
        y = y_a + (y_b - y_a) * k / n
        found = any(is_reddish(px[min(W - 1, int(rx(x)) + ddx), min(H - 1, int(ry(y)) + ddy)], t)
                    for ddx in (-1, 0, 1) for ddy in (-2, -1, 0, 1, 2))
        if found:
            hits += 1
    return hits >= int(n * frac) - 1, hits
sh = {}
sh["K1_line"] = shaft_ok(270, 359, 300, 359)
sh["K2_line"] = shaft_ok(270, 316, 322, 316)
sh["K3_line"] = shaft_ok(270, 276.5, 338, 276.5)
sh["K4_line"] = shaft_ok(270, 237.5, 352, 237.5)
sh["NS1"] = shaft_ok(557, 220, 557, 228)
sh["NS2"] = shaft_ok(587, 220, 587, 268)
sh["NS3"] = shaft_ok(616, 220, 616, 307)
sh["NS4"] = shaft_ok(645, 220, 645, 350)
sh["query"] = shaft_ok(316, 396, 316, 370)
for k, (ok, hits) in sh.items():
    results["shaft_" + k] = hits
    if not ok:
        fails.append("shaft_" + k)

# 9. arrowhead presence: blobs at expected head positions
def head_ok(cx, cy, t=50, r=6):
    bb = ink_bbox(rx(cx) - r, ry(cy) - r, rx(cx) + r, ry(cy) + r, lambda p: is_reddish(p, t))
    return bb is not None and bb[4] >= 8
heads = {
    "SM_n1": head_ok(544.5, 237), "SM_n2": head_ok(574, 277), "SM_n3": head_ok(603.5, 316.5), "SM_n4": head_ok(632.5, 359),
    "V_n1": head_ok(571, 237), "V_n2": head_ok(600.5, 277), "V_n3": head_ok(630, 316.5), "V_n4": head_ok(659, 359),
    "UP_1": head_ok(557, 214.5), "UP_2": head_ok(587, 214.5), "UP_3": head_ok(616, 214.5), "UP_4": head_ok(645, 214.5),
    "K1_head": head_ok(300.5, 359), "K4_head": head_ok(352, 237.5),
    "BLK1": head_ok(192.5, 237, 0, 6) or True,  # black heads checked separately below
}
for k, ok in heads.items():
    results["head_" + k] = ok
    if not ok:
        fails.append("head_" + k)
# black heads (Y->Wk at x192.5, Y->Wv at x761.5)
for cy in (237, 276.5):
    bb = ink_bbox(rx(186), ry(cy) - 5, rx(200), ry(cy) + 5, is_dark)
    results[f"blackhead_L_{cy}"] = None if bb is None else bb[4]
    if bb is None or bb[4] < 10:
        fails.append(f"blackhead_L_{cy}")
for cy in (237, 277):
    bb = ink_bbox(rx(755), ry(cy) - 5, rx(768), ry(cy) + 5, is_dark)
    results[f"blackhead_R_{cy}"] = None if bb is None else bb[4]
    if bb is None or bb[4] < 10:
        fails.append(f"blackhead_R_{cy}")

# 10. Z-row: magenta cells + dashed red rect + up arrow
def is_mag(p):
    r, g, b = p
    return r > 195 and 80 < g < 170 and b > 160
mb = ink_bbox(rx(280), ry(450), rx(380), ry(495), is_mag)
results["z2_magenta"] = mb
if mb is None or mb[4] < 300:
    fails.append("z2_magenta")
ta = ink_bbox(rx(296), ry(488), rx(326), ry(514), lambda p: is_reddish(p, 60))
results["z_arrow"] = ta
if ta is None or ta[4] < 60:
    fails.append("z_arrow")

# 11. legend: navy caption + W box ink
def is_navyc(p):
    r, g, b = p
    return b > 100 and r < 90 and g < 90
nv = ink_bbox(rx(766), ry(480), rx(866), ry(495), is_navyc)
results["legend_caption"] = nv
if nv is None or nv[4] < 40:
    fails.append("legend_caption")
wb = ink_bbox(rx(786), ry(456), rx(820), ry(490), is_dark)
results["legend_W"] = wb
if wb is None or wb[4] < 30:
    fails.append("legend_W")

# 12. pills: pale lavender fill present at the 3 pill centers
def is_pillf(p):
    r, g, b = p
    return r > 225 and g > 220 and b > 235
for nm, (cxx, cyy) in {"sim": (338, 166), "prob": (499, 166), "wsum": (664, 166)}.items():
    bb = ink_bbox(rx(cxx) - 20, ry(cyy) - 8, rx(cxx) + 20, ry(cyy) + 8, is_pillf)
    results["pill_" + nm] = None if bb is None else bb[4]
    if bb is None or bb[4] < 100:
        fails.append("pill_" + nm)

# 13. equation region ink NONZERO (mandatory check 3) — covered by fraction_ink
# 14. O box green presence
def is_og(p):
    r, g, b = p
    return 130 < r < 190 and 170 < g < 230 and 120 < b < 190 and g > r
ob = ink_bbox(rx(572), ry(118), rx(641), ry(144), is_og)
results["O_box"] = ob
if ob is None or ob[4] < 400:
    fails.append("O_box")

print(json.dumps(results, indent=1))
print("FAILS:", fails if fails else "NONE")
sys.exit(0)
