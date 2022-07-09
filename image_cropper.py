from PIL import Image
import os

# Removes transparent rows and columns from the start and end of an image

# Set images folder directory
images_path = "./static/lolranks"

def crop_image(image, x, y, width, height) -> Image:
    image = image.crop((x, y, x+width, y+height))
    return image

def check_transparent_row(image, row) -> bool:
    for x in range(image.size[0]):
        if image.getpixel((x, row))[3] != 0:
            return False
    return True

def check_transparent_column(image, column) -> bool:
    for y in range(image.size[1]):
        if image.getpixel((column, y))[3] != 0:
            return False
    return True

def crop_transparency(im) -> Image:
    width, height = im.size
    front_transparent_columns = 0
    back_transparent_columns = 0
    front_transparent_rows = 0
    back_transparent_rows = 0
    # check for transparent rows and columns
    for row in range(height):
        if check_transparent_row(im, row):
            front_transparent_rows += 1
        else:
            break
    for column in range(width):
        if check_transparent_column(im, column):
            front_transparent_columns += 1
        else:
            break
    for row in reversed(range(height)):
        if check_transparent_row(im, row):
            back_transparent_rows += 1
        else:
            break
    for column in reversed(range(width)):
        if check_transparent_column(im, column):
            back_transparent_columns += 1
        else:
            break
    cropped_image = crop_image(im, front_transparent_columns, front_transparent_rows, width-back_transparent_columns, height-back_transparent_rows)
    return cropped_image

def main():
    # Iterate over images in directory
    for path in os.listdir(images_path):
        image_path = os.path.join(images_path, path)
        im = Image.open(image_path)
        cropped_image = crop_transparency(im)
        cropped_image.save(image_path)
        im.close()

if __name__ == '__main__':
    main()
