from PIL import Image
import os

# Removes transparent rows and columns from the start and end of an image

# Set images folder directory
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

# Iterate over images in directory
for path in os.listdir(images_path):
    image_path = os.path.join(images_path, path)
    im = Image.open(image_path)
    pixels = im.load()
    width, height = im.size
    rows = []
    columns = []
    front_transparent_collumns = 0
    back_transparent_columns = 0
    front_transparent_rows = 0
    back_transparent_row = 0
    # check for transparent rows and columns
    for row in range(height):
        if check_transparent_row(im, row):
            front_transparent_rows += 1
        else:
            break
    cropped_image = im.crop((0, front_transparent_rows, width, height))
    for column in range(width):
        if check_transparent_column(im, column):
            front_transparent_collumns += 1
        else:
            break
    cropped_image = cropped_image.crop((front_transparent_collumns, 0, width, height))
    for row in reversed(range(height)):
        if check_transparent_row(im, row):
            back_transparent_row += 1
        else:
            break
    cropped_image = cropped_image.crop((0, 0, width-back_transparent_columns, height-back_transparent_row))
    for column in reversed(range(width)):
        if check_transparent_column(im, column):
            back_transparent_columns += 1
        else:
            break
    cropped_image = cropped_image.crop((0, 0, width-back_transparent_columns, height-back_transparent_row))

    cropped_image.save(image_path)
    im.close()

