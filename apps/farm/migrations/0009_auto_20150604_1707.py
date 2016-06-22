# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('farm', '0008_auto_20150603_2150'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='farmprofile',
            name='city',
        ),
        migrations.RemoveField(
            model_name='farmprofile',
            name='region',
        ),
        migrations.AddField(
            model_name='farmprofile',
            name='location',
            field=models.CharField(max_length=200, null=True, blank=True),
            preserve_default=True,
        ),
    ]
