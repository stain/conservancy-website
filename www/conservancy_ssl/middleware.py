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

from django import http

class RedirectToNonSslSite(object):

    def process_request(self, request):
        """Redirect to non-SSL site if not an admin request
        """

        if not request.path.startswith('/admin'):
            url = 'http://www.sfconservancy.org%s' % request.path
            return http.HttpResponseRedirect(url)

        return None
