# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0030_auto_20151028_1731'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='content',
            field=ckeditor.fields.RichTextField(default=None, verbose_name='Contenu', help_text="Texte de l'actualité"),
        ),
    ]
