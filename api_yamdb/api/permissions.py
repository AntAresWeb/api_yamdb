from rest_framework import permissions


class IsAuthorModeratorAdminOrReadOnly(permissions.BasePermission):
    """Разрешение без токена, изменения для автора,
    модератора или администратора."""
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user
                or request.user.is_moderator
                or request.user.is_admin
                )
