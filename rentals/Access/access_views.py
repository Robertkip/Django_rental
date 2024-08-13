from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from django.contrib.auth import login, logout
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status

from ..models import AccessControl, LargeResultsSetPagination
from ..serializers import AccessControlSerializer
from ..permissions import IsAdminOrOrganizer

#Access

#AccessControl View
@api_view(['GET'])
@permission_classes([IsAdminOrOrganizer])
def accesscontrol_list(request):
    if request.method == 'GET':
        if 'all' in request.query_params and request.query_params['all'] == '1':
            # Return all transactions as an array of objects without pagination
            accesscontrols = AccessControl.objects.all()
            serializer = AccessControlSerializer(accesscontrols, many=True)
            return Response(serializer.data)
        else:
            accesscontrols = AccessControl.objects.all()
            serializer = AccessControlSerializer(accesscontrols, many=True)
            return Response(serializer.data)
        
@api_view(['POST'])
def accesscontrol_create(request):
    if request.method == 'POST':
        serializer = AccessControlSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET', 'PUT', 'DELETE'])
def accesscontrol_detail(request, pk):
    try:
        accesscontrol = AccessControl.objects.get(pk=pk)
    except AccessControl.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = AccessControlSerializer(accesscontrol)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = AccessControlSerializer(accesscontrol, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        accesscontrol.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    