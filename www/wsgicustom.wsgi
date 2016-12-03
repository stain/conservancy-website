# wsgicustom.py

import os
import sys

root_dir = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, root_dir)
os.environ['DJANGO_SETTINGS_MODULE'] = 'conservancy.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
