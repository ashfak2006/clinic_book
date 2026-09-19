from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj == request.user


class RolePermission(permissions.BasePermission):
    allowed_role = None

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.is_active
            and getattr(request.user, "user_role", None) == self.allowed_role
        )


class IsDoctor(RolePermission):
    allowed_role = "doctor"


class IsReceptionist(RolePermission):
    allowed_role = "receptionist"


class IsPatient(RolePermission):
    allowed_role = "patient"


class IsClinicAdmin(RolePermission):
    allowed_role = "clinic_admin"


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and (
                getattr(request.user, "user_role", None) == "admin"
                or request.user.is_staff
                or request.user.is_superuser
            )
        )
class IsClinicAdminOrReceptionist(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.user_role == "clinic_admin" or request.user.user_role == "receptionist"
        )