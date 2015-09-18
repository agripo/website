# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations
from django.contrib.auth.management import create_permissions

from core.data.data_migrations import add_permissions_for_prod_stock_and_conf, save_site_configuration


def _make_permissions(apps, schema_editor):
    apps.models_module = True
    create_permissions(apps, verbosity=0)
    apps.models_module = None

    Group = apps.get_model("auth", "Group")
    Permission = apps.get_model("auth", "Permission")
    SiteConfiguration = apps.get_model("core", "SiteConfiguration")

    add_permissions_for_prod_stock_and_conf(Group, Permission)
    save_site_configuration(SiteConfiguration)


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_product_image'),
    ]

    operations = [
        migrations.RunPython(_make_permissions, reverse_code=lambda *args, **kwargs: True)
    ]
