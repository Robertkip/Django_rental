from django.contrib import admin
from .models import User, Venue, Event, Ticket, Transaction, AccessControl, EventFeedback, Notification, Report, Discount, EventOrganizer
# Register your models here.

admin.site.register(User)
admin.site.register(Venue)
admin.site.register(Event)
admin.site.register(Ticket)
admin.site.register(Transaction)
admin.site.register(AccessControl)
admin.site.register(EventFeedback)
admin.site.register(Notification)
admin.site.register(Report)
admin.site.register(Discount)
admin.site.register(EventOrganizer)
