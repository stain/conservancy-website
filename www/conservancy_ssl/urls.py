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


# Start with typical conservancy url scheme.  The middleware will
# intercept non-admin requests, but having the main conservancy urlconf
# repeated here allows us to browse the automatic documentation in the
# admin interface.

from conservancy.urls import *
from django.contrib import admin

admin.autodiscover()

urlpatterns += patterns('',
                        (r'^admin/doc/', include('django.contrib.admindocs.urls')),
                        (r'^admin/(.*)', admin.site.root),)
