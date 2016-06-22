# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0010_inivitationgroup_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='groupprofile',
            name='logo',
        ),
        migrations.AddField(
            model_name='group',
            name='logo',
            field=models.ImageField(default=b'group_profile/group_logo.jpg', upload_to=b'group_profile'),
            preserve_default=True,
        ),
    ]
