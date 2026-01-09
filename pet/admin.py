from django.contrib import admin
from .models import *
@admin.register(Pet)
class Pet(admin.ModelAdmin):
    list_display = ['name', 'species']