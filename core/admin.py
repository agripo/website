from django.contrib import admin
from django.db.models import Q
from django.utils import timezone
from solo.admin import SingletonModelAdmin

from admin_helper.admin import AdminHelperAdmin

from core.models.news import News
from core.models.shop import Product, Stock, ProductCategory, PastDelivery, FutureDelivery, DeliveryPoint, Delivery
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

    list_display = ('id', 'name', 'category', 'price', 'stock', 'is_available')

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


class BaseDeliveryAdmin(AdminHelperAdmin):
    fields = ['date', 'delivery_point', 'done', 'details']
    list_display = ['id', 'date', 'delivery_point', 'done', 'details']
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
