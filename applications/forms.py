# -*- coding: utf-8 -*-

from django import forms
from django.forms import Form

class SearchForm(Form):

    query = forms.CharField(max_length=200)
