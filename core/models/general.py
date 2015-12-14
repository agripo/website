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
    on_change_delete_cache = True
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
    email = models.EmailField(
        default="contact@agripo.net",
        verbose_name='Adresse email',
        help_text="Cette adresse sera utilisée pour l'envoi d'emails de réservation"
    )
    analytics_code = models.TextField(
        default="", verbose_name="Code d'Analytics", blank=True,
        help_text="Collez ici le code fourni qui doit être inséré dans toutes les pages sans l'"
                  "éventuel &lt;script&gt; du début, ni le &lt;/script&gt; de la fin."
    )

    def __str__(self):
        return "Configuration générale"

    class Meta:
        verbose_name = "Configuration générale"


class FlatPageHistory(models.Model):
    """
    Keep old contents from flatpages.
    """
    url = models.CharField(max_length=100, db_index=True, verbose_name="Adresse de la page")
    title = models.CharField(max_length=200, verbose_name="Titre de la page")
    content = models.TextField(blank=True, verbose_name="Contenu enregistré")
    mtime = models.DateTimeField(db_index=True, auto_now_add=True, verbose_name="Date d'enregistrement")

    @staticmethod
    def create_entry(flatpage):
        entry = FlatPageHistory()
        entry.url = flatpage.url
        entry.title = flatpage.title
        entry.content = flatpage.content
        entry.save()

    class Meta:
        verbose_name = "Pages statiques - Ancienne version"
        verbose_name_plural = "Pages statiques - Anciennes versions"
