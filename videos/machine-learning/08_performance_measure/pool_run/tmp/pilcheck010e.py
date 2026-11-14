from PIL import Image
import numpy as np
NS = '/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure'
orig = np.asarray(Image.open(NS + '/unique_slides/slide_010.jpg').convert('RGB')).astype(int)
r6 = np.asarray(Image.open(NS + '/recreated_pptx/qa/slide010/render_6.png').convert('RGB')).astype(int)
S = r6.shape[1] / 960.0

def masks(a):
    dark = a.sum(axis=2) < 300
    red = (a[:, :, 0] > 150) & (a[:, :, 0] - a[:, :, 1] > 70) & (a[:, :, 0] - a[:, :, 2] > 70)
    blue = (a[:, :, 2] > 120) & (a[:, :, 2] - a[:, :, 0] > 50)
    green = (a[:, :, 1] > 100) & (a[:, :, 1] - a[:, :, 0] > 40) & (a[:, :, 1] - a[:, :, 2] > 40)
    black = dark & ~red
    return {'black': black, 'red': red, 'blue': blue, 'green': green, 'dark': dark}

mo, mr = masks(orig), masks(r6)

def bbox(a, m, x0, y0, x1, y1, S):
    sub = np.zeros_like(m); sub[int(y0*S):int(y1*S), int(x0*S):int(x1*S)] = m[int(y0*S):int(y1*S), int(x0*S):int(x1*S)]
    ys, xs = np.where(sub)
    if not len(xs): return None
    return (round((xs.max()-xs.min()+1)/S,1), round((ys.max()-ys.min()+1)/S,1), round((xs.min()+xs.max())/2/S,1), round((ys.min()+ys.max())/2/S,1))

ELS = [
 ('band1', 70,111,656,138,'black'), ('band2', 70,144,656,175,'black'),
 ('rule', 70,136,656,148,'red'),
 ('meaningH', 70,199,617,233,'dark'), ('meaningL2', 70,233,617,258,'black'),
 ('recall', 84,275,200,310,'black'), ('precision', 341,297,410,312,'black'),
 ('pct60', 414,316,458,330,'blue'),
 ('callout1', 115,346,212,376,'black'), ('caption', 89,402,349,422,'dark'),
 ('bottom', 80,466,494,507,'blue'),
 ('predas1', 740,58,850,75,'red'), ('predas2', 740,172,850,188,'red'),
 ('m1hdrP', 740,76,788,96,'red'), ('m1hdrN', 792,76,842,96,'red'),
 ('m2hdrP', 740,194,788,216,'red'), ('m2hdrN', 792,194,842,216,'red'),
 ('m1rowP', 700,99,737,124,'red'), ('m1rowN', 700,127,737,150,'red'),
 ('m2rowP', 706,222,745,250,'red'), ('m2rowN', 706,254,745,280,'red'),
 ('m1TP', 740,99,789,124,'black'), ('m1FN', 792,99,843,124,'black'),
 ('m1FP', 740,127,789,150,'black'), ('m1TN', 792,127,843,150,'black'),
 ('m2v18', 748,222,799,250,'black'), ('m2v12', 802,222,855,250,'black'),
 ('m2v10', 748,254,799,280,'black'), ('m2v60', 802,254,855,280,'black'),
 ('actual1', 668,97,698,151,'red'), ('actual2', 668,220,698,283,'red'),
 ('treePos', 560,292,700,314,'red'), ('treeNeg', 740,292,870,314,'green'),
 ('leaf', 537,473,882,496,'dark'),
]
print(f'{"name":10s} {"orig(W,H,cx,cy)":>24s} {"r6(W,H,cx,cy)":>24s}')
for name, x0, y0, x1, y1, mk in ELS:
    bo = bbox(orig, mo[mk], x0, y0, x1, y1, 1.0)
    br = bbox(r6, mr[mk], x0, y0, x1, y1, S)
    print(f'{name:10s} {str(bo):>24s} {str(br):>24s}')

# grid lines in r6
def vlines(a, m, x0, x1, y0, y1, S, thr=0.6):
    reg = m[int(y0*S):int(y1*S), int(x0*S):int(x1*S)]
    frac = reg.mean(axis=0)
    cols = np.where(frac > thr)[0] + int(x0*S)
    groups = []
    if len(cols):
        st = cols[0]; p = cols[0]
        for c in cols[1:]:
            if c - p > int(2*S): groups.append((round(st/S,1), round(p/S,1))); st = c
            p = c
        groups.append((round(st/S,1), round(p/S,1)))
    return groups
def hlines(a, m, x0, x1, y0, y1, S, thr=0.6):
    reg = m[int(y0*S):int(y1*S), int(x0*S):int(x1*S)]
    frac = reg.mean(axis=1)
    rows = np.where(frac > thr)[0] + int(y0*S)
    groups = []
    if len(rows):
        st = rows[0]; p = rows[0]
        for r in rows[1:]:
            if r - p > int(2*S): groups.append((round(st/S,1), round(p/S,1))); st = r
            p = r
        groups.append((round(st/S,1), round(p/S,1)))
    return groups
redr = mr['red'] | mr['dark']
print('r6 m1 vlines:', vlines(r6, redr, 690, 870, 95, 153, S), 'hlines:', hlines(r6, redr, 690, 870, 95, 153, S))
print('r6 m2 vlines:', vlines(r6, redr, 695, 870, 218, 285, S), 'hlines:', hlines(r6, redr, 695, 870, 218, 285, S))
print('orig m1 vlines:', vlines(orig, mo['red']|mo['dark'], 690, 870, 95, 153, 1.0), 'hlines:', hlines(orig, mo['red']|mo['dark'], 690, 870, 95, 153, 1.0))
print('orig m2 vlines:', vlines(orig, mo['red']|mo['dark'], 695, 870, 218, 285, 1.0), 'hlines:', hlines(orig, mo['red']|mo['dark'], 695, 870, 218, 285, 1.0))
# purple ring in r6
purp = (r6[:,:,0]>80)&(r6[:,:,0]<170)&(r6[:,:,2]>120)&(r6[:,:,2]-r6[:,:,1]>40)
sub = np.zeros_like(purp); sub[int(218*S):int(255*S), int(700*S):int(862*S)] = purp[int(218*S):int(255*S), int(700*S):int(862*S)]
ys, xs = np.where(sub)
print('r6 purple ring bbox:', round(xs.min()/S,1), round(xs.max()/S,1), round(ys.min()/S,1), round(ys.max()/S,1), 'n=', len(xs))
# node70 center
gr = mr['green']
sub = np.zeros_like(gr); sub[int(380*S):int(406*S), int(760*S):int(860*S)] = gr[int(380*S):int(406*S), int(760*S):int(860*S)]
ys, xs = np.where(sub)
print('r6 node70 green center x:', round((xs.min()+xs.max())/2/S,1), '(target 808)')
# fraction ink
sub = mr['dark'][int(275*S):int(318*S), int(203*S):int(304*S)]
print('r6 fraction zone ink:', int(sub.sum()))
