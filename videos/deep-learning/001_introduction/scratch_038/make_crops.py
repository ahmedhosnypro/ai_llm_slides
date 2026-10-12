from PIL import Image
im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_038.jpg').convert('RGB')
D = '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/scratch_038/'
# full diagram box region
c1 = im.crop((150, 250, 815, 515)).resize((1330, 530), Image.LANCZOS)
c1.save(D+'diag_full_2x.png')
# brown slab + annotations
c2 = im.crop((180, 255, 400, 510)).resize((660, 765), Image.LANCZOS)
c2.save(D+'diag_slab_3x.png')
# filter stack + circles region
c3 = im.crop((380, 300, 812, 480)).resize((1296, 540), Image.LANCZOS)
c3.save(D+'diag_stack_3x.png')
print("ok")
