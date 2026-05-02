from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser

    fieldsets = UserAdmin.fieldsets + (
        ("Additional Info", {"fields": ("role", "created_at", "updated_at")}),
    )

    readonly_fields = ("created_at", "updated_at")

    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "role",
        "is_active",
        "created_at",
    )
    list_filter = ("role", "is_active", "created_at")
    search_fields = ("username", "email", "first_name", "last_name")
    ordering = ("-created_at",)


