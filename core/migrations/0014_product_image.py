# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_stock'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='news',
            options={'verbose_name': 'Actualité', 'verbose_name_plural': 'Actualités'},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'verbose_name': 'Produit', 'verbose_name_plural': 'Produits'},
        ),
        migrations.AlterModelOptions(
            name='productcategory',
            options={'verbose_name': 'Catégorie', 'verbose_name_plural': 'Catégories'},
        ),
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.ImageField(null=True, default='default/not_found.jpg', help_text="Cette image représente le produit.<br />Elle doit faire 150x150px. Si la largeur est différente de la hauteur, l'image apparaitra déformée.", blank=True, upload_to='products', verbose_name='Image'),
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(to='core.ProductCategory', verbose_name='Catégorie', help_text='Catégorie sous laquelle apparaît ce produit.'),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(
                verbose_name='Nom', help_text='Nom affiché dans les fiches produits', unique=True, max_length=28),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.PositiveIntegerField(verbose_name='Prix unitaire'),
        ),
        migrations.AlterField(
            model_name='product',
            name='stock',
            field=models.PositiveIntegerField(
                default=0, help_text='Champ alimenté automatiquement en fonction des déclarations des agriculteurs.'),
        ),
    ]
