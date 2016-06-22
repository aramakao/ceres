# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('farm', '0006_auto_20150601_2201'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='farmprofile',
            name='web_site2',
        ),
    ]
