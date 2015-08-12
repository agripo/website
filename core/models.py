from django.db import models
from django.contrib.auth.models import User, Group
from django.db.models import Q


class AgripoUser(User):

    def is_manager(self):
        return self.is_staff

    def add_to_managers(self):
        self.is_staff = True
        self.groups.add(Group.objects.get(name="managers"))
        self.save()
        return self

    def is_admin(self):
        return self.is_superuser

    def add_to_admins(self):
        self.is_superuser = True
        self.save()
        return self

    class Meta:
        proxy = True


class News(models.Model):
    title = models.CharField(max_length=120, blank=False)
    is_active = models.BooleanField(default=True)
    content = models.TextField(blank=False)
    creation_date = models.DateField(auto_now_add=True)
    edition_date = models.DateField(auto_now=True)
    publication_date = models.DateField(default=None, null=True, blank=True)
    writer = models.ForeignKey(AgripoUser, limit_choices_to=Q(is_staff=True))

    def __str__(self):
        return "{id} : {title} ({pub_date})".format(id=self.pk, title=self.title, pub_date=self.publication_date)

    def save(self, *args, **kwargs):
        if not self.publication_date:
            self.publication_date = self.creation_date
        super().save(*args, **kwargs)

    def get_edition_date(self, no_edition_return=None):
        if self.creation_date == self.edition_date:
            return no_edition_return
        return self.edition_date
