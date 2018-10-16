#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
from .models import UserProfile

class ProfileForm(forms.Form):
    first_name = forms.CharField(label='First Name', max_length=50, required=False)
    last_name = forms.CharField(label='Last Name', max_length=50, required=False)
    org = forms.CharField(label='Organization', max_length=50, required=False)

class AvatarUploadForm(forms.Form):
    avatar_file = forms.ImageField()