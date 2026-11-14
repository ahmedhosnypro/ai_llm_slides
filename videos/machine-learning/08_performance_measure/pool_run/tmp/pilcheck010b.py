from PIL import Image
import numpy as np

NS = '/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure'
rend = Image.open(NS + '/recreated_pptx/qa/slide010/render_3.png').convert('RGB')
rr = np.asarray(rend).astype(int)
H, W, _ = rr.shape
S = W / 960.0  # render px per orig px
print('render', rend.size, 'scale', S)

dark = rr.sum(axis=2) < 300
red = (rr[:, :, 0] > 150) & (rr[:, :, 0] - rr[:, :, 1] > 70) & (rr[:, :, 0] - rr[:, :, 2] > 70)
blue = (rr[:, :, 2] > 150) & (rr[:, :, 2] - rr[:, :, 0] > 60)

# 1. nothing outside house frame (frame at 0.15in)
out = dark.copy(); out[int(0.20*150):int(7.30*150), int(0.20*150):int(13.13*150)] = False
ys, xs = np.where(out)
print('ink outside frame:', len(xs))

# 2. region ink presence (orig px -> render px)
regions = {
    'gray band': (70, 111, 617, 174), 'meaning': (70, 199, 617, 258),
    'recall box': (69, 263, 319, 323), 'fraction in box': (203, 275, 304, 318),
    'precision box': (335, 290, 528, 337), 'callout L': (115, 318, 212, 376),
    'callout R': (223, 318, 320, 376), 'brace': (108, 387, 335, 401),
    'caption': (89, 402, 349, 422), 'bottom box': (76, 462, 498, 511),
    'matrix1': (673, 51, 867, 160), 'matrix2': (674, 169, 867, 287),
    'tree panel': (537, 289, 882, 503), 'planes': (588, 318, 854, 374),
    'nodes': (556, 377, 876, 469), 'leaf labels': (556, 481, 876, 499),
}
for name, (x0, y0, x1, y1) in regions.items():
    sub = dark[int(y0*S):int(y1*S), int(x0*S):int(x1*S)]
    print(f'{name}: ink {int(sub.sum())}')

# 3. matrix containment: red grid must be inside blue panel
def bbox_in(x0, y0, x1, y1, mask):
    sub = np.zeros_like(mask); sub[int(y0*S):int(y1*S), int(x0*S):int(x1*S)] = mask[int(y0*S):int(y1*S), int(x0*S):int(x1*S)]
    ys, xs = np.where(sub)
    return (xs.min()/S, xs.max()/S, ys.min()/S, ys.max()/S) if len(xs) else None

print('matrix1 red grid bbox (orig px):', bbox_in(673, 51, 867, 160, red))
print('matrix2 red grid bbox (orig px):', bbox_in(674, 169, 867, 287, red))
print('matrix1 blue border bbox:', bbox_in(660, 45, 880, 165, blue))
print('matrix2 blue border bbox:', bbox_in(660, 163, 880, 293, blue))

# 4. fraction present inside recall box (dark ink in fraction zone)
sub = dark[int(275*S):int(318*S), int(203*S):int(304*S)]
print('fraction zone ink:', int(sub.sum()))
# 5. precision box: no dark ink above its top edge (stray ink check) y 280-290
sub = dark[int(280*S):int(290*S), int(335*S):int(528*S)]
print('stray ink above precision box:', int(sub.sum()))
# 6. badge
yel = (rr[:, :, 0] > 245) & (rr[:, :, 1] > 240) & (rr[:, :, 2] > 180) & (rr[:, :, 2] < 215)
sub = yel[int(0.28*150):int(0.82*150), int(12.46*150):int(13.0*150)]
print('badge yellow px:', int(sub.sum()))
