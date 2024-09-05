from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from django.contrib.auth import login, logout
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status

from ..models import Venue, LargeResultsSetPagination
from ..serializers import VenueSerializer
from ..permissions import IsOwnerOnly


#Venue
@api_view(['GET'])
@permission_classes([IsOwnerOnly])
def venue_list(request):
    if request.method == 'GET':
        venues = Venue.objects.all()
        paginator = LargeResultsSetPagination()
        paginated_venues = paginator.paginate_queryset(venues, request)
        serializer = VenueSerializer(paginated_venues, many=True)
        return paginator.get_paginated_response(serializer.data)
    

@api_view(['GET'])
def venue_list_all(request):
    """
    List all venues. If the query parameter 'all=1' is passed, return all venues.
    """
    if request.query_params.get('all') == '1':
        venues = Venue.objects.all()
        serializer = VenueSerializer(venues, many=True)
        return Response(serializer.data)

    # Optional: Return an empty response or handle the case where 'all=1' is not provided.
    return Response({"error": "Query parameter 'all=1' not provided"}, status=400)


@api_view(['POST'])
def venue_create(request):
    if request.method == 'POST':
        serializer = VenueSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsOwnerOnly])
def venue_detail(request, pk):
    try:
        venue = Venue.objects.get(pk=pk)
    except Venue.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = VenueSerializer(venue)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = VenueSerializer(venue, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        venue.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

#venues/list/all
@api_view(['GET'])
def venue_all(request):
    if request.method =='GET':
            venues = Venue.objects.all()
            serializer = VenueSerializer(venues, many=True)
            return Response(serializer.data)