from PIL import Image
import numpy as np
NS = '/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure'

def load(p):
    return np.asarray(Image.open(p).convert('RGB')).astype(int)

def get_masks(a):
    dark = a.sum(axis=2) < 300
    red = (a[:, :, 0] > 150) & (a[:, :, 0] - a[:, :, 1] > 70) & (a[:, :, 0] - a[:, :, 2] > 70)
    blue = (a[:, :, 2] > 120) & (a[:, :, 2] - a[:, :, 0] > 50)
    green = (a[:, :, 1] > 100) & (a[:, :, 1] - a[:, :, 0] > 40) & (a[:, :, 1] - a[:, :, 2] > 40)
    white = (a[:, :, 0] > 225) & (a[:, :, 1] > 225) & (a[:, :, 2] > 225)
    black = dark & ~red
    anydark = dark
    return {'black': black, 'red': red, 'blue': blue, 'green': green, 'white': white, 'anydark': anydark}

def bbox(a, masks, x0, y0, x1, y1, mk, S):
    m = masks[mk]
    sub = np.zeros_like(m); sub[int(y0*S):int(y1*S), int(x0*S):int(x1*S)] = m[int(y0*S):int(y1*S), int(x0*S):int(x1*S)]
    ys, xs = np.where(sub)
    if not len(xs): return None
    return (round(float(xs.max()-xs.min()+1)/S,1), round(float(ys.max()-ys.min()+1)/S,1))

# name, x0,y0,x1,y1, mask, current fontSize
ELS = [
 ('band1', 70,111,656,138,'black',16),
 ('band2', 70,144,656,175,'black',16),
 ('meaningH', 70,199,617,233,'anydark',20),
 ('meaningL2', 70,233,617,258,'black',14),
 ('recall', 84,275,200,310,'black',16),
 ('precision', 341,297,410,312,'black',11),
 ('pct60', 414,316,458,330,'blue',11),
 ('callout1', 115,346,212,376,'black',10),
 ('callout2', 223,346,320,376,'black',10),
 ('caption', 89,402,349,422,'anydark',13),
 ('bottom', 80,466,494,507,'anydark',13),
 ('predas1', 740,58,850,75,'red',11),
 ('predas2', 740,172,850,188,'red',11),
 ('m1hdrP', 738,78,790,96,'red',11),
 ('m1hdrN', 790,78,844,96,'red',11),
 ('m2hdrP', 738,196,790,216,'red',11),
 ('m2hdrN', 790,196,844,216,'red',11),
 ('m1rowP', 700,99,737,124,'red',11),
 ('m1rowN', 700,127,737,150,'red',11),
 ('m2rowP', 706,222,745,250,'red',11),
 ('m2rowN', 706,254,745,280,'red',11),
 ('m1TP', 740,99,789,124,'black',12),
 ('m1FN', 792,99,843,124,'black',12),
 ('m1FP', 740,127,789,150,'black',12),
 ('m1TN', 792,127,843,150,'black',12),
 ('m2v18', 748,222,799,250,'black',12),
 ('m2v12', 802,222,855,250,'black',12),
 ('m2v10', 748,254,799,280,'black',12),
 ('m2v60', 802,254,855,280,'black',12),
 ('actual1', 668,97,698,151,'red',10),
 ('actual2', 682,220,704,282,'red',10),
 ('treePos', 560,292,700,314,'red',16),
 ('treeNeg', 740,292,870,314,'green',16),
 ('node30', 610,380,640,408,'white',12),
 ('node70', 794,380,824,408,'white',12),
 ('node18', 564,442,594,470,'white',12),
 ('leaf', 537,473,882,496,'anydark',11),
]

orig = load(NS + '/unique_slides/slide_010.jpg')
r5 = load(NS + '/recreated_pptx/qa/slide010/render_5.png')
S = 2001/960.0
mo = get_masks(orig); mr = get_masks(r5)
print(f'{"name":10s} {"origW":>6s} {"origH":>6s} {"r5W":>6s} {"r5H":>6s} {"kW":>5s} {"kH":>5s} {"k":>5s} {"cur":>4s} {"new":>5s}')
for name, x0, y0, x1, y1, mk, cur in ELS:
    bo = bbox(orig, mo, x0, y0, x1, y1, mk, 1.0)
    br = bbox(r5, mr, x0, y0, x1, y1, mk, S)
    if bo is None or br is None or br[0] == 0 or br[1] == 0:
        print(f'{name:10s} orig={bo} r5={br}  <-- MISSING')
        continue
    kw = bo[0]/br[0]; kh = bo[1]/br[1]; k = (kw+kh)/2
    print(f'{name:10s} {bo[0]:6.1f} {bo[1]:6.1f} {br[0]:6.1f} {br[1]:6.1f} {kw:5.2f} {kh:5.2f} {k:5.2f} {cur:4d} {cur*k:5.1f}')

# color samples from ORIGINAL
def sample(a, x0, y0, x1, y1, cond):
    sub = a[y0:y1, x0:x1].reshape(-1, 3)
    m = cond(sub)
    if not m.sum(): return None
    px = sub[m]
    return np.median(px, axis=0).astype(int).tolist(), int(m.sum())

print('orig 60pct blue (b-r>60):', sample(orig, 414, 316, 458, 330, lambda s: (s[:,2]-s[:,0] > 60)))
print('orig bottom text blue (b-r>60):', sample(orig, 80, 466, 494, 507, lambda s: (s[:,2]-s[:,0] > 60)))
print('orig callout yellow (r+g)/2-b>80:', sample(orig, 110, 340, 325, 380, lambda s: ((s[:,0]+s[:,1])/2 - s[:,2]) > 80))
print('orig callout1 box fill:', sample(orig, 120, 350, 205, 372, lambda s: (s.sum(axis=1) > 600)))
print('orig callout2 box fill:', sample(orig, 228, 350, 313, 372, lambda s: (s.sum(axis=1) > 600)))
print('orig m2 peach fill:', sample(orig, 748, 224, 798, 248, lambda s: (s[:,0]>230)&(s[:,1]>200)&(s[:,1]<240)&(s[:,2]>190)&(s[:,2]<230)))
print('orig m2 orange fill:', sample(orig, 802, 224, 854, 248, lambda s: (s[:,0]>230)&(s[:,1]>150)&(s[:,1]<200)&(s[:,2]<160)))
print('orig m1 lime fill:', sample(orig, 740, 99, 789, 124, lambda s: (s[:,0]>100)&(s[:,0]<200)&(s[:,1]>200)&(s[:,2]<100)))
print('orig m2 lime fill:', sample(orig, 802, 254, 854, 280, lambda s: (s[:,0]>100)&(s[:,0]<200)&(s[:,1]>200)&(s[:,2]<100)))
# purple ring bbox
purp = (orig[:,:,0]>80)&(orig[:,:,0]<170)&(orig[:,:,2]>120)&(orig[:,:,2]-orig[:,:,1]>40)
sub = np.zeros_like(purp); sub[215:255, 700:862] = purp[215:255, 700:862]
ys, xs = np.where(sub)
print('orig purple ring bbox:', xs.min(), xs.max(), ys.min(), ys.max(), 'n=', len(xs))
# m1/m2 panel borders blue sample
print('orig panel border blue:', sample(orig, 672, 53, 674, 157, lambda s: (s[:,2]-s[:,0] > 50)))
# R5 callout arrow color
print('r5 callout yellow:', sample(r5, int(110*S), int(340*S), int(325*S), int(380*S), lambda s: ((s[:,0]+s[:,1])/2 - s[:,2]) > 80))
