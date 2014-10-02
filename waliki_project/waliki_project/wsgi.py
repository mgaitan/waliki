"""
WSGI config for waliki_project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""
import os
import sys

# for demo
activate_this = '/home/waliki/.virtualenvs/waliki/bin/activate_this.py'
if os.path.exists(activate_this):
    with open(activate_this) as f:
        code = compile(f.read(), activate_this, 'exec')
        exec(code, dict(__file__=activate_this))

path = '/home/waliki/waliki/waliki_project'
if path not in sys.path:
    sys.path.append(path)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "waliki_project.settings")
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
