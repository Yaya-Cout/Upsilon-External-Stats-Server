"""Custom permissions checks."""
from rest_framework.permissions import BasePermission, IsAdminUser, SAFE_METHODS


class IsAdminOrReadOnlyAndPost(IsAdminUser):
    """Allow write permissions to admin users, and read/POST for everyone else."""

    def has_permission(self, request, view: object) -> bool:
        """Check if the user has permission to access the view."""
        is_admin = super().has_permission(request, view)
        allowed_methods = list(SAFE_METHODS)

        # Post is safe as it's handled by custom code
        allowed_methods.append("POST")
        return request.method in allowed_methods or is_admin
