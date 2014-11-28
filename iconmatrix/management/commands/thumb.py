# -*- coding: utf-8 -*-

import os
import shutil
from django.core.management.base import BaseCommand, CommandError
from applications.models import Application
from PIL import ImageFont, ImageDraw
from PIL import ImageFilter, Image
from django.conf import settings


def shadow_blur(image, width, height):

    background = (75, 75, 75) #(84, 84, 84)
    shadow = (0x00, 0x00, 0x00)

    canvas = Image.new('RGBA', (width, height), background)
    canvas.paste(shadow, (5, 13), image)

    for i in range(5):
        canvas = canvas.filter(ImageFilter.BLUR)

    return canvas


def drop_shadow(redraw_image, original_image):

    redraw_xy = (30, 137)
    original_xy = (271, 136)

    canvas = load_image('./static/images/dark-background.png')

    canvas.paste(shadow_blur(redraw_image, 202, 210), (redraw_xy[0], redraw_xy[1]))
    canvas.paste(shadow_blur(original_image, 138, 146), (original_xy[0], original_xy[1]))

    canvas.paste(redraw_image, (redraw_xy[0] + 5, redraw_xy[1] + 5), redraw_image)
    canvas.paste(original_image, (original_xy[0] + 5, original_xy[1] + 5), original_image)

    return canvas


def write_info(canvas, app):

    title = Image.new('RGBA', (396, 28), (70, 70, 70))

    draw = ImageDraw.Draw(title)
    draw.fontmode = "L"

    name_font = ImageFont.truetype(settings.FONT, 28)
    x, y = name_font.getsize(app.name)
    draw.text( (0, 0), app.name, (177, 177, 177), name_font)

    artist_font = ImageFont.truetype(settings.FONT, 15)

    if app.artist:
        draw.text( (x + 22, 11), "@%s" % app.artist, (177, 177, 177), artist_font)
    #else:
    #    draw.text( (x + 22, 11), "by Smartisan", (177, 177, 177), artist_font)

    canvas.paste(title, (22, 44))

    return canvas


def load_image(filename):

    if not os.path.exists(filename): return None

    image = Image.open(filename)
    #image.load()

    if image.mode != 'RGBA':
        image = image.convert('RGBA')

    return image


class Command(BaseCommand):


    def handle(self, *args, **options):

        apps = Application.objects.all()

        for app in apps:
            redraw = load_image(os.path.join('./uploads/icons/%s' % app.icon))
            original = load_image(os.path.join('./uploads/original/%s' % app.icon))

            if redraw != None and original != None:
                original.thumbnail((128, 128), Image.ANTIALIAS)

                thumb = drop_shadow(redraw, original)
                write_info(thumb, app)
                thumb.save(os.path.join('./uploads/thumb/dark/%s' % app.icon))

            #    print '+done: %s' % app.icon
            #else:
            #    print '-miss: %s' % app.icon
