from django.conf.urls.defaults import *
from django.conf import settings
from models import PressRelease, ExternalArticle # relative import

info_dict = {
    'queryset': PressRelease.objects.all().filter(sites__id__exact=settings.SITE_ID),
    'date_field': 'pub_date',
}

external_article_dict = {
    'articles': ExternalArticle.objects.all()
}

urlpatterns = patterns('django.views.generic.date_based',
   (r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/(?P<slug>[-\w]+)/$', 'object_detail', dict(info_dict, slug_field='slug')),
   (r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/$', 'archive_day', info_dict),
   (r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/$', 'archive_month', info_dict),
   (r'^(?P<year>\d{4})/$', 'archive_year', dict(info_dict,
                                                make_object_list=True)),
)

urlpatterns += patterns('',
   (r'^/?$', 'sflc.apps.news.views.custom_index', dict(info_dict, paginate_by=6)),
)
