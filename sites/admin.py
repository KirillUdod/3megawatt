from django.contrib import admin
from .models import Site

# Register your models here.


class SiteAdmin(admin.ModelAdmin):
    list_display = (u'name', u'date', u'a_value', u'b_value')


admin.site.register(Site, SiteAdmin)