from django.urls import path
from .access_views import accesscontrol_create, accesscontrol_list, accesscontrol_detail, accesscontrol_by_event

urlpatterns = [
    path('access/store', accesscontrol_create, name='accesscontrol-create'),
    path('access/list', accesscontrol_list, name='accesscontrol-list'),
    path('access/<int:pk>/', accesscontrol_detail, name='accesscontrol-detail'),
    path('access/event/<int:event_id>/', accesscontrol_by_event, name='accesscontrol-by-event'),
]