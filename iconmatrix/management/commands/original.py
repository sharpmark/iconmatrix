# -*- coding: utf-8 -*-

import os
import shutil
from django.core.management.base import BaseCommand,CommandError
from applications.models import Application
import urllib


class Command(BaseCommand):


    def handle(self, *args, **options):

        apps = Application.objects.all()

        for app in apps:
            try:
                dest_file = os.path.join('./uploads/original/%s' % app.icon)

                if not os.path.exists(dest_file):
                    urllib.urlretrieve(app.original_icon_image, dest_file)

            except:
                print 'not ' + app.original_icon_image
                if os.path.exists(dest_file):
                    os.path.remove(dest_file)
