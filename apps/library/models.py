# apps/library/models.py

from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "categories"

    def __str__(self):
        return self.name


class Book(models.Model):
    isbn = models.CharField(max_length=13, unique=True)
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=200)
    publisher = models.CharField(max_length=150, blank=True)
    publication_year = models.PositiveIntegerField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    total_copies = models.PositiveIntegerField(default=1)
    available_copies = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    description = models.TextField(blank=True)
    cover_image = models.ImageField(upload_to="covers/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "books"

    def __str__(self):
        return f"{self.title} ({self.isbn})"
