# -*- coding: utf-8 -*-

import os
import shutil
from django.core.management.base import BaseCommand,CommandError
from PIL import Image, ImageFilter


def dropShadow(redraw_image, original_image):

    offset = (0, 10)
    redraw_xy = (60, 60)
    original_xy = (360, 92)
    width = 540
    height = 360

    background = (0x3a, 0x3d, 0x3f)
    shadow = (0x00, 0x00, 0x00)
    iterations = 10

    canvas = Image.new('RGBA', (width, height), background)

    canvas.paste(shadow, (redraw_xy[0] + offset[0], redraw_xy[1] + offset[1]), redraw_image)
    canvas.paste(shadow, (original_xy[0] + offset[0], original_xy[1] + offset[1]), original_image)

    for i in range(iterations):
        canvas = canvas.filter(ImageFilter.BLUR)

    canvas.paste(redraw_image, (redraw_xy[0], redraw_xy[1]), redraw_image)
    canvas.paste(original_image, (original_xy[0], original_xy[1]), original_image)

    return canvas


def load_image(filename):

    if not os.path.exists(filename): return None

    image = Image.open(filename)
    image.load()

    if image.mode != 'RGBA':
        image = image.convert('RGBA')

    return image


class Command(BaseCommand):


    def handle(self, *args, **options):

        for root, dirs, files in os.walk(os.path.join('./uploads/icons')):
            for name in files:
                if name[-4:] != '.png': continue

                try:

                    redraw = load_image(os.path.join('./uploads/icons', name))

                    original = load_image(os.path.join('./uploads/original', name))

                    if redraw != None and original != None:
                        original.thumbnail((128, 128), Image.ANTIALIAS)

                        thumb = dropShadow(redraw, original)
                        thumb.save(os.path.join('./uploads/thumb', name))
                    else:
                        print 'warning: miss image ' + name
                except:
                    print 'error: read file ', name
