from django.contrib import admin
from conservancy.apps.summit_registration.models import SummitRegistration

class SummitRegistrationAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'affiliation', 'cle_credit')

admin.site.register(SummitRegistration, SummitRegistrationAdmin)

