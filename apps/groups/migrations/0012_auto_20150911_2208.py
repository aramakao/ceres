# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0011_auto_20150826_0355'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='address',
            field=models.CharField(max_length=30, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='group',
            name='phone',
            field=models.CharField(max_length=20, blank=True),
            preserve_default=True,
        ),
    ]
