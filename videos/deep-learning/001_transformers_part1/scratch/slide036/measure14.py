from PIL import Image
import numpy as np
im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_036.jpg').convert('RGB')
a = np.asarray(im).astype(int)

def colbands(x0,x1,y0,y1,label):
    print(label)
    reg = a[y0:y1, x0:x1]
    l = reg.mean(axis=2)
    ink = (l < 200).sum(axis=1)
    start=None
    for i,c in enumerate(ink):
        if c>=2 and start is None: start=i
        elif c<2 and start is not None:
            print('   band y%d..%d (h%d)' % (start+y0, i-1+y0, i-start)); start=None
    if start is not None: print('   band y%d..%d (h%d)' % (start+y0, y1-1, y1-start))

colbands(104,117,125,220,'LEFT V2 X-glyph column (x104..116):')
colbands(224,239,125,220,'RIGHT V2 M-glyph column (x224..238):')
colbands(178,193,125,345,'RIGHT V1 12-M column (x178..192):')
colbands(58,75,125,345,'LEFT V1 12-X column (x58..74):')
# count M glyphs = count bands; same for X
