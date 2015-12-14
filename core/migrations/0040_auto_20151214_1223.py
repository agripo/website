# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0039_insert_intial_flatpages_version'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='flatpagehistory',
            options={'verbose_name_plural': 'Pages statiques - Anciennes versions', 'verbose_name': 'Pages statiques - Ancienne version'},
        ),
        migrations.AlterField(
            model_name='flatpagehistory',
            name='content',
            field=models.TextField(blank=True, verbose_name='Contenu enregistré'),
        ),
        migrations.AlterField(
            model_name='flatpagehistory',
            name='mtime',
            field=models.DateTimeField(db_index=True, auto_now_add=True, verbose_name="Date d'enregistrement"),
        ),
        migrations.AlterField(
            model_name='flatpagehistory',
            name='title',
            field=models.CharField(max_length=200, verbose_name='Titre de la page'),
        ),
        migrations.AlterField(
            model_name='flatpagehistory',
            name='url',
            field=models.CharField(db_index=True, max_length=100, verbose_name='Adresse de la page'),
        ),
    ]
