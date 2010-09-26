from django.contrib import admin
from models import PodcastTag, Podcast

class PodcastTagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('label',)}

admin.site.register(PodcastTag, PodcastTagAdmin)

class PodcastAdmin(admin.ModelAdmin):
    list_display = ('pub_date', 'title')
    list_filter = ['pub_date']
    date_hierarchy = 'pub_date'
    search_fields = ['title', 'summary', 'body']
    prepopulated_fields = {'slug': ("title",)}
    filter_horizontal = ('tags',)


admin.site.register(Podcast, PodcastAdmin)
