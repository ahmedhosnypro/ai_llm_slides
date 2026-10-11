import numpy as np
from PIL import Image

im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_023.jpg').convert('RGB')
a = np.asarray(im).astype(int)
R, G, B = a[...,0], a[...,1], a[...,2]

blue = (B > R + 60) & (B > G + 60) & (B > 120)
red = (R > G + 60) & (R > B + 60) & (R > 120)
green = (G > R + 50) & (G > B + 50) & (G > 100)
dark = (R < 130) & (G < 130) & (B < 130)
ink = blue | red | green | dark

def bbox(m, x0, x1, y0, y1):
    sub = m[y0:y1+1, x0:x1+1]
    ys, xs = np.nonzero(sub)
    if len(ys) == 0: return None
    return (x0+int(xs.min()), x0+int(xs.max()), y0+int(ys.min()), y0+int(ys.max()), len(ys))

def pr(name, v):
    print(f'  {name}: {v}')

print('== LEFT CIRCLE (center 193,250.5) ==')
pr('axes horiz dark bbox', bbox(dark, 40, 335, 246, 255))
pr('axes vert dark bbox', bbox(dark, 186, 200, 115, 390))
pr('blue ink bbox x194..330 y180..260', bbox(blue, 194, 330, 180, 260))
pr('red ink bbox x194..330 y225..250', bbox(red, 194, 330, 225, 250))
pr('red ink bbox x194..330 y200..245', bbox(red, 194, 330, 200, 245))
pr('green ink bbox x170..330 y180..260', bbox(green, 170, 330, 180, 260))
pr('blue label bbox x194..330 y140..200', bbox(blue, 194, 330, 140, 200))
pr('red label bbox x250..330 y195..240', bbox(red, 250, 330, 195, 240))
pr('circle fill bbox', bbox((R>245)&(G>245)&(B>180)&(B<228), 60, 330, 120, 380))

print('== RIGHT CIRCLE (center 635.5,250.5) ==')
pr('axes horiz dark bbox', bbox(dark, 480, 780, 246, 255))
pr('axes vert dark bbox', bbox(dark, 628, 643, 115, 390))
pr('blue ink bbox x636..780 y180..260', bbox(blue, 636, 780, 180, 260))
pr('red ink bbox x636..780 y225..250', bbox(red, 636, 780, 225, 250))
pr('red ink bbox x636..780 y200..245', bbox(red, 636, 780, 200, 245))
pr('green ink bbox x610..780 y180..260', bbox(green, 610, 780, 180, 260))
pr('blue label bbox x636..780 y140..200', bbox(blue, 636, 780, 140, 200))
pr('red label bbox x690..780 y195..240', bbox(red, 690, 780, 195, 240))
pr('circle fill bbox', bbox((R>245)&(G>245)&(B>180)&(B<228), 480, 780, 120, 380))

print('== BLUE VECTOR ANGLE FITS ==')
for name, (cx, cy) in (('left', (193, 250)), ('right', (635, 250))):
    sub = blue[cy-80:cy+1, cx:cx+100]
    ys, xs = np.nonzero(sub)
    if len(ys):
        # exclude label: keep pixels whose distance from center < 80 and on a line from center
        pts = [(x, y) for x, y in zip(xs, ys)]
        ang = np.degrees(np.arctan2(-np.array([p[1] for p in pts]), np.array([p[0] for p in pts])))
        print(f'  {name} blue: n={len(pts)} ymin={ys.min()} ymax={ys.max()} xmin={xs.min()} xmax={xs.max()}')
        print(f'    angle range: {ang.min():.1f}..{ang.max():.1f}, median {np.median(ang):.1f}')
for name, (cx, cy) in (('left', (193, 250)), ('right', (635, 250))):
    sub = red[cy-40:cy+1, cx:cx+130]
    ys, xs = np.nonzero(sub)
    if len(ys):
        ang = np.degrees(np.arctan2(-np.array(ys), np.array(xs)))
        print(f'  {name} red: n={len(ys)} ymin={ys.min()} xmin={xs.min()} xmax={xs.max()} angles {ang.min():.1f}..{ang.max():.1f} median {np.median(ang):.1f}')

print('== EQUATION BOXES (clean) ==')
def linebands(m, x0, x1, y0, y1, mino=1):
    proj = m[y0:y1+1, x0:x1+1].sum(axis=1)
    idx = np.nonzero(proj > mino)[0]
    out = []
    if len(idx):
        s = idx[0]; p = idx[0]
        for i in idx[1:]:
            if i > p + 2: out.append((int(s), int(p))); s = i
            p = i
        out.append((int(s), int(p)))
    return [(y0 + r[0], y0 + r[1]) for r in out]

print(' treq x744..912 y84..184:')
for b in linebands(ink, 744, 912, 84, 184):
    print('   band y', b, 'cols', bbox(ink, 744, 912, b[0], b[1]))
print(' bceq x298..525 y326..424:')
for b in linebands(ink, 298, 525, 326, 424):
    print('   band y', b, 'cols', bbox(ink, 298, 525, b[0], b[1]))
print(' aftnorm x752..905 y318..378:')
for b in linebands(ink, 752, 905, 318, 378):
    print('   band y', b, 'cols', bbox(ink, 752, 905, b[0], b[1]))
print(' callout x298..531 y106..174:')
for b in linebands(ink, 298, 531, 106, 174):
    print('   band y', b, 'cols', bbox(ink, 298, 531, b[0], b[1]))
print(' cyanbar x60..858 y438..486:')
for b in linebands(ink, 60, 858, 438, 486):
    print('   band y', b, 'cols', bbox(ink, 60, 858, b[0], b[1]))
print(' maxbox x116..521 y502..530:')
for b in linebands(ink, 116, 521, 502, 530):
    print('   band y', b, 'cols', bbox(ink, 116, 521, b[0], b[1]))
print(' lossbox x573..761 y502..530:')
for b in linebands(ink, 573, 761, 502, 530):
    print('   band y', b, 'cols', bbox(ink, 573, 761, b[0], b[1]))

print('== COLOR SAMPLES ==')
for name, (x, y) in [('circle fill', (150, 200)), ('cyan bar fill', (400, 460)),
                     ('bar border top', (400, 433)), ('bar border left', (54, 460)),
                     ('callout border top', (400, 102)), ('callout border left', (294, 140)),
                     ('treq border top', (800, 80)), ('bceq border top', (400, 322)),
                     ('aftnorm border top', (800, 314)), ('arrow fill', (420, 245)),
                     ('arrow outline top', (420, 230)), ('title ink', (300, 80)),
                     ('panel bg', (30, 300)), ('canvas', (20, 20))]:
    print(f'  {name} @({x},{y}):', tuple(a[y, x]))
