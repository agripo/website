# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0017_commands_stuff'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerData',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('phone', models.CharField(max_length=15)),
                ('customer', models.OneToOneField(to='core.AgripoUser')),
            ],
        ),
        migrations.AlterModelOptions(
            name='delivery',
            options={'verbose_name': 'Date de livraison', 'verbose_name_plural': 'Dates de livraison'},
        ),
        migrations.AlterModelOptions(
            name='deliverypoint',
            options={'verbose_name': 'Lieu de livraison', 'verbose_name_plural': 'Lieux de livraison'},
        ),
        migrations.AddField(
            model_name='command',
            name='message',
            field=models.TextField(max_length=256, null=True, verbose_name='Message', default='', help_text='Informations supplémentaires en rapport avec votre commande'),
        ),
        migrations.AddField(
            model_name='command',
            name='total',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='command',
            name='customer',
            field=models.ForeignKey(null=True, to='core.AgripoUser'),
        ),
        migrations.AlterField(
            model_name='command',
            name='delivery',
            field=models.ForeignKey(to='core.Delivery', verbose_name='Lieu de livraison', help_text='Sélectionnez le lieu de livraison'),
        ),
        migrations.AlterField(
            model_name='delivery',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
