from django.urls import path
from . import views

urlpatterns = [
    path('books/', views.book_list_web, name='book_list_web'),
]