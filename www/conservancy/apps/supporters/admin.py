from django.contrib import admin
from conservancy.apps.supporters.models import Supporter

class SupporterAdmin(admin.ModelAdmin):
    list_display = ('display_name', 'display_until_date')

admin.site.register(Supporter, SupporterAdmin)
