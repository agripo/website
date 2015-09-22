import re
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.db import models, IntegrityError
from django.db.models import Q
from django.utils import timezone

from core.exceptions import CantSetCartQuantityOnUnsavedProduct, AddedMoreToCartThanAvailable
from core.models.general import session
from core.models.users import AgripoUser


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
        max_length=28, blank=False, null=False, unique=True, verbose_name="Nom",
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
            if self._get_session_key() in session:
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
    def static_clear_cart():
        pattern = re.compile("^{}$".format(Product.static_get_session_key("([0-9]+)")))
        for element in sorted(session.keys()):
            match = pattern.search(element)
            if match:
                del session[element]

    class Meta:
        verbose_name = "Produit"
        verbose_name_plural = "Produits"


class Stock(models.Model):
    product = models.ForeignKey(Product, related_name="one_farmers_stock")
    farmer = models.ForeignKey(AgripoUser, limit_choices_to=Q(groups__name='farmers'))
    stock = models.PositiveIntegerField(default=0, verbose_name="Stock")

    class Meta:
        unique_together = ("product", "farmer", )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._active_stock = self.stock

    def save(self, **kwargs):
        if not self.farmer.is_farmer():
            raise IntegrityError("Only farmers have stocks")

        self.set(self.stock)
        return super().save(**kwargs)

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

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Lieu de livraison"
        verbose_name_plural = "Lieux de livraison"


class DeliveryQueryset(models.query.QuerySet):

    def available(self):
        return self.filter(done=False, date__gte=timezone.now()).order_by("date")

    def done(self):
        return self.filter(Q(done=True) | Q(date__lt=timezone.now()))


class DeliveryManager(models.Manager):

    def get_queryset(self):
        return DeliveryQueryset(self.model, using=self._db)

    def available(self):
        return self.get_queryset().available()

    def done(self):
        return self.get_queryset().done()


class Delivery(models.Model):
    date = models.DateTimeField(default=timezone.now)
    delivery_point = models.ForeignKey(DeliveryPoint, verbose_name="Lieu de livraison")
    done = models.BooleanField(default=False, verbose_name="Livraison effectuée")

    objects = DeliveryManager()

    def __str__(self):
        return "{} à {}".format(self.date.strftime("Le %d/%m à %Hh%M"), self.delivery_point.name)

    def details_link(self):
        count = self.commands.count()
        if not count:
            return "", 0

        return reverse("delivery_details", kwargs=dict(id=self.pk)), count

    def details(self):
        total = {}
        total_price = 0
        commands = self.commands.all()
        for command in commands:
            total_price += command.total
            commandproducts = command.commandproduct_set.all()
            for commandproduct in commandproducts:
                if commandproduct.product.pk not in total:
                    total[commandproduct.product.pk] = dict(quantity=0, product=commandproduct, total=0)

                total[commandproduct.product.pk]['quantity'] += commandproduct.quantity

        return {
            'total': total,
            'total_price': total_price,
            'commands': commands
        }

    def write_done(self, done=True):
        self.done = done
        self.save()
        return self

    class Meta:
        verbose_name = "Date de livraison"
        verbose_name_plural = "Dates de livraison"


class FutureDelivery(Delivery):

    class Meta:
        proxy = True
        verbose_name = "Livraison future/planifiée"
        verbose_name_plural = "Livraisons futures/planifiées"


class PastDelivery(Delivery):

    class Meta:
        proxy = True
        verbose_name = "Livraison passée/effectuée"
        verbose_name_plural = "Livraisons passées/effectuées"


class Command(models.Model):
    """
    A command is the listing of the products for one customer in one delivery
    """
    customer = models.ForeignKey(AgripoUser, null=True)
    delivery = models.ForeignKey(
        Delivery, verbose_name="Lieu de livraison", related_name="commands",
        help_text="Sélectionnez le lieu de livraison")
    date = models.DateTimeField(auto_now_add=True)
    products = models.ManyToManyField(Product, through="CommandProduct")
    sent = models.BooleanField(default=False)
    message = models.TextField(
        max_length=256, null=True, default="", verbose_name="Message",
        help_text="Informations supplémentaires en rapport avec votre commande")
    total = models.PositiveIntegerField(default=0)

    def __str__(self):
        return "{} : {}".format(self.date.strftime("Le %d/%m à %Hh%M"), self.customer)

    def validate(self):
        # We get the products from the cart
        products = Product.static_get_cart_products()
        for product in products:
            the_product = Product.objects.get(id=product['id'])
            cp = CommandProduct(command=self, product=the_product, quantity=product['quantity'])
            cp.save()
            the_product.buy(product['quantity'])
            self.total += product['quantity'] * the_product.price

        Product.static_clear_cart()
        self.save()

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

    def __str__(self):
        return "{} / {}".format(self.command, self.product)

    def clean(self):
        if self.quantity <= 0:
            raise ValidationError('Quantity must be bigger than 0')

        return super().clean()

    class Meta:
        unique_together = ('command', 'product', )
