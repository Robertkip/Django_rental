from django.urls import path
from .paypal_views import payment_checkout, payment_failed, create_payment, execute_payment

urlpatterns = [
    path('checkout/', payment_checkout, name='checkout_payment'),
    path('create_payment/', create_payment, name='create_payment'),
    path('execute_payment/', execute_payment, name='execute_payment'),
    path('payment_failed', payment_failed, name='payment_failed')
]