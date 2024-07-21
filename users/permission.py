from rest_framework import permissions


class UserPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # whether superAdmin
        if request.user.is_superuser:
            return True
        # if not superAdmin, justify the login user ？= request.user.is_superuser
        return obj.user == request.user


class AddrPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # whether superAdmin
        if request.user.is_superuser:
            return True
        # if not superAdmin, justify the login user ？= request.user.is_superuser
        print("obj::",obj)
        print(obj.user)
        print("request:",request.user)
        return obj.user == request.user
