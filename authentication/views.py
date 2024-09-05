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
    user = get_object_or_404(User, email=request.data['email'])
    print("uSER OBTAINED")
    if not user.check_password(request.data['password']):
        print("PASSWORD INCORRECT")
        return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
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
    
    # Base user data
    user_data = {
        "id": user.id,
        "name": "Super Admin" if user.role == 'admin' else user.username,  # Name based on role
        "email": user.email,
        "email_verified_at": None,  # Assuming email verification is not implemented
        "phone": None,  # Assuming no phone number is stored
        "phone_verified_at": None,  # Assuming phone verification is not implemented
        "role": user.role,
        "department_id": 1,  # Assuming a default department_id
        "care_taker_id": None,  # Assuming no caretaker associated
        "permissions": None,  # Placeholder, will be set based on role
        "menuCounts": {
            "properties": 0,
            "tenants": 0,
            "caretakers": 0
        }
    }
    
    # Set permissions based on role
    if user.role == 'admin':
        user_data["permissions"] = '[\"admin\",\"admin.activity-logs\",\"admin.activity-logs.list\",\"admin.dashboard-stats\",\"config\",\"config.counties\",\"config.counties.store\",\"config.counties.list\",\"config.services\",\"config.services.store\",\"config.services.list\",\"config.units\",\"config.units.store\",\"config.units.list\",\"config.utilities\",\"config.utilities.store\",\"config.utilities.list\",\"config.amenities\",\"config.amenities.store\",\"config.amenities.list\",\"config.features\",\"config.features.store\",\"config.features.list\",\"config.tenant-contact-relationship\",\"config.tenant-contact-relationship.store\",\"config.tenant-contact-relationship.list\",\"config.tenant-asset-categories\",\"config.tenant-asset-categories.store\",\"config.tenant-asset-categories.list\",\"config.venues\",\"config.venues.list\",\"config.venues.store\",\"config.countries\",\"config.countries.list\",\"config.countries.store\",\"dashboard\",\"dashboard.stats\",\"events\",\"events.transactions\",\"events.transactions.list\",\"events.transactions.store\",\"events.event-feedbacks\",\"events.event-feedbacks.list\",\"events.event-feedbacks.store\",\"events.discounts\",\"events.discounts.list\",\"events.discounts.store\",\"events.bookings\",\"events.bookings.list\",\"events.bookings.store\",\"events.tickets\",\"events.tickets.list\",\"events.tickets.store\",\"events.list\",\"events.store\",\"logs\",\"logs.admin_activitylogs\",\"permissions\",\"permissions.departments\",\"permissions.departments.add_department\",\"permissions.departments.list_departments\",\"permissions.departments.delete_department\",\"permissions.departments.manage_permissions\",\"users\",\"users.add_user\",\"users.list_users\",\"users.get_any_user\",\"users.update_details\",\"users.reset_password\"]'
    else:
        user_data["permissions"] = '[\"config\",\"config.counties\",\"config.counties.list\",\"config.services\",\"config.services.store\",\"config.services.list\",\"config.units\",\"config.units.list\",\"config.utilities\",\"config.utilities.list\",\"config.amenities\",\"config.amenities.store\",\"config.amenities.list\",\"config.features\",\"config.features.list\",\"config.tenant-contact-relationship\",\"config.tenant-contact-relationship.list\",\"config.tenant-asset-categories\",\"config.tenant-asset-categories.list\",\"config.venues\",\"config.venues.list\",\"config.venues.store\",\"config.countries\",\"config.countries.list\",\"config.countries.store\",\"dashboard\",\"dashboard.stats\",\"events\",\"events.transactions\",\"events.transactions.list\",\"events.transactions.store\",\"events.event-feedbacks\",\"events.event-feedbacks.list\",\"events.event-feedbacks.store\",\"events.discounts\",\"events.discounts.list\",\"events.discounts.store\",\"events.bookings\",\"events.bookings.list\",\"events.bookings.store\",\"events.tickets\",\"events.tickets.list\",\"events.tickets.store\",\"events.list\",\"events.store\",\"users\",\"users.reset_password\"]'
    
    # Return the complete user data
    return Response(user_data)