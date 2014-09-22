from functools import wraps
from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.utils.decorators import available_attrs
from django.utils.encoding import force_str
from django.utils.six.moves.urllib.parse import urlparse
from django.shortcuts import resolve_url
from .settings import WALIKI_ANONYMOUS_USER_PERMISSIONS, WALIKI_LOGGED_USER_PERMISSIONS


def protected_by_guardian(perm, page):
    try:
        import guardian
    except ImportError:
        return False
    if 'guardian' not in settings.INSTALLED_APPS:
        return False



def page_permission(perm, login_url=None, raise_exception=False):

    def check_perms(user):

        """
        same than django's builtin permission_required decorator but supporting
        anonymous and logged users.
        """

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


    def decorator(view_func):
        @wraps(view_func, assigned=available_attrs(view_func))
        def _wrapped_view(request, *args, **kwargs):

            import ipdb; ipdb.set_trace()

            if check_perms(request.user):
                return view_func(request, *args, **kwargs)
            path = request.build_absolute_uri()
            # urlparse chokes on lazy objects in Python 3, force to str
            resolved_login_url = force_str(
                resolve_url(login_url or settings.LOGIN_URL))
            # If the login url is the same scheme and net location then just
            # use the path as the "next" url.
            login_scheme, login_netloc = urlparse(resolved_login_url)[:2]
            current_scheme, current_netloc = urlparse(path)[:2]
            if ((not login_scheme or login_scheme == current_scheme) and
                    (not login_netloc or login_netloc == current_netloc)):
                path = request.get_full_path()
            from django.contrib.auth.views import redirect_to_login
            return redirect_to_login(
                path, resolved_login_url, redirect_field_name)
        return _wrapped_view

    return decorator