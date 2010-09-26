from django.conf.urls.defaults import *

urlpatterns = patterns('conservancy.apps.contacts.views',
   (r'^/?$', 'subscribe'),
)
