# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0023_add_delivery_related_permissions'),
    ]

    operations = [
        migrations.AddField(
            model_name='siteconfiguration',
            name='analytics_code',
            field=models.TextField(
                default='', verbose_name="Code d'Analytics", blank=True,
                help_text="Collez ici le code fourni qui doit être inséré dans toutes les pages sans l'éventuel "
                          "&lt;script&gt; du début, ni le &lt;/script&gt; de la fin."),
        ),
    ]
