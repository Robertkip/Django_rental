from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes

from ..models import Notification
from ..serializers import NotificationSerializer


#Notification
@api_view(['GET'])
def notification_list(request):
    if request.method == 'GET':
        if 'all' in request.query_params and request.query_params['all'] == '1':
            # Return all transactions as an array of objects without pagination
            notifications = Notification.objects.all()
            serializer = NotificationSerializer(notifications, many=True)
            return Response(serializer.data)
        else:
            notifications = Notification.objects.all()
            serializer = NotificationSerializer(notifications, many=True)
            return Response(serializer.data)

@api_view(['POST'])
def notification_create(request):
    if request.method == 'POST':
        serializer = NotificationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET', 'PUT', 'DELETE'])
def notification_detail(request, pk):
    try:
        notification = Notification.objects.get(pk=pk)
    except Notification.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = NotificationSerializer(notification)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = NotificationSerializer(notification, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        notification.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)