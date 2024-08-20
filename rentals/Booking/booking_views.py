from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from django.contrib.auth import login, logout
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from ..models import Booking, Event, Ticket
from ..serializers import BookingSerializer, EventSerializer, TicketSerializer


#Booking
@api_view(['GET'])
def booking_list(request):
    if request.method == 'GET':
        if 'all' in request.query_params and request.query_params['all'] == '1':
            # Return all booking as an array of objects without pagination
            booking = Booking.objects.all()
            serializer = BookingSerializer(booking, many=True)
            return Response(serializer.data)
        else:
            booking = Booking.objects.all()
            serializer = BookingSerializer(booking, many=True)
            return Response(serializer.data)
        

# Get booking by Event ID
@api_view(['GET'])
def booking_by_event(request, event_id):
    if request.method == 'GET':
        booking = Booking.objects.filter(event_id=event_id)
        serializer = BookingSerializer(booking, many=True)
        return Response(serializer.data)
        
@api_view(['POST'])
def create_booking_by_event(request, event_id):
    if request.method == 'POST':
        # Add the event_id from the URL to the request data
        request_data = request.data.copy()
        request_data['event_id'] = event_id

        serializer = BookingSerializer(data=request_data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def booking_create(request):
    if request.method == 'POST':
        serializer = BookingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET', 'PUT', 'DELETE'])
def booking_detail(request, pk):
    try:
        booking = Booking.objects.get(pk=pk)
    except Booking.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = BookingSerializer(booking)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = BookingSerializer(booking, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        booking.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)