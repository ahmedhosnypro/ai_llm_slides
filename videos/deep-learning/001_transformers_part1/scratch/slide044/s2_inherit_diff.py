from PIL import Image
import numpy as np
a = np.asarray(Image.open("scratch/slide044/out/probe-1.png").convert("RGB"), dtype=np.int16)  # base only
b = np.asarray(Image.open("recreated_pptx/qa/slide044/render_1.png").convert("RGB"), dtype=np.int16)
print("shapes", a.shape, b.shape)
d = np.abs(a-b).max(axis=2)
mask = d > 30
ys, xs = np.where(mask)
print("delta px:", int(mask.sum()))
if mask.sum():
    print("bbox x", xs.min(), "..", xs.max(), " y", ys.min(), "..", ys.max())
    # expected zones (render px = frame px * 2000/960):
    # title zone: frame x482..892 y46..104 -> render x1004..1858 y96..217
    # inset zone: frame x733..914 y75..303 -> render x1527..1900 y156..631
    def in_zone(x,y):
        title = (1000<=x<=1865) and (90<=y<=220)
        inset = (1520<=x<=1905) and (150<=y<=640)
        return title or inset
    out = [(x,y) for x,y in zip(xs,ys) if not in_zone(x,y)]
    print("delta px OUTSIDE expected zones:", len(out))
    if out:
        ox = np.array([p[0] for p in out]); oy = np.array([p[1] for p in out])
        print("  outside bbox x", ox.min(), ox.max(), "y", oy.min(), oy.max(), "count", len(out))
        # sample some
        import collections
        cc = collections.Counter(((x//50*50, y//50*50) for x,y in out))
        print("  clusters:", cc.most_common(10))
