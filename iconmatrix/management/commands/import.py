# -*- coding: utf-8 -*-

import os
import shutil
from django.core.management.base import BaseCommand,CommandError
from app_parser.parser import get_app
from applications.models import Application
from accounts.models import User

class Command(BaseCommand):
    def handle(self, *args, **options):

        icon_dir = './uploads/icons'

        #TODO:artist = User.objects.get(pk=1)

        for root, dirs, files in os.walk(os.path.join(icon_dir)):
            for name in files:
                app = get_app(package_name = name[:-9].replace('_', '.'))

                if app.icon == '':
                    app.icon = name
                    #icon.artist = artist
                    app.save()
