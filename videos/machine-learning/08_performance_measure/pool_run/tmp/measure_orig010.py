from PIL import Image
import numpy as np
NS = '/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure'
img = Image.open(NS + '/unique_slides/slide_010.jpg').convert('RGB')
a = np.asarray(img).astype(int)
print('orig size', a.shape)
dark = a.sum(axis=2) < 300
red = (a[:, :, 0] > 150) & (a[:, :, 0] - a[:, :, 1] > 70) & (a[:, :, 0] - a[:, :, 2] > 70)
blue = (a[:, :, 2] > 120) & (a[:, :, 2] - a[:, :, 0] > 50)
green = (a[:, :, 1] > 100) & (a[:, :, 1] - a[:, :, 0] > 40) & (a[:, :, 1] - a[:, :, 2] > 40)

def bbox(x0, y0, x1, y1, mask):
    sub = np.zeros_like(mask); sub[y0:y1, x0:x1] = mask[y0:y1, x0:x1]
    ys, xs = np.where(sub)
    return (int(xs.min()), int(xs.max()), int(ys.min()), int(ys.max()), int(len(xs))) if len(xs) else None

# 1. gray band question text
print('question text bbox:', bbox(70, 111, 656, 175, dark))
# 2. meaning box: heading + lines
print('meaning box all ink:', bbox(70, 199, 617, 258, dark))
# rows of ink in meaning box
sub = dark[199:258, 70:617]
rows = np.where(sub.any(axis=1))[0]
print('meaning ink rows (abs y):', (rows + 199).min(), (rows + 199).max())
# split into lines by gaps
lines = []
start = rows[0]; prev = rows[0]
for r in rows[1:]:
    if r - prev > 2:
        lines.append((start + 199, prev + 199)); start = r
    prev = r
lines.append((start + 199, prev + 199))
for (y0, y1) in lines:
    s2 = dark[y0:y1+1, 70:617]
    xs = np.where(s2.any(axis=0))[0]
    print(f'  meaning line y{y0}-{y1} h={y1-y0+1} x{xs.min()+70}-{xs.max()+70} w={xs.max()-xs.min()+1}')
# 3. red rule in gray panel: red pixels in band
print('red rule in band:', bbox(70, 111, 656, 175, red))
# 4. m1 grid lines: red or dark vertical/horizontal lines in x690-870 y90-155
reg = red[90:155, 690:870] | dark[90:155, 690:870]
cols = np.where(reg.any(axis=0))[0] + 690
rows = np.where(reg.any(axis=1))[0] + 90
print('m1 line cols:', cols.tolist())
print('m1 line rows:', rows.tolist())
# 5. m2 grid lines x695-870 y215-285
reg = red[215:285, 695:870] | dark[215:285, 695:870]
cols = np.where(reg.any(axis=0))[0] + 695
rows = np.where(reg.any(axis=1))[0] + 215
print('m2 line cols:', cols.tolist())
print('m2 line rows:', rows.tolist())
# 6. blue samples: Positive header ~ (588-678, 296), =60% (414-458, 316-330)
for name, (x0, y0, x1, y1) in {'Positive hdr': (588, 290, 678, 310), '60pct': (414, 316, 458, 330), 'precision line1': (343, 297, 507, 312)}.items():
    sub = a[y0:y1, x0:x1].reshape(-1, 3)
    m = (sub[:, 2] > sub[:, 0] + 40) & (sub[:, 2] > 100)
    if m.sum():
        px = sub[m]
        print(name, 'blue median RGB:', np.median(px, axis=0).astype(int).tolist(), 'n=', int(m.sum()))
# 7. yellow callout arrows: region x110-325 y340-380, find saturated yellow
sub = a[340:380, 110:325].reshape(-1, 3)
m = (sub[:, 0] > 180) & (sub[:, 1] > 150) & (sub[:, 2] < 120) & (sub[:, 0] - sub[:, 2] > 100)
if m.sum():
    print('callout yellow median RGB:', np.median(sub[m], axis=0).astype(int).tolist(), 'n=', int(m.sum()))
# 8. tree headings Positive/Negative y290-310
print('tree Positive hdr bbox:', bbox(560, 290, 700, 312, red))
print('tree Negative hdr bbox:', bbox(740, 290, 870, 312, green))
# 9. node labels: 30 at (624,393), 70 at (808,393) d=32
print('node30 label bbox:', bbox(610, 380, 640, 408, dark))
print('node70 label bbox:', bbox(794, 380, 824, 408, dark))
# 10. leaf labels y475-495
sub = dark[475:495, 537:882]
xs = np.where(sub.any(axis=0))[0] + 537
print('leaf labels x range:', xs.min(), xs.max())
# leaf label height
ys = np.where(sub.any(axis=1))[0] + 475
print('leaf label y:', ys.min(), ys.max(), 'h=', ys.max()-ys.min()+1)
# 11. bottom box text lines
sub = dark[462:511, 76:498]
rows = np.where(sub.any(axis=1))[0] + 462
lines = []
start = rows[0]; prev = rows[0]
for r in rows[1:]:
    if r - prev > 2:
        lines.append((start, prev)); start = r
    prev = r
lines.append((start, prev))
for (y0, y1) in lines:
    s2 = dark[y0:y1+1, 76:498]
    xs = np.where(s2.any(axis=0))[0] + 76
    print(f'  bottom line y{y0}-{y1} h={y1-y0+1} x{xs.min()}-{xs.max()} w={xs.max()-xs.min()+1}')
# 12. caption y402
print('caption bbox:', bbox(80, 395, 360, 415, dark))
# 13. recall box text 'Recall =' and precision line1 height
print('Recall= bbox:', bbox(84, 275, 200, 310, dark))
# 14. matrix lettering: m1 P/N headers and values
print('m1 hdr P bbox:', bbox(699, 80, 778, 96, dark | red))
print('m1 val TP bbox:', bbox(700, 96, 778, 122, dark))
print('m2 val 18 bbox:', bbox(705, 220, 801, 250, dark))
