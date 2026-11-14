from PIL import Image
import numpy as np
NS = '/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure'
rend = Image.open(NS + '/recreated_pptx/qa/slide010/render_4.png').convert('RGB')
rr = np.asarray(rend).astype(int)
S = rr.shape[1] / 960.0
dark = rr.sum(axis=2) < 300
red = (rr[:, :, 0] > 150) & (rr[:, :, 0] - rr[:, :, 1] > 70) & (rr[:, :, 0] - rr[:, :, 2] > 70)
purple = (rr[:, :, 0] > 80) & (rr[:, :, 0] < 170) & (rr[:, :, 2] > 120) & (rr[:, :, 2] - rr[:, :, 1] > 40)
blue = (rr[:, :, 2] > 150) & (rr[:, :, 2] - rr[:, :, 0] > 60)

sub = dark[int(220*S):int(280*S), int(681*S):int(699*S)]
print('m2 row-label col ink:', int(sub.sum()))
sub = dark[int(96*S):int(148*S), int(681*S):int(699*S)]
print('m1 row-label col ink:', int(sub.sum()))
sub = dark[int(96*S):int(148*S), int(673*S):int(681*S)]
print('m1 Actual col ink:', int(sub.sum()))
sub = np.zeros_like(purple); sub[int(215*S):int(255*S), int(700*S):int(862*S)] = purple[int(215*S):int(255*S), int(700*S):int(862*S)]
print('purple ring px in m2 top row:', int(sub.sum()))

def bbox(x0, y0, x1, y1, mask):
    sub = np.zeros_like(mask); sub[int(y0*S):int(y1*S), int(x0*S):int(x1*S)] = mask[int(y0*S):int(y1*S), int(x0*S):int(x1*S)]
    ys, xs = np.where(sub)
    return (round(float(xs.min())/S, 1), round(float(xs.max())/S, 1), round(float(ys.min())/S, 1), round(float(ys.max())/S, 1)) if len(xs) else None

print('m1 red grid:', bbox(673, 51, 867, 160, red), 'panel:', bbox(660, 45, 880, 165, blue))
print('m2 red grid:', bbox(674, 169, 867, 287, red), 'panel:', bbox(660, 163, 880, 293, blue))
# fraction in recall box
sub = dark[int(275*S):int(318*S), int(203*S):int(304*S)]
print('fraction zone ink:', int(sub.sum()))
# bottom box blue text
sub = blue[int(462*S):int(511*S), int(76*S):int(498*S)]
print('bottom box blue ink:', int(sub.sum()))
