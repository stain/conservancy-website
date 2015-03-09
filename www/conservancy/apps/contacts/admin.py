from django.contrib import admin
from conservancy.apps.contacts.models import ContactEntry

class ContactEntryAdmin(admin.ModelAdmin):
    list_display = ('email', 'subscribe_conservancy')


admin.site.register(ContactEntry, ContactEntryAdmin)
