from django.urls import path
from .discount_views import discount_create, discount_list, discount_detail, discount_by_event

urlpatterns = [
    path('discount/store', discount_create, name='discount-create'),
    path('discount/list', discount_list, name='discount-list'),
    path('discount/<int:pk>/', discount_detail, name='discount-detail'),
    path('discount/store/<int:event_id>/', discount_by_event, name='discount-by-event'),
]