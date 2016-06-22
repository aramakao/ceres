# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0011_auto_20150819_0306'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedbackseller',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 19, 15, 7, 43, 7211, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
    ]
