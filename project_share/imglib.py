from PIL import Image


def resize_image(avatar, size=(48, 48)):
    image = Image.open(avatar.path)
    image.resize(size, Image.ANTIALIAS).save(avatar.path, 'PNG', quality=75)
