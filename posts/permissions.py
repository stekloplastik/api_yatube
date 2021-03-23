from rest_framework.permissions import (BasePermission, IsAuthenticated,
                                        SAFE_METHODS)


class IsAuthorOrReadOnly(BasePermission):
    """Проверяем владельца и безопасность метода"""
    def has_object_permission(self, request, view, obj):
        return request.user == obj.author or request.method in SAFE_METHODS
