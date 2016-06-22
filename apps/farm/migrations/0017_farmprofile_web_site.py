# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('farm', '0016_auto_20150826_0045'),
    ]

    operations = [
        migrations.AddField(
            model_name='farmprofile',
            name='web_site',
            field=models.CharField(max_length=100, null=True, blank=True),
            preserve_default=True,
        ),
    ]
