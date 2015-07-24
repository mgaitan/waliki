# -*- encoding: utf-8 -*-
from django.contrib.auth.models import AnonymousUser

from waliki import settings
from waliki.acl import check_perms

from rest_framework.permissions import BasePermission

class WalikiPermission(BasePermission):
    """
    	Base Permission Class for Waliki default and ACL rules
    """
    permission = ''
    
    def has_permission(self, request, view, *args, **kwargs):
    	slug = request.resolver_match.kwargs.get('slug', ' ')
    	if check_perms((self.permission), request.user, slug):
    		return True
    	else:
	    	if isinstance(request.user, AnonymousUser):
	    		if self.permission in settings.WALIKI_ANONYMOUS_USER_PERMISSIONS:
	    			return True
	    	else:
	    		if self.permission in settings.WALIKI_LOGGED_USER_PERMISSIONS:
	        		return True


class WalikiPermission_AddPage(WalikiPermission):
	permission = 'add_page'

class WalikiPermission_ViewPage(WalikiPermission):
	permission = 'view_page'

class WalikiPermission_ChangePage(WalikiPermission):
	permission = 'change_page'