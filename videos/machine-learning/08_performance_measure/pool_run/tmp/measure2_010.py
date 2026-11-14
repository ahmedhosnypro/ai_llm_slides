from PIL import Image
import numpy as np
NS = '/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure'

def load(p):
    return np.asarray(Image.open(p).convert('RGB')).astype(int)

def masks(a):
    dark = a.sum(axis=2) < 300
    red = (a[:, :, 0] > 150) & (a[:, :, 0] - a[:, :, 1] > 70) & (a[:, :, 0] - a[:, :, 2] > 70)
    darknr = dark & ~red  # dark non-red (black text)
    blue = (a[:, :, 2] > 120) & (a[:, :, 2] - a[:, :, 0] > 50)
    green = (a[:, :, 1] > 100) & (a[:, :, 1] - a[:, :, 0] > 40) & (a[:, :, 1] - a[:, :, 2] > 40)
    return dark, red, darknr, blue, green

def bbox(x0, y0, x1, y1, mask):
    sub = np.zeros_like(mask); sub[y0:y1, x0:x1] = mask[y0:y1, x0:x1]
    ys, xs = np.where(sub)
    return (int(xs.min()), int(xs.max()), int(ys.min()), int(ys.max())) if len(xs) else None

def vlines(x0, x1, y0, y1, mask, thr=0.6):
    reg = mask[y0:y1, x0:x1]
    frac = reg.mean(axis=0)
    cols = np.where(frac > thr)[0] + x0
    # group consecutive
    groups = []
    if len(cols):
        s = cols[0]; p = cols[0]
        for c in cols[1:]:
            if c - p > 2: groups.append((s, p)); s = c
            p = c
        groups.append((s, p))
    return groups

def hlines(x0, x1, y0, y1, mask, thr=0.6):
    reg = mask[y0:y1, x0:x1]
    frac = reg.mean(axis=1)
    rows = np.where(frac > thr)[0] + y0
    groups = []
    if len(rows):
        s = rows[0]; p = rows[0]
        for r in rows[1:]:
            if r - p > 2: groups.append((s, p)); s = r
            p = r
        groups.append((s, p))
    return groups

for tag, path, S in [('ORIG', NS + '/unique_slides/slide_010.jpg', 1.0),
                     ('R5', NS + '/recreated_pptx/qa/slide010/render_5.png', 2001/960.0)]:
    a = load(path)
    dark, red, darknr, blue, green = masks(a)
    def B(x0, y0, x1, y1, m):  # bbox in ORIG px units
        b = bbox(int(x0*S), int(y0*S), int(x1*S), int(y1*S), m)
        return None if b is None else tuple(round(v/S, 1) for v in b)
    print(f'== {tag} S={S:.4f} ==')
    print(' question text (black):', B(70, 111, 656, 138, darknr), ' red rule:', B(70, 136, 656, 148, red))
    print(' meaning heading:', B(70, 199, 617, 233, darknr), ' meaning line2:', B(70, 233, 617, 258, darknr))
    print(' m1 vlines:', [(round(g[0]/S,1), round(g[1]/S,1)) for g in vlines(int(690*S), int(870*S), int(90*S), int(155*S), red|dark)],
          ' hlines:', [(round(g[0]/S,1), round(g[1]/S,1)) for g in hlines(int(690*S), int(870*S), int(90*S), int(155*S), red|dark)])
    print(' m2 vlines:', [(round(g[0]/S,1), round(g[1]/S,1)) for g in vlines(int(695*S), int(870*S), int(210*S), int(290*S), red|dark)],
          ' hlines:', [(round(g[0]/S,1), round(g[1]/S,1)) for g in hlines(int(695*S), int(870*S), int(210*S), int(290*S), red|dark)])
    # m2 left cell content x705-752 y220-250 (is there a P label inside?)
    print(' m2 left-top cell ink (black):', B(705, 220, 752, 250, darknr), ' red:', B(705, 220, 752, 250, red))
    print(' m2 18 cell fill bbox (peach):', end=' ')
    sub = a[int(220*S):int(250*S), int(705*S):int(801*S)].reshape(-1,3)
    m = (sub[:,0]>230)&(sub[:,1]>200)&(sub[:,1]<240)&(sub[:,2]>190)&(sub[:,2]<230)
    print(int(m.sum()))
    print(' m1 P hdr:', B(699, 78, 778, 96, darknr|red), ' m1 TP:', B(700, 97, 777, 121, darknr))
    print(' m2 18 text:', B(705, 220, 801, 250, darknr), ' m2 12 text:', B(801, 220, 857, 250, darknr))
    print(' tree Pos hdr:', B(560, 292, 700, 314, red), ' Neg hdr:', B(740, 292, 870, 314, green))
    print(' node30:', B(608, 377, 640, 409, darknr), ' node70:', B(792, 377, 824, 409, darknr))
    print(' leaf labels:', B(537, 473, 882, 496, darknr))
    print(' bottom text (interior):', B(80, 466, 494, 507, darknr|blue))
    print(' caption:', B(80, 393, 360, 416, darknr))
    print(' Recall=:', B(84, 275, 200, 310, darknr))
    # blue: strongest blue pixel in 60% region and Positive header
    for name, (x0, y0, x1, y1) in {'60pct': (414, 316, 458, 330), 'PosHdr': (588, 296, 678, 312), 'precLine1': (343, 297, 507, 312)}.items():
        sub = a[int(y0*S):int(y1*S), int(x0*S):int(x1*S)].reshape(-1, 3)
        score = sub[:, 2] - sub[:, 0]
        idx = np.argsort(score)[-30:]
        px = sub[idx]
        print(f' {name} strongest-blue median:', np.median(px, axis=0).astype(int).tolist())
    # yellow arrows: most saturated yellow in callout region
    sub = a[int(340*S):int(380*S), int(110*S):int(325*S)].reshape(-1, 3)
    score = (sub[:, 0] + sub[:, 1]) / 2 - sub[:, 2]
    m = score > 80
    if m.sum():
        print(' callout yellow median:', np.median(sub[m], axis=0).astype(int).tolist(), 'n=', int(m.sum()))
    # precision box line1 color (black?) and =60% blue already; check 'Precision=' text color
    sub = a[int(297*S):int(312*S), int(343*S):int(507*S)].reshape(-1, 3)
    print(' prec line1 darkest median:', np.median(sub[sub.sum(axis=1) < 400], axis=0).astype(int).tolist() if (sub.sum(axis=1) < 400).sum() else 'none')
