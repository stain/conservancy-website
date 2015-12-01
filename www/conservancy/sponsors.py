from django.shortcuts import render_to_response
from conservancy import context_processors as context_processors
from django.template import RequestContext
from conservancy.apps.supporters.models import Supporter as Supporter
from datetime import datetime, timedelta

def view(request):
    """Conservancy Sponsors Page view

    Performs object queries necessary to render the sponsors page.
    """

    supporters = Supporter.objects.all().filter(display_until_date__gte=datetime.now())
    supporters_count = len(supporters)
    anonymous_count  = len(supporters.filter(display_name = 'Anonymous'))
    supporters = supporters.exclude(display_name = 'Anonymous').order_by('ledger_entity_id')

    c = {
        'supporters' : supporters,
        'supporters_count' : supporters_count,
        'anonymous_count' : anonymous_count
    }
    return render_to_response("sponsors.html", c, context_instance=RequestContext(request))
