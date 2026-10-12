from PIL import Image, ImageFont
import numpy as np
from collections import Counter
import glob

# find Arial-metric font
cands = glob.glob('/usr/share/fonts/**/LiberationSans-Regular.ttf', recursive=True) + \
        glob.glob('/usr/share/fonts/**/Arial*.ttf', recursive=True) + \
        glob.glob('/usr/share/fonts/**/Helvetica*.ttf', recursive=True)
print("font candidates:", cands[:5])

im0 = Image.open('videos/deep-learning/001_introduction/unique_slides/slide_010.jpg').convert('RGB')
b = np.asarray(im0).astype(int)
im = Image.open('videos/deep-learning/001_introduction/unique_slides/slide_012.jpg').convert('RGB')
a = np.asarray(im).astype(int)

def redcols(arr, label):
    out={}
    for x in range(20, 950):
        n = sum(1 for y in range(0,540) if arr[y,x,0]-arr[y,x,1]>60 and arr[y,x,0]-arr[y,x,2]>60 and arr[y,x,0]>110)
        if n>30: out[x]=n
    print(label, "red cols:", out)
redcols(a, "slide012")
redcols(b, "slide010")

# title box fill resample (above text: rows 85..98, x 110..350)
print("\ntitle fill (clean zone):", Counter(tuple(a[y,x]) for y in range(86,98) for x in range(110,350,3)).most_common(3))

# header black col profile rows 167..181: find word gaps x 356..600
prof = {}
for x in range(356, 610):
    prof[x] = sum(1 for y in range(167,182) if a[y,x].sum()<430)
runs=[]; s=None
for x in range(356, 610):
    if prof[x]>0:
        if s is None: s=x
        e=x
    else:
        if s is not None and x-s>0: runs.append((s,e)); s=None
if s: runs.append((s,609))
print("\nheader black word-runs:", runs)

# italic check: P stem slant, x 380..395 rows 167..182
print("\n'P' zone rows 167..182 (x 378..398) dark cols:")
for y in range(167, 183):
    dk=[x for x in range(376,400) if a[y,x].sum()<430]
    if dk: print(" row",y,dk)

# underline precise: rows 182..185 x 370..600 (sum<560)
for y in [182,183,184,185]:
    dk=[x for x in range(340,620) if a[y,x].sum()<560]
    print(" underline row",y, (dk[0],dk[-1],len(dk)) if dk else None)

# bullet stem widths: 'R' of Rotation x 127..140 rows 236..248
print("\nbullet1 'R' stem col profile x 125..142, rows 236..248:")
for x in range(125,143):
    n=sum(1 for y in range(236,249) if a[y,x].sum()<430)
    print("  col",x,n, end="; ")
print()
# red stem: 'F' x 128..142 rows 169..180
print("red 'F' stem col profile x 126..144:")
for x in range(126,145):
    n=sum(1 for y in range(169,181) if a[y,x,0]-a[y,x,1]>70 and a[y,x,0]>120)
    print("  col",x,n, end="; ")
print()
# title 'F' stem x 125..140 rows 102..116
print("title 'F' stem col profile x 123..142:")
for x in range(123,143):
    n=sum(1 for y in range(102,117) if a[y,x].sum()<430)
    print("  col",x,n, end="; ")
print()

# bullet2 full row profile (baseline)
print("\nbullet2 rows 278..298 ink counts:")
for y in range(278,299):
    ink=sum(1 for x in range(127,340) if a[y,x].sum()<430)
    print("  row",y,ink)
