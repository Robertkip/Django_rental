from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from django.contrib.auth import login, logout
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from ..models import DepartmentPermission
from ..serializers import DepartmentPermissionSerializer

#DepartmentPermission
@api_view(['GET'])
def department_permission_list(request):
    if request.method == 'GET':
        if 'all' in request.query_params and request.query_params['all'] == '1':
            # Return all transactions as an array of objects without pagination
            department_permission = DepartmentPermission.objects.all()
            serializer = DepartmentPermissionSerializer(department_permission, many=True)
            return Response(serializer.data)
        else:
            department_permission = DepartmentPermission.objects.all()
            serializer = DepartmentPermissionSerializer(department_permission, many=True)
            return Response(serializer.data)
        

@api_view(['POST'])
def department_permission_create(request):
    if request.method == 'POST':
        serializer = DepartmentPermissionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET', 'PUT', 'DELETE'])
def department_permission_detail(request, pk):
    try:
        department_permission = DepartmentPermission.objects.get(pk=pk)
    except DepartmentPermission.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = DepartmentPermissionSerializer(department_permission)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = DepartmentPermissionSerializer(department_permission, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        department_permission.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)