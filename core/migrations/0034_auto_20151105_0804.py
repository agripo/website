# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0033_auto_20151030_1504'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='description',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='product',
            name='quantity_type',
            field=models.CharField(default='k', verbose_name='Unité', max_length=1, choices=[('k', 'le kg'), ('L', 'le litre'), ('U', "l'unité")]),
        ),
        migrations.AddField(
            model_name='product',
            name='scientific_name',
            field=models.CharField(default='', verbose_name='Nom scientifique', help_text='Nom affiché entre parenthèses dans les fiches produits', max_length=60),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(unique=True, verbose_name='Nom', help_text='Nom affiché dans les fiches produits', max_length=60),
        ),
        migrations.AlterField(
            model_name='productcategory',
            name='name',
            field=models.CharField(unique=True, verbose_name='Nom de la catégorie', max_length=60),
        ),
    ]
