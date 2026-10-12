from PIL import ImageFont
def w(fontpath, size_pt, text):
    # size_pt at 72dpi = px
    f = ImageFont.truetype(fontpath, size_pt)
    return f.getbbox(text)[2] - f.getbbox(text)[0]

AR = "/usr/share/fonts/TTF/Arialbd.TTF"
LS = "/usr/lib/python3/site-packages/matplotlib/mpl-data/fonts/ttf/LiberationSerif-Regular.ttf"
import os
LS = None
for cand in ["/usr/share/fonts/liberation/LiberationSerif-Regular.ttf",
             "/usr/share/fonts/TTF/LiberationSerif-Regular.ttf"]:
    if os.path.exists(cand): LS = cand; break
LSB = LS.replace("-Regular", "-Bold")
CS = "/usr/share/fonts/TTF/Comic.TTF"
CSB = "/usr/share/fonts/TTF/Comicbd.TTF"
print("LS:", LS)
print("--- title 'Filters parameters' target 300px (333..633) ---")
for fp, nm in [(AR,"ArialBold"), (LSB,"TNRBold")]:
    for s in (34,36,38,40,42):
        print(f"  {nm} {s}pt: {w(fp,s,'Filters parameters'):.0f}")
print("--- line1 target 672px (102..774) ---")
t1 = "Number of parameters for different filters applied to same location in the image"
for s in (18,19,20,21,22):
    print(f"  TNR {s}pt: {w(LS,s,t1):.0f}")
print("--- line2 target 656px (102..758) ---")
runs = [("= ", 0), ("Filter size (2-D)", 1), (" * ", 0), ("Number of channels (K)", 1), ("  * ", 0), ("number of different filters", 1)]
for s in (18,19,20,21,22):
    tot = sum(w(LSB if b else LS, s, t) for t, b in runs)
    print(f"  TNR {s}pt (bold terms): {tot:.0f}")
print("--- line3 target 175px (102..277) '= 7*7  * 3  * 5  =735' ---")
runs3 = [("= ", 0), ("7*7", 1), ("  * ", 0), ("3", 1), ("  * ", 0), ("5", 1), ("  =735", 0)]
for s in (18,19,20,21,22):
    tot = sum(w(LSB if b else LS, s, t) for t, b in runs3)
    print(f"  TNR {s}pt: {tot:.0f}")
print("--- handwritten targets ---")
for s in (14,15,16,17):
    print(f"  Comic {s}pt 'RGB': {w(CSB,s,'RGB'):.0f}  (target ~64)")
for s in (16,18,20,22):
    print(f"  Comic {s}pt '735 weights': {w(CSB,s,'735 weights'):.0f}  (target ~168)")
for s in (12,14,16):
    print(f"  Comic {s}pt '3 dims': {w(CSB,s,'3 dims'):.0f}  (target ~36?)")
