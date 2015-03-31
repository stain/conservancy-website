from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Rss201rev2Feed 
from conservancy.apps.news.models import PressRelease
from conservancy.apps.blog.models import Entry as BlogEntry

from django.shortcuts import render_to_response
from django.conf import settings
from datetime import datetime

import itertools
import operator

class ConservancyFeedBase(Feed):
    def copyright_holder(self): return "Software Freedom Conservancy"

    def license_no_html(self): return "Licensed under the Creative Commons Attribution-ShareAlike 3.0 Unported License."

    def item_copyright(self, item):
        year = 2008
        for attr in ('pub_date', 'date_created', 'date_last_modified'):
            if hasattr(item, attr):
                if hasattr(getattr(item, attr), 'year'):
                    year = getattr(getattr(item, attr), 'year')
                    break
        return 'Copyright (C) %d, %s.  %s' % (year, self.copyright_holder(), self.license_no_html())

    def item_extra_kwargs(self, item):
        year = 2008
        for attr in ('pub_date', 'date_created', 'date_last_modified'):
            if hasattr(item, attr):
                if hasattr(getattr(item, attr), 'year'):
                    year = getattr(getattr(item, attr), 'year')
                    break
        return { 'year' : year }

class PressReleaseFeed(Feed):
    get_absolute_url = '/feeds/news/'
    title = "Software Freedom Conservancy News"
    link = "/news/"
    description = ""

    def items(self):
        return PressRelease.objects.filter(pub_date__lte=datetime.now(),
                                           sites__id__exact=settings.SITE_ID).order_by('-pub_date')[:10]
    def item_title(self, item):
        return item.headline

    def item_description(self, item):
        return item.summary

    def item_pubdate(self, item):
        return item.pub_date

class OmnibusFeedType(Rss201rev2Feed):
    def root_attributes(self):
        attrs = super(OmnibusFeedType, self).root_attributes()
        attrs['xmlns:itunes'] = 'http://www.itunes.com/dtds/podcast-1.0.dtd'
        attrs['xmlns:atom'] = 'http://www.w3.org/2005/Atom'
        attrs['xmlns:media'] = 'http://search.yahoo.com/mrss/'
        attrs['xmlns:dc'] = "http://purl.org/dc/elements/1.1/"
        return attrs

    def add_root_elements(self, handler):
        super(OmnibusFeedType, self).add_root_elements(handler)

    def add_item_elements(self, handler, item):
        super(OmnibusFeedType, self).add_item_elements(handler, item)
        # Block things that don't have an enclosure from iTunes in
        # case someone uploads this feed there.
        handler.addQuickElement("itunes:block", 'Yes')

class OmnibusFeed(ConservancyFeedBase):
    get_absolute_url = '/feeds/omnibus/'
    feed_type = OmnibusFeedType
    link ="/news/"
    title = "The Software Freedom Conservancy"
    description = "An aggregated feed of all RSS content available from the Software Freedom Conservancy, including both news items and blogs."
    title_template = "feeds/omnibus_title.html"
    description_template = "feeds/omnibus_description.html"
    author_email = "info@sfconservancy.org"
    author_link = "https://sfconservancy.org/"
    author_name = "Software Freedom Conservancy"

    def item_title(self, item):
        return item.headline

    def item_description(self, item):
        return item.summary

    def item_enclosure_mime_type(self): return "audio/mpeg"

    def item_enclosure_url(self, item):
        if hasattr(item, 'mp3_path'):
            return "https://sfconservancy.org" + item.mp3_path
    def item_enclosure_length(self, item):
        if hasattr(item, 'mp3_path'):
            return item.mp3_length

    def item_pubdate(self, item):
        return item.pub_date

    def item_author_name(self, item):
        if item.omnibus_type == "blog":
            return item.author.formal_name
        else:
            return "Software Freedom Conservancy"

    def item_author_link(self, obj):
        return "https://sfconservancy.org"

    def item_author_email(self, item):
        if item.omnibus_type == "news":
            return "info@sfconservancy.org"
        elif hasattr(item, 'author'):
            return "%s@sfconservancy.org" % item.author
        else:
            return "info@sfconservancy.org"

    def item_pubdate(self, item):
        if item.omnibus_type == "event":
            return item.date_created
        else:
            return item.pub_date

    def item_link(self, item):
        return item.get_absolute_url()

# http://groups.google.ca/group/django-users/browse_thread/thread/d22e8a8f378cf0e2

    def items(self):
        blogs = BlogEntry.objects.filter(pub_date__lte=datetime.now()).order_by('-pub_date')[:25]
        for bb in blogs:
            bb.omnibus_type = "blog"
            bb.omnibus_feed_description_template = "feeds/blog_description.html"
            bb.omnibus_feed_title_template = "feeds/blog_title.html"

        news = PressRelease.objects.filter(pub_date__lte=datetime.now(),
                                           sites__id__exact=settings.SITE_ID).order_by('-pub_date')[:25]
        for nn in news:
            nn.omnibus_type = "news"
            nn.omnibus_feed_description_template = "feeds/news_description.html"
            nn.omnibus_feed_title_template = "feeds/news_title.html"

        a  = [ ii for ii in itertools.chain(blogs, news)]
        a.sort(key=operator.attrgetter('pub_date'), reverse=True)
        return a


    def item_extra_kwargs(self, item):
        return super(OmnibusFeed, self).item_extra_kwargs(item)

class BlogFeed(ConservancyFeedBase):
    link = "/blog/"
    get_absolute_url = '/feeds/blog/'

    def get_object(self, request):
        return request

    def title(self, obj):
        answer = "The Software Freedom Conservancy Blog"

        GET = obj.GET
        tags = []
        if 'author' in GET:
            tags = GET.getlist('author')
        if 'tag' in GET:
            tags += GET.getlist('tag')

        if len(tags) == 1:
            answer += " (" + tags[0] + ")"
        elif len(tags) > 1:
            firstTime = True
            done = {}
            for tag in tags:
                if done.has_key(tag): continue
                if firstTime:
                    answer += " ("
                    firstTime = False
                else:
                    answer += ", "
                answer += tag
                done[tag] = tag
            answer += ")"
        else:
            answer += "."
        return answer
        
    def description(self, obj):
        answer = "Blogs at the Software Freedom Conservancy"

        GET = obj.GET
        tags = []
        if 'author' in GET: tags = GET.getlist('author')
        if 'tag' in GET:    tags += GET.getlist('tag')

        done = {}
        if len(tags) == 1:
            answer += " tagged with " + tags[0]
        elif len(tags) > 1:
            firstTime = True
            for tag in tags:
                if done.has_key(tag): continue
                if firstTime:
                    answer += " tagged with "
                    firstTime = False
                else:
                    answer += " or "
                answer += tag
                done[tag] = tag
        else:
            answer = "All blogs at the Software Freedom Conservancy"
        answer += "."

        return answer
        
    def item_title(self, item):
        return item.headline

    def item_description(self, item):
        return item.summary

    def item_author_name(self, item):
        return item.author.formal_name

    def item_author_email(self, item):
        return "%s@sfconservancy.org" % item.author

    def item_pubdate(self, item):
        return item.pub_date

    def items(self, obj):
        GET = obj.GET

        def OR_filter(field_name, subfield_name, objs):
            from django.db.models import Q
            return reduce(lambda x, y: x | y,
                          [Q(**{'%s__%s' % (field_name, subfield_name): x})
                           for x in objs])

        queryset = BlogEntry.objects.filter(pub_date__lte=datetime.now())

        if 'author' in GET:
            authors = GET.getlist('author')
            queryset = queryset.filter(OR_filter('author', 'username', authors))

        if 'tag' in GET:
            tags = GET.getlist('tag')
            queryset = queryset.filter(OR_filter('tags', 'slug', tags))

        return queryset.order_by('-pub_date')[:10]


def view(request):
    """Listing of all available feeds
    """

    feeds = (PressReleaseFeed, BlogFeed, OmnibusFeed)
    return render_to_response("feeds.html", {'feeds': feeds})
