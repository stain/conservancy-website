from django.conf.urls import patterns

INDEX_VIEW = 'conservancy.apps.supporter.views.index'
pattern_pairs = [(r'^/?$', INDEX_VIEW)]
pattern_pairs.extend(
    (r'^{}(?:\.html|/|)$'.format(basename), INDEX_VIEW)
    for basename in ['index', '2015-supporter-appeal', '2016-supporter-appeal']
)
pattern_pairs.append((r'', 'conservancy.static.views.index'))

urlpatterns = patterns('', *pattern_pairs)
