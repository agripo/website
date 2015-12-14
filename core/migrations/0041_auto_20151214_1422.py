# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0040_auto_20151214_1223'),
    ]

    operations = [
        migrations.AlterField(
            model_name='partner',
            name='logo',
            field=models.ImageField(help_text='Envoyez le logo du partenaire ici.<br /><strong>Il doit faire 330x220px</strong> pour ne pas être déformé. ', default=None, upload_to='partners', verbose_name='Logo (330x220 px)'),
        ),
    ]
