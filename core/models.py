from django.db import models
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


class Product(models.Model):
    name = models.CharField(max_length=28, blank=False, null=False, unique=True)
    category = models.ForeignKey(ProductCategory, blank=False, null=False)
    price = models.PositiveIntegerField()

    def clean(self):
        if self.name == '':
            raise ValidationError('Empty product name')

        if self.price <= 0:
            raise ValidationError('Price should be bigger than zero')

    def _get_session_key(self):
        return "product_{}_quantity".format(self.pk)

    def set_cart_quantity(self, quantity):
        if not self.id:
            raise Exception("Adding to cart on an unsaved object")
        session[self._get_session_key()] = quantity

    def get_cart_quantity(self):
        if self._get_session_key() in session:
            return session[self._get_session_key()]
        return 0

    def stock(self):
        return 10


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
