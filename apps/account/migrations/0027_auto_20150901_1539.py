# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0026_auto_20150901_1525'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='birth_day',
            field=models.DateField(default=datetime.datetime(2015, 9, 1, 15, 39, 18, 66270)),
            preserve_default=True,
        ),
    ]
