from haystack.views import SearchView
from haystack.forms import SearchForm

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test

from django.conf import settings

def user_has_permission(user):
    if 'view_page' in settings.WALIKI_ANONYMOUS_USER_PERMISSIONS:
        return True

    if user.is_authenticated() and user.is_active:
        return True

    return False

class WalikiSearchView(SearchView):

    # Permissions check for search page
    @method_decorator(user_passes_test(user_has_permission))
    def __call__(self, request):
        return super(WalikiSearchView, self).__call__(request)
