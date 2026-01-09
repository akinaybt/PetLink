from django.contrib import admin
from .models import *

@admin.register(CustomUser)
class CustomUser(admin.ModelAdmin):
    list_display = ['first_name', 'last_name']