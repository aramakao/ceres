# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('farm', '0015_auto_20150710_0343'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='farmprofile',
            name='logo',
        ),
        migrations.AddField(
            model_name='farm',
            name='logo',
            field=models.ImageField(default=b'farm_profile/farm_logo.jpg', upload_to=b'farm_profile'),
            preserve_default=True,
        ),
    ]
