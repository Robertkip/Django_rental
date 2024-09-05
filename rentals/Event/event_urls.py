from django .urls import path
from .event_views import event_create, event_list, event_detail, event_all


urlpatterns = [
    path('events/store', event_create, name='event-create'),
    path('events/list', event_list, name='event-list'),
    path('events/<int:pk>/', event_detail, name='event-detail'),
    path('events/list/all', event_all, name='event-all'),
]
# http://127.0.0.1:8000/api/events/list/all