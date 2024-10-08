from rest_framework.decorators import api_view
from rest_framework.response import Response
from rentals.serializers import UserSerializer
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.decorators import authentication_classes, permission_classes
from rentals.models import User

@api_view(['POST'])
def login(request):
    user = get_object_or_404(User, username=request.data['username'])
    print("uSER OBTAINED")
    if not user.check_password(request.data['password']):
        print("PASSWORD INCORRECT")
        return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
    print("Token generation")
    token, created = Token.objects.get_or_create(user=user)
    print("Token generated")
    serializer = UserSerializer(instance=user)
    print("Serializer data")
    return Response({"token": token.key, "User": serializer.data})


@api_view(['POST'])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user = User.objects.get(username=request.data['username'])
        user.set_password(request.data['password'])
        user.save()
        token = Token.objects.create(user=user)
        return Response({'token': token.key, "user": serializer.data})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def test_token(request):
    return Response("User is authenticated {}".format(request.user.email))