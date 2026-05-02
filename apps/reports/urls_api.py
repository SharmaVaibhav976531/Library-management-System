from django.urls import path
from .views import DashboardKPIAPIView, ExportCSVAPIView

urlpatterns = [
    path('dashboard/', DashboardKPIAPIView.as_view(), name='api_dashboard'),
    path('export/csv/', ExportCSVAPIView.as_view(), name='api_export_csv'),
]