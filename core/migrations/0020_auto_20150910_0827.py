# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0019_add_base_delivery_points'),
    ]

    operations = [
        migrations.CreateModel(
            name='FutureDelivery',
            fields=[
            ],
            options={
                'proxy': True,
                'verbose_name_plural': 'Livraisons futures/planifiées',
                'verbose_name': 'Livraison future/planifiée',
            },
            bases=('core.delivery',),
        ),
        migrations.CreateModel(
            name='PastDelivery',
            fields=[
            ],
            options={
                'proxy': True,
                'verbose_name_plural': 'Livraisons passées/effectuées',
                'verbose_name': 'Livraison passée/effectuée',
            },
            bases=('core.delivery',),
        ),
        migrations.AlterField(
            model_name='command',
            name='delivery',
            field=models.ForeignKey(to='core.Delivery', verbose_name='Lieu de livraison', related_name='commands', help_text='Sélectionnez le lieu de livraison'),
        ),
        migrations.AlterField(
            model_name='delivery',
            name='delivery_point',
            field=models.ForeignKey(to='core.DeliveryPoint', verbose_name='Lieu de livraison'),
        ),
    ]
