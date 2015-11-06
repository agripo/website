# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0035_import_flatpages2'),
    ]

    operations = [
        migrations.AddField(
            model_name='siteconfiguration',
            name='email',
            field=models.EmailField(default='contact@agripo.net', max_length=254, help_text="Cette adresse sera utilisée pour l'envoi d'emails de contact et de réservation", verbose_name='Adresse email de contact'),
        ),
    ]
