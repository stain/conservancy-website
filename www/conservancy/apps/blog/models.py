from django.db import models
from django.conf import settings
from conservancy import bsoup
from conservancy.apps.staff.models import Person
from datetime import datetime, timedelta

class EntryTag(models.Model):
    """Tagging for blog entries"""

    label = models.CharField(max_length=100)
    slug = models.SlugField()

    class Meta:
        db_table = 'techblog_entrytag' # legacy

    def __unicode__(self):
        return self.label

    def get_absolute_url(self):
        return u"/blog/?tag=%s" % self.slug

class Entry(models.Model, bsoup.SoupModelMixin):
    """Blog entry"""

    headline = models.CharField(max_length=200)
    slug = models.SlugField(unique_for_date='pub_date')
    summary = models.TextField(help_text="Use raw HTML.  Unlike in the press release model, this summary is not included at the beginning of the body when the entry is displayed.")
    body = models.TextField(help_text="Use raw HTML.  Include the full body of the post.")
    pub_date = models.DateTimeField()
    author = models.ForeignKey(Person)
    tags = models.ManyToManyField(EntryTag, null=True, blank=True)

    date_created = models.DateTimeField(auto_now_add=True)
    date_last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'techblog_entries' # legacy
        verbose_name_plural = 'entries'
        ordering = ('-pub_date',)
        get_latest_by = 'pub_date'

    SOUP_ATTRS = ['body']

    def __unicode__(self):
        return self.headline

    def get_absolute_url(self):
        return (u"/blog/%s/%s/"
                % (self.pub_date.strftime("%Y/%b/%d").lower(),
                   self.slug))

    def is_recent(self):
        return self.pub_date > (datetime.now() - timedelta(days=30))
        # question: does datetime.now() do a syscall each time is it called?

    # Ping google blogs and technorati.  Taken from
    # http://blog.foozia.com/blog/2007/apr/21/ping-technorati-your-django-blog-using-xml-rpc/
    def save(self):
        if settings.CONSERVANCY_DEVEL or True: # "or True" means it is disabled always
            super(Entry, self).save()
            return

        blog_name = 'Software Freedom Law Center Blog'
        blog_url =  'http://www.softwarefreedom.org/blog/'
        post_url = ('http://www.softwarefreedom.org'
                    + self.get_absolute_url())

        import xmlrpclib

        # Ping Technorati
        j = xmlrpclib.Server('http://rpc.technorati.com/rpc/ping')
        reply = j.weblogUpdates.ping(blog_name, blog_url)

        # Ping Google Blog Search
        j = xmlrpclib.Server('http://blogsearch.google.com/ping/RPC2')
        reply = j.weblogUpdates.ping(blog_name, blog_url, post_url)

        # Call any superclass's method
        super(Entry, self).save()
