from django.contrib import admin
from solo.admin import SingletonModelAdmin

from admin_helper.admin import AdminHelperAdmin

from core.models.news import News
from core.models.shop import Product, Stock, ProductCategory, Delivery, DeliveryPoint
from core.models.general import SiteConfiguration


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


class ProductCategoryAdmin(AdminHelperAdmin):
    fields = ['id', 'name', ]

    list_display = ('id', 'name',)

    readonly_fields = ('id', )


class ProductAdmin(AdminHelperAdmin):
    fieldsets = [
        ('General settings', {'fields': ['id', 'image_tag', 'image', 'name', 'category', 'price', 'stock', ]}),
    ]

    list_display = ('id', 'name', 'category', 'price', 'is_available')

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


admin.site.register(SiteConfiguration, SingletonModelAdmin)
admin.site.register(News, NewsAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductCategory, ProductCategoryAdmin)
admin.site.register(Stock, StockAdmin)
admin.site.register(Delivery, DeliveryAdmin)
admin.site.register(DeliveryPoint, DeliveryPointAdmin)
