from models import Entry, EntryTag # relative import
# from django.views.generic.list_detail import object_list
from django.views.generic import ListView
from django.views.generic.dates import YearArchiveView, MonthArchiveView, DayArchiveView, DateDetailView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from conservancy.apps.staff.models import Person
from django.shortcuts import get_object_or_404, render_to_response
from datetime import datetime

def OR_filter(field_name, objs):
    from django.db.models import Q
    return reduce(lambda x, y: x | y,
                  [Q(**{field_name: x.id}) for x in objs])

def last_name(person):
    return person.formal_name.rpartition(' ')[2]

class BlogListView(ListView):
    extra_context = {}
    
    def get_context_data(self, **kwargs):
        context = super(BlogListView, self).get_context_data(**kwargs)
        # context['key'] = 'value'
        context.update(self.extra_context)
        return context
                                    
def custom_index(request, queryset, *args, **kwargs):
    """Blog list view that allows scrolling and also shows an index by
    year.
    """

    kwargs = kwargs.copy()
    kwargs['extra_context'] = kwargs.get('extra_context', {}).copy()
    extra_context = kwargs['extra_context']

    date_field = kwargs['date_field']
    del kwargs['date_field']

    if not kwargs.get('allow_future', False):
        queryset = queryset.filter(**{'%s__lte' % date_field: datetime.now()})

    authors = []
    if 'author' in request.GET:
        authors = [get_object_or_404(Person, username=author)
                   for author in request.GET.getlist('author')]
        extra_context['authors'] = authors
        queryset = queryset.filter(OR_filter('author', authors))

    tags = []
    if 'tag' in request.GET:
        tags = [get_object_or_404(EntryTag, slug=tag)
                for tag in request.GET.getlist('tag')]
        extra_context['tags'] = tags
        queryset = queryset.filter(OR_filter('tags', tags))

    if authors or tags:
        query_string = '&'.join(['author=%s' % a.username for a in authors]
                                + ['tag=%s' % t.slug for t in tags])
        extra_context['query_string'] = query_string

    else:
        date_list = queryset.dates(date_field, 'year')
        extra_context['date_list'] = date_list

    # return object_list(request, queryset, *args, **kwargs)
    kwargs['queryset'] = queryset
    kwargs['extra_context'] = extra_context

    paginate_by = kwargs.get('paginate_by', 6)  # Show 6 news items per page, by default
    paginator = Paginator(queryset, paginate_by)

    page = request.GET.get('page')

    try:
        blog_entries = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        blog_entries = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        blog_entires = paginator.page(paginator.num_pages)

    return render_to_response('blog/entry_list.html',
                              {"blog_entries": blog_entries, "date_list" : date_list,
                               "authors" : authors, "tags" : tags })

    callable = BlogListView.as_view(**kwargs)
    return callable(request)

def techblog_redirect(request):
    """Redirect from the old 'techblog' to the new blog
    """

    path = request.path[len('/technology'):]
    if path == '/blog/':
        path += "?author=bkuhn"

    return relative_redirect(request, path)

def query(request):
    """Page to query the blog based on authors and tags
    """

    if request.GET:
        d = request.GET.copy()
        if 'authors' in d.getlist('all'):
            d.setlist('author', []) # remove author queries
        if 'tags' in d.getlist('all'):
            d.setlist('tag', []) # remove tag queries
        d.setlist('all', []) # remove "all" from the query string

        base_url = '/blog/'
        if 'rss' in d:
            base_url = '/feeds/blog/'
            d.setlist('rss', []) # remove it

        query_string = d.urlencode()

        return relative_redirect(request, '%s%s%s' % (base_url, '?' if query_string else '', query_string))

    else:
        authors = sorted(Person.objects.filter(currently_employed=True,
                                               entry__isnull=False).distinct(),
                         key=last_name)
        tags = EntryTag.objects.all().order_by('label')
        return render_to_response('blog/query.html',
                                  {'authors': authors, 'tags': tags})

def relative_redirect(request, path):
    from django import http
    from django.conf import settings

    host = request.get_host()
    if settings.FORCE_CANONICAL_HOSTNAME:
        host = settings.FORCE_CANONICAL_HOSTNAME

    url = "%s://%s%s" % (request.is_secure() and 'https' or 'http', host, path)
    return http.HttpResponseRedirect(url)

class BlogYearArchiveView(YearArchiveView):
    make_object_list = True
    allow_future = True
    extra_context = {}
    
    def get_context_data(self, **kwargs):
        context = super(BlogYearArchiveView, self).get_context_data(**kwargs)
        context.update(self.extra_context)
        return context

class BlogMonthArchiveView(MonthArchiveView):
    allow_future = True
    extra_context = {}
    
    def get_context_data(self, **kwargs):
        context = super(BlogMonthArchiveView, self).get_context_data(**kwargs)
        context.update(self.extra_context)
        return context

class BlogDayArchiveView(DayArchiveView):
    allow_future = True
    extra_context = {}
    
    def get_context_data(self, **kwargs):
        context = super(BlogDayArchiveView, self).get_context_data(**kwargs)
        context.update(self.extra_context)
        return context

class BlogDateDetailView(DateDetailView):
    allow_future = True
    extra_context = {}
    
    def get_context_data(self, **kwargs):
        context = super(BlogDateDetailView, self).get_context_data(**kwargs)
        context.update(self.extra_context)
        return context
