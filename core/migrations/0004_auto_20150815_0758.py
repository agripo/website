# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_add_permissions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='publication_date',
            field=models.DateTimeField(blank=True, default=None, null=True, unique=True),
        ),
    ]
