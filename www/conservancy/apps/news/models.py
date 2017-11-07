from django.db import models
from django.conf import settings
from conservancy import bsoup
from conservancy.apps.staff.models import Person
from conservancy.apps.events.models import Event
from django.contrib.sites.models import Site
from datetime import datetime, timedelta

class PressRelease(models.Model, bsoup.SoupModelMixin):
    """News release model"""

    headline = models.CharField(max_length=300)
    subhead = models.CharField(max_length=300, blank=True)
    slug = models.SlugField(unique_for_date="pub_date",
                            help_text=("automatically built from headline"))
    summary = models.TextField(help_text="First paragraph (raw HTML)")
    body = models.TextField(help_text="Remainder of post (raw HTML)",
                            blank=True)
    pub_date = models.DateTimeField("date [to be] published")
    sites = models.ManyToManyField(Site)

    date_last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-pub_date",)
        get_latest_by = "pub_date"

    SOUP_ATTRS = ['summary', 'body']

    def __unicode__(self):
        return self.headline

    def get_absolute_url(self):
        return u"/news/%s/%s/" % (self.pub_date.strftime("%Y/%b/%d").lower(),
                                  self.slug)

    def is_recent(self):
        return self.pub_date > (datetime.now() - timedelta(days=5))
        # question: does datetime.now() do a syscall each time is it called?

    def is_in_past_month(self):
        # This function is deprecated.  Use the date_within template
        # filter instead (example in conservancy/templates/frontpage.html)
        return self.pub_date > (datetime.now() - timedelta(days=30))

    def save(self):
        if settings.CONSERVANCY_DEVEL or True:
            super(PressRelease, self).save()
            return

        blog_name = 'Software Freedom Law Center News'
        blog_url =  'http://www.softwarefreedom.org/news/'
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
        super(PressRelease, self).save()

class ExternalArticleTag(models.Model):
    """A way to tag external articles"""

    label = models.CharField(max_length=100)

    date_created = models.DateField(auto_now_add=True)

    def __unicode__(self):
        return self.label

class PublicExternalArticleManager(models.Manager):
    def get_queryset(self):
        return super(PublicExternalArticleManager, self).get_queryset().filter(visible=True)

class ExternalArticle(models.Model):
    """A system for displaying Conservancy news mentions on the site.

    (Currently unused)
    """

    title = models.CharField(max_length=400)
    info = models.CharField(help_text="subscribers only? audio? pdf warning?",
                            blank=True, max_length=300)
    publication = models.CharField("source of article", max_length=300)
    # verify_exists removed https://docs.djangoproject.com/en/1.7/releases/1.4/
    url = models.URLField(blank=True)
    date = models.DateField()
    visible = models.BooleanField(help_text="Whether to display on website", default=True)

    tags = models.ManyToManyField(ExternalArticleTag, null=True, blank=True)
    people = models.ManyToManyField(Person, null=True, blank=True)
    event = models.ForeignKey(Event, null=True, blank=True)
    press_release = models.ForeignKey(PressRelease, null=True, blank=True)

    date_created = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ("-date_created",)
        get_latest_by = "date_created"

    def __unicode__(self):
        return u"%s (%s)" % (self.title, self.publication)

    objects = models.Manager()
    public = PublicExternalArticleManager()

