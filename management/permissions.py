from django.core.exceptions import PermissionDenied
from functools import wraps
from .models import UserRole

def role_required(allowed_roles):
    def decorator(view_func):
        @wraps(view_func)
        def wrapped(request, *args, **kwargs):
            try:
                user_role = UserRole.objects.get(user=request.user)
                if user_role.role.name in allowed_roles:
                    return view_func(request, *args, **kwargs)
            except UserRole.DoesNotExist:
                pass
            raise PermissionDenied("You don't have permission to access this resource.")
        return wrapped
    return decorator

# Permission constants
PERMISSIONS = {
    'admin': [
        'view_property',
        'add_property',
        'change_property',
        'delete_property',
        'view_maintenance',
        'add_maintenance',
        'change_maintenance',
        'view_payment',
        'add_payment',
        'change_payment',
    ],
    'property_manager': [
        'view_property',
        'change_property',
        'view_maintenance',
        'change_maintenance',
        'view_payment',
    ],
    'tenant': [
        'view_property',
        'add_maintenance',
        'view_maintenance',
        'add_payment',
        'view_payment',
    ]
}



