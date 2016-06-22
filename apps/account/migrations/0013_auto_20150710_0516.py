# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0012_auto_20150710_0511'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='birth_day',
            field=models.DateField(default=datetime.datetime(2015, 7, 10, 5, 16, 3, 365852)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='stateuser',
            name='text',
            field=models.TextField(max_length=200),
            preserve_default=True,
        ),
    ]
