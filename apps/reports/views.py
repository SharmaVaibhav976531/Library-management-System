from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Count, Sum
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated
import csv

from apps.library.models import Book
from apps.transactions.models import BookIssue, Fine, Member

@login_required
def dashboard_kpis(request):
    from apps.library.models import Book
    from apps.transactions.models import BookIssue, Fine, Member
    from django.utils import timezone
    from django.db.models import Count, Sum
    
    stats = {
        'total_books': Book.objects.count(),
        'total_members': Member.objects.filter(status='active').count(),
        'issued_today': BookIssue.objects.filter(
            issue_date=timezone.now().date()
        ).count(),
        'overdue': BookIssue.objects.filter(status='overdue').count(),
        'fines_collected': Fine.objects.filter(
            paid_status=True
        ).aggregate(total=Sum('amount'))['total'] or 0,
        'fines_pending': Fine.objects.filter(
            paid_status=False
        ).aggregate(total=Sum('amount'))['total'] or 0,
    }
    
    return render(request, 'reports/dashboard.jinja', {
        'title': 'Library Analytics',
        'user': request.user,
        'stats': stats
    })

@login_required
def export_csv(request):
    """Export library catalog to CSV file"""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="library_catalog.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['ISBN', 'Title', 'Author', 'Category', 'Total Copies', 'Available'])
    
    books = Book.objects.select_related('category').all()
    for book in books:
        writer.writerow([
            book.isbn,
            book.title,
            book.author,
            book.category.name if book.category else 'Uncategorized',
            book.total_copies,
            book.available_copies
        ])
    
    return response

class DashboardKPIAPIView(APIView):
    """API endpoint for dashboard KPIs - Admin only"""
    permission_classes = [IsAdminUser]
    
    def get(self, request):
        stats = {
            'total_books': Book.objects.aggregate(total=Count('id'))['total'] or 0,
            'total_members': Member.objects.filter(status='active').count(),
            'issued_today': BookIssue.objects.filter(
                issue_date=timezone.now().date()
            ).count(),
            'overdue': BookIssue.objects.filter(status='overdue').count(),
            'fines_collected': Fine.objects.filter(
                paid_status=True
            ).aggregate(total=Sum('amount'))['total'] or 0,
        }
        return Response({'success': True, 'data': stats})

class ExportCSVAPIView(APIView):
    """API endpoint for CSV export - Admin only"""
    permission_classes = [IsAdminUser]
    
    def get(self, request):
        return export_csv(request)