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

import os.path

from djangocommonsettings import *

SITE_ID = 2
ROOT_URLCONF = 'conservancy.urls'

FORCE_CANONICAL_HOSTNAME = False if DEBUG else 'sfconservancy.org'

ALLOWED_HOSTS = [ 'www.sfconservancy.org', 'aspen.sfconservancy.org', 'sfconservancy.org',  u'104.130.70.210' ]

REDIRECT_TABLE = {
    'www.sf-conservancy.org': 'sfconservancy.org',
}

_root_dir = os.path.abspath(os.path.dirname(__file__))
TEMPLATE_DIRS = (
    os.path.join(_root_dir, 'templates'),
    os.path.join(_root_dir, 'static'),
)
del _root_dir

# try:
#     from djangodebug import conservancy_hostname as FORCE_CANONICAL_HOSTNAME
# except:
#     pass
