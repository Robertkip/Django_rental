from django.urls import path
from .payment_views import payment_create, payment_detail, payment_list, update_payment_status

urlpatterns = [
    path('payment/store', payment_create, name='payment-create'),
    path('payment/list', payment_list, name='payment-list'),
    path('payment/<int:pk>/', payment_detail, name='payment-detail'),
    path('update_payment_status/<int:payment_id>/', update_payment_status, name='update_payment_status'),
]