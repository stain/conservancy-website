from django.conf.urls.defaults import *

urlpatterns = patterns('conservancy.apps.summit_registration.views',
   (r'^/?$', 'register'),
)
