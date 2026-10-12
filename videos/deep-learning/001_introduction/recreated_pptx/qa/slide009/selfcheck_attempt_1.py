# selfcheck attempt 1 (v3, unit-corrected) — closed-loop render vs measured original geometry.
# Render 150dpi: frame px * 2.08333 = render px. All wants given in FRAME px, converted here.
from PIL import Image
import numpy as np
import sys

REN = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/qa/slide009/render_1.png"
im = Image.open(REN).convert("RGB")
a = np.asarray(im).astype(int)
H, W, _ = a.shape
r, g, b = a[...,0], a[...,1], a[...,2]
S = 150/72.0
print(f"render {W}x{H}  scale={S:.4f}")

fails = []
def check(name, got, want_frame, tol=4.0):
    # want_frame: (x0,y0,x1,y1) in 960x540 frame px
    if got is None:
        print(f"FAIL {name}: EMPTY"); fails.append(name); return
    want = tuple(v*S for v in want_frame)
    d = max(abs(got[i]-want[i]) for i in range(4))
    print(f"{'OK ' if d<=tol else 'FAIL'} {name:22s} got ({got[0]:7.1f},{got[1]:7.1f})-({got[2]:7.1f},{got[3]:7.1f})  want ({want[0]:7.1f},{want[1]:7.1f})-({want[2]:7.1f},{want[3]:7.1f})  maxd={d:.1f}")
    if d > tol: fails.append(name)

def bbox_in(mask, fx0,fy0,fx1,fy1):
    m = np.zeros((H,W),bool)
    m[int(fy0*S):int(fy1*S), int(fx0*S):int(fx1*S)] = True
    ys, xs = np.nonzero(mask & m)
    if len(xs)==0: return None
    return (float(xs.min()), float(ys.min()), float(xs.max()), float(ys.max()))

redm = (r>110) & (r - np.maximum(g,b) > 50)
inkm = (r<115) & (g<115) & (b<115)
def near(t, tol):
    return (abs(r-t[0])<=tol)&(abs(g-t[1])<=tol)&(abs(b-t[2])<=tol)

check("title_ink", bbox_in(redm, 210,60,730,96), (219,68,715,91), 6)
check("panel_border_L", bbox_in(redm, 64,150,76,450), (69,150,72,450), 4)
check("panel_border_R", bbox_in(redm, 888,150,900,450), (893,150,896,450), 4)
check("panel_border_T", bbox_in(redm, 740,94,880,112), (740,99.5,880,102), 4)
check("panel_border_B", bbox_in(redm, 300,458,500,470), (300,463.5,500,466.5), 4)

navym  = (b>55)&(b<210)&(r<130)&(g<130)&(b-r>40)
purplem= near((114,34,124),45)
greenm = (g>85)&(g<200)&(g-r>25)&(g-b>25)
maroonm= (r>88)&(r<142)&(g<45)&(b<70)
check("box1_borderL", bbox_in(navym, 140,215,152,235), (145,215,147.5,235), 4)
check("box2_borderL", bbox_in(navym, 287,215,298,235), (291,215,294,235), 4)
check("box2_borderR", bbox_in(navym, 404,215,415,235), (407,215,411,235), 4)
check("box3_borderT", bbox_in(greenm, 460,202,540,212), (460,206.5,540,210), 4)
check("box4_borderT", bbox_in(maroonm, 600,202,700,213), (600,207.5,700,210.5), 4)
check("box4_borderL", bbox_in(maroonm, 582,218,592,255), (586.5,218,589.5,255), 4)
check("box5_borderL", bbox_in(purplem, 742,218,753,255), (746.5,218,749.5,255), 4)
check("box5_borderR", bbox_in(purplem, 857,218,868,255), (861,218,863.5,255), 4)

check("box1_fill", bbox_in(near((250,254,216),10), 150,213,246,260), (149,212,247,261), 6)
check("box2_fill", bbox_in(near((226,254,252),10), 298,213,404,260), (296,212,406,261), 6)
check("box3_fill", bbox_in(near((242,254,234),10), 447,213,554,260), (445,212,556,262), 6)
box4m = (r>135)&(r<185)&(g<45)&(b<60)
check("box4_fill", bbox_in(box4m, 592,213,718,262), (590,212,720,263), 6)
check("box5_fill", bbox_in(near((234,190,244),10), 754,213,857,260), (752,212,859,261), 6)

check("box1_text", bbox_in(inkm, 152,214,244,258), (155,222,239,254), 7)
check("box2_text", bbox_in(inkm, 299,214,403,258), (309,221,392,252), 7)
check("box3_text", bbox_in(inkm, 448,214,553,258), (463,221,538,252), 7)
check("box5_text", bbox_in(inkm, 755,214,856,258), (760,221,850,255), 7)
whitem = (r>200)&(g>200)&(b>200)
check("box4_whitetext", bbox_in(whitem, 596,226,714,248), (598,231,709,242), 6)

check("td_fill", bbox_in(near((246,222,194),12), 84,142,204,193), (83,142,205,193), 5)
check("td_text", bbox_in(inkm, 92,144,196,190), (108,150,177,183), 5)

yel = (r>170)&(g>170)&(b<90)
check("fr_fill", bbox_in(yel, 792,315,875,345), (790,314,876,346), 6)
check("fr_text", bbox_in(inkm, 806,316,861,345), (810,316,854,343), 6)
check("fr_border_T", bbox_in(inkm, 815,306,852,315), (816,309,851,313.5), 4)

grayband = (abs(r-g)<12)&(abs(g-b)<12)&(np.maximum(np.maximum(r,g),b)<238)&(np.minimum(np.minimum(r,g),b)>150)
check("label1_outer", bbox_in(grayband, 237,287,332,335), (241,291,328,331), 5)
check("label2_outer", bbox_in(grayband, 382,287,477,335), (386,291,473,331), 5)
check("label3_outer", bbox_in(grayband, 533,287,628,335), (537,291,624,331), 5)
check("label4_outer", bbox_in(grayband, 690,287,785,335), (694,291,781,331), 5)
check("label1_text", bbox_in(inkm, 246,294,324,328), (258,298,310,323), 6)
check("label2_text", bbox_in(inkm, 391,294,469,328), (405,298,454,323), 6)
check("label3_text", bbox_in(inkm, 542,294,620,328), (552,298,608,323), 6)
check("label4_text", bbox_in(inkm, 699,294,777,328), (707,298,768,323), 6)

check("arrow1", bbox_in(redm, 251,230,292,243), (250,235,291,239), 5)
check("arrow2", bbox_in(redm, 410,230,440,243), (409,235,440,239), 5)
arrow3m = redm & (b<18)
check("arrow3", bbox_in(arrow3m, 563,230,585,243), (562,235,585.5,239), 5)
check("arrow4", bbox_in(redm, 726,230,748,243), (724,235,748,239), 5)

check("curve1", bbox_in(redm, 88,181,150,249), (96,188,143,241), 7)
check("curve2", bbox_in(redm, 822,228,892,314), (830,236,882,309), 7)

darkm = (np.maximum(np.maximum(r,g),b) < 90)
check("blackbar", bbox_in(darkm, 30,514,930,540), (38,518,921,537.5), 4)

inner = np.zeros((H,W),bool)
inner[int(103*S):int(462*S), int(73*S):int(892*S)] = True
content = (inkm | redm | yel | box4m)
excl = np.zeros((H,W),bool)
excl[:int(102*S), :] = True; excl[:, :int(72*S)] = True; excl[:, int(894*S):] = True; excl[int(462*S):, :] = True
stray = int((content & ~inner & ~excl).sum())
print(f"\ncontainment stray px: {stray}")
if stray > 50: fails.append("containment")

# line bands: tops compared in RENDER px vs frame wants *S; close bands (<7px) merged
def bands_bottom(mask, fx0,fy0,fx1,fy1, label, want_bottoms_frame, tol=4.5):
    m = np.zeros((H,W),bool)
    m[int(fy0*S):int(fy1*S), int(fx0*S):int(fx1*S)] = True
    prof = (mask & m).sum(axis=1)
    raw, inl = [], False
    for i,c in enumerate(prof):
        if c>2 and not inl: st=i; inl=True
        if c<=2 and inl: raw.append([st,i-1]); inl=False
    if inl: raw.append([st,len(prof)-1])
    merged = []
    for bd in raw:
        if merged and bd[0]-merged[-1][1] < 7: merged[-1][1] = bd[1]
        else: merged.append(bd)
    bots = [b[1] for b in merged]
    want = [w*S for w in want_bottoms_frame]
    ok = len(bots)==len(want) and all(abs(t-w)<=tol for t,w in zip(bots,want))
    print(f"{'OK ' if ok else 'FAIL'} {label}: bottoms={bots} want={[round(w,1) for w in want]}")
    if not ok: fails.append(label+"_bands")

def bands(mask, fx0,fy0,fx1,fy1, label, want_tops_frame, tol=4.5):
    m = np.zeros((H,W),bool)
    m[int(fy0*S):int(fy1*S), int(fx0*S):int(fx1*S)] = True
    prof = (mask & m).sum(axis=1)
    raw, inl = [], False
    for i,c in enumerate(prof):
        if c>2 and not inl: st=i; inl=True
        if c<=2 and inl: raw.append([st,i-1]); inl=False
    if inl: raw.append([st,len(prof)-1])
    merged = []
    for bd in raw:
        if merged and bd[0]-merged[-1][1] < 7: merged[-1][1] = bd[1]
        else: merged.append(bd)
    tops = [b[0] for b in merged]
    want = [w*S for w in want_tops_frame]
    ok = len(tops)==len(want) and all(abs(t-w)<=tol for t,w in zip(tops,want))
    if len(tops)>=2:
        ok = ok and abs((tops[-1]-tops[0]) - (want[-1]-want[0])) <= tol
    print(f"{'OK ' if ok else 'FAIL'} {label}: tops={tops} want={[round(w,1) for w in want]}")
    if not ok: fails.append(label+"_bands")

print("\nline bands (render px tops):")
bands_bottom(inkm, 152,214,244,258, "box1 text", [232, 254])  # baseline-ish bottoms
bands(inkm, 246,294,324,328, "label1 text", [298, 314])
bands(inkm, 92,144,196,190, "training text", [150, 171])
bands(inkm, 806,315,861,345, "final text", [316, 333])
bands(whitem, 596,224,714,250, "classification", [231])

def xw(mask, fx0,fy0,fx1,fy1, label, want_w, tol=5):
    m = np.zeros((H,W),bool)
    m[int(fy0*S):int(fy1*S), int(fx0*S):int(fx1*S)] = True
    ys, xs = np.nonzero(mask & m)
    if len(xs)==0: print(f"  {label}: EMPTY"); fails.append(label); return
    w_frame = (xs.max()-xs.min()+1)/S
    d = abs(w_frame - want_w)
    print(f"{'OK ' if d<=tol else 'FAIL'} {label}: ink w={w_frame:.1f} frame px (want {want_w})")
    if d>tol: fails.append(label)
print("\ntext widths (frame px):")
xw(inkm, 152,241,244,257, "box1 'processing'", 85)
xw(inkm, 299,238,403,254, "box2 'Extraction'", 84)
xw(inkm, 448,238,553,254, "box3 'Selection'", 76)
xw(inkm, 755,241,856,257, "box5 'processing'", 88)
xw(whitem, 596,228,714,246, "box4 'Classification'", 112, 6)
xw(inkm, 92,148,196,167, "td 'Training'", 70)

print("\n==== RESULT:", "ALL PASS" if not fails else f"FAILURES: {fails}", "====")
sys.exit(1 if fails else 0)
