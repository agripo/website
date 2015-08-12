from django.contrib import admin
from core.models import News, AgripoUser

class NewsAdmin(admin.ModelAdmin):
    fieldsets = [
        ('General settings', {'fields': ['id', 'title', 'is_active', 'publication_date']}),
        ('Contents - French', {'fields': ['content', "writer"], 'classes': ('grp-collapse grp-closed',)},),
    ]

    list_display = ('__str__', 'is_active', 'publication_date', 'writer')

    list_filter = ['is_active', 'publication_date', 'writer']
    readonly_fields = ('id',)


admin.site.register(News, NewsAdmin)
