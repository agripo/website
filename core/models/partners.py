from django.conf import settings
from django.db import models


class Partner(models.Model):
    on_change_delete_cache = True
    name = models.CharField(
        max_length=128, unique=True, verbose_name="Nom du partenaire", help_text="Nom du partenaire",
        default=None)
    description = models.TextField(verbose_name="Description du partenaire", default=None)
    website = models.URLField(verbose_name="Site internet du partenaire", default=None)
    logo = models.ImageField(
        upload_to='partners', blank=False, null=False, default="default/not_found.jpg", verbose_name="Logo",
        help_text="Envoyez le logo du partenaire ici.<br />"
                  "Il doit faire 150x150px. "
                  "Si la largeur est différente de la hauteur, l'image apparaitra déformée."
    )

    def __str__(self):
        return self.name

    def logo_tag(self):
        return u'<img src="{}" style="width:150px;height:150px;"/>'.format(settings.MEDIA_URL + str(self.logo))

    logo_tag.short_description = 'Logo'
    logo_tag.allow_tags = True

    class Meta:
        verbose_name = "Partenaire"
