from django.conf.urls import patterns, url, include
from models import Entry, EntryTag # relative import
from conservancy.apps.staff.models import Person
from datetime import datetime
from views import last_name, BlogYearArchiveView, BlogMonthArchiveView, BlogDayArchiveView, BlogDateDetailView

extra_context = {}

info_dict = {
    'queryset': Entry.objects.all(),
    'date_field': 'pub_date',
    'extra_context': extra_context,
}

# urlpatterns = patterns('django.views.generic.date_based',
urlpatterns = patterns('',
   # (r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/(?P<slug>[-\w]+)/$', 'object_detail', dict(info_dict, slug_field='slug')),
   # (r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/$', 'archive_day', info_dict),
   # (r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/$', 'archive_month', info_dict),
   # (r'^(?P<year>\d{4})/$', 'archive_year', dict(info_dict,
   #                                              make_object_list=True)),
   (r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/(?P<slug>[-\w]+)/$', BlogDateDetailView.as_view(**info_dict)),
   (r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/$', BlogDayArchiveView.as_view(**info_dict)),
   (r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/$', BlogMonthArchiveView.as_view(**info_dict)),
   (r'^(?P<year>\d{4})/$', BlogYearArchiveView.as_view(**info_dict)),
)

urlpatterns += patterns('conservancy.apps.blog.views',
   (r'^/?$', 'custom_index', dict(info_dict, paginate_by=10)),
   (r'^query/$', 'query'),
)

# Code to display authors and tags on each blog page

def all_tags_by_use_amount():
    """Returns all tags with an added 'cnt' attribute (how many times used)

    Also sorts the tags so most-used tags appear first.
    """

    # tally use amount
    retval = []
    current = None
    for obj in EntryTag.objects.filter(entry__pub_date__lte=datetime.now(),
                                       entry__isnull=False).order_by('label'):
        if current is not None and obj.id == current.id:
            current.cnt += 1
        else:
            if current is not None:
                retval.append(current)
            current = obj
            current.cnt = 1
    if current is not None:
        retval.append(current)

    # sort and return
    retval.sort(key=lambda x: -x.cnt)
    return retval

def all_authors():
    return sorted(Person.objects.filter(entry__isnull=False).distinct(),
                  key=last_name)

# The functions are passed to the context uncalled so they will be
# called for each web request.  If we want to only make these database
# queries a single time when a web server process begins, call both
# functions below (i.e. make both lines below end in '()')

extra_context['all_authors'] = all_authors
extra_context['all_tags'] = all_tags_by_use_amount
