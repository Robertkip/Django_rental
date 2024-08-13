from django.urls import path
from .access_views import accesscontrol_create, accesscontrol_list, accesscontrol_detail

urlpatterns = [
    path('access/store', accesscontrol_create, name='accesscontrol-create'),
    path('access/list', accesscontrol_list, name='accesscontrol-list'),
    path('access/<int:pk>/', accesscontrol_detail, name='accesscontrol-detail'),
]