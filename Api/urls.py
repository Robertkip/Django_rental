"""Api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('authentication.urls')),
    path('api/', include('rentals.urls')),
    path('api/', include('rentals.Venue.venue_urls')),
    path('api/', include('rentals.Access.access_urls')),
    path('api/', include('rentals.Discount.discount_urls')),
    path('api/', include('rentals.Eventfeedback.eventfeedback_urls')),
    path('api/', include('rentals.Ticket.ticket_urls')),
    path('api/', include('rentals.Notification.notification_urls')),
    path('api/', include('rentals.Country.country_urls')),
    path('api/', include('rentals.Departmentpermission.departmentpermission_urls')),
    path('api/', include('rentals.Department.department_urls')),
    path('api/', include('rentals.Booking.booking_urls')),
    path('api/', include('rentals.Report.report_urls')),
    path('api/', include('rentals.Event.event_urls')),
    path('api/', include('rentals.urls_permisions')),
    path('api/', include('rentals.Read_Json.json_urls')),
]
