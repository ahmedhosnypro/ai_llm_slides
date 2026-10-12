from PIL import Image
import numpy as np
V='/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction'
f16=np.asarray(Image.open(V+'/unique_slides/slide_016.jpg').convert('RGB')).astype(int)
f09=np.asarray(Image.open(V+'/unique_slides/slide_009.jpg').convert('RGB')).astype(int)
print('f16 x128..132, y225..246:')
for y in range(225,247):
    print(y,[tuple(f16[y,x]) for x in range(128,133)])
print()
print('f16 y242..246, x135..151:')
for y in range(242,247):
    print(y,[tuple(f16[y,x]) for x in range(135,152)])
print()
print('f09 same regions for comparison:')
print('f09 x128..132 y225..246:')
for y in range(225,247):
    print(y,[tuple(f09[y,x]) for x in range(128,133)])
