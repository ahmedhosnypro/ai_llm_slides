from PIL import Image
import numpy as np

F = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_017.jpg").convert("RGB")
a = np.asarray(F).astype(int)
H, W = a.shape[:2]
r, g, b = a[:,:,0], a[:,:,1], a[:,:,2]

def bbox(mask, name):
    ys, xs = np.where(mask)
    if len(xs) == 0:
        print(name, ": none"); return None
    print("%-14s n=%6d  x %3d..%3d  y %3d..%3d" % (name, len(xs), xs.min(), xs.max(), ys.min(), ys.max()))
    return (xs.min(), xs.max(), ys.min(), ys.max())

def near(c, tol=22):
    return (np.abs(r-c[0])<tol)&(np.abs(g-c[1])<tol)&(np.abs(b-c[2])<tol)

# parent card fills (001 measured): h1 EF8C96, h2 C5C1F4, h3 F8FF9A, h4 D4FFE5, h5 F7E2CD
for name, c in [("card_h1", (0xEF,0x8C,0x96)), ("card_h2", (0xC5,0xC1,0xF4)), ("card_h3", (0xF8,0xFF,0x9A)),
                ("card_h4", (0xD4,0xFF,0xE5)), ("card_h5", (0xF7,0xE2,0xCD))]:
    bbox(near(c, 18), name)

# spec card fills for MY frame: h1 F08A8A, h2 C9B8E8, h3 F6E96B, h4 A8E4A0, h5 F8D0A0
for name, c in [("spec_h1", (0xF0,0x8A,0x8A)), ("spec_h2", (0xC9,0xB8,0xE8)), ("spec_h3", (0xF6,0xE9,0x6B)),
                ("spec_h4", (0xA8,0xE4,0xA0)), ("spec_h5", (0xF8,0xD0,0xA0))]:
    bbox(near(c, 18), name)

# tan dot product box: parent D8C0A8 / spec D2B48C
bbox(near((0xD8,0xC0,0xA8), 16), "tan_parent")
bbox(near((0xD2,0xB4,0x8C), 16), "tan_spec")

# gold W boxes F5C242
bbox(near((0xF5,0xC2,0x42), 20), "gold_F5C242")

# magenta FF69B4 (X2 highlight)
bbox(near((0xFF,0x69,0xB4), 25), "magenta")

# pill fills: scaling FBD8E8 / pillSoftmax E4D8F4 (parent) ; spec F2B8C6 / C9A0DC
bbox(near((0xFB,0xD8,0xE8), 14), "pillScaling_p")
bbox(near((0xF2,0xB8,0xC6), 14), "pillScaling_s")
bbox(near((0xE4,0xD8,0xF4), 12), "pillSoftmax_p")
bbox(near((0xC9,0xA0,0xDC), 16), "pillSoftmax_s")
