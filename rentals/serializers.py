from rest_framework import serializers
from .models import User, Venue, Event, Ticket, Transaction, AccessControl, EventFeedback, Notification, Report, Discount, EventOrganizer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password', 'phone_number', 'role', 'created_at', 'updated_at']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])  # Hash the password
        user.save()
        return user
    

class VenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venue
        fields = ['id', 'name', 'location', 'capacity', 'facilities', 'charge_rate', 'contact_info', 'created_at', 'updated_at']


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'name', 'description', 'start_date', 'end_date', 'venue_id', 'organizer_id', 'created_at', 'updated_at']


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['id', 'event_id', 'ticket_type', 'price', 'quantity_available', 'quantity_sold', 'created_at', 'updated_at']


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'user_id', 'ticket_id', 'transaction_date', 'payment_method', 'amount', 'status', 'created_at', 'updated_at']


class AccessControlSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccessControl
        fields = ['id', 'event_id', 'user_id', 'access_level', 'created_at', 'updated_at']

class EventFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventFeedback
        fields = ['id', 'event_id', 'user_id', 'rating', 'comments', 'created_at', 'updated_at']

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'user_id', 'message', 'status', 'created_at', 'updated_at']


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ['id', 'event_id', 'report_type', 'data', 'generated_at', 'created_at', 'updated_at']


class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = ['id', 'event_id', 'code', 'description', 'discount_percentage', 'start_date', 'end_date', 'created_at', 'updated_at']

class EventOrganizerSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventOrganizer
        fields = ['id', 'event_id', 'user_id', 'role', 'created_at', 'updated_at']