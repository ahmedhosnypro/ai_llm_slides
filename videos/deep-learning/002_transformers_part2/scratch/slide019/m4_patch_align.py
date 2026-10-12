# m4: patch-based local shift search between MY frame and warped-001 frame.
# For each patch, find (dx,dy) in [-8..8] minimizing SSD -> displacement field.
from PIL import Image
import numpy as np

my = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_019.jpg').convert('RGB')).astype(float)
wa = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide019/warped_001_in_002frame.png').convert('RGB')).astype(float)

patches = {
  'title_left':   (230, 40, 330, 80),
  'title_right':  (620, 40, 720, 80),
  'badge':        (858, 55, 894, 88),
  'legend1':      (330, 105, 500, 135),
  'left_panel_top':(120, 290, 220, 330),
  'left_panel_bot':(120, 420, 220, 470),
  'mid_header':   (300, 45, 380, 75),
  'mid_box':      (330, 250, 430, 290),
  'right_top':    (640, 90, 740, 130),
  'right_mid':    (660, 230, 760, 270),
  'right_low':    (640, 420, 740, 470),
  'nx_circle':    (790, 270, 830, 300),
}
for name, (x0, y0, x1, y1) in patches.items():
    p0 = my[y0:y1, x0:x1]
    best = None
    for dy in range(-8, 9):
        for dx in range(-8, 9):
            q = wa[y0+dy:y1+dy, x0+dx:x1+dx]
            if q.shape != p0.shape: continue
            s = np.abs(p0 - q).mean()
            if best is None or s < best[0]:
                best = (s, dx, dy)
    s0 = np.abs(p0 - wa[y0:y1, x0:x1]).mean()
    print(f'{name:16s} shift dx={best[1]:+d} dy={best[2]:+d}  ssd {s0:7.2f} -> {best[0]:7.2f}')
