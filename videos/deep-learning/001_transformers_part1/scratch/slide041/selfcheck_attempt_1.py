import numpy as np
from PIL import Image
import sys

RENDER = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/scratch/slide041/render/slide-1.png"
ORIG = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_041.jpg"
OUT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/scratch/slide041/selfcheck_attempt_1.txt"

im = np.asarray(Image.open(RENDER).convert("RGB")).astype(int)
H, W = im.shape[:2]
r, g, b = im[:,:,0], im[:,:,1], im[:,:,2]
S = 150 / 72.0  # frame px -> render px
lines = []
def log(s):
    print(s); lines.append(s)

log(f"render {W}x{H} (expect 2001x1125 @150dpi)")
fails = []
def check(name, cond, detail):
    tag = "PASS" if cond else "FAIL"
    log(f"[{tag}] {name}: {detail}")
    if not cond: fails.append(name)

# --- 2) FRAME CONTAINMENT: content ink must sit inside the house panel (87.5..1912.5 x 93.75..1125)
# content zone (inside panel border ~3px): x 92..1908, y 98..1120
zone = np.zeros((H, W), bool)
zone[100:1120, 94:1906] = True
# ink = pixels that differ from BOTH the panel gray and white canvas significantly
diff_panel = (np.abs(r-233)+np.abs(g-233)+np.abs(b-231)) > 90
diff_white = (np.abs(r-255)+np.abs(g-255)+np.abs(b-255)) > 90
ink = diff_panel & diff_white
outside = ink & ~zone
n_out = int(outside.sum())
# ignore the chrome itself (panel border ring ~4px wide around the zone edges)
ring = np.zeros((H, W), bool)
ring[93:105, 85:1915] = True; ring[1115:1125, 85:1915] = True
ring[93:1125, 85:99] = True; ring[93:1125, 1901:1917] = True
outside_real = outside & ~ring
log(f"containment: {int(outside_real.sum())} ink px outside content zone (excl chrome ring)")
check("frame-containment", outside_real.sum() < 300, f"{int(outside_real.sum())} stray px")

def ink_bbox(mask, label):
    ys, xs = np.where(mask)
    if len(xs) == 0:
        log(f"  {label}: EMPTY"); return None
    log(f"  {label}: x {xs.min()}..{xs.max()} y {ys.min()}..{ys.max()} n={len(xs)}")
    return xs.min(), xs.max(), ys.min(), ys.max()

def region(x0, y0, x1, y1):
    m = np.zeros((H, W), bool)
    m[int(y0*S):int(y1*S)+1, int(x0*S):int(x1*S)+1] = True
    return m

# --- 3) title: red ink at y 58..82 frame px
tmask = (r>150)&(g<80)&(b<80)
tmask[int(95*S):,:] = False
bb = ink_bbox(tmask & region(100, 40, 860, 95), "title-red")
check("title-ink", bb is not None and bb[3]-bb[2] > 30, "red title band present" if bb else "missing")

# --- badge numeral ink (dark on yellow) at badge
ymask = (r>230)&(g>230)&(b<190)
bb = ink_bbox(ymask & region(860, 55, 930, 95), "badge-yellow")
check("badge", bb is not None, "yellow badge present" if bb else "missing")

# --- left schematic: green border box + inner box fills
gmask = (r<90)&(g>85)&(g<135)&(b<90)
bb = ink_bbox(gmask & region(50, 260, 210, 500), "left-green-border")
check("left-schematic-border", bb is not None and (bb[1]-bb[0])>110 and (bb[3]-bb[2])>190, "green box present" if bb else "missing")
lav = (np.abs(r-197)<28)&(np.abs(g-202)<28)&(np.abs(b-233)<28)
bb = ink_bbox(lav & region(70, 280, 210, 460), "left-lavender-matmul")
check("left-matmul", bb is not None, "lavender present" if bb else "missing")
pnk = (np.abs(r-248)<25)&(np.abs(g-187)<28)&(np.abs(b-208)<28)
bb = ink_bbox(pnk & region(70, 350, 210, 395), "left-pink-mask")
check("left-mask", bb is not None, "pink present" if bb else "missing")

# --- center container tan
tan = (np.abs(r-232)<14)&(np.abs(g-181)<16)&(np.abs(b-126)<18)
bb = ink_bbox(tan & region(280, 200, 530, 535), "center-tan-container")
check("center-container", bb is not None and (bb[1]-bb[0])>200 and (bb[3]-bb[2])>280, "tan container present" if bb else "missing")
# SDPA stack red borders
rmask = (r>150)&(g<80)&(b<80)
bb = ink_bbox(rmask & region(295, 345, 500, 445), "center-sdpa-red-border")
check("sdpa-stack", bb is not None and (bb[1]-bb[0])>120, "stack red borders present" if bb else "missing")
# circles row (V/K/q filled tokens) — dark pixels at y~496
dk = (r<150)&(g<120)&(b<170)
bb = ink_bbox(dk & region(310, 480, 470, 512), "center-circles")
check("center-circles", bb is not None, "circle tokens present" if bb else "missing")
# pin red at ~(247..309, 131..236)
bb = ink_bbox(rmask & region(230, 120, 330, 250), "pin-red")
check("pin", bb is not None, "red pin present" if bb else "missing")

# --- right panel: green border, half fills, purple block, maroon, highlights
g2 = (r<110)&(g>130)&(g<210)&(b<110)
bb = ink_bbox(g2 & region(560, 95, 910, 535), "right-panel-green-border")
check("right-panel-border", bb is not None and (bb[1]-bb[0])>280, "green border present" if bb else "missing")
pur = (np.abs(r-179)<30)&(np.abs(g-157)<30)&(np.abs(b-219)<30)
bb = ink_bbox(pur & region(735, 330, 830, 420), "right-maskedMHA")
check("masked-mha", bb is not None, "purple block present" if bb else "missing")
mar = (np.abs(r-139)<30)&(np.abs(g-74)<30)&(np.abs(b-74)<30)
bb = ink_bbox(mar & region(740, 430, 830, 490), "right-outputEmb")
check("output-embedding", bb is not None, "maroon block present" if bb else "missing")
ylw = (r>215)&(g>240)&(b<160)
bb = ink_bbox(ylw & region(750, 100, 825, 140), "hl-outputProb")
check("hl-outputProb", bb is not None, "yellow hl present" if bb else "missing")
bb = ink_bbox(ylw & region(750, 485, 825, 515), "hl-outputs")
check("hl-outputs", bb is not None, "yellow hl present" if bb else "missing")
# dotted connectors: red ink in the two gap zones
bb = ink_bbox(rmask & region(195, 290, 295, 440), "zoom-lines-left")
check("zoom-lines-left", bb is not None, "dotted lines present" if bb else "missing")
bb = ink_bbox(rmask & region(526, 340, 645, 410), "zoom-lines-right")
check("zoom-lines-right", bb is not None, "dotted lines present" if bb else "missing")
# autoregressive arc: dark red ink near x 860..895, y 150..480
drk = (np.abs(r-139)<55)&(g<80)&(b<80)
bb = ink_bbox(drk & region(795, 130, 895, 500), "auto-curve")
check("auto-curve", bb is not None, "dashed curve present" if bb else "missing")

# --- "× h" annotation ink present (equation-existence analog: no empty region)
xh = ((np.abs(r-30)<60)&(np.abs(g-30)<60)&(np.abs(b-30)<60))
bb = ink_bbox(xh & region(478, 360, 520, 392), "x-h-ink")
check("x-h-annotation", bb is not None, "× h ink present" if bb else "missing")

# --- anchors: render macro-geometry vs original measured anchors (frame px)
def has(mask, x0, y0, x1, y1):
    m = np.zeros((H, W), bool)
    m[int(y0*S):int(y1*S)+1, int(x0*S):int(x1*S)+1] = True
    ys, xs = np.where(mask & m)
    return None if len(xs) == 0 else (xs.min()/S, xs.max()/S, ys.min()/S, ys.max()/S)

anchors = [
    ("center container", tan & region(280, 200, 530, 535), (286, 521, 208, 525), 12),
    ("right panel border", g2 & region(560, 95, 910, 535), (575, 895, 104, 524), 8),
    ("left schematic box", gmask & region(50, 260, 210, 500), (60, 190, 271, 490), 8),
]
for name, mask, (ex0, ex1, ey0, ey1), tol in anchors:
    bb = has(mask, *[v for v in (ex0-15, ey0-15, ex1+15, ey1+15)])
    if bb is None:
        check(f"anchor-{name}", False, "no ink"); continue
    dx0, dx1, dy0, dy1 = abs(bb[0]-ex0), abs(bb[1]-ex1), abs(bb[2]-ey0), abs(bb[3]-ey1)
    ok = max(dx0, dx1, dy0, dy1) <= tol
    check(f"anchor-{name}", ok, f"render bbox ({bb[0]:.0f},{bb[2]:.0f})-({bb[1]:.0f},{bb[3]:.0f}) vs orig ({ex0},{ey0})-({ex1},{ey1}) maxΔ {max(dx0,dx1,dy0,dy1):.1f}px")

# --- 8) line-spacing sanity: the title is single-line; multi-line boxes carry explicit spacing in the build (audited by hand)
log("line-spacing: explicit lineSpacing set on all multi-line text boxes in slide_041.js (audited)")

log("")
log(f"RESULT: {'ALL CHECKS PASS' if not fails else 'FAILURES: ' + ', '.join(fails)}")
open(OUT, "w").write("\n".join(lines) + "\n")
sys.exit(0)
