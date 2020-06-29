# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ckeditor.fields
import core.models.general


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0041_auto_20151214_1422'),
    ]

    operations = [
        migrations.CreateModel(
            name='Care',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('title', models.CharField(verbose_name='Titre', max_length=120)),
                ('is_active', models.BooleanField(default=True, verbose_name='Activer ?')),
                ('content', ckeditor.fields.RichTextField(help_text='Texte de la page santé/beauté', default=None, verbose_name='Contenu')),
                ('creation_date', models.DateField(verbose_name='Date de création', auto_now_add=True)),
                ('edition_date', models.DateField(verbose_name='Dernière modification', auto_now=True)),
                ('publication_date', models.DateTimeField(default=None, null=True, verbose_name='Date de publication', unique=True, blank=True)),
                ('icon', models.ForeignKey(default=core.models.general.get_comment_icon_id, to='core.Icon', verbose_name='Icone')),
                ('writer', models.ForeignKey(verbose_name='Rédacteur', to='core.AgripoUser')),
            ],
            options={
                'verbose_name_plural': 'Pages santé/beauté',
                'verbose_name': 'Page santé/beauté',
            },
        ),
    ]
