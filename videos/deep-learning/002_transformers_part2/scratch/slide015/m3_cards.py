from PIL import Image
import numpy as np
from scipy import ndimage

im = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_015.jpg').convert('RGB')).astype(int)

# sample colors along expected card positions to learn the child's actual card fills
# parent h1 card x56..604 y274..526; child expected x~98..646 y~176..428
for (name, x, y) in [
    ('h1 card mid', 350, 400), ('h1 card mid2', 250, 300),
    ('h2 card sliver left', 130, 240), ('h3 sliver', 170, 200), ('h4 sliver', 220, 160), ('h5 sliver', 260, 130),
    ('plane area', 200, 120), ('plane area2', 300, 100),
    ('query container', 300, 405), ('token strip2 (hot)', 275, 405),
    ('bottom title zone', 480, 470), ('W boxes zone', 620, 370),
    ('sigma box', 460, 250), ('input ellipse', 130, 320), ('key ellipse', 185, 320),
    ('top peek zone', 570, 60), ('h5 tag zone', 787, 100),
]:
    if 0 <= x < 960 and 0 <= y < 540:
        print(f'{name:22s} ({x:3d},{y:3d}) rgb={tuple(im[y, x])}')
