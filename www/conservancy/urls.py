# Copyright 2005-2008, James Garrison
# Copyright 2010, 2012 Bradley M. Kuhn

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

from django.conf.urls import url, include
from django.contrib import admin, admindocs

from conservancy import feeds, frontpage, sponsors
import conservancy.apps.fundgoal.views as fundgoal_views
import conservancy.static.views as static_views

admin.autodiscover()

urlpatterns = [
    url(r'^$', frontpage.view),
    url(r'^sponsors$', frontpage.view),
    url(r'^sponsors/$', sponsors.view),
    url(r'^sponsors/index.html$', sponsors.view),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^feeds/blog/?$', feeds.BlogFeed()),
    url(r'^feeds/news/?$', feeds.PressReleaseFeed()),
    url(r'^feeds/omnibus/?$', feeds.OmnibusFeed()),
    url(r'^feeds/?$', feeds.view),
    url(r'^news(/|$)', include('conservancy.apps.news.urls')),
    url(r'^blog(/|$)', include('conservancy.apps.blog.urls')),
    # formerly static templated things... (dirs with templates)
    url(r'^error/(40[134]|500)(?:/index\.html|/|)$', static_views.handler),
    url(r'^error', static_views.index),
    url(r'^about', static_views.index),
    url(r'^donate', static_views.index),
    url(r'^copyleft-compliance', static_views.index,
                           {'fundraiser_sought' : 'vmware-match-0'}),
    url(r'^projects', static_views.index),
    url(r'^npoacct', static_views.index,
                  {'fundraiser_sought' : 'npoacct'}),
    url(r'^contractpatch', include('conservancy.apps.contractpatch.urls')),
    url(r'^overview', static_views.index),
    url(r'^privacy-policy', static_views.index),
    url(r'^supporter', include('conservancy.apps.supporter.urls')),
    url(r'^fundraiser_data', fundgoal_views.view),
]
