from rest_framework.permissions import BasePermission

class IsOwner(BasePermission):
    message = 'you are not the owner of this expense'

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user