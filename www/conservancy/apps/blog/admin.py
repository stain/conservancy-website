from django.contrib import admin
from conservancy.apps.blog.models import EntryTag, Entry

class EntryTagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('label',)}

admin.site.register(EntryTag, EntryTagAdmin)

class EntryAdmin(admin.ModelAdmin):
    list_display = ('pub_date', 'headline', 'author')
    list_filter = ['pub_date']
    date_hierarchy = 'pub_date'
    search_fields = ['headline', 'summary', 'body']
    prepopulated_fields = {'slug': ("headline",)}
    filter_horizontal = ('tags',)


admin.site.register(Entry, EntryAdmin)
