# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import core.models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_add_icons'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='icon',
            field=models.ForeignKey(to='core.Icon', default=core.models.get_comment_icon_id),
        ),
    ]
