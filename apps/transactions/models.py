from django.db import models
from django.conf import settings
from apps.library.models import Book
from datetime import datetime, timedelta
from django.utils import timezone

class Member(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    member_code = models.CharField(max_length=20, unique=True)
    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    address = models.TextField(blank=True)
    membership_type = models.CharField(max_length=50, default='Standard')
    membership_start = models.DateField()
    membership_end = models.DateField()
    status = models.CharField(max_length=20, default='active')
    class Meta: db_table = 'members'
    def __str__(self): return f"{self.full_name} ({self.member_code})"

class BookIssue(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    issued_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    issue_date = models.DateField(default=timezone.now)
    due_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, default='issued', choices=[('issued','Issued'),('returned','Returned'),('overdue','Overdue')])
    fine_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    fine_paid = models.BooleanField(default=False)
    class Meta: db_table = 'book_issues'
    def calculate_fine(self):
        if self.return_date and self.return_date > self.due_date:
            days = (self.return_date - self.due_date).days
            return days * 5.00  # ₹5/day
        return 0.00

class Reservation(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    reservation_date = models.DateField(auto_now_add=True)
    expiry_date = models.DateField()
    status = models.CharField(max_length=20, default='pending')
    class Meta: db_table = 'reservations'

class Fine(models.Model):
    issue = models.ForeignKey(BookIssue, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    reason = models.TextField(default='Overdue return')
    paid_status = models.BooleanField(default=False)
    paid_date = models.DateField(null=True, blank=True)
    class Meta: db_table = 'fines'

class Notification(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    message = models.TextField()
    notification_type = models.CharField(max_length=50)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta: db_table = 'notifications'