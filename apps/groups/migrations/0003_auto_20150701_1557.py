# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0002_groupmember'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='address',
            field=models.CharField(default=b'address', max_length=30),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='group',
            name='phone',
            field=models.CharField(default=b'000', max_length=20),
            preserve_default=True,
        ),
    ]
