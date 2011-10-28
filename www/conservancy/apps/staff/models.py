from django.db import models

class Person(models.Model):
    """Staff members

    Referenced from other models (blog, events, etc)
    """

    username = models.CharField(max_length=20)
    formal_name = models.CharField(max_length=200)
    casual_name = models.CharField(max_length=200)
#    title = models.CharField(max_length=200, blank=True)
#    biography = models.TextField(blank=True)
#    phone = models.CharField(max_length=30, blank=True)
#    gpg_key = models.TextField(blank=True)
#    gpg_fingerprint = models.CharField(max_length=100, blank=True)
    currently_employed = models.BooleanField(default=True)

    date_created = models.DateTimeField(auto_now_add=True)
    date_last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'people'

    def __unicode__(self):
        return self.username

    def biography_url(self):
        return u"/about/#%s" % self.username

