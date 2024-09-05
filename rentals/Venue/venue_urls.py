from django.urls import path
from .venue_views import venue_create, venue_list, venue_detail, venue_all, venue_list_all

urlpatterns = [
    path('venues/store', venue_create, name='venue-create'),
    path('venues/list', venue_list, name='venue-list'),
    path('venues/<int:pk>/', venue_detail, name='venue-detail'),
    path('config/venues/all', venue_all, name='venue-all'),
    path('venues/list/all', venue_list_all, name='venue-list-all'),
]