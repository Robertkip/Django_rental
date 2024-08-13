from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from django.contrib.auth import login, logout
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status

from ..models import Ticket, LargeResultsSetPagination
from ..serializers import TicketSerializer
from ..permissions import IsAdminOrOrganizer




#Ticket views
@api_view(['GET'])
# @permission_classes([IsAdminOrOrganizer])
def ticket_list(request):
    if request.method == 'GET':
        if 'all' in request.query_params and request.query_params['all'] == '1':
            # Return all transactions as an array of objects without pagination
            tickets = Ticket.objects.all()
            serializer = TicketSerializer(tickets, many=True)
            return Response(serializer.data)
        else:
            # Return paginated tickets
            tickets = Ticket.objects.all()
            paginator = LargeResultsSetPagination()
            paginated_tickets = paginator.paginate_queryset(tickets, request)
            serializer = TicketSerializer(paginated_tickets, many=True)
            return paginator.get_paginated_response(serializer.data)

@api_view(['POST'])
def ticket_create(request):
    if request.method == 'POST':
        serializer = TicketSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAdminOrOrganizer])
def ticket_detail(request, pk):
    try:
        ticket = Ticket.objects.get(pk=pk)
    except Ticket.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = TicketSerializer(ticket)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = TicketSerializer(ticket, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        ticket.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    