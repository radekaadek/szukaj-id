from PIL import Image
import os

images_path = "./static/lolranks"

def crop_image(image, x, y, width, height, image_path):
    image = image.crop((x, y, x+width, y+height))
    image.save(image_path)

def check_transparent_row(image, row):
    for x in range(image.size[0]):
        if image.getpixel((x, row))[3] != 0:
            return False
    return True

def check_transparent_column(image, column):
    for y in range(image.size[1]):
        if image.getpixel((column, y))[3] != 0:
            return False
    return True

# Iterate directory
for path in os.listdir(images_path):
    image_path = os.path.join(images_path, path)
    im = Image.open(image_path)
    pixels = im.load()
    width, height = im.size
    rows = []
    columns = []
    # check for transparent rows and columns
    for row in range(height):
        if check_transparent_row(im, row):
            rows.append(row)
    for column in range(width):
        if check_transparent_column(im, column):
            columns.append(column)
    # crop image
    for row in rows:
        crop_image(im, 0, row, width, 1, image_path)
    for column in columns:
        crop_image(im, column, 0, 1, height, image_path)
    im.close()

