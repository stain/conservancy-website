from django.contrib import admin
from conservancy.apps.news.models import PressRelease, ExternalArticleTag, ExternalArticle

class PressReleaseAdmin(admin.ModelAdmin):
    list_display = ("headline", "pub_date")
    list_filter = ['pub_date']
    date_hierarchy = 'pub_date'
    search_fields = ['headline', 'summary', 'body']
    prepopulated_fields = { 'slug' : ("headline",), }

admin.site.register(PressRelease, PressReleaseAdmin)
admin.site.register(ExternalArticleTag)

class ExternalArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "publication", "visible", "date")
    list_filter = ['date']
    date_hierarchy = 'date'
    search_fields = ["title", "info", "publication"]

admin.site.register(ExternalArticle, ExternalArticleAdmin)



