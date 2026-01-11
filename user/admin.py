from django.contrib import admin
from .models import *

@admin.register(CustomUser)
class CustomUser(admin.ModelAdmin):
    """
    This class represents a custom user administration interface for the Django admin site.

    The class is used to define how the `CustomUser` model should be displayed and managed
    in the Django admin interface. It focuses on configuring the admin view by specifying
    which fields should be displayed in the listing.

    :ivar list_display: Specifies the fields of the `CustomUser` model to be displayed in
        the list view of the Django admin interface.
    :type list_display: list[str]
    """
    list_display = ['first_name', 'last_name']