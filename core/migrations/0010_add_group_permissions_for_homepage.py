# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.contrib.auth.management import create_permissions


def make_permissions(apps, schema_editor):
    apps.models_module = True
    create_permissions(apps, verbosity=0)
    apps.models_module = None

    Group = apps.get_model("auth", "Group")
    Permission = apps.get_model("auth", "Permission")

    managers_group = Group.objects.get(name="managers")

    managers_group.permissions.add(
        Permission.objects.get(codename='change_siteconfiguration'),
    )


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_auto_20150821_1910'),
    ]

    operations = [
        migrations.RunPython(make_permissions, reverse_code=lambda *args, **kwargs: True)
    ]
