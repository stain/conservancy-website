from django.conf.urls import patterns, url, include

urlpatterns = patterns(
    '',
    (r'', 'conservancy.apps.contractpatch.views.index'),
)
