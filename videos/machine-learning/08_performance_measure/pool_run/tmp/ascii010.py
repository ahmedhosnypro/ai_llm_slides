from PIL import Image
import numpy as np

NS = '/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure'
im = Image.open(NS + '/unique_slides/slide_010.jpg').convert('RGB')
a = np.asarray(im).astype(int)

red = (a[:, :, 0] > 150) & (a[:, :, 0] - a[:, :, 1] > 70) & (a[:, :, 0] - a[:, :, 2] > 70)
paleblue = (a[:, :, 2] > 235) & (a[:, :, 0] > 220) & (a[:, :, 0] < 245) & (a[:, :, 1] > 230) & (a[:, :, 2] - a[:, :, 0] > 8)
dark = a.sum(axis=2) < 400
blue_txt = (a[:, :, 2] > 150) & (a[:, :, 2] - a[:, :, 0] > 60) & (a[:, :, 1] < 160)
gray = (a.sum(axis=2) > 250) & (a.sum(axis=2) < 620)

def ascii_map(x0, y0, x1, y1, step=4):
    print(f'--- map x{x0}-{x1} y{y0}-{y1} step {step} (R=red B=bluebox #=dark b=bluetext g=gray .=bg) ---')
    hdr = '     ' + ''.join(str((x0 + i * step) // 100 % 10) for i in range((x1 - x0) // step))
    print(hdr)
    for y in range(y0, y1, step):
        row = ''
        for x in range(x0, x1, step):
            blk = slice(y, min(y + step, y1)), slice(x, min(x + step, x1))
            if red[blk].sum() > 2: row += 'R'
            elif paleblue[blk].sum() > 8: row += 'B'
            elif dark[blk].sum() > 2: row += '#'
            elif blue_txt[blk].sum() > 2: row += 'b'
            elif gray[blk].sum() > 4: row += 'g'
            else: row += '.'
        print(f'{y:4d} {row}')

ascii_map(60, 255, 660, 375, 4)
print()
ascii_map(660, 40, 900, 300, 4)
print()
ascii_map(530, 285, 900, 515, 4)
