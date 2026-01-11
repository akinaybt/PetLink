from django.contrib import admin
from .models import *

@admin.register(Pet)
class Pet(admin.ModelAdmin):
    """
        Represents the admin configuration for the Pet model.

        This class is used for customizing the appearance and behavior of the
        Pet model in the Django admin interface. It determines the fields to
        display in the admin list view.

        :ivar list_display: A list specifying the names of fields to display
            in the list view of the admin interface.
        :type list_display: list
        """
    list_display = ['name', 'species']