from django.views.generic.list_detail import object_list
from conservancy.apps.news.models import ExternalArticle
from conservancy.apps.events.models import Event
from datetime import datetime

def custom_index(request, queryset, *args, **kwargs):
    """News index.  Calls a generic list view, but passes additional
    context including past and future events, and an index of news by
    year.
    """

    articles = None
    #if not request.GET.has_key("page"):
    #    articles = ExternalArticle.public.all().order_by("-date")[:10]

    if (not kwargs.has_key('allow_future')) or not kwargs['allow_future']:
        queryset = queryset.filter(**{'%s__lte' % kwargs['date_field']:
                                      datetime.now()})

    future_events = Event.future.all().filter(date_tentative=False).order_by("date")
    past_events = Event.past.all().order_by("-date")[:6]

    date_list = queryset.dates(kwargs['date_field'], 'year')

    kwargs = dict(kwargs, extra_context={'articles': articles,
                                         'date_list': date_list,
                                         'future_events': future_events,
                                         'past_events': past_events})
    del kwargs['date_field']

    return object_list(request, queryset, *args, **kwargs)

#    num_navigation = 3 # in each direction
#    page_navigation = range(max((page - num_navigation), 1),
#                            min((page + num_navigation), page_count) + 1)
