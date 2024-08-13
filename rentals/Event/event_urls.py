from django .urls import path
from .event_views import event_create, event_list, event_detail


urlpatterns = [
    path('events/store', event_create, name='event-create'),
    path('events/list', event_list, name='event-list'),
    path('events/<int:pk>/', event_detail, name='event-detail'),
]