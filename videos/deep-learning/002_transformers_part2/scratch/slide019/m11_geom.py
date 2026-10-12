# m11: precise geometry of pin, yellow band(s), dark-green vertical, leader lines.
from PIL import Image
import numpy as np

A, Bx, C, D = 20.9473, 0.95679, 2.2031, 0.95651
myI = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_019.jpg').convert('RGB')
parI = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_019.jpg').convert('RGB')
my = np.asarray(myI).astype(int)
wa = np.asarray(parI.transform((960, 540), Image.AFFINE, (1.0/Bx, 0, -A/Bx, 0, 1.0/D, -C/D), resample=Image.BILINEAR)).astype(int)

def to_build_f(fx, fy):
    f1x = (fx - A)/Bx; f1y = (fy - C)/D
    return (f1x + 2.998)/1.004491, (f1y + 1.812)/1.000708

def yellow_mask(img):
    r, g, b = img[...,0], img[...,1], img[...,2]
    return (r > 180) & (g > 180) & (b < 140)

def red_mask(img):
    r, g, b = img[...,0], img[...,1], img[...,2]
    return (r > 120) & (g < 90) & (b < 90)

for tag, img in [('MY', my), ('001', wa)]:
    ym = yellow_mask(img); ym[:46,:] = False; ym[514:,:] = False; ym[:, :60] = False; ym[:, 900:] = False
    ys, xs = np.where(ym)
    print(f'{tag} yellow px={len(xs)}')
    if len(xs):
        # row profile: count per row, find bands
        rows = np.bincount(ys, minlength=540)
        bands = []
        inb = False
        for y in range(46, 514):
            if rows[y] > 8 and not inb: inb, y0 = True, y
            elif rows[y] <= 8 and inb: inb = False; bands.append((y0, y-1))
        if inb: bands.append((y0, 513))
        for (y0, y1) in bands:
            sel = (ys >= y0) & (ys <= y1)
            print(f'  band rows {y0}..{y1}  x {xs[sel].min()}..{xs[sel].max()}  -> build y {to_build_f(0, y0)[1]:.1f}..{to_build_f(0, y1)[1]:.1f} x {to_build_f(xs[sel].min(), 0)[0]:.1f}..{to_build_f(xs[sel].max(), 0)[0]:.1f}')
    rm = red_mask(img); rm[:46,:] = False; rm[514:,:] = False; rm[:, :60] = False; rm[:, 900:] = False
    # pin: restrict to x 500..680, y 300..500 (away from title/arrows)
    rm2 = np.zeros_like(rm); rm2[300:500, 500:680] = rm[300:500, 500:680]
    ys2, xs2 = np.where(rm2)
    if len(xs2):
        print(f'{tag} pin-red px={len(xs2)} bbox x {xs2.min()}..{xs2.max()} y {ys2.min()}..{ys2.max()} -> build x {to_build_f(xs2.min(),0)[0]:.1f}..{to_build_f(xs2.max(),0)[0]:.1f} y {to_build_f(0,ys2.min())[1]:.1f}..{to_build_f(0,ys2.max())[1]:.1f}')
    else:
        print(f'{tag} pin-red px=0')

# dark-green vertical near frame x825: raw cuts
for fy in (220, 260, 300, 340, 380):
    print(f'MY cut fy={fy} x816..832:', ' '.join(f'{x}:{my[fy,x,0]},{my[fy,x,1]},{my[fy,x,2]}' for x in range(816, 833)))
    print(f'001 cut fy={fy} x816..832:', ' '.join(f'{x}:{wa[fy,x,0]},{wa[fy,x,1]},{wa[fy,x,2]}' for x in range(816, 833)))
