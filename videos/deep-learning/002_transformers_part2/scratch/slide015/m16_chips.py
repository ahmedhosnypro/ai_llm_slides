from PIL import Image
import numpy as np
im = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_015.jpg').convert('RGB')).astype(int)
def hx(t): return '#%02X%02X%02X' % tuple(t)
print('h1 chip column scan x586..640, y340..432:')
print('      ' + ' '.join(f'{x:4d}' for x in range(586, 641, 6)))
for y in range(340, 433, 4):
    print(f'y={y:3d}: ' + ' '.join(hx(im[y,x]) for x in range(586, 641, 6)))
print()
print('h2 chip column scan x636..690, y305..415:')
print('      ' + ' '.join(f'{x:4d}' for x in range(636, 691, 6)))
for y in range(305, 416, 4):
    print(f'y={y:3d}: ' + ' '.join(hx(im[y,x]) for x in range(636, 691, 6)))
