from django.db import models

class ContactEntry(models.Model):
    """Conservancy contact system

    Hopefully this will be deprecated soon"""

    email = models.EmailField() # should make it unique, but we really cannot
    subscribe_conservancy = models.BooleanField(default=False)

    class Meta:
        ordering = ('email',)

