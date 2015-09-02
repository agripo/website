from django.db import models
from django.contrib.auth.models import User, Group
from django.db.models import Q
from django.utils import timezone
from solo.models import SingletonModel
from ckeditor.fields import RichTextField


SITECONF_DEFAULT_NEWS_COUNT = 9


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


def get_comment_icon_id():
    return Icon.objects.get(icon="comment").pk


class News(models.Model):
    title = models.CharField(max_length=120, blank=False)
    is_active = models.BooleanField(default=True)
    icon = models.ForeignKey(Icon, blank=False, default=get_comment_icon_id)
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


def make_permissions(Group, Permission):
    managers_group = Group(name="managers")
    managers_group.save()
    managers_group.permissions.add(
        Permission.objects.get(codename='add_news'),
        Permission.objects.get(codename='change_news'),
        Permission.objects.get(codename='delete_news')
    )
