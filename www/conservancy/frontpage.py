from django.shortcuts import render_to_response
from conservancy.apps.supporters.models import Supporter as Supporter
from conservancy.apps.news.models import PressRelease
from conservancy.apps.blog.models import Entry as BlogEntry
from datetime import datetime, timedelta

def view(request):
    """Conservancy front page view

    Performs all object queries necessary to render the front page.
    """

    supporters_count = len(Supporter.objects.all().filter(display_until_date__gte=datetime.now()))
    press_releases = PressRelease.objects.all().filter(pub_date__lte=datetime.now(), sites=2)[:5]
    blog = BlogEntry.objects.all().filter(pub_date__lte=datetime.now())[:3]

    c = {
        'press_releases': press_releases,
        'supporters_count': supporters_count,
        'blog' : blog
    }
    return render_to_response("frontpage.html", c)
