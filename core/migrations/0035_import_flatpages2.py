# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import migrations

from core.data.data_migrations import insert_flatpages2_contents, revert_insert_flatpages_contents


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0034_auto_20151105_1018'),
    ]

    operations = [
        migrations.RunPython(insert_flatpages2_contents, reverse_code=revert_insert_flatpages_contents)
    ]
