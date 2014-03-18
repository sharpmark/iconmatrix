import os
import shutil
from django.core.management.base import BaseCommand,CommandError
from app_parser.parser import get_app_from_url
from applications.models import Application
from icons.models import *
from django.contrib.auth.models import User

class Command(BaseCommand):
    def handle(self, *args, **options):
        dir_base = './uploads/res'

        dir_128px = 'mipmap-xhdpi'
        dir_192px = 'mipmap-xxhdpi'

        dir_dest = './uploads/'

        artist = User.objects.get(pk=1)

        for root, dirs, files in os.walk(os.path.join(dir_base, dir_128px)):
            for name in files:
                app_wdj_url = 'http://www.wandoujia.com/apps/' + name[:-9].replace('_', '.')
                app = get_app_from_url(app_wdj_url)

                if app != None:
                    if app.status != Application.UPLOAD and app.status != Application.FINISH:
                        icon = Icon(application=app)
                        icon.image_192px = image_192px_name(icon, name)
                        icon.image_128px = image_128px_name(icon, name)
                        icon.artist = artist

                        shutil.copy2(os.path.join(dir_base, dir_192px, name), icon.image_192px.path)
                        shutil.copy2(os.path.join(dir_base, dir_128px, name), icon.image_128px.path)

                        icon.public_image()

                        icon.save()

                        app.last_icon = icon
                        app.status = Application.FINISH
                        app.save()
