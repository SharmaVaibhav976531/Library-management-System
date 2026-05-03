from django.urls import path
from . import views

urlpatterns = [
    path("", views.transaction_history_view, name="transaction_history"),
    path("issue/", views.issue_book_view, name="issue_page"),
    path("return/", views.return_book_view, name="return_page"),
    path('fine/<int:fine_id>/pay/', views.pay_fine_view, name='pay_fine'),
]
