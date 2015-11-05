# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import core.models.general
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0032_add_partners_related_permissions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='command',
            name='customer',
            field=models.ForeignKey(null=True, verbose_name='Client', to='core.AgripoUser'),
        ),
        migrations.AlterField(
            model_name='command',
            name='date',
            field=models.DateTimeField(verbose_name='Date', auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='command',
            name='products',
            field=models.ManyToManyField(through='core.CommandProduct', verbose_name='Produits', to='core.Product'),
        ),
        migrations.AlterField(
            model_name='command',
            name='sent',
            field=models.BooleanField(verbose_name='Envoyée ?', default=False),
        ),
        migrations.AlterField(
            model_name='command',
            name='total',
            field=models.PositiveIntegerField(verbose_name='Total', default=0),
        ),
        migrations.AlterField(
            model_name='customerdata',
            name='customer',
            field=models.OneToOneField(verbose_name='Client', to='core.AgripoUser'),
        ),
        migrations.AlterField(
            model_name='customerdata',
            name='phone',
            field=models.CharField(max_length=15, verbose_name='Numéro de téléphone'),
        ),
        migrations.AlterField(
            model_name='delivery',
            name='date',
            field=models.DateTimeField(verbose_name='Date de la livraison', default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='deliverypoint',
            name='description',
            field=models.TextField(max_length=512, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='deliverypoint',
            name='name',
            field=models.CharField(unique=True, verbose_name='Nom', max_length=64),
        ),
        migrations.AlterField(
            model_name='news',
            name='creation_date',
            field=models.DateField(verbose_name='Date de création', auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='news',
            name='edition_date',
            field=models.DateField(verbose_name='Dernière modification', auto_now=True),
        ),
        migrations.AlterField(
            model_name='news',
            name='icon',
            field=models.ForeignKey(to='core.Icon', verbose_name='Icone', default=core.models.general.get_comment_icon_id),
        ),
        migrations.AlterField(
            model_name='news',
            name='is_active',
            field=models.BooleanField(verbose_name='Activer ?', default=True),
        ),
        migrations.AlterField(
            model_name='news',
            name='publication_date',
            field=models.DateTimeField(unique=True, verbose_name='Date de publication', default=None, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='news',
            name='title',
            field=models.CharField(max_length=120, verbose_name='Titre'),
        ),
        migrations.AlterField(
            model_name='news',
            name='writer',
            field=models.ForeignKey(verbose_name='Rédacteur', to='core.AgripoUser'),
        ),
        migrations.AlterField(
            model_name='product',
            name='bought',
            field=models.PositiveIntegerField(verbose_name='Acheté', help_text='Champ alimenté automatiquement en fonction des commandes passées', default=0),
        ),
        migrations.AlterField(
            model_name='product',
            name='farmers',
            field=models.ManyToManyField(through='core.Stock', verbose_name='Agriculteurs', to='core.AgripoUser'),
        ),
        migrations.AlterField(
            model_name='product',
            name='stock',
            field=models.PositiveIntegerField(verbose_name='Stock', help_text='Champ alimenté automatiquement en fonction des déclarations des agriculteurs.', default=0),
        ),
        migrations.AlterField(
            model_name='productcategory',
            name='name',
            field=models.CharField(unique=True, verbose_name='Nom de la catégorie', max_length=28),
        ),
        migrations.AlterField(
            model_name='stock',
            name='farmer',
            field=models.ForeignKey(verbose_name='Agriculteur', to='core.AgripoUser'),
        ),
        migrations.AlterField(
            model_name='stock',
            name='product',
            field=models.ForeignKey(verbose_name='Produit', to='core.Product', related_name='one_farmers_stock'),
        ),
    ]
