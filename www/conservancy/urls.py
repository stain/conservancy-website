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

from django.conf.urls import patterns, url, include
from django.contrib import admin

# import conservancy.settings
from django.conf import settings
from conservancy.feeds import BlogFeed, PressReleaseFeed, OmnibusFeed
# from django.views.static import serve
# from django.conf.urls.static import static
# from django.contrib.staticfiles.urls import staticfiles_urlpatterns
# import conservancy.static.overview.views

# handler404 = 'modpythoncustom.view404'
# handler401 = 'conservancy.static.views.handler401'
# handler403 = 'conservancy.static.views.handler403'
handler404 = 'conservancy.static.views.handler404'
# handler500 = 'conservancy.static.views.handler500'

admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', 'conservancy.frontpage.view'),
    (r'^sponsors$', 'conservancy.frontpage.view'),
    (r'^sponsors/$', 'conservancy.sponsors.view'),
    (r'^sponsors/index.html$', 'conservancy.sponsors.view'),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', admin.site.urls),
    (r'^feeds/blog/?$', BlogFeed()),
    (r'^feeds/news/?$', PressReleaseFeed()),
    (r'^feeds/omnibus/?$', OmnibusFeed()),
    (r'^feeds/?$', 'conservancy.feeds.view'),
    (r'^news(/|$)', include('conservancy.apps.news.urls')),
    (r'^blog(/|$)', include('conservancy.apps.blog.urls')),
    # formerly static templated things... (dirs with templates)
    (r'^error', 'conservancy.static.views.index'),
    (r'^about', 'conservancy.static.views.index'),
    (r'^donate', 'conservancy.static.views.index'),
    (r'^copyleft-compliance', 'conservancy.static.views.index',
                           {'fundraiser_sought' : 'vmware-match-0'}),
    (r'^members', 'conservancy.static.views.index'),
    (r'^npoacct', 'conservancy.static.views.index',
                  {'fundraiser_sought' : 'npoacct'}),
    (r'^overview', 'conservancy.static.views.index'),
    (r'^privacy-policy', 'conservancy.static.views.index'),
    (r'^supporter', 'conservancy.static.views.index'),
    (r'^fundraiser_data', 'conservancy.apps.fundgoal.views.view'),
)

# urlpatterns += url(regex  = r'^%s(?P<path>.*)$' % conservancy.settings.STATIC_URL[1:],
# urlpatterns += url(regex  = r'^/overview',
#                    view   = 'django.views.static.serve',
#                    kwargs = {'document_root': conservancy.settings.STATIC_ROOT,
#                              'show_indexes' : True})
# urlpatterns += (r'^(?P<path>.*)$', 'django.views.static.serve', 
# urlpatterns += (r'^overview/$', 'django.views.static.serve', 
#                 {'document_root': conservancy.settings.STATIC_ROOT,
#                  'show_indexes' : True})

# https://docs.djangoproject.com/en/1.7/howto/static-files/
#  + static(conservancy.settings.STATIC_URL, document_root=conservancy.settings.STATIC_ROOT)

# urlpatterns += staticfiles_urlpatterns()

# urlpatterns += static(settings.STATIC_URL, view='django.contrib.staticfiles.views.serve',
# urlpatterns += static('/', view='django.contrib.staticfiles.views.serve',
#                       document_root=settings.STATIC_ROOT,
#                       show_indexes=True)




