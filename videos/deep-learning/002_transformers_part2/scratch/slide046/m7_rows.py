from PIL import Image
import numpy as np
im = Image.open('videos/deep-learning/002_transformers_part2/unique_slides/slide_046.jpg').convert('RGB')
a = np.asarray(im).astype(int)
def sx(fx): return (fx - 17.582) / 0.962329
def sy(fy): return fy / 0.955556
# column1 bar spans frame x 205.1+-24 -> 181..229. print color runs
for name, ymid in [('final',73),('postFFN',178),('postLN',286),('outatt',390),('X',496)]:
    print(f'--- {name} row, y={ymid} ---')
    for x in range(178, 232, 2):
        print(f'  x={x} slide={sx(x):.1f}: {tuple(a[ymid,x])}')
