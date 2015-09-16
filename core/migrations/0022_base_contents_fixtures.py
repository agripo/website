# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import migrations

from core.data.data_migrations import insert_flatpages_contents, revert_insert_flatpages_contents


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0021_stock_stock_and_delivery_done'),
        ('flatpages', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(insert_flatpages_contents, reverse_code=revert_insert_flatpages_contents)
    ]
