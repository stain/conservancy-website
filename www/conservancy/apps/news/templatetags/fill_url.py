import urlparse

from django import template

register = template.Library()

@register.filter(name='fill_url')
def fill_url(given_url, base_url):
    """"Fill out" missing pieces of one URL from another.

    This function parses the given URL, and if it's missing any pieces
    (scheme, netloc, etc.), it fills those in from the base URL.
    Typical usage is "/URL/path"|fill_url:"https://hostname/"
    to generate "https://hostname/URL/path".
    """
    given_parts = urlparse.urlsplit(given_url)
    base_parts = urlparse.urlsplit(base_url)
    return urlparse.urlunsplit(
        given_part or base_part for given_part, base_part in zip(given_parts, base_parts)
    )
