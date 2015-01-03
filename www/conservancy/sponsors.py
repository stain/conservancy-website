from django.shortcuts import render_to_response
from conservancy.apps.supporters.models import Supporter as Supporter
from datetime import datetime, timedelta

def view(request):
    """Conservancy Sponsors Page view

    Performs object queries necessary to render the sponsors page.
    """

    supporters = Supporter.objects.all().filter(display_until_date__gte=datetime.now())
    anonymous_count  = len(supporters.filter(display_name = 'Anonymous'))
    supporters = supporters.exclude(display_name = 'Anonymous')

    c = {
        'supporters' : supporters,
        'anonymous_count' : anonymous_count
    }
    return render_to_response("sponsors.html", c)
