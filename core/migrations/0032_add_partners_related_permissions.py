# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations
from django.contrib.auth.management import create_permissions

from core.data.data_migrations import add_partners_related_permissions


def _make_permissions(apps, schema_editor):
    apps.models_module = True
    create_permissions(apps, verbosity=0)
    apps.models_module = None

    Group = apps.get_model("auth", "Group")
    Permission = apps.get_model("auth", "Permission")

    add_partners_related_permissions(Group, Permission)


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0031_auto_20151028_1744'),
    ]

    operations = [
        migrations.RunPython(_make_permissions, reverse_code=lambda *args, **kwargs: True)
    ]
