# Copyright 2005-2008, James Garrison
# Copyright 2010, Bradley M. Kuhn

# This software's license gives you freedom; you can copy, convey,
# propagate, redistribute, modify and/or redistribute modified versions of
# this program under the terms of the GNU Affero General Public License
# (AGPL) as published by the Free Software Foundation (FSF), either
# version 3 of the License, or (at your option) any later version of the
# AGPL published by the FSF.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Affero
# General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program in a file in the toplevel directory called
# "AGPLv3".  If not, see <http://www.gnu.org/licenses/>.

from django.conf.urls import patterns, url, include
from django.conf import settings
from models import PressRelease, ExternalArticle # relative import
from views import NewsYearArchiveView, NewsMonthArchiveView, NewsDayArchiveView, NewsDateDetailView

info_dict = {
    'queryset': PressRelease.objects.all().filter(sites__id__exact=settings.SITE_ID),
    'date_field': 'pub_date',
}

external_article_dict = {
    'articles': ExternalArticle.objects.all()
}

urlpatterns = patterns('',
#    (r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/(?P<slug>[-\w]+)/$', 'conservancy.apps.news.views.object_detail', info_dict),
   (r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/(?P<slug>[-\w]+)/$', NewsDateDetailView.as_view(**info_dict)),
#   (r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/$', 'conservancy.apps.news.views.archive_day', info_dict),
   (r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/$', NewsDayArchiveView.as_view(**info_dict)),
#   (r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/$', 'conservancy.apps.news.views.archive_month', info_dict),
   (r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/$', NewsMonthArchiveView.as_view(**info_dict)),
#   (r'^(?P<year>\d{4})/$', 'conservancy.apps.news.views.archive_year',
#    dict(info_dict, make_object_list=True)),
   (r'^(?P<year>\d{4})/$', NewsYearArchiveView.as_view(**info_dict)),
)

urlpatterns += patterns('',
   (r'^/?$', 'conservancy.apps.news.views.custom_index', dict(info_dict, paginate_by=6)),
)
