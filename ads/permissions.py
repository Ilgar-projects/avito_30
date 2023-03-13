from rest_framework.permissions import BasePermission

from users.models import UserRoles


class IsSelectionOwner(BasePermission):
    message = "Вы не имеете право изменять эту подборку"

    def has_object_permission(self, request, view, selection):
        if request.user == selection.owner:
            return True
        return False


class IsAdAuthorOrStaff(BasePermission):
    message = "Вы не имеете право изменять это объявление"

    def has_object_permission(self, request, view, ad):
        if request.user == ad.author or request.user.role != UserRoles.MEMBER:
            return True
        return False