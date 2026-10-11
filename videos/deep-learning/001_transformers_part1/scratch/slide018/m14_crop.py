from PIL import Image
im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_018.jpg').convert('RGB')
c = im.crop((180, 85, 690, 420))
c = c.resize((c.width*2, c.height*2), Image.LANCZOS)
c.save('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/scratch/slide018/crop_gap.png')
print("saved", c.size)
