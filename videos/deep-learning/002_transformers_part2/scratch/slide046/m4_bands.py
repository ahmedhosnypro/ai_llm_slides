from PIL import Image
import numpy as np
im = Image.open('videos/deep-learning/002_transformers_part2/unique_slides/slide_046.jpg').convert('RGB')
a = np.asarray(im).astype(int)
H, W = a.shape[:2]
def near(c, tol):
    return (np.abs(a - np.array(c)).max(axis=2) <= tol)
COLORS = {
 'pastel_pink FFB6C1': ((0xFF,0xB6,0xC1), 40),
 'pastel_yel FFFF99': ((0xFF,0xFF,0x99), 35),
 'pastel_grn C1E1C1': ((0xC1,0xE1,0xC1), 30),
 'pastel_lav D8BFD8': ((0xD8,0xBF,0xD8), 30),
 'navy 00008B': ((0x00,0x00,0x8B), 55),
 'ffnbox DDEBF7': ((0xDD,0xEB,0xF7), 12),
 'tile FFE699': ((0xFF,0xE6,0x99), 18),
 'graybar D9D9D9': ((0xD9,0xD9,0xD9), 14),
 'cont E2EFDA': ((0xE2,0xEF,0xDA), 12),
 'callout FFCCCC': ((0xFF,0xCC,0xCC), 22),
 'cap_hl FFFF00': ((0xFF,0xFF,0x00), 60),
 'green 00B050': ((0x00,0xB0,0x50), 50),
 'orange E8A020': ((0xE8,0xA0,0x20), 55),
 'dred 990000': ((0x99,0x00,0x00), 45),
 'blue 0000CC': ((0x00,0x00,0xCC), 55),
 'yellow FFFF00 cell': ((0xFF,0xFF,0x00), 25),
}
for name,(c,tol) in COLORS.items():
    m = near(c, tol)
    rows = m.sum(axis=1)
    bands = []
    inb = False
    for y in range(H):
        if rows[y] > 25 and not inb: inb=True; y0=y
        elif rows[y] <= 25 and inb: inb=False; bands.append((y0,y-1,int(rows[y0:y].max())))
    if inb: bands.append((y0,H-1,int(rows[y0:].max())))
    print(f"{name}: bands(y0,y1,maxcount) = {bands}")
