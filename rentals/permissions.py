from rest_framework import permissions

from rest_framework.authentication import TokenAuthentication

class BearerTokenAuthentication(TokenAuthentication):
    keyword = 'Bearer'


class IsAdmin(permissions.BasePermission):
    """
    Custom permission to allow access only to admin users.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'Admin'
    
class IsOrganizer(permissions.BasePermission):
    """
    Custom permission to allow access only to organizer users.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'Organizer'
    

class IsAttendee(permissions.BasePermission):
    """
    Custom permission to allow access only to attendee users.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'Attendee'
    

class IsAdminOrOrganizer(permissions.BasePermission):
    """
    Custom permission to allow access only to Admin and Organizer users.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.role == 'Admin' or request.user.role == 'Organizer'
        )
    
class IsOwnerOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True

        return obj.user == request.user