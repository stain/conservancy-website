from django.db import models

class SummitRegistration(models.Model):
    """Form fields for summit registrants"""

    name = models.CharField(max_length=300)
    affiliation = models.CharField(max_length=700, blank=True)
    address = models.TextField(blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=100, blank=True)
    date_created = models.DateField(auto_now_add=True)
    cle_credit = models.BooleanField(default=True)

    class Meta:
        ordering = ('name',)

