from rest_framework.permissions import BasePermission
from core.models import AccountMember, Role

class IsAdminUser(BasePermission):
    """Allow only Admins of the account"""
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return AccountMember.objects.filter(user=request.user, role__role_name=Role.ADMIN).exists()

class IsAdminOrReadOnly(BasePermission):
    """Admins can create/update/delete; Normal users can read & update"""
    def has_permission(self, request, view):
        if request.method in ["GET", "PUT", "PATCH"]:
            return request.user.is_authenticated
        return AccountMember.objects.filter(user=request.user, role__role_name=Role.ADMIN).exists()
