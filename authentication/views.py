from rest_framework.decorators import api_view
from rest_framework.response import Response
from rentals.serializers import UserSerializer
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from authentication.permission import BearerTokenAuthentication
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.decorators import authentication_classes, permission_classes
from rentals.models import User

@api_view(['POST'])
def login(request):
    # Ensure 'email' and 'password' are provided in the request
    email = request.data.get('email')
    password = request.data.get('password')

    if not email or not password:
        return Response({"detail": "Email and password are required."}, status=status.HTTP_400_BAD_REQUEST)

    user = get_object_or_404(User, email=email)
    print("User obtained")

    if not user.check_password(password):
        print("Password incorrect")
        return Response({"detail": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)

    print("Token generation")
    token, created = Token.objects.get_or_create(user=user)
    print("Token generated")

    serializer = UserSerializer(instance=user)
    print("Serializer data")

    return Response({"token": token.key, "user": serializer.data})

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
@authentication_classes([SessionAuthentication, BearerTokenAuthentication])
@permission_classes([IsAuthenticated])
def test_token(request):
    token, _ = Token.objects.get_or_create(user=request.user)
    user = request.user
    user_data = {
        "username": user.username,
        'email': user.email,
        "role": user.role
    }
    return Response(user_data)

