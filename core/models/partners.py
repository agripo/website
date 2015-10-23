from django.db import models


class Partner(models.Model):
    name = models.CharField(
        max_length=128, unique=True, verbose_name="Nom du partenaire", help_text="Nom du partenaire",
        default=None)
    description = models.TextField(verbose_name="Description du partenaire", default=None)
    website = models.URLField(verbose_name="Site internet du partenaire", default=None)

    def __str__(self):
        return self.name
