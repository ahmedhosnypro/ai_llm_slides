from PIL import Image
import numpy as np
NS = '/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure'
rend = Image.open(NS + '/recreated_pptx/qa/slide010/render_5.png').convert('RGB')
rr = np.asarray(rend).astype(int)
S = rr.shape[1] / 960.0
print('render size', rr.shape, 'S=', S)
dark = rr.sum(axis=2) < 300
red = (rr[:, :, 0] > 150) & (rr[:, :, 0] - rr[:, :, 1] > 70) & (rr[:, :, 0] - rr[:, :, 2] > 70)
purple = (rr[:, :, 0] > 80) & (rr[:, :, 0] < 170) & (rr[:, :, 2] > 120) & (rr[:, :, 2] - rr[:, :, 1] > 40)
blue = (rr[:, :, 2] > 150) & (rr[:, :, 2] - rr[:, :, 0] > 60)
green = (rr[:, :, 1] > 110) & (rr[:, :, 1] - rr[:, :, 0] > 40) & (rr[:, :, 1] - rr[:, :, 2] > 40)
grayfill = (abs(rr[:, :, 0] - 217) < 12) & (abs(rr[:, :, 1] - 217) < 12) & (abs(rr[:, :, 2] - 217) < 12)

def bbox(x0, y0, x1, y1, mask):
    sub = np.zeros_like(mask); sub[int(y0*S):int(y1*S), int(x0*S):int(x1*S)] = mask[int(y0*S):int(y1*S), int(x0*S):int(x1*S)]
    ys, xs = np.where(sub)
    return (round(float(xs.min())/S, 1), round(float(xs.max())/S, 1), round(float(ys.min())/S, 1), round(float(ys.max())/S, 1)) if len(xs) else None

# 1. Actual gutter: red ink between Actual label col and grid left edge (m1 grid gx=699, m2 gx=705)
sub = red[int(90*S):int(155*S), int(682*S):int(697*S)]
print('m1 red ink in gutter x682-697:', int(sub.sum()))
sub = red[int(210*S):int(285*S), int(683*S):int(703*S)]
print('m2 red ink in gutter x683-703:', int(sub.sum()))
# Actual label ink present
sub = dark[int(96*S):int(148*S), int(674*S):int(682*S)]
print('m1 Actual col ink:', int(sub.sum()))
sub = dark[int(220*S):int(280*S), int(675*S):int(683*S)]
print('m2 Actual col ink:', int(sub.sum()))
# row label ink
sub = dark[int(96*S):int(148*S), int(684*S):int(698*S)]
print('m1 row-label col ink:', int(sub.sum()))
sub = dark[int(220*S):int(280*S), int(684*S):int(704*S)]
print('m2 row-label col ink:', int(sub.sum()))

# 2. purple ring bbox in m2 top row, must be inside grid right edge 857
print('purple ring m2 top row bbox:', bbox(700, 215, 862, 255, purple))
print('m2 red grid bbox:', bbox(674, 169, 867, 287, red))
print('m1 red grid bbox:', bbox(673, 51, 867, 160, red))

# 3. node 70 center x (green circle near y393)
print('node70 green bbox:', bbox(760, 380, 860, 406, green))
print('node30 red bbox:', bbox(590, 380, 660, 406, red))

# 4. gray band right edge vs meaning panel right edge (617)
print('gray band bbox:', bbox(60, 105, 700, 180, grayfill))

# fraction zone ink, bottom blue ink
sub = dark[int(275*S):int(318*S), int(203*S):int(304*S)]
print('fraction zone ink:', int(sub.sum()))
sub = blue[int(462*S):int(511*S), int(76*S):int(498*S)]
print('bottom box blue ink:', int(sub.sum()))
# tree leaf labels row y481
sub = dark[int(475*S):int(495*S), int(537*S):int(882*S)]
print('leaf label ink:', int(sub.sum()))
