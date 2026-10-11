from PIL import Image
import numpy as np
im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/recreated_pptx/qa/slide036/render_4.png').convert('RGB')
a = np.asarray(im).astype(int)
H,W = a.shape[:2]
K = W/960.0
lum = a.mean(axis=2)
fails=[]
def check(cond,msg):
    print(('PASS ' if cond else 'FAIL ')+msg)
    if not cond: fails.append(msg)

# 1. FRAME CONTAINMENT (fixed): ink must stay inside panel (42..918 x 45..540) +-3px,
# excluding the chrome panel border itself and the badge disc.
m = lum<200
Y,X = np.ogrid[:H,:W]
badge = ((X-893*K)**2+(Y-71*K)**2) <= (21*K)**2
panel = (X>(42-1)*K)&(X<(918+2)*K)&(Y>(45-1)*K)&(Y<539*K)
border_band = (np.abs(X-42*K)<=2.5*K)|(np.abs(X-918.5*K)<=2.5*K)|(np.abs(Y-45*K)<=2.5*K)
viol = m & ~panel & ~badge & ~border_band
viol[int(536*K):,:] = False  # bottom stroke half-visible is chrome
ys,xs = np.where(viol)
print('outside-panel content ink px:', len(xs))
if len(xs):
    print('  bbox frame: x%.0f..%.0f y%.0f..%.0f' % (xs.min()/K, xs.max()/K, ys.min()/K, ys.max()/K))
check(len(xs)<80, 'frame containment')

# 2. closed-loop equation bands vs ORIGINAL measured regions (tol 5 frame px)
def inkband(x0,y0,x1,y1):
    reg = a[int(y0*K):int(y1*K), int(x0*K):int(x1*K)]
    mm = reg.mean(axis=2)<190
    ys,xs = np.where(mm)
    if len(xs)==0: return None
    return (xs.min()/K+x0, ys.min()/K+y0, xs.max()/K+x0, ys.max()/K+y0)
regions = {
 'sqrt_d1 (L3)':      ((605,168,644,192),(610,170,633,187)),
 'sqrt_d2 (L4)':      ((605,197,644,221),(610,199,633,216)),
 'stmt1 sqrt-d tok':  ((300,243,336,272),(304,246,335,268)),
 'stmt2 4sqrt-d tok': ((649,243,697,272),(655,246,697,268)),
 'fbox3 sqrt-d':      ((780,316,812,346),(786,323,805,339)),
 'fbox1 w_ij inner':  ((393,318,407,356),(394,325,409,350)),
 'fbox2 fraction':    ((592,300,640,370),(592,306,634,369)),
}
for name,((x0,y0,x1,y1),(ex0,ey0,ex1,ey1)) in regions.items():
    bb = inkband(x0,y0,x1,y1)
    if bb is None: check(False, name+' EMPTY'); continue
    d = (abs(bb[0]-ex0),abs(bb[1]-ey0),abs(bb[2]-ex1),abs(bb[3]-ey1))
    check(max(d)<=5, f'{name} band {tuple(round(v) for v in bb)} vs orig d={tuple(round(v) for v in d)}')

# 3. delimiter full-bbox spans (measure the delimiter PNG region ink, not a narrow column)
def delimband(x0,y0,x1,y1,label):
    reg = a[int(y0*K):int(y1*K), int(x0*K):int(x1*K)]
    mm = reg.mean(axis=2)<200
    ys,xs = np.where(mm)
    if len(xs)==0: print(f'{label}: NO INK'); return None
    bb=(xs.min()/K+x0, ys.min()/K+y0, xs.max()/K+x0, ys.max()/K+y0)
    print(f'{label}: x{bb[0]:.0f}..{bb[2]:.0f} y{bb[1]:.0f}..{bb[3]:.0f}')
    return bb
for (x0,y0,x1,y1,exp,lab) in [
  (50,128,64,352,(51,132,62,349),'d v1L ('),
  (71,128,84,352,(72,132,80,349),'d v1L )'),
  (93,127,103,218,(94,131,100,214),'d v2L ('),
  (169,128,179,352,(170,132,176,349),'d v1R ('),
  (195,128,205,352,(196,132,202,349),'d v1R )'),
  (300,404,314,521,(301,408,307,517),'fc1L ('),
  (421,379,434,521,(422,383,428,517),'fc1R ('),
  (517,378,530,522,(518,382,524,518),'fc2a ('),
  (583,378,596,522,(586,382,591,518),'fc2b ('),
  (829,379,837,520,(832,383,836,516),'fc2d ('),
]:
    bb = delimband(x0,y0,x1,y1,lab)
    if bb:
        d = (abs(bb[0]-exp[0]),abs(bb[1]-exp[1]),abs(bb[2]-exp[2]),abs(bb[3]-exp[3]))
        check(max(d)<=7, f'{lab} span vs orig d={tuple(round(v) for v in d)}')

# 4. key text-band widths vs original (title/subtitle now fixed?)
def bandw(x0,y0,x1,y1,thr=190):
    reg = a[int(y0*K):int(y1*K), int(x0*K):int(x1*K)]
    mm = reg.mean(axis=2)<thr
    ys,xs = np.where(mm)
    if len(xs)==0: return None
    return (xs.min()/K+x0, ys.min()/K+y0, xs.max()/K+x0, ys.max()/K+y0)
t = bandw(150,48,860,76)
check(t and abs(t[0]-374)<=12 and abs(t[2]-616)<=12,
      f'title band {tuple(round(v) for v in t if t)} vs orig x374..616')
sb = bandw(120,79,860,102)
check(sb and abs(sb[0]-191)<=10 and abs(sb[2]-805)<=10,
      f'subtitle band {tuple(round(v) for v in sb if sb)} vs orig (191,78,805,101)')
l3 = bandw(320,164,608,190)
check(l3 and abs(l3[2]-602)<=12, f'eqbox L3 text right edge {l3[2] if l3 else None} vs orig 602')
l1 = bandw(318,116,600,138)
check(l1 and abs(l1[2]-569)<=12, f'eqbox L1 right edge {l1[2] if l1 else None} vs orig 569')
r1 = bandw(46,394,140,414)
check(r1 and abs(r1[2]-129)<=10, f'remember L1 right edge {r1[2] if r1 else None} vs orig 129')
s1 = bandw(338,240,600,272)
check(s1 and abs(s1[2]-585)<=14, f'stmt1 prose right edge {s1[2] if s1 else None} vs orig 585')

# 5. highlight present at subtitle start
reg = a[int(78*K):int(100*K), int((498-436.7)*K):int(300*K)]
yel = (reg[:,:,0]>230)&(reg[:,:,1]>230)&(reg[:,:,2]<120)
check(int(yel.sum())>500, f'subtitle highlight yellow px {int(yel.sum())}')

# 6. colors of key fills in render vs original-frame targets
def med(x0,y0,x1,y1):
    return tuple(np.median(a[int(y0*K):int(y1*K),int(x0*K):int(x1*K)].reshape(-1,3),axis=0).astype(int))
pairs = [
  ('EQBOX fill', (630,112,655,122), (254,255,253)),
  ('STMT1 fill', (570,245,592,258), (229,255,236)),
  ('STMT2 fill', (860,245,885,258), (255,248,215)),
  ('VEC fill',   (120,310,140,330), (252,255,228)),
  ('FC2 fill',   (645,478,700,492), (249,227,250)),
]
for name,(x0,y0,x1,y1),exp in pairs:
    got = med(x0,y0,x1,y1)
    check(all(abs(g-e)<=14 for g,e in zip(got,exp)), f'{name} fill {got} vs {exp}')

print()
print('FAILS:', len(fails))
for f in fails: print(' -', f)
