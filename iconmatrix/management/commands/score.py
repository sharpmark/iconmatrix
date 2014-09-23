# -*- coding: utf-8 -*-

import os
import shutil
from django.core.management.base import BaseCommand,CommandError
from app_parser.parser import get_app
from applications.models import Application
from accounts.models import User

class Command(BaseCommand):
    def handle(self, *args, **options):

        apps = Application.objects.all()

        for app in apps:
            app.like_count = app.get_like_count()
            app.unlike_count = app.get_unlike_count()
            app.save()
