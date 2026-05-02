from rest_framework import serializers
from .models import Category, Book

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class BookSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category.name')
    class Meta:
        model = Book
        fields = '__all__'
    def validate_isbn(self, value):
        if Book.objects.filter(isbn=value).exists():
            raise serializers.ValidationError("ISBN already exists.")
        return value