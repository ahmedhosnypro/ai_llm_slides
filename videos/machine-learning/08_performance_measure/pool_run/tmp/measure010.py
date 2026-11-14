from PIL import Image
import numpy as np
im = Image.open('/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure/unique_slides/slide_010.jpg').convert('RGB')
a = np.asarray(im).astype(int)
dark = (a.sum(axis=2) < 300)

def ink_bbox(x0, y0, x1, y1, label):
    sub = dark[y0:y1, x0:x1]
    ys, xs = np.where(sub)
    if len(xs) == 0:
        print(label, 'none')
        return
    print(f'{label}: x {x0+xs.min()}-{x0+xs.max()} y {y0+ys.min()}-{y0+ys.max()}')

ink_bbox(60, 255, 540, 330, 'formula-region ink')
ink_bbox(60, 255, 320, 330, 'recall-box ink')
ink_bbox(320, 255, 540, 330, 'fraction ink')
ink_bbox(330, 285, 540, 345, 'precision ink')
ink_bbox(80, 320, 340, 385, 'callout ink')
ink_bbox(80, 400, 540, 440, 'caption ink')
ink_bbox(70, 199, 617, 258, 'meaning ink')
ink_bbox(70, 111, 617, 176, 'band ink')
ink_bbox(300, 40, 660, 120, 'title ink')
ink_bbox(76, 462, 498, 511, 'bottombox ink')
ink_bbox(674, 51, 867, 160, 'matrix1 ink')
ink_bbox(674, 169, 867, 287, 'matrix2 ink')
ink_bbox(537, 290, 882, 320, 'tree headers ink')
ink_bbox(560, 310, 880, 380, 'planes ink')
ink_bbox(537, 340, 882, 395, 'nodes row1')
ink_bbox(537, 410, 882, 465, 'nodes row2')
ink_bbox(537, 455, 882, 485, 'leaf labels')
