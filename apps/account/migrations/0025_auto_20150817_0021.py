# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0024_auto_20150804_2223'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='birth_day',
            field=models.DateField(default=datetime.datetime(2015, 8, 17, 0, 21, 34, 25476)),
            preserve_default=True,
        ),
    ]
