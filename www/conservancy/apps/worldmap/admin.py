from django.contrib import admin
from conservancy.apps.worldmap.models import EarthLocation

class EarthLocationAdmin(admin.ModelAdmin):
    list_display = ("label", "html_map_link")

admin.site.register(EarthLocation, EarthLocationAdmin)
