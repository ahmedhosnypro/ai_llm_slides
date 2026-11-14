#!/usr/bin/env python3
from PIL import Image
NS = '/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure'
orig = Image.open(f'{NS}/unique_slides/slide_024.jpg').convert('RGB')
rend = Image.open(f'{NS}/recreated_pptx/qa/slide024/render_7.png').convert('RGB').resize((960, 540), Image.LANCZOS)

def is_red(p):
    r, g, b = p
    return r > 140 and r > g + 60 and r > b + 60

top = sum(1 for x in range(60, 900) if is_red(rend.getpixel((x, 82))))
bot = sum(1 for x in range(60, 900) if is_red(rend.getpixel((x, 500))))
lft = sum(1 for y in range(83, 500) if is_red(rend.getpixel((59, y))))
rgt = sum(1 for y in range(83, 500) if is_red(rend.getpixel((899, y))))
print('inner frame runs top/bot/left/right:', top, bot, lft, rgt)
print('panel fill (500,150):', rend.getpixel((500, 150)), 'orig:', orig.getpixel((500, 150)))

def ink(img, x0, y0, x1, y1):
    n = 0
    for y in range(y0, y1):
        for x in range(x0, x1):
            r, g, b = img.getpixel((x, y))
            if not (r > 245 and g > 245 and b > 245):
                n += 1
    return n

for name, box in {'plane7': (633, 295, 774, 356), 'plane3': (112, 234, 214, 288),
                  'testplane': (341, 130, 405, 170), 'gauge': (530, 128, 566, 162)}.items():
    print(name, 'ink orig:', ink(orig, *box), 'render:', ink(rend, *box))

def dashed(img):
    ys = [y for y in range(190, 470) if sum(1 for x in range(473, 484) if sum(img.getpixel((x, y))) < 560) >= 2]
    return (min(ys), max(ys)) if ys else None

print('dashed extent orig:', dashed(orig), 'render:', dashed(rend))

def redblob(img):
    pts = [(x, y) for y in range(185, 225) for x in range(475, 515) if is_red(img.getpixel((x, y)))]
    if not pts:
        return None
    return (min(p[0] for p in pts), max(p[0] for p in pts), min(p[1] for p in pts), max(p[1] for p in pts))

print('thr marker orig:', redblob(orig), 'render:', redblob(rend))

def titlew(img):
    pts = [x for y in range(8, 82) for x in range(100, 860) if is_red(img.getpixel((x, y)))]
    return (min(pts), max(pts)) if pts else None

print('title x-extent orig:', titlew(orig), 'render:', titlew(rend))
print('render lower matrix hlines:')
for y in range(150, 230):
    run = sum(1 for x in range(90, 232) if is_red(rend.getpixel((x, y))))
    if run > 25:
        print('  y=', y, 'run=', run)
print('bg:', rend.getpixel((500, 520)), 'outer frame:', rend.getpixel((11, 270)))
