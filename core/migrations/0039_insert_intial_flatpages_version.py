# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

from core.data.data_migrations import insert_flatpages_history, revert_insert_flatpages_history


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0038_flatpagehistory'),
    ]

    operations = [
        migrations.RunPython(insert_flatpages_history, reverse_code=revert_insert_flatpages_history)
    ]
