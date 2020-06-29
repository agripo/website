from django.contrib import admin
from solo.admin import SingletonModelAdmin

from admin_helper.admin import AdminHelperAdmin

# Note: we are renaming the original Admin and Form as we import, as seen in https://gist.github.com/elidickinson/1379652
from django.contrib.flatpages.admin import FlatPageAdmin as FlatPageAdminOld
from django.contrib.flatpages.admin import FlatpageForm as FlatpageFormOld
from django.contrib.flatpages.models import FlatPage
from django import forms
from ckeditor.widgets import CKEditorWidget

from core.models.news import News
from core.models.care import Care
from core.models.partners import Partner
from core.models.shop import Product, Stock, ProductCategory, Delivery, DeliveryPoint
from core.models.general import SiteConfiguration, FlatPageHistory


class NewsAdmin(AdminHelperAdmin):
    fieldsets = [
        ('General settings', {'fields': ['id', 'title', 'is_active', 'icon', 'publication_date']}),
        ('Contents - French', {'fields': ['content', "writer"], 'classes': ('grp-collapse grp-closed',)},),
    ]

    list_display = ('id', 'title', 'is_active', 'publication_date', 'writer')

    list_filter = ['is_active', 'publication_date', 'writer']
    readonly_fields = ('id',)

    class Media:
        css = {
            "all": ("css/icon_selector.css", "css/font-awesome.min.css")
        }
        js = ("js/icon_selector.js",)


class CareAdmin(AdminHelperAdmin):
    fieldsets = [
        ('General settings', {'fields': ['id', 'title', 'is_active', 'icon', 'publication_date']}),
        ('Contents - French', {'fields': ['content', "writer"], 'classes': ('grp-collapse grp-closed',)},),
    ]

    list_display = ('id', 'title', 'is_active', 'publication_date', 'writer')

    list_filter = ['is_active', 'publication_date', 'writer']
    readonly_fields = ('id',)

    class Media:
        css = {
            "all": ("css/icon_selector.css", "css/font-awesome.min.css")
        }
        js = ("js/icon_selector.js",)


class PartnerAdmin(AdminHelperAdmin):
    fields = ['name', 'description', 'logo_tag', 'logo', 'website']

    list_display = ('name', 'website')

    readonly_fields = ('logo_tag',)


class ProductCategoryAdmin(AdminHelperAdmin):
    fields = ['id', 'name', ]

    list_display = ('id', 'name',)

    readonly_fields = ('id', )


class ProductAdmin(AdminHelperAdmin):
    fieldsets = [
        ('Informations générales', {'fields': [
            'id', 'image_tag', 'image', 'name', 'category', 'price',]}),
        ('Informations supplémentaires', {'fields': [
            'scientific_name', 'quantity_type', 'description', 'stock', ]}),
    ]

    list_display = ('id', 'name', 'scientific_name', 'category', 'price', 'is_available')

    list_filter = ['category', ]
    readonly_fields = ('id', 'stock', 'image_tag',)


class StockAdmin(AdminHelperAdmin):
    fields = [
        'product', 'farmer', 'stock',
    ]

    list_display = ('product', 'farmer', 'stock')

    list_filter = ['farmer', 'product', ]


class DeliveryPointAdmin(AdminHelperAdmin):
    fields = ['name', 'description', ]
    list_display = ['id', 'name']


class DeliveryAdmin(AdminHelperAdmin):
    fields = ['date', 'delivery_point', 'done', 'details']
    list_display = ['id', 'date', 'delivery_point', 'done', 'details']
    readonly_fields = ['details']
    list_filter = ['delivery_point', 'date', 'done']
    ordering = ['-date']

    def details(self, obj):
        link, count = obj.details_link()
        if link:
            return '<a href="{}">Préparer la livraison des {} commandes</a>'.format(link, count)

        return "Aucune commande pour cette livraison"
    details.allow_tags = True


class FlatPageHistoryAdmin(admin.ModelAdmin):
    readonly_fields = ('url', 'mtime', 'title', 'content')
    list_display = ('url', 'mtime', 'title')


class FlatpageForm(FlatpageFormOld):
    content = forms.CharField(widget=CKEditorWidget(config_name='awesome_ckeditor'))

    class Meta:
        model = FlatPage  # this is not automatically inherited from FlatpageFormOld
        fields = '__all__'


class FlatPageAdmin(FlatPageAdminOld):
    form = FlatpageForm

    def save_model(self, request, obj, form, change):
        """save a copy of the Flatpage to OldPage"""
        FlatPageHistory.create_entry(obj)
        obj.save()


admin.site.unregister(FlatPage)
admin.site.register(FlatPage, FlatPageAdmin)


admin.site.register(FlatPageHistory, FlatPageHistoryAdmin)
admin.site.register(SiteConfiguration, SingletonModelAdmin)
admin.site.register(Partner, PartnerAdmin)
admin.site.register(News, NewsAdmin)
admin.site.register(Care, CareAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductCategory, ProductCategoryAdmin)
admin.site.register(Stock, StockAdmin)
admin.site.register(Delivery, DeliveryAdmin)
admin.site.register(DeliveryPoint, DeliveryPointAdmin)
