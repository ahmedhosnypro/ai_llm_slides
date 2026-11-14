from PIL import Image
import numpy as np
NS = '/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure'
a = np.asarray(Image.open(NS + '/unique_slides/slide_010.jpg').convert('RGB')).astype(int)

def cls(px):
    r, g, b = px
    if r + g + b < 300: return '#'          # black
    if r > 150 and r - g > 70 and r - b > 70: return 'R'  # red
    if b > 120 and b - r > 50: return 'B'   # blue
    if g > 100 and g - r > 40 and g - b > 40: return 'G'  # green
    if r > 80 and r < 170 and b > 120 and b - g > 40: return 'P'  # purple
    if r > 200 and g > 180 and b < 120 and r - b > 100: return 'Y'  # yellow
    if r > 230 and g > 200 and 190 < b < 235: return 'p'  # peach
    if r > 230 and 150 < g < 200 and b < 160: return 'o'  # orange
    if 100 < r < 200 and g > 200 and b < 100: return 'l'  # lime
    if abs(r - 217) < 15 and abs(g - 217) < 15 and abs(b - 217) < 15: return '.'  # gray fill
    if r > 235 and g > 235 and b > 235: return ' '
    return '?'

def dump(x0, y0, x1, y1, step=2, label=''):
    print(f'--- {label} x{x0}-{x1} y{y0}-{y1} step{step} ---')
    hdr = '     ' + ''.join(str((x // 10) % 10) for x in range(x0, x1, step))
    print(hdr)
    for y in range(y0, y1, step):
        row = ''.join(cls(a[y, x]) for x in range(x0, x1, step))
        print(f'{y:4d} {row}')

dump(660, 45, 885, 165, 2, 'M1 PANEL')
dump(660, 160, 885, 295, 2, 'M2 PANEL')
