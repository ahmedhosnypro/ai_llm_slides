from PIL import Image
im43 = Image.open("unique_slides/slide_043.jpg").convert("RGB")
im44 = Image.open("unique_slides/slide_044.jpg").convert("RGB")
def crop_up(im, box, scale, out):
    c = im.crop(box)
    c = c.resize((c.width*scale, c.height*scale), Image.LANCZOS)
    c.save(out)
    print(out, c.size)
# titles x3
crop_up(im43, (500, 44, 920, 104), 3, "scratch/slide044/title43_x3.png")
crop_up(im44, (500, 44, 920, 104), 3, "scratch/slide044/title44_x3.png")
# inset x4
crop_up(im44, (726, 70, 916, 308), 4, "scratch/slide044/inset44_x4.png")
# badge zone 44 x4 (occlusion detail)
crop_up(im44, (860, 40, 920, 100), 6, "scratch/slide044/badge44_x6.png")
