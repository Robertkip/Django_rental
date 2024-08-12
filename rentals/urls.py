from django.urls import path
from .views import user_logout, user_list, user_detail, venue_list, venue_detail, venue_create, event_list, event_create, event_detail, ticket_create, ticket_list, ticket_detail, transaction_create, transaction_list, transaction_detail, accesscontrol_list, accesscontrol_detail, eventfeedback_list, eventfeedback_detail, report_list, report_detail, discount_list, discount_detail, eventorganizer_list, eventorganizer_detail, department_list, department_detail, country_list, country_detail, activitylogs_list, activitylogs_detail



urlpatterns = [
    path('logout/', user_logout, name='logout'),
    path('users/', user_list, name="user_list"),
    path('users/<int:pk>/', user_detail, name="user_detail"),
    path('venues/store', venue_create, name='venue-create'),
    path('venues/list', venue_list, name='venue-list'),
    path('venues/<int:pk>/', venue_detail, name='venue-detail'),
    path('events/store', event_create, name='event-create'),
    path('events/list', event_list, name='event-list'),
    path('events/<int:pk>/', event_detail, name='event-detail'),
    path('tickets/store', ticket_create, name='ticket-create'),
    path('tickets/list', ticket_list, name='ticket-list'),
    path('tickets/<int:pk>/', ticket_detail, name='ticket-detail'),
    path('transaction/store', transaction_create, name='transaction-create'),
    path('transaction/list', transaction_list, name='transaction-list'),
    path('transaction/<int:pk>/', transaction_detail, name='transaction-detail'),
    path('access/store', accesscontrol_list, name='accesscontrol-list'),
    path('access/list/<int:pk>/', accesscontrol_detail, name='accesscontrol-detail'),
    path('eventfeedback/store', eventfeedback_list, name='eventfeedback-list'),
    path('eventfeedback/list/<int:pk>/', eventfeedback_detail, name='eventfeedback-detail'),
    path('report/store', report_list, name='report-list'),
    path('report/list/<int:pk>/', report_detail, name='report-detail'),
    path('discount/store', discount_list, name='discount-list'),
    path('discount/list/<int:pk>/', discount_detail, name='discount-detail'),
    path('eventorganizer/store', eventorganizer_list, name='eventorganizer-list'),
    path('eventorganizer/list/<int:pk>/', eventorganizer_detail, name='eventorganizer-detail'),
    path('department/store', department_list, name='department-list'),
    path('department/list/<int:pk>/', department_detail, name='department-detail'),
    path('country/store', country_list, name='country-list'),
    path('country/list/<int:pk>/', country_detail, name='country-detail'),
    path('activitylog/store', activitylogs_list, name='activitylogs-list'),
    path('activitylog/list/<int:pk>/', activitylogs_detail, name='activitylogs-detail'),
    
]