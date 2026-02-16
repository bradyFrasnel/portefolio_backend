from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Permission personnalisée :
    - Les utilisateurs administrateurs peuvent effectuer toutes les opérations
    - Les autres utilisateurs ne peuvent que lire (GET, HEAD, OPTIONS)
    """
    
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff

class IsAuthenticatedOrReadOnly(permissions.BasePermission):
    """
    Permission personnalisée :
    - Les utilisateurs authentifiés peuvent effectuer toutes les opérations
    - Les utilisateurs non authentifiés ne peuvent que lire
    """
    
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated
