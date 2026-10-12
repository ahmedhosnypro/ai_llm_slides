from PIL import Image
import numpy as np
r = np.asarray(Image.open('videos/deep-learning/002_transformers_part2/recreated_pptx/qa/slide045/render_1.png').convert('RGB')).astype(int)
print('render size', r.shape)
S = 150/72  # pt -> px
# top row: slide y 175..192.5 -> px 364.6..400.5 ; col1 bar slide x 169.9..219.9 -> px 354..458
def classify(p):
    r_,g,b = p
    mx, mn = max(p), min(p)
    if r_>140 and g<90 and b<90: return 'R'
    if mx>=250 and mx-mn<10: return '.'
    if mx-mn<18: return 'g' if r_<225 else 'G'
    if g>=r_ and g>b: return 'n' if g<200 else 'v'
    if r_>200 and g>200 and b<190: return 'y'
    if r_>200 and b>190 and g<r_-20: return 'm'
    if b>r_ and b>=g: return 'l'
    return '?'
print('render top-row strip, y 366..400 (step 2), x 350..462:')
for y in range(366, 401, 2):
    print(f'{y:4d} ' + ''.join(classify(r[y,x]) for x in range(350, 462, 1)))
