# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_siteconfiguration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='siteconfiguration',
            name='homepage_content',
            field=ckeditor.fields.RichTextField(help_text="Contenu de la page d'accueil", verbose_name="Page d'accueil"),
        ),
        migrations.AlterField(
            model_name='siteconfiguration',
            name='news_count',
            field=models.IntegerField(help_text='Nombre de news dans la liste des news', verbose_name='Actualités', default=9),
        ),
        migrations.AlterField(
            model_name='siteconfiguration',
            name='site_title',
            field=models.CharField(help_text="Titre du site (dans l'onglet du navigateur)", max_length=255, verbose_name='Titre du site', default='Site title'),
        ),
    ]
