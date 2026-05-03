from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone

from .models import Member, BookIssue, Reservation, Fine, Notification

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = (
        "member_code",
        "full_name",
        "user",
        "phone",
        "membership_type",
        "membership_status_badge",
        "membership_period",
    )

    search_fields = (
        "member_code",
        "full_name",
        "phone",
        "user__username",
    )

    list_filter = (
        "membership_type",
        "status",
        "membership_start",
        "membership_end",
    )

    readonly_fields = ("membership_status_badge",)

    fieldsets = (
        ("Member Info", {
            "fields": (
                "user",
                "member_code",
                "full_name",
                "phone",
                "address",
            )
        }),
        ("Membership Details", {
            "fields": (
                "membership_type",
                "membership_start",
                "membership_end",
                "status",
                "membership_status_badge",
            )
        }),
    )

    ordering = ("-membership_start",)

    def membership_period(self, obj):
        return f"{obj.membership_start} → {obj.membership_end}"
    membership_period.short_description = "Membership Period"



    def membership_status_badge(self, obj):
        if not obj.pk or not obj.membership_end:
            return "-"

        today = timezone.now().date()

        if obj.membership_end < today:
            color = "red"
            label = "Expired"
        else:
            color = "green"
            label = "Active"

        return format_html(
            '<span style="color:white;background:{};padding:4px 8px;border-radius:6px;">{}</span>',
            color,
            label,
        )

    membership_status_badge.short_description = "Status"

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("user")


@admin.register(BookIssue)
class BookIssueAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "book",
        "member",
        "issued_by",
        "issue_date",
        "due_date",
        "status_badge",
        "fine_display",
    )

    search_fields = (
        "book__title",
        "member__full_name",
        "member__member_code",
    )

    list_filter = (
        "status",
        "issue_date",
        "due_date",
        "fine_paid",
    )

    readonly_fields = ("fine_display",)

    fieldsets = (
        ("Issue Details", {
            "fields": (
                "book",
                "member",
                "issued_by",
            )
        }),
        ("Dates", {
            "fields": (
                "issue_date",
                "due_date",
                "return_date",
            )
        }),
        ("Fine Info", {
            "fields": (
                "fine_amount",
                "fine_paid",
                "fine_display",
            )
        }),
        ("Status", {
            "fields": ("status",)
        }),
    )

    ordering = ("-issue_date",)

    def status_badge(self, obj):
        today = timezone.now().date()

        if obj.status == "returned":
            color, label = "#10b981", "Returned"
        elif obj.due_date < today and obj.status == "issued":
            color, label = "#ef4444", "Overdue"
        else:
            color, label = "#3b82f6", "Issued"

        return format_html(
            '<span style="padding:4px 10px;border-radius:12px;color:white;background:{};">{}</span>',
            color, label
        )
    status_badge.short_description = "Status"

    def fine_display(self, obj):
        fine = obj.calculate_fine()
        return f"₹ {fine:.2f}"
    fine_display.short_description = "Calculated Fine"

    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            "book", "member", "issued_by"
        )


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "book",
        "member",
        "reservation_date",
        "expiry_date",
        "status_badge",
    )

    search_fields = (
        "book__title",
        "member__full_name",
    )

    list_filter = (
        "status",
        "reservation_date",
        "expiry_date",
    )

    ordering = ("-reservation_date",)

    def status_badge(self, obj):
        today = timezone.now().date()
        if obj.expiry_date < today:
            color, label = "#ef4444", "Expired"
        elif obj.status.lower() == "pending":
            color, label = "#f59e0b", "Pending"
        else:
            color, label = "#10b981", obj.status.title()

        return format_html(
            '<span style="padding:4px 10px;border-radius:12px;color:white;background:{};">{}</span>',
            color, label
        )
    status_badge.short_description = "Status"

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("book", "member")


@admin.register(Fine)
class FineAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "issue",
        "amount",
        "paid_status_badge",
        "paid_date",
    )

    search_fields = (
        "issue__member__full_name",
        "issue__book__title",
    )

    list_filter = (
        "paid_status",
        "paid_date",
    )

    ordering = ("-paid_date",)

    def paid_status_badge(self, obj):
        if obj.paid_status:
            color, label = "#10b981", "Paid"
        else:
            color, label = "#ef4444", "Unpaid"

        return format_html(
            '<span style="padding:4px 10px;border-radius:12px;color:white;background:{};">{}</span>',
            color, label
        )
    paid_status_badge.short_description = "Payment Status"

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("issue")


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = (
        "member",
        "notification_type",
        "is_read",
        "created_at",
    )

    search_fields = (
        "member__full_name",
        "message",
    )

    list_filter = (
        "notification_type",
        "is_read",
        "created_at",
    )

    readonly_fields = ("created_at",)

    ordering = ("-created_at",)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("member")
