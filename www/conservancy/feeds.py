from django.contrib.syndication.feeds import Feed
from conservancy.apps.news.models import PressRelease

from django.shortcuts import render_to_response
from django.conf import settings
import datetime

class PressReleaseFeed(Feed):
    title = "Software Freedom Conservancy News"
    link = "/news/"
    description = ""

    def items(self):
        return PressRelease.objects.filter(pub_date__lte=datetime.datetime.now(),
                                           sites__id__exact=settings.SITE_ID).order_by('-pub_date')[:10]

    def item_pubdate(self, item):
        return item.pub_date

feed_dict = {
    'news': PressReleaseFeed,
}

# make each feed know its canonical url
for k, v in feed_dict.items():
    v.get_absolute_url = '/feeds/%s/' % k

def view(request):
    """Listing of all available feeds
    """

    return render_to_response("feeds.html", {'feeds': feed_dict.values()})
