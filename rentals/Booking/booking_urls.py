from django.urls import path
from .booking_views import booking_create, booking_list, booking_detail, booking_by_event


urlpatterns = [
    path('booking/store/<int:event_id>/', booking_by_event, name='booking-by-event'),
    path('booking/store', booking_create, name='booking-create'),
    path('booking/list', booking_list, name='booking-list'),
    path('booking/<int:pk>/', booking_detail, name='booking-detail'),
]