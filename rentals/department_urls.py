from django.urls import path
from .department_views import department_permission_create, department_permission_list, department_permission_detail

urlpatterns = [
    path('department_permission/store', department_permission_create, name='department_permission-create'),
    path('department_permission/list', department_permission_list, name='department_permission-list'),
    path('department_permission/<int:pk>/', department_permission_detail, name='department_permission-detail'),
]