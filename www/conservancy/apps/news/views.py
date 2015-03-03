# from django.views.generic.list_detail import object_list
from django.views.generic import ListView
from django.views.generic.dates import YearArchiveView, MonthArchiveView, DayArchiveView, DateDetailView
from conservancy.apps.news.models import ExternalArticle
from conservancy.apps.events.models import Event
from datetime import datetime
# for debugging...
from django.http import HttpResponse


class NewsListView(ListView):
    extra_context = {}
    def get_context_data(self, **kwargs):
        context = super(NewsListView, self).get_context_data(**kwargs)
        # context['key'] = 'value'
        context.update(self.extra_context)
        return context
                                    
def custom_index(request, queryset, *args, **kwargs):
    """News index.  Calls a generic list view, but passes additional
    context including past and future events, and an index of news by
    year.
    """
    # debug = '<pre>This is news'
    # debug += '\nqueryset: ' + str(queryset)
    # debug += '\nargs: ' + str(args)
    # debug += '\nkwargs: ' + str(kwargs)
    # debug += '</pre>'
    # return HttpResponse(debug)

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
                                         'past_events': past_events,
                                         'page': 1})
    del kwargs['date_field']

    # return object_list(request, queryset, *args, **kwargs)
    # callable = NewsListView.as_view(queryset=queryset,
    #                                 extra_context=kwargs,
    #                                 paginate_by=kwargs['paginate_by'])
    kwargs['queryset'] = queryset
    callable = NewsListView.as_view(**kwargs)
    return callable(request)

#    num_navigation = 3 # in each direction
#    page_navigation = range(max((page - num_navigation), 1),
#                            min((page + num_navigation), page_count) + 1)

class NewsYearArchiveView(YearArchiveView):
    # queryset = Article.objects.all()
    # date_field = "pub_date"
    make_object_list = True
    allow_future = True

# def archive_year(request, **kwargs):
#     callable = NewsYearArchiveView.as_view(**kwargs)
#     return callable(request)

class NewsMonthArchiveView(MonthArchiveView):
    allow_future = True

# def archive_month(request, **kwargs):
#     # return HttpResponse("archive_month")
#     callable = NewsMonthArchiveView.as_view(**kwargs)
#     return callable(request)

class NewsDayArchiveView(DayArchiveView):
    allow_future = True

# def archive_day(request, **kwargs):
#     # return HttpResponse("archive_day")
#     callable = NewsDayArchiveView.as_view(**kwargs)
#     return callable(request)

class NewsDateDetailView(DateDetailView):
    # extra_context = {}
    allow_future = True
    # slug_url_kwarg = 'slug'

    # def get_context_data(self, **kwargs):
    #     context = super(NewsDateDetailView, self).get_context_data(**kwargs)
    #     context.update(self.extra_context)
    #     return context

# def object_detail(request, **kwargs):
#     # extra_context = {}
#     # extra_context['slug'] = kwargs['slug']
#     # del kwargs['slug']
#     # kwargs['extra_context'] = extra_context
#     # return HttpResponse("object_detail: " + str(kwargs))
#     # slug = kwargs['slug']
#     # del kwargs['slug']
#     callable = NewsDateDetailView.as_view(**kwargs)
#     return callable(request)

