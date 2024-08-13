from django.urls import path
from .venue_views import venue_create, venue_list, venue_detail

urlpatterns = [
    path('venues/store', venue_create, name='venue-create'),
    path('venues/list', venue_list, name='venue-list'),
    path('venues/<int:pk>/', venue_detail, name='venue-detail'),
]