from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Book

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "description_short", "created_at")
    search_fields = ("name",)
    ordering = ("name",)
    readonly_fields = ("created_at",)

    def description_short(self, obj):
        return (obj.description[:50] + "...") if obj.description else "-"
    description_short.short_description = "Description"


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = (
        "cover_preview",
        "title",
        "isbn",
        "author",
        "category",
        "copies_status",
        "price",
        "created_at",
    )

    list_filter = (
        "category",
        "publication_year",
        "created_at",
    )

    search_fields = (
        "title",
        "isbn",
        "author",
        "publisher",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
        "cover_preview",
    )

    ordering = ("-created_at",)
    list_per_page = 20

    fieldsets = (
        ("Book Information", {
            "fields": (
                "isbn",
                "title",
                "author",
                "publisher",
                "publication_year",
                "category",
            )
        }),
        ("Inventory Details", {
            "fields": (
                "total_copies",
                "available_copies",
            )
        }),
        ("Pricing & Description", {
            "fields": (
                "price",
                "description",
            )
        }),
        ("Cover Image", {
            "fields": (
                "cover_image",
                "cover_preview",
            )
        }),
        ("Timestamps", {
            "fields": (
                "created_at",
                "updated_at",
            )
        }),
    )


    def cover_preview(self, obj):
        if obj.cover_image:
            return format_html(
                '<img src="{}" style="height:60px;border-radius:6px;" />',
                obj.cover_image.url
            )
        return "-"
    cover_preview.short_description = "Cover"

    def copies_status(self, obj):
        if obj.available_copies == 0:
            color = "#ef4444"
            label = "Out of Stock"
        elif obj.available_copies < obj.total_copies:
            color = "#f59e0b"
            label = "Partially Available"
        else:
            color = "#10b981"
            label = "Available"

        return format_html(
            '<span style="padding:4px 10px;border-radius:12px;color:white;background:{};">{} ({}/{})</span>',
            color,
            label,
            obj.available_copies,
            obj.total_copies,
        )
    copies_status.short_description = "Copies"

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related("category")
