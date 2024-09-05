from django.urls import path
from .views import user_logout, listAdmin, listUsers, get_user_by_id, user_detail, transaction_create, transaction_list, transaction_detail, eventorganizer_create, eventorganizer_list, eventorganizer_detail, activitylogs_create, activitylogs_list, activitylogs_detail

urlpatterns = [
    path('logout/', user_logout, name='logout'),
    path('users/list/admin', listAdmin, name="listAdmin"),
    path('users/users', listUsers, name="listUsers"),
    path('users/<int:pk>/', user_detail, name="user_detail"),
    path('users/get/any/<int:pk>/', get_user_by_id, name='get-user-by-id'),
    path('transactions/store', transaction_create, name='transaction-create'),
    path('transactions/list', transaction_list, name='transaction-list'),
    path('transaction/<int:pk>/', transaction_detail, name='transaction-detail'),
    path('eventorganizer/store', eventorganizer_create, name='eventorganizer-create'),
    path('eventorganizer/list', eventorganizer_list, name='eventorganizer-list'),
    path('eventorganizer/<int:pk>/', eventorganizer_detail, name='eventorganizer-detail'),
    path('activitylog/store', activitylogs_create, name='activitylogs-create'),
    path('activitylog/list', activitylogs_list, name='activitylogs-list'),
    path('activitylog/<int:pk>/', activitylogs_detail, name='activitylogs-detail'),
]