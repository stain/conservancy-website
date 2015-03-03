# wsgicustom.py

import os
import sys

sys.path = ['/var/www'] + sys.path
os.environ['DJANGO_SETTINGS_MODULE'] = 'conservancy.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
