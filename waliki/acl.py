from functools import wraps
from collections import Iterable
from django.conf import settings
from django.shortcuts import render
from django.core.exceptions import PermissionDenied
from django.utils.decorators import available_attrs
from django.utils.encoding import force_str
from django.utils.six.moves.urllib.parse import urlparse
from django.utils.six import string_types
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.shortcuts import resolve_url
from .models import ACLRule
from .settings import (WALIKI_ANONYMOUS_USER_PERMISSIONS,
                       WALIKI_LOGGED_USER_PERMISSIONS,
                       WALIKI_RENDER_403)


def check_perms(perms, user, slug, raise_exception=False):
    """a helper user to check if a user has the permissions
    for a given slug"""
    if isinstance(perms, string_types):
        perms = {perms}
    else:
        perms = set(perms)

    allowed_users = ACLRule.get_users_for(perms, slug)

    if allowed_users:
        return user in allowed_users

    if perms.issubset(set(WALIKI_ANONYMOUS_USER_PERMISSIONS)):
        return True

    if user.is_authenticated() and perms.issubset(set(WALIKI_LOGGED_USER_PERMISSIONS)):
        return True

    # First check if the user has the permission (even anon users)
    if user.has_perms(perms):
        return True
    # In case the 403 handler should be called raise the exception
    if raise_exception:
        raise PermissionDenied
    # As the last resort, show the login form
    return False


def permission_required(perms, login_url=None, raise_exception=False, redirect_field_name=REDIRECT_FIELD_NAME):
    """
    this is analog to django's builtin ``permission_required`` decorator, but
    improved to check per slug ACLRules and default permissions for
    anonymous and logged in users

    if there is a rule affecting a slug, the user needs to be part of the
    rule's allowed users. If there isn't a matching rule, defaults permissions
    apply.
    """

    def decorator(view_func):
        @wraps(view_func, assigned=available_attrs(view_func))
        def _wrapped_view(request, *args, **kwargs):

            if check_perms(perms, request.user, kwargs['slug'], raise_exception=raise_exception):
                return view_func(request, *args, **kwargs)
            if request.user.is_authenticated():
                if WALIKI_RENDER_403:
                    return render(request, 'waliki/403.html', kwargs, status=403)
                else:
                    raise PermissionDenied

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