# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_news_icon'),
    ]

    operations = [
        migrations.CreateModel(
            name='SiteConfiguration',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('site_title', models.CharField(max_length=255, help_text="Titre du site (dans l'onglet du navigateur)", default='Site title')),
                ('news_count', models.IntegerField(help_text='Nombre de news dans la liste des news', default=9)),
                ('homepage_content', models.TextField(help_text="Contenu de la page d'accueil")),
            ],
            options={
                'verbose_name': 'Configuration générale',
            },
        ),
    ]
