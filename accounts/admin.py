from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from . import models


@admin.register(models.User)
class UserAdmin(DjangoUserAdmin):
    fieldsets = (
        (None, {"fields": ("email", "password")},),
        (
            "Personal Info",
            {"fields": ("first_name", "last_name", "is_it_manager",
                        "is_it_engineer","phone_number","job_title", "department", 'city')},
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (
            "Important Dates",
            {"fields": ("last_login", "date_joined")},
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2", "is_it_manager", "is_it_engineer",),
            },
        ),
    )
    list_display = (
        'id',
        "email",
        "first_name",
        "last_name",
        "is_it_manager",
        "is_it_engineer",
    )
    list_display_links = list_display
    list_filter = ("is_it_manager", "is_it_engineer", "is_staff",
                   "is_superuser", "is_active", "groups",)
    search_fields = ("email", "first_name", "last_name")
    ordering = ("email",)
