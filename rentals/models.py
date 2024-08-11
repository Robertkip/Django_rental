# myapp/models.py
from django.db.models import JSONField
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from rest_framework.pagination import PageNumberPagination

class LargeResultsSetPagination(PageNumberPagination):
    page_size = 2  # Set the default page size
    page_size_query_param = 'page_size'  # Allow clients to set page size
    max_page_size = 100  # Set maximum page size

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

#User model
class User(AbstractBaseUser, PermissionsMixin):
    role_choices = (
        ('Admin', 'Admin'),
        ('Attendee', 'Attendee'),
        ('Organizer', 'Organizer'),
    )

    # Optional fields
    username = models.CharField(max_length=100, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15, blank=True, null=True)  # Adjust max_length as needed
    role = models.CharField(max_length=10, choices=role_choices, default='Attendee')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'name']

    objects = UserManager()

    def __str__(self):
        return f'{self.username} - {self.name} - {self.email} - {self.phone_number} - {self.role}'


#Venue model
class Venue(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    capacity = models.IntegerField()
    facilities = models.TextField()
    charge_rate = models.DecimalField(max_digits=10, decimal_places=2)
    contact_info = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name}, {self.location}, {self.capacity}, {self.charge_rate}'
    
#Event model
class Event(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    venue_id = models.ForeignKey(Venue, on_delete=models.CASCADE)
    organizer_id = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name}, {self.description}, {self.start_date}, {self.end_date}'
    
#Ticket model   
class Ticket(models.Model):
    id = models.AutoField(primary_key=True)
    event_id = models.ForeignKey(Event, on_delete=models.CASCADE)
    ticket_type = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity_available = models.IntegerField()
    quantity_sold = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.event_id}, {self.ticket_type}, {self.price}, {self.quantity_available}, {self.quantity_sold}'


class Transaction(models.Model):
    PAYMENT_METHOD_CHOICES = (
        ('credit_card', 'Credit Card'),
        ('paypal', 'PayPal'),
    )
    
    STATUS_CHOICES = (
        ('completed', 'Completed'),
        ('pending', 'Pending'),
        ('failed', 'Failed'),
    )
    
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    ticket_id = models.ForeignKey(Ticket, on_delete=models.CASCADE)# Ensure 'Ticket' is imported or defined
    transaction_date = models.DateTimeField()
    payment_method = models.CharField(max_length=100, choices=PAYMENT_METHOD_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user_id}, {self.payment_method}, {self.amount}, {self.transaction_date}'


#AccessControl
class AccessControl(models.Model):
    Access_choices = (
        ('full', 'Full'),
        ('restricted', 'Restricted'),
    )
    id = models.AutoField(primary_key=True)
    event_id = models.ForeignKey(Event, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    access_level = models.CharField(max_length=50, choices=Access_choices)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
                return f'User: {self.user_id.name}, Event: {self.event_id.name}, Access Level: {self.access_level}'
    

#Eventfeedback
class EventFeedback(models.Model):
    id = models.AutoField(primary_key=True)
    event_id = models.ForeignKey(Event, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(choices=[(i, str(i)) for i in range(1, 6)])  # Ratings from 1 to 5
    comments = models.TextField(blank=True)  # Optional comments field
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Feedback by {self.user_id.name} for {self.event_id.name}: {self.rating} stars'


#Notification
class Notification(models.Model):
    STATUS_CHOICES = (
        ('read', 'Read'),
        ('unread', 'Unread'),
    )
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='unread')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Notification for {self.user_id.name}: {self.message[:20]}: {self.status}'


#Report
class Report(models.Model):
    REPORT_TYPE_CHOICES = (
        ('sales', 'Sales'),
        ('attendance', 'Attendance'),
        # Add other report types as necessary
    )
    
    id = models.AutoField(primary_key=True)
    event_id = models.ForeignKey(Event, on_delete=models.CASCADE)
    report_type = models.CharField(max_length=50, choices=REPORT_TYPE_CHOICES)
    data = JSONField()  # Use JSONField to store detailed report data
    generated_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def to_dict(self):
        return {
            'id': self.id,
            'event_id': self.event_id.id,
            'report_type': self.report_type,
            'data': self.data,
            'generated_at': self.generated_at,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
        }
    


#Discount
class Discount(models.Model):
    id = models.AutoField(primary_key=True)
    event_id = models.ForeignKey(Event, on_delete=models.CASCADE)
    code = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f'{self.code} {self.description}'


#EventOrganizer
class EventOrganizer(models.Model):
    role_choices = (
        ('Main-Organizer', 'Main-Organizer'),
        ('Co-Organizer', 'Co-Organizer'),
    )
    id = models.AutoField(primary_key=True)
    event_id = models.ForeignKey(Event, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=50, choices=role_choices)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user_id.name} - {self.role}'


class Department(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name
    
