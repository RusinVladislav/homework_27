from rest_framework.permissions import BasePermission

from users.models import UserRoles


class IsSelectionOwner(BasePermission):
    message = "У Вас нет права доступа к этой подборке"

    def has_object_permission(self, request, view, obj):
        if request.User == obj.owner:
            return True
        return False


class IsAdOwnerOrStaff(BasePermission):
    message = "У Вас нет права доступа к этому объявлению"

    def has_object_permission(self, request, view, obj):
        if request.User == obj.author or request.User.role in [UserRoles.ADMIN, UserRoles.MODERATOR]:
            return True
        return False
