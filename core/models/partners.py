from ckeditor.fields import RichTextField
from django.conf import settings
from django.db import models


class Partner(models.Model):
    on_change_delete_cache = True
    name = models.CharField(
        max_length=128, unique=True, verbose_name="Nom du partenaire", help_text="Nom du partenaire",
        default=None)
    description = RichTextField(
        config_name='awesome_ckeditor', verbose_name="Description du partenaire",
        help_text="Contenu de la page d'accueil", default=None
    )
    website = models.URLField(verbose_name="Site internet du partenaire", default=None)
    logo = models.ImageField(
        upload_to='partners', blank=False, default=None, verbose_name="Logo (330x220 px)",
        help_text="Envoyez le logo du partenaire ici.<br />"
                  "<strong>Il doit faire 330x220px</strong> pour ne pas être déformé. "
    )

    def __str__(self):
        return self.name

    def logo_tag(self):
        return u'<img src="{}" style="width:150px;height:150px;"/>'.format(settings.MEDIA_URL + str(self.logo))

    logo_tag.short_description = 'Logo'
    logo_tag.allow_tags = True

    class Meta:
        verbose_name = "Partenaire"
