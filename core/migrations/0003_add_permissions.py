# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.contrib.auth.management import create_permissions

from core.models import make_permissions


def _make_permissions(apps, schema_editor):
    apps.models_module = True
    create_permissions(apps, verbosity=0)
    apps.models_module = None

    Group = apps.get_model("auth", "Group")
    Permission = apps.get_model("auth", "Permission")

    make_permissions(Group, Permission)


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_news'),
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.RunPython(_make_permissions, reverse_code=lambda *args, **kwargs: True)
    ]
