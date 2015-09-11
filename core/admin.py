from django.contrib import admin
from django.db.models import Q
from django.utils import timezone
from solo.admin import SingletonModelAdmin

from core.models.news import News
from core.models.shop import Product, Stock, ProductCategory, PastDelivery, FutureDelivery, DeliveryPoint, Delivery
from core.models.general import SiteConfiguration


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

    list_filter = ['category', ]
    readonly_fields = ('id', 'stock', 'image_tag',)


class StockAdmin(admin.ModelAdmin):
    fields = [
        'product', 'farmer', 'stock',
    ]

    list_display = ('product', 'farmer', 'stock_setter')

    list_filter = ['farmer', 'product', ]


class DeliveryPointAdmin(admin.ModelAdmin):
    fields = ['name', 'description', ]


class BaseDeliveryAdmin(admin.ModelAdmin):
    fields = ['date', 'delivery_point', 'done', 'details']
    list_display = ['__str__', 'done_setter', 'details']
    readonly_fields = ['details']
    list_filter = ['delivery_point', 'done']
    ordering = ['-date']

    def details(self, obj):
        count = obj.commands.count()
        if count > 0:
            return '<a href="{}">Préparer la livraison des {} commandes</a>'.format(
                Delivery.details_link(pk=obj.pk), count)

        return "Aucune commande pour cette livraison"
    details.allow_tags = True


class PastDeliveryAdmin(BaseDeliveryAdmin):

    def get_queryset(self, request):
        return super().get_queryset(request).filter(Q(date__lte=timezone.now) | Q(done=True))


class FutureDeliveryAdmin(BaseDeliveryAdmin):
    ordering = ['date']

    def get_queryset(self, request):
        return super().get_queryset(request).filter(date__gte=timezone.now, done=False)


admin.site.register(SiteConfiguration, SingletonModelAdmin)
admin.site.register(News, NewsAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductCategory, ProductCategoryAdmin)
admin.site.register(Stock, StockAdmin)
admin.site.register(PastDelivery, PastDeliveryAdmin)
admin.site.register(FutureDelivery, FutureDeliveryAdmin)
admin.site.register(DeliveryPoint, DeliveryPointAdmin)
