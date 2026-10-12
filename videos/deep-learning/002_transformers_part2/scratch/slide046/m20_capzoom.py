from PIL import Image
import numpy as np
for fname, ys in [('046', range(500, 520)), ('045', range(494, 514))]:
    a = np.asarray(Image.open(f'videos/deep-learning/002_transformers_part2/unique_slides/slide_{fname}.jpg').convert('RGB')).astype(int)
    print(f'===== {fname} caption band: per-row spans of dark-navy (b>100,r<80,g<80) and dark-red-ish (r>90..180, g<80, b<80) and full-width scan =====')
    for y in ys:
        row = a[y]
        navy = [x for x in range(150, 910) if row[x][2]>100 and row[x][0]<80 and row[x][1]<80]
        maroon = [x for x in range(150, 910) if 80<row[x][0]<190 and row[x][1]<90 and row[x][2]<100]
        def spans(xs):
            if not xs: return []
            out=[]; s=xs[0]; p=xs[0]
            for x in xs[1:]:
                if x-p>4: out.append((s,p)); s=x
                p=x
            out.append((s,p)); return out
        print(f'  {fname} y={y}: navy spans {spans(navy)[:14]}')
        print(f'           maroon spans {spans(maroon)[:16]}')
