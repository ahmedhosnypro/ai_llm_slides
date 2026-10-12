# m12 (slide005): decoder-stack + PE-box zone maps — render vs frame (frame space).
# Classify: O=outlined-box border (dark stroke), T=text ink, otherwise dominant fill.
from PIL import Image
import numpy as np

my = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_005.jpg').convert('RGB')).astype(int)
rw = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide005/warped_render3.png').convert('RGB')).astype(int)

def zone(name, bx0, bx1, by0, by1, step=2):
    print(f'== {name} (build x{bx0}..{bx1} y{by0}..{by1}, {step}pt cells) ==')
    for tag, img in (('RENDER', rw), ('FRAME ', my)):
        print(f'  {tag}:')
        for by in range(by0, by1, step):
            row = []
            for bx in range(bx0, bx1, step):
                fx, fy = int(18.0787 + 0.961084 * bx), int(0.4700 + 0.957187 * by)
                r, g, b = img[fy, fx]
                lum = (int(r) + int(g) + int(b)) / 3
                if lum < 90: c = '#'          # dark ink/border
                elif lum < 150: c = '+'       # mid
                elif r > 200 and g > 200 and b < 160: c = 'Y'
                elif r > 180 and g < 140 and b < 110: c = 'O'  # orange/salmon
                elif b > r + 30 and b > 140: c = 'P'           # purple/blue
                elif g > r + 20 and g > 150: c = 'G'           # green
                else: c = '.'
                row.append(c)
            print(f'    {by:3d} ' + ''.join(row))

# decoder stack: Add&Norm/FF/Add&Norm inside the olive block (build x744..842 y198..280)
zone('DECODER STACK', 744, 842, 198, 280)
# PE box + purple block bottom (build x740..840 y395..460)
zone('DEC PE BOX', 740, 840, 395, 460)
