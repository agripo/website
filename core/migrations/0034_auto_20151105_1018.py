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
            field=models.TextField(blank=True, verbose_name='Description du produit', default=''),
        ),
        migrations.AddField(
            model_name='product',
            name='quantity_type',
            field=models.CharField(verbose_name='Unité', default='k', choices=[('k', 'le kg'), ('L', 'le litre'), ('U', "l'unité")], max_length=1),
        ),
        migrations.AddField(
            model_name='product',
            name='scientific_name',
            field=models.CharField(blank=True, verbose_name='Nom scientifique', default='', max_length=60, help_text='Nom affiché entre parenthèses dans les fiches produits'),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(verbose_name='Nom', unique=True, help_text='Nom affiché dans les fiches produits', max_length=60),
        ),
        migrations.AlterField(
            model_name='productcategory',
            name='name',
            field=models.CharField(verbose_name='Nom de la catégorie', max_length=60, unique=True),
        ),
    ]
