from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsUserOrAdmin(BasePermission):
    """
    Custom permission to allow:
    - 'user' group to view 'tilat', 'varaajat', and 'varaukset' and add 'varaukset' only.
    - 'admin' group to have full CRUD access.
    """

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.user.groups.filter(name='Admin').exists():
                return True  # Admins have full access

            elif request.user.groups.filter(name='User').exists():
                if view.action in ['list', 'retrieve'] or (view.action == 'create' and view.basename == 'varaukset'):
                    return True  # Users can view all and create reservations only

        return False
