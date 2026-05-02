from django.urls import path
from .views import IssueBookAPIView, ReturnBookAPIView

urlpatterns = [
    path('issue/', IssueBookAPIView.as_view(), name='api_issue_book'),
    path('return/', ReturnBookAPIView.as_view(), name='api_return_book'),
]