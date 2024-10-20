"""
WSGI config for myproject project.
It exposes the WSGI callable as a module-level variable named ``application``.
For more information on this file, see
https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/
"""

import os
import sys
from django.core.wsgi import get_wsgi_application

os.environ['DJANGO_SETTINGS_MODULE'] = 'cycling_api.settings'

path='/home/david/cycling_climbs_api'
if path not in sys.path:
        sys.path.append(path)

application = get_wsgi_application()
