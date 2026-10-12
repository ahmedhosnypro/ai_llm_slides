from PIL import Image
import numpy as np
im = Image.open('videos/deep-learning/001_introduction/unique_slides/slide_022.jpg').convert('RGB')
a = np.asarray(im).astype(int)
r, g, b = a[:,:,0], a[:,:,1], a[:,:,2]

# fine map of callout zone x595..830 y385..485, cell 3
def cls(px):
    rr,gg,bb = px
    if rr<90 and gg<90 and bb<90: return "K"      # black
    if rr>150 and rr-gg>45 and rr-bb>40: return "R"
    if rr>190 and gg>190 and bb<215 and rr-bb>18: return "t"  # tan-ish fill
    if abs(rr-232)<16 and abs(gg-232)<16 and abs(bb-232)<16: return "."
    if rr>235 and gg>235 and bb>235: return " "
    return "?"
print("callout zone (K=black R=red t=tan .=gray ' '=white ?=other)")
hdr = "     " + "".join(str(((595+i*3)//10)%10) for i in range((830-595)//3))
print(hdr)
for y in range(385, 486, 3):
    row = ""
    for x in range(595, 830, 3):
        # modal class in 3x3
        from collections import Counter
        c = Counter(cls(a[y+dy, x+dx]) for dy in range(3) for dx in range(3))
        row += c.most_common(1)[0][0]
    print(f"{y:4d} " + row)

# tan fill: most saturated percentile
tan_zone = a[400:440, 640:800].reshape(-1,3)
tanpx = np.array([p for p in tan_zone if p[0]-p[2] > 12])
print("\ntan fill n=", len(tanpx), " modal:", Counter(map(tuple, tanpx)).most_common(4))
