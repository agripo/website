from django.db import models
from django.db.models import Q
from django.utils import timezone

from core.models.general import Icon, get_comment_icon_id, all_but_forbidden_icon
from core.models.users import AgripoUser


class News(models.Model):
    on_change_delete_cache = True
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
            is_active=True).order_by('-publication_date')[0:2]

    class Meta:
        verbose_name = "Actualité"
        verbose_name_plural = "Actualités"
