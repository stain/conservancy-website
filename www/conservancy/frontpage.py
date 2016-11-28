from conservancy import render_template_with_context
from conservancy.apps.supporters.models import Supporter as Supporter
from conservancy.apps.news.models import PressRelease
from conservancy.apps.blog.models import Entry as BlogEntry
from datetime import datetime

def view(request):
    """Conservancy front page view

    Performs all object queries necessary to render the front page.
    """

    now = datetime.now()
    context = {
        'press_releases': PressRelease.objects.all().filter(pub_date__lte=now, sites=2)[:5],
        'supporters_count': len(Supporter.objects.all().filter(display_until_date__gte=now)),
        'blog': BlogEntry.objects.all().filter(pub_date__lte=now)[:5],
    }
    return render_template_with_context(request, "frontpage.html", context)
