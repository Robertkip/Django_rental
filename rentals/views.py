# rentals/views.py
import os
import json
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from django.contrib.auth import login, logout
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from .models import User, Venue, Event, Ticket, Transaction, AccessControl, EventFeedback, Notification, Report, Discount, EventOrganizer, LargeResultsSetPagination, Department, Country, Activitylogs
from .serializers import UserSerializer, VenueSerializer, EventSerializer, TicketSerializer, TransactionSerializer, AccessControlSerializer, EventFeedbackSerializer, NotificationSerializer, ReportSerializer, DiscountSerializer, EventOrganizerSerializer, DepartmentSerializer, CountrySerializer, ActivitylogsSerializer
from django.core.exceptions import ObjectDoesNotExist
from .permissions import IsAdmin, IsOrganizer, IsAttendee, IsAdminOrOrganizer, IsOwnerOnly


@api_view(['POST'])
def register_user(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
def user_login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({'error': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)

    user = None
    try:
        if '@' in username:
            # Assuming the username is an email address
            user = User.objects.get(username=username)
            print(user)
            # raise ValueError("Invalid username format")
        user = UserSerializer.fields.__get__(username=username)
    except User.DoesNotExist:
        user = authenticate(username=username, password=password)
    if user:
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_logout(request):
    if request.method == 'POST':
        try:
            # Delete the user's token to logout
            request.user.auth_token.delete()
            return Response({'message': 'Successfully logged out.'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
@api_view(['GET', 'POST'])
@permission_classes([IsAdmin])
def user_list(request):

    if request.method == 'GET':
        users = User.objects.all()
        paginator = LargeResultsSetPagination()
        paginated_users = paginator.paginate_queryset(users, request)
        serializer = UserSerializer(paginated_users, many=True)
        return paginator.get_paginated_response(serializer.data)

    # Handle POST request (if needed)

@api_view(['POST'])
def user_create(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    # elif request.method == 'POST':
        # serializer = UserSerializer(data=request.data)
        # if serializer.is_valid():
        #     serializer.save()
        #     return Response(serializer.data, status=status.HTTP_201_CREATED)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsOwnerOnly])
def user_detail(request, pk):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


#Venue
@api_view(['GET', 'POST'])
# @permission_classes([IsOwnerOnly])
def venue_list(request):
    if request.method == 'GET':
        venues = Venue.objects.all()
        paginator = LargeResultsSetPagination()
        paginated_venues = paginator.paginate_queryset(venues, request)
        serializer = VenueSerializer(paginated_venues, many=True)
        return paginator.get_paginated_response(serializer.data)

@api_view(['POST'])
def venue_create(request):
    if request.method == 'POST':
        serializer = VenueSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
# @permission_classes([IsOwnerOnly])
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
    

# Event Views
@api_view(['GET', 'POST'])
# @permission_classes([IsAdminOrOrganizer])
def event_list(request):
    if request.method == 'GET':
        if 'all' in request.query_params and request.query_params['all'] == '1':
            # Return all transactions as an array of objects without pagination
            events = Event.objects.all()
            serializer = EventSerializer(events, many=True)
            return Response(serializer.data)

        events = Event.objects.all()
        paginator = LargeResultsSetPagination()
        paginated_events = paginator.paginate_queryset(events, request)
        serializer = EventSerializer(paginated_events, many=True)
        return paginator.get_paginated_response(serializer.data)
    
@api_view(['POST'])
def event_create(request):
    if request.method == 'POST':
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def event_detail(request, pk):
    try:
        event = Event.objects.get(pk=pk)
    except Event.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = EventSerializer(event)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = EventSerializer(event, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


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
    

#Transaction view
@api_view(['GET'])
# @permission_classes([IsAdmin])
def transaction_list(request):
    if request.method == 'GET':
        if 'all' in request.query_params and request.query_params['all'] == '1':
            # Return all transactions as an array of objects without pagination
            transactions = Transaction.objects.all()
            serializer = TransactionSerializer(transactions, many=True)
            return Response(serializer.data)
        else:
            # Return paginated transactions
            transactions = Transaction.objects.all()
            paginator = LargeResultsSetPagination()
            paginated_transactions = paginator.paginate_queryset(transactions, request)
            serializer = TransactionSerializer(paginated_transactions, many=True)
            return paginator.get_paginated_response(serializer.data)


@api_view(['POST'])
def transaction_create(request):
    if request.method == 'POST':
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET', 'PUT', 'DELETE'])
def transaction_detail(request, pk):
    try:
        transaction = Transaction.objects.get(pk=pk)
    except Transaction.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = TransactionSerializer(transaction)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = TransactionSerializer(transaction, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        transaction.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

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
    

#Eventfeedback
@api_view(['GET', 'POST'])
def eventfeedback_list(request):
    if request.method == 'GET':
        if 'all' in request.query_params and request.query_params['all'] == '1':
            # Return all transactions as an array of objects without pagination
            eventfeedbacks = EventFeedback.objects.all()
            serializer = EventFeedbackSerializer(eventfeedbacks, many=True)
            return Response(serializer.data)
        else:
            eventfeedbacks = EventFeedback.objects.all()
            serializer = EventFeedbackSerializer(eventfeedbacks, many=True)
            return Response(serializer.data)

@api_view(['POST'])
def eventfeedback_create(request):
    if request.method == 'POST':
        serializer = EventFeedbackSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET', 'PUT', 'DELETE'])
def eventfeedback_detail(request, pk):
    try:
        eventfeedback = EventFeedback.objects.get(pk=pk)
    except EventFeedback.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = EventFeedbackSerializer(eventfeedback)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = EventFeedbackSerializer(eventfeedback, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        eventfeedback.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

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
    

#Report
@api_view(['GET'])
def report_list(request):
    if request.method == 'GET':
        if 'all' in request.query_params and request.query_params['all'] == '1':
            # Return all transactions as an array of objects without pagination
            reports = Report.objects.all()
            serializer = ReportSerializer(reports, many=True)
            return Response(serializer.data)
        else:
            reports = Report.objects.all()
            serializer = ReportSerializer(reports, many=True)
            return Response(serializer.data)

@api_view(['POST'])
def report_create(request):
    if request.method == 'POST':
        serializer = ReportSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET', 'PUT', 'DELETE'])
def report_detail(request, pk):
    try:
        report = Report.objects.get(pk=pk)
    except Report.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ReportSerializer(report)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ReportSerializer(report, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        report.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


#Discount
@api_view(['GET'])
def discount_list(request):
    if request.method == 'GET':
        discounts = Discount.objects.all()
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
    

#EventOrganizer
@api_view(['GET'])
def eventorganizer_list(request):
    if request.method == 'GET':
        eventorganizers = EventOrganizer.objects.all()
        serializer = EventOrganizerSerializer(eventorganizers, many=True)
        return Response(serializer.data)
    
@api_view(['POST'])
def eventorganizer_create(request):
    if request.method == 'POST':
        serializer = EventOrganizerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def eventorganizer_detail(request, pk):
    try:
        eventorganizer = EventOrganizer.objects.get(pk=pk)
    except EventOrganizer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = EventOrganizerSerializer(eventorganizer)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = EventOrganizerSerializer(eventorganizer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        eventorganizer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

# from .models import User
# from .serializers import RecordsSerializer

# class RecordsView(generics.ListAPIView):
    # queryset = Billing.objects.all()
    # serializer_class = BillingRecordsSerializer
#     pagination_class = LargeResultsSetPagination


#Departments
@api_view(['GET'])
def department_list(request):
    if request.method == 'GET':
        departments = Department.objects.all()
        serializer = DepartmentSerializer(departments, many=True)
        return Response(serializer.data)

@api_view(['POST'])
def department_create(request):
    if request.method == 'POST':
        serializer = DepartmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET', 'PUT', 'DELETE'])
def department_detail(request, pk):
    try:
        department = Department.objects.get(pk=pk)
    except Department.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = DepartmentSerializer(department)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = DepartmentSerializer(department, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        department.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

#country

@api_view(['GET'])
def country_list(request):
    if request.method == 'GET':
        countries = Country.objects.all()
        serializer = CountrySerializer(countries, many=True)
        return Response(serializer.data)
    
@api_view(['POST'])
def country_create(request):
    if request.method == 'POST':
        serializer = CountrySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET', 'PUT', 'DELETE'])
def country_detail(request, pk):
    try:
        country = Country.objects.get(pk=pk)
    except Country.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CountrySerializer(country)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = CountrySerializer(country, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        country.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

#Activitylogs
@api_view(['GET'])
def activitylogs_list(request):
    if request.method == 'GET':
        activitylog = Activitylogs.objects.all()
        serializer = ActivitylogsSerializer(activitylog, many=True)
        return Response(serializer.data)


@api_view(['POST'])
def activitylogs_create(request):
    if request.method == 'POST':
        serializer = ActivitylogsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# View to handle GET, PUT, and DELETE requests for individual activity logs
@api_view(['GET', 'PUT', 'DELETE'])
def activitylogs_detail(request, pk):
    try:
        activitylog = Activitylogs.objects.get(pk=pk)
    except Activitylogs.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ActivitylogsSerializer(activitylog)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ActivitylogsSerializer(activitylog, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        activitylog.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def read_json(
request):
    if request.method == 'GET':
        # Specify the directory containing your JSON files
        json_dir = os.path.join(os.getcwd(), 'permissions', 'modules')

        # List all JSON files in the directory and remove the .json extension
        json_files = [os.path.splitext(f)[0] for f in os.listdir(json_dir) if f.endswith('.json')]
        
        # Return the list of JSON filenames without the extension in the response
        return Response({"modules": json_files})
    
def extract_permissions(children_dict, parent_key=""):
    permissions = [parent_key] if parent_key else []
    for key, value in children_dict.items():
        current_key = f"{parent_key}.{value['main']}" if parent_key else value['main']
        permissions.append(current_key)
        if "children" in value:
            permissions.extend(extract_permissions(value["children"], current_key))
    return permissions

@api_view(['GET'])
def single_json(request, module):
    if request.method == 'GET':
        # Specify the directory containing your JSON files
        json_dir = os.path.join(os.getcwd(), 'permissions', 'modules')
        
        # Build the full path to the JSON file with the provided module name
        json_path = os.path.join(json_dir, f"{module}.json")
        
        # Check if the file exists
        if os.path.exists(json_path):
            # Read the JSON file
            with open(json_path, 'r') as json_file:
                json_content = json.load(json_file)
            
            # Extract the permissions
            children = json_content.get('children', {})
            permissions = extract_permissions(children, json_content.get('main', module))
            
            # Prepare the response
            response = {
                "module": json_content.get("main", module),
                "permissions": permissions
            }
            
            # Return the response
            return Response(response, status=status.HTTP_200_OK)
        else:
            return Response({"error": "File not found"}, status=status.HTTP_404_NOT_FOUND)
