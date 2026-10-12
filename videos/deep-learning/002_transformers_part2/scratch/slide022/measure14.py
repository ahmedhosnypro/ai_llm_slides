from PIL import Image
import numpy as np
im = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_022.jpg').convert('RGB')).astype(int)
R, G, B = im[:,:,0], im[:,:,1], im[:,:,2]
red = (R-G>40)&(R-B>40)&(R>120)

# all red pixel columns below row-3 boxes (y 294..300) -> +delta glyphs
sub = red[294:301, 160:892]
colfrac = sub.mean(axis=0)
xs = np.arange(160, 892)
on = colfrac > 0.15
runs, s = [], None
for i, v in enumerate(on):
    if v and s is None: s = i
    if not v and s is not None: runs.append((s+160, i-1+160)); s = None
print("+delta glyph column runs y[294,300]:", runs)
# red pixel rows for each glyph cluster (vertical extent)
for a,b in runs:
    blk = red[290:305, a:b+1]
    ys = np.where(blk.any(axis=1))[0]
    print(f"  glyph x[{a},{b}] rows {290+ys.min()}..{290+ys.max()}")

# ARROWS: saturated non-red non-cream pixels in the 5 gaps + last gap, y 264..300
def gap_scan(a, b, lbl):
    found = {}
    for x in range(a, b+1):
        for y in range(262, 303):
            r,g,bb = im[y,x]
            if not ((r>235 and g>215 and bb>185) or (abs(r-g)<22 and abs(g-bb)<22 and r>170)):
                found.setdefault(y//4, []).append((x, (r,g,bb)))
    print(f"{lbl} gap x[{a},{b}]:", {k*4: v[:3] for k,v in sorted(found.items())[:8]})
for (a,b,lbl) in [(236,249,"gap1"),(307,326,"gap2"),(384,398,"gap3"),(456,473,"gap4"),(531,545,"gap5"),(796,807,"gap6")]:
    gap_scan(a,b,lbl)
