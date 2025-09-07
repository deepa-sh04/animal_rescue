# core/admin.py
from django.contrib import admin
from .models import Animal, Profile # Make sure to import Profile

admin.site.register(Animal)
admin.site.register(Profile)