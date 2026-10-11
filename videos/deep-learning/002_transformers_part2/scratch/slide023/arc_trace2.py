from PIL import Image
import numpy as np
im = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_023.jpg').convert('RGB')).astype(int)
r, g, b = im[:,:,0], im[:,:,1], im[:,:,2]
# orange-ish: strong R-B gap, moderate R
orange = (r-b>55)&(r-g>30)&(r>150)
print("orange mask map, y292..335, x150..880 (1 char per 4px):")
for y in range(292, 336):
    line=""
    for x in range(150, 881, 4):
        seg = orange[y, x:x+4]
        line += "#" if seg.any() else "."
    print(f"{y:3d} {line}")
ys, xs = np.where(orange[292:336, 150:881])
print("orange bbox y", 292+ys.min(), "..", 292+ys.max(), " x", 150+xs.min(), "..", 150+xs.max(), " count", len(ys))
