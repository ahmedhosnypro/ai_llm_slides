from PIL import Image
import numpy as np
from collections import Counter
im = np.asarray(Image.open('unique_slides/slide_022.jpg').convert('RGB')).astype(int)
r, g, b = im[:,:,0], im[:,:,1], im[:,:,2]

def modal(x0,y0,x1,y1,label,q=4):
    reg = im[y0:y1, x0:x1].reshape(-1,3)
    rq = (reg // q * q)
    c = Counter(map(tuple, rq))
    top = c.most_common(4)
    s = ' | '.join('%02X%02X%02X x%d' % (t[0][0],t[0][1],t[0][2],t[1]) for t in top)
    print(f'{label} [{x0},{y0},{x1},{y1}]: {s}')

# interior modal fills (safe empty spots)
modal(180,110,220,130, 'aug box fill TL corner area')
modal(380,210,410,235, 'aug box fill BR area')
modal(560,110,600,130, 'weights box fill')
modal(100,265,140,285, 'decision box fill left')
modal(700,320,750,335, 'decision box fill right')
modal(250,360,290,380, 'diagram box fill top')
modal(560,470,600,500, 'diagram box fill bottom-right')
modal(640,400,670,415, 'callout fill')
# panel bg
modal(70,270,110,300, 'panel bg left of decision box')
modal(830,100,880,140, 'panel bg right of weights box')
# canvas
modal(5,270,35,300, 'canvas outside panel')

# borders: scan for red pixels near comp bbox edges
def edge_scan(label, xs, ys):
    best = []
    for y in ys:
        for x in xs:
            v = im[y,x]
            if v[0]>120 and v[1]<100 and v[2]<100:
                best.append((x,y,tuple(v)))
    print(label, best[:8], '...' if len(best)>8 else '', f'n={len(best)}')

# aug box: white comp x84..417 y90..244 -> border just outside/inside
edge_scan('aug top edge y87-91 x200-300:', range(200,300), range(87,92))
edge_scan('aug left edge x82-88 y150-200:', range(82,89), range(150,200))
edge_scan('aug bottom edge y243-248 x200-300:', range(200,300), range(243,249))
edge_scan('aug right edge x415-421 y150-200:', range(415,422), range(150,200))
# weights box x530..791 y90..244
edge_scan('weights left edge x527-533 y150-200:', range(527,534), range(150,200))
# decision box x83..765 y257..340
edge_scan('decision top edge y254-259 x300-400:', range(300,400), range(254,260))
edge_scan('decision bottom edge y338-344 x300-400:', range(300,400), range(338,345))
# diagram box x230..611 y352..506
edge_scan('diagram left edge x227-233 y420-470:', range(227,234), range(420,470))
edge_scan('diagram top edge y349-355 x300-400:', range(300,400), range(349,356))
edge_scan('diagram bottom edge y504-510 x300-400:', range(300,400), range(504,511))
