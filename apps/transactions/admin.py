from django.contrib import admin
from .models import Member, BookIssue, Reservation, Fine


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ("full_name", "member_code", "phone", "membership_type", "status")
    search_fields = ("full_name", "member_code", "phone")
    list_filter = ("status", "membership_type")


@admin.register(BookIssue)
class BookIssueAdmin(admin.ModelAdmin):
    list_display = ("id", "book", "member", "issue_date", "due_date", "status")
    search_fields = ("book__title", "member__full_name")
    list_filter = ("status", "issue_date")


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ("id", "book", "member", "reservation_date", "status")
    search_fields = ("book__title", "member__full_name")
    list_filter = ("status", "reservation_date")


@admin.register(Fine)
class FineAdmin(admin.ModelAdmin):
    list_display = ("id", "issue", "amount", "paid_status", "paid_date")
    search_fields = ("issue__member__full_name",)
    list_filter = ("paid_status", "paid_date")
