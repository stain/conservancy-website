from django.conf.urls import patterns, url, include

urlpatterns = patterns('conservancy.apps.contacts.views',
   (r'^/?$', 'subscribe'),
)
