# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0024_siteconfiguration_analytics_code'),
    ]

    operations = [
        migrations.DeleteModel(
            name='FutureDelivery',
        ),
        migrations.DeleteModel(
            name='PastDelivery',
        ),
        migrations.AlterModelOptions(
            name='delivery',
            options={'verbose_name': 'Livraison', 'verbose_name_plural': 'Livraisons'},
        ),
    ]
