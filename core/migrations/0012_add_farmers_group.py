# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.contrib.auth.management import create_permissions

from core.data_migrations import create_farmers_group


def _make_permissions(apps, schema_editor):
    apps.models_module = True
    create_permissions(apps, verbosity=0)
    apps.models_module = None

    Group = apps.get_model("auth", "Group")

    create_farmers_group(Group)


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_product_and_category'),
    ]

    operations = [
        migrations.RunPython(_make_permissions, reverse_code=lambda *args, **kwargs: True)
    ]
