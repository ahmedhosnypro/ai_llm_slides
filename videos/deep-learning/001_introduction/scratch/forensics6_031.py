from PIL import Image, ImageFont
import numpy as np

im = Image.open("videos/deep-learning/001_introduction/unique_slides/slide_031.jpg").convert("RGB")
a = np.asarray(im).astype(int)
R,G,B = a[:,:,0],a[:,:,1],a[:,:,2]
blueish=(B-R>35)&(B>140)
reddish=(R-B>50)&(R-G>50)&(R>90)

def word_runs(mask, y0, y1, x0=90, x1=900, gap=4):
    m = mask[y0:y1+1, x0:x1]
    colc = m.sum(axis=0)
    runs=[]; s=None; last=None
    for i,v in enumerate(colc>0):
        if v:
            if s is None: s=i
            last=i
        else:
            if s is not None and i-last>gap:
                runs.append((x0+s, x0+last)); s=None
    if s is not None: runs.append((x0+s, x0+last))
    return runs

print("L1 words:", word_runs(blueish,142,160))
print("L2 words:", word_runs(blueish,195,211))
print("L3a words:", word_runs(blueish,220,242))
print("L3b words:", word_runs(blueish,246,268))
print("bullet1 words:", word_runs(reddish,302,323,120,600))
print("bullet2 words:", word_runs(reddish,341,357,120,600))
print("label words:", word_runs(blueish,445,464,370,620))

# ---- font metric solving ----
SERIF="/usr/share/fonts/liberation/LiberationSerif-Bold.ttf"
SANS="/usr/share/fonts/liberation/LiberationSans-Bold.ttf"
def ink(fontpath, text, fs):
    f = ImageFont.truetype(fontpath, int(round(fs*4)))  # 4x for precision
    bb = f.getbbox(text)
    return (bb[2]-bb[0])/4.0, (bb[3]-bb[1])/4.0, bb[1]/4.0, bb[3]/4.0  # w,h,top,bot (pt)

def solve(fontpath, text, meas_w, meas_h):
    # solve fs so ink width == meas_w; report predicted ink height
    w0,_,_,_ = ink(fontpath, text, 20)
    fs = 20*meas_w/w0
    w,h,top,bot = ink(fontpath, text, fs)
    return fs, w, h

cases = [
 ("title", "Where to Get Filters for Recognition", 599, 34),
 ("L1", "There are Several, handcrafted filters in computer vision", 569, 19),
 ("L2", "For example:", 131, 17),
]
splits3 = [
 ("A: ...smoothing, low- | level ...", "Canny, Sobel, Gaussian blur, smoothing, low-", "level segmentation, morphological filters, Gabor filters,..."),
 ("B: ...segmentation, | morphological ...", "Canny, Sobel, Gaussian blur, smoothing, low- level segmentation,", "morphological filters, Gabor filters,..."),
 ("C: ...morphological | filters ...", "Canny, Sobel, Gaussian blur, smoothing, low- level segmentation, morphological", "filters, Gabor filters,..."),
]
for name, path in [("SERIF",SERIF),("SANS",SANS)]:
    print(f"\n===== {name} =====")
    for cname, text, mw, mh in cases:
        fs,w,h = solve(path, text, mw, mh)
        print(f"  {cname}: solved fs={fs:.1f}  pred w={w:.0f} (target {mw})  pred ink h={h:.1f} (meas {mh})")
    for sname, t3a, t3b in splits3:
        fs_a,w_a,h_a = solve(path, t3a, 652, 23)
        fs_b,w_b,h_b = solve(path, t3b, 378, 23)
        print(f"  L3 {sname}: fs_a={fs_a:.1f} (h {h_a:.1f}) | fs_b={fs_b:.1f} (h {h_b:.1f})")
    for bname, text, mw, mh in [("bullet1","Are they optimal for recognition?",328,22),("bullet2","Can we learn them from our data?",329,17),("label","Filter Parameters",209,20)]:
        fs,w,h = solve(path, text, mw, mh)
        print(f"  {bname}: solved fs={fs:.1f}  pred ink h={h:.1f} (meas {mh})")
