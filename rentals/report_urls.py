from django.urls import path
from .report_views import report_create, report_list, report_detail

urlpatterns = [
    path('report/store', report_create, name='report-create'),
    path('report/list', report_list, name='report-list'),
    path('report/<int:pk>/', report_detail, name='report-detail'),
]