# m2_sample.py — direct pixel color sampling of slide_032.jpg
import numpy as np
from PIL import Image
F = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_032.jpg"
a = np.asarray(Image.open(F).convert("RGB")).astype(int)
def patch(x, y, r=3):
    p = a[max(0,y-r):y+r+1, max(0,x-r):x+r+1].reshape(-1,3)
    med = np.median(p, axis=0).astype(int)
    return tuple(med)
pts = {
 "chrome_panel(100,300)": (100,300),
 "chrome_panel(700,120)": (700,120),
 "slide_margin(20,270)": (20,270),
 "eqpanel_inside(150,100)": (150,100),
 "eqpanel_inside(430,240)": (430,240),
 "eqpanel_border_top(262,74?)": (262,74),
 "pill(140,126)": (140,126),
 "pill_circle_inside(105,126)": (105,126),
 "matrix_cell_r1c1(240,107)": (240,107),
 "matrix_cell_r2c2(278,150)": (278,150),
 "matrix_cell_r3c3(317,191)": (317,191),
 "matrix_cell_r4c4(352,234)": (352,234),
 "matrix_border(240,130)": (240,130),
 "outcell_1(430,97)": (430,97),
 "outcell_2(430,140)": (430,140),
 "outcell_3(430,182)": (430,182),
 "outcell_4(430,224)": (430,224),
 "netpanel_inside(700,470)": (700,470),
 "netpanel_inside(550,300)": (550,300),
 "band(700,390)": (700,390),
 "band(600,340)": (600,340),
 "input_circle(540,447)": (540,447),
 "output_circle(540,292)": (540,292),
 "title_ink(650,140)": (650,140),
 "arrow_inside(515,330)": (515,330),
 "arrow_inside(500,390)": (500,390),
 "badge(893,71)": (893,71),
}
for k,(x,y) in pts.items():
    c = patch(x,y)
    print(f"{k:38s} ({x:3d},{y:3d}) rgb={c} hex=#{c[0]:02X}{c[1]:02X}{c[2]:02X}")
