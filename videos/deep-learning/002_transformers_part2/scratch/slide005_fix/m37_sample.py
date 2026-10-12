# m37_sample.py — RGB samples at the ambiguous verticals/regions, orig vs render_4
from PIL import Image

VID = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2"
FR = Image.open(VID + "/unique_slides/slide_005.jpg").convert("RGB")
RD = Image.open(VID + "/recreated_pptx/qa/slide005/render_4.png").convert("RGB")
SX, SY = 2.16770, 2.17684
po, pr = FR.load(), RD.load()

def s(label, fx, fy):
    r, g, b = po[fx, fy]
    rx, ry = round((fx - 18.0787) * SX), round((fy - 0.4700) * SY)
    r2, g2, b2 = pr[rx, ry]
    print(f"{label:34s} frame({fx},{fy}) ORIG rgb({r},{g},{b})   REND4 rgb({r2},{g2},{b2})")

print("--- the constant verticals in the d1end window ---")
for x in (610, 620, 624, 627, 630, 636, 640, 643, 646, 652, 658, 664):
    s(f"col x{x}", x, 360)
print("--- rows through the box region ---")
for y in (342, 345, 350, 356, 362, 368, 371, 376, 380):
    s(f"row y{y} @x655", 655, y)
    s(f"row y{y} @x627", 627, y)
print("--- d1 dash corridor above the box ---")
for y in (330, 334, 338, 341):
    s(f"dash @y{y} expected x", round(506.5 + (y - 243.5) / 0.828), y)
print("--- h assembly: hook + rect border + gray verticals ---")
for (x, y) in ((470, 360), (474, 360), (477, 345), (477, 355), (483, 345), (484, 355),
               (476, 365), (474, 370), (483, 330), (470, 343), (493, 362), (493, 347)):
    s(f"asm ({x},{y})", x, y)
print("--- ghost ring / circle edges ---")
for (x, y) in ((483, 352), (486, 384), (505, 362), (493, 374), (493, 351)):
    s(f"circle ({x},{y})", x, y)
