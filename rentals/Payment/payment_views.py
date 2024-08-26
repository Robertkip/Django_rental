from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from ..models import Payment
from ..serializers import PaymentSerializer


#Notification
@api_view(['GET'])
def payment_list(request):
    if request.method == 'GET':
        if 'all' in request.query_params and request.query_params['all'] == '1':
            # Return all transactions as an array of objects without pagination
            payments = Payment.objects.all()
            serializer = PaymentSerializer(payments, many=True)
            return Response(serializer.data)
        else:
            payments = Payment.objects.all()
            serializer = PaymentSerializer(payments, many=True)
            return Response(serializer.data)

@api_view(['POST'])
def payment_create(request):
    if request.method == 'POST':
        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET', 'PUT', 'DELETE'])
def payment_detail(request, pk):
    try:
        payment = Payment.objects.get(pk=pk)
    except Payment.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PaymentSerializer(payment)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = PaymentSerializer(payment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        payment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

# update payment status
@api_view(['POST'])
def update_payment_status(request, payment_id):
    try:
        payment = Payment.objects.get(id=payment_id)

        # Ensure the status is currently '0' (Pending)
        if payment.status != '0':
            return Response({'error': 'Payment status can only be updated from 0 (Pending)'}, status=status.HTTP_400_BAD_REQUEST)

        # Get the new status from the request
        new_status = request.data.get('status')

        # Validate the new status
        if new_status not in ['1', '2']:
            return Response({'error': 'Invalid status. Status must be 1 (Completed) or 2 (Failed)'}, status=status.HTTP_400_BAD_REQUEST)

        # Update the payment status
        payment.status = new_status
        payment.save()

        return Response({'status': f'Payment status updated to {new_status}'}, status=status.HTTP_200_OK)
    except Payment.DoesNotExist:
        return Response({'error': 'Payment not found'}, status=status.HTTP_404_NOT_FOUND)