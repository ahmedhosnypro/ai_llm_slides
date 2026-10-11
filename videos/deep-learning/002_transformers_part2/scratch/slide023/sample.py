from PIL import Image
import numpy as np
im = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_023.jpg').convert('RGB')).astype(int)

def avg(y0,y1,x0,x1,label):
    px = im[y0:y1+1, x0:x1+1].reshape(-1,3).mean(axis=0)
    print(f"{label}: avg ({px[0]:.0f},{px[1]:.0f},{px[2]:.0f}) over y{y0}..{y1} x{x0}..{x1}")

# ROW1
avg(128,146,185,225,"R1 box1 interior")
avg(126,128,180,228,"R1 box1 top border")
avg(148,150,180,228,"R1 box1 bottom border")
avg(120,150,176,178,"R1 box1 left border")
avg(120,150,226,230,"R1 box1 right border")
avg(130,145,234,242,"R1 between boxes")
avg(120,150,160,172,"R1 container left edge zone")
avg(120,150,870,880,"R1 container right edge zone")
avg(132,141,185,225,"R1 box1 text zone")
# ROW2
avg(190,222,180,225,"R2 box1 interior")
avg(186,190,200,240,"R2 container top border zone")
avg(196,216,205,208,"R2 box1 left border")
avg(196,216,240,243,"R2 box1 right border")
avg(196,216,250,258,"R2 lavender between boxes")
# ROW3
avg(266,298,180,225,"R3 box1 interior")
avg(260,264,200,240,"R3 container top border zone")
avg(266,298,240,262,"R3 between boxes")
avg(270,292,197,204,"R3 box1 left border zone")
