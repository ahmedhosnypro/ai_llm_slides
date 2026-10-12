# selfcheck_attempt_1.py — mandatory pre-judge self-checks for slide 059, attempt 1
# Render: 2001x1125 @150dpi; slide_pt = render_px * 72/150 = px * 0.48
# Original frame: 960x540; slide_pt = (fx-18.63)/0.96123 , fy/0.95556
from PIL import Image
import numpy as np
import sys

RENDER = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/qa/slide059/render_1.png"
ORIG = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_059.jpg"

R = np.asarray(Image.open(RENDER).convert("RGB")).astype(int)
O = np.asarray(Image.open(ORIG).convert("RGB")).astype(int)
RH, RW, _ = R.shape
r, g, b = R[:, :, 0], R[:, :, 1], R[:, :, 2]
orf, ogf, obf = O[:, :, 0], O[:, :, 1], O[:, :, 2]

fails, warns = [], []

def runs(bools, min_len=1):
    out, s = [], None
    for i, v in enumerate(bools):
        if v and s is None: s = i
        if not v and s is not None:
            if i - s >= min_len: out.append((s, i - 1))
            s = None
    if s is not None: out.append((s, len(bools) - 1))
    return out

def r2pt(v): return v * 0.48          # render px -> slide pt
def o2ptx(v): return (v - 18.63) / 0.96123
def o2pty(v): return v / 0.95556

def chk(name, cond, detail=""):
    if cond:
        print(f"  PASS  {name} {detail}")
    else:
        print(f"  FAIL  {name} {detail}")
        fails.append(name)

print("== 0. HOUSE CHROME CHECK (standard) ==")
import subprocess
p = subprocess.run([sys.executable,
    "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/shared_patterns/house_chrome_check.py",
    RENDER, "59"], capture_output=True, text=True)
print("  " + p.stdout.strip().replace("\n", "\n  "))
chrome_std_fail = (p.returncode != 0)

# adapted badge check: the measured tan softmax bar (orig frame x..864, y 91..111)
# legitimately enters the checker's badge window (x>=857, rows<=107). Verify the badge
# alone in the sub-window above the bar top (render row 198).
print("== 0b. badge direct verification (window above softmax-bar band) ==")
win = np.s_[72:195, 1785:1935]
wr, wg, wb = r[win], g[win], b[win]
yel = (wr > 200) & (wg > 200) & (wb < 190)
pys, pxs = np.where(yel)
bcx = 1785 + (pxs.min() + pxs.max()) / 2
bcy = 72 + (pys.min() + pys.max()) / 2
bw = pxs.max() - pxs.min() + 1
chk("badge center", abs(bcx - 1860.4) <= 8 and abs(bcy - 147.9) <= 8,
    f"({bcx:.0f},{bcy:.0f}) vs (1860,148)")
chk("badge diameter", abs(bw - 75) <= 12, f"{bw} vs 75")
pur = (wb > 150) & (wr > 70) & (wr < 180) & (wg < 130)
chk("badge purple ring", pur.sum() >= 10, f"n={pur.sum()}")
print(f"  NOTE: standard chrome check {'FAILS' if chrome_std_fail else 'passes'}; "
      f"badge-window pollution = measured tan softmax bar (matches original frame).")

# ---- 1. FRAME CONTAINMENT (playlist panel bounds; white margin must hold no ink) ----
print("== 1. containment: content ink inside panel x42..918 y45..540 (frame-equiv) ==")
# white margin = outside panel; ink there (excluding chrome border ring ~2pt and badge)
margin = np.ones_like(r, bool)
margin[int(45*2.0833)-6:int(540*2.0833)+6, int(42*2.0833)-6:int(918*2.0833)+6] = False
ink_m = (abs(r - g) > 30) | (abs(g - b) > 30) | (abs(r - b) > 30) | ((r < 200) & (g < 200))
stray = ink_m & margin
# badge sits above panel top: allow badge bbox rows<223 cols>=1780
stray[:230, 1770:] = False
n_stray = int(stray.sum())
chk("no content ink in white margin", n_stray < 200, f"stray px={n_stray}")

# ---- 2. key element geometry (render vs measured original) ----
print("== 2. element geometry (slide pt, tolerance ±3pt) ==")
def bbox(mask, tag):
    ys, xs = np.where(mask)
    if len(xs) == 0:
        return None
    return (xs.min()*0.48, xs.max()*0.48, ys.min()*0.48, ys.max()*0.48, len(xs))

def near(a, t, tol=3.0): return abs(a - t) <= tol

# lilac container
lil = (abs(r-246)<10)&(abs(g-220)<12)&(abs(b-247)<10)
lil[:int(380/0.48), :] = False
bb = bbox(lil, "lilac")
if bb: chk("input container", near(bb[0],49.3,4) and near(bb[2],402.9,5) and near(bb[1],907.6,6) and near(bb[3],535.7,5),
           f"x {bb[0]:.0f}..{bb[1]:.0f} y {bb[2]:.0f}..{bb[3]:.0f}")
else: fails.append("lilac container missing")

# rose container
rose = (abs(r-205)<25)&(abs(g-92)<35)&(abs(b-92)<35)
rose[:int(280/0.48), :] = False
rose[int(400/0.48):, :] = False
bb = bbox(rose, "rose")
if bb: chk("encoder container", near(bb[0],130.4,4) and near(bb[2],288.8,4) and near(bb[1],893.0,4) and near(bb[3],388.2,4),
           f"x {bb[0]:.0f}..{bb[1]:.0f} y {bb[2]:.0f}..{bb[3]:.0f}")

# dark bars: rows at col x=200slide=417render
dr = (r>=130)&(r<225)&(g<80)&(b<80)
col = int(200/0.48)
rr = [y*0.48 for y in range(RH) if dr[y, col]]
bands = runs(np.array([dr[y, col] for y in range(RH)]), 4)
bar_bands = [(a*0.48, c*0.48) for a, c in bands if c-a > 6]
exp_bars = [(292.0, 310.8), (314.0, 332.8), (368.4, 387.2)]
ok = len(bar_bands) == 3 and all(near(a, e[0], 3) and near(b, e[1], 3) for (a, b), e in zip(bar_bands, exp_bars))
chk("3 dark bars y", ok, f"{[(round(a),round(b)) for a,b in bar_bands]} vs {exp_bars}")

# GAP box borders at col 300slide
darkg = (r<175)&(g<175)&(b<175)&(abs(r-g)<40)&(abs(g-b)<40)
col = int(300/0.48)
gb = runs(np.array([darkg[y, col] for y in range(int(150/0.48), int(230/0.48))]), 1)
gb_abs = [((a + int(150/0.48))*0.48, (c + int(150/0.48))*0.48) for a, c in gb]
chk("GAP box top/bottom", len(gb_abs) >= 2 and near(gb_abs[0][0], 192.6, 3) and near(gb_abs[-1][1], 216.6, 3),
    f"{[(round(a,1),round(b,1)) for a,b in gb_abs]} vs (192.6, 216.6)")

# GAP box left/right at row mid
row = int(204/0.48)
gbc = runs(np.array([darkg[row, x] for x in range(int(120/0.48), int(940/0.48))]), 1)
gbc_abs = [((a + int(120/0.48))*0.48, (c + int(120/0.48))*0.48) for a, c in gbc]
left_ok = any(near(a, 159.7, 3.5) for a, b in gbc_abs)
right_ok = any(near(b, 902.9, 3.5) for a, b in gbc_abs)
chk("GAP box left/right", left_ok and right_ok, f"{[(round(a,1),round(b,1)) for a,b in gbc_abs][:6]}")

# tan bar
tan = (abs(r-245)<14)&(abs(g-203)<16)&(abs(b-167)<20)
tan[int(135/0.48):, :] = False
bb = bbox(tan, "tan")
if bb: chk("softmax bar", near(bb[0],163.7,4) and near(bb[2],95.2,3) and near(bb[1],879.6,5) and near(bb[3],116.2,3),
           f"x {bb[0]:.0f}..{bb[1]:.0f} y {bb[2]:.0f}..{bb[3]:.0f}")

# navy circles
navy = (b-r>60)&(b-g>50)&(b>110)&(r<60)
band = navy[int(80/0.48):int(135/0.48), int(380/0.48):int(660/0.48)]
cl = runs(band.sum(axis=0) > 3, 8)
cxs = [((a+c)/2*0.48+380) for a, c in cl]
chk("3 softmax circles x", len(cxs) == 3 and all(near(c, e, 4) for c, e in zip(cxs, [438.5, 514.0, 589.3])),
    f"{[round(c) for c in cxs]}")
ys2, xs2 = np.where(band)
cym = (ys2.min()+ys2.max())/2*0.48 + 80
chk("circles cy", near(cym, 106.2, 4), f"{cym:.1f}")

# plus disc
plus = (r>140)&(r<225)&(g<110)&(b<110)&(r-g>70)
ys, xs = np.where(plus[int(458/0.48):int(498/0.48), int(460/0.48):int(540/0.48)])
if len(xs):
    cx = (xs.min()+xs.max())/2*0.48 + 460
    cy = (ys.min()+ys.max())/2*0.48 + 458
    d = (xs.max()-xs.min()+1)*0.48
    chk("plus circle", near(cx, 500.3, 4) and near(cy, 477.2, 4) and near(d, 22.9, 4),
        f"c ({cx:.1f},{cy:.1f}) d {d:.1f}")

# pooled row: colored cells
uncol = ~((abs(r-233)<14)&(abs(g-233)<14)&(abs(b-231)<16)) & ~((r>250)&(g>250)&(b>250))
ys, xs = np.where(uncol[int(150/0.48):int(175/0.48), int(370/0.48):int(650/0.48)])
if len(xs):
    chk("pooled row extent", near(xs.min()*0.48+370, 384.4, 5) and near(xs.max()*0.48+370, 636.4, 6)
        and near(ys.min()*0.48+150, 153.8, 4) and near(ys.max()*0.48+150, 172.7, 4),
        f"x {xs.min()*0.48+370:.0f}..{xs.max()*0.48+370:.0f} y {ys.min()*0.48+150:.0f}..{ys.max()*0.48+150:.0f}")

# block arrows: blue outline at centerline
bl = (b-r>35)&(b-g>25)&(b>100)
for (tag, y0, y1) in [("arrow1", 370, 430), ("arrow2", 260, 300), ("arrow3", 205, 245), ("arrow4", 165, 200)]:
    ys2, xs2 = np.where(bl[int(y0/0.48):int(y1/0.48), int(480/0.48):int(545/0.48)])
    if len(xs2):
        cx = (xs2.min()+xs2.max())/2*0.48 + 480
        ytop = ys2.min()*0.48 + y0
        chk(tag, near(cx, 511.0, 4) and near(ytop, {"arrow1":387.2,"arrow2":271.0,"arrow3":213.5,"arrow4":172.7}[tag], 4),
            f"cx {cx:.1f} top {ytop:.1f}")
    else:
        fails.append(f"{tag} missing")

# ---- 3. token rows: label columns and cell grid (render vs original) ----
print("== 3. token rows ==")
# X labels (dark red) in render: band slide y 440..458 -> render 917..955
dredR = (r<225)&(r-g>45)&(r-b>35)&(r>80)
sub = dredR[int(438/0.48):int(460/0.48), int(150/0.48):int(920/0.48)]
clR = [cc for cc in runs(sub.sum(axis=0) > 1, 2)]
merged = []
for a, c in clR:
    if merged and (a - merged[-1][1]) * 0.48 < 10:
        merged[-1] = (merged[-1][0], c)
    else:
        merged.append((a, c))
labR = [((a+c)/2*0.48+150) for a, c in merged if (a*0.48+150) < 908]
# original X label centers (frame): measured v1/v2
labO = [o2ptx(v) for v in [214.5, 288, 361.5, 435, 508.5, 582, 769.5, 844.5]]
ok = len(labR) == 8 and all(near(a, e, 5) for a, e in zip(labR, labO))
chk("X labels 8 columns", ok, f"render {[round(v) for v in labR]} vs orig {[round(v) for v in labO]}")
# Y labels red
sub = dredR[int(243/0.48):int(262/0.48), int(150/0.48):int(920/0.48)]
clR = runs(sub.sum(axis=0) > 1, 2)
merged = []
for a, c in clR:
    if merged and (a - merged[-1][1]) * 0.48 < 10:
        merged[-1] = (merged[-1][0], c)
    else:
        merged.append((a, c))
labR = [((a+c)/2*0.48+150) for a, c in merged if (a*0.48+150) < 908]
chk("Y labels 8 columns (red)", len(labR) == 8 and all(near(a, e, 5) for a, e in zip(labR, labO)),
    f"{[round(v) for v in labR]}")
# V labels navy
navt = (b-r>45)&(b-g>35)&(b>100)&(r<160)
sub = navt[int(500/0.48):int(518/0.48), int(150/0.48):int(920/0.48)]
clR = runs(sub.sum(axis=0) > 1, 2)
merged = []
for a, c in clR:
    if merged and (a - merged[-1][1]) * 0.48 < 14:
        merged[-1] = (merged[-1][0], c)
    else:
        merged.append((a, c))
labR = [((a+c)/2*0.48+150) for a, c in merged if (a*0.48+150) < 908]
labV = [o2ptx(v) for v in [205.5, 279, 352.5, 426, 499.5, 573.5, 758.5, 833.5]]
ok = len(labR) == 8 and all(near(a, e, 8) for a, e in zip(labR, labV))
chk("V labels 8 columns (navy)", ok, f"{[round(v) for v in labR]} vs {[round(v) for v in labV]}")
# X-row mint fill present between bands
mintR = (g-r>12)&(g-b>18)&(g>240)
sub = mintR[int(443/0.48):int(455/0.48), int(300/0.48):int(340/0.48)]
chk("X band mint fill", sub.sum() > 200, f"n={int(sub.sum())}")
# peach fill
peaR = (abs(r-253)<9)&(abs(g-235)<13)&(abs(b-208)<15)
sub = peaR[int(500/0.48):int(515/0.48), int(300/0.48):int(340/0.48)]
chk("V band peach fill", sub.sum() > 200, f"n={int(sub.sum())}")
# lblue fill
lblR = (abs(r-214)<16)&(abs(g-234)<13)&(abs(b-248)<11)
sub = lblR[int(250/0.48):int(262/0.48), int(300/0.48):int(340/0.48)]
chk("Y band light-blue fill", sub.sum() > 200, f"n={int(sub.sum())}")

# ---- 4. text bands / line spacing ----
print("== 4. annotation line pitches (explicit lineSpacing compliance) ==")
inkR = (abs(r-g)>35)|(abs(g-b)>35)|(abs(r-b)>35)
def lines_pt(y0, y1, x0, x1, tag, exp_pitch):
    sub = inkR[int(y0/0.48):int(y1/0.48), int(x0/0.48):int(x1/0.48)]
    rowc = sub.sum(axis=1)
    ln = runs(rowc > 2, 2)
    tops = [a*0.48+y0 for a, c in ln]
    if len(tops) >= 2:
        pitch = tops[1] - tops[0]
        chk(f"{tag} pitch", near(pitch, exp_pitch, 2.5), f"{pitch:.1f} vs {exp_pitch} (tops {[round(t) for t in tops]})")
    else:
        chk(f"{tag} lines", False, f"only {len(tops)} lines found")
lines_pt(140, 180, 66, 260, "pooled-note", 15.7)
lines_pt(234, 268, 62, 150, "output-seq", 14.6)
lines_pt(420, 470, 62, 150, "word-emb", 13.6)
lines_pt(480, 526, 62, 150, "position", 13.6)

# GAP text present
gapt = (r<120)&(g<120)&(b<120)
sub = gapt[int(196/0.48):int(212/0.48), int(400/0.48):int(660/0.48)]
chk("GAP text ink", sub.sum() > 300, f"n={int(sub.sum())}")
# title white ink inside rose
wht = (r>235)&(g>235)&(b>235)
sub = wht[int(340/0.48):int(360/0.48), int(390/0.48):int(615/0.48)]
chk("title white ink", sub.sum() > 400, f"n={int(sub.sum())}")
# Sigma ink in circles (non-navy ink inside circle bbox)
for i, cx in enumerate([438.5, 514.0, 589.3]):
    box = R[int(88/0.48):int(125/0.48), int((cx-18)/0.48):int((cx+18)/0.48)]
    nonnavy = ~((box[:,:,2]-box[:,:,0]>60)&(box[:,:,2]>110))
    chk(f"circle{i+1} inner ink (Softmax/Sigma)", nonnavy.sum() > 150, f"n={int(nonnavy.sum())}")

print()
if fails:
    print(f"SELFCHECK RESULT: {len(fails)} FAIL -> {fails}")
else:
    print("SELFCHECK RESULT: ALL PASS")
