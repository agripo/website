# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0037_auto_20151106_1706'),
    ]

    operations = [
        migrations.CreateModel(
            name='FlatPageHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('url', models.CharField(verbose_name='URL', max_length=100, db_index=True)),
                ('title', models.CharField(max_length=200)),
                ('content', models.TextField(blank=True)),
                ('mtime', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Modified')),
            ],
        ),
    ]
