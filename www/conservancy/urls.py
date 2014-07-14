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

from django.conf.urls.defaults import *
from django.contrib import admin
from conservancy.feeds import BlogFeed, PressReleaseFeed, OmnibusFeed

handler404 = 'modpythoncustom.view404'

admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/(.*)', admin.site.urls),
    (r'^feeds/blog/?$', BlogFeed()),
    (r'^feeds/news/?$', PressReleaseFeed()),
    (r'^feeds/omnibus/?$', OmnibusFeed()),
    (r'^feeds/?$', 'conservancy.feeds.view'),
    (r'^news(/|$)', include('conservancy.apps.news.urls')),
    (r'^blog(/|$)', include('conservancy.apps.blog.urls')),
)
