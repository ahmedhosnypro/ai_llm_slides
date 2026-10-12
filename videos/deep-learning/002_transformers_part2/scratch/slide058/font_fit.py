#!/usr/bin/env python3
"""Fit Arial Bold em size per title segment from frame ink widths (slide-2 certified mapping)."""
from PIL import ImageFont, ImageDraw, Image

FONT = "/usr/share/fonts/TTF/Arialbd.TTF"
A, SX, SY = 18.63, 0.96123, 0.95556  # slide-2 certified mapping

def to_slide(fx): return (fx - A) / SX
def to_slide_y(fy): return fy / SY

# frame ink segments (x0,x1) from word-run analysis
segs = {
    "L1 full 'Transformer Encoder'": (224, 697),
    "L1 'Transformer'": (224, 497),
    "L1 'Encoder'": (513, 697),
    "L2 full 'as a Classifier'": (318, 631),
    "L2 'as'": (318, 367),
    "L2 'a'": (384, 409),
    "L2 'Classifier'": (423, 631),
}
texts = {
    "L1 full 'Transformer Encoder'": "Transformer Encoder",
    "L1 'Transformer'": "Transformer",
    "L1 'Encoder'": "Encoder",
    "L2 full 'as a Classifier'": "as a Classifier",
    "L2 'as'": "as",
    "L2 'a'": "a",
    "L2 'Classifier'": "Classifier",
}

font100 = ImageFont.truetype(FONT, 100)
img = Image.new("L", (2000, 300))
draw = ImageDraw.Draw(img)

print(f"{'segment':34s} {'ink_slide_pt':>12s} {'em_fit':>7s}")
ems = []
for k, (x0, x1) in segs.items():
    bbox = draw.textbbox((0, 0), texts[k], font=font100)  # anchor 'la'
    ink100 = bbox[2] - bbox[0]
    w_slide = (x1 - x0 + 1) / SX
    em = w_slide / (ink100 / 100)
    ems.append(em)
    print(f"{k:34s} {w_slide:12.2f} {em:7.2f}")
print("em mean", round(sum(ems) / len(ems), 2), "spread", round(max(ems) - min(ems), 2))

# ink heights: L1 y 229..264, L2 y 282..317 (36 px each) -> slide 37.7 tall
h1 = (264 - 229 + 1) / SY
h2 = (317 - 282 + 1) / SY
for t in ["Transformer Encoder", "as a Classifier"]:
    bb = draw.textbbox((0, 0), t, font=font100)
    print(f"'{t}' ink h at em: {h1:.1f}pt -> em_h = {h1 / ((bb[3]-bb[1]) / 100):.2f}")

# ink top positions in slide pts
print("L1 ink top/bottom slide:", round(to_slide_y(229), 2), round(to_slide_y(264.999), 2))
print("L2 ink top/bottom slide:", round(to_slide_y(282), 2), round(to_slide_y(317.999), 2))
# centers
print("L1 cx:", round((to_slide(224) + to_slide(697)) / 2, 2))
print("L2 cx:", round((to_slide(318) + to_slide(631)) / 2, 2))
# gap checks (ink-to-ink)
print("L1 space ink gap slide:", round((513 - 497) / SX, 2))
print("L2 gaps:", round((384 - 367) / SX, 2), round((423 - 409) / SX, 2))
# predicted ink-to-ink gaps at em=49: space advance .278em minus r-right-bearing minus E-left-bearing etc
bb1 = draw.textbbox((0, 0), "Transformer", font=font100)
adv_T = draw.textlength("Transformer", font=font100)
bbE = draw.textbbox((adv_T, 0), "Encoder", font=font100)
gap100 = bbE[0] - bb1[2]
print("predicted L1 word gap at em:", round(gap100 / 100 * (sum(ems) / len(ems)), 2))
