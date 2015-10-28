# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0027_partner'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='partner',
            options={'verbose_name': 'Partenaire'},
        ),
        migrations.AddField(
            model_name='partner',
            name='logo',
            field=models.ImageField(upload_to='partners', verbose_name='Logo', default='default/not_found.jpg', help_text="Envoyez le logo du partenaire ici.<br />Il doit faire 150x150px. Si la largeur est différente de la hauteur, l'image apparaitra déformée."),
        ),
    ]
