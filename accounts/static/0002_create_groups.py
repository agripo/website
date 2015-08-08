# -*- coding: utf-8 -*-
from __future__ import unicode_literals
#from django.contrib.auth.models import Group

from django.db import migrations
from accounts.groups import GROUP_ADMIN, GROUP_MANAGERS


def create_initial_groups(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Group.objects.create(name=GROUP_ADMIN)
    Group.objects.create(name=GROUP_MANAGERS)
    print("Groups created : {}".format(Group.objects.all()))


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_initial_groups)
    ]
