from django.contrib import admin
from urlshort.models import Urls

# Register your models here.
class UrlsAdmin(admin.ModelAdmin):
    list_display = ('short_id','given_URL','published_date', 'count')
    ordering = ('-published_date',)
 
admin.site.register(Urls, UrlsAdmin) 