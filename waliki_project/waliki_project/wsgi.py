"""
WSGI config for waliki_project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""
import os
import sys

# for demo
INTERP = '/home/waliki/.virtualenvs/waliki/bin/python'
if os.path.exists(INTERP) and sys.executable != INTERP:
    #INTERP is present twice so that the new python interpreter knows the actual executable path
    os.execl(INTERP, INTERP, *sys.argv)
    sys.path.append('/home/waliki/waliki/waliki_project')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "waliki_project.settings")
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
