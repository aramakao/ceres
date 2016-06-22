# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0004_auto_20150705_0526'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groupprofile',
            name='banner',
            field=models.ImageField(default=b'group_profile/group_banner.jpg', upload_to=b'group_profile'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='groupprofile',
            name='logo',
            field=models.ImageField(default=b'group_profile/group_logo.jpg', upload_to=b'group_profile'),
            preserve_default=True,
        ),
    ]
