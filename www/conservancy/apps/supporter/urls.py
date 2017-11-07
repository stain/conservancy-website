from django.conf.urls import url
from conservancy.apps.supporter import views as supp_views
from conservancy.static import views as static_views

INDEX_VIEW = supp_views.index
urlpatterns = [url(r'^/?$', INDEX_VIEW)]
urlpatterns.extend(
    url(r'^{}(?:\.html|/|)$'.format(basename), INDEX_VIEW)
    for basename in ['index', '2015-supporter-appeal', '2016-supporter-appeal']
)
urlpatterns.append(url(r'', static_views.index))
