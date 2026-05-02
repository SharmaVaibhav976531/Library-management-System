from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard_kpis, name='reports_dashboard'),
    path('export/csv/', views.export_csv, name='export_csv'),
]