from django.views.generic.list_detail import object_list
from django.shortcuts import render_to_response
from django.http import Http404, HttpResponse
from django.template import loader
from django.core.exceptions import ObjectDoesNotExist
from models import Event # relative import

def event_detail(request, year, slug, queryset, **kwargs):
    """This view shows event detail.

    Nothing special, but it is necessary because
    django.views.generic.date_based.object_detail only works with
    slugs that are unique and specified by day, but we make slugs
    unique by year.
    """

    try:
        event = queryset.get(date__year=year, slug__exact=slug)
    except ObjectDoesNotExist:
        raise Http404, "Event does not exist"
    return render_to_response('events/event_detail.html', {'event': event})

def custom_index(request, queryset, *args, **kwargs):
    """Scrollable index of future and past events, with date index.
    """

    future_events = None
    if not request.GET.has_key("page"):
        future_events = Event.future.all().order_by("date")

    date_list = queryset.dates(kwargs['date_field'], 'year')

    kwargs = dict(kwargs, extra_context={'date_list': date_list,
                                         'future_events': future_events})
    del kwargs['date_field']
    del kwargs['allow_future']

    return object_list(request, queryset, *args, **kwargs)

def future_event_ics(request, queryset, *args, **kwargs):
    """ICS calendar view of future events

    This view just renders information into a template that looks like
    an ics file.  If in the future we want a 'real' implementation of
    this function, there is a python 'vobject' library that can be
    used.  Search google for details, or see
    http://www.technobabble.dk/2008/mar/06/exposing-calendar-events-using-icalendar-django/
    Hopefully at some point this functionality is integrated into
    django.contrib.
    """

    future_events = Event.future.all().order_by("date")

    return HttpResponse(loader.render_to_string('events/calendar.ics',
                                                {'events': future_events}),
                        mimetype='text/calendar')
