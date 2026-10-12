# fit_fonts_037.py — PIL metric fit for slide 037 text blocks (frame px, 1px=1pt).
from PIL import ImageFont

F = "/usr/share/fonts/TTF/"
ARIAL_B = F + "Arialbd.TTF"
TIMES = F + "Times.TTF"
TIMES_B = F + "Timesbd.TTF"
GEORGIA = F + "Georgia.TTF"
GEORGIA_B = F + "Georgiab.TTF"
COMIC = F + "Comic.TTF"

print("== TITLE Arial Bold: 'How many filter can we apply on the image' target ink w=709 (x128..837), cap band 80..104 (24px), desc to 112 ==")
st = "How many filter can we apply on the image"
for size in range(29, 37):
    f = ImageFont.truetype(ARIAL_B, size)
    bb = f.getbbox(st)
    capH = f.getbbox("H")[3] - f.getbbox("H")[1]
    ydesc = f.getbbox("y")[3] - f.getbbox("y")[1]
    print(f"  {size}pt: ink w={bb[2]-bb[0]} (x0={bb[0]}), H cap={capH}, y desc-below-baseline~{ydesc}, ink h={bb[3]-bb[1]}")

def runs_width(segs, font_reg, font_bold, size):
    w = 0
    for text, bold in segs:
        f = ImageFont.truetype(font_bold if bold else font_reg, size)
        bb = f.getbbox(text)
        w += bb[2] - bb[0]
    return w

L1 = [("We can Apply ", False), ("multiple filters", True), (" on the ", False),
      ("same location", True), (" (e.g. 5 different filters on", False)]
L2 = [("the same location.  For Example:", False)]
L3 = [("[ one to ", False), ("detect edges", True), (", one to ", False), ("detect lines", True),
      (", one to ", False), ("detect curves", True), (", ...etc)", False)]

for name, segs, target in [("L1", L1, 803), ("L2", L2, 336), ("L3", L3, 718)]:
    print(f"== YELLOW BOX {name}: target ink w={target} ==")
    for fam_reg, fam_b, fam in [(TIMES, TIMES_B, "Times"), (GEORGIA, GEORGIA_B, "Georgia")]:
        for size in range(17, 25):
            w = runs_width(segs, fam_reg, fam_b, size)
            print(f"  {fam} {size}pt: mixed-run w={w}")

print("== QUESTION Comic Sans: 'How many weights for these 5 neurons?' target ink w=510 (x73..583), ink band 453..483 ==")
sq = "How many weights for these 5 neurons?"
for size in range(20, 32):
    f = ImageFont.truetype(COMIC, size)
    bb = f.getbbox(sq)
    capH = f.getbbox("H")[3] - f.getbbox("H")[1]
    print(f"  {size}pt: ink w={bb[2]-bb[0]} (x0={bb[0]}), H cap={capH}, ink h={bb[3]-bb[1]}")
