from djangocommonsettings import *

SITE_ID = 2
MEDIA_ROOT = '/var/www/external-website/conservancy/static/media/'
MEDIA_URL = 'http://conservancy.softwarefreedom.org/media'
ROOT_URLCONF = 'conservancy.urls'
FORCE_CANONICAL_HOSTNAME = "conservancy.softwarefreedom.org"

TEMPLATE_DIRS = (
    '/var/www/external-website/conservancy/templates',
)

try:
    from djangodebug import conservancy_hostname as FORCE_CANONICAL_HOSTNAME
except:
    pass
