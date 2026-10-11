from PIL import Image
import numpy as np
im = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_023.jpg').convert('RGB')).astype(int)
r, g, b = im[:,:,0], im[:,:,1], im[:,:,2]
luma = (0.299*r + 0.587*g + 0.114*b)
print("ROW3 box1 (x168..230): per-row count luma<215 and min:")
for y in range(266, 303):
    seg = luma[y,168:231]
    c = (seg<215).sum()
    print(f"  y{y}: dark {c:3d}  min {seg.min():.0f}  mean {seg.mean():.0f}")
print()
print("ROW2 box1 (x163..225): per-row count luma<200 (on lavender 224):")
for y in range(186, 228):
    seg = luma[y,163:226]
    c = (seg<200).sum()
    print(f"  y{y}: dark {c:3d}  min {seg.min():.0f}  mean {seg.mean():.0f}")
