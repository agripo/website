# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0028_auto_20151026_0926'),
    ]

    operations = [
        migrations.AlterField(
            model_name='partner',
            name='logo',
            field=models.ImageField(default=None, upload_to='partners', verbose_name='Logo', help_text="Envoyez le logo du partenaire ici.<br />Il doit faire 150x150px. Si la largeur est différente de la hauteur, l'image apparaitra déformée."),
        ),
    ]
