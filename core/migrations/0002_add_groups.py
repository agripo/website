# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations
from core.groups import GROUP_ADMIN, GROUP_MANAGERS


def create_initial_groups(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Group.objects.create(name=GROUP_ADMIN)
    Group.objects.create(name=GROUP_MANAGERS)


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_initial_groups)
    ]
