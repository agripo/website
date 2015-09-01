# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_add_farmers_group'),
    ]

    operations = [
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('stock', models.PositiveIntegerField(default=0)),
                ('farmer', models.ForeignKey(to='core.AgripoUser')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='stock',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='stock',
            name='product',
            field=models.ForeignKey(related_name='one_farmers_stock', to='core.Product'),
        ),
        migrations.AddField(
            model_name='product',
            name='farmers',
            field=models.ManyToManyField(to='core.AgripoUser', through='core.Stock'),
        ),
        migrations.AlterUniqueTogether(
            name='stock',
            unique_together=set([('product', 'farmer')]),
        ),
    ]
