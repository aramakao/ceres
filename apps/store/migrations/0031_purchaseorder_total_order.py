# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0030_auto_20151210_2120'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchaseorder',
            name='total_order',
            field=models.FloatField(default=0),
        ),
    ]
