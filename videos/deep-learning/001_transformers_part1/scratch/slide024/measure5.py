# Pass 5: topology maps + targeted color samples.
from PIL import Image
import numpy as np

im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_024.jpg').convert('RGB')
a = np.asarray(im).astype(int)
r, g, b = a[..., 0], a[..., 1], a[..., 2]

# RED map 96x54 (cell 10px), excluding outer frame border band
red = (r > 140) & (g < 120) & (b < 120)
red[:50, :] = False; red[532:, :] = False; red[:, :46] = False; red[:, 914:] = False
print("RED map (cell=10px, x: 0-96 -> *10, y: 5-53 -> *10):")
print("    " + ''.join(str((i // 10) % 10) for i in range(96)))
for cy in range(5, 54):
    row = ''.join('#' if red[cy*10:(cy+1)*10, cx*10:(cx+1)*10].sum() >= 6
                  else ('+' if red[cy*10:(cy+1)*10, cx*10:(cx+1)*10].any() else '.')
                  for cx in range(96))
    print(f"y{cy*10:3d} {row}")

# targeted samples
def s(x, y, label):
    p = a[y, x]
    print(f"s ({x:3d},{y:3d}) {label:34s} rgb=({p[0]:3d},{p[1]:3d},{p[2]:3d}) #{p[0]:02X}{p[1]:02X}{p[2]:02X}")

print("\n-- circle border scan y=291, x 38..52 --")
for x in range(38, 53): s(x, 291, 'circle left edge')
print("-- circle border scan x=278, y 52..66 --")
for y in range(52, 67): s(278, y, 'circle top edge')
print("-- sentence box: top border scan x=700, y 100..114 --")
for y in range(100, 115): s(700, y, 'sentbox top')
print("-- sentence box fill --")
for x, y in [(500, 112), (700, 113), (860, 128), (492, 127), (895, 127), (700, 143)]:
    s(x, y, 'sentbox fill/edge')
print("-- node borders --")
s(202, 100, "'in' top border"); s(202, 188, "'in' bottom border")
s(360, 120, "garden top border"); s(119, 250, "'the' top border")
s(268, 244, "Boy(in) top border"); s(268, 332, "Boy(in) bottom border")
s(268, 262, "Boy(in) fill"); s(743, 264, "Boy(out) fill")
s(608, 419, "Boy(in-put) fill"); s(432, 324, "tree top border")
print("-- block arrow interior --")
for x, y in [(560, 295), (600, 290), (560, 305), (620, 300), (530, 298), (655, 298)]:
    s(x, y, 'blockarrow')
print("-- gray bg / white margin --")
s(950, 270, "outer margin"); s(300, 30, "top margin"); s(470, 270, "panel gray")
