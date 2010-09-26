from django.conf import settings
from django import http
from django.utils.cache import patch_response_headers

class ForceCanonicalHostnameMiddleware(object):

    def process_request(self, request):
        """Modified common middleware for Conservancy site

        * Performs redirects to strip trailing "index.html"
        * performs redirects based on APPEND_SLASH
        * performs redirects based on site-specific REDIRECT_TABLE
        * adds cache headers to provide hints to squid
        """

        # Check for a redirect based on settings.APPEND_SLASH
        host = http.get_host(request)
        old_url = [host, request.path]
        new_url = old_url[:]
        # Append a slash if append_slash is set and the URL doesn't have a
        # trailing slash or a file extension.
        if settings.APPEND_SLASH and (old_url[1][-1] != '/') and ('.' not in old_url[1].split('/')[-1]):
            new_url[1] = new_url[1] + '/'
            if settings.DEBUG and request.method == 'POST':
                raise RuntimeError, "You called this URL via POST, but the URL doesn't end in a slash and you have APPEND_SLASH set. Django can't redirect to the slash URL while maintaining POST data. Change your form to point to %s%s (note the trailing slash), or set APPEND_SLASH=False in your Django settings." % (new_url[0], new_url[1])
        # Strip trailing index.html
        if new_url[1].endswith('/index.html'):
            new_url[1] = new_url[1][:new_url[1].rfind('index.html')]
        # Consult redirect table (if exists)
        if hasattr(settings, "REDIRECT_TABLE"):
            if settings.REDIRECT_TABLE.has_key(new_url[1]):
                new_url[1] = settings.REDIRECT_TABLE[new_url[1]]
        if new_url != old_url:
            # Force canonical hostname
            if settings.FORCE_CANONICAL_HOSTNAME:
                new_url[0] = settings.FORCE_CANONICAL_HOSTNAME
            # Redirect
            if new_url[0]:
                newurl = "%s://%s%s" % (request.is_secure() and 'https' or 'http', new_url[0], new_url[1])
            else:
                newurl = new_url[1]
            if request.GET:
                newurl += '?' + request.GET.urlencode()
            return http.HttpResponseRedirect(newurl)

        return None

    def process_response(self, request, response):
        # provide hints to squid
        if request.method in ('GET', 'HEAD') and response.status_code == 200:
            patch_response_headers(response)
        return response
