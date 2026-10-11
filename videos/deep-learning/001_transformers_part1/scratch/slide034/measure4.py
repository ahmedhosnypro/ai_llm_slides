from PIL import Image
import numpy as np
img = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_034.jpg').convert('RGB')
a = np.asarray(img).astype(int)

def runs_col(x, y0, y1, label, thresh=24):
    print(f"-- col x={x} ({label})")
    prev=None; start=y0
    for y in range(y0,y1):
        c=tuple(a[y,x]//thresh)
        if c!=prev:
            if prev is not None and y-start>=2:
                mid=tuple(a[(start+y)//2,x])
                if not (mid[0]>228 and mid[1]>228 and mid[2]>225) or True:
                    print(f"   y {start}..{y-1} ~{mid}")
            prev=c; start=y
    mid=tuple(a[y1-1,x]); print(f"   y {start}..{y1-1} ~{mid}")

def runs_row(y, x0, x1, label, thresh=24):
    print(f"-- row y={y} ({label})")
    prev=None; start=x0
    for x in range(x0,x1):
        c=tuple(a[y,x]//thresh)
        if c!=prev:
            if prev is not None and x-start>=2:
                mid=tuple(a[y,(start+x)//2])
                print(f"   x {start}..{x-1} ~{mid}")
            prev=c; start=x
    print(f"   x {start}..{x1-1} ~{tuple(a[y,x1-1])}")

# concept box: find its full outline. Column scan through left border x~64
runs_col(64, 95, 270, "concept left edge")
runs_col(240, 95, 270, "through concept box center")
# concept box bottom border: row scan
runs_row(258, 40, 420, "concept bottom?")
# inside box: sample fills
print("concept box interior samples:", tuple(a[130,110]), tuple(a[130,300]), tuple(a[200,320]), tuple(a[230,100]))
# large equation box in concept top-left: row scan y=130
runs_row(130, 60, 400, "large eq box band")
# small eq box right of arrow: row scan y=190
runs_row(190, 230, 400, "small eq box band")
