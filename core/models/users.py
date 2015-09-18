from django.contrib.auth.models import User, Group
from django.db import IntegrityError, models


class AgripoUser(User):

    def is_farmer(self):
        return self.groups.filter(name="farmers").exists()

    def add_to_farmers(self):
        if not self.email:
            raise IntegrityError("The farmers must have a valid email set in their account")
        self.groups.add(Group.objects.get(name="farmers"))
        self.save()
        return self

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


class CustomerData(models.Model):
    customer = models.OneToOneField(AgripoUser)
    phone = models.CharField(max_length=15)
