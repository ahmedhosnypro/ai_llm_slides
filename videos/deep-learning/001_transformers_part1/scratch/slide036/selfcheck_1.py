from PIL import Image
import numpy as np
im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/recreated_pptx/qa/slide036/render_1.png').convert('RGB')
a = np.asarray(im).astype(int)
H,W = a.shape[:2]
K = W/960.0  # render px per original-frame px
print(f'render {W}x{H}, K={K:.4f}')

def inkregion(x0,y0,x1,y1,label,thr=180):
    x0,y0,x1,y1 = [int(v*K) for v in (x0,y0,x1,y1)]
    reg = a[y0:y1, x0:x1]
    l = reg.mean(axis=2)
    m = l < thr
    ys,xs = np.where(m)
    if len(xs)==0:
        print(f'{label}: NO INK in ({x0},{y0})-({x1},{y1})'); return None
    bb = (xs.min()/K+x0/K, ys.min()/K+y0/K, xs.max()/K+x0/K, ys.max()/K+y0/K)
    print(f'{label}: ink x{bb[0]:.0f}..{bb[2]:.0f} y{bb[1]:.0f}..{bb[3]:.0f} (frame-px) n={len(xs)}')
    return bb

def colorat(x,y,label):
    c = a[int(y*K),int(x*K)]
    print(f'{label} @({x},{y}): rgb{tuple(c)}')

fails=[]
def check(cond,msg):
    print(('PASS ' if cond else 'FAIL ')+msg)
    if not cond: fails.append(msg)

# 1. FRAME CONTAINMENT: panel x42..918 y45..540 (frame px). Content ink must be inside.
# scan for ink outside panel (excluding chrome border rows/cols +-3)
lum = a.mean(axis=2)
out = lum<170
out[:int(95),:] = False; out[int(538*K):,:] = False
out[:,:int(89)] = False; out[:,int(1916):] = False
ys,xs = np.where(out)
print('content ink outside panel:', len(xs))
check(len(xs)<50, 'frame containment (no content ink outside panel)')

# 2. EQUATIONS EXIST (nonzero ink in each equation region)
inkregion(604,166,640,192,'eq sqrt_d1 (L3 tail)')
inkregion(604,195,640,220,'eq sqrt_d2 (L4 tail)')
inkregion(300,240,340,272,'eq sqrt_d stmt1')
inkregion(650,240,705,272,'eq 4sqrt_d stmt2')
inkregion(585,300,645,372,'eq fraction fbox2')
inkregion(782,318,810,344,'eq sqrt_d fbox3')
inkregion(390,312,410,356,'eq w_ij inner fbox1')

# 3. equation closed-loop: compare band edges vs original measured regions (tol 4 frame px)
regions = {
 'sqrt_d1': (604,166,640,192,(610,170,633,187)),
 'sqrt_d2': (604,195,640,220,(610,199,633,216)),
 'stmt1_sqrtd': (298,240,345,272,(305,246,335,268)),
 'stmt2_4sqrtd': (648,240,708,272,(655,246,700,268)),
 'fbox2_frac': (585,300,648,372,(590,306,645,369)),
 'fbox3_sqrtd': (780,318,812,344,(786,323,805,339)),
 'fbox1_wij': (386,310,412,358,(392,314,410,353)),
}
for name,(x0,y0,x1,y1,exp) in regions.items():
    bb = inkregion(x0,y0,x1,y1,f'band {name}')
    if bb:
        dx0=abs(bb[0]-exp[0]); dy0=abs(bb[1]-exp[1]); dx1=abs(bb[2]-exp[2]); dy1=abs(bb[3]-exp[3])
        ok = max(dx0,dy0,dx1,dy1) <= 5
        check(ok, f'{name} ink band vs original (d=({dx0:.0f},{dy0:.0f},{dx1:.0f},{dy1:.0f})) tol 5')

# 4. delimiter coverage: left paren ink top/bottom vs enclosed block
def colink(x,y0,y1,label):
    x = int(x*K); reg = a[int(y0*K):int(y1*K), max(0,x-2):x+3]
    l = reg.mean(axis=2); m=(l<200).sum(axis=1)
    ys = np.where(m>0)[0]
    if len(ys)==0: print(f'{label}: NO INK'); return None
    return (ys.min()/K+y0, ys.max()/K+y0)
r = colink(53,110,370,'VEC v1L ( stroke')
check(r and abs(r[0]-132)<=6 and abs(r[1]-349)<=6, f'VEC v1L left paren span {r} ~ y132..349')
r = colink(173,110,370,'VEC v1R ( stroke')
check(r and abs(r[0]-132)<=6 and abs(r[1]-349)<=6, f'VEC v1R left paren span {r}')
r = colink(303,395,525,'FC1 left ( stroke')
check(r and abs(r[0]-408)<=8 and abs(r[1]-517)<=8, f'FC1 left paren span {r}')
r = colink(519,375,525,'FC2 a ( stroke')
check(r and abs(r[0]-382)<=8 and abs(r[1]-518)<=8, f'FC2 a left paren span {r}')

# 5. region fills/colors
def medregion(x0,y0,x1,y1):
    reg = a[int(y0*K):int(y1*K), int(x0*K):int(x1*K)].reshape(-1,3)
    return tuple(np.median(reg,axis=0).astype(int))
print('EQBOX fill:', medregion(630,112,655,122), 'expect ~(255,255,255)')
print('STMT1 fill:', medregion(570,245,590,258), 'expect ~(230,252,236)')
print('STMT2 fill:', medregion(860,245,885,258), 'expect ~(255,248,215)')
print('VEC fill:', medregion(120,310,140,330), 'expect ~(252,255,228)')
print('FC2 fill:', medregion(640,480,700,495), 'expect ~(249,227,250)')
print('FC1 fill:', medregion(440,390,470,405), 'expect panel gray')
print('badge ring px:', colorat(893,53,'badge top ring'))

# 6. text bands present (title/subtitle/eqbox lines/remember lines)
inkregion(360,50,640,80,'title band')
inkregion(180,75,820,105,'subtitle band')
inkregion(318,116,575,138,'eqbox L1')
inkregion(318,139,575,160,'eqbox L2')
inkregion(320,166,606,190,'eqbox L3 text')
inkregion(320,195,606,219,'eqbox L4 text')
inkregion(46,396,135,415,'remember L1')
inkregion(100,412,170,432,'remember L2')
inkregion(50,430,220,452,'remember L3')
inkregion(100,460,170,480,'remember L4')
inkregion(50,478,220,498,'remember L5')
inkregion(340,420,410,450,'fc1 SoftMax label')
inkregion(630,425,690,452,'fc2 Scaled label')
inkregion(755,425,830,452,'fc2 SoftMax label')
inkregion(60,100,240,132,'vec headers row')
print()
print('FAILS:', len(fails))
for f in fails: print(' -', f)
