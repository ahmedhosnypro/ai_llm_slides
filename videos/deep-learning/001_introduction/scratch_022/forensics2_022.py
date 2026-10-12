from PIL import Image
import numpy as np
im = np.asarray(Image.open('unique_slides/slide_022.jpg').convert('RGB')).astype(int)
def px(x,y,label):
    reg = im[y-1:y+2, x-1:x+2].reshape(-1,3).mean(axis=0)
    print(f'({x},{y}) {label}: rgb=({reg[0]:.0f},{reg[1]:.0f},{reg[2]:.0f}) #%02X%02X%02X' % tuple(reg.astype(int)))
px(20,270,'canvas left of panel')
px(500,60,'above panel / title zone bg')
px(500,270,'panel mid bg (between boxes?)')
px(60,60,'panel top-left inside')
px(250,150,'aug vector box fill')
px(650,150,'weights box fill')
px(300,300,'decision box fill')
px(400,430,'diagram box fill')
px(700,425,'tan callout fill')
px(500,535,'bottom bar')
px(500,528,'bottom bar upper')
px(42,270,'panel left border?')
px(918,270,'panel right border?')
px(500,45,'panel top border?')
# scan for the red borders around aug box (row 90ish)
row = im[92, 80:430]
redish = [(80+i, tuple(v)) for i,v in enumerate(row) if v[0]>140 and v[1]<90]
print('aug box top border red cols at y92:', redish[:6], '...', redish[-3:] if redish else '')
col = im[90:250, 85]
redishc = [(90+i, tuple(v)) for i,v in enumerate(col) if v[0]>140 and v[1]<90]
print('aug box left border red rows at x85:', redishc[:4], redishc[-3:] if redishc else '')
# decision box borders: row through y=298
row2 = im[298, 80:780]
rd2 = [(80+i, tuple(v)) for i,v in enumerate(row2) if v[0]>140 and v[1]<90]
print('decision box red cols at y298 (first/last):', rd2[:3], rd2[-3:] if rd2 else '')
# diagram box borders
row3 = im[430, 220:620]
rd3 = [(220+i, tuple(v)) for i,v in enumerate(row3) if v[0]>140 and v[1]<90]
print('diagram box red cols at y430:', rd3[:3], rd3[-3:] if rd3 else '')
# tan callout borders
row4 = im[425, 620:830]
rd4 = [(620+i, tuple(v)) for i,v in enumerate(row4) if v[0]>140 and v[1]<90]
print('callout red cols at y425:', rd4[:3], rd4[-3:] if rd4 else '')
col4 = im[380:470, 700]
rd4c = [(380+i, tuple(v)) for i,v in enumerate(col4) if v[0]>140 and v[1]<90]
print('callout red rows at x700:', rd4c[:3], rd4c[-3:] if rd4c else '')
