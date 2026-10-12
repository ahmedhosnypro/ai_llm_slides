from PIL import Image
import os
R = Image.open('recreated_pptx/qa/slide022/render_4.png').convert('RGB')
O = Image.open('unique_slides/slide_022.jpg').convert('RGB')
OUT = 'recreated_pptx/qa/slide022/crops'
os.makedirs(OUT, exist_ok=True)
S = 150/72.0  # frame px -> render px (2.0833)
regions = {
  'eq1':  (75, 82, 425, 252),
  'eq2':  (522, 82, 800, 252),
  'dec':  (75, 249, 773, 348),
  'diag': (222, 344, 825, 514),
}
for name, (x0, y0, x1, y1) in regions.items():
    rc = R.crop((int(x0*S), int(y0*S), int(x1*S), int(y1*S)))
    oc = O.crop((x0, y0, x1, y1)).resize(rc.size, Image.LANCZOS)
    rc.save(f'{OUT}/{name}_render.png')
    oc.save(f'{OUT}/{name}_orig.png')
    print(name, rc.size)
