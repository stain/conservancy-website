# from django.views.generic.list_detail import object_list
from django.views.generic import ListView
from django.template import RequestContext
from conservancy import context_processors as context_processors
from django.shortcuts import render_to_response
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
                                    
def listing(request, *args, **kwargs):
    news_queryset = PressRelease.objects.all()

#    if (not kwargs.has_key('allow_future')) or not kwargs['allow_future']:
    news_queryset = news_queryset.filter(**{'%s__lte' % kwargs['date_field']:
                          datetime.now()})

    date_list = news_queryset.dates(kwargs['date_field'], 'year')

    paginate_by = kwargs.get('paginate_by', 6)  # Show 6 news items per page, by default
    paginator = Paginator(news_queryset, paginate_by)

    page = request.GET.get('page')
    try:
        news = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        news = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        news = paginator.page(paginator.num_pages)

    return render_to_response('news/pressrelease_list.html', {"news": news, "date_list" : date_list}, context_instance=RequestContext(request))

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

