# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0023_auto_20150905_1639'),
    ]

    operations = [
        migrations.AddField(
            model_name='mailbox',
            name='reply',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
