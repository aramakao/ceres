# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0013_auto_20150710_0516'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stateuser',
            name='hearts',
        ),
        migrations.AlterField(
            model_name='profile',
            name='birth_day',
            field=models.DateField(default=datetime.datetime(2015, 7, 13, 15, 53, 23, 461641)),
            preserve_default=True,
        ),
    ]
