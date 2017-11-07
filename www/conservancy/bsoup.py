# -*- encoding: utf-8 -*-

import io
import re

import bs4
import bs4.element

class BeautifulSoup(bs4.BeautifulSoup):
    """A wrapper of the original BeautifulSoup class, with convenience methods added."""

    IMAGE_ATTRS = {
        'img': 'src',
        'video': 'poster',
    }
    NON_BODY_TEXT_TAGS = frozenset([
        'img',
        'video',
    ])
    SENTENCE_END = re.compile(r'[.?!]\s*\W*\s*$')

    def __init__(self, src, parser='html5lib'):
        # WARNING!  It seems like it would be ideal to use the 'lxml' parser
        # for speed, but that doesn't work in our web application.  On
        # Debian stretch, at least, using lxml causes the web server WSGI
        # application to go into an infinite loop.
        super(BeautifulSoup, self).__init__(src, parser)

    def _body_text(self, root):
        # "Body text" is all the strings under the root element, in order,
        # except:
        # * strings inside NON_BODY_TEXT_TAGS
        # * strings inside containers of NON_BODY_TEXT_TAGS.  A container is
        #   an element that has a NON_BODY_TEXT_TAGS element as its first child.
        #   For example, in <div> <video …> … </div>, none of the div's strings
        #   are included in the body text, because it's considered to be a
        #   <video> container, and any strings are probably a caption, fallback
        #   text, or other non-body text.
        started = False
        for child in root.children:
            child_type = type(child)
            if issubclass(child_type, bs4.element.Tag):
                if child.name in self.NON_BODY_TEXT_TAGS:
                    if not started:
                        break
                else:
                    for s in self._body_text(child):
                        yield s
            # It's not worth it to use issubclass here, because elements that
            # don't have body text like Comments and CDATA are subclasses of
            # NavigableString.
            elif child_type is bs4.element.NavigableString:
                if started:
                    yield child
                elif child.isspace():
                    pass
                else:
                    yield child
                    started = True

    def body_text(self):
        """Return an iterator of strings comprising this document's body text."""
        return self._body_text(self)

    def some_body_text(self, char_target=300):
        """Return an iterator of strings with some of this document's body text.

        This is the same as body_text, except after it yields a string that
        looks like the end of a sentence, it checks whether it has yielded
        at least `char_target` characters.  If so, the iterator stops.
        """
        # This implementation is likely to overshoot `char_target` a lot,
        # because it doesn't look inside the strings it yields, just at the
        # end of them.  We can implement something smarter later if needed.
        char_count = 0
        for s in self.body_text():
            yield s
            char_count += len(s)
            if (char_count > char_target) and self.SENTENCE_END.search(s):
                break

    @staticmethod
    def is_video_source(elem):
        try:
            return elem.name == 'source' and elem.parent.name == 'video'
        except AttributeError:
            return False

    def iter_attr(self, tag, attr_name, **kwargs):
        kwargs[attr_name] = True
        for elem in self.find_all(tag, **kwargs):
            yield elem[attr_name]

    def iter_image_urls(self):
        """Return an iterator of source URL strings of all images in this document.

        Images include <img> tags and <video> poster attributes.
        """
        for elem in self.find_all(list(self.IMAGE_ATTRS.keys())):
            try:
                yield elem[self.IMAGE_ATTRS[elem.name]]
            except KeyError:
                pass

    def iter_video_urls(self):
        """Return an iterator of source URL strings of all videos in this document."""
        return self.iter_attr(self.is_video_source, 'src')


class SoupModelMixin:
    """Mixin for models to parse HTML with BeautifulSoup.

    Classes that use this mixin must define `SOUP_ATTRS`, a list of strings
    that name attributes with HTML in them.  After that, all the public methods
    are usable.
    """

    SOUP_ATTRS = []

    def _get_soup(self):
        try:
            return self._soup
        except AttributeError:
            html = io.StringIO()
            for attr_name in self.SOUP_ATTRS:
                html.write(getattr(self, attr_name))
            html.seek(0)
            self._soup = BeautifulSoup(html)
            return self._soup

    def get_description(self):
        """Return a string with a brief excerpt of body text from the HTML."""
        return u''.join(self._get_soup().some_body_text())

    def get_image_urls(self):
        """Return an iterator of source URL strings of all images in the HTML.

        Images include <img> tags and <video> poster attributes.
        """
        return self._get_soup().iter_image_urls()

    def get_video_urls(self):
        """Return an iterator of source URL strings of all videos in the HTML."""
        return self._get_soup().iter_video_urls()
