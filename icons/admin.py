# -*- coding: utf-8 -*-
from django.contrib import admin
from icons.models import Icon, Comment, Like
from icons.admin_set_artist import ui_list

class IconAdmin(admin.ModelAdmin):
    fields = ['artist']
    list_display = ['application', 'image_icon']
    list_filter = ['application__status', 'artist']
    actions = ui_list

admin.site.register(Icon, IconAdmin)
