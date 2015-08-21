from django.contrib import admin
from core.models import News, AgripoUser
from solo.admin import SingletonModelAdmin
from core.models import SiteConfiguration


class NewsAdmin(admin.ModelAdmin):
    fieldsets = [
        ('General settings', {'fields': ['id', 'title', 'is_active', 'icon', 'publication_date']}),
        ('Contents - French', {'fields': ['content', "writer"], 'classes': ('grp-collapse grp-closed',)},),
    ]

    list_display = ('__str__', 'is_active', 'publication_date', 'writer')

    list_filter = ['is_active', 'publication_date', 'writer']
    readonly_fields = ('id',)

    class Media:
        css = {
            "all": ("css/icon_selector.css", "css/font-awesome.min.css")
        }
        js = ("js/icon_selector.js",)


admin.site.register(SiteConfiguration, SingletonModelAdmin)
admin.site.register(News, NewsAdmin)
