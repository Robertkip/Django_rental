from django.urls import path
from .ticket_views import ticket_create, ticket_list, ticket_detail

urlpatterns = [
    path('ticket/store', ticket_create, name='ticket-create'),
    path('ticket/list', ticket_list, name='ticket-list'),
    path('ticket/<int:pk>/', ticket_detail, name='ticket-detail'),
]