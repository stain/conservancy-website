from django.db import models

class ContactEntry(models.Model):
    """SFLC contact system

    Hopefully this will be deprecated soon"""

    email = models.EmailField() # should make it unique, but we really cannot
    subscribe_sflc = models.BooleanField()
    subscribe_sfc = models.BooleanField()

    class Meta:
        ordering = ('email',)

