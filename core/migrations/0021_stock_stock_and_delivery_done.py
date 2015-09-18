# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0020_auto_20150910_0827'),
    ]

    operations = [
        migrations.AddField(
            model_name='delivery',
            name='done',
            field=models.BooleanField(verbose_name='Livraison effectuée', default=False),
        ),
        migrations.AlterField(
            model_name='stock',
            name='stock',
            field=models.PositiveIntegerField(verbose_name='Stock', default=0),
        ),
    ]
