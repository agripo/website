# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations
from core.icons import import_icons


def _add_icons(apps, schema_editor):
    Icon = apps.get_model("core", "Icon")
    import_icons(Icon)


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_icon'),
    ]

    operations = [
        migrations.RunPython(_add_icons, reverse_code=lambda *args, **kwargs: True)
    ]
