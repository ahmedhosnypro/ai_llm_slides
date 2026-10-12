# m10: probe key regions in MY frame vs warped-001 (F21 space) with color censuses.
from PIL import Image
import numpy as np
from collections import Counter

A, Bx, C, D = 20.9473, 0.95679, 2.2031, 0.95651
my = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_019.jpg').convert('RGB')).astype(int)
wa = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide019/warped_001_f21.png').convert('RGB')).astype(int)

def census(img, x0, y0, x1, y1, n=6):
    reg = img[y0:y1, x0:x1].reshape(-1, 3)
    q = (reg // 24 * 24)
    c = Counter(map(tuple, q))
    tot = len(reg)
    return ', '.join(f'{r},{g},{b} x{int(100*k/tot)}%' for (r, g, b), k in c.most_common(n))

def probe(name, bx0, by0, bx1, by1):
    # build pt -> my-frame px
    fx0 = int(18.0787 + 0.961084*bx0); fx1 = int(18.0787 + 0.961084*bx1)
    fy0 = int(0.4700 + 0.957187*by0); fy1 = int(0.4700 + 0.957187*by1)
    print(f'--- {name}: build x{bx0}..{bx1} y{by0}..{by1} -> frame x{fx0}..{fx1} y{fy0}..{fy1}')
    print('  MY :', census(my, fx0, fy0, fx1, fy1))
    print('  001:', census(wa, fx0, fy0, fx1, fy1))

probe('legend1 (Normalization Layer)', 141, 100, 344, 132)
probe('legend2 (Feed Forward Layer)', 309, 141, 516, 173)
probe('legend3 (Residual Connections)', 262, 179, 467, 211)
probe('leader1 mid run', 430, 112, 560, 130)
probe('leader4 dive', 560, 180, 620, 300)
probe('pin core', 545, 350, 620, 430)
probe('pin tip zone', 590, 430, 640, 490)
probe('001-pin-location check', 545, 350, 620, 430)
probe('yellow band encoder side', 565, 415, 720, 495)
probe('yellow band decoder side', 760, 415, 905, 495)
probe('enc V circle', 654, 392, 672, 409)
probe('enc K circle', 668, 392, 686, 409)
probe('enc Q circle', 682, 392, 700, 409)
probe('dec chevrons top', 776, 192, 792, 208)
probe('dec chevrons low', 764, 308, 782, 324)
probe('vert line x840', 836, 205, 844, 405)
probe('trunk x834', 830, 205, 838, 405)
probe('leader3 arrowhead', 735, 230, 752, 245)
probe('leader4 arrowhead', 638, 297, 653, 311)
