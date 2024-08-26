# myapp/models.py
from django.db.models import JSONField
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from rest_framework.pagination import PageNumberPagination
from datetime import datetime

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
    username = models.CharField(max_length=100, unique=True, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    state = models.CharField(max_length=100, null=True, blank=True)
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
    def upload_to(instance, filename):
    # Use datetime to construct the file path
        return f'tickven/{datetime.now().year}/{datetime.now().month}/{datetime.now().day}/{filename}'

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    contact_name = models.CharField(max_length=100)
    contact_phone = models.CharField(max_length=15, blank=True, null=True)
    capacity = models.IntegerField()
    description = models.TextField(default=None, blank=True, null=True)
    facilities = models.TextField(null=True, blank=True)
    charge_rate = models.DecimalField(max_digits=10, decimal_places=2)
    state = models.CharField(max_length=100, null=True, blank=True)
    file = models.FileField(upload_to=upload_to, null=True, blank=True)  # Add file field
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name}, {self.location}, {self.capacity}, {self.description}, {self.charge_rate}, {self.contact_name}, {self.file}'
    
#Event model
class Event(models.Model):
    def upload_to(instance, filename):
    # Use datetime to construct the file path
        return f'tickven/{datetime.now().year}/{datetime.now().month}/{datetime.now().day}/{filename}'

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    state = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    venue_id = models.ForeignKey(Venue, on_delete=models.CASCADE)
    organizer_id = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to=upload_to, null=True, blank=True)  # Add file field
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name}, {self.description}, {self.file}, {self.start_date}, {self.end_date}'


#Ticket model   
class Ticket(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    event_id = models.ForeignKey(Event, on_delete=models.CASCADE)
    state = models.CharField(max_length=100, null=True, blank=True)
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
    reference_id = models.CharField(max_length=100)
    state = models.CharField(max_length=100, null=True, blank=True)
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
    state = models.CharField(max_length=100, null=True, blank=True)
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
    state = models.CharField(max_length=100, null=True, blank=True)
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
    state = models.CharField(max_length=100, null=True, blank=True)
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
    state = models.CharField(max_length=100, null=True, blank=True)
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
    state = models.CharField(max_length=100, null=True, blank=True)
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
    state = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user_id.name} - {self.role}'


class Department(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    state = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name
    
class Country(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    descrption = models.TextField()
    state = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name}, {self.descrption}, {self.state}'
    
class Activitylogs(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    state = models.CharField(max_length=100, null=True, blank=True)
    slug = models.CharField(max_length=100)
    log = models.TextField()
    device = models.CharField(max_length=100)
    ip_address = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self) -> str:
        return f'{self.user_id.name} - {self.slug} - {self.log} - {self.device} - {self.ip_address} - {self.created_at} - {self.updated_at}'


class Booking(models.Model):
    id = models.AutoField(primary_key=True)
    event_id = models.ForeignKey(Event, on_delete=models.CASCADE)
    ticket_id = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    remaining_amount = models.DecimalField(max_digits=10, decimal_places=2)
    state = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f'{self.event_id.name}, {self.ticket_id.name}, {self.user_id.name}, {self.name}, {self.email}, {self.phone}, {self.paid_amount}, {self.remaining_amount}, {self.state}, {self.created_at}, {self.updated_at}'

class DepartmentPermission(models.Model):
    id = models.AutoField(primary_key=True)
    permissions = models.CharField(max_length=255)
    department_id = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='permissions')
    module = models.CharField(max_length=255)
    urls = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.department_id} - {self.module} - {self.permissions} - {self.urls} - {self.created_at} - {self.updated_at}'
    

class Payment(models.Model):
    status_choices = (
        ('0', '0'),
        ('1', '1'),
        ('2', '2'),
    )
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    tickets = models.IntegerField(null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, choices=status_choices)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user_id.name} - {self.tickets} - {self.amount} - {self.status} - {self.created_at} - {self.updated_at}'