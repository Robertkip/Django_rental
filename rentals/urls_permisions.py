from django.urls import path
from .views_permissions import assignDeparmentPermision

urlpatterns = [
    path('sh-departments/department/permissions/<int:id>/<str:module>', assignDeparmentPermision, name='assignDeparmentPermision'),
]
