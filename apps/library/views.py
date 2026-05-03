from rest_framework import viewsets, filters, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from .models import Category, Book
from .serializers import CategorySerializer, BookSerializer
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'author', 'isbn']
    ordering_fields = ['title', 'publication_year']

@login_required
def book_list_web(request):
    query = request.GET.get('q', '').strip()
    
    books = Book.objects.select_related('category').all()
    
    if query:
        books = books.filter(
            Q(title__icontains=query) | 
            Q(author__icontains=query) | 
            Q(isbn__icontains=query)
        )
        
    return render(request, 'library/book_list.jinja', {
        'books': books.order_by('title'),
        'query': query,
        'title': 'Library Catalog'
    })