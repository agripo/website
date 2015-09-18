from ckeditor.fields import RichTextField
from django.contrib.sessions.backends.db import SessionStore
from django.db import models
from solo.models import SingletonModel

from core.data.icons import UNUSED_ICON


SITECONF_DEFAULT_NEWS_COUNT = 9
session = SessionStore()


class Icon(models.Model):
    icon = models.CharField(max_length=28, unique=True)

    def __str__(self):
        return 'Icon {}'.format(self.icon)


def all_but_forbidden_icon():
    return ~models.Q(icon=UNUSED_ICON)


def get_comment_icon_id():
    return Icon.objects.get(icon="comment").pk


class SiteConfiguration(SingletonModel):
    site_title = models.CharField(
        max_length=255, default='Site title', verbose_name='Titre du site',
        help_text="Titre du site (dans l'onglet du navigateur)"
    )
    news_count = models.IntegerField(
        default=SITECONF_DEFAULT_NEWS_COUNT, verbose_name='Actualités',
        help_text="Nombre de news dans la liste des news"
    )
    homepage_content = RichTextField(
        config_name='awesome_ckeditor', verbose_name='Page d\'accueil',
        help_text="Contenu de la page d'accueil"
    )

    def __str__(self):
        return "Configuration générale"

    class Meta:
        verbose_name = "Configuration générale"
