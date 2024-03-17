from PIL import Image
import random

image = Image.open('image2.png')
width, height = image.size

new_image = Image.new(image.mode, (width, height))

for x in range(width):
    for y in range(height):
        new_image.putpixel((x, y),
                           (random.randint(0, 255),
                            random.randint(0, 255),
                            random.randint(0, 255)))
new_image.save('image3.png')


im = Image.open('image3.png')
mode = im.mode
num_colors = im.getbands()

if len(num_colors) == 3:
    new_im = im.convert("L")
else:
    raise ValueError("Cannot convert image to monochrome.")

new_im.save('image3.png')
