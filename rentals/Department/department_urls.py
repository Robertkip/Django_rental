from django .urls import path
from .department_views import department_create, department_list, department_detail

urlpatterns = [
    path('department/store', department_create, name='department-create'),
    path('department/list', department_list, name='department-list'),
    path('department/<int:pk>/', department_detail, name='department-detail'),
]