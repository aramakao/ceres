# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import autoslug.fields
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('farm', '0002_auto_20150512_1923'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='farm',
            name='web_site',
        ),
        migrations.AddField(
            model_name='farm',
            name='slug',
            field=autoslug.fields.AutoSlugField(default=datetime.datetime(2015, 5, 13, 15, 26, 12, 664803, tzinfo=utc), editable=False),
            preserve_default=False,
        ),
    ]
