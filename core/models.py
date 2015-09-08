import re
from core.exceptions import AddedMoreToCartThanAvailable, CantSetCartQuantityOnUnsavedProduct
from django.conf import settings
from django.db import models, IntegrityError
from django.contrib.auth.models import User, Group
from django.db.models import Q
from django.core.exceptions import ValidationError
from django.utils import timezone
from solo.models import SingletonModel
from ckeditor.fields import RichTextField
from django.contrib.sessions.backends.db import SessionStore

from core.icons import UNUSED_ICON


SITECONF_DEFAULT_NEWS_COUNT = 9
session = SessionStore()


class SiteConfiguration(SingletonModel):
    site_title = models.CharField(max_length=255, default='Site title', verbose_name='Titre du site', help_text="Titre du site (dans l'onglet du navigateur)")
    news_count = models.IntegerField(default=SITECONF_DEFAULT_NEWS_COUNT, verbose_name='Actualités', help_text="Nombre de news dans la liste des news")
    homepage_content = RichTextField(config_name='awesome_ckeditor', verbose_name='Page d\'accueil', help_text="Contenu de la page d'accueil")

    def __str__(self):
        return "Configuration générale"

    class Meta:
        verbose_name = "Configuration générale"


class AgripoUser(User):

    def is_farmer(self):
        return self.groups.filter(name="farmers").exists()

    def add_to_farmers(self):
        if not self.email:
            raise IntegrityError("The farmers must have a valid email set in their account")
        self.groups.add(Group.objects.get(name="farmers"))
        self.save()
        return self

    def is_manager(self):
        return self.is_staff

    def add_to_managers(self):
        self.is_staff = True
        self.save()
        self.groups.add(Group.objects.get(name="managers"))
        return self

    def is_admin(self):
        return self.is_superuser

    def add_to_admins(self):
        self.is_superuser = True
        self.save()
        return self

    class Meta:
        proxy = True


class Icon(models.Model):
    icon = models.CharField(max_length=28, unique=True)

    def __str__(self):
        return 'Icon {}'.format(self.icon)


def all_but_forbidden_icon():
    return ~models.Q(icon=UNUSED_ICON)


def get_comment_icon_id():
    return Icon.objects.get(icon="comment").pk


class ProductCategory(models.Model):
    name = models.CharField(max_length=28, blank=False, null=False, unique=True)

    def clean(self):
        if self.name == '':
            raise ValidationError('Empty category name')

    def __str__(self):
        return "{} : {}".format(self.id, self.name)

    class Meta:
        verbose_name = "Catégorie de produits"
        verbose_name_plural = "Catégories de produits"


class Product(models.Model):
    name = models.CharField(
        max_length=28, blank=False, null=False, unique=True,verbose_name="Nom",
        help_text="Nom affiché dans les fiches produits")
    category = models.ForeignKey(
        ProductCategory, blank=False, null=False, verbose_name="Catégorie",
        help_text="Catégorie sous laquelle apparaît ce produit.")
    price = models.PositiveIntegerField(verbose_name="Prix unitaire", default=0, blank=False, null=False)
    image = models.ImageField(
        upload_to='products', blank=True, null=True, default="default/not_found.jpg", verbose_name="Image",
        help_text="Cette image représente le produit.<br />"
                  "Elle doit faire 150x150px. "
                  "Si la largeur est différente de la hauteur, l'image apparaitra déformée."
    )
    farmers = models.ManyToManyField(AgripoUser, through="Stock")
    stock = models.PositiveIntegerField(
        default=0,
        help_text="Champ alimenté automatiquement en fonction des déclarations des fermiers.")
    bought = models.PositiveIntegerField(
        default=0,
        help_text="Champ alimenté automatiquement en fonction des commandes passées")

    def __str__(self):
        return "{} : {}".format(self.id, self.name)

    def clean(self):
        if self.name == '':
            raise ValidationError('Empty product name')

        if self.price <= 0:
            raise ValidationError('Price should be bigger than zero')

    def image_tag(self):
        return u'<img src="{}" style="width:150px;height:140px;"/>'.format(settings.MEDIA_URL + str(self.image))

    image_tag.short_description = 'Miniature'
    image_tag.allow_tags = True

    def set_cart_quantity(self, quantity):
        if not self.id:
            raise CantSetCartQuantityOnUnsavedProduct

        if quantity > self.available_stock():
            raise AddedMoreToCartThanAvailable

        if quantity == 0:
            del session[self._get_session_key()]
        else:
            session[self._get_session_key()] = quantity

        return self

    def get_cart_quantity(self):
        if self._get_session_key() in session:
            return session[self._get_session_key()]
        return 0

    def buy(self, quantity):
        if self.available_stock() < quantity:
            raise AddedMoreToCartThanAvailable()

        self.bought += quantity
        self.save()
        return self

    def available_stock(self):
        return self.stock - self.bought

    def is_available(self):
        return self.available_stock() > 0

    is_available.__name__ = "Disponible"
    is_available.boolean = True

    def _get_session_key(self):
        return Product.static_get_session_key(self.pk)

    @staticmethod
    def static_get_session_key(product_id):
        return "product_{}_quantity".format(product_id)

    @staticmethod
    def static_get_cart_products():
        pattern = re.compile("^{}$".format(Product.static_get_session_key("([0-9]+)")))
        ret = []
        for element in sorted(session.keys()):
            match = pattern.search(element)
            if match:
                ret.append(dict(
                    id=int(match.group(1)), quantity=session[element], session_key=element))

        return ret

    @staticmethod
    def clear_cart():
        pattern = re.compile("^{}$".format(Product.static_get_session_key("([0-9]+)")))
        for element in sorted(session.keys()):
            match = pattern.search(element)
            if match:
                del session[element]

    class Meta:
        verbose_name = "Produit"
        verbose_name_plural = "Produits"


class News(models.Model):
    title = models.CharField(max_length=120, blank=False)
    is_active = models.BooleanField(default=True)
    icon = models.ForeignKey(Icon, blank=False, default=get_comment_icon_id, limit_choices_to=all_but_forbidden_icon)
    content = models.TextField(blank=False)
    creation_date = models.DateField(auto_now_add=True)
    edition_date = models.DateField(auto_now=True)
    publication_date = models.DateTimeField(default=None, null=True, blank=True, unique=True)
    writer = models.ForeignKey(AgripoUser, limit_choices_to=Q(is_staff=True))

    def __str__(self):
        return "{id} : {title} ({pub_date})".format(
            id=self.pk, title=self.title, pub_date=self.publication_date)

    def save(self, *args, **kwargs):
        if not self.publication_date:
            self.publication_date = timezone.now()
        super().save(*args, **kwargs)

    def get_edition_date(self, no_edition_return=None):
        if self.creation_date == self.edition_date:
            return no_edition_return
        return self.edition_date

    def get_previous(self):
        return News.objects.filter(
            publication_date__lt=self.publication_date,
            is_active=True).order_by('-publication_date').first()

    def get_next(self):
        return News.objects.filter(
            publication_date__gt=self.publication_date,
            is_active=True).order_by('publication_date').first()

    @staticmethod
    def get_last():
        return News.objects.filter(
            publication_date__lt=timezone.now(),
            is_active=True).order_by('-publication_date')[0:3]

    class Meta:
        verbose_name = "Actualité"
        verbose_name_plural = "Actualités"


class Stock(models.Model):
    product = models.ForeignKey(Product, related_name="one_farmers_stock")
    farmer = models.ForeignKey(AgripoUser, limit_choices_to=Q(groups__name='farmers'))
    stock = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ("product", "farmer", )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._active_stock = self.stock

    def save(self):
        if not self.farmer.is_farmer():
            raise IntegrityError("Only farmers have stocks")

        self.set(self.stock)
        return super().save()

    def set(self, stock):
        """
        Updating the stock for this product in this farmer's account and on the product's general data
        :param stock: The new stock for this product and for this farmer
        :return: the Stock object
        """
        self.stock = stock
        self.product.stock -= self._active_stock
        self.product.stock += stock
        self.product.save()
        self._active_stock = stock
        return self


class DeliveryPoint(models.Model):
    name = models.CharField(max_length=64, unique=True)
    description = models.TextField(max_length=512)


class Delivery(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    delivery_point = models.ForeignKey(DeliveryPoint)


class Command(models.Model):
    """
    A command is the listing of the products for one customer in one delivery
    """
    customer = models.ForeignKey(AgripoUser)
    delivery = models.ForeignKey(Delivery)
    date = models.DateTimeField(auto_now_add=True)
    products = models.ManyToManyField(Product, through="CommandProduct")
    sent = models.BooleanField(default=False)

    def validate(self):
        # We get the products from the cart
        products = Product.static_get_cart_products()
        for product in products:
            the_product = Product.objects.get(id=product['id'])
            cp = CommandProduct(command=self, product=the_product, quantity=product['quantity'])
            cp.save()
            the_product.buy(product['quantity'])

        Product.clear_cart()

    def is_sent(self):
        return self.sent

    def send(self):
        self.sent = True
        self.save()
        return self


class CommandProduct(models.Model):
    command = models.ForeignKey(Command)
    product = models.ForeignKey(Product)
    quantity = models.PositiveSmallIntegerField()

    def clean(self):
        if self.quantity <= 0:
            raise ValidationError('Quantity must be bigger than 0')

        return super().clean()

    class Meta:
        unique_together = ('command', 'product', )
