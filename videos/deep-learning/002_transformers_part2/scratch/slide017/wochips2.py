from PIL import Image
import numpy as np
F = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_017.jpg").convert("RGB")
a = np.asarray(F).astype(int)
r, g, b = a[:,:,0], a[:,:,1], a[:,:,2]
# tinted chip fills: pinkish FCE8E8/F2C8F0, greenish E8FCE8, bluish E8E8F8?
pink = (r>235)&(g<225)&(b<235)&(r-b>8)&(r-g>12)
grn  = (g>235)&(r<235)&(g-r>8)&(g-b>8)
blu  = (b>235)&(r<235)&(b-r>8)&(b-g>8)
for name, m in [("pink", pink), ("green", grn), ("blue", blu)]:
    mm = m[330:525, 570:810]
    ys, xs = np.where(mm)
    if len(xs)==0: print(name, "none"); continue
    print(name, "n=%d x %d..%d y %d..%d" % (len(xs), xs.min()+570, xs.max()+570, ys.min()+330, ys.max()+330))
    # column clusters
    import collections
    colc = collections.Counter((x+570)//20*20 for x in xs)
    print("   x-clusters:", dict(sorted(colc.items())))
# headpanels: dashed green borders x 595..810 y 230..480
grnb = (g>110)&(r<140)&(b<140)&(g-r>40)&(g-b>40)
mm = grnb[230:480, 595:810]
ys, xs = np.where(mm)
print("headpanel green dash n=%d" % len(xs))
if len(xs):
    import collections
    colc = collections.Counter((x+595)//20*20 for x in xs)
    print("   x-clusters:", dict(sorted(colc.items())))
    rowc = collections.Counter((y+230)//20*20 for y in ys)
    print("   y-clusters:", dict(sorted(rowc.items())))
