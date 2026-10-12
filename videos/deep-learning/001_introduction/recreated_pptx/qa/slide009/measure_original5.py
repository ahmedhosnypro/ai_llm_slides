# stage 5: exact bboxes of boxes/ellipses/labels, border colors, arrow shapes, text ink
from PIL import Image
import numpy as np
from collections import Counter
from scipy import ndimage

im = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_009.jpg").convert("RGB")
a = np.asarray(im).astype(int)
H, W, _ = a.shape
r, g, b = a[...,0], a[...,1], a[...,2]

def bbox_of(mask):
    ys, xs = np.nonzero(mask)
    if len(xs)==0: return None
    return (int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max()), int(mask.sum()))

def modal(x0,x1,y0,y1,n=4):
    reg = a[y0:y1, x0:x1].reshape(-1,3)
    return Counter(map(tuple, (reg//2*2))).most_common(n)

def comp_bboxes(mask, minpx=150, maxpx=60000):
    lab, n = ndimage.label(mask)
    out = []
    for i in range(1, n+1):
        m = lab == i
        s = int(m.sum())
        if not (minpx <= s <= maxpx): continue
        ys, xs = np.nonzero(m)
        out.append((int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max()), s))
    return sorted(out, key=lambda t: t[0])

# --- chain boxes: fill masks within band y200..275 ---
print("== chain box fill bboxes (band y200..275) ==")
band = np.zeros((H,W), bool); band[200:275,:] = True
for name, cond in [
    ("paleyellow", (r>238)&(g>238)&(b>200)&(b<235)&(r-b>18)),
    ("palecyan",   (g>232)&(b>232)&(r<232)&(g-r>12)),
    ("palegreen",  (g>238)&(r<238)&(b<238)&(g-r>10)&(g-b>10)&(abs(g-b)<20)),
    ("darkred",    (r>120)&(r<200)&(g<70)&(b<70)&(r-np.maximum(g,b)>80)),
    ("lavender",   (b>232)&(r>210)&(r<245)&(g<225)&(b-g>12)),
]:
    m = cond & band
    print(f"  {name}: components:", comp_bboxes(m, 300))

print("\n== chain box border colors (sample edges) ==")
# Pre processing box ~x148..248 y211..262: left border col ~148-149
print("  PreProc left edge modal (x147..151, y220..250):", modal(147,151,220,250,6))
print("  PreProc top edge modal (x160..240, y209..213):", modal(160,240,209,213,6))
print("  Cyan box left edge (x292..296, y220..250):", modal(292,296,220,250,6))
print("  Green box left edge (x441..445, y220..250):", modal(441,445,220,250,6))
print("  Lav box left edge (x752..756, y220..250):", modal(752,756,220,250,6))
print("  DarkRed box left edge (x574..578, y220..250):", modal(574,578,220,250,6))

print("\n== fill modals (box interiors) ==")
print("  PreProc fill:", modal(160,240,215,225))
print("  Cyan fill:", modal(310,390,215,225))
print("  Green fill:", modal(460,540,215,225))
print("  DarkRed fill (flat area y212..220 x620..700):", modal(620,700,212,220))
print("  Lav fill:", modal(770,840,215,225))

# --- ellipses ---
print("\n== Training Data ellipse ==")
peach = (r>236)&(g>200)&(g<235)&(b>160)&(b<215)&(r-g>12)&(g-b>15)
print("  peach comps:", comp_bboxes(peach, 500))
print("  peach fill modal (x120..170,y150..165):", modal(120,170,150,165))
# its outline: dark ring
print("  outline modal (sample bbox edge x88..92,y160..175):", modal(88,92,160,175,6))

print("\n== Final Result ellipse ==")
yel = (r>170)&(g>170)&(b<90)&(abs(r-g)<45)
print("  yellow comps:", comp_bboxes(yel, 300))
print("  yellow fill modal (x830..880,y320..335):", modal(830,880,320,335,6))
print("  ellipse outline modal (edge y308..312 x840..880):", modal(840,880,306,312,6))

# --- gray labels: border check ---
print("\n== gray label boxes ==")
print("  label1 fill modal (x250..320,y295..305):", modal(250,320,295,305))
print("  label1 top edge (x250..320,y289..293):", modal(250,320,289,293,6))
print("  label1 left edge (x239..243,y300..320):", modal(239,243,300,320,6))

# --- arrows: vertical thickness at gap midpoints ---
print("\n== straight arrows: vertical extent at given x ==")
for x in [258, 268, 278, 286, 424, 434, 566, 573, 748, 755]:
    col = a[200:275, x]
    redys = [200+i for i in range(75) if col[i][0]>130 and col[i][0]-max(col[i][1],col[i][2])>55]
    print(f"  x={x}: red y {redys}")

print("\n== curved arrow 1 trace (x90..150, y185..245) ==")
m = (r>130)&(r-np.maximum(g,b)>55)
sub = m[185:245, 90:150]
ys, xs = np.nonzero(sub)
pts = sorted(zip(xs+90, ys+185))
# print a few sample points per x
from itertools import groupby
for x, grp in groupby(pts, key=lambda t: t[0]):
    yy = [p[1] for p in grp]
    print(f"   x={x}: y {min(yy)}..{max(yy)} n={len(yy)}")

print("\n== curved arrow 2 trace (x825..890, y230..315) ==")
sub = m[230:315, 825:890]
ys, xs = np.nonzero(sub)
pts = sorted(zip(xs+825, ys+230))
for x, grp in groupby(pts, key=lambda t: t[0]):
    yy = [p[1] for p in grp]
    if x % 2 == 0 or len(yy)>3:
        print(f"   x={x}: y {min(yy)}..{max(yy)} n={len(yy)}")

# --- text ink in boxes (black) for font metrics ---
print("\n== black text ink bboxes ==")
ink = (r<110)&(g<110)&(b<110)
def inkbox(x0,x1,y0,y1,label):
    mm = np.zeros((H,W),bool); mm[y0:y1,x0:x1]=True
    bb = bbox_of(ink & mm)
    print(f"  {label}: {bb}")
inkbox(150,247,205,270,"PreProc text zone")
inkbox(295,405,205,270,"Cyan text zone")
inkbox(445,555,205,270,"Green text zone")
inkbox(580,742,205,270,"DarkRed white-text zone (invert)")
inkbox(755,855,205,270,"Lav text zone")
inkbox(90,200,135,200,"TrainingData ellipse text")
inkbox(800,895,310,350,"FinalResult text")
inkbox(240,330,291,332,"label1 text")
inkbox(694,782,291,332,"label4 text")
# white text in dark red box: white-ish inside box
whitem = (r>200)&(g>200)&(b>200)
mm = np.zeros((H,W),bool); mm[211:264, 578:742]=True
print("  Classification white-text bbox:", bbox_of(whitem & mm))

# gray labels text bbox all 4
for i,(x0,x1) in enumerate([(241,328),(386,473),(537,624),(694,781)],1):
    mm = np.zeros((H,W),bool); mm[291:332, x0:x1]=True
    print(f"  label{i} ink bbox:", bbox_of(ink & mm))
