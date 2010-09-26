from django.contrib import admin
from models import ContactEntry

class ContactEntryAdmin(admin.ModelAdmin):
    list_display = ('email', 'subscribe_sflc', 'subscribe_sfc')


admin.site.register(ContactEntry, ContactEntryAdmin)
