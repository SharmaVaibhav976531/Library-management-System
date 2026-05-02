from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import BookIssue, Member, Reservation, Fine
from apps.library.models import Book


def transaction_history_view(request):
    issues = BookIssue.objects.all().order_by("-issue_date")
    return render(
        request,
        "transactions/history.jinja",
        {"issues": issues, "title": "Transaction History"},
    )


def issue_book_view(request):
    if request.method == "POST":
        with transaction.atomic():
            member_id = request.POST.get("member_id")
            book_id = request.POST.get("book_id")
            try:
                member = Member.objects.select_for_update().get(id=member_id)
                book = Book.objects.select_for_update().get(id=book_id)
                if book.available_copies <= 0 or member.status != "active":
                    messages.error(request, "Invalid issue request.")
                    return redirect("issue_page")
                BookIssue.objects.create(
                    book=book,
                    member=member,
                    issued_by=request.user,
                    due_date=timezone.now() + timedelta(days=14),
                )
                book.available_copies -= 1
                book.save()
                messages.success(request, "Book issued successfully.")
            except Exception as e:
                messages.error(request, str(e))
    return render(request, "transactions/issue.jinja", {"title": "Issue Book"})


def return_book_view(request):
    if request.method == "POST":
        issue_id = request.POST.get("issue_id")
        try:
            issue = BookIssue.objects.get(id=issue_id, status__in=["issued", "overdue"])
            issue.return_date = timezone.now()
            fine = issue.calculate_fine()
            issue.fine_amount = fine
            issue.status = "overdue" if fine > 0 else "returned"
            issue.save()
            issue.book.available_copies += 1
            issue.book.save()
            if fine > 0:
                Fine.objects.create(issue=issue, amount=fine)
            messages.success(request, f"Book returned. Fine: ₹{fine:.2f}")
        except Exception as e:
            messages.error(request, str(e))
    return redirect("transaction_history")


class IssueBookAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        return Response(
            {"detail": "Issue logic handled via web view"}, status=status.HTTP_200_OK
        )


class ReturnBookAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        return Response(
            {"detail": "Return logic handled via web view"}, status=status.HTTP_200_OK
        )
