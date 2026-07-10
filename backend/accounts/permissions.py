from rest_framework.permissions import BasePermission


class IsManager(BasePermission):
    """Allows access only to users with the manager role."""

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_manager)


class IsOwnerOrManager(BasePermission):
    """Object-level: owners can access their own objects; managers can access any."""

    def has_object_permission(self, request, view, obj):
        if request.user.is_manager:
            return True
        owner = getattr(obj, "user", None) or getattr(obj, "owner", None)
        return owner == request.user
