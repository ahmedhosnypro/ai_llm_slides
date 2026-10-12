#!/usr/bin/env python3
"""Pass 5: C3/C4 true extents, citation font discrimination (Arial vs Times via cap+width),
cursor blob isolation, clean-fill census, E-line left inks, underline widths."""
from PIL import Image, ImageFont
import glob

S060 = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_060.jpg"
img = Image.open(S060).convert("RGB")
px = img.load()
FX0, SX, SY = 18.63, 0.96123, 0.95556
def TX(fx): return (fx - FX0) / SX
def TY(fy): return fy / SY

def blueish(p):
    r, g, b = p
    return b > 100 and (b - r) > 35 and (b - g) > 25

def reddish(p):
    r, g, b = p
    return r > 110 and (r - g) > 45 and (r - b) > 35

fonts = {}
for pat, key in (("**/Arialbd.TTF", "b"), ("**/Arial.TTF", "r"), ("**/Ariali.TTF", "i"),
                 ("**/Arialbi.TTF", "bi"), ("**/LiberationSerif-Italic.ttf", "ti"),
                 ("**/LiberationSerif-BoldItalic.ttf", "tbi")):
    c = glob.glob("/usr/share/fonts/" + pat, recursive=True) or glob.glob("/usr/share/fonts/" + pat.replace("**/", "**/"), recursive=True)
    if not c:
        c = glob.glob('/usr/share/fonts/**/' + pat.split('/')[-1], recursive=True)
    if c:
        fonts[key] = c[0]
print("fonts:", {k: v for k, v in fonts.items() if 'Serif' in v or 'Arial' in v})

def em_for(text, target_pt, key, size=300):
    f = ImageFont.truetype(fonts[key], size)
    return target_pt / (f.getlength(text) / size)

# ---- C3 rows 292..322 and C4 rows 350..376: blue counts + extents (x 84..872, exclude border halo)
for name, y0, y1 in (("C3", 292, 322), ("C4", 350, 376)):
    print(f"== {name}")
    for y in range(y0, y1 + 1):
        xs = [x for x in range(84, 872) if blueish(px[x, y])]
        print(y, len(xs), (min(xs), max(xs)) if xs else None)

# citation text-row extents (exclude underline rows)
cits = {
    "C1": (169, 181, "Radford et al., OpenAI. June 2018 and February 2019."),
    "C2": (233, 245, "Devlin et al., Google AI Language. May 2019."),
    "C3": (296, 308, "Liu et al., Facebook AI. June 2019."),
    "C4": (355, 367, "Zhang Dai et al. Carnegie Mellon University and Google Brain"),
}
print("== citation fits: ink width / em(Arial italic) / em(Times italic) / cap-derived ==")
for name, (y0, y1, text) in cits.items():
    xs = [x for y in range(y0, y1 + 1) for x in range(84, 872) if blueish(px[x, y])]
    x0, x1 = min(xs), max(xs)
    w = TX(x1 + 1) - TX(x0)
    ea = em_for(text, w, "i")
    et = em_for(text, w, "ti")
    print(f"{name}: fx {x0}..{x1} slide x {TX(x0):.1f}..{TX(x1+1):.1f} w {w:.1f}  emA {ea:.2f} emT {et:.2f}")

# cap heights measured: C1 top 168.5 baseline 181.5 -> 13.0 ; C2 232.5..245.5 -> 13.0
# Arial cap 0.716em, Times cap 0.662em
for cap, nm in ((13.0, "C1/C2 cap 13.0"), (13.6, "C4 cap 13.6")):
    print(f"{nm}: Arial em {cap/0.716:.2f}  Times em {cap/0.662:.2f}")

# ---- cursor: dark px x 620..877, y 370..480
dk = [(x, y) for y in range(370, 480) for x in range(620, 877) if sum(px[x, y]) < 300]
print("== cursor-ish dark px x>620,y>370:", len(dk))
if dk:
    print("bbox:", min(p[0] for p in dk), min(p[1] for p in dk), max(p[0] for p in dk), max(p[1] for p in dk))
    print("sample:", dk[:10])

# ---- clean fill census (x 600..820, y 458..476 — below E6, above box bottom, right of text)
from collections import Counter
c = Counter()
for y in range(458, 477):
    for x in range(600, 821):
        c[px[x, y]] += 1
tot = sum(c.values())
print("fill census top:", c.most_common(4), "mean:", tuple(round(sum(k[i] * v for k, v in c.items()) / tot) for i in range(3)))

# ---- entry left/right ink (blue-only cols left of red start) + red extents -> slide
ents = {
    "E1": (146, 159, 89, 593, "GPT-1 and GPT-2 (Generative Pre-trained Transformers)", "GPT-1 and GPT-2 ", "(Generative Pre-trained Transformers)"),
    "E2": (210, 223, 90, 686, "BERT (Bidirectional Encoder Representations from Transformers)", "BERT ", "(Bidirectional Encoder Representations from Transformers)"),
    "E3": (275, 288, 89, 524, "RoBERTa (Robustly Optimized BERT Approach)", "RoBERTa ", "(Robustly Optimized BERT Approach)"),
    "E4": (334, 347, 92, 781, "Transformer-XL: Attentive Language ModelsBeyond a Fixed-Length Context", "Transformer-XL: ", "Attentive Language ModelsBeyond a Fixed-Length Context"),
    "E5": (396, 409, 89, 432, "T5 (Text-to-Text Transfer Transformer)", "T5 ", "(Text-to-Text Transfer Transformer)"),
    "E6": (439, 452, 89, 592, "GPT-3  (175 Billion Parameter, Beta Release June 2020)", "GPT-3  ", "(175 Billion Parameter, Beta Release June 2020)"),
}
print("== entries: full-line em(ArialB/bi), run boundary check ==")
for name, (y0, y1, fx0, fx1, full, blue, red) in ents.items():
    key = "bi" if name == "E4" else "b"
    w = TX(fx1 + 1) - TX(fx0)
    em = em_for(full, w, key)
    # predicted red-start offset from left ink: advance(blue)/em*em = advance(blue)*em/300*...
    f = ImageFont.truetype(fonts[key], 300)
    adv_blue = f.getlength(blue) / 300 * em
    # measured red start:
    rxs = [x for y in range(y0, y1 + 1) for x in range(fx0, fx1 + 1) if reddish(px[x, y])]
    red_start = min(rxs) if rxs else None
    print(f"{name}: ink {fx0}..{fx1} w {w:.1f} em {em:.2f} | blue adv->red start {TX(fx0)+adv_blue:.1f} vs measured {TX(red_start):.1f} "
          f"(blue ink ends {TX(max(x for y in range(y0,y1+1) for x in range(fx0,min(rxs)-1 if rxs else fx1) if blueish(px[x,y]))):.1f})")

# ---- title left/right precise + em with double space vs single space discrimination
xs = [x for y in range(60, 95) for x in range(60, 900) if reddish(px[x, y])]
print(f"TITLE ink fx {min(xs)}..{max(xs)} slide {TX(min(xs)):.1f}..{TX(max(xs)+1):.1f} w {TX(max(xs)+1)-TX(min(xs)):.1f}")
for txt in ("What is Next  (as of 2020)", "What is Next (as of 2020)"):
    print(f"  '{txt}' emB {em_for(txt, TX(max(xs)+1)-TX(min(xs)), 'b'):.2f}")
