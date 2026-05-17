from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie
from django.contrib import messages
from django.utils import timezone
from django.db.models import Count, Sum
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .serializers import UserRegistrationSerializer
from .models import CustomUser
from apps.library.models import Book
from apps.transactions.models import BookIssue, Fine, Member


@ensure_csrf_cookie
def home_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    return render(
        request,
        "accounts/login.jinja",
        {"title": "LMS Login"},
    )


@login_required
def dashboard_view(request):
    """Dashboard view with KPI stats for all roles"""
    stats = {
        "total_books": Book.objects.aggregate(total=Count("id"))["total"] or 0,
        "total_members": Member.objects.filter(status="active").count(),
        "issued_today": BookIssue.objects.filter(
            issue_date=timezone.now().date()
        ).count(),
        "overdue": BookIssue.objects.filter(status="overdue").count(),
        "fines_collected": Fine.objects.filter(paid_status=True).aggregate(
            total=Sum("amount")
        )["total"]
        or 0,
    }
    return render(
        request,
        "dashboard.jinja",
        {"title": "Admin Dashboard", "user": request.user, "stats": stats},
    )


@csrf_protect
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user and user.is_active:
            login(request, user)
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid credentials or inactive account")

    return render(
        request,
        "accounts/login.jinja",
        {"title": "LMS Login"},
    )


def logout_view(request):
    logout(request)
    return redirect("home")


class UserRegistrationView(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]
