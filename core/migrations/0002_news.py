# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('title', models.CharField(max_length=120)),
                ('is_active', models.BooleanField(default=True)),
                ('content', models.TextField()),
                ('creation_date', models.DateField(auto_now_add=True)),
                ('edition_date', models.DateField(auto_now=True)),
                ('publication_date', models.DateField(null=True, default=None, blank=True)),
                ('writer', models.ForeignKey(to='core.AgripoUser')),
            ],
        ),
    ]
