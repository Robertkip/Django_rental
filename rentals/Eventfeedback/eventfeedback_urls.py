from django.urls import path
from .eventfeedback_views import eventfeedback_create, eventfeedback_list, eventfeedback_detail, eventfeedback_by_event, create_eventfeedback_by_event


urlpatterns = [
    path('eventfeedback/store', eventfeedback_create, name='eventfeedback-create'),
    path('eventfeedback/list', eventfeedback_list, name='eventfeedback-list'),
    path('eventfeedback/<int:pk>/', eventfeedback_detail, name='eventfeedback-detail'),
    path('eventfeedback/store/<int:event_id>/', create_eventfeedback_by_event, name='create-eventfeedback-by-event'),
    path('eventfeedback/store/<int:event_id>/', eventfeedback_by_event, name='eventfeedback-by-event'),
]