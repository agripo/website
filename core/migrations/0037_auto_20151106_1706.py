# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0036_siteconfiguration_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='siteconfiguration',
            name='email',
            field=models.EmailField(max_length=254, verbose_name='Adresse email', help_text="Cette adresse sera utilisée pour l'envoi d'emails de réservation", default='contact@agripo.net'),
        ),
    ]
