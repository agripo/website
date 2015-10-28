# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0029_auto_20151028_1609'),
    ]

    operations = [
        migrations.AlterField(
            model_name='partner',
            name='description',
            field=ckeditor.fields.RichTextField(default=None, verbose_name='Description du partenaire', help_text="Contenu de la page d'accueil"),
        ),
    ]
