from django.shortcuts import render_to_response
from sflc.apps.news.models import PressRelease
from datetime import datetime, timedelta

def view(request):
    """Conservancy front page view

    Performs all object queries necessary to render the front page.
    """

    press_releases = PressRelease.objects.all().filter(pub_date__lte=datetime.now(), sites=2)[:5]

    c = {
        'press_releases': press_releases,
    }
    return render_to_response("frontpage.html", c)
