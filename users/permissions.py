# users/permissions.py
from rest_framework import permissions

class HasEntidad(permissions.BasePermission):
    message = 'El usuario debe tener una entidad asignada.'

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            hasattr(request.user, 'entidad') and
            request.user.entidad is not None
        )