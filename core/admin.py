from django.contrib import admin
from core.models import News, Product, Stock, ProductCategory, Delivery, DeliveryPoint
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


class ProductCategoryAdmin(admin.ModelAdmin):
    fields = ['id', 'name', ]

    list_display = ('__str__', )

    readonly_fields = ('id', )


class ProductAdmin(admin.ModelAdmin):
    fieldsets = [
        ('General settings', {'fields': ['id', 'image_tag', 'image', 'name', 'category', 'price', 'stock', ]}),
    ]

    list_display = ('__str__', 'category', 'price', 'stock', 'is_available')

    list_filter = ['category',]
    readonly_fields = ('id', 'stock', 'image_tag',)


class StockAdmin(admin.ModelAdmin):
    fields = [
        'product', 'farmer', 'stock',
    ]

    list_display = ('product', 'farmer', 'stock')

    list_filter = ['farmer', 'product', ]


class DeliveryPointAdmin(admin.ModelAdmin):
    fields = ['name', 'description', ]


class DeliveryAdmin(admin.ModelAdmin):
    fields = ['date', 'delivery_point']
    list_display = ['date', 'delivery_point']
    list_filter = ['date']



admin.site.register(SiteConfiguration, SingletonModelAdmin)
admin.site.register(News, NewsAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductCategory, ProductCategoryAdmin)
admin.site.register(Stock, StockAdmin)
admin.site.register(Delivery, DeliveryAdmin)
admin.site.register(DeliveryPoint, DeliveryPointAdmin)
