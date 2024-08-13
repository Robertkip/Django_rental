from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from django.contrib.auth import login, logout
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from ..models import Discount
from ..serializers import DiscountSerializer


#Discount
@api_view(['GET'])
def discount_list(request):
    if request.method == 'GET':
        if 'all' in request.query_params and request.query_params['all'] == '1':
            # Return all transactions as an array of objects without pagination
            discounts = Discount.objects.all()
            serializer = DiscountSerializer(discounts, many=True)
            return Response(serializer.data)
        else:
            discounts = Discount.objects.all()
            serializer = DiscountSerializer(discounts, many=True)
            return Response(serializer.data)


@api_view(['GET'])
def discount_by_event(request, event_id):
    if request.method == 'GET':
        discounts = Discount.objects.filter(event_id=event_id)
        serializer = DiscountSerializer(discounts, many=True)
        return Response(serializer.data)

@api_view(['POST'])
def discount_create(request):
    if request.method == 'POST':
        serializer = DiscountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def discount_detail(request, pk):
    try:
        discount = Discount.objects.get(pk=pk)
    except Discount.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = DiscountSerializer(discount)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = DiscountSerializer(discount, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        discount.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    