# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0009_auto_20150715_1656'),
    ]

    operations = [
        migrations.AddField(
            model_name='inivitationgroup',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 7, 15, 19, 12, 38, 650059, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
    ]
