from django.db import models

class EarthLocation(models.Model):
    """Represents latitude and longitude, with a label"""

    label = models.CharField(max_length=300, unique=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    date_created = models.DateTimeField(auto_now_add=True)
    date_last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (("latitude", "longitude"),)

    def __unicode__(self):
        return self.label

    def google_maps_link(self):
        return ("http://maps.google.com/maps?ll=%s,%s&z=15"
                % (self.latitude, self.longitude))

    default_map_link = google_maps_link

    def html_map_link(self): # for Admin, fixme: fix_ampersands
        return '<a href="%s">map link</a>' % self.default_map_link()
    html_map_link.allow_tags = True

