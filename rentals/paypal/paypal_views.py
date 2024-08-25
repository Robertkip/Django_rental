from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect


import paypalrestsdk
from django.conf import settings
from django.shortcuts import render, redirect
from django.urls import reverse

paypalrestsdk.configure({
    "mode": "sandbox",  # Change to "live" for production
    "client_id": 'ATVqy_gxh3jcW3IbIkJ57IrFa0CrckaryDRcCwbvJm4rFgS-EEmPK30_ZIOyew0hj0gnaK-1rnwGRJ9Z',
    "client_secret": 'EG9k4t2ERwrsh3YgaxZXYwMfzppgapDX7zjVgHM-2y-HwaH0gPeSXQzf0U3CMaTpUYDMmM1rDHjwNyPX',
})

@csrf_protect
def create_payment(request):
    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal",
        },
        "redirect_urls": {
            "return_url": request.build_absolute_uri(reverse('execute_payment')),
            "cancel_url": request.build_absolute_uri(reverse('payment_failed')),
        },
        "transactions": [
            {
                "amount": {
                    "total": "10.00",  # Total amount in USD
                    "currency": "USD",
                },
                "description": "Payment for Product/Service",
            }
        ],
    })

    if payment.create():
        return redirect(payment.links[1].href)  # Redirect to PayPal for payment
    else:
        return render(request, 'payment_failed.html')
    

@csrf_protect

def execute_payment(request):
    payment_id = request.GET.get('paymentId')
    payer_id = request.GET.get('PayerID')

    payment = paypalrestsdk.Payment.find(payment_id)

    if payment.execute({"payer_id": payer_id}):
        return render(request, 'payment_success.html')
    else:
        return render(request, 'payment_failed.html')
@csrf_protect
def payment_checkout(request):
    return render(request, 'checkout.html')
@csrf_protect
def payment_failed(request):
    return render(request, 'payment_failed.html')