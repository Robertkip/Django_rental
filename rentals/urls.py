from django.urls import path
from .views import user_logout, user_list,read_json, single_json, user_detail, venue_list, venue_detail, venue_create, event_list, event_create, event_detail, ticket_create, ticket_list, ticket_detail, transaction_create, transaction_list, transaction_detail, accesscontrol_create, accesscontrol_list, accesscontrol_detail, eventfeedback_create, eventfeedback_list, eventfeedback_detail, report_create, report_list, report_detail, discount_create, discount_list, discount_detail, eventorganizer_create, eventorganizer_list, eventorganizer_detail, department_create, department_list, department_detail, country_create, country_list, country_detail, activitylogs_create, activitylogs_list, activitylogs_detail, booking_create, booking_list, booking_detail, department_permission_create, department_permission_list, department_permission_detail


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
    path('transactions/store', transaction_create, name='transaction-create'),
    path('transactions/list', transaction_list, name='transaction-list'),
    path('transaction/<int:pk>/', transaction_detail, name='transaction-detail'),
    path('access/store', accesscontrol_create, name='accesscontrol-create'),
    path('access/list', accesscontrol_list, name='accesscontrol-list'),
    path('access/<int:pk>/', accesscontrol_detail, name='accesscontrol-detail'),
    path('eventfeedback/store', eventfeedback_create, name='eventfeedback-create'),
    path('eventfeedback/list', eventfeedback_list, name='eventfeedback-list'),
    path('eventfeedback/<int:pk>/', eventfeedback_detail, name='eventfeedback-detail'),
<<<<<<< HEAD
    path('report/store', report_create, name='report-create'),
    path('report/list', report_list, name='report-list'),
    path('report/<int:pk>/', report_detail, name='report-detail'),
    path('discount/store', discount_create, name='discount-create'),
    path('discount/list', discount_list, name='discount-list'),
    path('discount/<int:pk>/', discount_detail, name='discount-detail'),
    
    path('eventorganizer/store', eventorganizer_list, name='eventorganizer-list'),
    path('eventorganizer/list/<int:pk>/', eventorganizer_detail, name='eventorganizer-detail'),
    path('department/store', department_create, name='department-create'),
    path('department/list', department_list, name='department-list'),
    path('department/<int:pk>/', department_detail, name='department-detail'),
    path('country/store', country_create, name='country-create'),
    path('country/list', country_list, name='country-list'),
    path('country/<int:pk>/', country_detail, name='country-detail'),
    path('activitylog/store', activitylogs_create, name='activitylogs-create'),
    path('activitylog/list', activitylogs_list, name='activitylogs-list'),
    path('activitylog/<int:pk>/', activitylogs_detail, name='activitylogs-detail'),
    path('booking/store', booking_create, name='booking-create'),
    path('booking/list', booking_list, name='booking-list'),
    path('booking/<int:pk>/', booking_detail, name='booking-detail'),
    path('department_permission/store', department_permission_create, name='department_permission-create'),
    path('department_permission/list', department_permission_list, name='department_permission-list'),
    path('department_permission/<int:pk>/', department_permission_detail, name='department_permission-detail'),
    
=======
    path('reports/store', report_create, name='report-create'),
    path('reports/list', report_list, name='report-list'),
    path('reports/<int:pk>/', report_detail, name='report-detail'),
    path('discounts/store', discount_create, name='discount-create'),
    path('discounts/list', discount_list, name='discount-list'),
    path('discounts/<int:pk>/', discount_detail, name='discount-detail'),

    path('eventorganizers/store', eventorganizer_list, name='eventorganizer-list'),
    path('eventorganizers/list/<int:pk>/', eventorganizer_detail, name='eventorganizer-detail'),
    path('departments/store', department_create, name='department-create'),
    path('departments/list', department_list, name='department-list'),
    path('departments/<int:pk>/', department_detail, name='department-detail'),
    path('countries/store', country_create, name='country-create'),
    path('countries/list', country_list, name='country-list'),
    path('countries/<int:pk>/', country_detail, name='country-detail'),
    path('activitylogs/store', activitylogs_create, name='activitylogs-create'),
    path('activitylogs/list', activitylogs_list, name='activitylogs-list'),
    path('activitylogs/<int:pk>/', activitylogs_detail, name='activitylogs-detail'),
>>>>>>> c8f831b59b29b4fed9fb1aca4abbc86f11d16e9c
    path('read_json', read_json, name='read_json'),
    path('single_json/<str:module>', single_json, name='single_json')
]