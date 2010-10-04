from django.conf.urls.defaults import *
from conservancy.feeds import feed_dict

handler404 = 'modpythoncustom.view404'

urlpatterns = patterns('',
    (r'^$', 'conservancy.frontpage.view'),
    (r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed',
     {'feed_dict': feed_dict}),
    (r'^feeds/$', 'conservancy.feeds.view'),
    (r'^news/', include('conservancy.apps.news.urls')),
    (r'^blog/', include('conservancy.apps.blog.urls')),
)
