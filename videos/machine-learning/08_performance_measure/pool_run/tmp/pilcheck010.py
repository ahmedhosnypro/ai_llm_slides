from PIL import Image
import numpy as np

NS = '/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure'
orig = Image.open(NS + '/unique_slides/slide_010.jpg').convert('RGB')
rend = Image.open(NS + '/recreated_pptx/qa/slide010/render_1.png').convert('RGB')
print('orig', orig.size, 'render', rend.size)
ro = np.asarray(orig).astype(int)
rr = np.asarray(rend).astype(int)
S = rend.size[0] / orig.size[0]  # px per orig px
print('scale', S)

def ink(mask):
    ys, xs = np.where(mask)
    if len(xs) == 0:
        return None
    return xs.min(), xs.max(), ys.min(), ys.max()

dark_o = ro.sum(axis=2) < 300
dark_r = rr.sum(axis=2) < 300
bo = ink(dark_o); br = ink(dark_r)
print('orig ink bbox (px):', bo, '-> in:', [round(v/72, 2) for v in bo])
print('rend ink bbox (px):', br, '-> in:', [round(v/150, 2) for v in br])

# house frame containment: red frame at 0.15in -> 22.5px at 150dpi; check no dark ink outside frame+margin
frame = (22, 22, rend.size[0]-22, rend.size[1]-22)
outside = dark_r.copy()
outside[frame[1]:frame[3], frame[0]:frame[2]] = False
ys, xs = np.where(outside)
print('dark ink outside house frame:', len(xs), (xs.min(), xs.max(), ys.min(), ys.max()) if len(xs) else '')

# red frame presence in render
red_r = (rr[:, :, 0] > 150) & (rr[:, :, 0] - rr[:, :, 1] > 70) & (rr[:, :, 0] - rr[:, :, 2] > 70)
# check frame edges at 0.15in=22.5px and 13.18in=1977px, 7.35in=1102px
for name, sl in [('top', red_r[20:26, :]), ('bottom', red_r[1098:1106, :]), ('left', red_r[:, 20:26]), ('right', red_r[:, 1974:1982])]:
    print('frame', name, 'red px:', int(sl.sum()))

# badge: yellow oval near x=12.48in=1872px, y=0.30in=45px
yel = (rr[:, :, 0] > 240) & (rr[:, :, 1] > 230) & (rr[:, :, 2] < 180)
sub = yel[30:80, 1860:1935]
ys, xs = np.where(sub)
print('badge yellow px:', len(xs), 'bbox in render px:', (1860+xs.min(), 1860+xs.max(), 30+ys.min(), 30+ys.max()) if len(xs) else '')

# region checks: compare ink presence in key regions (orig px * S)
regions = {
    'gray band': (70, 111, 617, 174),
    'meaning box': (70, 199, 617, 258),
    'formula box': (70, 264, 316, 321),
    'fraction': (345, 291, 440, 330),
    'precision box': (337, 293, 525, 334),
    'callouts': (80, 320, 314, 371),
    'brace': (108, 387, 335, 401),
    'caption': (190, 410, 450, 430),
    'bottom box': (76, 462, 498, 511),
    'matrix1': (673, 51, 867, 160),
    'matrix2': (674, 169, 867, 287),
    'tree panel': (537, 292, 882, 503),
    'planes': (588, 318, 854, 374),
}
for name, (x0, y0, x1, y1) in regions.items():
    ro_sub = dark_o[y0:y1, x0:x1]
    rr_sub = dark_r[int(y0*S):int(y1*S), int(x0*S):int(x1*S)]
    print(f'{name}: orig ink {int(ro_sub.sum())} px, render ink {int(rr_sub.sum())} px')
