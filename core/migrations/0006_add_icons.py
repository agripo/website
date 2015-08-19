# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations
from core import icons


def add_icons(apps, schema_editor):
    Icon = apps.get_model("core", "Icon")
    done = []

    for cat in icons:
        for icon in icons[cat]:
            if icon not in done:
                i = Icon(icon=icon)
                i.save()
                done.append(icon)

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_icon'),
    ]

    operations = [
        migrations.RunPython(add_icons, reverse_code=lambda *args, **kwargs: True)
    ]
