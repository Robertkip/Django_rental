from django.urls import path
from .views import user_logout, user_list, user_detail, venue_list, venue_detail, event_list, event_detail, ticket_list, ticket_detail, transaction_list, transaction_detail, accesscontrol_list, accesscontrol_detail, eventfeedback_list, eventfeedback_detail, report_list, report_detail, discount_list, discount_detail, eventorganizer_list, eventorganizer_detail, department_list, department_detail

urlpatterns = [
    path('logout/', user_logout, name='logout'),
    path('users/', user_list, name="user_list"),
    path('users/<int:pk>/', user_detail, name="user_detail"),
    path('venues/', venue_list, name='venue-list'),
    path('venues/<int:pk>/', venue_detail, name='venue-detail'),
    path('events/', event_list, name='event-list'),
    path('events/<int:pk>/', event_detail, name='event-detail'),
    path('tickets/', ticket_list, name='ticket-list'),
    path('tickets/<int:pk>/', ticket_detail, name='ticket-detail'),
    path('transaction/', transaction_list, name='transaction-list'),
    path('transaction/<int:pk>/', transaction_detail, name='transaction-detail'),
    path('access/', accesscontrol_list, name='accesscontrol-list'),
    path('access/<int:pk>/', accesscontrol_detail, name='accesscontrol-detail'),
    path('eventfeedback/', eventfeedback_list, name='eventfeedback-list'),
    path('eventfeedback/<int:pk>/', eventfeedback_detail, name='eventfeedback-detail'),
    path('report/', report_list, name='report-list'),
    path('report/<int:pk>/', report_detail, name='report-detail'),
    path('discount/', discount_list, name='discount-list'),
    path('discount/<int:pk>/', discount_detail, name='discount-detail'),
    path('eventorganizer/', eventorganizer_list, name='eventorganizer-list'),
    path('eventorganizer/<int:pk>/', eventorganizer_detail, name='eventorganizer-detail'),
    path('department/', department_list, name='department-list'),
    path('department/<int:pk>/', department_detail, name='department-detail'),
]