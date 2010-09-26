from django.contrib import admin
from models import EventTag, Event, EventMedia

admin.site.register(EventTag)

class EventAdmin(admin.ModelAdmin):
    list_display = ("title", "date", "date_tentative", "location")
    list_filter = ['date']
    date_hierarchy = 'date'
    search_fields = ["title", "description", "earth_location"]
    prepopulated_fields = {'slug' : ("title",) }

admin.site.register(Event, EventAdmin)

class EventMediaAdmin(admin.ModelAdmin):
    list_display = ("event", "format", "novel")

admin.site.register(EventMedia, EventMediaAdmin)


