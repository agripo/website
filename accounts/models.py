from django.contrib.auth.models import Group, UserManager, PermissionsMixin
from django.db import models
from django.utils import timezone

from django.contrib.auth.models import AbstractBaseUser

class User(PermissionsMixin):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True, blank=False)
    last_login = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ('email',)

    objects = UserManager()

    def add_to_group(self, group_name):
        group = Group.objects.get(name=group_name)
        self.groups.add(group)
        self.save()
        pass
    
    def is_authenticated(self):
        return True

    def __str__(self):
        return self.email
