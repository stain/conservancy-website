from django.conf.urls.defaults import *

urlpatterns = patterns('sflc.apps.summit_registration.views',
   (r'^/?$', 'register'),
)
