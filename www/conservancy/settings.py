# Copyright 2005-2008, Software Freedom Law Center, Inc.
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

from djangocommonsettings import *

SITE_ID = 2
MEDIA_ROOT = '/var/www/conservancy/static/media/'
MEDIA_URL = 'http://sfconservancy.org/media'
ROOT_URLCONF = 'conservancy.urls'
FORCE_CANONICAL_HOSTNAME = "sfconservancy.org"

TEMPLATE_DIRS = (
    '/var/www/conservancy/templates',
)

try:
    from djangodebug import conservancy_hostname as FORCE_CANONICAL_HOSTNAME
except:
    pass
