from PIL import Image
import numpy as np
im = Image.open("videos/deep-learning/001_introduction/unique_slides/slide_031.jpg").convert("RGB")
a = np.asarray(im).astype(int)
R,G,B = a[:,:,0],a[:,:,1],a[:,:,2]
dark = (R<110)&(G<110)&(B<110)

# theta glyphs only (exclude bracket columns 634-643 and 824-833)
inner = dark[390:505, 648:822]
rowc = inner.sum(axis=1)
on = rowc>0
bands=[]; s=None
for i,v in enumerate(on):
    if v and s is None: s=i
    if not v and s is not None:
        bands.append((s+390,i-1+390)); s=None
if s is not None: bands.append((s+390,504))
print("theta-ink row bands (x648..822):", bands)

# bracket vertical extent + width profile
br = dark[390:505, 630:648]
rows = np.where(br.any(axis=1))[0]
print("left bracket ink y:", 390+rows[0], "..", 390+rows[-1])
cols = np.where(br.any(axis=0))[0]
print("left bracket ink x:", 630+cols[0], "..", 630+cols[-1])

# one theta glyph bbox (col1 row1 region)
g = dark[390:440, 646:680]
rows = np.where(g.any(axis=1))[0]; cols = np.where(g.any(axis=0))[0]
print("first theta glyph bbox: x", 646+cols[0],"..",646+cols[-1]," y",390+rows[0],"..",390+rows[-1])

# bullet dot vertical extent
reddish = (R-B>50)&(R-G>50)&(R>90)
d = reddish[295:330, 133:152]
rows = np.where(d.any(axis=1))[0]
print("bullet dot y extent:", 295+rows[0],"..",295+rows[-1])

# blue text left edge per line + color sample of text ink
blueish=(B-R>35)&(B>140)
for (y0,y1,label) in [(142,161,"L1"),(195,212,"L2"),(220,243,"L3a"),(246,269,"L3b")]:
    m = blueish[y0:y1, :]
    cols=np.where(m.any(axis=0))[0]
    # darkest pixel in band
    band = a[y0:y1, cols[0]:cols[-1]+1]
    lum = band.sum(axis=2)
    iy,ix = np.unravel_index(lum.argmin(), lum.shape)
    print(f"{label}: x {cols[0]}..{cols[-1]}  darkest px {tuple(band[iy,ix])}")
# bullet text color
band = a[302:324, 152:470]; lum=band.sum(axis=2)
iy,ix=np.unravel_index(lum.argmin(),lum.shape)
print("bullet1 darkest px:", tuple(band[iy,ix]))
# title color
band = a[87:121, 180:779]; lum=band.sum(axis=2)
iy,ix=np.unravel_index(lum.argmin(),lum.shape)
print("title darkest px:", tuple(band[iy,ix]))
# matrix glyph color
band = a[397:495, 634:834]; lum=band.sum(axis=2)
iy,ix=np.unravel_index(lum.argmin(),lum.shape)
print("matrix darkest px:", tuple(band[iy,ix]))
# label text color
band = a[445:465, 388:597]; lum=band.sum(axis=2)
iy,ix=np.unravel_index(lum.argmin(),lum.shape)
print("label darkest px:", tuple(band[iy,ix]))
# red frame line + red box border color
band = a[300:310, 55:62]; print("red frame line mean:", band.reshape(-1,3).mean(axis=0).round(0))
band = a[440:460, 840:845]; print("matrix right border mean:", band.reshape(-1,3).mean(axis=0).round(0))
