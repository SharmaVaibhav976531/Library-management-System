from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser

    # ---------- LIST PAGE ----------
    list_display = (
        "username",
        "email",
        "full_name",
        "role_badge",
        "is_active",
        "last_login",
        "created_at",
    )

    list_filter = (
        "role",
        "is_active",
        "is_staff",
        "is_superuser",
        "created_at",
    )

    search_fields = ("username", "email", "first_name", "last_name")
    ordering = ("-created_at",)
    list_per_page = 25

    # ---------- READONLY ----------
    readonly_fields = (
        "created_at",
        "updated_at",
        "last_login",
        "date_joined",
    )

    # ---------- FIELDSETS (Edit Page) ----------
    fieldsets = (
        ("Authentication", {
            "fields": ("username", "password")
        }),
        ("Personal Info", {
            "fields": ("first_name", "last_name", "email")
        }),
        ("Role & Status", {
            "fields": ("role", "is_active", "is_staff", "is_superuser")
        }),
        ("Permissions", {
            "fields": ("groups", "user_permissions"),
            "classes": ("collapse",),
        }),
        ("Important Dates", {
            "fields": ("last_login", "date_joined", "created_at", "updated_at")
        }),
    )

    # ---------- ADD USER FORM ----------
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "username",
                "email",
                "password1",
                "password2",
                "role",
                "is_active",
                "is_staff",
            ),
        }),
    )

    # ---------- CUSTOM COLUMNS ----------
    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    full_name.short_description = "Full Name"

    def role_badge(self, obj):
        colors = {
            "admin": "#ef4444",      # red
            "librarian": "#3b82f6",  # blue
            "member": "#10b981",     # green
        }
        return format_html(
            '<span style="padding:4px 10px;border-radius:12px;color:white;background:{};">{}</span>',
            colors.get(obj.role, "#6b7280"),
            obj.role.upper(),
        )
    role_badge.short_description = "Role"

    # ---------- PERFORMANCE ----------
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related()
