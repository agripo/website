# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations

from core.data.data_migrations import create_base_deliverypoints_and_deliveries


def _make_data_migration(apps, schema_editor):
    DeliveryPoint = apps.get_model("core", "DeliveryPoint")
    Delivery = apps.get_model("core", "Delivery")

    create_base_deliverypoints_and_deliveries(DeliveryPoint, Delivery)


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_other_command_stuffs_and_customerdata'),
    ]

    operations = [
        migrations.RunPython(_make_data_migration, reverse_code=lambda *args, **kwargs: True)
    ]
