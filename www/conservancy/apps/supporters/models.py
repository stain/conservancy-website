from django.db import models

class Supporter(models.Model):
    """Conservancy Supporter listing"""

    display_name = models.CharField(max_length=200, blank=False)
    display_until_date = models.DateTimeField("date until which this supporter name is displayed")
    ledger_entity_id = models.CharField(max_length=200, blank=False)

    def test(self):
        return "TESTING"
    def __unicode__(self):
        return self.display_name

    class Meta:
        ordering = ('ledger_entity_id',)
