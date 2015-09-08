# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_force_product_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='Command',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('sent', models.BooleanField(default=False)),
                ('customer', models.ForeignKey(to='core.AgripoUser')),
            ],
        ),
        migrations.CreateModel(
            name='CommandProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('quantity', models.PositiveSmallIntegerField()),
                ('command', models.ForeignKey(to='core.Command')),
            ],
        ),
        migrations.CreateModel(
            name='Delivery',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='DeliveryPoint',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True)),
                ('description', models.TextField(max_length=512)),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='bought',
            field=models.PositiveIntegerField(default=0, help_text='Champ alimenté automatiquement en fonction des commandes passées'),
        ),
        migrations.AddField(
            model_name='delivery',
            name='delivery_point',
            field=models.ForeignKey(to='core.DeliveryPoint'),
        ),
        migrations.AddField(
            model_name='commandproduct',
            name='product',
            field=models.ForeignKey(to='core.Product'),
        ),
        migrations.AddField(
            model_name='command',
            name='delivery',
            field=models.ForeignKey(to='core.Delivery'),
        ),
        migrations.AddField(
            model_name='command',
            name='products',
            field=models.ManyToManyField(through='core.CommandProduct', to='core.Product'),
        ),
        migrations.AlterUniqueTogether(
            name='commandproduct',
            unique_together=set([('command', 'product')]),
        ),
    ]
