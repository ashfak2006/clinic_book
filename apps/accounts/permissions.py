from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj == request.user

class IsDoctor(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.user_role == 'doctor' and request.user.is_active
class IsReceptionist(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.user_role == 'receptionist' and request.user.is_active
class IsPatient(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.user_role == 'patient' and request.user.is_active
class IsClinicAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.user_role == 'clinic_admin' and request.user.is_active

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.user_role == 'admin'