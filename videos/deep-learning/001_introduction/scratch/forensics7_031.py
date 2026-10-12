from PIL import Image, ImageFont
import numpy as np

# word-run width data (measured from frame)
L1 = [("There",58),("are",32),("Several,",80),("handcrafted",122),("filters",58),("in",19),("computer",97),("vision",59)]
L3A = [("Canny,",70),("Sobel,",59),("Gaussian",92),("blur,",45),("smoothing,",110),("low-",41),("level",44),("segmentation,",138)]
L3B = [("morphological",143),("filters,",62),("Gabor",64),("filters,...",85)]
BUL = [("they",40),("optimal",75),("for",28),("recognition?",122),("we",26),("learn",50),("them",49),("from",47),("our",33),("data?",53)]
LAB = [("Filter",61),("Parameters",138)]
TIT = None

im = Image.open("videos/deep-learning/001_introduction/unique_slides/slide_031.jpg").convert("RGB")
a = np.asarray(im).astype(int)
R,G,B = a[:,:,0],a[:,:,1],a[:,:,2]
reddish=(R-B>50)&(R-G>50)&(R>90)
# title word runs
def word_runs(mask, y0, y1, x0, x1, gap=4):
    m = mask[y0:y1+1, x0:x1]; colc = m.sum(axis=0)
    runs=[]; s=None; last=None
    for i,v in enumerate(colc>0):
        if v:
            if s is None: s=i
            last=i
        else:
            if s is not None and i-last>gap: runs.append((x0+s, x0+last)); s=None
    if s is not None: runs.append((x0+s, x0+last))
    return runs
print("title words:", word_runs(reddish,87,120,150,820))
tl = (R-G>60)&(R-B>60)&(R>120)
tw = word_runs(tl,87,120,150,820)
print("title words loose:", tw)

FONTS = {
 "Serif-Bold": "/usr/share/fonts/liberation/LiberationSerif-Bold.ttf",
 "Sans-Bold": "/usr/share/fonts/liberation/LiberationSans-Bold.ttf",
 "Serif-Reg": "/usr/share/fonts/liberation/LiberationSerif-Regular.ttf",
 "Sans-Reg": "/usr/share/fonts/liberation/LiberationSans-Regular.ttf",
}
groups = {"body": L1+L3A+L3B+BUL, "label": LAB}
for fname, path in FONTS.items():
    f = ImageFont.truetype(path, 80)
    for gname, words in groups.items():
        # joint solve: fs minimizing sum((pred-meas)^2/meas^2)
        best=(1e9,0)
        for fs10 in range(150, 320):
            fs=fs10/10
            sse=0
            for w,meas in words:
                pred = f.getlength(w)*fs/80.0
                sse += (pred-meas)**2/meas**2
            if sse<best[0]: best=(sse,fs)
        sse,fs = best
        # per-word report at best fs
        errs = [ (w, round(f.getlength(w)*fs/80.0-meas,1)) for w,meas in words[:6] ]
        print(f"{fname:11s} {gname}: best fs={fs:.1f} relSSE={sse:.4f} errs(px) {errs}")
# title solve per font
title_text = "Where to Get Filters for Recognition"
tmeas = 599
for fname, path in FONTS.items():
    f = ImageFont.truetype(path, 80)
    best=(1e9,0)
    for fs10 in range(280, 440):
        fs=fs10/10
        pred = f.getlength(title_text)*fs/80.0
        sse=(pred-tmeas)**2
        if sse<best[0]: best=(sse,fs,pred)
    print(f"{fname:11s} title: fs={best[1]:.1f} pred w={best[2]:.0f} (meas 599)")
