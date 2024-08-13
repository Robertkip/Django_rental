from django.urls import path
from .notification_views import notification_create, notification_list, notification_detail


urlpatterns = [
    path('notification/store', notification_create, name='notification-create'),
    path('notification/list', notification_list, name='notification-list'),
    path('notification/<int:pk>/', notification_detail, name='notification-detail'),
]