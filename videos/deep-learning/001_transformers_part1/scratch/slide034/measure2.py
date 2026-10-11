from PIL import Image
import numpy as np
img = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_034.jpg').convert('RGB')
a = np.asarray(img).astype(int)
H,W = a.shape[:2]

# vertical scan at x=460 (through peach panel) for fill transitions
print("col x=460 runs:")
prev=None; start=0
for y in range(40,540):
    c = tuple(a[y,460]//24)
    if c!=prev:
        if prev is not None and y-start>3: print(f"  y {start}..{y-1}: ~{tuple(a[(start+y)//2,460])}")
        prev=c; start=y
print("  y",start,"..539: ~",tuple(a[520,460]))

# horizontal scan at y=300 (peach panel body left..right)
print("row y=300 runs (color transitions):")
prev=None; start=0
for x in range(0,960):
    c = tuple(a[300,x]//30)
    if c!=prev:
        if prev is not None and x-start>2: print(f"  x {start}..{x-1}: ~{tuple(a[300,(start+x)//2])}")
        prev=c; start=x
print("  x",start,"..959: ~",tuple(a[300,955]))
