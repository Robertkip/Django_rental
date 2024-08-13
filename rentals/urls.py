from django.urls import path
from .views import user_logout, user_list, read_json, single_json, user_detail, transaction_create, transaction_list, transaction_detail, eventfeedback_create, eventfeedback_list, eventfeedback_detail, discount_create, discount_list, discount_detail, eventorganizer_create, eventorganizer_list, eventorganizer_detail, activitylogs_create, activitylogs_list, activitylogs_detail

urlpatterns = [
    path('logout/', user_logout, name='logout'),
    path('users/', user_list, name="user_list"),
    path('users/<int:pk>/', user_detail, name="user_detail"),
    path('transactions/store', transaction_create, name='transaction-create'),
    path('transactions/list', transaction_list, name='transaction-list'),
    path('transaction/<int:pk>/', transaction_detail, name='transaction-detail'),
    path('eventfeedback/store', eventfeedback_create, name='eventfeedback-create'),
    path('eventfeedback/list', eventfeedback_list, name='eventfeedback-list'),
    path('eventfeedback/<int:pk>/', eventfeedback_detail, name='eventfeedback-detail'),
    path('discount/store', discount_create, name='discount-create'),
    path('discount/list', discount_list, name='discount-list'),
    path('discount/<int:pk>/', discount_detail, name='discount-detail'),
    path('eventorganizer/store', eventorganizer_create, name='eventorganizer-create'),
    path('eventorganizer/list', eventorganizer_list, name='eventorganizer-list'),
    path('eventorganizer/<int:pk>/', eventorganizer_detail, name='eventorganizer-detail'),
    path('activitylog/store', activitylogs_create, name='activitylogs-create'),
    path('activitylog/list', activitylogs_list, name='activitylogs-list'),
    path('activitylog/<int:pk>/', activitylogs_detail, name='activitylogs-detail'),
    path('read_json', read_json, name='read_json'),
    path('single_json/<str:module>', single_json, name='single_json'),
]