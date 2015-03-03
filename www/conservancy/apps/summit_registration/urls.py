from django.conf.urls import patterns, url, include

urlpatterns = patterns('conservancy.apps.summit_registration.views',
   (r'^/?$', 'register'),
)
