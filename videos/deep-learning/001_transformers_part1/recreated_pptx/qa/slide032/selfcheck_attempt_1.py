# selfcheck_attempt_1.py — closed-loop PIL checks: render (2001x1125) vs frame (960x540)
# scale render->frame = 2001/960; tolerance ~4px @150dpi = ~1.92 frame px
import numpy as np
from PIL import Image
FR = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_032.jpg"
RN = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/recreated_pptx/qa/slide032/render_1.png"
f = np.asarray(Image.open(FR).convert("RGB")).astype(int)
r = np.asarray(Image.open(RN).convert("RGB")).astype(int)
S = r.shape[1] / f.shape[1]  # 2.0844
def ink_bbox(img, x0,y0,x1,y1, thr=68):
    # non-background ink inside region: pixel differs from local bg (white or gray)
    reg = img[y0:y1, x0:x1]
    mx = reg.max(axis=2); mn = reg.min(axis=2); sat = mx-mn
    white = (mx>=238)&(sat<=14)
    gray = (np.abs(reg[:,:,0]-reg[:,:,1])<=8)&(np.abs(reg[:,:,1]-reg[:,:,2])<=8)&(mx>=200)&(mx<246)
    ink = ~(white|gray)
    ys,xs = np.where(ink)
    if len(xs)==0: return None
    return (int(xs.min())+x0, int(ys.min())+y0, int(xs.max())+x0, int(ys.max())+y0)
def cmp(name, fb, rb):
    if fb is None or rb is None:
        print(f"{name:26s} MISSING ink frame={fb} render={rb}  FAIL"); return
    d = [ (rb[i]-fb[i])/S if i%2==0 else (rb[i]-fb[i])/S for i in range(4) ]
    # report in frame px
    dd = [d[i] for i in range(4)]
    ok = all(abs(v)<=2.0 for v in dd)
    print(f"{name:26s} frame x{fb[0]}..{fb[2]} y{fb[1]}..{fb[3]} | render/scale x{rb[0]/S:.1f}..{rb[2]/S:.1f} y{rb[1]/S:.1f}..{rb[3]/S:.1f} | d(framepx) dx0={dd[0]:+.1f} dy0={dd[1]:+.1f} dx1={dd[2]:+.1f} dy1={dd[3]:+.1f}  {'OK' if ok else 'FIX'}")
# regions (frame px)
regs = {
 "eq panel border": (50,62,475,282),
 "pill block": (64,100,215,152),
 "matrix": (212,78,382,266),
 "output column": (404,80,458,262),
 "X2 label": (108,150,150,192),
 "WQ label": (168,198,222,242),
 "equals": (378,158,408,192),
 "title": (550,115,860,144),
 "subtitle": (540,142,870,178),
 "arrow": (470,135,570,248),
 "net panel": (470,238,916,514),
 "band": (484,300,898,434),
 "out circle row": (500,248,895,310),
 "in circle row": (500,436,895,496),
}
for name,(x0,y0,x1,y1) in regs.items():
    fb = ink_bbox(f, x0,y0,x1,y1)
    rb = ink_bbox(r, int(x0*S),int(y0*S),int(x1*S),int(y1*S))
    cmp(name, fb, rb)
# color samples render vs frame (scaled points)
pts = {
 "eq panel fill": (300,90), "matrix cell fill": (240,92), "chip fill": (248,108),
 "outcell fill": (430,95), "band fill": (700,415), "out circle fill": (550,288),
 "in circle fill": (528,455), "canvas margin": (20,270), "chrome panel": (100,300),
}
print("\n-- color spot checks (frame vs render/scale) --")
for name,(x,y) in pts.items():
    fc = f[y,x]; rc = r[int(y*S),int(x*S)]
    print(f"{name:18s} frame #{fc[0]:02X}{fc[1]:02X}{fc[2]:02X}  render #{rc[0]:02X}{rc[1]:02X}{rc[2]:02X}")
# containment: any ink outside chrome panel (x42..918,y45..536) besides white canvas?
mxr = r.max(axis=2); mnr = r.min(axis=2); satr = mxr-mnr
nonwhite = ~((mxr>=238)&(satr<=14))
panel = np.zeros(r.shape[:2],bool)
panel[int(45*S):int(537*S), int(42*S):int(919*S)] = True
outside = nonwhite & ~panel
# exclude badge zone (badge is chrome, inside panel anyway)
ys,xs = np.where(outside)
print(f"\ncontainment: non-white ink px outside chrome panel = {len(xs)}")
if len(xs): 
    print("  sample outside ink at (frame px):", [(round(x/S,1),round(y/S,1)) for x,y in list(zip(xs,ys))[:12]])
