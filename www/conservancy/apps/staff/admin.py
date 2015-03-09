from django.contrib import admin
from conservancy.apps.staff.models import Person

class PersonAdmin(admin.ModelAdmin):
    list_display = ("username", "formal_name", "casual_name",
                    "currently_employed")
    list_filter = ["currently_employed"]

admin.site.register(Person, PersonAdmin)
