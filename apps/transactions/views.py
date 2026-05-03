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
from django.contrib.auth.decorators import login_required


def transaction_history_view(request):
    issues = BookIssue.objects.all().order_by("-issue_date")
    return render(
        request,
        "transactions/history.jinja",
        {"issues": issues, "title": "Transaction History"},
    )


@login_required
def issue_book_view(request):
    members = Member.objects.filter(status="active").order_by("full_name")
    books = Book.objects.filter(available_copies__gt=0).order_by("title")

    if request.method == "POST":
        with transaction.atomic():
            member_id = request.POST.get("member_id")
            book_id = request.POST.get("book_id")
            try:
                member = Member.objects.select_for_update().get(id=member_id)
                book = Book.objects.select_for_update().get(id=book_id)

                # Validation checks
                if book.available_copies <= 0:
                    messages.error(request, "No copies available for this book.")
                    return redirect("issue_page")

                if member.status != "active":
                    messages.error(request, "Member account is not active.")
                    return redirect("issue_page")

                overdue_count = BookIssue.objects.filter(
                    member=member, status="overdue"
                ).count()
                if overdue_count >= 2:
                    messages.error(
                        request, "Member has reached overdue book limit (2)."
                    )
                    return redirect("issue_page")

                # Create issue record
                issue = BookIssue.objects.create(
                    book=book,
                    member=member,
                    issued_by=request.user,
                    issue_date=timezone.now().date(),
                    due_date=timezone.now().date() + timedelta(days=14),
                    status="issued",
                )

                # Decrement available copies
                book.available_copies -= 1
                book.save()

                messages.success(
                    request,
                    f"✅ Book '{book.title}' issued to {member.full_name}. Due: {issue.due_date.strftime('%d %b %Y')}",
                )
                return redirect("book_list_web")

            except Member.DoesNotExist:
                messages.error(request, "Selected member not found.")
            except Book.DoesNotExist:
                messages.error(request, "Selected book not found.")
            except Exception as e:
                messages.error(request, f"Error: {str(e)}")

    return render(
        request,
        "transactions/issue.jinja",
        {"title": "Issue Book", "members": members, "books": books},
    )


@login_required
def return_book_view(request):
    if request.method == "POST":
        issue_id = request.POST.get("issue_id")

        try:
            with transaction.atomic():
                # Fetch the issue record (include both 'issued' and 'overdue' status)
                issue = BookIssue.objects.select_for_update().get(id=issue_id)

                # Check if already returned
                if issue.status == "returned":
                    messages.error(request, "Book has already been returned.")
                    return redirect("transaction_history")

                # Set return date
                issue.return_date = timezone.now().date()

                # Calculate fine if overdue
                if issue.return_date > issue.due_date:
                    days_overdue = (issue.return_date - issue.due_date).days
                    fine_amount = days_overdue * 5.00  # ₹5 per day
                    issue.fine_amount = fine_amount

                    # Create fine record
                    Fine.objects.create(
                        issue=issue,
                        amount=fine_amount,
                        reason=f"Overdue by {days_overdue} days",
                        paid_status=False,
                    )

                    messages.warning(
                        request,
                        f"⚠️ Book is {days_overdue} days overdue. Fine: ₹{fine_amount:.2f}",
                    )
                else:
                    issue.fine_amount = 0.00
                    messages.success(request, "✅ Book returned on time. No fine.")

                issue.status = "returned"

                # Update book availability
                book = issue.book
                book.available_copies += 1
                book.save()

                # Save issue record
                issue.save()

                messages.success(
                    request,
                    f"✅ Book '{book.title}' returned successfully! Fine: ₹{issue.fine_amount:.2f}",
                )

        except BookIssue.DoesNotExist:
            messages.error(request, "Transaction not found.")
        except Exception as e:
            messages.error(request, f"Error processing return: {str(e)}")
            import traceback

            traceback.print_exc()

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


@login_required
def pay_fine_view(request, fine_id):
    """Process fine payment"""
    try:
        with transaction.atomic():
            fine = Fine.objects.select_for_update().get(
                id=fine_id, 
                paid_status=False
            )
            
            # Mark as paid
            fine.paid_status = True
            fine.paid_date = timezone.now().date()
            fine.save()
            
            messages.success(
                request, 
                f"✅ Fine of ₹{fine.amount:.2f} collected successfully!"
            )
            
    except Fine.DoesNotExist:
        messages.error(request, "Fine already paid or not found.")
    except Exception as e:
        messages.error(request, f"Payment failed: {str(e)}")
    
    return redirect('transaction_history')
