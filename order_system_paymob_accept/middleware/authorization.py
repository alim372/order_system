from rest_framework.permissions import BasePermission


class user(BasePermission):
    """
    Allows access for editor users.
    """
    def has_permission(self, request, view):
        if request.user.is_anonymous == True:
            return False
        return request.user and request.user.type == 'user'


class administrator(BasePermission):
    """
    Allows access for administrator users.
    """

    def has_permission(self, request, view):
        if request.user.is_anonymous == True:
            return False
        return request.user and request.user.type == 'administrator'

class viewer(BasePermission):
    """
    Allows access for viewer users.
    """

    def has_permission(self, request, view):
        if request.user.is_anonymous == True:
            return False
        return request.user and request.user.type == 'viewer'
