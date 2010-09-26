from django.conf.urls.defaults import *
from models import Event # relative import

info_dict = {
    'queryset': Event.objects.all(),
    'date_field': 'date',
    'allow_future': True,
}

urlpatterns = patterns('django.views.generic.date_based',
    (r'^(?P<year>\d{4})/$', 'archive_year', dict(info_dict,
                                                 make_object_list=True)),
)

urlpatterns += patterns('sflc.apps.events.views',
    (r'^/?$', 'custom_index', dict(info_dict, queryset=Event.past.all(), paginate_by=10)),
    (r'^(?P<year>\d{4})/(?P<slug>[-\w]+)/$', 'event_detail', dict(info_dict, slug_field='slug')),
    (r'^ics/$', 'future_event_ics', info_dict),
)
