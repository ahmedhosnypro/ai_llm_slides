from PIL import Image
import numpy as np
im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_036.jpg').convert('RGB')
a = np.asarray(im).astype(int)

def classify(px):
    r,g,b = px
    l = (r+g+b)/3
    if l>225: return '.'
    if b > r+40 and b>90: return 'B'
    if r > g+50 and r>90 and g<160: return 'R'
    if r>200 and 150<g<215 and b<160: return 'T'
    return 'k'

def fmap(x0,x1,y0,y1,step=2,label=''):
    print(f'--- {label} ---')
    for y in range(y0,y1,step):
        row=''
        for x in range(x0,x1,step):
            block = a[y:y+step, x:x+step].reshape(-1,3)
            sat = block.max(axis=1)-block.min(axis=1)
            l = block.mean(axis=1)
            i = int(np.argmax(sat*0.6 + (255-l)))
            c = classify(block[i])
            row += c if c!='.' else ('.' if l.mean()>228 else ':')
        print('%4d %s' % (y,row))

fmap(340,432,415,470,2,'FC1 arrow+label x340-432 y415-470')
fmap(293,340,415,522,2,'FC1 left chips x293-340')
