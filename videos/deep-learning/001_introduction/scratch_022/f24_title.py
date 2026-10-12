from PIL import ImageFont
title = "Visualization of Single Perceptron"
cands = {
 'TNR-Bold-32': '/usr/share/fonts/liberation/LiberationSerif-Bold.ttf',
 'TNR-Bold-31.7': None,
 'Arial-Bold-30': '/usr/share/fonts/liberation/LiberationSans-Bold.ttf',
 'Arial-Bold-29.3': None,
}
import os
paths = {}
for p in ['/usr/share/fonts/liberation/LiberationSerif-Bold.ttf','/usr/share/fonts/liberation/LiberationSans-Bold.ttf']:
    if os.path.exists(p): paths[os.path.basename(p)] = p
print('fonts found:', paths)
if 'LiberationSerif-Bold.ttf' in paths:
    for fs in (30,31,31.5,32,33,34):
        f = ImageFont.truetype(paths['LiberationSerif-Bold.ttf'], int(fs*4))  # 4x for precision
        w = f.getlength(title)/4
        print(f'TNR Bold {fs}: advance {w:.1f}px (target 490)')
if 'LiberationSans-Bold.ttf' in paths:
    for fs in (28,29,29.5,30,31):
        f = ImageFont.truetype(paths['LiberationSans-Bold.ttf'], int(fs*4))
        w = f.getlength(title)/4
        print(f'Arial Bold {fs}: advance {w:.1f}px (target 490)')
