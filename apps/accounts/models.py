# apps/accounts/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class CustomUser(AbstractUser):
    ROLE_CHOICES = (('admin', 'Admin'), ('librarian', 'Librarian'), ('member', 'Member'))
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='member')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f"{self.username} ({self.role})"