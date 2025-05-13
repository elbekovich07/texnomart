from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, object):
        user = request.user
        if request.method in permissions.SAFE_METHODS:
            return True
        if user.is_staff and user.is_superuser:
            return True
        else:
            return False
