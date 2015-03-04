# from django.views.generic.list_detail import object_list
from django.views.generic import ListView
from django.views.generic.dates import YearArchiveView, MonthArchiveView, DayArchiveView, DateDetailView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from conservancy.apps.news.models import ExternalArticle
from conservancy.apps.news.models import PressRelease
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
                                    
def listing(request):
    news_queryset = PressRelease.objects.all()

#    if (not kwargs.has_key('allow_future')) or not kwargs['allow_future']:
    news_queryset = news_queryset.filter(**{'%s__lte' % kwargs['date_field']:
                          datetime.now()})

    date_list = news.dates(kwargs['date_field'], 'year')

    paginator = Paginator(news_queryset, 6) # Show 6 news items per page

    page = request.GET.get('page')
    try:
        news = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        news = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        news = paginator.page(paginator.num_pages)

    return render_to_response('pressrelease_list.html', {"news": news, "date_list" : date_list})

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

    paginate_by = kwargs.get('paginate_by', 6)
    paginator = Paginator(queryset, paginate_by)
    page = request.GET.get('page')
    try:
        p = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        p = paginator.page(1)
        page = 1
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        p = paginator.page(paginator.num_pages)
        page = paginator.num_pages
    kwargs = dict(kwargs, extra_context={'articles': articles,
                                         'date_list': date_list,
                                         'future_events': future_events,
                                         'past_events': past_events,
                                         # 'paginator': paginator,
                                         'page': page,
                                         # 'is_paginated': True,
                                         # 'num_pages': paginator.num_pages
                                     })
    del kwargs['date_field']
    kwargs['queryset'] = queryset
    
    # return object_list(request, queryset, *args, **kwargs)
    # callable = NewsListView.as_view(queryset=queryset,
    #                                 extra_context=kwargs,
    #                                 paginate_by=kwargs['paginate_by'])
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

