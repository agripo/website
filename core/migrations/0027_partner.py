# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0026_auto_20151021_0848'),
    ]

    operations = [
        migrations.CreateModel(
            name='Partner',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=128, unique=True, help_text='Nom du partenaire', verbose_name='Nom du partenaire', default=None)),
                ('description', models.TextField(verbose_name='Description du partenaire', default=None)),
                ('website', models.URLField(verbose_name='Site internet du partenaire', default=None)),
            ],
        ),
    ]
