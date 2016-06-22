# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_auto_20150518_2157'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='web_site',
        ),
        migrations.AlterField(
            model_name='profile',
            name='birth_day',
            field=models.DateField(default=datetime.datetime(2015, 5, 27, 16, 9, 53, 663552)),
            preserve_default=True,
        ),
    ]
