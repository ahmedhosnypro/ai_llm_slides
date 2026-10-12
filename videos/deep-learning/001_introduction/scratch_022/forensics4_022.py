from PIL import Image
import numpy as np
im = np.asarray(Image.open('unique_slides/slide_022.jpg').convert('RGB')).astype(int)

def runs_row(y, x0, x1, label):
    out=[]
    prev=None
    for x in range(x0,x1):
        v=tuple(im[y,x]); 
        if v!=prev: out.append(f'{x}:{v}'); prev=v
    print(f'row y={y} {label}:', ' '.join(out[:28]))

def runs_col(x, y0, y1, label):
    out=[]; prev=None
    for y in range(y0,y1):
        v=tuple(im[y,x])
        if v!=prev: out.append(f'{y}:{v}'); prev=v
    print(f'col x={x} {label}:', ' '.join(out[:28]))

# aug box edges (white comp x84..417 y90..244)
runs_row(88, 240, 260, 'through top edge')
runs_row(160, 80, 92, 'through left edge')
runs_row(160, 414, 424, 'through right edge')
runs_col(250, 241, 250, 'through bottom edge')
# decision box (x83..765 y257..340)
runs_row(255, 300, 320, 'decision top edge')
runs_col(400, 253, 262, 'decision top edge col')
runs_col(400, 336, 345, 'decision bottom edge col')
# diagram box (x230..611 y352..506)
runs_row(350, 300, 320, 'diagram top edge')
runs_col(400, 502, 512, 'diagram bottom edge col')
runs_col(232, 400, 420, 'diagram left edge col')
# weights box (x530..791 y90..244)
runs_row(88, 640, 660, 'weights top edge')
runs_col(531, 150, 200, 'weights left edge col')
