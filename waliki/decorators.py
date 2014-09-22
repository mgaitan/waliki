from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied
from .settings import WALIKI_ANONYMOUS_USER_PERMISSIONS, WALIKI_LOGGED_USER_PERMISSIONS


def permission_required(perm, login_url=None, raise_exception=False):
    """
    same than django's builtin permission_required decorator but supporting
    anonymous and logged users.
    """
    def check_perms(user):
        if perm in WALIKI_ANONYMOUS_USER_PERMISSIONS:
            return True

        if user.is_authenticated() and perm in WALIKI_LOGGED_USER_PERMISSIONS:
            return True

        if not isinstance(perm, (list, tuple)):
            perms = (perm, )
        else:
            perms = perm
        # First check if the user has the permission (even anon users)
        if user.has_perms(perms):
            return True
        # In case the 403 handler should be called raise the exception
        if raise_exception:
            raise PermissionDenied
        # As the last resort, show the login form
        return False

    return user_passes_test(check_perms, login_url=login_url)
